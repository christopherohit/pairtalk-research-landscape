# PairQuotient: Nuisance-Quotiented Renderer Feedback

## Status and claim boundary

PairQuotient is the current PairTalk architecture hypothesis. Its named
mechanism is a support-time quotient of personalized-renderer residuals: image
errors that can be explained by static appearance, registration, camera, or
other declared nuisance variables are removed before renderer feedback is
lifted into an audio-predictable motion correction.

This document specifies a testable architecture, not a novelty proof or a
major-conference-ready result. The local corpus search found no paper that
implements the same operational tuple

```text
same-utterance target support
+ learned image-feature nuisance quotient
+ signed personalized-renderer lift
+ correspondence-breaking certificate
+ exact fallback
```

but this is only a scoped negative search over the collected sources. The
architecture has synthetic tests and no accepted real-renderer episode yet.
It must not be described as improving 3DGS images, generalizing across people
or languages, or being ready for submission until those claims are measured.

## Why PairLift failed

PairLift showed that the frozen personalized EmoTaG renderer has a usable local
gradient: its linearized benefit correlates with actual per-frame image benefit
at `0.626`, with `96%` sign agreement. However, the aligned correction reduced
certificate MSE by only `4.477e-6`; shuffled correspondence achieved
`1.499e-5`, and a static support-mean lift achieved `3.185e-5`.[^1]

The failure is therefore structural rather than a request for another damping
sweep. The support residual contains motion error and nuisance error. If
appearance mismatch or registration bias lies in a renderer-sensitive image
direction, the ordinary Gauss-Newton inverse can encode it as motion even when
it is static or unrelated to speech. PairQuotient changes the optimization
space instead of tuning the same inverse.

## Core operator

Let the frozen audio-to-motion base predict `p_t`, and let the frozen
personalized renderer be `R_theta`. For a declared image feature `phi`, define

```text
e_t = phi(I_t) - phi(R_theta(p_t))       image-feature residual
J_t = d phi(R_theta(m)) / d m | p_t      renderer motion Jacobian
```

For support-only nuisance basis `U_n` with orthonormal columns, define the
quotient projector

```text
Q = I - U_n U_n^T.
```

PairQuotient forms its renderer terms after projecting both sides of the local
image model:

```text
e_t^Q = Q e_t
J_t^Q = Q J_t
G_t^Q = (J_t^Q)^T J_t^Q / K
g_t^Q = (J_t^Q)^T e_t^Q / K
d_t^Q = (G_t^Q / s + lambda I)^-1 (g_t^Q / s)
s = mean_t trace(G_t^Q) / D.
```

An audio/context predictor `h_S` is fitted only on paired support frames:

```text
h_S: x_t -> d_t^Q
m_hat_q = p_q + gamma h_S(x_q).
```

Ridge regression is the current falsifiable probe, not the contribution. A
future temporal network is warranted only if the quotient mechanism first
passes with the low-capacity predictor.

The implementation never materializes the `K x K` projector. It evaluates

```text
Q e = e - U_n(U_n^T e)
Q J = J - U_n(U_n^T J),
```

which costs `O(T K r + T K D)` storage/compute around the cached image feature,
Jacobian, and a small nuisance rank `r`.

## Estimating the nuisance quotient

The nuisance basis must be learned from the fit portion of target support only.
It cannot use certificate or query images.

### Declared temporal nuisance design

Construct a low-dimensional support design `Z` from variables that are not the
desired speech correction. Candidate columns are:

- a constant, handled explicitly by the temporal mean residual;
- low-order DCT components fixed before evaluation;
- tracked camera and head-pose variables;
- frame exposure or global color statistics;
- matte-boundary and torso-registration diagnostics.

The first real experiment should use only signals actually available for every
identity and freeze their definitions before certificate evaluation. Adding a
nuisance signal after inspecting certificate images invalidates that
certificate.

### Protecting speech variation

Let `X` contain the audio and frozen-base context that PairQuotient is allowed
to preserve. Residualize nuisance regressors against `X`:

