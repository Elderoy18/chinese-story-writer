#!/usr/bin/env python3
"""Step 15 -- the explanation step: every place the finders flagged becomes one
feedback item, with one correction and an explanation built from the teacher's
rule card and her most similar past corrections. No judging step: nothing is
dropped (judge v1, step 14, lowered recall and is not used).

    finders' candidates (06 run 1, 08, 13), data/11_categories/edits_train.jsonl,
    data/12_rule_cards/cards.json
        ->  data/15_explain/items.jsonl         one feedback item per place, with everything it was built from
            data/15_explain/candidates.jsonl    the same items in finder format (scored by step 7)
            reports/15_feedback.md              the feedback each test scene would get
            reports/15_explain.md               summary
            review/15_explanations_review.csv   a sample of explanations, for the teacher to rate
            review/15_explanations_instructions.md

    python scripts/15_explain.py
    python scripts/07_score.py 15_explain

For each scene of each test story:
  1. Merge: overlapping flags from the three finders become one PLACE.
  2. Retrieve (TRAIN material only): her 3 most similar past corrections, by
     embedding the error in its clause (他们给[+了]神农灵芝), and through them a
     category -- the teacher finder's category when it flagged the place,
     otherwise the most common category among those 3 -- which picks the
     RULE CARD (step 12).
  3. Choose ONE correction, by rule, no LLM: a proposal identical to one of her
     past corrections > the teacher finder's correction > the AI checker's >
     the correction model's.
  4. Strength: "error", or "suggestion" when only the correction model flagged
     it (or only a low-confidence AI flag) and none of her past corrections
     changes the same wording. Suggestions are worded softly, never dropped.
  5. Explain: one LLM call per scene writes, for every item, a short English
     explanation following the card's template and her notes, and sorts it
     into her dimensions. It explains the chosen correction; it may repair the
     correction only if it is not valid Chinese, and it never drops an item.
"""
import csv
import json
import random
import re
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import importlib.util

import numpy as np

from llm import api_key, cached_json_call, embed, prompt_version

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
SPLIT = ROOT / "data" / "03_split" / "split.json"
TRAIN_EDITS = ROOT / "data" / "11_categories" / "edits_train.jsonl"
CARDS = ROOT / "data" / "12_rule_cards" / "cards.json"
OUT = ROOT / "data" / "15_explain"
CACHE = OUT / "cache"
FEEDBACK = ROOT / "reports" / "15_feedback.md"
REPORT = ROOT / "reports" / "15_explain.md"
SHEET = ROOT / "review" / "15_explanations_review.csv"
INSTRUCTIONS = ROOT / "review" / "15_explanations_instructions.md"

MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"
TOP_K = 3
WORKERS = 8
REVIEW_SAMPLE = 60
FINDERS = {"06_find_baseline": ("AI checker", lambda c: c["run"] == 1), "08_find_gec": ("correction model", None),
           "13_find_teacher": ("teacher's pattern/rule", None)}
PRIORITY = {"teacher's pattern/rule": 2, "AI checker": 1, "correction model": 0}
SECTIONS = {"grammar": "Grammar", "word_choice": "Vocabulary", "coherence_reference": "Coherence: reference",
            "coherence_temporality": "Coherence: temporality (了/着/在)", "coherence_connectors": "Coherence: connectors",
            "content": "Content", "other": "Other"}

spec = importlib.util.spec_from_file_location("score", ROOT / "scripts" / "07_score.py")
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)

SYSTEM = """You write the error feedback a beginner learner of Chinese sees for ONE scene of the narrative they are writing. A supervising teacher's rules and past corrections guide every explanation.

For each item you get: the learner's clause with the problem marked 【 】, the correction to explain, its strength (error or suggestion), the teacher's rule card for this kind of error (rule, explanation pattern, her terms), and her most similar past corrections with her notes.

For EVERY item write:
- explanation: one or two short English sentences that tell the learner what is wrong and the rule, following the card's explanation pattern and her terms (e.g. 了completed, 在+Place, 看look vs. 看到see). Chinese only for the words, particles and formulas themselves. For a "suggestion", phrase it as a possible improvement ("It would be more natural to say ..."), not as a mistake. For a comment item with no correction (e.g. a character's first appearance), say what to do.
- dimension: grammar | word_choice | coherence_reference | coherence_temporality | coherence_connectors | content | other -- usually the card's dimension.
- corrected: repeat the given correction. Change it ONLY if it is not valid Chinese in this clause; then give the minimal valid correction and set correction_changed to true.
Never drop an item and never judge whether it should be shown: every item is shown. Keep the tone encouraging and simple."""

SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["items"],
    "properties": {"items": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["item_id", "explanation", "dimension", "corrected", "correction_changed"],
        "properties": {"item_id": {"type": "string"}, "explanation": {"type": "string"},
                       "dimension": {"type": "string", "enum": list(SECTIONS)},
                       "corrected": {"type": "string"}, "correction_changed": {"type": "boolean"}}}}},
}

bare = lambda s: re.sub(r"[^一-鿿]", "", s or "")


def clean_corrected(s):
    """The model sometimes repeats the whole 'X → Y' it was given; keep Y. '(delete)' / '∅' mean nothing."""
    s = (s or "").split("→")[-1].strip()
    return "" if s in ("(delete)", "∅", "(comment, no correction)") else s


def clause_marked(text, s, t):
    lo = max(text.rfind("，", 0, s), text.rfind("。", 0, s)) + 1
    ends = [i for i in (text.find("，", t), text.find("。", t)) if i >= 0]
    hi = min(ends) if ends else len(text)
    return text[lo:s] + "【" + text[s:t] + "】" + text[t:hi] if t > s else text[lo:s] + "【^】" + text[s:hi]


def main():
    api_key()
    texts = {s["sample_id"]: s["text"] for s in json.load(open(CORPUS, encoding="utf-8"))["samples"]}
    split = json.load(open(SPLIT, encoding="utf-8"))
    cards = {c["id"]: c for c in json.load(open(CARDS, encoding="utf-8")) if c.get("card")}
    train = [e for e in map(json.loads, open(TRAIN_EDITS, encoding="utf-8")) if e["start"] is not None]
    show = lambda e: score.show(texts[e["sample_id"]], e)

    # 1. merge the three finders' flags into places
    cands = []
    for name, (label, keep) in FINDERS.items():
        for c in map(json.loads, open(ROOT / "data" / name / "candidates.jsonl", encoding="utf-8")):
            if c["start"] is not None and (keep is None or keep(c)):
                cands.append({**c, "finder": label})
    places = []
    for c in sorted(cands, key=lambda c: (c["sample_id"], c["start"])):
        g = next((g for g in places if g[0]["sample_id"] == c["sample_id"] and any(score.overlaps(c, x) for x in g)), None)
        g.append(c) if g else places.append([c])

    # 2. retrieval: her nearest train corrections, by the error in its clause
    tv = np.array(embed([show(e) for e in train], CACHE))
    tv /= np.linalg.norm(tv, axis=1, keepdims=True)
    cv = dict(zip(*(lambda ts: (ts, embed(ts, CACHE)))([show(c) for g in places for c in g])))

    scenes = {(t["sample_id"], sc["scene"]): sc for t in split["test"] for sc in t["scenes"]}
    by_scene = defaultdict(list)
    for k, g in enumerate(places):
        sid = g[0]["sample_id"]
        key = next(kk for kk, sc in scenes.items() if kk[0] == sid and sc["start"] <= g[0]["start"] <= sc["end"])
        v = np.array([cv[show(c)] for c in g])
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        sims = (v @ tv.T).max(axis=0)
        order = np.argsort(-sims)[:TOP_K]
        near = [train[i] for i in order]
        teacher_cat = next((c["type"] for c in g if c["finder"] == "teacher's pattern/rule" and c["type"] in cards), None)
        cat = teacher_cat or next((c for c, _ in Counter(e["category"] for e in near).most_common() if c in cards), "other")

        # 3. one correction, by rule
        def rank(c):
            hers = any(bare(c["original"]) == bare(e["original"]) and bare(c["corrected"]) == bare(e["corrected"]) for e in near)
            return (hers, PRIORITY[c["finder"]], c.get("confidence") == "high")
        chosen = max(g, key=rank)
        # 4. strength
        finders = {c["finder"] for c in g}
        weak_only = finders == {"correction model"} or (finders == {"AI checker"} and all(c.get("confidence") == "low" for c in g))
        same_wording = any(bare(e["original"]) and bare(e["original"]) in bare("".join(c["original"] for c in g)) for e in near)
        strength = "suggestion" if weak_only and not same_wording else "error"
        by_scene[key].append({"item_id": f"I{k}", "sample_id": sid, "scene": key[1], "group": g, "near": near,
                              "near_sims": [round(float(sims[i]), 3) for i in order], "category": cat,
                              "chosen": chosen, "strength": strength, "finders": sorted(finders),
                              "comment": chosen["op"] == "comment"})

    # 5. explain, one call per scene
    def user_for(key):
        sid, _ = key
        cur = scenes[key]
        L = [f"CURRENT SCENE:\n{texts[sid][cur['start']:cur['end']]}", "", "ITEMS:"]
        for it in by_scene[key]:
            c, k = it["chosen"], cards.get(it["category"], {}).get("card")
            fix = "(comment, no correction)" if it["comment"] else f"{c['original'] or '∅'} → {c['corrected'] or '(delete)'}"
            L.append(f"\n[{it['item_id']}] {clause_marked(texts[sid], c['start'], c['end'])}   correction: {fix}   strength: {it['strength']}")
            if c.get("why") and c["finder"] != "correction model":
                L.append(f"  checker's note: {c['why']}")
            if k:
                L.append(f"  rule card ({it['category']}, {SECTIONS[cards[it['category']]['section']]}): {k['rule']}  "
                         f"Pattern: {k['explanation_template']}" + (f"  Her terms: {', '.join(k['her_terms'])}" if k["her_terms"] else ""))
            for e in it["near"]:
                L.append(f"  her past correction: {show(e)}" + (f" — her note: {e['teacher_note']}" if e["teacher_note"] else ""))
        return "\n".join(L)

    keys = sorted(by_scene)
    with ThreadPoolExecutor(WORKERS) as pool:
        recs = list(pool.map(lambda k: cached_json_call(CACHE, MODEL, REASONING_EFFORT, SYSTEM, SCHEMA, "feedback", user_for(k)), keys))

    items, usage = [], Counter()
    for key, (rec, _) in zip(keys, recs):
        usage.update({k: v for k, v in rec.get("usage", {}).items() if isinstance(v, int)})
        ans = {a["item_id"]: a for a in rec["output"]["items"]}
        for it in by_scene[key]:
            a = ans.get(it["item_id"], {})
            c = it["chosen"]
            items.append({
                "item_id": f"{it['sample_id']}/scene{it['scene']}/{it['item_id']}", "sample_id": it["sample_id"], "scene": it["scene"],
                "start": c["start"], "end": c["end"], "op": c["op"], "original": c["original"],
                "corrected": clean_corrected(a.get("corrected", c["corrected"])) if not it["comment"] else None,
                "correction_changed": a.get("correction_changed", False)
                and clean_corrected(a.get("corrected", "")) != (c["corrected"] or ""), "chosen_from": c["finder"],
                "finders": it["finders"], "strength": it["strength"], "category": it["category"],
                "dimension": a.get("dimension", cards.get(it["category"], {}).get("section", "other")),
                "explanation": re.sub(r"^[^:：。]{0,40}→[^:：。]{0,40}[:：]\s*", "", a.get("explanation", "(no explanation returned)")),
                "clause": clause_marked(texts[it["sample_id"]], c["start"], c["end"]),
                "proposals": [{"finder": x["finder"], "edit": show(x)} for x in it["group"]],
                "her_nearest": [{"edit": show(e), "note": e["teacher_note"], "category": e["category"], "similarity": s}
                                for e, s in zip(it["near"], it["near_sims"])],
            })

    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "items.jsonl", "w", encoding="utf-8") as fh:
        for it in items:
            fh.write(json.dumps(it, ensure_ascii=False) + "\n")
    with open(OUT / "candidates.jsonl", "w", encoding="utf-8") as fh:
        for it in items:
            fh.write(json.dumps({"cand_id": it["item_id"], "sample_id": it["sample_id"], "scene": it["scene"], "run": 1,
                                 "op": it["op"], "start": it["start"], "end": it["end"], "original": it["original"],
                                 "corrected": it["corrected"] or "", "before": "", "after": "", "type": it["category"],
                                 "confidence": "high" if it["strength"] == "error" else "low", "why": it["explanation"]},
                                ensure_ascii=False) + "\n")
    (OUT / "run_info.json").write_text(json.dumps({"model": f"{MODEL} explanations over LLM run 1 + GEC + teacher finder (no judging)",
                                                   "reasoning_effort": REASONING_EFFORT, "prompt_version": prompt_version(SYSTEM, SCHEMA),
                                                   "n_runs": 1, "tokens": dict(usage)}, indent=1), encoding="utf-8")
    write_feedback(items, split, texts)
    write_report(items, usage)
    write_sheet(items)
    print(f"{len(items)} feedback items in {len(keys)} scenes; tokens {dict(usage)}")
    print(f"Reports: {FEEDBACK.relative_to(ROOT)}, {REPORT.relative_to(ROOT)}; review: {SHEET.relative_to(ROOT)}")


