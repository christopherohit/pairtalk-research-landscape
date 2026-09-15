# PairTalk Research Dossier

## Executive decision

No complete architecture currently passes both the mechanism and utility gates.
The strict same-utterance XLS-R residual remains the strongest validated
utility primitive:
aligned support improves correlation by `+0.0126`, while shuffled support gives
`-0.0025`. PairBank full, PairRoute, PairField, and PairSolve do not preserve
that signal strongly enough and are rejected as primary architectures.

The new **PairTangent** differential residual transport is the first named
candidate to pass the frozen *mechanism* gate: it improves correlation over its
anchor-only ablation by `+0.0038`, wins on `5/7` identity means, separates from
shuffled support by `+0.0154`, preserves mean content at `0.9581`, and drives
OOD trust to effectively zero. It does **not** pass the utility gate: the gain
over paired low-rank is only `+0.0038` (identity-bootstrap 95% CI
`[-0.0025,+0.0109]`) and MSE worsens by `0.0049`. PairTangent is therefore a
real, support-identifiable mechanism, but not yet a primary architecture and
must not be integrated into InsTaG/3DGS.

The current **PairCert strict-score** protocol requires an untouched support
certificate against equal-search-budget circular-shift nulls. Across seven
identities and three seeds it accepts `0/21` aligned episodes and `0/21`
externally shuffled episodes, so every correction falls back to paired
low-rank: correlation gain, MSE improvement, and aligned-minus-shuffled gain
are all `0.0000`, with mean content `0.9723`. Both the mechanism and utility
gates fail. PairCert is therefore blocked from 3DGS integration.

An older MSE-scored PairCert protocol is retained as historical evidence in
`probe/results/paircert_7id_control.{json,md}`. It accepted `6/21` aligned and
`0/21` shuffled episodes and reported `+0.0079` correlation and `+0.0030` MSE
improvement, but improved only `2/7` identity means. It must not be substituted
for the current strict-score result or reported as the current PairCert
verdict.

The newer **PairCouncil** diagnostic finds a large proposal-ensemble effect:
four FLOAT modes improve mean correlation over neutral by `+0.0784` on five
identities. However, uniform averaging and shuffled-support weights are both
slightly better than the learned support-conditioned convex weights. Static
PairCouncil is therefore also rejected. The query oracle establishes proposal
complementarity only; it does not validate support-conditioned arbitration.

The subsequent **PairJudge** implementation replaces individual proposal-cost
targets with entropy-regularized barycentric logit margins and passes all
synthetic recovery/invariance tests. A solver audit found the initial mirror
solver had not converged, so that artifact was retained as `pre_repair` and the
full protocol was rerun with a Newton-KKT oracle. The corrected real
5-identity x 3-support-block FLOAT pilot fails decisively: mean correlation is
`0.3441` versus `0.3807` for uniform fusion (`-0.0367`), MSE is worse by
`0.0415`, and 0/5 identities improve. It still beats support-audio-shuffled
fusion by `+0.0100` and mismatched-identity support by `+0.0061`, so support
correspondence is detectable but insufficient to beat the generic ensemble.
PairJudge is a documented falsifier, not a validated paper architecture.

The expensive 3DGS ablation remains blocked. PairTangent now supplies a
support-identifiable mechanism that survives aligned-vs-shuffled controls, but
its utility gate is still open; no candidate is integrated into InsTaG until
the utility claim is stronger or explicitly narrowed.

The new **PairScope** proposal defines a target-specific correction chart from
same-utterance residuals and renderer-visible motion directions. Its first
multi-identity pilot uses a generic FLAME surface finite-difference Gram as a
proxy. Across seven identities and three seeds, the proxy
improves FLAME-proxy MSE over paired low-rank by `+0.0028` and beats shuffled
correspondence by `+0.0052`, but Jae-in and May violate the per-identity
content guard and correlation remains `-0.0075` below full-D strict XLS-R.
PairScope therefore fails its post-hoc proxy and utility gates. A subsequent
single-identity actual EmoTaG renderer pilot extracts a stable Gram but also
fails its untouched image certificate: PSNR is `20.604175` versus `20.604496`
for raw EmoTaG and aligned image-MSE benefit is `-6.40e-7`. The query path is
the exact raw fallback. The equations and boundary are in
`research/PairScope_architecture_spec.md`; the renderer record is in
`research/PairScope_actual_renderer_obama.md`.

The materially different **PairLift** follow-up uses the signed personalized-
renderer image error, not observability alone. It lifts each support error into
a damped Gauss-Newton motion target and predicts that target from audio. On the
untouched Obama image certificate, aligned PairLift improves raw MSE by
`4.48e-6`, but shuffled correspondence improves by `1.50e-5` and a static
support-mean lift improves by `3.18e-5`. Both mechanism and image gates fail,
and the gated query is exactly raw EmoTaG. PairLift is a documented falsifier,
not evidence of image-quality improvement; see
`research/PairLift_architecture_spec.md` and
`research/PairLift_actual_renderer_obama.md`.

## Scope and evidence labels

