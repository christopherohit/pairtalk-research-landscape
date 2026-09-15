# Personalized Audio-Driven 3D Gaussian Talking Heads

## Executive Findings

Personalized audio-driven talking heads are already a crowded research area.
Speaker/style conditioning, short-reference adaptation, low-rank fine-tuning,
generic residual branches, learned gates, few-shot neural rendering, and
five-second 3D Gaussian Splatting (3DGS) personalization all appear in prior
work. A credible new contribution cannot rest on any one of those labels.

The strongest reproducible signal in the current PairTalk workspace is a
narrower supervision primitive: run a frozen motion teacher on the target's
own support utterance, align the teacher motion with tracked real motion, and
learn the frame-specific discrepancy. Under a leakage-controlled protocol over
seven identities and three seeds, a full-dimensional XLS-R residual adapter
improves motion correlation by `+0.0126`, improves MSE by `+0.0033`, and loses
its gain when support correspondence is broken. Mean content remains `0.9515`,
although amplitude error worsens by `0.0126`.[^1]

This result establishes value in same-utterance correspondence for the tested
motion proxy. It does not establish novelty, image quality, multilingual
generalization, or conference readiness. A separate paired-versus-unpaired
control reaches positive identity-level improvements in distribution,
content, and correlation, but one identity falls below its content guard.[^2]

Several attempts to turn the primitive into a complete architecture have been
falsified. PairTangent identifies a correspondence-dependent differential
mechanism but does not match the strict residual's utility.[^3] PairCert's
strict support certificate accepts no aligned or shuffled episode and therefore
falls back everywhere.[^4] PairBank, PairField, PairRoute, PairSolve,
PairCouncil, and PairJudge each fail a declared mechanism or utility boundary.

PairScope was the first renderer-linked architecture candidate. It restricts target correction
to paired residual directions that are observable through a target-specific
renderer metric. Its first real-data test substitutes a generic FLAME surface
Jacobian Gram for the unavailable personalized renderer Jacobian. The proxy
improves FLAME-proxy MSE over paired low-rank by `+0.0028` and separates from
shuffled support by `+0.0052`; both comparisons have positive identity-bootstrap
intervals and exact sign-flip `p=0.03125`. However, PairScope remains below the
full-dimensional XLS-R residual by `0.0075` correlation, worsens motion MSE by
`0.0018`, and fails the per-identity content guard for Jae-in and May.[^5]

The resulting decision is conservative: keep the verified EmoTaG reproduction
as the renderer baseline; retain same-utterance XLS-R as the utility primitive;
and keep PairScope as a falsified first renderer-observability operator. A
subsequent one-identity actual EmoTaG pilot extracts a stable renderer Gram but
fails its untouched motion and image certificates, so the exact raw renderer
fallback is retained and no 3DGS improvement is claimed.[^5]

PairLift is the materially different signed-feedback follow-up. It computes a
per-frame damped Gauss-Newton target from the actual support-image residual and
personalized-renderer Jacobian. Aligned PairLift reduces untouched certificate
image MSE by `4.48e-6`, but shuffled correspondence reduces it by `1.50e-5` and
a static support-mean lift by `3.18e-5`. The gradient is numerically stable, so
this is evidence that static appearance/registration nuisance dominates the
audio-conditioned lift in the tested episode. PairLift also fails and returns
the exact raw query fallback.[^5]

## Evidence Map

The evidence is best read as a ladder. Each level permits a narrower statement
than the level above it.

| Level | Evidence currently available | Statement permitted |
|---|---|---|
| Literature | Primary papers, local full-text corpus, refreshed metadata catalog | Identifies occupied mechanisms and a scoped negative search result |
| Synthetic invariants | PairScope chart tests plus PairLift quadratic-loss, recovery, cached-lift, and zero-gradient tests | Establishes algebraic implementation properties |
| Motion-space proxy | Seven identities, three seeds, support-only selection, disjoint query | Supports same-utterance correspondence and proxy mechanism comparisons |
| Generic geometry proxy | Finite-difference FLAME surface Jacobian Gram | Supports local mesh-sensitivity comparisons only |
| Personalized renderer baseline | EmoTaG 20k adaptation and disjoint query render | Establishes a reproducible unmodified renderer baseline |
| Personalized renderer intervention | PairScope and PairLift completed for one Obama seed; both certificates failed | No adapter image-quality or query-gain claim is permitted |
| Human/perceptual evidence | Not completed | Required for naturalness or preference claims |

