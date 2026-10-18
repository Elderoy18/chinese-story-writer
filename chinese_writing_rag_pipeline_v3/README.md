# Chinese writing feedback pipeline, v3

Self-contained: every script reads only files inside this folder.

- OpenAI key: `.env` here (git-ignored; one line, `OPENAI_API_KEY=...`).
- Python: steps 1-3 and 5 use the standard library only; step 4 (HanLP) runs in
  this folder's `.venv`, and HanLP's model is downloaded into `.models/hanlp`
  (both git-ignored; exact package versions in `requirements.txt`).

```
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
python scripts/01_extract.py
python scripts/02_corpus.py
python scripts/03_split.py
.venv/Scripts/python scripts/04_parse.py     # first run downloads the HanLP model (~115 MB)
python scripts/05_align.py --split test      # LLM; responses cached in data/05_align/cache
python scripts/05_align.py --split train
```

Plan: a baseline built from the basic data only (B0), then the teacher's
feedback data added in separate, measured stages. Evaluation is precision-first:
false positives and incorrect corrections count before recall.

| Step | Script | Reads | Writes | Status |
|---|---|---|---|---|
| 1 | `01_extract.py` | `raw/basic_data/`, `raw/feedback_data/` (.docx, .md) | `data/01_extracted/<folder>/<name>.json` -- paragraphs (text + bold ranges) and Word margin comments with the text they are attached to; `reports/01_extract.md` | done; basic data identical to the earlier pipeline |
| 2 | `02_corpus.py` | step 1 (basic data only), `raw/stories.json` | `data/02_corpus/corpus.json` -- samples, sentences, located quotes, split feedback, content flags, model stories, scene lists, coherence rubric; `parse_units.jsonl` -- the Chinese HanLP parses | done; identical to the earlier pipeline (+ rubric) |
| 3 | `03_split.py` | step 2 | `data/03_split/split.json` -- the same 20 test / 87 train stories as before; each test story records which of her feedback checks reviewed system output on it (`reviewed_in`) | done; identical split |
| 4 | `04_parse.py` (`.venv`) | step 2's units, `raw/custom_words.tsv` | `data/04_parse/parses.jsonl` -- words, parts of speech, names, dependency links, character positions, and our own story-word labels (`story_entity`: character / object / place / group) | done; identical parse (+ labels) |
| 5 | `05_align.py --split test/train` | steps 2-4, OpenAI | `data/05_align/edits_<split>.jsonl` -- her corrections as exact edits (test = answer key: 250 error edits + 21 comments; train = her memory: 1,143 edits); `review/05_align_<split>.csv` | done; same places as the earlier run (98%), boundaries/splits differ for ~22% of items |
| 6 | `06_s0v2_labels.py` | her comments on S0 (`S0_v2_feedback check`), OpenAI | `data/06_s0v2_labels/comments.jsonl` -- each of her 104 comments with the item it is about and what it says (tags); `review/06_s0v2_comment_tags.csv`; `reports/06_s0v2_labels.md` -- S0 measured on the 6 stories she reviewed. Evaluation labels only, never system input | done |
| 7 | `07_b0_write.py` (+ `b0_lib.py`) | corpus, split, train edits, rubric, OpenAI | `data/07_b0_write/items.jsonl` -- B0 clause-level corrections, 3 runs per test scene | done |
| 8 | `08_b0_vote.py` | step 7 | `data/08_b0_vote/items.jsonl` -- corrections at least 2 of 3 runs agree on | done |
| 9 | `09_b0_verify.py` | step 8, OpenAI | `data/09_b0_verify/items.jsonl` -- after an independent drop-when-unsure check | done; measured, rejects many of her real errors -- not used in B0 |
| 10 | `10_b0_enrich.py` | corpus (model stories, rubric), step 8, OpenAI | `data/10_b0_enrich/enrich.jsonl` -- vocabulary suggestions (≤2/scene, same level), expressiveness ideas (≤2/scene, one per clause), encouragement | done |
| 11 | `11_b0_content.py --split train`, then test | corpus (scene lists, her train flags), OpenAI | `data/11_b0_content/checks_<split>.jsonl` -- verdict per required scene; learner notes built from the majority verdicts in her scene-list wording; `reports/11_b0_content_<split>.md`; `review/11_b0_content_review.csv` | done |
| 12 | `12_b0_assemble.py` | steps 8, 10, 11 | `runs/B0/` -- **round B0, frozen** (feedback per story, manifest, scripts copy); `review/B0_feedback_for_teacher.md`, `review/B0_labels.csv` + instructions | B0 ready for the teacher |
| 13 | `13_b1_write.py` | corpus, split, train edits, rubric (written out as the A/B/C checklist), OpenAI | `data/13_b1_write/items.jsonl` -- one line per error (student's phrase：corrected phrase，what and why), Grammar and Vocab or Coherence: Reference/Temporality/Conjunction, 3 runs | done |
| 14 | `14_b1_vote.py` | step 13 | `data/14_b1_vote/items.jsonl` -- lines at least 2 of 3 runs agree on | done |
| 15 | `10_b0_enrich.py --corrections data/14_b1_vote/items.jsonl --out data/15_b1_enrich` | step 14 | `data/15_b1_enrich/enrich.jsonl` -- new words, expressiveness, encouragement | done |
| 16 | `16_b1_assemble.py` | steps 14, 15, 11 | `runs/B1/` -- **round B1, frozen**, in the agreed format; `review/B1_feedback_for_teacher.md`, `review/B1_labels.csv` + instructions | B1 ready for the teacher |
| -- | `score.py <items.jsonl ...>` | answer key, `review/labels/teacher_labels.jsonl` | `reports/score_<name>.md` -- precision-first: false positives / scene (labelled – worst case), incorrect corrections, same-as-hers, consistency across runs, recall last | ready |

## Conventions

- **Character positions never move.** Text changes only one character for one,
  so every later position points at the same character as in the source file.
- **Test stories are held out** of everything built from her data; only the
  evaluation reads their corrections.
- **Every report lists what a script could not handle cleanly**, for checking by hand.
