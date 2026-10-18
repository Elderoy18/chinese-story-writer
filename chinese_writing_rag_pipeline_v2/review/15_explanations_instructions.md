# Feedback explanations: quality check

For every error the system finds, the learner sees a correction and a short English explanation, written
from the teacher's rule card for that kind of error and her own past corrections of similar errors. The
sheet `15_explanations_review.csv` holds a sample of 60 of these from the test stories: half at places the
teacher also corrected, half at places she did not mark. Items shown as "suggestion" are worded as a
possible improvement rather than a mistake.

| Column | Meaning |
|---|---|
| student_clause | the learner's clause, with the problem marked 【 】 (【^】: something is missing here) |
| correction | the correction shown |
| explanation_shown_to_learner | the explanation exactly as the learner would see it |
| shown_as | error, or suggestion |
| her_marking | whether the teacher corrected this place in her own feedback |

## What to fill in

- **TEACHER_RATING**: `good`, `acceptable`, `wrong rule` (the explanation gives the wrong reason),
  `wrong correction`, or `not an error`.
- **TEACHER_BETTER_EXPLANATION** (optional): how she would explain it.
- **TEACHER_NOTE** (optional): anything else, e.g. "too long", "too technical", "should be a suggestion".

Rows already filled in are kept if the sheet is rebuilt.