Motion correlation, motion MSE, and generic FLAME surface error must not be
presented as PSNR, LPIPS, LMD, lip readability, identity preservation, or human
preference. This separation is especially important because recent work argues
that conventional geometric or reconstruction measures do not fully capture
temporal synchronization, lip readability, and expressiveness.[^6]

## Research Landscape

### Occupied personalization mechanisms

VOCA demonstrates identity-conditioned speaking styles in audio-driven 3D face
animation and released a 12-speaker 4D dataset.[^7] Imitator adapts a
style-agnostic motion prior to a short target reference video.[^8] StyleTalk
extracts a speaking-style code from reference video and modulates its decoder,
while Mimic explicitly disentangles style and content in facial motion.[^9][^10]
These works make a generic reference style embedding or short-reference
personalization an unsafe novelty headline.

TalkLoRA adapts transformer-based speech-driven animation with low-rank
parameter updates.[^11] Therefore neither low rank nor parameter-efficient
adaptation is sufficient as a contribution. PairScope's retained rank is a
capacity control; its proposed distinction is that the output coordinates are
constructed from target paired residuals and renderer observability, not that
the predictor happens to be low rank.

Few-shot neural rendering is also occupied. Dynamic Facial Radiance Fields
condition a NeRF on appearance images for few-shot identity adaptation.[^12]
NeRFFaceSpeech combines a generative prior, NeRF, and audio-correlated
parametric-face dynamics for one-shot synthesis.[^13] These papers remove
“few-shot renderer” or “parametric face plus renderer” as standalone claims.

### Occupied 3DGS mechanisms

GaussianSpeech couples audio sequence modeling with a personalized 3D Gaussian
avatar and expression-dependent appearance, including perceptual and wrinkle
losses.[^14] EGSTalker combines efficient audio-spatial deformation with 3DGS
and reports three-to-five-minute personalization.[^15] Recent blendshape work
maps disentangled speech and expression components into FLAME parameters to
drive Gaussian avatars.[^16] These results occupy broad claims around
audio-conditioned Gaussians, efficient deformation, and FLAME-driven 3DGS.

EmoTaG is the closest renderer boundary. It uses a FLAME-Gaussian formulation,
a Gated Residual Motion Network, semantic emotion guidance, and five-second
AdaIN-based personalization.[^17] PairTalk must not rebrand a base/residual
branch, sigmoid gate, FLAME deformation, emotion guidance, or five-second
adaptation as new. A compatible intervention should remain upstream of FLAME
deformation and preserve the unmodified EmoTaG path as an exact fallback.

### Occupied residual and test-time mechanisms

SubtleTalk models weakly correlated upper-face and head motion through residual
flow matching, regional controls, prosody, and valence-arousal signals.[^18]
Consequently, “residual flow” and “weakly correlated dynamics” are occupied.
TT-SAC performs parameter-free generator/encoder feedback at inference to
refine conditioning without paired target supervision.[^19] Generic test-time
adaptation and self-consistency are therefore occupied too.

The local full-text search found no exact operational method that constructs a
target/avatar-specific correction coordinate chart from same-utterance paired
residuals and the personalized renderer's measured motion sensitivity. This is
a scoped negative search result, not proof of novelty. TT-SAC includes a
generator-feature Jacobian in theoretical fixed-point analysis, so any PairScope
claim must distinguish an operational support-time renderer metric from that
analysis.

### Search coverage

The refreshed catalog contains 949 OpenAlex records, 147 arXiv records, 46
GitHub repositories, and two Hugging Face dataset results across queries for
talking heads, Gaussian splatting, same-utterance supervision, correspondence,
retargeting, uncertainty, conformal prediction, and renderer-aware motion. No
collection errors were recorded.[^20] The two Hugging Face results are clearly
too sparse to count as exhaustive dataset coverage. Dataset discovery and
license review therefore remain partly manual.

## Data and Asset Readiness

### Local motion pilot

