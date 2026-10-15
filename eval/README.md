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
- `snapshots/<name>/` -- the retrieval corpus, frozen: built by
  `make_snapshot.py` from the current pipeline sources **with the held-out
  samples removed**, searched locally (exact cosine), never touching the live
  database. Vectors live in `cache/` (not committed; rebuilt on demand).

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
