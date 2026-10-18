#!/usr/bin/env python3
"""Step 12 -- one rule card per category: the teacher's rule, how to explain
the error to a learner, and her clearest examples. These are what the judging
and explanation steps retrieve for a candidate error of that category.

    data/11_categories/taxonomy.json, edits_train.jsonl
        ->  data/12_rule_cards/cards.json
            review/12_rule_cards.md                     the cards, readable (teacher)
            review/12_rule_cards_review.csv             categories + cards, for approval
            review/12_rule_cards_instructions.md

    python scripts/12_rule_cards.py

Built from the TRAIN edits only. For each category the LLM sees the category
definition, every note she wrote on corrections in it (with counts), and up to
MAX_SHOWN of her corrections in it (her notes first). It writes:
  rule                  1-2 sentences, her terminology, learner level
  explanation_template  how one error of this kind is explained to a learner
  examples              3-5 of HER corrections, chosen by id from those shown
                        (never invented), each with a one-line explanation
                        that follows her note when she wrote one
  not_an_error          where the rule does NOT apply, if her notes or examples
                        show it (helps the judging step reject false flags)
Code adds, from the edits themselves: how many corrections the category has,
and its most common HanLP edit shapes (e.g. "insert 了 after VV") -- the
starting point for writing a pattern or parser check.

The review sheet holds both decisions for each category: the category itself
(keep / rename / merge / split / remove) and its card (approve / edit).
"""
import csv
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from llm import api_key, cached_json_call

ROOT = Path(__file__).resolve().parent.parent
CATS = ROOT / "data" / "11_categories"
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
OUT_DIR = ROOT / "data" / "12_rule_cards"
CACHE = OUT_DIR / "cache"
DOC = ROOT / "review" / "12_rule_cards.md"
SHEET = ROOT / "review" / "12_rule_cards_review.csv"
INSTRUCTIONS = ROOT / "review" / "12_rule_cards_instructions.md"

MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"
MAX_SHOWN = 30
WORKERS = 8
DIMENSION = {"grammar": "Grammar", "word_choice": "Vocabulary (word choice)", "coherence_reference": "Coherence: reference",
             "coherence_temporality": "Coherence: temporality", "coherence_connectors": "Coherence: connectors",
             "content": "Content", "other": "Other"}

SYSTEM = """You write one rule card for a Chinese teacher's feedback system. The card covers one category of her corrections of beginner learners' narrative writing. The system uses the card to decide whether a flagged error belongs to this rule and to explain the error to the learner the way she would.

You receive the category, every note she wrote on corrections in it (with counts), and some of her corrections in it ([+X] add X, [-X] delete X, [A→B] replace A with B, ⟦X⟧ a comment about X), each with an id.

Write:
- rule: one or two sentences stating the rule, in her terminology and shorthand (了completed, 在+Place, V. + directional complement + Place + 来/去), simple enough for a beginner.
- explanation_template: how ONE error of this kind is explained to a learner, as a short pattern with slots in angle brackets, e.g. "<wrong> → <correct>: <action> is finished, so it takes 了 (了completed)." English prose; Chinese only for the words, particles and formulas themselves.
- examples: 3 to 5 of HER corrections, by their id, that best show the rule -- clear, short, different from each other; prefer ones with her note. For each, a one-line English explanation in the template's style that follows her note when she wrote one. Never invent an example.
- not_an_error: one or two sentences on when this rule does NOT apply or what should NOT be flagged under it -- only if her notes, her examples or the category definition show it; otherwise "".
- her_terms: the shorthand terms she uses for this rule (from her notes), [] if none.
Do not add rules or claims beyond what her notes and corrections support."""

SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["rule", "explanation_template", "examples", "not_an_error", "her_terms"],
    "properties": {
        "rule": {"type": "string"}, "explanation_template": {"type": "string"},
        "examples": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                                 "required": ["edit_id", "explanation"],
                                                 "properties": {"edit_id": {"type": "string"}, "explanation": {"type": "string"}}}},
        "not_an_error": {"type": "string"},
        "her_terms": {"type": "array", "items": {"type": "string"}},
    },
}