The local pilot contains 5-second support and disjoint 15-second query clips at
25 FPS for Obama, Obama2, Macron, Lieu, Jae-in, May, and Shaheen. Motion is
represented by 50 FLAME expression coordinates plus three jaw coordinates from
SMIRK. Frozen XLS-R features contain 25 hidden layers of width 1024. The
current clips have complete tracked-frame coverage, but language and identity
are confounded: Macron and Jae-in provide useful French and Korean stress tests,
while May's language metadata remains uncertain. These data cannot support a
general multilingual claim.

### Renderer assets

The EmoTaG release scene contains 375 processed neutral Obama frames, cameras,
motion arrays, audio features, identity features, emotion features, and Sapiens
depth/normal priors for the first 125 support frames. The local manifest records
52 of 52 expected release files with SHA256 values. The renderer environment
uses Python 3.9, PyTorch 2.1.1, CUDA 12.1, PyTorch3D 0.7.9, and compiled
Gaussian/hash-grid dependencies. Heavy import and CUDA checks pass 39 of 39
checks.[^21]

Optional preprocessing is not completely reproduced. DeepFace is intentionally
uninstalled because the release environment leaves it unpinned, and PyAudio
requires unavailable PortAudio headers. Neither is needed to adapt and render
the processed neutral scene, but a full preprocessing-reproduction claim would
require resolving them.

### Access and licensing

Local availability is not redistribution permission. FLOAT is marked for
non-commercial use in the current notes; FLAME model terms apply to geometric
assets; public video datasets may carry source-specific identity, voice, and
redistribution restrictions; and the EmoTaG checkpoint and processed scene
still need an explicit publication/redistribution audit.[^22]

| Asset | Research role | Current use boundary |
|---|---|---|
| Local target clips | Motion pilot | Internal research; source rights unresolved |
| SMIRK | 53-D tracking | Record checkpoint provenance and confidence |
| XLS-R | Frozen multilingual representation | Do not infer multilingual generalization from seven identities |
| FLAME 2020 and masks | Geometry proxy and motion coordinates | FLAME license applies |
| EmoTaG scene/checkpoint | Personalized renderer baseline | Public availability is not a redistribution grant |
| VOCASET/BIWI | Candidate 3D motion evaluation | Provider terms and identity restrictions apply |
| MEAD/HDTF | Emotion and talking-face candidates | Audit source and redistribution terms before use |
| Multiface | Multi-view neural rendering | Strong access/storage and non-commercial constraints |
| SubtleTalk-Face | Future upper-face pretraining candidate | Dataset release and license not verified locally |

## Reproducible EmoTaG Baseline

The unmodified neutral Obama EmoTaG adaptation uses 125 support frames and
20,000 iterations. It completed in about 55 minutes 31 seconds. Every support
frame was sampled exactly 160 times. The final checkpoint hashes are:

- `chkpnt_face_20000.pth`:
  `7c368e2f6934c49ac1674e8ed8d39e09f43a87661852a796851281ab21725367`;
- `chkpnt_face_latest.pth`:
  `2d2f7d3f0cafc43372659753ca49a0a0d73d55ed0f128cbce619f1d5cc5f7a57`.

The disjoint evaluation covers frames `125..374`: 250 frames at 512 by 512,
25 FPS, H.264, with zero failed renders and zero landmark failures. Results are
PSNR `21.002462`, SSIM `0.925434`, LPIPS `0.069348`, and LMD `1.976103`.[^23]
The last frame is a visible green-fringe outlier with PSNR `13.9447`. It remains
in the aggregate and must appear in failure analysis.

Three evaluation-path defects were fixed. A negative `N_views` value had been
interpreted as Python's `frames[:-1]` rather than “all frames.” A CUDA face mask
was passed directly to NumPy. An already normalized background plate was
divided by 255 a second time, producing an invalid low-quality composite. The
corrected plate render produces PSNR near 21 rather than the earlier invalid
value near 3. Training used explicit `N_views=125`, so the negative-slice fix
does not change the 20,000-iteration optimization.

This baseline demonstrates executable renderer adaptation and held-out
rendering. It is one neutral identity and contains a visible failure; it does
not establish a state-of-the-art reproduction.

## Same-Utterance Supervision

For support audio `a_s`, frozen teacher motion `p_s`, and tracked target motion
`y_s`, PairTalk first fits a low-capacity base calibrator `B_S` and computes

