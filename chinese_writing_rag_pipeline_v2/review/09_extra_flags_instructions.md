# Places flagged that the teacher did not mark

The automatic checkers were run on the 20 test stories, and they flagged 155 places that the
teacher's own corrections do not mark. Some of these are likely real errors that were simply not
marked; others are things the teacher accepts. Her judgment on each place shows how often the
checkers are right, and teaches the system which kinds of flags to keep and which to drop.

## The sheet: `09_extra_flags.csv` (opens in Excel)

One row per flagged place, story by story in reading order.

| Column | Meaning |
|---|---|
| story | the student story |
| sentence_with_flag | the clause, with the flagged text in 【 】 (【^】 marks a place where something may be missing) |
| flagged_text | the student's words that were flagged |
| suggested_corrections | the correction(s) proposed: [+X] add X, [-X] delete X, [A→B] replace A with B |
| reasons_given | the checker's short reason, where it gave one |
| flagged_by | which checker flagged it: the AI checker (and in how many of its 3 tries), the correction model, or both |

## What to fill in

- **TEACHER_DECISION**: `error` (a real error that should be corrected), `not an error`, or `unsure`.
- **TEACHER_CORRECTION** (optional): her own correction, if it differs from the suggested ones.
- **TEACHER_NOTE** (optional): anything worth recording, e.g. "acceptable for this level" or "style only".

Places flagged by both checkers, or by the AI checker in all 3 tries, are the most likely to be real
errors; places flagged only once are the least certain. Rows already filled in are kept if the sheet
is rebuilt.
