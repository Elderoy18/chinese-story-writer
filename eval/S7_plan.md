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

## Phase 1 -- data: snapshot `base-v5` -- BUILT 18 Oct (review sheets pending)

**What can go in (consequence of D1).** All 20 test stories are held out, and her newest
item-level feedback is *about* them: every align-test note and all 104 S0_v2 comments (6
stories, all in the test set). Those stay in the answer key. `base-v5` gets what is not about a
test story: her general rules (`more rules.docx`), her revisions of the critique labels (Pear
Story), and everything built from her corrections on the 87 training stories. Some general rules
were probably prompted by her comments on test stories (e.g. why 古代的时候 is redundant); they
contain no test sentence and are kept -- a limitation to state in the paper. Production (Phase 5)
uses everything, including the test-story feedback.

| Step | Status (18 Oct) |
|---|---|
| 1.1 | Done as `raw/iteration data/critique_label_revisions.json`: her 40 comments of 15 Oct on 30 critiqued AI items, verbatim, with Claude's reading as label changes (26 change labels; 3 'perhaps' labels kept as tentative). Two new labels: `overcorrection`, `wrong_or_missing_explanation`. Review: `chinese_writing_rag_pipeline/review/critique_revisions_review.csv`. Align-test / S0_v2 verdicts stay in `eval/test_set_h20.json` / v3 (test stories). |
| 1.2 | Done: `raw/aligned_edits_train.jsonl` (frozen copy of v2's 1,196 training edits; all match a v1 correction line exactly and carry its rule labels). 659 of 729 training corrections get exact edits; rule-card examples show the student's whole clause before and after her fix. Her align-test notes, missed items and alternatives are test-only. |
| 1.3 | Done: `extra_rules.json` 8 -> 20 rules (12 new from `more rules.docx`; 一V就 reworded to her latest; 5 marked restated). The refined 告诉 / 住在 / 别+Num+MW rules exist only in test-story notes -> production only. Over-correction card from 1.1. |
| 1.4 | Done as rule-card metadata `standard_fix` (shown only when S7-2's flag is on). Only 13 of 49 cards have a fix she makes 2+ times (e.g. +了 x15 / -了 x7, 看->看到 x6, -他 x10, 是毒->有毒 x3); most of her fixes are clause rewrites. |
| 1.5 | Done: `scripts/mine_triggers.py` -> `review/triggers/`: 22 proposed rule-card triggers (9 rules, 14 suggested) + all 27 teacher-rule triggers measured. Teacher-rule triggers of the **new** rules below 0.5 precision are held in `triggers_pending_review` (rule shown, no pointer); S6's 8 original rules unchanged. Rule-card triggers enter a snapshot only after review (S7-4). |
| 1.6 | Done: 920 `rule_example` chunks (student's clause -> parent rule card). Inert until S7-5 searches them. |
| 1.7 | Changed to a review report: `scripts/find_opposite_fixes.py` -> `review/contradictions/` -- 11 patterns where her own corrections go both ways in the same context (e.g. +了 / -了 after 吃: completed vs 没+V). Not a build blocker: both directions are her real corrections; the deciding condition belongs in the rule. |
| 1.8 | Done: `base-v5` (2,018 chunks, embedded). vs `base-v4-h20`: 48 rule cards, 11 AI-error cards, 1 teacher rule rewritten; +920 rule_example, +12 teacher rules, +2 AI-error cards. S6 and S6-h20 still identical. |
| -- | Note: the two new AI-error cards are not in S6's pinned card list (code), so they reach prompts only via a flag (S7-0b, below). |

Original plan for Phase 1:

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
| S7-0b | + the two new AI-error cards (over-correction, wrong/missing explanation) pinned like S6's others -- a flag adding them to the pinned list | 1 | incorrect corrections, explanations |
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

- **18 Oct -- Phase 1 prerequisites.** Added `eval/make_test_set_h20.py` -> `eval/test_set_h20.json`
  (20 stories, 60 scenes; 184 correction lines with rule labels; 288 aligned edits, 286 approved
  by her, 1 rejected, 1 undecided; 64 review notes: 46 rule explanations, 11 missed errors,
  2 alternatives, 4 comments, 1 rejected fix). `eval/make_snapshot.py`: `--test-set`; stops if a
  held-out sentence is in any chunk's text; drops (and records) hand-made list entries quoting
  phrases found only in held-out stories -- this caught her vocabulary-suggestion example 1,
  which quotes shennong_samples#4. Built `base-v4-h20` (S6's sources, 20 held out: 1,084
  chunks). `eval/lib.mjs` / `run_stage.mjs`: per-stage `testSet`. Stages `S6-h20` (+ `-r2`,
  `-r3`) = S6 unchanged on `base-v4-h20` and the 20 stories: the S7 baseline. Check: S6 still
  identical. Note: `base-v4-h20`'s manifest hashes differ from `base-v4` for
  `story_scenes.md` (Windows line endings from git; same bytes otherwise) and
  `extra_rules.json` (rebuilt file) -- the chunks they produce are identical.

- **18 Oct -- Phase 1 data.** Added `chinese_writing_rag_pipeline/scripts/aligned_edits.py`
  (exact-edit helpers), `mine_triggers.py`, `find_opposite_fixes.py`; data
  `raw/aligned_edits_train.jsonl` (+ `.about.json`), `raw/iteration data/critique_label_revisions.json`;
  changed `chunk_builder.py` (exact edits, clause examples, standard fixes, rule_example chunks),
  `build_iteration_chunks.py` (applies revisions; cards show her revised comments),
  `rule_descriptions.py` (2 new labels; false-positive description no longer says
  "over-correction"), `extra_rules.json` (20 rules), `eval/make_snapshot.py` (new inputs). Review
  sheets in `chinese_writing_rag_pipeline/review/`: `critique_revisions_review.csv`,
  `triggers/`, `contradictions/`. Built and embedded `base-v5`. Production chunk files
  (`chunks/*.jsonl`) and the live database are untouched until Phase 5.

- **18 Oct -- Phase 2 (first part).** Added `eval/s7/evaluate.py` (accuracy over repeated runs,
  lexical + information consistency, retrieval Jaccard and card reach, attribution) ->
  `eval/reports/S7_<name>.md`. Reuses `eval/v1_vs_v2/score.py`'s parsing and judge; fixes the
  lexical metric (English explanation no longer counted as corrected text). Variant inputs
  (A/B, fixed retrieval) deferred to just before S7-4 -- only the retrieval stages need them.

- **18 Oct -- baseline and S7-0 measured** (`eval/reports/S7_S6-h20.md`, `S7_S7-0.md`; 3 runs each,
  20 stories / 60 scenes; harness now leaves out scenes whose judge prompt OpenAI's content filter
  refuses -- for all runs and stages, list in `eval/s7/out/refused.json`; none so far).
  S6-h20: FP 0.54/scene (0.40-0.72), incorrect 0.41 (0.37-0.48), fully right 70%, recall 75%;
  consistency: lexical 24%, information 62% of places flagged in every run; retrieval identical
  across runs (Jaccard 1.0); **card reach 34%** -- 13 rule cards never reached the prompt at any
  of their places (word_choice 0/48, resultative_complement 0/15, verb_object_collocation 0/14...);
  only pinned cards reach every place (了 29/29). Of her corrections missed or misfixed, ~45 per
  run had no card in the prompt vs ~20 with it -- but ~68 per run were fixed right without
  their card, so this is a pointer, not proof, that retrieval stages will help.
  S7-0 (new data, same code): every accuracy figure within S6's run-to-run range (incorrect
  0.48, at S6's highest run; FP 0.56); lexical 31%, information 64% (+2, within noise);
  孟母 expressiveness 74% vs 67%; card reach 35%. **Verdict: neutral** -- the new data alone does
  not change behaviour, as expected (most of it is only used by later stages). Kept as the base
  for S7-0b onward, since those stages need base-v5.

- **18 Oct -- S7-0b measured** (`eval/reports/S7_S7-0b.md`): pinning her two revised critique cards
  (over-correction, wrong/missing explanation). FP 0.57 (0.48-0.65), incorrect 0.43 (0.38-0.50) --
  lower than S7-0's 0.48 but inside both stages' run-to-run ranges; fully right 69%; information
  consistency 60% (S7-0 64%, S6 62%), same error identified 67% (74%). **Verdict: not accepted**
  (no consistency gain; accuracy within noise). Flag `revisedCritiqueCards` kept for later
  combination; S7-1 re-pointed to extend S7-0. Note: with 3 runs x 60 scenes, differences of a
  few points in consistency are within run-to-run noise.

- **18 Oct -- S7-1 measured** (`eval/reports/S7_S7-1.md`): reasoning effort medium (extends S7-0).
  Information consistency 69% (S7-0 64%, S6 62%), same error identified 77% (74%, 73%), places
  flagged in every run 66% (62%), lexical 33%; incorrect 0.43 (0.40-0.47), FP 0.61 (0.57-0.65,
  under S7-0's highest run 0.62), fully right 70%, recall 77%. Cost: median 30 s per scene vs 22 s
  (+8 s), ~40% more output tokens. **Verdict: accepted (provisionally)** -- the first stage whose
  consistency gain (+5 points) is at the edge of run-to-run noise rather than inside it, with
  accuracy unchanged; FP is at the top of the allowed range, to watch. Later stages extend S7-1.

- **18 Oct -- S7-2 built** (extends S7-1). `lib/rag/promptStages.ts`: flag `citeRules` -- instruction 10
  (every error item ends with `[rule: name]` / `[teacher rule: id]` / `[vocab list]` / `[rule: none]`;
  reuse the cited card's standard fix and terms when it fits); rule cards render her standard fix
  (`formatRuleCard(hit, showStandardFix)`); teacher rules carry ids (`formatTeacherRules(..., showIds)`);
  `RetrievedChunk.standard_fix` type. Production's `retrieve.ts` does not fetch `standard_fix` yet,
  and the app must strip the citation from what learners see (Phase 5). `eval/s7/evaluate.py`: a
  Citations section (items citing a rule that was / was not in the prompt, `[rule: none]`, accuracy
  by citation kind, same citation across runs). Guards: S6, S6-h20, S7-0, S7-1 identical.

- **18 Oct -- S7-2 measured** (`eval/reports/S7_S7-2.md`): **information consistency 77%** (S7-1 69%),
  same error identified 87% (77%), lexical 37% (33%); FP 0.56 (0.48-0.62) vs 0.61; incorrect 0.43
  (0.42-0.45, narrower); fully right 72%; recall 73% (-4, within the 5-point limit). Citations: 99-100%
  of items cite; 0-1 per run cite a rule not in the prompt; ~30% cite [rule: none]; the same rule is
  cited at the same place in every run 77%. Items citing [rule: none] are wrong 21-27% vs 17-19% for
  rule-card citations -- so hiding [rule: none] items (S7-7) would drop ~3x more correct items than
  wrong ones: S7-7 as planned is unlikely to pass. **Verdict: accepted** -- the largest consistency
  gain so far, accuracy unchanged or better. Later stages extend S7-2.

- **18 Oct -- S7-3 measured** (`eval/reports/S7_S7-3.md`): end-of-story scene check. Content notes worded
  "Missing scene:" / "You need to" **100%** (S7-2 43%, S6 49%) -- her explicit request; her flagged scenes
  still caught 98% (44-46 of 46); same verdict for a required scene in all 3 runs 72% (no same-measure
  baseline: earlier stages have no per-scene verdicts; the S6 6-story judge-based figure was 69%).
  The checker is strict: of 360 verdicts only 14% "told", 37% "partly told", 29% "missing", 20% "wrong";
  ~5 notes per story in every stage vs her 46 flags over 20 stories -- the content judge marks ~100% of
  notes correct in every stage, so it cannot tell whether notes go beyond her standard: needs her check.
  **Verdict: accepted** (wording as she asked, nothing lost). Learners see only the notes (D4).
  **Noise check:** S7-3's scene prompts are byte-identical to S7-2's, so their scene numbers differ only
  by chance: information consistency 77% vs 71%, same error 87% vs 80%, FP 0.56 vs 0.49. Run-to-run
  noise on these is ~6 points, more than assumed. Pooling the 6 runs, the S7-2 configuration gives
  information consistency ~74% and same error ~83% vs S7-1's 69% / 77% -- still a gain, about half
  what S7-2 alone suggested. From here, judge a stage on its pooled runs where prompts repeat, and
  treat differences under ~6 points as noise.

- **18 Oct -- S7-4 built** (extends S7-3). Data: `raw/iteration data/rule_card_triggers.json` -- 14
  regex triggers on 5 rule cards (word_choice, resultative_complement, verb_object_collocation,
  word_class_misuse, time_expression), the `suggested_keep=yes` rows of `review/triggers/` (>=50% of
  training matches at her corrections), taken over **provisionally, unreviewed**; `chunk_builder.py`
  attaches them as rule-card metadata `triggers`; snapshot `base-v6` = base-v5 + those triggers (no
  text change, embeddings reused). Code: flag `ruleCardTriggers` -- a matching trigger adds its card
  (with the matched places listed) and one past correction labelled with that rule, nearest to the
  matched sentence (`grammarTag` filter). Offline check (no LLM): card reach 35% -> 43%
  (word_choice 0 -> 6/48, resultative_complement 0 -> 4/15, word_class_misuse 0 -> 3/7), +0.2 cards
  per scene. Production's `getChunksByType` does not return `grammar_tag` -- Phase 5.

- **18 Oct -- S7-4 measured** (`eval/reports/S7_S7-4.md`). Whole set: FP 0.43 (0.37-0.48), the lowest of
  any stage; incorrect 0.42; fully right 72%; recall 72%; card reach 43% (35%); information consistency
  67%, same error 74% (down). **Split by scene** (S7-4's prompt differs from S7-3's only in the 18 scenes
  where a trigger fired; the other 42 are byte-identical): in triggered scenes FP fell 0.81 (S7-2) /
  0.61 (S7-3) -> 0.43 and consistency held (information 75% vs 77/72%); in identical scenes FP was
  flat (0.45/0.44/0.43) and information consistency fell 78/71 -> 62% -- pure noise, since nothing
  changed there. So the triggers cut false positives where they apply and did not hurt consistency;
  the overall consistency drop is noise (larger than estimated: up to 16 points on 42 scenes).
  **Verdict: accepted.** Lesson for the harness: report effects on the scenes a stage changed,
  against the same scenes in the previous stage (`--changed-only`, to add).

- **18 Oct -- harness: accuracy split + variant consistency.** `eval/s7/evaluate.py` adds "Accuracy split":
  lexical accuracy (corrected text is hers, any alternative) and information accuracy (right fix, clean
  text) at her corrections; retrieval accuracy (card reach) x generation accuracy given the card / without
  it. S6-h20 vs S7-4: reach 34% -> 43%; caught-and-right given the card ~70% both, without it ~60%;
  information accuracy 72-76% -> 76-78%; lexical 26-29% -> 32%. New `eval/s7/variants.mjs` +
  `variants_score.py` (Phase 2's deferred variant inputs): per target error, the scene with her other
  corrections applied (target kept verbatim), run once with the original's retrieval (fixed:
  generation only) and with its own (end-to-end); scored against original run 1, with run 2 as the
  noise floor -> `eval/reports/S7_variants_<stage>.md` (a. retrieval Jaccard + card reach, b. generation,
  c. end-to-end; lexical + information; accuracy at the target). Running for S7-4 and S6-h20.

- **18 Oct -- S7-5 built** (extends S7-4, snapshot base-v6). Flag `ruleExamples`: each sentence of the scene
  is searched against the 920 `rule_example` chunks (student sentences she corrected, `parent_id` = their
  rule card); the cards of the top 2 matches per sentence are added (at most 4 new cards per scene), each
  shown with the closest corrected sentence and "check whether the scene really has the same error".
  Offline, card reach: S7-4 43% -> **72%** (+3.4 cards/scene, prompt +17%); for comparison, more
  whole-scene similarity slots give 48% (+4 cards) / 60% (+8 cards) -- per-sentence matching on her
  corrected sentences is ~3x more efficient per added card. Settings chosen from a no-LLM sweep
  (top 1/2/3 per sentence x cap 2/4/6/all: 57-82%). Also added: stage `S0-h20` (+r2, r3) -- the floor,
  S0's prompt and flags on base-v4-h20 and the 20 stories; `score.py` parses S0's original output format.
  Variant runs queued for S0-h20, S6-h20, S7-0, S7-0b, S7-1, S7-2, S7-4 (S7-3 skipped: scene prompts
  identical to S7-2's).

- **18 Oct -- S7-5 measured** (`eval/reports/S7_S7-5.md`): card reach 72% (S7-4 43%); recall 75% (72%);
  information accuracy at her corrections 76-81% (76-78%); same error identified 79% (75%); but **false
  positives 0.53/scene (0.47-0.62) vs S7-4's 0.43 (0.37-0.48)** -- back to S6's level -- with incorrect
  corrections and items fully right unchanged. **Verdict: rejected** (false positives are her top priority).
  S7-4 remains the accepted configuration; flag `ruleExamples` kept, off. Likely cause: the extra
  material (+3.4 cards per scene, and near-identical corrected sentences shown on the cards) invites
  flagging. Next (S7-6, redefined): keep the prompt size constant -- per-sentence rule_example
  matches REPLACE the 4 whole-scene similarity cards instead of adding cards, and no example
  sentences are shown -- to test whether better-targeted retrieval helps without the extra material.

- **18-19 Oct -- floor and variants.** `S0-h20` (no teacher input, 20 stories): FP 1.27/scene, incorrect 0.57,
  fully right 58%, recall 92%, card reach 17%, flagged missing scenes caught 25%. Variant reports
  (`eval/reports/S7_variants_<stage>.md`, 156 target errors): retrieval Jaccard original vs variant S0 0.81 ->
  S7-4 0.95; information consistency, rerun noise floor / generation-only / end-to-end: S0 65/69/65%,
  S7-4 72/75/73%; lexical 22/17/22% -> 38/34/45%; lexical accuracy (her exact fix) 8-10% -> 29-32%. In both,
  generation-only and end-to-end sit at the rerun noise floor: changing the surrounding text (and the
  retrieval it brings) does not make answers less consistent than rerunning; what is left is model
  randomness. Fixed: `eval/lib.mjs` embedding cache -- parallel runs could save different API vectors
  for the same text (last writer won); now the first saved vector wins (re-read before embedding,
  merge on save, atomic writes). S7-5's guard reports one changed scene because of that race (its runs
  used the other vector); no verdict depends on it.

## Decisions

- **D1 (18 Oct): 20 held-out stories.** S6 re-baselined on `base-v4-h20`.
- **D2 (18 Oct): keep S6's sections**, Grammar & Vocabulary combined; vocabulary suggestions in
  their own section, no "(suggestion)" tag in the corrections list.
- **D3 (18 Oct): triggers go to `chinese_writing_rag_pipeline/review/triggers/`** for review;
  sent on to her if needed.
- **D4 (18 Oct): what learners see at END STORY** -- only a bulleted list of the missed content (the
  "Content & Completeness" notes). The "Scene check" section from S7-3 is internal: kept in the stored
  feedback for analysis, stripped by the app before display (Phase 5). The evaluation already judges
  only the "Content & Completeness" notes, so scoring is unaffected. No scene numbers: bullets never say
  "Scene 2:" or number the required scenes; where content belongs is described by the surrounding
  events (already required by `noSceneNumbers`, inherited by every S7 stage). Phase 5: the content route
  streams the model's text straight to the learner, so hiding the Scene check means buffering until
  "## Content & Completeness" starts, or producing the verdicts in a separate call.
- **D6 (19 Oct): no rule citations or Scene check in anything people read.** Learners and the teacher
  never see `[rule: ...]` / `[teacher rule: ...]` / `[vocab list]` or the "## Scene check" section. They stay
  in the raw feedback stored in the run JSON (and, in the app, in the stored scene record) for evaluation.
  Removed by `lib/rag/displayFeedback.ts` (`feedbackForDisplay`, for the app in Phase 5) and by the same
  rules in `eval/export_feedback.py` (review markdown; all S7 feedback folders re-exported).
- **D5 (18 Oct): consistency vs accuracy.** A consistency drop is acceptable when accuracy rose,
  especially when the stage changed nothing the measure depends on (e.g. S7-3 changed only the
  end-of-story prompt). Accuracy (her priority: no false positives / incorrect corrections) wins.