```text
E_s = y_s - B_S(p_s).
```

The supervision is unusual because the teacher is evaluated on the target's
own utterance. The real and teacher sequences therefore share time and speech
content. A competitor without correspondence can still use the target clip's
marginal statistics; the relevant control is not “no personalization” but an
unpaired distribution-matching baseline.

Across seven identities and three seeds, the paired calibrator improves over
unpaired marginal quantile transport by `+0.0481` distribution gap, `+0.0745`
content, and `+0.0303` correlation. The amplitude-error difference is
inconclusive. May's paired content is `0.9253`, below the `0.95` guard.[^2]
This supports correspondence value for one fixed calibrator, not architecture
novelty or renderer quality.

The stronger strict XLS-R residual freezes alignment, evaluation dimensions,
base state, feature normalization, PCA, hyperparameters, and residual gain
using four support seconds plus one validation second. It refits on all five
support seconds and evaluates once on the disjoint query. Aligned support gives
`+0.0126` correlation; shuffled support gives `-0.0025`. The identity-bootstrap
95% interval for aligned correlation gain is `[+0.0054,+0.0205]`, and the exact
identity sign-flip test gives `p=0.015625`.[^1]

This is the utility target a complete architecture must match. Improving a
specialized proxy while losing this motion signal is insufficient.

## PairScope Architecture

### Core operator

Let `R_theta(m)` be a frozen personalized renderer and `phi` a declared image
or renderer-feature map. At support frame `t`, compute

```text
J_t = d phi(R_theta(m_t)) / d m_t
G = mean_t J_t^T W_t J_t,
```

where `W_t` is non-negative. `G` measures first-order image-feature sensitivity
to motion. It may be rank deficient when motion directions are locally
unobservable.

For the support residual matrix `E`, define

```text
K = E G E^T.
```

If `(A, Lambda)` are its retained positive eigenpairs, construct

```text
U = E^T A Lambda^(-1/2).
```

Then `U^T G U = I` up to numerical tolerance. The small audio/context predictor
learns only renderer-observable coordinates:

```text
c_t = E_t G U
delta_q = U h(x_q)
m_hat_q = B_S(p_q) + gamma delta_q.
```

The implementation explicitly projects the basis into the range of `G`, which
suppresses arbitrary metric-null support noise. It retains constant observable
offsets instead of losing them through residual centering. If observable energy
is zero, it returns the base prediction exactly. Seven synthetic tests cover
Gram accumulation, PSD spectrum controls, orthogonality, constant offsets,
zero-energy fallback, and null-space suppression.[^5]

### Why the operator is narrower than a generic residual

The candidate contribution is not the ridge predictor, low rank, a gate, or a
FLAME basis. It is the target-specific coordinate chart defined jointly by:

1. same-utterance target residuals;
2. the personalized renderer's local response to motion;
3. support-only correspondence certification;
4. exact fallback when evidence is absent.

Removing any one of these elements collapses the distinction. `G=I` reduces
the chart to a motion-coordinate residual subspace. A random metric with the
same spectrum tests whether eigenvalue concentration alone explains the
result. Shuffled support tests correspondence. A full-dimensional XLS-R
residual tests whether restricting the output chart actually earns its place.

### Proxy implementation

The current proxy decodes the licensed generic FLAME model, samples five
support frames, applies central finite differences to all 53 expression/jaw
coordinates, and accumulates face-surface vertex Jacobian Grams. The matrix is
normalized to trace 53. It is generic geometry: it contains no target Gaussian
appearance, visibility, view, rasterization, or image-feature information.

The conditioning configuration is frozen from the strict full-dimensional
XLS-R comparator. PairScope searches ranks `{2,4,8,16}`, ridge strengths
`{1,10,100,1000}`, and residual scales `{0,0.25,0.5,0.75,1}` on the reserved
support second. A hard content rule requires validation content at least
`min(0.95, base_content)`, and scale zero is always an eligible exact fallback.

### Proxy results

