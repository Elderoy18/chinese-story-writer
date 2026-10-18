# Variant consistency: S6-h20

156 target errors (her corrections on the 20 test stories that share a scene with at least one other of her corrections). Each variant = the scene with her OTHER corrections applied; the target error is kept word for word. Stage `S6-h20`, snapshot `base-v4-h20`; one run per variant and mode.

## a. Retrieval (original scene vs variant, each doing its own retrieval)

- Jaccard of retrieved chunk ids: mean 0.95, median 0.95, min 0.78; identical sets 35/156 (22%)
- Card reach for the target's rule card: original 54/155 (35%), variant 54/155 (35%); same outcome in both 151/155 (97%)

## b, c. Consistency at the target error

| Compared with original run 1 | Same decision (flag / no flag) | Lexical (both flagged: identical text) | Information (both flagged: same error, equivalent fix) |
|---|---|---|---|
| original run 2 -- nothing changed (noise floor) | 128/156 (82%) | 36/108 (33%) | 75/108 (69%) |
| **b. variant, fixed retrieval** -- generation only | 129/156 (83%) | 33/110 (30%) | 75/109 (69%) |
| **c. variant, own retrieval** -- end-to-end | 135/156 (87%) | 38/115 (33%) | 77/114 (68%) |

## Accuracy at the target error

| Output | Target caught | Lexical accuracy (her fix) | Information accuracy (right fix, clean text) |
|---|---|---|---|
| original scene, run 1 | 124/156 (79%) | 37/156 (24%) | 90/156 (58%) |
| variant, fixed retrieval (generation) | 123/156 (79%) | 41/156 (26%) | 102/156 (65%) |
| variant, own retrieval (end-to-end) | 127/156 (81%) | 39/156 (25%) | 99/156 (63%) |

Reading: if b is close to the noise floor, the model is consistent when only the surrounding text changes; if c is clearly below b, retrieval changes with the input are what make the answer change.
