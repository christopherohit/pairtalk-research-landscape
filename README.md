# PairTalk Research Landscape

This repository is a dated, reproducible research-landscape package for
few-shot personalized audio-driven talking heads. It combines a public-metadata
collector with literature notes, architecture hypotheses, experiment records,
negative results, and dataset/asset access checks developed during PairTalk
research in 2026.

It is intended to make the reasoning and failure history inspectable. It is not
a paper claim, benchmark release, systematic-review guarantee, or substitute
for checking original sources.

## Evidence Status and Date Boundary

The notes are snapshots written during 2026 and should be read with their dates
and evidence labels intact. The field changes quickly; publication status,
repository availability, licenses, and model releases may have changed since a
snapshot was written.

The documents contain:

- literature observations and scoped negative searches;
- architecture proposals that were later falsified or weakened;
- synthetic invariants;
- motion-space and single-renderer pilot measurements;
- plans that were never authorized for execution;
- explicit claim and asset boundaries.

They do **not** establish validated image-quality gains, multilingual
generalization, new-identity performance, human preference, commercial
fitness, or novelty. A statement that no exact match was found in the reviewed
corpus is not proof that prior art does not exist.

## Repository Contents

### Reproducible collector

- `collect_landscape.py` queries OpenAlex, arXiv search, GitHub repository
  search, and the Hugging Face datasets API through public endpoints.
- Results are deduplicated per source, filtered by an explicit weighted keyword
  score, sorted, and written as JSON and CSV.
- Per-query failures are recorded rather than aborting the entire collection.

### Research records

- `PairTalk_deep_research_2026.md` - broad evidence map, occupied mechanisms,
  data readiness, PairScope analysis, falsified alternatives, and recommended
  next experiments.
- `PairTalk_frontier_landscape_2026.md` - compact September 2026 frontier
  snapshot and claim-hygiene checklist.
- `PairTalk_major_conference_architecture_2026.md` - PairQuotient hypothesis,
  controls, staged evidence plan, and exploratory failure.
- `PairTalk_research_dossier.md` - consolidated measurements across PairJudge,
  PairTangent, PairCert, PairScope, PairLift, PairBank, and related baselines.

### Structured planning data

- `dataset_access_matrix.csv` and `dataset_access_matrix.md` distinguish local
  availability from permission to use, publish, or redistribute.
- `frontier_novelty_matrix.csv` records occupied claims, proposed PairTalk
  boundaries, evidence locations, and audit status. It is a working comparison
  aid, not a novelty opinion.

Some dated notes mention paths under private research worktrees such as
`probe/results/` or `research/papers/`. Those references preserve provenance;
the underlying private artifacts, paper text, media, and model assets are not
part of this repository.

## Installation

Python 3.10 or newer is required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

The collector depends on `requests` and `beautifulsoup4`.

## Run the Metadata Collection

```bash
python collect_landscape.py --out catalog
```

The output directory is created automatically. A successful run writes:

| File | Contents |
|---|---|
| `landscape.json` | Timestamp, query lists, complete retained records, and errors |
| `papers_openalex.csv` | OpenAlex work metadata and relevance scores |
| `papers_arxiv.csv` | Parsed arXiv search results and abstracts |
| `code_github.csv` | GitHub repository metadata |
| `datasets_huggingface.csv` | Hugging Face dataset metadata |

The script prints retained counts per source. If any source/query request
fails, it then prints a warning and stores details in `landscape.json` under
`errors`.

## Collection Method

The collector uses fixed query lists covering talking-head 3DGS, few-shot
personalization, multilingual motion, renderer feedback, correspondence,
counterfactual validation, abstention, inverse rendering, articulatory
constraints, and related topics.

Records are assigned a deterministic keyword score from the
`RELEVANCE_WEIGHTS` mapping. Thresholds are deliberately permissive:

- OpenAlex and arXiv records require score at least `4`;
- GitHub repositories require score at least `4`;
- Hugging Face datasets require score at least `3`.

OpenAlex works are deduplicated by DOI or normalized title/year. Other sources
use arXiv ID, GitHub full name, or Hugging Face dataset ID. Matched queries are
merged so readers can see why a record entered the catalog.

The scoring is a retrieval heuristic, not a classifier. It can miss relevant
work, retain false positives, and overweight terminology shared across
unrelated papers.

## Reproducibility Notes

The generated catalog is intentionally not committed because:

- upstream search results, counts, citations, stars, and metadata change;
- public APIs may rate-limit, reorder, or omit results;
- arXiv HTML structure may change;
- anonymous GitHub API limits are restrictive;
- third-party metadata remains governed by source terms.

For a report or paper, preserve the exact output directory, collection time,
Python/dependency versions, network region if relevant, and the repository
commit. Do not silently replace an older catalog with a new run while retaining
old conclusions.

The script includes short delays between requests but has no persistent cache,
authentication support, pagination beyond its declared per-query limits, or
automatic retry/backoff. It may take several minutes because it runs many
queries. A partial run is still inspectable through the `errors` list.

## Validation Without Network Access

The module can be syntax-checked and its CLI inspected without contacting
external services:

```bash
python -m py_compile collect_landscape.py
python collect_landscape.py --help
```

There is currently no mocked API test suite. Changes to parsing logic should
add saved minimal fixtures before being treated as robust against upstream HTML
or schema changes.

## Reading the Research Notes Responsibly

Use the following hierarchy:

1. Original paper, official code, dataset card, and license are primary.
2. Structured local measurements are evidence only for their declared data and
   protocol.
3. Architecture documents are hypotheses until a frozen experiment passes.
4. Proxy motion or geometry metrics are not rendered-image evidence.
5. Synthetic invariants validate implementation properties, not utility.
6. Failed gates remain failures even when one secondary metric improves.

Several notes deliberately preserve negative outcomes. Do not select only the
positive intermediate numbers while omitting shuffled controls, static
anchors, confidence intervals, or failed decision gates.

## Dataset and Asset Governance

`Available locally` means files were inspectable in the original research
workspace. It does not mean the asset may be redistributed, used commercially,
used for biometric processing, or included in a public benchmark.

Before using an asset, independently verify:

- dataset and source-media licenses;
- checkpoint and code licenses;
- identity consent and intended purpose;
- commercial/non-commercial restrictions;
- derivative-work and redistribution restrictions;
- privacy, biometric-data, and retention requirements;
- whether an access URL still points to the same version.

The access matrix is planning documentation, not legal advice or license
clearance.

## Source and API Considerations

- OpenAlex metadata is obtained from the OpenAlex public API.
- arXiv records are parsed from public search HTML; the collector does not
  download PDFs.
- GitHub results use the public repository search API and may be heavily rate
  limited without authentication.
- Hugging Face results use the public datasets API and may include gated or
  private-state metadata fields.

Respect each service's current terms, robots/rate policies, attribution rules,
and data licenses. Do not use this script to evade authentication, gates, or
access controls.

## Contributing

Useful contributions include corrected citations, updated release/license
status with primary-source links, parser fixtures, reproducibility metadata,
and clearly labeled replication results. Keep observations separate from
claims, record dates, preserve failed experiments, and state when evidence is
synthetic, proxy, pilot, or conference-scale.

Do not add copyrighted paper PDFs, restricted datasets, identity media,
checkpoints without redistribution rights, secrets, access tokens, or locally
extracted biometric features.

## License

Repository-authored code and documentation are released under the MIT License.
The license does not relicense third-party metadata, paper content, datasets,
media, model weights, code, trademarks, or cited works. Those remain subject to
their original terms.
