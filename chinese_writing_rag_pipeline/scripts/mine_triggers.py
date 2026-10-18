#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Propose regex triggers for rule cards from the teacher's exact edits, measure
every trigger (proposed ones and the teacher rules' own) on the training
stories, and write a review sheet. Nothing here enters a snapshot until the
sheet is reviewed: see review/triggers/instructions.md.

    python scripts/mine_triggers.py [--test-set ../eval/test_set_h20.json]
        -> review/triggers/triggers_review.csv, review/triggers/instructions.md

Training stories = every graded sample not in the test set. A trigger is a hint
"check this rule here", never an error by itself (v2 showed that her
corrections, lifted out of their sentence as patterns, over-fire), so each one
is measured before it is kept:
  fires          -- matches in the students' original texts
  at_her_edit    -- matches overlapping a place she corrected (any rule)
  at_this_rule   -- ... overlapping a correction labelled with this rule
  in_corrected   -- matches still present after all her edits are applied
                    (the pattern survives her correction: often fine usage)
  in_model       -- matches in the four native model stories
  precision      -- at_her_edit / fires
Proposed triggers come from corrections with this rule only: the edited text
itself (2+ characters), or the edited text joined to the word before or after
it (HanLP word boundaries from the v2 parse), when that pattern recurs in 2+
stories. Suggested keep = at_this_rule >= 2, precision >= 0.5, in_model == 0.
"""
import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, "scripts")
from aligned_edits import ALIGNED_EDITS_PATH, ERROR_OPS, first_alternative  # noqa: E402

CORPUS_PATH = "extracted/basic_corpus.json"
RULE_LABELS_PATH = "raw/correction_rules.json"
EXTRA_RULES_PATH = Path("raw/iteration data/extra_rules.json")
OUT_DIR = Path("review/triggers")
MIN_STORIES = 2
SUGGEST = {"at_this_rule": 2, "precision": 0.5}


def apply_edits(text, edits):
    out, pos = [], 0
    for e in sorted(edits, key=lambda e: (e["start"], e["end"])):
        if e["start"] < pos:
            continue
        out += [text[pos:e["start"]], first_alternative(e["corrected"])]
        pos = e["end"]
    return "".join(out + [text[pos:]])


def overlaps(m_start, m_end, e):
    if e["start"] == e["end"]:  # insertion point
        return m_start <= e["start"] <= m_end
    return m_start < e["end"] and e["start"] < m_end


def candidates(e):
    o = e["original"] or ""
    left, right = e.get("hanlp_left") or "", e.get("hanlp_right") or ""
    out = set()
    if len(o) >= 2:
        out.add(o)
    if o and len(o) <= 2:
        if left and not re.search(r"\W", left):
            out.add(left + o)
        if right and not re.search(r"\W", right):
            out.add(o + right)
    if not o and left and right and not re.search(r"\W", left + right):
        out.add(left + right)  # where something is missing
    return out


def measure(pattern, stories, model_texts, rule=None):
    rx = re.compile(pattern)
    r = {"fires": 0, "at_her_edit": 0, "at_this_rule": 0, "in_corrected": 0, "in_model": 0, "examples": []}
    for s in stories.values():
        for m in rx.finditer(s["text"]):
            r["fires"] += 1
            hit = [e for e in s["edits"] if overlaps(m.start(), m.end(), e)]
            r["at_her_edit"] += bool(hit)
            r["at_this_rule"] += bool(rule and any(rule in e["rules"] for e in hit))
            if len(r["examples"]) < 3:
                lo, hi = max(0, m.start() - 6), m.end() + 6
                r["examples"].append(("✓ " if hit else "✗ ") + s["text"][lo:hi])
        r["in_corrected"] += len(rx.findall(s["corrected"]))
    r["in_model"] = sum(len(rx.findall(t)) for t in model_texts)
    r["precision"] = round(r["at_her_edit"] / r["fires"], 2) if r["fires"] else None
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-set", default="../eval/test_set_h20.json")
    args = ap.parse_args()
    corpus = json.load(open(CORPUS_PATH, encoding="utf-8"))
    held = {s["sample_id"] for s in json.load(open(args.test_set, encoding="utf-8"))["samples"]}
    labels = json.load(open(RULE_LABELS_PATH, encoding="utf-8"))["rules"]

    edits = defaultdict(list)
    for line in open(ALIGNED_EDITS_PATH, encoding="utf-8"):
        e = json.loads(line)
        if e["op"] in ERROR_OPS and e["start"] is not None and e["sample_id"] not in held:
            e["rules"] = labels.get(e["teacher_line"], [])
            edits[e["sample_id"]].append(e)
    stories = {s["sample_id"]: {"text": s["raw_text"], "edits": edits[s["sample_id"]],
                                "corrected": apply_edits(s["raw_text"], edits[s["sample_id"]])}
               for s in corpus["samples"] if s["sample_id"] not in held}
    model_texts = [m["text"] for m in corpus["model_stories"]]

    # proposed rule-card triggers: recurring patterns from single-rule corrections
    support = defaultdict(set)
    for sid, s in stories.items():
        for e in s["edits"]:
            if len(e["rules"]) == 1:
                for c in candidates(e):
                    support[(e["rules"][0], c)].add(sid)
    rows = []
    for (rule, cand), sids in sorted(support.items()):
        if len(sids) < MIN_STORIES:
            continue
        m = measure(re.escape(cand), stories, model_texts, rule)
        keep = (m["at_this_rule"] >= SUGGEST["at_this_rule"] and (m["precision"] or 0) >= SUGGEST["precision"]
                and m["in_model"] == 0)
        rows.append({"kind": "rule_card (proposed)", "rule": rule, "trigger_regex": re.escape(cand),
                     "from_n_stories": len(sids), **{k: v for k, v in m.items() if k != "examples"},
                     "examples": " | ".join(m["examples"]), "suggested_keep": "yes" if keep else "no"})

    # the teacher rules' triggers (already in extra_rules.json; measured for review)
    for r in json.load(open(EXTRA_RULES_PATH, encoding="utf-8"))["rules"]:
        for t, status in [(t, "teacher_rule") for t in r["triggers"]] +                          [(t, "teacher_rule (pending review)") for t in r.get("triggers_pending_review", [])]:
            m = measure(t, stories, model_texts)
            rows.append({"kind": status, "rule": r["id"], "trigger_regex": t, "from_n_stories": "",
                         **{k: v for k, v in m.items() if k not in ("examples", "at_this_rule")}, "at_this_rule": "",
                         "examples": " | ".join(m["examples"]),
                         "suggested_keep": "yes" if (m["precision"] or 0) >= SUGGEST["precision"] and m["in_model"] == 0 else "check"})

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cols = ["kind", "rule", "trigger_regex", "from_n_stories", "fires", "at_her_edit", "at_this_rule", "precision",
            "in_corrected", "in_model", "examples", "suggested_keep", "KEEP (yes/no)", "NOTE"]
    with open(OUT_DIR / "triggers_review.csv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row in rows:
            w.writerow({**row, "KEEP (yes/no)": "", "NOTE": ""})
    proposed = [r for r in rows if r["kind"].startswith("rule_card")]
    teacher = [r for r in rows if r["kind"].startswith("teacher_rule")]
    (OUT_DIR / "instructions.md").write_text(INSTRUCTIONS.format(
        n_stories=len(stories), n_prop=len(proposed), n_prop_keep=sum(r["suggested_keep"] == "yes" for r in proposed),
        n_rules=len({r["rule"] for r in proposed}), n_teacher=len(teacher),
        n_teacher_check=sum(r["suggested_keep"] == "check" for r in teacher), **SUGGEST), encoding="utf-8")
    print(f"{len(stories)} training stories; {len(proposed)} proposed rule-card triggers for "
          f"{len({r['rule'] for r in proposed})} rules ({sum(r['suggested_keep'] == 'yes' for r in proposed)} suggested); "
          f"{len(teacher)} teacher-rule triggers measured -> {OUT_DIR}/triggers_review.csv")


INSTRUCTIONS = """# Reviewing the regex triggers

A trigger is a pattern matched against the student's text. When it matches, the
model is shown the rule with the place it matched, as something **to check** --
never as an error by itself. Triggers make the same rule reach every story that
has the pattern (today rule cards are found only by similarity to the whole
scene, so the 不是…而是 card reached 2 of the 6 test scenes that contain it).

`triggers_review.csv` lists {n_prop} triggers proposed for {n_rules} rule cards
(from her corrections on {n_stories} training stories; {n_prop_keep} suggested)
and the {n_teacher} triggers of her teacher rules ({n_teacher_check} marked "check").

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
| suggested_keep | proposed: yes if at_this_rule >= {at_this_rule}, precision >= {precision} and in_model = 0; teacher rules: "check" if below that |

## What to do

Fill **KEEP (yes/no)** for each row (leave blank to accept `suggested_keep`), and
NOTE anything worth telling her. Low precision is not always bad: a hint that
fires often at correct text costs the model attention and risks false positives,
which she cares about most -- prefer `no` when unsure. Then tell Claude; the kept
rule-card triggers go into `raw/iteration data/rule_card_triggers.json` and into
the snapshot for stage S7-4.
"""

if __name__ == "__main__":
    main()