```text
Z_perp = (I - P_X) Z.
```

Regress centered image residuals on `Z_perp`, producing `E_nuis`, then take its
leading right singular vectors together with the normalized support-mean
residual:

```text
E_nuis = Z_perp A
U_n = orth([mean(E), top_right_singular_vectors(E_nuis)]).
```

This construction is deliberately asymmetric. Audio/context is protected;
only the part of the declared nuisance design linearly independent of that
protected space is allowed to define the quotient. It cannot guarantee causal
separation, and nonlinear audio-nuisance dependence remains a risk. That risk
must be exposed by the ablations below rather than hidden by a broader claim.

## Mechanism-level invariants

The quotient has testable behavior independent of downstream metrics:

1. **Nuisance invariance.** For any frame coefficients `c_t` and `A_t`, adding
   `U_n c_t` to `e_t` or `U_n A_t` to `J_t` leaves `G_t^Q`, `g_t^Q`, and the
   quotient base loss unchanged.
2. **Coordinate invariance.** Replacing `U_n` by `U_n O` for an orthogonal
   matrix `O` leaves the operator unchanged. The subspace, not a chosen basis,
   is the object.
3. **PairLift containment.** With nuisance rank zero, PairQuotient exactly
   reduces to the unquotiented PairLift renderer terms.
4. **Speech protection.** If a candidate nuisance regressor lies entirely in
   the protected speech design, it contributes no nuisance basis direction.
5. **Exact abstention.** A rejected certificate returns a copy bitwise equal to
   the frozen base motion; an all-nuisance image error yields zero correction.

These properties are implemented in `probe/pairquotient.py` and tested in
`probe/test_pairquotient.py`.[^2]

## Architecture placement

```text
target support audio ---------------------> frozen base motion p_s
       |                                             |
       |                                             v
       |                                  frozen personalized renderer
       |                                             |
       |                         paired target image - rendered image
       |                                             |
       +--> protected speech design X                v
nuisance metadata Z --> residualize against X --> nuisance basis U_n
                                                     |
renderer Jacobian J_s --------------------------> quotient Q
                                                     |
                                                     v
                                      quotient Gauss-Newton lift d_s^Q
                                                     |
support audio/context --------------------------> predictor h_S
                                                     |
                                      support-only certificate
                                          /                  \
                                      reject                accept
                                        |                     |
query audio --> frozen base p_q --------+---- exact base      + correction
```

PairQuotient sits upstream of FLAME deformation and the unmodified EmoTaG
renderer. It does not replace EmoTaG's Gaussian representation, emotion path,
or five-second AdaIN personalization.[^3]

## Novelty boundary against nearby work