- **Fact** means it is directly supported by a cited paper, model card, local file, or reproducible command output.
- **Measurement** means it is produced by the PairTalk probe protocol in this workspace.
- **Interpretation** means a research judgment from those facts; it is not a literature claim.
- **Proposal** means an architecture or experiment to implement next.

## Literature landscape

### Occupied ground

| Work | What it already contributes | Consequence for the paired adapter |
|---|---|---|
| Learn2Talk (2024) | Uses a 2D talking-face teacher to improve 3D motion and 3DGS synthesis.[^1] | “Use a teacher” is not new. The distinction must be target-own-audio paired supervision, not teacher distillation alone. |
| GaussianTalker / TalkingGaussian (2024) | Speaker-specific or structure-persistent 3DGS talking heads.[^2][^3] | A 3DGS talking-head backbone is not a contribution by itself. |
| TalkLoRA (2024) | Low-rank adaptation for speech-driven animation.[^4] | Calling a low-rank residual alone new is unsafe. The adapter must make same-utterance paired supervision and certification central. |
| VQTalker (2024) | Facial-motion tokenization for multilingual talking avatars.[^5] | “Multilingual” or discrete facial units alone are occupied. |
| DiffusionTalker (2025) | Personalizer-guided distillation and contrastive audio personalizer.[^6] | Generic personalizer/distillation language will be rejected as repackaging. |
| StyleSpeaker (2025) | Fine-grained style modeling from audio for 3D facial animation.[^7] | Audio style conditioning is occupied; the adapter needs paired target evidence and a measurable fallback guarantee. |
| MemoryTalker (ICCV 2025) | Stores and retrieves motion, then audio-guides stylization without requiring motion at inference.[^8] | A memory/retrieval story alone is not enough; the adapter must use teacher--real correspondence and not just a motion bank. |
| Polyglot (2026) | mHuBERT, Whisper, CLIP, and a reference-motion style embedding on PolySet/MultiTalk across 20 languages.[^9] | Multilingual style preservation is directly occupied. The adapter should claim paired teacher correction, not multilingual style embeddings. |
| EmoTaG (CVPR 2026) | Few-shot 3DGS personalization with a Gated Residual Motion Network.[^10] | “Gated residual” is occupied. Any gate here must be derived from support validation and OOD density, with no persistent speaker ID. |
| EmbedTalk (2026) | Replaces tri-plane representation with per-Gaussian embeddings.[^11] | A credible paper needs an equally crisp structural change; the adapter changes the personalization operator, not the Gaussian representation. |
| PD-GS (2026) | HuBERT plus time-aligned phonemes and a learned linguistic fusion gate for 3DGS.[^12] | Phoneme gating is occupied; do not present it as the new thing. |
| SDTalk / AvatarForcing (2026) | Structured motion fields and streaming/local-future dynamics.[^13][^14] | Temporal/world-model additions are likely incremental for this project; keep them as controls, not the headline. |

Additional adjacent work found in the refreshed catalog covers unseen-identity generalization (MGGTalk), multi-subject lip sync (GenSync), density control (PGSTalker), wobble suppression (GaussianHeadTalk), emotional/stylized control (ESGaussianFace, EmoZone-Talker, GaussianEmoTalker), single-image generalization (Splat-Portrait), and fine-grained regional facial control.[^29][^30][^31][^32][^33][^34][^35][^36][^37] None of the searched text exposes the exact same-utterance teacher--real support operator, but this negative search result is not proof of novelty.

### The defensible whitespace

The literature repeatedly supplies one of the following: a universal audio-to-motion prior, a reference style embedding, a memory, a generic residual gate, or a teacher. The probe isolates a narrower working hypothesis:

1. The teacher can be executed on the **target's own audio**.
2. Therefore the target's short support clip gives frame-aligned `(teacher motion, target motion)` without a new annotation or a second utterance.
3. A correction can be conditioned on the audio/teacher state while being supervised by the same-utterance residual.
4. A support-only validation and density signal can turn the correction off for shuffled or OOD support.

This combination is not a proof of novelty. It is the exact hypothesis that must be checked against the final versions of Learn2Talk, EmoTaG, Polyglot, MemoryTalker, and any concurrent 2026 submissions.

## Data inventory

### Local mounted data

The mounted InsTaG data root is `/mnt/disk_2/shared/data/nhanht41-InsTaG-data`. The current raw speakers are:

| Split | Identities | Role in PairTalk |
|---|---|---|
| Target/probe | Obama, Obama2, Lieu | English target folds; 5 s support and disjoint 15 s test. |
| Target/probe | Macron | French stress test; Whisper identified `fr=0.982910` in the earlier run. |
| Pretrain/extra | Jae-in, May, Shaheen | Additional held-out probes. Jae-in was recognized as Korean (`ko=0.906738`), Shaheen as English (`en=0.997559`), and May was recognized as Welsh with uncertain reliability (`cy=0.891113`); do not claim May is Welsh without manual verification. |
| Pretrain/extra | Obama1 | Fully clipped, tracked, and encoded with XLS-R; the base real/teacher tracks have `125/125` and `375/375` coverage. It has not been added to the five-identity proposal-bank control. |

