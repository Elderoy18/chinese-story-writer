#!/usr/bin/env python3
"""Step 14 -- the judging step: every place the finders flagged is judged with
the teacher's own material -- keep it, drop it, and give the correction she
would give.

    finders' candidates (06 run 1, 08, 13), data/11_categories/edits_train.jsonl,
    data/12_rule_cards/cards.json
        ->  data/14_judge_input/candidates.jsonl   the flags BEFORE judging (scored for comparison)
            data/14_judge/candidates.jsonl         the errors kept AFTER judging (scored by step 7)
            data/14_judge/judgments.jsonl          every decision with what the judge saw
            reports/14_judge.md

    python scripts/14_judge.py
    python scripts/07_score.py 14_judge_input
    python scripts/07_score.py 14_judge

Input: the practical setup -- one LLM run (step 6, run 1) + the GEC model
(step 8) + the teacher finder (step 13). Overlapping flags are merged into one
PLACE, which lists every correction proposed there.

Retrieval, per place (TRAIN material only):
  - her 3 most similar past corrections: each flag is embedded as "the clause
    with the edit marked" (e.g. 他们给[+了]神农灵芝), the same way as all her
    train corrections, and the nearest are taken -- similarity of the ERROR in
    its clause, not of the whole scene
  - the rule cards of those corrections' categories (and of the teacher
    finder's category, when it flagged the place), at most MAX_CARDS

Judging: one LLM call per scene, so the judge reads the scene (and earlier
scenes) as a whole. For each place: keep or drop; its category; the minimal
correction, following hers when her past corrections show how she fixes that
kind of error; the exact span (it may narrow or widen the flag). It never adds
places of its own -- finding is the finders' job.
"""
import json
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
OUT = ROOT / "data" / "14_judge"
INPUT_OUT = ROOT / "data" / "14_judge_input"
CACHE = OUT / "cache"
REPORT = ROOT / "reports" / "14_judge.md"

MODEL = "gpt-5.6-terra"
REASONING_EFFORT = "medium"
TOP_K = 3
MAX_CARDS = 2
WORKERS = 8
FINDERS = {"06_find_baseline": ("AI checker", lambda c: c["run"] == 1), "08_find_gec": ("correction model", None),
           "13_find_teacher": ("teacher's pattern/rule", None)}

spec = importlib.util.spec_from_file_location("score", ROOT / "scripts" / "07_score.py")
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)

SYSTEM = """You are the judging step of a feedback system for beginner learners of Chinese writing a narrative scene by scene. Automatic checkers have flagged places in the learner's CURRENT scene. Decide, place by place, what the supervising teacher would do.

For each place you see: the flagged text (marked 【 】 in its clause), the corrections the checkers proposed, her most similar past corrections from other learners' stories (with her notes), and the rule card(s) of her matching categories.

Her standard, from her corrections and rule cards:
- She corrects real errors of grammar, word choice and coherence (reference, aspect markers 了/着/在, connectors), and content that contradicts the story.
- She does not correct punctuation, and does not replace correct, natural Chinese with a more elegant alternative; simple wording is fine for a beginner.
- A rule card's "not an error" line describes what she does NOT flag.

For each place:
- decision: keep (a real error she would correct) or drop (acceptable at this level, a style preference, or not an error). Do not keep a flag just because a checker raised it; do not drop one only because it is small if it breaks one of her rules.
- category: the id of the rule card it falls under ("other" if none shown fits).
- original: the learner's characters that are wrong, copied EXACTLY from the scene ("" if something is missing); you may narrow or widen the flagged span to the real error.
- before / after: up to 4 learner characters immediately before and after "original", copied EXACTLY, to locate it.
- corrected: the minimal correction. When her past corrections show how she fixes this kind of error, correct it HER way.
- confidence: high or low.
- reason: a short English phrase.
Answer for every place id, and only for those; earlier scenes are context only."""

SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["places"],
    "properties": {"places": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["place_id", "decision", "category", "original", "before", "after", "corrected", "confidence", "reason"],
        "properties": {
            "place_id": {"type": "string"}, "decision": {"type": "string", "enum": ["keep", "drop"]},
            "category": {"type": "string"}, "original": {"type": "string"}, "before": {"type": "string"},
            "after": {"type": "string"}, "corrected": {"type": "string"},
            "confidence": {"type": "string", "enum": ["high", "low"]}, "reason": {"type": "string"},
        }}}},
}


def clause_marked(text, s, t):
    lo = max(text.rfind("，", 0, s), text.rfind("。", 0, s)) + 1
    ends = [i for i in (text.find("，", t), text.find("。", t)) if i >= 0]
    hi = min(ends) if ends else len(text)
    return text[lo:s] + "【" + text[s:t] + "】" + text[t:hi] if t > s else text[lo:s] + "【^】" + text[s:hi]


def place_in(text, r0, r1, e):
    orig, b, a = e["original"], e["before"], e["after"]
    for pre, post in ((b, a), (b, ""), ("", a), ("", "")):
        needle = pre + orig + post
        if not needle:
            continue
        hits = [m.start() for m in re.finditer(re.escape(needle), text[r0:r1])]
        if len(hits) == 1 or (hits and pre and post):
            st = r0 + hits[0] + len(pre)
            return st, st + len(orig)
    return None


