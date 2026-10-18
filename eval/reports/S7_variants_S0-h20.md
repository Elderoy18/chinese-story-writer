# Variant consistency: S0-h20

156 target errors (her corrections on the 20 test stories that share a scene with at least one other of her corrections). Each variant = the scene with her OTHER corrections applied; the target error is kept word for word. Stage `S0-h20`, snapshot `base-v4-h20`; one run per variant and mode.

## a. Retrieval (original scene vs variant, each doing its own retrieval)

- Jaccard of retrieved chunk ids: mean 0.81, median 0.75, min 0.27; identical sets 68/156 (44%)
- Card reach for the target's rule card: original 26/155 (17%), variant 26/155 (17%); same outcome in both 151/155 (97%)

## b, c. Consistency at the target error

| Compared with original run 1 | Same decision (flag / no flag) | Lexical (both flagged: identical text) | Information (both flagged: same error, equivalent fix) |
|---|---|---|---|
| original run 2 -- nothing changed (noise floor) | 145/156 (93%) | 29/134 (22%) | 87/134 (65%) |
| **b. variant, fixed retrieval** -- generation only | 145/156 (93%) | 23/137 (17%) | 94/137 (69%) |
| **c. variant, own retrieval** -- end-to-end | 146/156 (94%) | 30/138 (22%) | 89/137 (65%) |

## Accuracy at the target error

| Output | Target caught | Lexical accuracy (her fix) | Information accuracy (right fix, clean text) |
|---|---|---|---|
| original scene, run 1 | 144/156 (92%) | 16/156 (10%) | 112/156 (72%) |
| variant, fixed retrieval (generation) | 141/156 (90%) | 12/156 (8%) | 111/156 (71%) |
| variant, own retrieval (end-to-end) | 142/156 (91%) | 15/156 (10%) | 114/156 (73%) |

Reading: if b is close to the noise floor, the model is consistent when only the surrounding text changes; if c is clearly below b, retrieval changes with the input are what make the answer change.