All eight completed base-probe speakers have 5 s and 15 s clips, 25 FPS video,
16 kHz mono audio, and 100% SMIRK tracking coverage for the generated probe
clips. The five PairCouncil identities also have complete `auto`, `happy`, and
`sad` proposal tracks. The local mount does not contain a machine-readable
license manifest; treat it as research-only until the InsTaG dataset terms are
verified.

### Public data candidates

| Dataset | Useful signal | Access/license caution |
|---|---|---|
| PolySet / MultiTalk | Multilingual talking-head video and 3DMM expression supervision; Polyglot reports 20 languages and 420 hours for MultiTalk.[^9] | Request/release terms must be checked; do not redistribute clips without permission. |
| MEAD | Emotion, identity, and synchronized speech/video.[^15] | Research license and identity/voice restrictions apply. |
| VOCASET | 3D facial motion paired with speech.[^16] | Access is controlled by the dataset provider. |
| BIWI | 3D face tracking and speech/pose sequences.[^17] | Check academic-only terms and identity restrictions. |
| HDTF | High-definition talking-face videos with audio.[^18] | Verify redistribution and commercial-use terms. |
| VFHQ | High-quality face video for restoration/pretraining.[^19] | Useful for appearance, not a replacement for paired 3D motion labels. |
| Multiface | Multi-view face capture and neural rendering.[^20] | Strong privacy/access restrictions; likely too expensive for the first 25-week plan. |
| VoxCeleb2, LRS2/LRS3, MuAViC | Large-scale audiovisual speech and language diversity.[^21][^22][^23] | Speaker identity and redistribution terms must be respected; use for representation pretraining/evaluation, not casual rehosting. |
| RAVDESS, CREMA-D, GRID, TCD-TIMIT | Controlled emotion, phonetic, or audiovisual speech tests.[^24][^25][^26][^27] | Each has a separate license/consent policy; use only after a written matrix is completed. |

The automated catalog is in `research/catalog/landscape.json`, with CSV exports for OpenAlex, arXiv, GitHub, and Hugging Face. The catalog is a discovery aid, not a license decision.

## Measurements

### Protocol

- Fit on the first 5 seconds, reserve the last 1 second of that support for model selection, and evaluate on a disjoint 15-second clip from 10--25 seconds.
- The teacher is run on the target's own audio; real motion is tracked from the target video.
- The baseline is paired low-rank calibration with content and distribution losses.
- The proposed probe adds an audio-conditioned residual over that baseline; all test metrics are computed only after the support-only model selection.
- `corr_with_real` and MSE are motion-space diagnostics, not 3DGS image metrics.

### PairJudge barycentric proposal pilot

PairJudge uses local FLAME expression bases and anatomical vertex masks to
derive lips/eyes/face coefficient influence, while treating the three jaw
coordinates as a separate region. A shared pairwise ridge head predicts
centered barycentric logit margins from proposal-descriptor differences; it
does not use proposal IDs or query ground truth. Hyperparameters are selected
with three contiguous 25-frame support blocks and a 3-frame embargo.

| Condition | Corr | MSE | Amp. error |
|---|---:|---:|---:|
| PairJudge | 0.3441 | 0.39563 | 0.1680 |
| Uniform | 0.3807 | 0.35412 | 0.2720 |
| Shuffled support audio | 0.3340 | 0.40967 | 0.1545 |
| Mismatched identity | 0.3379 | 0.37582 | 0.1551 |

The identity-bootstrap 95% interval for correlation gain over uniform is
`[-0.0490, -0.0251]`. Accepted/fallback fractions are `0.9997/0.0003`; all
identical-proposal, permutation, convex-hull, mask, and no-query-GT invariants
pass. The frozen verdict is **FAIL** because PairJudge does not beat uniform,
does not improve MSE, and wins on 0/5 identities. Full corrected results are in
`probe/results/pairjudge_5id_3seed.json` and the architecture boundary is in
`research/PairJudge_architecture_spec.md`; the earlier non-converged result is
retained as `probe/results/pairjudge_5id_3seed_pre_repair.json`.

### Four-identity encoder control

The multilingual `facebook/wav2vec2-xls-r-300m` model was downloaded from its local Hugging Face model card and extracted as 25 hidden states of width 1024. The aligned XLS-R residual field was compared against the same paired low-rank baseline over three seeds.

| Condition | Corr improvement | MSE improvement | Distribution improvement | Mean content |
|---|---:|---:|---:|---:|
| English wav2vec2 | +0.0065 | +0.0032 | +0.0076 | 0.9598 |
| XLS-R aligned | **+0.0100** | **+0.0035** | +0.0028 | 0.9641 |
| XLS-R shuffled support | -0.0022 | -0.0027 | -0.0069 | 0.9769 |

XLS-R aligned improves correlation on all four identities and keeps mean content above 0.95. The shuffled control removes the correlation gain, which is evidence that frame correspondence—not just extra parameters—is doing the work. Full machine-readable results are in `probe/results/audio_residual_encoder_control.json` and `probe/results/audio_residual_encoder_control.md`.