def render(items):
    L = []
    for dim, title in SECTIONS.items():
        rows = [it for it in items if it["dimension"] == dim]
        if not rows:
            continue
        L.append(f"**{title}**")
        for it in sorted(rows, key=lambda it: it["start"]):
            fix = f"{it['original'] or '∅'} → {it['corrected'] or '(delete)'}" if it["corrected"] is not None else f"⟦{it['original']}⟧"
            L.append(f"- {'(suggestion) ' if it['strength'] == 'suggestion' else ''}{fix}: {it['explanation']}")
    return L


def write_feedback(items, split, texts):
    L = ["# The feedback each test scene would get (error sections only)", "",
         "Every flagged place from the AI checker (one run), the correction model and the teacher finder, with one correction "
         "and an explanation from the teacher's rule card and past corrections. Nothing is filtered.", ""]
    for t in split["test"]:
        L.append(f"## {t['sample_id']}")
        for sc in t["scenes"]:
            L += ["", f"### Scene {sc['scene']}", "", f"> {texts[t['sample_id']][sc['start']:sc['end']]}", ""]
            L += render([it for it in items if it["sample_id"] == t["sample_id"] and it["scene"] == sc["scene"]]) or ["(nothing flagged)"]
        L.append("")
    FEEDBACK.write_text("\n".join(L) + "\n", encoding="utf-8")


