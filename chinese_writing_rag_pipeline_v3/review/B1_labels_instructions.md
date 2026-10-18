# Judging the corrections (B1_labels.csv)

Each row is one correction the system would show a student: its category, the student's words, the
corrected words and the explanation.

- **VERDICT**: `right` -- a real error and the correction is right; `correction wrong` -- there is an error,
  but the corrected words are wrong or still contain an error; `not an error` -- the original was fine.
- **CATEGORY_OK**: `yes` if the category is right, `no` otherwise.
- **EXPLANATION_OK**: `yes` if the explanation says correctly what is wrong and why, `no` otherwise.
- **NOTE**: anything else, in any language.

The answers are kept and reused: a correction judged once is not asked again in later rounds.