### Seven-identity expansion

The three added speakers produce a more realistic stress test. Across three seeds, the aligned XLS-R probe has the following means over Obama, Obama2, Macron, Lieu, Jae-in, May, and Shaheen:

| Metric | Paired low-rank | XLS-R residual | Difference |
|---|---:|---:|---:|
| Correlation with real motion | 0.3259 (seed 1; 0.325--0.327 across seeds) | 0.3350 | about +0.008 |
| MSE | 0.3006 (seed 1) | 0.2991 | about -0.0015 |
| Content vs teacher | 0.9753 | 0.9561 | lower, but above the 0.95 guard |

The residual improves correlation on 6/7 identities in every seed. May selects residual scale 0 on all three seeds, a useful negative result: the system is allowed to refuse a correction. Jae-in and Macron are particularly important because they test Korean and French audio conditions; May remains language-uncertain.

The exact folds are `probe/results/audio_residual_xlsr_7id_seed0.json`, `probe/results/audio_residual_xlsr_7id_seed1.json`, and `probe/results/audio_residual_xlsr_7id_seed2.json`.

### Strict leakage-controlled expansion

The new runner `probe/run_audio_residual_strict_probe.py` fits alignment, metric dimensions, base calibration, audio normalization, PCA/scaler state, expert configuration, and residual gain using only the first four support seconds plus a reserved one-second validation segment. It refits once on all five support seconds and evaluates on a disjoint fifteen-second clip; no query-time correction is allowed.

Across seven identities and three seeds, aligned XLS-R residual gives `+0.0126` mean correlation, `+0.0033` MSE improvement, `+0.0051` distribution improvement, and mean content `0.9515`. Correlation improves on `6--7/7` identities per seed. The correspondence-breaking shuffled control gives `-0.0025` correlation and only `2--4/7` wins. The identity bootstrap 95% interval for aligned correlation improvement is `[+0.0054, +0.0205]`; the exact sign-flip test over identity means is `p=0.015625`.

Amplitude error worsens by `0.0126`, so the method must report this trade-off rather than hide it. Full details are in `probe/results/audio_residual_xlsr_strict_7id_control.md` and the six JSON runs with the `strict_7id` prefix.

### PairTangent differential residual pilot

PairTangent is a new motion-space mechanism, not a proposal selector. It fits
the finite-difference field
`[X_t, Delta X_t] -> Delta(R_t-P_t)` from the same-utterance support pair,
integrates it with a leaky anchor from the support residual mean, and applies
per-region FLAME coherence and query-density gates. The fixed anatomical
partition is derived from the local FLAME masks (lips, eyes, remaining face,
jaw); all leak, gain, and region choices are support-validation-only.

The strict seven-identity, three-seed pilot uses the same `4 s` selection +
`1 s` validation + disjoint `15 s` query protocol as the XLS-R residual. The
anchor-only ablation sets the leak to zero after the tangent field is fitted.

| Quantity | PairTangent result |
|---|---:|
| Correlation vs paired low-rank | `+0.0038` |
| Correlation vs anchor-only | `+0.0038` |
| Shuffled correlation vs paired low-rank | `-0.0116` |
| Aligned minus shuffled correlation | `+0.0154` |
| MSE improvement vs paired low-rank | `-0.0049` |
| Distribution improvement vs paired low-rank | `-0.0526` |
| Amplitude-error improvement | `+0.0185` |
| Mean content vs teacher | `0.9581` |
| In-domain / OOD trust | `0.0892 / 0.0000` |

Correlation improves on `5/7` identities versus low-rank and versus the
anchor-only ablation. The identity-bootstrap 95% interval for correlation gain
versus low-rank is `[-0.0025,+0.0109]`; the exact sign-flip test is `p=0.3594`.
The aligned-minus-shuffled interval is `[+0.0046,+0.0271]` with `p=0.0469`.
The mechanism gate is **PASS**, while the utility gate is **FAIL** because the
predeclared `+0.005` correlation and positive-MSE conditions are not met.
This is evidence for the paired differential mechanism, not evidence for a
better renderer or for conference-level readiness.

The implementation and pre-registration are in `probe/pair_tangent.py`,
`probe/run_pair_tangent_probe.py`, and
`research/PairTangent_architecture_spec.md`. Machine-readable results are in
`probe/results/pair_tangent_7id_control.json` and
`probe/results/pair_tangent_7id_control.md`.

### PairCert strict-score pilot

The current strict-score rerun applies the support certificate before any
query correction. It accepts no episode in either condition (`0/21` aligned,
`0/21` shuffled), yielding exactly zero aggregate correlation and MSE change
relative to paired low-rank. The aligned-minus-shuffled correlation interval is
`[0.0000,0.0000]`, and the identity sign-flip test is `p=1.0`. The mechanism
gate is **FAIL** because aligned support is not accepted more often than
shuffled support and produces no correspondence-specific gain. The utility
gate is also **FAIL** (`0/7` identity wins and no MSE improvement).

