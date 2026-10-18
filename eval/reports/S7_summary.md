# S7 statistical summary (20 test stories, 60 scenes)

Each cell: mean ± standard deviation (lowest–highest) over the runs (3 per stage; S7-4: 6, two sets of 3). Judged against her answer key (`eval/test_set_h20.json`) by the judge of `eval/v1_vs_v2/score.py`. Made by `eval/s7/summary.py`.

## Accuracy (her order of priority)

| Stage | Verdict | False positives / scene | Incorrect corrections / scene | Items fully right | Corrected text not fully correct | Recall |
|---|---|---|---|---|---|---|
| S0 (floor: no teacher input) | floor | 1.27 ± 0.04 (1.23–1.32) | 0.57 ± 0.05 (0.52–0.62) | 58% ± 1 (57%–60%) | 11% ± 1 (10%–12%) | 92% ± 2 (90%–94%) |
| S6 (previous system) | baseline | 0.54 ± 0.16 (0.40–0.72) | 0.41 ± 0.07 (0.37–0.48) | 70% ± 3 (68%–73%) | 17% ± 2 (15%–19%) | 75% ± 2 (73%–77%) |
| S7-0 new data | neutral, kept | 0.56 ± 0.06 (0.50–0.62) | 0.48 ± 0.11 (0.40–0.60) | 70% ± 3 (67%–72%) | 15% ± 1 (14%–16%) | 76% ± 4 (73%–80%) |
| S7-0b + revised critique cards | not accepted | 0.57 ± 0.08 (0.48–0.65) | 0.43 ± 0.06 (0.38–0.50) | 69% ± 3 (66%–72%) | 16% ± 0 (16%–16%) | 75% ± 1 (74%–77%) |
| S7-1 + reasoning effort medium | accepted | 0.61 ± 0.04 (0.57–0.65) | 0.43 ± 0.03 (0.40–0.47) | 70% ± 1 (69%–71%) | 16% ± 1 (15%–16%) | 77% ± 2 (74%–79%) |
| S7-2 + rule citations, standard fixes | accepted | 0.56 ± 0.07 (0.48–0.62) | 0.43 ± 0.02 (0.42–0.45) | 72% ± 2 (70%–73%) | 14% ± 1 (13%–15%) | 73% ± 5 (68%–77%) |
| S7-3 + end-of-story scene check | accepted | 0.49 ± 0.07 (0.42–0.55) | 0.41 ± 0.05 (0.37–0.47) | 74% ± 0 (74%–74%) | 13% ± 1 (11%–14%) | 73% ± 2 (71%–76%) |
| S7-4 + rule-card triggers | accepted | 0.51 ± 0.13 (0.37–0.75) | 0.43 ± 0.04 (0.37–0.48) | 71% ± 2 (69%–75%) | 16% ± 2 (13%–18%) | 73% ± 2 (71%–76%) |
| S7-5 + cards via corrected sentences (added) | rejected | 0.53 ± 0.08 (0.47–0.62) | 0.42 ± 0.03 (0.38–0.43) | 72% ± 4 (68%–75%) | 15% ± 3 (12%–18%) | 75% ± 1 (74%–76%) |
| S7-6 cards via corrected sentences (replacing) | pending tie-break | 0.46 ± 0.03 (0.43–0.48) | 0.43 ± 0.11 (0.33–0.55) | 72% ± 2 (70%–73%) | 16% ± 2 (14%–18%) | 72% ± 3 (70%–76%) |

## Display, categories, content, expressiveness