| Work | Occupied mechanism | Why it does not yet collapse PairQuotient |
|---|---|---|
| Learn2Talk | A 2D talking-face teacher and 3D sync expert supervise a 3D motion model | Teacher guidance is occupied; PairQuotient's proposed object is a target-support image-residual quotient measured through a frozen personalized renderer.[^4] |
| MANGO | Alternating motion and 3DGS-renderer training propagates photometric and perceptual loss into predicted FLAME motion | Renderer-supervised motion is occupied; MANGO jointly trains with image loss rather than estimating a support-only nuisance equivalence class and certifying a correction at adaptation time.[^5] |
| TexTalker | Joint audio-driven motion and dynamic wrinkle texture, with codebooks and pivot-based disentangled style injection | Appearance-motion/style factorization is occupied; it does not quotient frozen-renderer error modulo target nuisance before inverse lifting.[^6] |
| Follow Your Motion | A diffusion editing stage learns multi-scale rendered motion trajectories and dynamically reweights landmark attention | Post-render temporal correction is occupied; it does not infer target motion from quotient Gauss-Newton support feedback.[^7] |
| TT-SAC | Parameter-free test-time fixed-point update of conditioning through a generator-encoder loop | Generic feedback and test-time adaptation are occupied. Its Jacobian appears in fixed-point analysis; PairQuotient operationally measures `J^T Q J` and `J^T Q e` from paired target support.[^8] |
| SuperHead | Multi-view, multi-expression dynamics-aware 3D GAN inversion jointly optimizes appearance, depth, geometry, and rigged Gaussians | Dynamic inverse rendering is occupied; its goal is avatar super-resolution, not speech-protected nuisance removal for an audio-to-motion correction.[^9] |
| FG-3DGS | Frequency-aware regional Gaussian deformation and post-render alignment improve fine facial motion | Frequency/region separation is occupied. PairQuotient's low-frequency variables are nuisance candidates residualized against protected audio, not facial deformation branches.[^10] |
| PD-GS | Time-aligned phonemes and HuBERT features are fused by a learned gate for closure-level articulation | Explicit linguistic alignment and gating are occupied; PairQuotient neither introduces phoneme tokens nor claims a fusion gate.[^11] |
| 3DiFACE | Fully convolutional diffusion, one-minute speaking-style fine-tuning, and sparse keyframe guidance support diverse editable motion | Short-reference style personalization and sparse editing are occupied; PairQuotient uses five-second paired renderer error and no motion editing objective.[^12] |
| AnyTalk | Zero-audio character fine-tuning preserves a 2D video prior, followed by landmark-based optimization that uplifts video to blendshapes | 2D-to-3D uplift and zero-audio disentanglement are occupied; PairQuotient uses real same-utterance residuals and a renderer-Jacobian quotient.[^13] |
| PairLift | Signed personalized-renderer Gauss-Newton feedback | PairQuotient strictly contains PairLift at rank zero and changes the residual/Jacobian space before inversion; the distinction is valid only if nuisance controls improve correspondence specificity.[^1] |

The local full-text search over the downloaded corpus found no occurrence of a
renderer-residual quotient, an orthogonal-complement projector used this way,
or an equivalence-class formulation for personalized audio-driven 3DGS. Search
coverage is not exhaustive, and vocabulary mismatch can hide related work.

## Required controls

Every PairQuotient experiment must include equal-budget controls:

| Control | Falsified explanation |
|---|---|
| Frozen EmoTaG base | Any intervention is unnecessary or harmful |
| PairLift rank zero | The quotient adds nothing beyond signed renderer feedback |
| Static PairLift anchor | A generic motion offset explains image improvement |
| Shuffled correspondence | Marginal support statistics, not frame alignment, explain the result |
| Random equal-rank quotient | Removing arbitrary image dimensions is sufficient |
| Mean-only quotient | The result is merely temporal mean subtraction |
| Nuisance quotient without speech protection | Residualizing `Z` against audio is unnecessary |
| Nuisance-only predictor | Camera/exposure/pose, rather than speech, predicts the correction |
| Tracked-motion XLS-R residual | The new complete architecture must face the strongest current motion utility primitive |

An oracle basis constructed using certificate or query labels may be reported
only as a diagnostic upper bound and must never enter model selection.

## Frozen evaluation protocol

### Existing Obama episode

- Frames `100..124` have already been consumed once as PairLift's untouched
  certificate. They cannot certify PairQuotient.
- Frames `125..374` remain sealed and must not be inspected, tuned on, or
  rendered for PairQuotient unless a support-only certificate has already
  passed under a frozen protocol.
- Frames `0..99` may be used for exploratory engineering only, with that label.
  They cannot establish a confirmatory image claim.

### New confirmatory identity or scene

Use a new processed identity/scene with at least 125 support frames:

```text
75 fit | 25 selection | 25 untouched certificate | disjoint query
```

Before reading certificate results, freeze:

- image feature and masks;
- nuisance columns, protected design, rank grid, and random-control seeds;
- finite-difference epsilon and stability tolerance;
- damping, ridge, context, and correction-gain grids;
- shuffled temporal offsets and the acceptance thresholds.