| Comparison | Correlation improvement | Motion-MSE improvement | FLAME-proxy-MSE improvement | Proxy wins |
|---|---:|---:|---:|---:|
| vs paired low-rank | +0.0051 | +0.0015 | +0.0028 | 6/7 |
| vs full-D strict XLS-R | -0.0075 | -0.0018 | +0.0003 | 4/7 |
| vs shuffled correspondence | +0.0067 | +0.0034 | +0.0052 | 6/7 |
| vs identity metric | -0.0080 | -0.0019 | +0.0009 | 5/7 |
| vs random matched spectrum | +0.0004 | +0.0000 | +0.0024 | 7/7 |

The FLAME-proxy-MSE improvement over paired low-rank has a 95% identity
bootstrap interval `[+0.0004,+0.0058]`; aligned minus shuffled has
`[+0.0010,+0.0117]`. Both exact sign-flip tests give `p=0.03125`. Mean content
is `0.9543`, but Jae-in and May fall below `0.95`. PairScope selects scale zero
in six of 21 episodes.[^5]

The geometry orientation contains real proxy signal: it beats random-spectrum
orientation in all seven identity means on the proxy metric. Yet the mechanism
does not survive the full gate. Its correlation is lower than the identity
metric and full-dimensional residual, and query content is not uniformly safe.
The correct verdict is proxy mechanism **fail**, utility **fail**.

## Falsified Alternatives

| Architecture | Surviving observation | Closing result |
|---|---|---|
| PairTangent | Aligned-shuffled separation and OOD abstention | Only `+0.0038` correlation over base; MSE worsens `0.0049` |
| PairCert strict | Exact certificate/fallback implementation | `0/21` aligned and `0/21` shuffled accepts |
| PairBank | Some no-density correlation gain | Full certificate gains only `+0.0034`; null rejection weak |
| PairSolve | Stable closed-form subspace | `+0.0018` correlation, only `3/7` wins |
| PairField | Numerically stable retrieval | Essentially no correlation change; shuffled equivalent |
| PairRoute | Sparse coordinate routing | Discards most useful residual signal |
| PairCouncil | Strong proposal complementarity | Learned support weights lose to uniform fusion |
| PairJudge | Detects support correspondence | Loses decisively to uniform fusion |
| PairScope | Stable renderer observability extraction | Actual image MSE worsens; certificate rejects it |
| PairLift | Signed renderer gradient predicts local image reduction | Shuffled and static controls improve more than aligned audio |

These negative results are valuable. They show that support identifiability,
proposal diversity, a certificate, a low-rank subspace, or an OOD gate can each
exist without competitive utility. A publishable architecture must satisfy
mechanism and utility simultaneously.

## Required Next Experiment

The renderer extraction and certificate harness are now complete. Repeating a
PairScope rank/threshold sweep or a PairLift damping sweep on the same Obama
certificate would be adaptive reuse, not new evidence. The next operator must
remove static appearance/registration nuisance before fitting an audio-linked
correction, and it must be evaluated on a new untouched identity or split. The
250 Obama query frames remain sealed.

### Reusable renderer-term extraction

1. Load the verified neutral Obama EmoTaG 20k checkpoint and freeze Gaussian,
   camera, identity, FLAME shape, and motion-prior parameters.
2. Declare the renderer feature `phi` before evaluation. Candidate features are
   masked RGB, a frozen perceptual feature, and an explicit lip-region feature;
   their weights must be fixed from support only.
3. Check the finite-difference scale on a declared support subset before a new
   identity is certified; use autograd agreement when the renderer path permits
   it.
4. Store per-frame `G_t` and signed `g_t` terms without retaining a pixel-sized
   covariance. Save frame IDs, feature definition, normalization, and hashes.
5. Reject any future operator if its perturbation response is unstable or if
   its aligned gain does not exceed static and shuffled controls.

### Support protocol

A certificate and hyperparameter selection cannot reuse the same frames
without qualification. For a renderer-stage claim, use a three-way support
split such as 75 frames for fitting, 25 for selection, and 25 untouched frames
for certification. The final accepted model may then be refit on all 125
support frames. The 250 query frames remain metrics-only.

For each predeclared temporal shift, rerun the same selection search after
breaking support conditioning correspondence. Accept only if aligned rendered
benefit is positive and exceeds the 90th percentile shifted-null benefit. This
certificate is a conditional falsifier, not causal proof.

### Ablation matrix