def show(text, e):
    s, t = e["start"], e["end"]
    lo = max(text.rfind("，", 0, s), text.rfind("。", 0, s)) + 1
    ends = [i for i in (text.find("，", t), text.find("。", t)) if i >= 0]
    hi = min(ends) if ends else len(text)
    mid = {"comment": f"⟦{text[s:t]}⟧", "insert": f"[+{e['corrected']}]", "delete": f"[-{e['original']}]"}.get(
        e["op"], f"[{e['original']}→{e['corrected']}]")
    return text[lo:s] + mid + text[t:hi]


def shape(e):
    """A coarse edit shape for counting: 'insert 了 after VV', 'delete PN', 'replace VV -> VV'."""
    h = e.get("hanlp") or {}
    pos = lambda t: t["pos"] if t else "-"
    if e["op"] == "insert":
        what = e["corrected"] if len(e["corrected"]) <= 2 else "words"
        return f"insert {what} after {pos(h.get('left'))}"
    if e["op"] == "delete":
        ws = h.get("words") or []
        return "delete " + ("+".join(t["pos"] for t in ws) if ws else e["original"])
    if e["op"] == "replace":
        ws = h.get("words") or []
        return "replace " + ("+".join(t["pos"] for t in ws) if ws else "?")
    return "comment"