def write_report(items, usage):
    key, _, _ = score.load_key()
    on_hers = lambda it: any(e["sample_id"] == it["sample_id"] and score.overlaps(it, e) for e in key)
    same = lambda it: any(e["sample_id"] == it["sample_id"] and score.overlaps(it, e) and e["op"] != "comment"
                          and bare(e["corrected"]) == bare(it["corrected"]) and bare(e["original"]) == bare(it["original"]) for e in key)
    pct = lambda a, b: f"{a}/{b} ({100 * a / b:.0f}%)" if b else "0/0"
    hit = [it for it in items if on_hers(it) and it["corrected"] is not None]
    L = ["# Step 15 report: explanations", "",
         f"- {len(items)} feedback items (one per flagged place, nothing dropped); about {len(items) / 60:.1f} per scene; tokens {dict(usage)}",
         f"- strength: " + ", ".join(f"{k} {v}" for k, v in Counter(it["strength"] for it in items).items()),
         f"- correction chosen from: " + ", ".join(f"{k} {v}" for k, v in Counter(it["chosen_from"] for it in items).most_common()),
         f"- correction repaired by the explanation step (not valid Chinese): {sum(it['correction_changed'] for it in items)}",
         f"- items on a correction she made: {pct(len([it for it in items if on_hers(it)]), len(items))}",
         f"- of those with a correction, the SAME correction as hers: {pct(sum(1 for it in hit if same(it)), len(hit))}", "",
         "## Items per dimension", "", *[f"- {SECTIONS[k]}: {v}" for k, v in Counter(it["dimension"] for it in items).most_common()], "",
         "## Strength vs. whether she marked the place", "", "| Strength | Items | On a correction she made |", "|---|---|---|"]
    for s in ("error", "suggestion"):
        rows = [it for it in items if it["strength"] == s]
        L.append(f"| {s} | {len(rows)} | {pct(sum(1 for it in rows if on_hers(it)), len(rows))} |")
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


COLUMNS = ["item_id", "student_clause", "correction", "explanation_shown_to_learner", "shown_as", "her_marking",
           "TEACHER_RATING", "TEACHER_BETTER_EXPLANATION", "TEACHER_NOTE"]
HUMAN = ["TEACHER_RATING", "TEACHER_BETTER_EXPLANATION", "TEACHER_NOTE"]


def write_sheet(items):
    key, _, _ = score.load_key()
    marked = lambda it: any(e["sample_id"] == it["sample_id"] and score.overlaps(it, e) for e in key)
    rng = random.Random(15)
    hers = [it for it in items if marked(it)]
    other = [it for it in items if not marked(it)]
    sample = rng.sample(hers, min(REVIEW_SAMPLE // 2, len(hers))) + rng.sample(other, min(REVIEW_SAMPLE // 2, len(other)))
    kept = {}
    if SHEET.exists():
        with open(SHEET, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                if any(row.get(h) for h in HUMAN):
                    kept[row["item_id"]] = row
    with open(SHEET, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(COLUMNS)
        for it in sorted(sample, key=lambda it: it["item_id"]):
            k = kept.get(it["item_id"], {})
            fix = f"{it['original'] or '∅'} → {it['corrected'] or '(delete)'}" if it["corrected"] is not None else "(comment)"
            w.writerow([it["item_id"], it["clause"], fix, it["explanation"], "suggestion" if it["strength"] == "suggestion" else "error",
                        "she corrected this place" if marked(it) else "she did not mark this place", *[k.get(h, "") for h in HUMAN]])
    INSTRUCTIONS.write_text(INSTRUCTIONS_TEXT.format(n=len(sample)), encoding="utf-8")


INSTRUCTIONS_TEXT = """# Feedback explanations: quality check

For every error the system finds, the learner sees a correction and a short English explanation, written
from the teacher's rule card for that kind of error and her own past corrections of similar errors. The
sheet `15_explanations_review.csv` holds a sample of {n} of these from the test stories: half at places the
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
"""


if __name__ == "__main__":
    main()
