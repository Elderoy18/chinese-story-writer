# S7 plan: more consistent (and more accurate) feedback, built on S6

Goal: the same error gets the same verdict, fix and explanation -- across reruns and across
different stories -- without more false positives or incorrect corrections (her priority:
"可以接受AI miss errors，但是不能出现false positives或incorrect corrections").

## Why on top of S6, not a new folder

S6 is a *stage*: switches in `lib/rag/promptStages.ts` (shared with the app) + prompt overrides
in `eval/stages.json` + a frozen snapshot (`eval/snapshots/base-v4`). Every change below is a new
stage extending S6, switched on by a new flag that defaults to **off**, so S6 and the app are
unchanged until a stage is promoted. The only copy is the data: a new snapshot `base-v5`.

Guardrail: `eval/check_stage_unchanged.mjs` re-renders S6's system and user prompts and
retrieved chunks for all 18 scenes (and the 6 content prompts) from the current code and
compares them with the prompts stored in `eval/runs/S6/`. Run it after every code change; it
must report "identical".

## What we know going in

- S6 beats v2 on every point she raised; v1-S0 (no teacher input) already made a third of v2's
  incorrect corrections, so v1's design (the model finds and fixes errors, reading the whole
  scene) is the one to keep. Her iterations S1-S6 cut false positives (1.06 -> 0.50 / scene) and
  fixed the content check (5/15 -> 14/15).
- S6 run 3 times: retrieval identical every run (Jaccard 1.0, 54 pairs), yet the same corrected
  text at only ~27% of the places flagged every time; content verdicts agree 69%. Rerun
  inconsistency is all generator.
- Across places, retrieval is content-driven: the 不是…而是 card reached 2 of the 6 scenes that
  contain the pattern, and S6 never caught that error.
- Her data helps as guidance, hurts as authority. In v2, places flagged only by patterns mined
  from her corrections were wrong 58% of the time (11/19) and half were not places she marked:
  her corrections are tied to their sentence, and lifted out as general patterns they over-fire.
  (Most of v2's incorrect corrections, 32 of 37, came from its LLM and correction-model finders,
  through its display and one-fix-per-place steps -- not from her data.) S6 gives her data to a
  model that decides whether it applies. **Risk for this plan:** the triggers in 1.5 are the same
  kind of thing as v2's mined patterns -- they stay hints the model checks, their false alarms
  are measured before they are kept, and S7-4 is accepted only if false positives do not rise.

---

## Phase 0 -- housekeeping (before anything else) -- DONE 18 Oct

| Step | What | Mechanism | Status |
|---|---|---|---|
| 0.1 | Starting commit. | -- | `1426465` ("v2 and v3 additions") |
| 0.2 | `eval/check_stage_unchanged.mjs` (above). | guard | done; S6, S5, S4 identical; a deliberately altered S6 prompt is caught |
| 0.3 | Restore the missing sources of S6's snapshot. `extra_rules.json` (never committed) rebuilt from the 8 teacher-rule chunks in `base-v4`; `story_scenes.md` (deleted in `6383630`) restored from `87cb456` -- byte-identical to the version `base-v4` was built from. The new rules in `more rules.docx` are added in 1.3, not here, so the restored file is exactly S6's. | 10 | done |
| 0.4 | `build_iteration_chunks.py` and `make_snapshot.py` stop with an error when a source file is missing, instead of silently returning no chunks. AI-critique docs are read from an explicit list (`CRITIQUE_DOCS`): her new `AI_Feedback_Tags_and_Teacher_Critiques with comments.docx` has "AI feedback" headings but no story and was crashing the build. | 10 | done |
| 0.5 | Check: rebuilding from today's sources reproduces `base-v4` exactly (1,246 chunks, same ids, content and order); the pipeline's own `build_iteration_chunks.py` writes a file identical to the committed `chunks/iteration_chunks.jsonl`. | 10 | done |

## Phase 1 -- data: snapshot `base-v5`

All new inputs are frozen copies inside `chinese_writing_rag_pipeline/raw/iteration data/`
(with their hashes in the snapshot manifest), never read across from v2/v3 folders.

