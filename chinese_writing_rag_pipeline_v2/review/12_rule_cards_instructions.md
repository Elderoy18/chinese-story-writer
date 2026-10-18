# Error categories and rule cards: what to check

The teacher's corrections on the practice stories were sorted into 61 categories, built from her own
notes and terminology, and one rule card was drafted for each. When the feedback system flags an
error, it looks up the card of that category: the card helps decide whether the flag is a real error
of that kind, and the explanation the learner sees follows the card. Every example on a card is one
of her own corrections.

- `12_rule_cards.md` -- the categories and cards, readable, grouped by dimension.
- `12_rule_cards_review.csv` -- the same, one row per category, with columns for her decisions.

## What to fill in (in the .csv)

- **CATEGORY_DECISION**: `keep`, `rename`, `merge with <category_id>`, `split` (how, in the note), or `remove`.
- **CARD_DECISION**: `approve`, or `edit` (her wording in TEACHER_WORDING).
- **TEACHER_WORDING** (optional): her preferred name, rule, or explanation.
- **TEACHER_NOTE** (optional): anything else -- an example that is a poor choice, a rule missing from
  the list, or a case that should not be flagged.

Points worth particular attention: whether the rule is stated the way she would explain it to a
beginner, whether the examples are typical, and the "not an error under this rule" line, which keeps
the system from flagging acceptable Chinese. Rows already filled in are kept if the sheet is rebuilt.