The authoritative current artifacts are
`probe/results/paircert_strict_7id_control.json` and
`probe/results/paircert_strict_7id_control.md`. The older MSE-scored artifacts
remain available under the prefix `paircert_7id`; they describe a different
certificate score and are historical, not contradictory reruns of the same
frozen test.

### PairScope generic-FLAME proxy pilot

PairScope builds a paired residual kernel `K = E G E^T`, where `G` is intended
to be a support-averaged target-renderer Jacobian Gram. The completed proxy
uses finite-difference generic FLAME surface displacement instead of a
personalized renderer and explicitly labels itself non-renderer evidence.
Selection follows the strict `4 s` fit + `1 s` validation + disjoint `15 s`
protocol, with a hard validation content guard and exact scale-zero fallback.

| Comparison | Corr. | Motion MSE | FLAME proxy MSE | Proxy wins |
|---|---:|---:|---:|---:|
| PairScope geometry vs paired low-rank | +0.0051 | +0.0015 | +0.0028 | 6/7 |
| PairScope geometry vs full-D XLS-R | -0.0075 | -0.0018 | +0.0003 | 4/7 |
| PairScope geometry vs shuffled support | +0.0067 | +0.0034 | +0.0052 | 6/7 |

Mean content is `0.9543`, but Jae-in and May are below `0.95` at the identity
level. This supports only a follow-up renderer-Jacobian experiment; it does
not establish PSNR, LPIPS, LMD, or image-quality gain. The machine-readable
runs are `probe/results/pairscope_proxy_7id_seed{0,1,2}.json`, and the
identity-level summary is `probe/results/pairscope_proxy_7id_3seed.md`.

### Current limitation

The result is still a motion-space proxy. It does not establish PSNR, LPIPS, LMD, Sync-C, or real-time throughput in InsTaG. The 3DGS experiment is a required gate, not an optional polish step.

### PairLift signed renderer-error pilot

PairLift replaces PairScope's support-averaged sensitivity chart with per-frame
signed renderer feedback. For support image residual `e_t` and motion Jacobian
`J_t`, it extracts `G_t = J_t^T J_t / K` and `g_t = J_t^T e_t / K`, then uses
`(G_t/s + lambda I)^-1(g_t/s)` as the audio-regression target. The operator is
implemented outside the dirty EmoTaG checkout and has an exact raw fallback.

On the 25-frame actual-renderer certificate, aligned PSNR/SSIM/LPIPS are
`20.606730/0.932187/0.068713` versus raw
`20.604496/0.932106/0.068744`. This small MSE gain does not pass the mechanism
gate: shuffled support and the static-anchor control improve MSE more. The
signed gradient is stable across two finite-difference epsilons (five-frame
mean cosine `0.985`), so the failure is attributed to correspondence
identification rather than a zero or random gradient. No query render is
authorized.

### PairBank strict falsifier

The actual `PairBank` implementation was run with the same leakage-controlled
`4 s` fit / `1 s` selection split, a segmented shifted-support counterfactual,
and a disjoint `15 s` query over seven identities and three seeds. The full
certificate/density configuration improved correlation by only `+0.0034` over
paired low-rank, with `5/7` identity wins and mean content `0.9704`. Its
identity bootstrap 95% interval was `[+0.0010,+0.0063]` and the exact sign-flip
test was `p=0.0625`. The aligned-minus-shuffled difference was `+0.0034`, below
the predeclared `+0.005` gate. The certificate accepted `12/21` aligned and
`9/21` shuffled episodes, so the null rejection is not yet selective enough.

The no-density ablation reached `+0.0085` correlation improvement, but reduced
mean content to `0.9581` and worsened amplitude error; this is a diagnostic
trade-off, not a pass for the full method. These results are in
`probe/results/pairbank_strict_7id_control.md` and
`probe/results/pairbank_strict_7id_control.json`. Do not start the expensive
3DGS ablation until the PairBank motion-space gate is repaired or explicitly
narrowed.

### Rejected architectural variants

**PairField retrieval.** The implementation in `probe/audio_paired_residual_field.py` was numerically stabilized and evaluated on seven identities. Mean correlation moved only `0.326994 -> 0.327029`, it won correlation on only `2/7` identities, and shuffled support was effectively equivalent. It is a documented falsifier, not a proposed method.

**PairSolve closed-form subspace solver.** The implementation in `probe/paired_residual_solver.py` passes five synthetic unit tests, but the strict seven-identity, three-seed protocol gives only `+0.0018` mean correlation, `3/7` wins, and mean content `0.9706`; the predeclared acceptance gate was `+0.005`, at least `5/7`, and content `>=0.95`. Its separately certified shuffled control still selects nonzero gains for Jae-in and Shaheen, so the certificate is not yet trustworthy.

The detailed machine-readable runs are `probe/results/pairsolve_strict_7id_seed0.json`, `probe/results/pairsolve_strict_7id_seed1.json`, and `probe/results/pairsolve_strict_7id_seed2.json`.

**PairRoute coordinate routing.** The cross-fitted router selected only `11.9%`
of score dimensions and reached `+0.00154` correlation over paired low-rank on
seed 0, with `4/7` identity wins. The corresponding shuffled run still reached
`+0.00055`; the ungated selected ridge retained `+0.01258`, showing that the
coordinate certificate discards most of the useful residual. PairRoute was
stopped after seed 0 rather than tuned on query.

