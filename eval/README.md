# Stage evaluation: what each human-in-the-loop iteration changed

Each stage switches on one more iteration of the teacher's input and is run
over the same held-out samples, so every "after" can be compared with its
"before". Stages are defined in `stages.json`; the prompt pieces each stage
switches on are in `lib/rag/promptStages.ts`. S4 renders exactly the prompt
the app uses.

| Stage | Adds |
|---|---|
| S0 | Basic data + the original prompt (no human-in-the-loop input) |
| S1 | Critique of the AI feedback: rules 1-8, pinned AI-error cards, structured format |
| S2 | Required-scene list: end-of-story content check against `scene_list` |
| S3 | Vocabulary error list: wrong words are errors; vocab entries retrieved |
| S4 | Coherence rules: rules A-C, Coherence & Expressiveness, pinned reference/了 cards, earlier scenes, model story |

## Test set and retrieval

- `test_set.json` -- 6 held-out graded samples (3 孟母, 3 神农), each split
  into 3 scenes, with the teacher's corrections and content flags as gold.
  Made once by `make_test_set.py`.
- `test_set_h20.json` -- the S7 test set: the 20 stories the teacher reviewed
  in the alignment check (`align test.xlsx`; v2's test split), 60 scenes. It
  includes the 6 stories above with the same scenes. Gold adds her corrections
  as exact edits with her review decision, and her review notes (missed errors,
  alternative fixes, rule explanations). Made by `make_test_set_h20.py`; known
  issues in her review are listed in the file's `_known_issues`.
- `snapshots/<name>/` -- the retrieval corpus, frozen: built by
  `make_snapshot.py` from the current pipeline sources **with the held-out
  samples removed**, searched locally (exact cosine), never touching the live
  database. Vectors live in `cache/` (not committed; rebuilt on demand).
  `--test-set` chooses which stories are held out (default `test_set.json`).
  The build also stops if a held-out sentence appears in any chunk's text; an
  entry of her hand-made lists (vocabulary errors / suggestion examples /
  teacher rules) quoting a phrase found only in held-out stories is dropped
  instead and listed in the manifest (`dropped_for_held_out`).
- A stage runs on the test set named by its `testSet` field in `stages.json`
  (default `test_set.json`; inherited like `snapshot`).

| Snapshot | Sources | Held out |
|---|---|---|
| `base-v4` | S6's | 6 (`test_set.json`) |
| `base-v4-h20` | S6's, exactly (chunks verified identical) | 20 (`test_set_h20.json`); her suggestion example 1 dropped (quotes shennong_samples#4) |

## Running

```
python eval/make_snapshot.py base          # once per snapshot
node eval/embed_snapshot.mjs base
node eval/run_stage.mjs S0                 # -> runs/S0/<sample>.json
node eval/run_stage.mjs S1
node eval/compare.mjs S0 S1                # -> reports/S0_vs_S1.md (teacher review)
node eval/compare.mjs --summary S0 S1 S2 S3 S4   # -> reports/summary.md
```

Each run file keeps, per scene, the exact user prompt, the retrieved chunk
ids and the feedback; `runs/<stage>/stage.json` keeps the resolved stage, the
full system prompt, the model and the snapshot manifest.

`make_snapshot.py` stops if any source file is missing (and records the hash of
each input, including the AI-critique docs and `critique_labels.json`, in the
manifest).

## Guard: earlier stages stay unchanged

Later stages share code with earlier ones (`lib/rag/promptStages.ts`, the
pipeline scripts). After any change there, check that the stages kept for
comparison still render exactly the prompts their stored runs used:

```
node eval/check_stage_unchanged.mjs            # S6 (the S7 baseline)
node eval/check_stage_unchanged.mjs S6 S5 S4
```

It re-renders every scene and content prompt (system, user, retrieved chunk
ids) from the current code and the stage's frozen snapshot and compares them
with `runs/<stage>/`. No LLM calls. "identical" = the stage is preserved; any
difference is listed and the exit code is 1. New behaviour must go behind a new
flag (default off) or in a new snapshot, never into an existing stage.

## Teacher in the loop: refining a stage

The report `reports/<before>_vs_<after>.md` shows the teacher's own
corrections, both feedbacks per scene, and a review checklist with a verdict.
If the "after" is not good enough:

1. Add a refined stage to `stages.json` that extends the stage being refined
   and changes only what the teacher asked for:
   - prompt wording -- `"fragments": {"rule2": "overrides/S1-v2/rule2.txt"}`
     (fragment names: `FRAGMENT_NAMES` in `lib/rag/promptStages.ts`), or
     `"extraRules": ["..."]` for a new numbered rule;
   - data (vocab entries, scenes) -- edit the files in
     `chinese_writing_rag_pipeline/raw/iteration data/`, build a new snapshot
     (`python eval/make_snapshot.py base-v2`, then embed it) and set
     `"snapshot": "base-v2"`.
2. `node eval/run_stage.mjs S1-v2`, then compare it with both its "before"
   (`S0 S1-v2`) and the version it refines (`S1 S1-v2`).
3. Once accepted, promote it: put the new wording into the default fragment
   in `promptStages.ts` (or keep the new data files), and re-point later
   stages' `"extends"` if they should build on it.