**Held-out rule (D1: 20 stories).** The test set is the 20 stories she reviewed in the align
test (v2's test split; same scene splits as v1 for the 6 shared stories). Nothing about them
enters `base-v5`: their corrections, all 64 align-test notes on them (they stay in the answer
key), and her S0_v2 comments on any of them. `make_snapshot.py` asserts this by searching every
chunk for held-out sample ids and their sentences.

| Step | What | Mechanism |
|---|---|---|
| 1.1 | **Her verdicts file** `her_verdicts.jsonl`: one line per item she judged -- source (align test / critique comments / S0_v2 / S4 / S5), date, item, verdict, her correction, her note, and `supersedes` when she revised an earlier verdict. Used for evaluation and to rebuild labels; latest verdict wins. | 1 |
| 1.2 | **Aligned corrections.** Replace the heuristic `correction_item` split (original / corrected / why) with her exact aligned edits (v2 `05_align`, 232/234 accepted on test; train edits as aligned). Attach her align-test notes as the "why"; add her "miss" items as new corrections; keep "another correction" as accepted alternatives. Each edit inherits the v1 rule labels of the correction it came from (matched by her original line). | 5 |
| 1.3 | **Rule updates.** Refined rules replace old wording (告诉 no 了 only before speech content; 住在 is a state, no 了; 别 cannot take Num + MW). Teacher rules: 8 -> 17. New AI-error card: **over-correction** (changes more than needed / does not preserve the learner's meaning), from her 15 Oct critique comments; relabel the critiqued AI items she revised. | 1, 12 |
| 1.4 | **Standard fix per rule card** (`standard_fix`): the fix pattern she uses for that rule, with 2-3 of her aligned edits as canonical examples ("住了在 -> 住在", "搬了到 -> 搬到了"). | 11 |
| 1.5 | **Rule-card triggers, mined offline with HanLP.** For each rule: parse her train corrections, propose regex triggers from the recurring error shapes, and measure each trigger on train data -- fires on her marked errors (recall) vs fires on correct text: her corrected sentences and the model stories (false alarms). Keep triggers above a precision threshold. Written to `chinese_writing_rag_pipeline/review/triggers/` (`triggers_review.csv`: rule, regex, examples it catches, false alarms, keep? + `instructions.md`) for you to check (D3), and to send on to her if needed. Only reviewed triggers enter `base-v5`. Only the regex runs live. | 6 |
| 1.6 | **Error-example index.** New chunk type `rule_example`: one per corrected student sentence, text = the student's original sentence, `parent_id` = its rule card. A similarity hit on an example returns its card. | 2 |
| 1.7 | **Contradiction check.** At build time, list rules / cards / examples on the same pattern that disagree (e.g. two 告诉+了 rules), and revised items still present beside their replacement. The build stops until each is resolved (replaced, or marked "both true" with the condition). | 12 |
| 1.8 | Build `base-v5`, embed it, record counts and hashes in the manifest. | 10 |

## Phase 2 -- measurement harness (`eval/consistency/`)

**Test set.** `eval/test_set_h20.json`: the 20 stories, scenes from v2's split, gold = her aligned
answer key (with her alternatives and the "miss" items from the align test) + her content flags,
each correction carrying its v1 rule labels.

**Fair baseline.** `base-v4` includes 14 of the 20 stories, so S6 is re-run on `base-v4-h20` --
`base-v4`'s exact sources with all 20 held out -- before it is compared with anything.

**Test units.** Her corrections on the held-out stories, each a "target error" with its rule
labels.

**Inputs per target error** (our version of the paper's paraphrases -- the error is kept
verbatim, only its surroundings change; built from her data, no LLM rewriting):
- **original** -- the scene as written;
- **variant A** -- every *other* sentence in the scene replaced by her corrected version, so only
  this error is left;
- **variant B** -- the erroneous sentence placed in a different scene of the same story.
- Natural variants: the same rule broken in different stories (already in the test set).

**Run modes** (new options for `eval/run_stage.mjs`): `--variant A|B`, and `--fixed-retrieval`
(every variant gets the chunks retrieved for the original). Plus the existing reruns (3 runs of
the same input).

| Level | What varies | Measure |
|---|---|---|
| a. Retrieval | input (original / A / B) | Jaccard of retrieved chunk ids per pair; **rule-card recall** (is the card for her error retrieved?) |
| b. Generator | input, retrieval fixed | at the target error: **lexical** = identical Chinese corrected text (explanation stripped -- fixes the parser leak found earlier); **information** = judge says same error identified + equivalent fix (her alternatives count as equal) |
| c. End-to-end | everything | same lexical / information comparison |
| Reruns | nothing | same, isolates model randomness |

**Attribution** (per her correction, and -- once items cite cards -- per wrong item):

| Card for her error in the prompt? | Output | Blame |
|---|---|---|
| no | missed / wrong | retrieval |
| yes | missed | generation (ignored) |
| yes | wrong fix | generation (misapplied) |
| yes | right | working |

**Accuracy** (from `eval/v1_vs_v2/score.py`, unchanged judge, 3 runs, mean and range): false
positives / scene, incorrect corrections / scene, items fully right, corrected text not fully
correct, partial sentences, wrong category, content scenes caught, recall.

**Baseline**: S6 on `base-v4-h20` through the full harness. Report: `eval/reports/S7_baseline.md`.

**Output format (D2)** stays S6's: Grammar & Vocabulary Corrections (errors only, one combined
section, since she often disagreed with the grammar/vocabulary split) / Vocabulary Suggestions
(own section) / Coherence: Reference, Temporality, Conjunction / Expressiveness / Encouragement;
end of story: Content & Completeness. Scoring treats Grammar and Vocabulary as one category.
A "(suggestion)" tag inside the corrections list is *not* used: her vocabulary list says these
"should be listed as an error not a suggestion", several S0_v2 comments ask for a suggestion to
be treated as an error, and in v2 "suggestion" items were false positives twice as often as
errors (22% vs 11%). It can be tried later as its own stage if wanted.

## Phase 3 -- stages (each extends the last accepted one; 3 runs; one change each)

Generator side first (that is where the rerun gap is), then retrieval, then the filter.

| Stage | Change | Mechanism | Expect to move |
|---|---|---|---|
| S7-0 | S6 on `base-v5` (new data, no code change) | 1, 5, 10, 12 | accuracy; a bit of b |
| S7-1 | reasoning effort low -> medium | 14 | b, reruns |
| S7-2 | each correction names its rule card (or past correction); the card's standard fix and explanation pattern are to be reused, not reworded | 8, 11 | b (lexical + information), "explanation needed", attribution of wrong items |
| S7-3 | content check returns a fixed verdict per required scene (told / missing / wrong) before the notes | 13 | content agreement across runs |
| S7-4 | rule-card triggers + correction examples filtered by the triggered rule | 6, 4 | a, c, recall |
| S7-5 | error-example index (`rule_example` hits return their card) | 2 | a, c |
| S7-6 | one similarity search per sentence instead of per scene | 3 | a, c |
| S7-7 | hide an item whose cited card was not retrieved, does not exist, or does not match the error | 9 | false positives |

**Accept a stage only if:**
1. false positives / scene and incorrect corrections / scene are not above the *highest* of the
   previous stage's 3 runs (run-to-run spread is ~0.2 / scene, so smaller "gains" are noise);
2. information consistency (b or c, whichever it targets) improves;
3. recall drops by no more than 5 points (she accepts misses, but not a collapse).

Otherwise the stage is recorded as a negative result (like S6-2pass) and the next one extends
the last accepted stage.

## Phase 4 -- teacher check

For the best stage: a side-by-side sheet for 2 stories (S6's 3 runs vs the new stage's 3 runs),
so the consistency difference is visible. Her verdicts go into `her_verdicts.jsonl` (1.1) and
are used to re-check the judge (how often the judge agrees with her).

## Phase 5 -- promote to the app

1. Set the accepted flags in `PRODUCTION_FLAGS`; merge accepted prompt overrides into the
   default fragments.
2. If S7-2 is accepted: strip the cited card name from what the learner sees (keep it in the
   stored scene record for analysis, next to `feedbackChunkIds`).
3. Rebuild the live database from the `base-v5` sources: `run_pipeline.py --embed` (with 0.3/0.4
   done, it can no longer drop the teacher rules).
4. Smoke-test the feedback route on one story in the app.

## Costs (rough)

- Phase 1: one-off LLM calls for 1.2 (matching edits to v1 labels) -- small.
- Baseline + each stage, 20 stories (~60 scenes): ~3 runs x 60 scenes x (original + A + B) x 2
  retrieval modes = ~1,000 feedback calls, plus judge calls (cached). Nine runs (baseline + 8
  stages) ~ 9,000 feedback calls. To cut this: run variants A/B only for the stages that target
  retrieval (S7-4 to S7-6); reruns + original for the rest (~180 calls each).

## Progress log

- **18 Oct -- Phase 0.** Added `eval/check_stage_unchanged.mjs`; restored
  `raw/iteration data/extra_rules.json` and `story_scenes.md`; `build_iteration_chunks.py`
  (missing sources stop the build; critique docs listed in `CRITIQUE_DOCS`) and
  `eval/make_snapshot.py` (checks inputs first; records critique docs and labels in the
  manifest). Docs: `eval/README.md` (guard section), `run_pipeline.py` docstring, `design.md`
  §10. Result: S6 is reproducible from source and guarded; the v1 pipeline builds again.

## Decisions

- **D1 (18 Oct): 20 held-out stories.** S6 re-baselined on `base-v4-h20`.
- **D2 (18 Oct): keep S6's sections**, Grammar & Vocabulary combined; vocabulary suggestions in
  their own section, no "(suggestion)" tag in the corrections list.
- **D3 (18 Oct): triggers go to `chinese_writing_rag_pipeline/review/triggers/`** for review;
  sent on to her if needed.