**Static PairCouncil.** Four same-audio FLOAT modes provide strong generic
ensemble diversity: support convex averaging improves correlation over neutral
by `+0.0784` and MSE by `0.0524` on all `5/5` identities. The target-specific
claim fails, because support-learned weights underperform uniform averaging by
`0.0025` correlation and underperform correspondence-broken support weights by
`0.0016`. The council also worsens amplitude error and distribution gap. The
coordinate oracle reaches `0.7044` mean correlation, but it is non-deployable.
Full results are in `probe/results/teacher_council_5id_control.md` and
`probe/results/teacher_council_5id.json`.

## Archived architecture: PairBank

### One-sentence contribution

**PairBank replaces a fixed speaker/style code with a target-specific expert selected from a five-second teacher-on-own-audio pair, then applies the certified residual inside the 3DGS deformation field.**

### Computation

Let `P_s` be the direct-audio base or universal teacher motion on support, `R_s` the tracked target motion, and `A_s` the multilingual audio representation.

1. Compute residual support `E_s = R_s - P_s`.
2. Build a finite expert bank over multilingual encoder layer, temporal radius, regularization, optional teacher-state conditioning, and residual gain. Each expert is a small regularized audio-to-residual map with no persistent identity parameter.
3. Select the expert and gain on the reserved support second while preserving teacher velocity/content. A correspondence-breaking shifted-support counterfactual must not achieve the same validation gain; otherwise PairBank sets the gain to zero.
4. Refit only the selected expert on all five support seconds and estimate query density against its support feature manifold. Low-density queries fall back to the direct-audio base.
5. Produce `Y_q = B_q + g_q * Delta_q`; map `Delta_q` through a zero-initialized spatial injector and add it to InsTaG's audio latent before `sigma_net`.

The motion-space implementation is `probe/pairbank.py` with synthetic tests in `probe/test_pairbank.py`; the strict falsifier is `probe/run_audio_residual_strict_probe.py`. The clean InsTaG integration is isolated in the `feature/pairbank` worktree at `deep-research/InsTaG-pairbank`.

### Why this is not the rejected ideas

- It is not a per-dimension affine map; those maps cannot change correlation by algebraic invariance, as recorded in `probe/results/invariance.txt`.
- It is not a person-specific residual atlas; the atlas overfits support and fails held-out queries.
- It is not a generic gated residual copied from EmoTaG; expert/gain selection uses a correspondence-breaking certificate and the query gate has an explicit density fallback.
- It is not a generic multilingual style embedding copied from Polyglot; the target-specific basis is built from teacher--real correspondence for the same utterance.
- It is not a phoneme tokenization method copied from VQTalker or PD-GS.

### InsTaG integration point

The safest integration is before the deformation decoder, while preserving the existing universal motion route:

1. Keep InsTaG's existing `audio_net`, hash-grid encoders, and `sigma_net` as the base path.
2. Cache a 5 s target support pair once: target-audio teacher FLAME motion, target tracked FLAME motion, and the XLS-R layer bank.
3. Run PairBank support selection and write per-frame residual/trust arrays; no target embedding is stored.
4. Add a zero-initialized `PairBankSpatialInjector` that maps the residual to InsTaG's `audio_dim` latent and fuses `z = z_audio + lambda * z_pair`, where `lambda` is certificate- and density-gated.
5. Feed `z` into the existing per-Gaussian attention and `sigma_net`; do not post-process rendered Gaussians.
6. Keep a checkpoint-compatible flag off by default. A base InsTaG checkpoint must load without PairBank parameters.

The existing InsTaG worktree already contains a separate recurrent world-model experiment. PairBank must be evaluated with that flag off first; otherwise two new mechanisms become confounded. A separate clean worktree is used for this reason.

### Training losses

Use the ordinary InsTaG photometric/perceptual losses plus:

- `L_pair`: paired support motion reconstruction;
- `L_vel`: velocity and acceleration consistency;
- `L_content`: teacher ordering/rhythm preservation;
- `L_cert`: support-validation gain and content preservation;
- `L_gate`: sparsity and monotonic density calibration;
- `L_ood`: shuffled-support and scaled-audio negative episodes force fallback;
- `L_delta`: small residual norm, applied only when coherence is high.

Do not train the gate with held-out test motion. The 1 s support validation split is allowed; the 15 s test is metrics-only.

## Kill-switch and acceptance gates

### Cheapest motion-space falsifier

Run the same 7-identity, 3-seed protocol with:

1. paired low-rank;
2. paired audio residual with aligned support;
3. paired audio residual with support residuals shuffled;
4. paired residual with OOD audio/state scaling;
5. direct-audio-only fallback.

Before any 3DGS hour is spent, kill the architecture if any of these hold:

- aligned paired audio residual does not improve mean `corr_with_real` by at least `0.005` over paired low-rank;
- aligned paired audio residual does not improve at least 5/7 identities;
- mean `content_vs_teacher` falls below `0.95`;
- shuffled support retains more than half of the aligned correlation gain;
- OOD gate is not lower than in-domain gate;
- the correction is nonzero when support residual is zero.