Fit `U_n` only on the 75 fit frames. Hyperparameter selection may use the next
25 frames, but the quotient basis must not be re-estimated from them. Evaluate
the selected configuration once on the 25 certificate frames. Only an accepted
certificate authorizes a disjoint query render.

### Acceptance gate

The mechanism gate requires all of the following on the untouched support
certificate:

1. positive actual image-MSE benefit over the frozen base;
2. aligned benefit greater than unquotiented PairLift and the static anchor;
3. aligned benefit greater than the 90th percentile of equal-budget shuffled
   correspondence controls;
4. aligned benefit greater than the random equal-rank quotient;
5. LPIPS does not worsen and lip-region error does not regress;
6. the finite-difference response remains numerically stable;
7. rejection produces the exact frozen-base output.

These gates establish correspondence specificity for an episode; they do not
prove causality or cross-identity generalization.

## Conference-scale evidence plan

### Stage A: exploratory mechanism test

Use only non-sealed development frames to verify that the learned basis removes
more energy from static/registration diagnostics than from lip-region dynamic
residuals. Report removed residual energy and removed Jacobian energy
separately. A high removed-energy number is not automatically good: removing
most Jacobian energy can make the quotient unidentifiable.

### Stage B: new-identity renderer certificate

Reproduce the frozen renderer for a new identity, run the three-way support
split, and execute every control once. Failure closes the current nuisance
definition; it does not authorize tuning on the disjoint query.

### Stage C: multi-identity study

After one confirmatory mechanism pass, evaluate at least seven identities with
identity-level bootstrap intervals and an exact sign/randomization test. Keep
language and identity effects separate. Report every identity and every failed
episode.

### Stage D: perceptual and systems evidence

Report PSNR, SSIM, LPIPS, LMD, a declared audio-visual synchronization metric,
identity similarity, temporal failure rate, FPS, peak VRAM, and support-time
cost. A randomized human study is required for naturalness or preference
claims. The existing green-fringe EmoTaG outlier remains in failure analysis.

## Failure criteria

Close or revise PairQuotient if any of these occurs:

- random quotient matches the learned quotient;
- shuffled support matches aligned support;
- mean-only projection captures the entire gain;
- protected audio energy is systematically removed;
- quotient Jacobians become ill-conditioned or epsilon-unstable;
- motion improves only under the local quadratic but not the actual renderer;
- gains appear only after choosing nuisance variables using certificate images;
- the complete method loses decisively to the strict full-dimensional XLS-R
  residual on motion while failing to add image or perceptual benefit.

## Current implementation evidence

The synthetic core currently verifies zero-rank containment, nuisance and
basis-rotation invariance, recovery of static plus declared non-speech nuisance,
speech-design protection, removal of a static renderer bias that misleads raw
PairLift, zero correction for all-nuisance error, and bitwise exact fallback.[^2]

This is algebraic evidence only. No PairQuotient real-image result has been
generated, and no query render is authorized by this document.

## Exploratory Obama development run

To check whether the operator can train at all, a development-only run used
the already available neutral Obama frames `0..99`: 75 fit frames and 25
selection frames. The raw per-frame image residual/Jacobian terms were saved
once; no frame `100..374` entered fitting, selection, or any reported metric.

The best selection-set local-quadratic benefits were:

| Method | Local benefit |
|---|---:|
| PairQuotient aligned | `+2.685e-6` |
| PairLift rank-zero control | `+2.543e-6` |
| PairQuotient shuffled | `+4.958e-6` |
| PairQuotient random quotient | `+2.561e-6` |
| PairLift static anchor | `+1.067e-5` |

The exploratory mechanism gate therefore fails: shuffled correspondence and
the static anchor both beat aligned PairQuotient. The learned rank-4 quotient
removed `69.2%` of residual energy but only `0.116%` of Jacobian energy, so it
is removing mostly static image error rather than creating a correspondence-
specific renderer chart. The selection motion guard remained barely eligible
(`content_vs_teacher = 0.9504`), while aligned motion MSE was `0.3431` versus
`0.3415` for PairLift and `0.3499` for shuffled PairQuotient.

