# Reviewing the regex triggers

A trigger is a pattern matched against the student's text. When it matches, the
model is shown the rule with the place it matched, as something **to check** --
never as an error by itself. Triggers make the same rule reach every story that
has the pattern (today rule cards are found only by similarity to the whole
scene, so the 不是…而是 card reached 2 of the 6 test scenes that contain it).

`triggers_review.csv` lists 22 triggers proposed for 9 rule cards
(from her corrections on 87 training stories; 14 suggested)
and the 27 triggers of her teacher rules (12 marked "check").

## Columns

| Column | Meaning |
|---|---|
| kind | `rule_card (proposed)`: mined from her corrections; `teacher_rule`: in use in `extra_rules.json`; `teacher_rule (pending review)`: drafted for her new rules but held back (precision below 0.5) until reviewed -- the rule itself is still shown to the model, without "check here" pointers |
| rule | the rule card / teacher rule the trigger points to |
| trigger_regex | the pattern (a literal string unless it contains `[...]`, `(?:...)` etc.) |
| from_n_stories | proposed: how many stories her corrections with this pattern come from |
| fires | matches in the students' original texts (training stories) |
| at_her_edit | ... of which at a place she corrected |
| at_this_rule | ... of which at a correction labelled with this rule |
| precision | at_her_edit / fires -- how often a match is at a real error |
| in_corrected | matches left after her corrections are applied (pattern survives her fix) |
| in_model | matches in the native model stories (should be 0) |
| examples | up to 3 matches in context; ✓ = at a place she corrected, ✗ = not |
| suggested_keep | proposed: yes if at_this_rule >= 2, precision >= 0.5 and in_model = 0; teacher rules: "check" if below that |

## What to do

Fill **KEEP (yes/no)** for each row (leave blank to accept `suggested_keep`), and
NOTE anything worth telling her. Low precision is not always bad: a hint that
fires often at correct text costs the model attention and risks false positives,
which she cares about most -- prefer `no` when unsure. Then tell Claude; the kept
rule-card triggers go into `raw/iteration data/rule_card_triggers.json` and into
the snapshot for stage S7-4.