The earlier strict ridge/XLS-R probe passes the motion-space gates, but the
actual PairBank certificate/expert implementation currently does not. PairBank
must be repaired or narrowed before any 3DGS rendering evidence is collected;
PairSolve is below the predeclared gate and should not replace it.

### First 3DGS ablation matrix

| Variant | Purpose |
|---|---|
| InsTaG base | Existing universal baseline. |
| Direct audio + paired low-rank adapter | Measures paired supervision without the new field. |
| Direct audio + paired residual, no gate | Tests whether the residual alone is useful. |
| Direct audio + paired residual + support gate | Proposed method. |
| Proposed + shuffled support | Negative control. |
| Proposed + English wav2vec vs XLS-R | Measures multilingual encoder contribution. |
| Proposed + world-model flag off/on | Separates the paired adapter from the existing InsTaG dynamics experiment. |

Report PSNR, LPIPS, LMD, AUE-L/FVMD if available, Sync-C/Sync-D, FPS, peak VRAM, support preprocessing time, and failure rate. Report every identity, not only the mean.

## 25-week execution plan

1. **Weeks 1--3:** finish dataset/license matrix; track Obama1; manually verify May language; add a second held-out clip where possible.
2. **Weeks 4--7:** train the paired adapter on public 3DMM data or the available InsTaG pretrain identities; run support-only gate calibration and shuffled/OOD controls.
3. **Weeks 8--11:** implement the zero-initialized InsTaG adapter and checkpoint compatibility tests.
4. **Weeks 12--16:** train base, paired-only, ungated, and gated 3DGS variants on two RTX 4090s; freeze all evaluation protocols before test runs.
5. **Weeks 17--20:** cross-language and cross-identity evaluation, user study, throughput/VRAM, and failure analysis.
6. **Weeks 21--23:** final novelty search, licensing audit, ablations, and reproducibility package.
7. **Weeks 24--25:** paper figures, supplementary, model card, and submission.

## Decision

Archive **PairBank**, **PairRoute**, **PairField**, **PairSolve**, static
**PairCouncil**, and current strict-score **PairCert** as falsified primary
architectures. Retain strict paired XLS-R as the strongest utility primitive
and **PairTangent** as a mechanism-pass / utility-fail candidate. Retain
**PairScope** as a documented negative renderer-observability result: both its
generic-FLAME proxy and first actual EmoTaG image certificate fail. Retain
**PairLift** as the signed-renderer-feedback falsifier: its aligned correction
reduces image MSE but loses to shuffled and static controls. Do not start
another PairTalk 3DGS ablation until a materially different mechanism passes
the utility gate (or a new
experiment explicitly narrows the claim), beats shuffled and
mismatched-support controls under a frozen support-only protocol, and has an
independent lip-sync measurement. The unmodified EmoTaG 20k baseline is
complete and does not count as PairTalk integration.

## Sources

