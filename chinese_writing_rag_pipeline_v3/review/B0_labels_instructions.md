# Judging the corrections (B0_labels.csv)

Each row is one correction the system would show a student: the student's sentence, the corrected
sentence, and the errors in it with their categories.

- **VERDICT**: `right` -- a real error and the corrected sentence is correct; `correction wrong` -- there is
  an error, but the corrected sentence is wrong or still contains an error; `not an error` -- the original
  was fine.
- **CATEGORY_OK**: `yes` if every error is in the right category, `no` otherwise (a note on which is welcome).
- **NOTE**: anything else, in any language.

The answers are kept and reused: a correction judged once is not asked again in later rounds.
