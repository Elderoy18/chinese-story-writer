# Variant consistency: S7-4

156 target errors (her corrections on the 20 test stories that share a scene with at least one other of her corrections). Each variant = the scene with her OTHER corrections applied; the target error is kept word for word. Stage `S7-4`, snapshot `base-v6`; one run per variant and mode.

## a. Retrieval (original scene vs variant, each doing its own retrieval)

- Jaccard of retrieved chunk ids: mean 0.95, median 0.96, min 0.83; identical sets 35/156 (22%)
- Card reach for the target's rule card: original 67/155 (43%), variant 64/155 (41%); same outcome in both 150/155 (97%)

## b, c. Consistency at the target error

| Compared with original run 1 | Same decision (flag / no flag) | Lexical (both flagged: identical text) | Information (both flagged: same error, equivalent fix) |
|---|---|---|---|
| original run 2 -- nothing changed (noise floor) | 134/156 (86%) | 41/109 (38%) | 78/108 (72%) |
| **b. variant, fixed retrieval** -- generation only | 138/156 (88%) | 39/114 (34%) | 85/113 (75%) |
| **c. variant, own retrieval** -- end-to-end | 136/156 (87%) | 50/111 (45%) | 81/111 (73%) |

## Accuracy at the target error

| Output | Target caught | Lexical accuracy (her fix) | Information accuracy (right fix, clean text) |
|---|---|---|---|
| original scene, run 1 | 122/156 (78%) | 46/156 (29%) | 99/156 (63%) |
| variant, fixed retrieval (generation) | 124/156 (79%) | 50/156 (32%) | 102/156 (65%) |
| variant, own retrieval (end-to-end) | 120/156 (77%) | 47/156 (30%) | 100/156 (64%) |

Reading: if b is close to the noise floor, the model is consistent when only the surrounding text changes; if c is clearly below b, retrieval changes with the input are what make the answer change.