[^1]: Y. Zhuang et al., “Learn2Talk: 3D Talking Face Learns from 2D Talking Face,” arXiv:2404.12888, 2024. https://arxiv.org/abs/2404.12888
[^2]: H. Yu et al., “GaussianTalker: Speaker-specific Talking Head Synthesis via 3D Gaussian Splatting,” arXiv:2404.14037, 2024. https://arxiv.org/abs/2404.14037
[^3]: J. Li et al., “TalkingGaussian: Structure-Persistent 3D Talking Head Synthesis via Gaussian Splatting,” arXiv:2404.15264, 2024. https://arxiv.org/abs/2404.15264
[^4]: J. Saunders and V. P. Namboodiri, “TalkLoRA: Low-Rank Adaptation for Speech-Driven Animation,” arXiv:2408.13714, 2024. https://arxiv.org/abs/2408.13714
[^5]: T. Liu et al., “VQTalker: Towards Multilingual Talking Avatars through Facial Motion Tokenization,” arXiv:2412.09892, 2024. https://arxiv.org/abs/2412.09892
[^6]: P. Chen et al., “DiffusionTalker: Efficient and Compact Speech-Driven 3D Talking Head via Personalizer-Guided Distillation,” arXiv:2503.18159, 2025. https://arxiv.org/abs/2503.18159
[^7]: A. Yang et al., “StyleSpeaker: Audio-Enhanced Fine-Grained Style Modeling for Speech-Driven 3D Facial Animation,” arXiv:2503.09852, 2025. https://arxiv.org/abs/2503.09852
[^8]: H. K. Kim et al., “MemoryTalker: Personalized Speech-Driven 3D Facial Animation via Audio-Guided Stylization,” arXiv:2507.20562, 2025. https://arxiv.org/abs/2507.20562
[^9]: F. Nocentini et al., “Polyglot: Multilingual Style Preserving Speech-Driven Facial Animation,” arXiv:2604.16108, 2026. https://arxiv.org/abs/2604.16108; project page: https://fedenoce.github.io/polyglot/
[^10]: H. Xu et al., “EmoTaG: Emotion-Aware Talking Head Synthesis on Gaussian Splatting with Few-Shot Personalization,” arXiv:2603.21332, 2026. https://arxiv.org/abs/2603.21332
[^11]: A. Saggar et al., “EmbedTalk: Talking Head Synthesis using Gaussian Embeddings,” arXiv:2603.07604, 2026. https://arxiv.org/abs/2603.07604
[^12]: A. Fu and Y. Zhou, “PD-GS: Phoneme-Driven 3DGS for Audio-Driven Talking Heads,” arXiv:2608.05218, 2026. https://arxiv.org/abs/2608.05218
[^13]: P. Jia et al., “SDTalk: Structured Facial Priors and Dual-Branch Motion Fields for Generalizable Gaussian Talking Head Synthesis,” arXiv:2605.09956, 2026. https://arxiv.org/abs/2605.09956
[^14]: L. Cui et al., “AvatarForcing: One-Step Streaming Talking Avatars via Local-Future Sliding-Window Denoising,” arXiv:2603.14331, 2026. https://arxiv.org/abs/2603.14331
[^15]: W. Wang et al., “MEAD: A Large-scale Audio-visual Dataset for Emotional Talking-face Generation,” official repository, https://github.com/uniBruce/Mead
[^16]: MPI-IS, “VOCASET / VOCA: Voice Operated Character Animation,” https://voca.is.tue.mpg.de/
[^17]: ETH Zurich, “BIWI 3D Audiovisual Corpus,” https://data.vision.ee.ethz.ch/cvl/datasets/
[^18]: Z. Zhang et al., “HDTF: High-definition Talking Face Dataset,” official repository, https://github.com/MRzzm/HDTF
[^19]: L. Xie et al., “VFHQ: A Dataset for Video Face Super-Resolution,” https://liangbinxie.github.io/projects/vfhq/
[^20]: J. W. Li et al., “MultiFace: A Dataset for Neural Face Rendering,” official repository, https://github.com/facebookresearch/multiface
[^21]: J. S. Chung et al., VoxCeleb2, https://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox2.html
[^22]: Meta AI, “MuAViC,” official repository, https://github.com/facebookresearch/muavic
[^23]: T. Afouras et al., LRS2/LRS3, https://www.robots.ox.ac.uk/~vgg/data/lip_reading/
[^24]: S. Livingstone and F. Russo, RAVDESS, https://zenodo.org/record/1188976
[^25]: H. Cao et al., CREMA-D, https://github.com/CheyneyComputerScience/CREMA-D
[^26]: M. Cooke et al., GRID Corpus, https://spandh.dcs.shef.ac.uk/gridcorpus/
[^27]: N. Harte and E. Gillen, “TCD-TIMIT,” Trinity College Dublin resource page, https://www.tcd.ie/scss/Sigmedia/Resources/TCD-TIMIT/
[^28]: Meta AI, “facebook/wav2vec2-xls-r-300m,” Hugging Face model card, https://huggingface.co/facebook/wav2vec2-xls-r-300m
[^29]: S. Gong et al., “Monocular and Generalizable Gaussian Talking Head Animation,” arXiv:2504.00665, 2025. https://arxiv.org/abs/2504.00665
[^30]: A. Agarwal et al., “GenSync: A Generalized Talking Head Framework for Audio-driven Multi-Subject Lip-Sync using 3D Gaussian Splatting,” arXiv:2505.01928, 2025. https://arxiv.org/abs/2505.01928
[^31]: T. Zhu et al., “PGSTalker: Real-Time Audio-Driven Talking Head Generation via 3D Gaussian Splatting with Pixel-Aware Density Control,” arXiv:2509.16922, 2025. https://arxiv.org/abs/2509.16922
[^32]: M. Agarwal et al., “GaussianHeadTalk: Wobble-Free 3D Talking Heads with Audio Driven Gaussian Splatting,” arXiv:2512.10939, 2025. https://arxiv.org/abs/2512.10939
[^33]: C. Ma et al., “ESGaussianFace: Emotional and Stylized Audio-Driven Facial Animation via 3D Gaussian Splatting,” arXiv:2601.01847, 2026. https://arxiv.org/abs/2601.01847
[^34]: T. Shi et al., “Splat-Portrait: Generalizing Talking Heads with Gaussian Splatting,” arXiv:2601.18633, 2026. https://arxiv.org/abs/2601.18633
[^35]: S. Xie et al., “Toward Fine-Grained Facial Control in 3D Talking Head Generation,” arXiv:2602.09736, 2026. https://arxiv.org/abs/2602.09736
[^36]: T. Chen et al., “EmoZone-Talker: Regional Semantic Control of Audio-Driven 3DGS Talking Heads via Facial Action Units,” arXiv:2606.15848, 2026. https://arxiv.org/abs/2606.15848
[^37]: H. Yang et al., “GaussianEmoTalker: Real-Time Emotional Talking Head Synthesis with Audio-Driven and Blendshape-Based 3D Gaussian Splatting,” arXiv:2607.00959, 2026. https://arxiv.org/abs/2607.00959
