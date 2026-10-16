# Integrated HanLP-RAG pipeline

A rebuild of the feedback pipeline, built step by step. Everything it uses lives in this folder.
Each step is one script with one output folder and one report in `reports/`; a step is
reviewed before the next one is built.

Run from anywhere (paths are relative to this folder). Steps 1-3 need only standard-library
Python; step 4 needs HanLP, installed in this folder's own virtual environment:

```
cd integrated_HanLP-RAG_pipeline
python -m venv .venv                              # once
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python scripts/04_parse.py          # first run downloads the HanLP model (~115 MB) to %APPDATA%/hanlp
```

| Step | Script | Reads | Writes | Status |
|---|---|---|---|---|
| 1 | `scripts/01_extract.py` | `raw/basic_data/*.docx` | `data/01_extracted/<name>.json` -- paragraphs + bold ranges | for review |
| 2 | `scripts/02_corpus.py` | step 1, `raw/stories.json`, `raw/basic_data/story_scenes.md` | `data/02_corpus/corpus.json` -- samples, sentences, located quotes, split feedback, content flags, model stories, the teacher's required-scene lists; `parse_units.jsonl` -- the Chinese HanLP will parse, by unit_id | for review |
| 3 | `scripts/03_split.py` | step 2 | `data/03_split/split.json` -- 20 test samples (with scenes), 87 train | for review |
| 4 | `scripts/04_parse.py` | step 2's `parse_units.jsonl`, `raw/custom_words.txt` | `data/04_parse/parses.jsonl` -- HanLP words, parts of speech, names and dependency links, each word with its character position | for review |
| 5 | `scripts/05_align.py` | steps 2-4, OpenAI | `data/05_align/edits_test.jsonl` -- the teacher's corrections on the test stories as exact edits (the answer key); `review/05_align_test.csv` -- review sheet | test set accepted after a read-through; train (`--split train`) aligned, flagged items in `review/05_align_train.csv` |
| 6 | `scripts/06_find_baseline.py` | steps 2-3, OpenAI | `data/06_find_baseline/candidates.jsonl` -- errors an LLM finds in each test scene with no teacher material, 3 runs | done |
| 7 | `scripts/07_score.py [finder]` | step 5 answer key, a finder's candidates | `reports/07_score_<finder>.md` -- recall, stability, candidates matching nothing she marked | done for the baseline |
| 8 | `scripts/08_find_gec.py` (in `.venv`) | steps 2-3 | `data/08_find_gec/candidates.jsonl` -- edits from an offline GEC model (HillZhang/real_learner_bart_CGEC, ~1.5 GB, Hugging Face cache) on the test scenes; `rewrites.jsonl` -- its sentence rewrites | done |
| 9 | `scripts/09_extra_flags.py` | answer key, finders' candidates | `review/09_extra_flags.csv` + `_instructions.md` -- places the finders flagged that the teacher did not mark, for her to judge | sheet ready for the teacher |
| 10 | `scripts/10_content.py [--split train]` | corpus (samples + scene lists), split, OpenAI | `data/10_content/checks_<split>.jsonl` -- told / partly / missing per required scene (test: 3 runs); `reports/10_content_<split>.md` (+ `_train_v1`, `_train_v2` calibration history); `review/10_content_review.csv` + `_instructions.md` -- test disagreements with her flags | calibrated on train (v3); test measured; sheet ready for the teacher |
| 11 | `scripts/11_categorize.py` | step 5 edits (train + test), coherence rubric, OpenAI | `data/11_categories/taxonomy.json` -- 62 categories built from train edits; `edits_<split>.jsonl` -- every edit with its category and HanLP signature; `reports/11_categories.md` | draft list; reviewed with the rule cards (step 12) |
| 12 | `scripts/12_rule_cards.py` | step 11 categories + train edits, OpenAI | `data/12_rule_cards/cards.json` -- one card per category: rule, explanation template, 3-5 of her corrections, not-an-error line, HanLP edit shapes; `review/12_rule_cards.md` (readable) + `12_rule_cards_review.csv` + `_instructions.md` -- categories and cards, for the teacher | draft awaiting the teacher |
| 13 | `scripts/13_find_teacher.py` (no LLM) | step 11 train edits, step 4 parses, split | `data/13_find_teacher/patterns.json` -- her wording patterns mined from train; `candidates.jsonl` -- her patterns + HanLP checks of her rules on the test scenes; `reports/13_find_teacher.md` -- train calibration per part | done; scored with step 7 |
| 14 | `scripts/14_judge.py` | finders' candidates (06 run 1, 08, 13), train edits (embeddings), rule cards, OpenAI | `data/14_judge_input/` -- flags before judging; `data/14_judge/candidates.jsonl` -- errors kept; `judgments.jsonl`; `reports/14_judge.md` (v1 kept as `14_judge_v1.md`) | v1 measured on test: lowered recall (70% -> 58%); NOT USED -- documented negative result |
| 15 | `scripts/15_explain.py` | finders' candidates (06 run 1, 08, 13), train edits (embeddings), rule cards, OpenAI | `data/15_explain/items.jsonl` -- one feedback item per flagged place (correction, strength, category, explanation, what it was built from); `reports/15_feedback.md` -- the feedback each test scene gets; `reports/15_explain.md`; `review/15_explanations_review.csv` + `_instructions.md` -- 60 explanations for the teacher to rate | done; awaiting the teacher's ratings |
| 16 | `scripts/16_enrich.py` | test scenes, model stories, parses, step 15 items, coherence rubric, OpenAI | `data/16_enrich/enrich.jsonl` -- per scene: expressiveness ideas, vocabulary suggestions, encouragement; `reports/16_enrich.md` -- expressiveness profile (learners vs model story) | done |
| 17 | `scripts/17_assemble_s0.py` | steps 10, 15, 16 | `runs/S0/` -- **round S0, frozen**: complete feedback per story (`feedback.json`, `feedback/*.md`), `manifest.json` (models, prompt versions, file hashes, git commit), `scripts/` copy; `review/S0_feedback_for_teacher.md` + `S0_story_ratings.csv` | S0 sent for teacher review |

Shared helper: `scripts/llm.py` (one cached structured-output OpenAI call; used by steps 5 and 6).

## Conventions

- **Character positions never move.** Step 1 changes characters only one-for-one, so every
  start/end position (quotes, sentences, later HanLP tokens and error spans) points at the
  same character in the original text.
- **Test samples are held out** of every step that learns from the teacher's data; only the
  evaluation reads them.
- **Every report lists what the script could not handle cleanly**, for checking by hand.