This is a useful training diagnosis, not a performance claim. Actual image
rendering of the 25 selection frames was attempted but could not run in the
current sandbox because CUDA is unavailable; the required unsandboxed approval
request also failed with `404 No active credentials`. No certificate or query
render was attempted as a workaround.

## Research snapshot

The refreshed metadata catalog, generated September 15, 2026, contains 949
deduplicated OpenAlex records, 147 arXiv records, 46 GitHub repositories, and
two Hugging Face dataset records across 41 paper, 15 code, and 17 dataset
queries, with zero collection errors.[^14] Twelve newly prioritized boundary
papers were downloaded and text-extracted successfully.[^15]

## Sources

[^1]: PairTalk workspace, “PairLift: Renderer-Error Lifting for Same-Utterance Personalization” and actual-renderer certificate, `research/PairLift_architecture_spec.md` and `research/PairLift_actual_renderer_obama.md`, accessed September 15, 2026.
[^2]: PairTalk workspace, PairQuotient implementation and synthetic invariants, `probe/pairquotient.py` and `probe/test_pairquotient.py`, accessed September 15, 2026.
[^3]: H. Xu et al., “[EmoTaG: Emotion-Aware Talking Head Synthesis on Gaussian Splatting with Few-Shot Personalization](https://arxiv.org/abs/2603.21332),” CVPR 2026, arXiv:2603.21332.
[^4]: Y. Zhuang et al., “[Learn2Talk: 3D Talking Face Learns from 2D Talking Face](https://arxiv.org/abs/2404.12888),” arXiv:2404.12888, 2024.
[^5]: L. Zhu et al., “[MANGO: Natural Multi-speaker 3D Talking Head Generation via 2D-Lifted Enhancement](https://arxiv.org/abs/2601.01749),” arXiv:2601.01749, 2026.
[^6]: X. Li et al., “[Towards High-fidelity 3D Talking Avatar with Personalized Dynamic Texture](https://arxiv.org/abs/2503.00495),” arXiv:2503.00495, 2025.
[^7]: H. Yang et al., “[Follow Your Motion: A Generic Temporal Consistency Portrait Editing Framework with Trajectory Guidance](https://arxiv.org/abs/2503.22225),” arXiv:2503.22225, 2025.
[^8]: Z. Zhang, L. Wang, Y. Zhang, and Y. Gao, “[Test-Time Self-Adaptive Conditioning for Stable Audio-Driven Talking-Head Generation](https://arxiv.org/abs/2605.25488),” arXiv:2605.25488, 2026.
[^9]: D.-J. Huang et al., “[From Blurry to Believable: Enhancing Low-quality Talking Heads with 3D Generative Priors](https://arxiv.org/abs/2602.06122),” arXiv:2602.06122, 2026.
[^10]: S. Xie et al., “[Toward Fine-Grained Facial Control in 3D Talking Head Generation](https://arxiv.org/abs/2602.09736),” arXiv:2602.09736, 2026.
[^11]: A. Fu and Y. Zhou, “[PD-GS: Phoneme-Driven 3DGS for Audio-Driven Talking Heads](https://arxiv.org/abs/2608.05218),” arXiv:2608.05218, 2026.
[^12]: B. Thambiraja et al., “[3DiFACE: Synthesizing and Editing Holistic 3D Facial Animation](https://arxiv.org/abs/2509.26233),” arXiv:2509.26233, 2025.
[^13]: K. Yun et al., “[AnyTalk: Speech Animation for Arbitrary Characters Leveraging a Video Generation Model](https://arxiv.org/abs/2608.16143),” arXiv:2608.16143, 2026.
[^14]: PairTalk workspace, generated catalog `research/catalog/landscape.json`, September 15, 2026.
[^15]: PairTalk workspace, nuisance-boundary download script and local primary-paper corpus, `research/fetch_nuisance_boundary_papers.sh` and `research/papers/text/`, September 15, 2026.