def main():
    api_key()
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    texts = {s["sample_id"]: s["text"] for s in corpus["samples"]}
    split = json.load(open(SPLIT, encoding="utf-8"))
    cards = {c["id"]: c for c in json.load(open(CARDS, encoding="utf-8")) if c.get("card")}
    train = [e for e in map(json.loads, open(TRAIN_EDITS, encoding="utf-8")) if e["start"] is not None]

    # ---- the flags, merged into places ----------------------------------
    cands = []
    for name, (label, keep) in FINDERS.items():
        for c in map(json.loads, open(ROOT / "data" / name / "candidates.jsonl", encoding="utf-8")):
            if c["start"] is not None and (keep is None or keep(c)):
                cands.append({**c, "finder": label, "finder_dir": name})
    INPUT_OUT.mkdir(parents=True, exist_ok=True)
    with open(INPUT_OUT / "candidates.jsonl", "w", encoding="utf-8") as fh:
        for c in cands:
            fh.write(json.dumps({**c, "run": 1}, ensure_ascii=False) + "\n")
    (INPUT_OUT / "run_info.json").write_text(json.dumps({"model": "LLM run 1 + GEC + teacher finder (before judging)",
                                                         "reasoning_effort": "-", "prompt_version": "-", "n_runs": 1}), encoding="utf-8")
    places = []
    for c in sorted(cands, key=lambda c: (c["sample_id"], c["start"])):
        g = next((g for g in places if g[0]["sample_id"] == c["sample_id"] and any(score.overlaps(c, x) for x in g)), None)
        g.append(c) if g else places.append([c])

    # ---- retrieval: her nearest train corrections, by the error in its clause
    show = lambda e: score.show(texts[e["sample_id"]], e)
    train_vecs = np.array(embed([show(e) for e in train], CACHE))
    train_vecs /= np.linalg.norm(train_vecs, axis=1, keepdims=True)
    cand_texts = [show(c) for g in places for c in g]
    cand_vecs = dict(zip(cand_texts, embed(cand_texts, CACHE)))

    scene_of = {}
    for t in split["test"]:
        for sc in t["scenes"]:
            scene_of[(t["sample_id"], sc["scene"])] = sc
    by_scene = defaultdict(list)
    for k, g in enumerate(places):
        sid = g[0]["sample_id"]
        sc = next(sc for (s, _), sc in scene_of.items() if s == sid and sc["start"] <= g[0]["start"] <= sc["end"])
        v = np.array([cand_vecs[show(c)] for c in g])
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        sims = (v @ train_vecs.T).max(axis=0)
        near = [train[i] for i in np.argsort(-sims)[:TOP_K]]
        near_sims = [float(sims[i]) for i in np.argsort(-sims)[:TOP_K]]
        cats = [c["type"] for c in g if c["finder_dir"] == "13_find_teacher" and c["type"] in cards]
        cats += [cat for cat, _ in Counter(e["category"] for e in near).most_common() if cat in cards]
        cats = list(dict.fromkeys(cats))[:MAX_CARDS]
        by_scene[(sid, sc["scene"])].append({"place_id": f"P{k}", "group": g, "near": near, "near_sims": near_sims, "cards": cats,
                                             "start": min(c["start"] for c in g), "end": max(c["end"] for c in g)})

    # ---- judging, one call per scene ---------------------------------------
    def user_for(key):
        sid, scene = key
        t = next(t for t in split["test"] if t["sample_id"] == sid)
        text = texts[sid]
        earlier = [text[sc["start"]:sc["end"]] for sc in t["scenes"] if sc["scene"] < scene]
        cur = scene_of[key]
        L = []
        if earlier:
            L.append("EARLIER SCENES (context only):\n" + "\n".join(earlier))
        L += [f"CURRENT SCENE:\n{text[cur['start']:cur['end']]}", "", "FLAGGED PLACES:"]
        for p in by_scene[key]:
            L.append(f"\n[{p['place_id']}] {clause_marked(text, p['start'], p['end'])}")
            for c in p["group"]:
                L.append(f"  proposed by the {c['finder']}: {show(c)}" + (f" ({c['why']})" if c.get("why") and c["finder_dir"] != "08_find_gec" else ""))
            for e in p["near"]:
                L.append(f"  her past correction ({e['category']}): {show(e)}" + (f" — her note: {e['teacher_note']}" if e["teacher_note"] else ""))
            for cid in p["cards"]:
                k = cards[cid]["card"]
                L.append(f"  rule card {cid}: {k['rule']}" + (f" Not an error: {k['not_an_error']}" if k["not_an_error"] else ""))
        return "\n".join(L)

    keys = sorted(by_scene)
    with ThreadPoolExecutor(WORKERS) as pool:
        recs = list(pool.map(lambda k: cached_json_call(CACHE, MODEL, REASONING_EFFORT, SYSTEM, SCHEMA, "judgment", user_for(k)), keys))

    kept, judgments, usage = [], [], Counter()
    for key, (rec, _) in zip(keys, recs):
        usage.update({k: v for k, v in rec.get("usage", {}).items() if isinstance(v, int)})
        sid, scene = key
        cur = scene_of[key]
        answers = {a["place_id"]: a for a in rec["output"]["places"]}
        for p in by_scene[key]:
            a = answers.get(p["place_id"])
            j = {"sample_id": sid, "scene": scene, "place_id": p["place_id"], "start": p["start"], "end": p["end"],
                 "proposals": [{"finder": c["finder"], "edit": show(c)} for c in p["group"]],
                 "her_nearest": [{"edit": show(e), "note": e["teacher_note"], "category": e["category"], "similarity": round(s, 3)}
                                 for e, s in zip(p["near"], p["near_sims"])],
                 "cards": p["cards"], "answer": a}
            judgments.append(j)
            if not a or a["decision"] != "keep":
                continue
            pos = place_in(texts[sid], cur["start"], cur["end"], a)
            if pos is None:  # fall back to the flagged span
                pos = (p["start"], p["end"])
            op = "insert" if not a["original"] else "delete" if not a["corrected"] else "replace"
            kept.append({"cand_id": f"{sid}/{p['place_id']}", "sample_id": sid, "story_id": t_story(split, sid), "scene": scene,
                         "run": 1, "op": op, "start": pos[0], "end": pos[1], "original": a["original"], "corrected": a["corrected"],
                         "before": a["before"], "after": a["after"], "type": a["category"], "confidence": a["confidence"],
                         "why": a["reason"], "finders": sorted({c["finder"] for c in p["group"]})})

    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in (("candidates.jsonl", kept), ("judgments.jsonl", judgments)):
        with open(OUT / name, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    (OUT / "run_info.json").write_text(json.dumps({"model": f"{MODEL} judge over LLM run 1 + GEC + teacher finder",
                                                   "reasoning_effort": REASONING_EFFORT, "prompt_version": prompt_version(SYSTEM, SCHEMA),
                                                   "n_runs": 1, "tokens": dict(usage)}, indent=1), encoding="utf-8")
    write_report(judgments, kept, texts, usage)
    print(f"{len(places)} places in {len(keys)} scenes -> kept {len(kept)}, dropped {len(places) - len(kept)}; tokens {dict(usage)}")
    print(f"Report: {REPORT.relative_to(ROOT)}")


def t_story(split, sid):
    return next(t["story_id"] for t in split["test"] if t["sample_id"] == sid)


def write_report(judgments, kept, texts, usage):
    key, _, _ = score.load_key()
    on_hers = lambda j: any(e["sample_id"] == j["sample_id"] and score.overlaps(j, e) for e in key)
    pct = lambda a, b: f"{a}/{b} ({100 * a / b:.0f}%)" if b else "0/0"
    hers = [j for j in judgments if on_hers(j)]
    other = [j for j in judgments if not on_hers(j)]
    kept_d = lambda js: sum(1 for j in js if j["answer"] and j["answer"]["decision"] == "keep")
    L = ["# Step 14 report: the judging step", "",
         f"- {len(judgments)} flagged places (LLM run 1 + GEC + teacher finder), judged one scene at a time; tokens {dict(usage)}",
         f"- kept {len(kept)}, dropped {len(judgments) - len(kept)}", "",
         "## What was kept", "", "| Flagged places | Kept |", "|---|---|",
         f"| on a correction she made | {pct(kept_d(hers), len(hers))} |",
         f"| on nothing she marked | {pct(kept_d(other), len(other))} |", "",
         "Dropping a place she corrected is a loss; dropping a place she did not mark is usually the judge doing its job "
         "(her answers on `review/09_extra_flags.csv` will show how often those were real errors).", "",
         "## Places she corrected that the judge dropped", ""]
    for j in hers:
        if j["answer"] and j["answer"]["decision"] == "drop":
            L.append(f"- {j['sample_id']}: {clause_marked(texts[j['sample_id']], j['start'], j['end'])} — judge: {j['answer']['reason']}")
    L += ["", "## Places she did not mark that the judge kept (first 40)", ""]
    for j in [j for j in other if j["answer"] and j["answer"]["decision"] == "keep"][:40]:
        a = j["answer"]
        L.append(f"- {j['sample_id']}: {clause_marked(texts[j['sample_id']], j['start'], j['end'])} → {a['original']}→{a['corrected']} ({a['category']}) — {a['reason']}")
    L += ["", "## Example decisions with what the judge saw (first 8)", ""]
    for j in judgments[:8]:
        a = j["answer"] or {}
        L += [f"**{j['sample_id']} {j['place_id']}** {clause_marked(texts[j['sample_id']], j['start'], j['end'])}",
              *[f"- proposed by the {p['finder']}: {p['edit']}" for p in j["proposals"]],
              *[f"- her past correction ({n['category']}, sim {n['similarity']}): {n['edit']}" + (f" — {n['note']}" if n["note"] else "") for n in j["her_nearest"]],
              f"- cards: {', '.join(j['cards'])}",
              f"- **decision: {a.get('decision')}** {a.get('original', '')}→{a.get('corrected', '')} ({a.get('category')}) — {a.get('reason')}", ""]
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
