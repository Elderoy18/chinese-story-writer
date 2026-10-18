# Content check: places where the checker and the teacher's flags disagree

For each test story, an automatic content check went through the teacher's list of required scenes
and decided whether each scene is told, partly told, or missing. Most of its decisions match the
teacher's "Miss ... scene" notes. The sheet `11_b0_content_review.csv` lists the 37 cases where they do
not, so that the teacher can say which reading is right.

| Column | Meaning |
|---|---|
| story | the student story |
| required_scene | the scene from the teacher's scene list |
| teacher_flag | what the teacher's notes on this story say about the scene |
| checker_verdict | what the content check decided (the most common answer over its 3 tries) |
| checker_runs | its answer in each of the 3 tries |
| student_words_used | the student's words the check relied on, if any |
| what_checker_says_is_missing | the part of the scene the check found missing |

## What to fill in

- **TEACHER_DECISION**: `told`, `partly told`, or `missing` -- the right verdict for this scene in this story.
- **TEACHER_NOTE** (optional): e.g. "half-told scenes are not flagged at this level", or "the student's version counts".

The answers show whether the check is too strict or too lenient, and how half-told scenes should be
treated. Rows already filled in are kept if the sheet is rebuilt.