def main():
    tax = json.load(open(CATS / "taxonomy.json", encoding="utf-8"))["categories"]
    train = [json.loads(l) for l in open(CATS / "edits_train.jsonl", encoding="utf-8")]
    texts = {s["sample_id"]: s["text"] for s in json.load(open(CORPUS, encoding="utf-8"))["samples"]}
    api_key()

    def card_for(c):
        mine = [e for e in train if (e["category"] == c["id"] or e["second_category"] == c["id"]) and e["start"] is not None]
        if not mine:
            return c, mine, None, {}
        mine.sort(key=lambda e: (not e["teacher_note"], e["category_confidence"] != "high", len(show(texts[e["sample_id"]], e))))
        shown = mine[:MAX_SHOWN]
        notes = Counter(e["teacher_note"].strip() for e in mine if e["teacher_note"].strip())
        user = "\n".join([
            f"CATEGORY: {c['name']} ({DIMENSION[c['section']]})", f"definition: {c['definition']}", "",
            f"HER NOTES IN THIS CATEGORY ({len(notes)} distinct):", *([f"{n} | {t}" for t, n in notes.most_common()] or ["(none)"]), "",
            f"HER CORRECTIONS ({len(shown)} of {len(mine)}):",
            *[f"[{e['edit_id']}] {show(texts[e['sample_id']], e)}" + (f"  || her note: {e['teacher_note']}" if e["teacher_note"] else "")
              for e in shown],
        ])
        rec, _ = cached_json_call(CACHE, MODEL, REASONING_EFFORT, SYSTEM, SCHEMA, "rule_card", user)
        return c, mine, rec["output"], {e["edit_id"]: e for e in shown}

    with ThreadPoolExecutor(WORKERS) as pool:
        results = list(pool.map(card_for, [c for c in tax if c["id"] != "other"]))

    cards, invented = [], 0
    for c, mine, out, shown in results:
        if out is None:
            cards.append({**c, "n_train": 0, "card": None})
            continue
        examples = []
        for ex in out["examples"]:
            e = shown.get(ex["edit_id"].strip("[] "))  # ids are shown in brackets; the model sometimes copies them
            if e is None:
                invented += 1
                continue
            examples.append({"edit_id": e["edit_id"], "sample_id": e["sample_id"], "display": show(texts[e["sample_id"]], e),
                             "original": e["original"], "corrected": e["corrected"], "op": e["op"],
                             "her_note": e["teacher_note"], "explanation": ex["explanation"]})
        cards.append({**c, "n_train": len(mine), "edit_shapes": Counter(shape(e) for e in mine).most_common(5),
                      "card": {"rule": out["rule"], "explanation_template": out["explanation_template"],
                               "examples": examples, "not_an_error": out["not_an_error"], "her_terms": out["her_terms"]}})

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "cards.json").write_text(json.dumps(cards, ensure_ascii=False, indent=1), encoding="utf-8")
    write_doc(cards)
    write_sheet(cards)
    print(f"{sum(1 for c in cards if c['card'])} cards ({invented} example ids not among those shown, dropped) -> data/12_rule_cards/cards.json")
    print(f"Review: {DOC.relative_to(ROOT)}, {SHEET.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Teacher-facing outputs
# ---------------------------------------------------------------------------
def ordered(cards):
    return sorted(cards, key=lambda c: (list(DIMENSION).index(c["section"]), -c["n_train"]))


def write_doc(cards):
    L = ["# Error categories and rule cards (draft)", "",
         "One card per category of the teacher's corrections, drafted from her notes and her corrections on the",
         "practice stories. The feedback system uses a card to decide whether a flagged error belongs to the rule and",
         "to explain it to the learner. Every example is one of her own corrections. Decisions go in",
         "`12_rule_cards_review.csv` (see `12_rule_cards_instructions.md`).", ""]
    current = None
    for c in ordered(cards):
        if c["section"] != current:
            current = c["section"]
            L += [f"## {DIMENSION[current]}", ""]
        k = c["card"]
        L += [f"### {c['name']}  ·  `{c['id']}`", "", f"*{c['n_train']} of her corrections.* Category definition: {c['definition']}", ""]
        if not k:
            L += ["(No corrections in this category -- no card.)", ""]
            continue
        L += [f"**Rule.** {k['rule']}", "", f"**How an error is explained.** {k['explanation_template']}", ""]
        if k["her_terms"]:
            L += [f"**Her terms.** {' · '.join(k['her_terms'])}", ""]
        L += ["**Her examples.**", ""]
        for ex in k["examples"]:
            L.append(f"- {ex['display']} — {ex['explanation']}" + (f"  *(her note: {ex['her_note']})*" if ex["her_note"] else ""))
        if k["not_an_error"]:
            L += ["", f"**Not an error under this rule.** {k['not_an_error']}"]
        L.append("")
    DOC.write_text("\n".join(L) + "\n", encoding="utf-8")


COLUMNS = ["category_id", "dimension", "category_name", "definition", "her_corrections", "rule", "explanation_template",
           "examples", "not_an_error", "CATEGORY_DECISION", "CARD_DECISION", "TEACHER_WORDING", "TEACHER_NOTE"]
HUMAN = ["CATEGORY_DECISION", "CARD_DECISION", "TEACHER_WORDING", "TEACHER_NOTE"]


def write_sheet(cards):
    kept = {}
    if SHEET.exists():
        with open(SHEET, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                if any(row.get(h) for h in HUMAN):
                    kept[row["category_id"]] = row
    with open(SHEET, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(COLUMNS)
        for c in ordered(cards):
            k, kk = c["card"] or {}, kept.get(c["id"], {})
            w.writerow([c["id"], DIMENSION[c["section"]], c["name"], c["definition"], c["n_train"], k.get("rule", ""),
                        k.get("explanation_template", ""), "\n".join(f"{x['display']} — {x['explanation']}" for x in k.get("examples", [])),
                        k.get("not_an_error", ""), *[kk.get(h, "") for h in HUMAN]])
    INSTRUCTIONS.write_text(INSTRUCTIONS_TEXT.format(n=len(cards)), encoding="utf-8")


INSTRUCTIONS_TEXT = """# Error categories and rule cards: what to check

The teacher's corrections on the practice stories were sorted into {n} categories, built from her own
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
"""


if __name__ == "__main__":
    main()