| Variant | Question |
|---|---|
| EmoTaG 20k base | Reproducible unmodified renderer control |
| Full-D strict XLS-R | Strongest current same-utterance utility primitive |
| PairScope actual Gram | Archived sensitivity-only falsifier |
| PairLift signed gradient | Archived signed-feedback falsifier |
| PairLift static anchor | Does nuisance correction explain image gain? |
| PairLift shuffled support | Does temporal correspondence matter? |
| Future nuisance-orthogonal operator | Does dynamic audio-linked signal survive after static removal? |
| Any operator without certificate | Does the certificate prevent harmful episodes? |

### Metrics

Report PSNR, SSIM, LPIPS, LMD, lip-sync metrics, identity similarity, temporal
failure rate, FPS, peak VRAM, support preprocessing time, and per-identity
results. Include the existing green-fringe baseline outlier. Image metrics and
motion metrics should appear in separate tables. Human evaluation, if added,
must use randomized paired comparisons and report rater count, protocol, and
uncertainty.

### Decision gates

Before collecting query results, freeze thresholds for:

- positive image-space gain over EmoTaG base;
- positive image-space gain over full-D strict XLS-R;
- aligned improvement greater than shifted/null improvement;
- at least five of seven identity wins for the primary metric in a multi-person
  experiment;
- no mean content degradation and no systematic lip-sync regression;
- exact fallback under rejected certificate and zero observable energy;
- uncertainty intervals and an identity-level randomization test.

Failure of a primary gate should close the current formulation. It should not
trigger query-driven changes to feature masks, Jacobian epsilon, chart rank,
gain, or identity exclusions.

## Publication Assessment

The project has three credible assets: a reproducible personalized 3DGS
baseline, a leakage-controlled same-utterance supervision signal, and a
renderer-observable chart hypothesis with strong falsifiers. It does not yet
have a validated complete architecture.

The current evidence is below the standard needed for a major-conference claim
because:

- the best complete candidate does not match the strongest motion baseline;
- actual personalized-renderer interventions exist for only one identity and
  both fail their certificates;
- per-identity content safety fails;
- no image-space intervention is accepted for disjoint query rendering;
- dataset language, identity diversity, and licensing are insufficient for a
  broad generalization claim;
- no perceptual study or independent lip-sync study has been run.

A defensible eventual paper claim would be narrow: same-utterance paired
support can identify target-specific correction directions, and a personalized
renderer metric can restrict and certify those directions before inference.
That claim becomes credible only if actual image-space results beat both the
unmodified renderer and the full-dimensional paired residual under the frozen
controls.

## Recommendations

1. Keep `PairScope` and `PairLift` as documented negative results. PairLift's
   signed feedback improves raw MSE slightly but loses to both required nulls.
2. Do not tune either operator on the 250 query frames. Both support-only gates
   select the exact raw EmoTaG fallback.
3. Require a nuisance-orthogonal operator and a new untouched identity/split,
   not another rank, damping, or threshold sweep on Obama.
4. Reuse the verified per-frame renderer-term extractor, static control,
   shuffled control, and three-way certificate for any replacement hypothesis.
5. Expand identities and deconfound language before any multilingual claim.
6. Complete a written license/provenance matrix before packaging data,
   checkpoints, contact sheets, or rendered clips for release.

## Sources

