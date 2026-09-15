# Dataset and Asset Access Matrix

This matrix separates what is already present locally from what is merely a
candidate external source. “Available” means the files can be inspected in the
workspace; it does not mean that every source-video or checkpoint license has
been cleared for redistribution or publication.

| Asset | Role | Status | Main restriction/caveat | Next action |
|---|---|---|---|---|
| FLOAT motion bank | Correlated proposal pilot | Local | CC BY-NC-ND 4.0; source portrait rights remain separate; not independent teachers | Use only as a non-commercial falsifier |
| SMIRK motion | 53-D target and neutral teacher | Local | Checkpoint/model terms | Record provenance/confidence |
| XLS-R features | Multilingual audio representation | Local | Model-card terms; current identities/languages confounded | Add bilingual same-speaker clips |
| FLAME 2020 + vertex masks | Anatomical region masks | Local | FLAME model license applies | Keep license record and cite FLAME |
| HDTF | External pretraining/evaluation | External | Video-source rights differ from repo metadata | Audit each source |
| MultiTalk | Multilingual candidate | External | Non-commercial research only; no redistribution | Build same-identity bilingual subset |
| MEAD | Emotion/proposal training | External | License unresolved in current notes | Complete license audit |
| Multiface | Neural rendering candidate | External | CC BY-NC 4.0; large storage | Defer unless storage is approved |
| InsTaG | Renderer baseline | External/reference | Default is about 10 s, not automatically 125 frames | Rerun exact 125-frame baseline |
| SadTalker | Independent proposal route | External | Repo/checkpoint/third-party audit needed | Map to common 53-D space |
| UniTalker D1 | Independent FLAME proposal route | External | Implementation/model terms need audit | Start only after motion-space pass |
| EmoTaG evaluation release | Processed neutral/MEAD baseline scenes | Local, 52/52 hashed | Public access is not a redistribution grant; source/checkpoint terms remain separate | Exact environment + Sapiens + adaptation smoke test |
| EmoTaG pretrained checkpoint | Multi-identity EMA GRMN prior | Local, hash recorded | Public download is not a redistribution/commercial-use grant | Load and smoke-test in release environment |
| SubtleTalk-Face | Weakly-correlated dynamics pretraining candidate | Announced; local repo has no data | Paper reports about 3,900 identities/74 h; release/license still pending | Monitor official release only |

For detailed paths, access states, and caveats, see
`research/dataset_access_matrix.csv`. The broader literature and source links
are in `research/PairTalk_research_dossier.md`.
