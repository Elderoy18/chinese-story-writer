# Corrections that go in opposite directions

`opposite_fixes.csv` lists 11 patterns where her corrections on the
training stories go both ways in the same context: adding a character after a
word in one story and removing it after the same word in another, or changing
A to B in one place and B to A in another. Each row shows up to three examples
of each direction (the student's clause -> her fix, her note, the rule labels).

These are her real corrections, so both directions are usually right -- for
different reasons. When both are retrieved for the same scene, the model sees
what looks like a contradiction. For each row, fill in what decides it (e.g.
"了 after 告诉 only when no quoted speech follows"); that condition can then be
added to the rule card or teacher rule, so the model applies it the same way
every time. Leave blank if it is unclear; send the unclear ones to her.