[^1]: PairTalk workspace, “Strict Paired XLS-R Residual Control,” `probe/results/audio_residual_xlsr_strict_7id_control.md`, local reproducible artifact, accessed September 2026.
[^2]: PairTalk workspace, “Same-Utterance Paired Contribution Control,” `probe/results/contribution_7id_3seed.md`, local reproducible artifact, accessed September 2026.
[^3]: PairTalk workspace, “PairTangent Architecture and Pre-Registered Pilot,” `research/PairTangent_architecture_spec.md`, local artifact, accessed September 2026.
[^4]: PairTalk workspace, “PairCert Strict-Score Pilot,” `probe/results/paircert_strict_7id_control.md`, local reproducible artifact, accessed September 2026.
[^5]: PairTalk workspace, PairScope and PairLift renderer studies: `research/PairScope_architecture_spec.md`, `probe/results/pairscope_proxy_7id_3seed.md`, `research/PairScope_actual_renderer_obama.md`, `research/PairLift_architecture_spec.md`, and `research/PairLift_actual_renderer_obama.md`, local reproducible artifacts, accessed September 2026.
[^6]: C.-Y. Lee et al., “[Perceptually Accurate 3D Talking Head Generation: New Definitions, Speech-Mesh Representation, and Evaluation Metrics](https://arxiv.org/abs/2503.20308),” arXiv:2503.20308, 2025.
[^7]: D. Cudeiro, T. Bolkart, C. Laidlaw, A. Ranjan, and M. J. Black, “[Capture, Learning, and Synthesis of 3D Speaking Styles](https://arxiv.org/abs/1905.03079),” arXiv:1905.03079, 2019.
[^8]: B. Thambiraja, I. Habibie, S. Aliakbarian, D. Cosker, and C. Theobalt, “[Imitator: Personalized Speech-driven 3D Facial Animation](https://arxiv.org/abs/2301.00023),” arXiv:2301.00023, 2023.
[^9]: Y. Ma et al., “[StyleTalk: One-shot Talking Head Generation with Controllable Speaking Styles](https://arxiv.org/abs/2301.01081),” arXiv:2301.01081, 2023.
[^10]: H. Fu et al., “[Mimic: Speaking Style Disentanglement for Speech-Driven 3D Facial Animation](https://arxiv.org/abs/2312.10877),” arXiv:2312.10877, 2023.
[^11]: J. Saunders and V. P. Namboodiri, “[TalkLoRA: Low-Rank Adaptation for Speech-Driven Animation](https://arxiv.org/abs/2408.13714),” arXiv:2408.13714, 2024.
[^12]: S. Shen et al., “[Learning Dynamic Facial Radiance Fields for Few-Shot Talking Head Synthesis](https://arxiv.org/abs/2207.11770),” ECCV 2022, arXiv:2207.11770.
[^13]: G. Kim, K. Seo, S. Cha, and J. Noh, “[NeRFFaceSpeech: One-shot Audio-driven 3D Talking Head Synthesis via Generative Prior](https://arxiv.org/abs/2405.05749),” arXiv:2405.05749, 2024.
[^14]: S. Aneja et al., “[GaussianSpeech: Audio-Driven Gaussian Avatars](https://arxiv.org/abs/2411.18675),” arXiv:2411.18675, 2024.
[^15]: T. Zhu et al., “[EGSTalker: Real-Time Audio-Driven Talking Head Generation with Efficient Gaussian Deformation](https://arxiv.org/abs/2510.08587),” arXiv:2510.08587, 2025.
[^16]: Y. Mao et al., “[Learning Disentangled Speech- and Expression-Driven Blendshapes for 3D Talking Face Animation](https://arxiv.org/abs/2510.25234),” arXiv:2510.25234, 2025.
[^17]: H. Xu et al., “[EmoTaG: Emotion-Aware Talking Head Synthesis on Gaussian Splatting with Few-Shot Personalization](https://arxiv.org/abs/2603.21332),” CVPR 2026, arXiv:2603.21332.
[^18]: C. Ding et al., “[SubtleTalk: Generating Controllable Weakly-correlated Facial Dynamics for 3D Talking Heads via Residual Flow Matching](https://arxiv.org/abs/2608.06408),” ACM Multimedia 2026.
[^19]: Z. Zhang, L. Wang, Y. Zhang, and Y. Gao, “[Test-Time Self-Adaptive Conditioning for Stable Audio-Driven Talking-Head Generation](https://arxiv.org/abs/2605.25488),” arXiv:2605.25488, 2026.
[^20]: PairTalk workspace, `research/catalog/landscape.json`, generated September 15, 2026; 949 OpenAlex, 147 arXiv, 46 GitHub, two Hugging Face records, zero collection errors.
[^21]: PairTalk workspace, “EmoTaG Environment Status,” `research/EmoTaG_environment_status.md`, local environment and CUDA verification artifact, accessed September 2026.
[^22]: PairTalk workspace, “Dataset and Asset Access Matrix,” `research/dataset_access_matrix.md`, local access review, accessed September 2026.
[^23]: PairTalk workspace, EmoTaG disjoint query metrics at `/mnt/disk_2/shared/data/nhanht41-EmoTaG-output/neutral_Obama_baseline20k/test/metrics_baseline20k_test250/metrics.txt`, local reproducible artifact, accessed September 2026.
