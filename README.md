# PairTalk Research Landscape

Reproducible collection code and research notes for few-shot personalized,
audio-driven talking heads, with emphasis on paired support supervision,
renderer feedback, counterfactual validation, and abstention.

## Contents

- `collect_landscape.py`: collects OpenAlex, arXiv, GitHub, and Hugging Face
  metadata using public endpoints.
- `dataset_access_matrix.*`: access and redistribution constraints considered
  during experiment planning.
- `frontier_novelty_matrix.csv`: working comparison matrix, not proof of
  novelty.
- `PairTalk_*_2026.md`: dated research notes and architecture exploration.

## Reproduce The Metadata Collection

```bash
pip install -e .
python collect_landscape.py --out catalog
```

The generated catalog is intentionally ignored because it is large, changes
with upstream services, and may contain third-party metadata under separate
terms.

## Evidence And Ethics Boundary

These documents include hypotheses, pilot failures, and negative results. They
must not be read as validated image-quality, multilingual, new-identity, or
novelty claims. No datasets, identity media, checkpoints, FLAME assets, paper
PDFs, or locally extracted features are redistributed. Historical references to
local experiment artifacts are provenance notes; those artifacts are not part
of this public repository.

Code in this repository is MIT licensed. Third-party metadata and cited works
remain subject to their original licenses and terms.