| Stage | Partial sentences | Wrong category | Her flagged scenes caught | Notes in her wording | Good ideas 孟母 | Good ideas 神农 |
|---|---|---|---|---|---|---|
| S0 (floor: no teacher input) | 3% ± 1 (2%–3%) | 20% ± 1 (18%–21%) | 25% ± 3 (22%–26%) | 79% ± 10 (72%–91%) | – | – |
| S6 (previous system) | 7% ± 2 (6%–10%) | 7% ± 1 (6%–8%) | 99% ± 1 (98%–100%) | 49% ± 3 (47%–53%) | 67% ± 3 (65%–70%) | 83% ± 6 (80%–90%) |
| S7-0 new data | 7% ± 1 (6%–8%) | 6% ± 2 (4%–7%) | 99% ± 1 (98%–100%) | 49% ± 5 (43%–52%) | 74% ± 3 (71%–77%) | 81% ± 6 (76%–88%) |
| S7-0b + revised critique cards | 7% ± 2 (5%–8%) | 6% ± 2 (3%–8%) | 99% ± 1 (98%–100%) | 50% ± 8 (41%–57%) | 74% ± 1 (74%–75%) | 84% ± 3 (81%–87%) |
| S7-1 + reasoning effort medium | 7% ± 1 (6%–8%) | 4% ± 1 (3%–5%) | 99% ± 1 (98%–100%) | 47% ± 4 (43%–51%) | 67% ± 3 (65%–71%) | 83% ± 0 (83%–83%) |
| S7-2 + rule citations, standard fixes | 8% ± 1 (8%–9%) | 4% ± 1 (4%–5%) | 99% ± 1 (98%–100%) | 43% ± 2 (41%–45%) | 68% ± 2 (65%–69%) | 82% ± 6 (75%–87%) |
| S7-3 + end-of-story scene check | 7% ± 3 (4%–11%) | 5% ± 1 (4%–6%) | 98% ± 2 (96%–100%) | 100% ± 0 (100%–100%) | 75% ± 1 (74%–76%) | 82% ± 3 (78%–85%) |
| S7-4 + rule-card triggers | 8% ± 2 (5%–9%) | 5% ± 1 (4%–7%) | 99% ± 1 (98%–100%) | 100% ± 0 (100%–100%) | 70% ± 3 (66%–73%) | 80% ± 5 (71%–87%) |
| S7-5 + cards via corrected sentences (added) | 8% ± 2 (5%–10%) | 7% ± 1 (5%–7%) | 99% ± 1 (98%–100%) | 100% ± 0 (100%–100%) | 72% ± 4 (69%–77%) | 83% ± 2 (81%–85%) |
| S7-6 cards via corrected sentences (replacing) | 7% ± 1 (7%–9%) | 6% ± 1 (4%–7%) | 99% ± 1 (98%–100%) | 100% ± 0 (100%–100%) | 73% ± 6 (67%–79%) | 82% ± 5 (77%–87%) |

## Retrieval and consistency across the 3 runs of a set (same input, same retrieval)

| Stage (set) | Card reach | Information consistency | Same error identified | Lexical consistency | Places flagged in every run |
|---|---|---|---|---|---|
| S0 (floor: no teacher input) | 17% | 61% | 71% | 14% | 78% |
| S6 (previous system) | 34% | 62% | 73% | 24% | 65% |
| S7-0 new data | 35% | 64% | 74% | 31% | 62% |
| S7-0b + revised critique cards | 35% | 60% | 67% | 26% | 62% |
| S7-1 + reasoning effort medium | 35% | 69% | 77% | 33% | 66% |
| S7-2 + rule citations, standard fixes | 35% | 77% | 87% | 37% | 63% |
| S7-3 + end-of-story scene check | 35% | 71% | 80% | 31% | 63% |
| S7-4 + rule-card triggers | 43% | 67% | 75% | 30% | 62% |
| S7-4 + rule-card triggers (set 2) | 43% | 69% | 81% | 33% | 62% |
| S7-5 + cards via corrected sentences (added) | 72% | 66% | 79% | 26% | 66% |
| S7-6 cards via corrected sentences (replacing) | 61% | 75% | 84% | 35% | 64% |

## Variant inputs: the same error in a different context (156 target errors)

Retrieval Jaccard = chunks shared by the original scene and its variant. Consistency at the target error vs original run 1: same flag decision / lexical / information.

| Stage | Retrieval Jaccard | Rerun (noise floor) | b. Generation only (fixed retrieval) | c. End-to-end (own retrieval) |
|---|---|---|---|---|
| S0 (floor: no teacher input) | 0.81 | 93% / 22% / 65% | 93% / 17% / 69% | 94% / 22% / 65% |
| S6 (previous system) | 0.95 | 82% / 33% / 69% | 83% / 30% / 69% | 87% / 33% / 68% |
| S7-0 new data | 0.96 | 87% / 42% / 68% | 89% / 34% / 69% | 83% / 38% / 70% |
| S7-4 + rule-card triggers | 0.95 | 86% / 38% / 72% | 88% / 34% / 75% | 87% / 45% / 73% |

## Reading the numbers

- Run-to-run noise is large: S7-4's two sets of 3 runs (identical prompts) gave false positives 0.43 and 0.59 per scene. Differences in false positives smaller than ~0.1 per scene between stages measured with 3 runs each are not evidence either way.
- Consistency differences of a few points are also within noise (identical-prompt stages S7-2 / S7-3 differed by 6 points).
- Card reach and retrieval Jaccard are deterministic (no model randomness).
