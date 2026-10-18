# Variant consistency: S7-0

156 target errors (her corrections on the 20 test stories that share a scene with at least one other of her corrections). Each variant = the scene with her OTHER corrections applied; the target error is kept word for word. Stage `S7-0`, snapshot `base-v5`; one run per variant and mode.

## a. Retrieval (original scene vs variant, each doing its own retrieval)

- Jaccard of retrieved chunk ids: mean 0.96, median 0.96, min 0.83; identical sets 37/156 (24%)
- Card reach for the target's rule card: original 57/155 (37%), variant 57/155 (37%); same outcome in both 153/155 (99%)

## b, c. Consistency at the target error

| Compared with original run 1 | Same decision (flag / no flag) | Lexical (both flagged: identical text) | Information (both flagged: same error, equivalent fix) |
|---|---|---|---|
| original run 2 -- nothing changed (noise floor) | 135/156 (87%) | 47/111 (42%) | 76/111 (68%) |
| **b. variant, fixed retrieval** -- generation only | 139/156 (89%) | 40/117 (34%) | 81/117 (69%) |
| **c. variant, own retrieval** -- end-to-end | 130/156 (83%) | 41/109 (38%) | 76/109 (70%) |

## Accuracy at the target error

| Output | Target caught | Lexical accuracy (her fix) | Information accuracy (right fix, clean text) |
|---|---|---|---|
| original scene, run 1 | 123/156 (79%) | 38/156 (24%) | 100/156 (64%) |
| variant, fixed retrieval (generation) | 128/156 (82%) | 42/156 (27%) | 102/156 (65%) |
| variant, own retrieval (end-to-end) | 121/156 (78%) | 40/156 (26%) | 94/156 (60%) |

Reading: if b is close to the noise floor, the model is consistent when only the surrounding text changes; if c is clearly below b, retrieval changes with the input are what make the answer change.
