#!/usr/bin/env python3
"""Step 5 -- turn the teacher's corrections into exact edits on the student's
text (the answer key), with an LLM, checked by code and by a person.

    data/02_corpus/corpus.json, data/03_split/split.json, data/04_parse/parses.jsonl
        ->  data/05_align/edits_<split>.jsonl      one edit per line
            data/05_align/cache/                   one LLM response per feedback line
            review/05_align_<split>.csv            review sheet (opens in Excel)
            reports/05_align_<split>.md

    python scripts/05_align.py --pilot        # 2 test samples
    python scripts/05_align.py                # the 20 test samples (the answer key)
    python scripts/05_align.py --split train  # the train samples (later)

One LLM call per feedback line. The model sees the student's sentence(s) and
the teacher's whole line, and returns, for each fix / instruction / note-only
part, the minimal edit(s) she means -- plus a separate comment edit when a note
describes a different error from the fix. It returns text, not positions: the
characters that change plus a few characters either side, which code finds in
the student text.

Code checks every edit:
  placed       its text + context occurs in the student text (gives the position)
  reproduces   applying a fix's edits makes the teacher's fix appear
  word edge    whether the edit starts/ends inside a HanLP word (哲学[+家]人
               is suspicious: 家 probably replaces 人)
and records the HanLP words each edit touches, with their parts of speech.

Every test item goes on the review sheet; train items only when a check
fails or the model was unsure. Decisions typed into the sheet are kept when
this step is re-run. LLM responses are cached by input + prompt + model.

Needs OPENAI_API_KEY (environment, or the repository's .env.local).
Standard library only.
"""
import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from llm import api_key, cached_json_call, prompt_version

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
SPLIT = ROOT / "data" / "03_split" / "split.json"
PARSES = ROOT / "data" / "04_parse" / "parses.jsonl"
OUT_DIR = ROOT / "data" / "05_align"
CACHE = OUT_DIR / "cache"
REVIEW_DIR = ROOT / "review"
REPORTS = ROOT / "reports"

MODEL = "gpt-5.6-terra"          # the app's feedback model
REASONING_EFFORT = "medium"      # offline, so accuracy over speed
WORKERS = 8
PILOT = ["mengmu_samples#10", "shennong_samples#8"]

PUNCT = re.compile(r"[\s，。！？、；：,.!?;:“”‘’\"'（）()…]")
ELLIPSIS = re.compile(r"……|…|\.\.\.")
EDGE_PUNCT = "，。！？、；：,.!?;:“”‘’\"'（）() "

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------
SYSTEM = """You turn a Chinese teacher's handwritten corrections into exact edits on a learner's text. You do not correct anything yourself, and you do not judge whether she is right.

INPUT: the learner's text and ONE feedback line. The line starts with the learner text she is commenting on (the quote), then her feedback in parts. Each part lists pieces:
- fix (has a ref): her corrected Chinese for one stretch of the quote. She usually writes only the stretch she changed, not the whole sentence.
- instruction (has a ref): "delete X" or "add X".
- note (no ref): her explanation, in English with occasional Chinese.
- comment (ref ends in "/note"): a part with no fix, only a note.

TASK: for every ref, return the edit(s) she means. In addition, if a note describes a DIFFERENT error from its part's fix (e.g. fix 在古代 together with the note "better to introduce 孟子 when this character first appears"), return an extra comment edit for that error with ref "<part>/note".

EACH EDIT:
- op: insert | delete | replace | comment | unplaceable
- original: the learner characters that change, copied EXACTLY ("" for insert). For a comment: the learner characters the note is about, or the whole quote if nothing narrower.
- corrected: the replacement ("" for delete and for comment).
- before / after: up to 4 learner characters immediately before and after "original", copied EXACTLY, so the edit can be located. Use "" only at the start or end of the learner text.
- note: the teacher's note that explains this edit, copied exactly; "" if none does.
- confidence: high, or low whenever you had to choose between readings.
- reason: a short English phrase on how you read her correction.

RULES:
1. Minimal, one edit per error. If her rewrite fixes several separate errors, return one edit for each, not one replace over the clause. A reordering may be one replace spanning the moved words.
2. Learner characters next to her fragment may be replaced by it or may stay -- decide from the Chinese. E.g. learner 古代的时候，孟子… with fix 在古代 is a replace of 古代的时候 by 在古代, not an insertion of 在.
3. "add X" with no position: put X where the grammar and her other fixes show it belongs.
4. "……" in a fix marks a pattern (一……就) or "the rest unchanged"; edit only what she changes.
5. If you cannot tell what she means, use op unplaceable and say why.

EXAMPLE (another learner):
learner text: 所以孟子才八岁，跟孟母一起搬家三次。
quote: 所以孟子才八岁，跟孟母一起搬家三次
part p0: fix [ref p0/k0] 就跟孟母搬了三次家 ; notes: 才 Num.就V. ; 了completed ; V. + Num. + MW. + Obj.
edits:
{"ref":"p0/k0","op":"insert","original":"","corrected":"就","before":"才八岁，","after":"跟孟母一","note":"才 Num.就V.","confidence":"high","reason":"adds 就 for 才…就"}
{"ref":"p0/k0","op":"delete","original":"一起","corrected":"","before":"跟孟母","after":"搬家三次","note":"","confidence":"high","reason":"her fix leaves out 一起"}
{"ref":"p0/k0","op":"replace","original":"搬家三次","corrected":"搬了三次家","before":"母一起","after":"。","note":"了completed","confidence":"high","reason":"adds 了 and moves the frequency before the object"}"""

SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["edits"],
    "properties": {"edits": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["ref", "op", "original", "corrected", "before", "after", "note", "confidence", "reason"],
        "properties": {
            "ref": {"type": "string"},
            "op": {"type": "string", "enum": ["insert", "delete", "replace", "comment", "unplaceable"]},
            "original": {"type": "string"}, "corrected": {"type": "string"},
            "before": {"type": "string"}, "after": {"type": "string"},
            "note": {"type": "string"},
            "confidence": {"type": "string", "enum": ["high", "low"]},
            "reason": {"type": "string"},
        }}}},
}
PROMPT_VERSION = prompt_version(SYSTEM, SCHEMA)


# ---------------------------------------------------------------------------
# Building the input
# ---------------------------------------------------------------------------
def action_groups(part):
    """The refs the model answers for in one part: consecutive fix pieces as ONE
    group (step 2 split her fix at ，, but 孟子现在没有朋友，因为他老是读书 is one
    correction), each instruction alone, or a note-only part as one comment.
    -> [(ref, kind, text, piece indices)]"""
    pieces = part["pieces"]
    if not any(k["kind"] in ("fix", "instruction") for k in pieces):
        return [(f"{part['pid']}/note", "comment", "，".join(k["text"] for k in pieces), list(range(len(pieces))))]
    groups, run = [], []

    def close():
        if run:
            groups.append((f"{part['pid']}/k" + "-".join(map(str, run)), "fix",
                           "，".join(pieces[n]["text"] for n in run), list(run)))
            run.clear()

    for n, k in enumerate(pieces):
        if k["kind"] == "fix":
            run.append(n)
            continue
        close()
        if k["kind"] == "instruction":
            groups.append((f"{part['pid']}/k{n}", "instruction", k["text"], [n]))
    close()
    return groups


def line_input(sample, f):
    """(the text the model sees, the region of the story it covers, refs it must answer)."""
    sents = {s["sid"]: s for s in sample["sentences"]}
    cov = [sents[i] for i in f["location"]["sentence_ids"]]
    r0, r1 = cov[0]["start"], cov[-1]["end"]
    lines = [f"learner text: {sample['text'][r0:r1]}", f"quote: {f['quote']}"]
    if f.get("quote_note"):
        lines.append(f"note on the quote: {f['quote_note']}")
    refs = {}
    for p in f["parts"]:
        groups = action_groups(p)
        if groups[0][1] == "comment":
            lines.append(f"part {p['pid']}: comment [ref {groups[0][0]}] {groups[0][2]}")
        else:
            acts = " ; ".join(f"{g[1]} [ref {g[0]}] {g[2]}" for g in groups)
            used = {n for g in groups for n in g[3]}
            notes = [k["text"] for n, k in enumerate(p["pieces"]) if n not in used]
            lines.append(f"part {p['pid']}: {acts}" + (f" ; notes: {' ; '.join(notes)}" if notes else ""))
        for g in groups:
            refs[g[0]] = {"part": p, "kind": g[1], "text": g[2], "pieces": g[3]}
    return "\n".join(lines), (r0, r1), refs


def aligned(user):
    return cached_json_call(CACHE, MODEL, REASONING_EFFORT, SYSTEM, SCHEMA, "edits", user)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------
def place(text, r0, r1, e):
    """Story position of an edit from its text + context; None if not found or ambiguous."""
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


def bare(s):
    return PUNCT.sub("", s or "")


def reproduces(text, r0, r1, edits, fix):
    """Does applying the edits make the teacher's fix appear in the region?"""
    fix = ELLIPSIS.sub("", fix).strip(EDGE_PUNCT)
    out = text[r0:r1]
    for e in sorted(edits, key=lambda e: e["start"], reverse=True):
        out = out[:e["start"] - r0] + e["corrected"] + out[e["end"] - r0:]
    return all(bare(seg) in bare(out) for seg in fix.split("，") if bare(seg))


def hanlp_view(tokens, start, end, op):
    """The HanLP words an edit touches, and whether its edges fall inside a word."""
    touched = [t for t in tokens if t["story_start"] < end and t["story_start"] + len(t["text"]) > start] if end > start else []
    left = next((t for t in reversed(tokens) if t["story_start"] + len(t["text"]) <= start), None)
    right = next((t for t in tokens if t["story_start"] >= end), None)
    bounds = {t["story_start"] for t in tokens} | {t["story_start"] + len(t["text"]) for t in tokens}
    inside = [p for p in ({start} if op == "insert" else {start, end}) if p not in bounds]
    w = lambda t: {"text": t["text"], "pos": t["pos"], "rel": t["rel"]} if t else None
    return {"words": [w(t) for t in touched], "left": w(left), "right": w(right), "edge_inside_word": bool(inside)}


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["test", "train"], default="test")
    ap.add_argument("--pilot", action="store_true", help=f"only {', '.join(PILOT)}")
    args = ap.parse_args()
    tag = "pilot" if args.pilot else args.split

    corpus = json.load(open(CORPUS, encoding="utf-8"))
    split = json.load(open(SPLIT, encoding="utf-8"))
    wanted = set(PILOT) if args.pilot else (
        {t["sample_id"] for t in split["test"]} if args.split == "test" else set(split["train"]))
    samples = [s for s in corpus["samples"] if s["sample_id"] in wanted]

    tokens_of = defaultdict(list)  # sample -> HanLP tokens with story positions
    for line in open(PARSES, encoding="utf-8"):
        u = json.loads(line)
        if u["kind"] == "student_sentence" and u["source"]["sample_id"] in wanted:
            tokens_of[u["source"]["sample_id"]] += u["tokens"]

    jobs = []
    for s in samples:
        for f in s["feedback"]:
            user, region, refs = line_input(s, f)
            jobs.append((s, f, user, region, refs))

    api_key()  # fail early if missing
    print(f"{len(jobs)} feedback lines ({tag}), model {MODEL} ({REASONING_EFFORT}), prompt {PROMPT_VERSION}")
    with ThreadPoolExecutor(WORKERS) as pool:
        results = list(pool.map(lambda j: aligned(j[2]), jobs))

    edits, items, usage = [], [], Counter()
    for (s, f, user, (r0, r1), refs), (rec, _) in zip(jobs, results):
        usage.update({k: v for k, v in rec.get("usage", {}).items() if isinstance(v, int)})
        text = s["text"]
        by_ref = defaultdict(list)
        for e in rec["output"]["edits"]:
            by_ref[e["ref"]].append(e)
        all_refs = list(refs) + [r for r in by_ref if r not in refs]
        for ref in all_refs:
            info = refs.get(ref)
            extra_note = info is None and re.fullmatch(r"p\d+/note", ref) is not None
            item_id = f"{s['sample_id']}/{f['fid']}/{ref}"
            problems, rows = [], []
            for m, e in enumerate(by_ref.get(ref, [])):
                pos = place(text, r0, r1, e) if e["op"] != "unplaceable" else None
                rows.append({
                    "edit_id": f"{item_id}/e{m}", "sample_id": s["sample_id"], "story_id": s["story_id"],
                    "split": "test" if args.split == "test" or args.pilot else "train",
                    "fid": f["fid"], "ref": ref,
                    "from": "note (separate error)" if extra_note else (info["kind"] if info else "unknown ref"),
                    "op": e["op"], "start": pos[0] if pos else None, "end": pos[1] if pos else None,
                    "original": e["original"], "corrected": e["corrected"] if e["op"] != "comment" else None,
                    "teacher_note": e["note"], "teacher_piece": info["text"] if info else None,
                    "teacher_line": f["raw"], "confidence": e["confidence"], "llm_reason": e["reason"],
                    "hanlp": hanlp_view(tokens_of[s["sample_id"]], pos[0], pos[1], e["op"]) if pos else None,
                })
                if e["op"] == "unplaceable":
                    problems.append(f"could not place: {e['reason']}")
                elif pos is None:
                    problems.append(f'not found in the text: {e["before"]}[{e["original"]}]{e["after"]}')
            if info is None and not extra_note:
                problems.append("ref not in the teacher's line")
            if not rows:
                problems.append("no edit returned")
            placed = [r for r in rows if r["start"] is not None and r["op"] in ("insert", "delete", "replace")]
            if info and info["kind"] == "fix" and placed and not reproduces(text, r0, r1, placed, info["text"]):
                problems.append("edits do not reproduce her fix")
            if any(r["confidence"] == "low" for r in rows):
                problems.append("model unsure")
            if any(r["hanlp"] and r["hanlp"]["edge_inside_word"] for r in rows):
                problems.append("edit edge inside a HanLP word")
            for r in rows:
                r["problems"] = problems
            edits += rows
            items.append({"item_id": item_id, "split": rows[0]["split"] if rows else "", "problems": problems,
                          "student_text": text[r0:r1], "teacher_line": f["raw"],
                          "piece": info["text"] if info else ("(separate error in a note)" if extra_note else ref),
                          "reading": " ; ".join(display(text, r) for r in rows) or "(none)",
                          "notes": " ; ".join(r["teacher_note"] for r in rows if r["teacher_note"]),
                          "words": " ; ".join(" ".join(f"{w['text']}/{w['pos']}" for w in r["hanlp"]["words"])
                                              for r in rows if r["hanlp"]),
                          "reason": " ; ".join(r["llm_reason"] for r in rows)})

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"edits_{tag}.jsonl"
    with open(out, "w", encoding="utf-8") as fh:
        for e in edits:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    sheet = REVIEW_DIR / f"05_align_{tag}.csv"
    write_sheet(items, sheet, include_all=(args.split == "test" or args.pilot))
    report = REPORTS / f"05_align_{tag}.md"
    write_report(report, tag, items, edits, usage, sum(1 for _, c in results if c), len(jobs))
    print(f"{len(edits)} edits -> {out.relative_to(ROOT)}")
    print(f"review sheet {sheet.relative_to(ROOT)}; report {report.relative_to(ROOT)}; tokens {dict(usage)}")


def display(text, e):
    """The edit inside its quote: 他们给[+了]神农灵芝."""
    if e["start"] is None:
        return f'(unplaced {e["op"]}: {e["original"]}→{e["corrected"] or ""})'
    s, t = e["start"], e["end"]
    lo = max(text.rfind("，", 0, s), text.rfind("。", 0, s)) + 1  # start of the clause
    hi_c = [i for i in (text.find("，", t), text.find("。", t)) if i >= 0]
    hi = min(hi_c) if hi_c else len(text)
    mid = {"comment": f"⟦{text[s:t]}⟧", "insert": f"[+{e['corrected']}]", "delete": f"[-{e['original']}]"}.get(
        e["op"], f"[{e['original']}→{e['corrected']}]")
    return text[lo:s] + mid + text[t:hi]


# ---------------------------------------------------------------------------
# Review sheet and report
# ---------------------------------------------------------------------------
COLUMNS = ["item_id", "check_first", "student_text", "teacher_line", "teacher_piece",
           "edits_read_by_model", "her_note_for_each", "hanlp_words", "model_reason",
           "DECISION", "CORRECTION", "REVIEWER_NOTE"]
HUMAN = ["DECISION", "CORRECTION", "REVIEWER_NOTE"]


def write_sheet(items, path, include_all):
    """DECISION: ok / wrong (write the right edit in CORRECTION, e.g. 古代的时候→在古代) /
    drop (not an error edit). Rows with check_first filled in are listed first.
    Existing decisions are carried over by item_id."""
    kept = {}
    if path.exists():
        with open(path, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                if any(row.get(h) for h in HUMAN):
                    kept[row["item_id"]] = row
    rows = [i for i in items if include_all or i["problems"]]
    rows.sort(key=lambda i: (not i["problems"], i["item_id"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(COLUMNS)
        for i in rows:
            k = kept.get(i["item_id"], {})
            w.writerow([i["item_id"], "; ".join(i["problems"]), i["student_text"], i["teacher_line"], i["piece"],
                        i["reading"], i["notes"], i["words"], i["reason"],
                        k.get("DECISION", ""), k.get("CORRECTION", ""), k.get("REVIEWER_NOTE", "")])
    if kept:
        print(f"  kept {len(kept)} earlier review decisions")


def write_report(path, tag, items, edits, usage, cached, n_lines):
    probs = Counter(p.split(":")[0] for i in items for p in i["problems"])
    ops = Counter(e["op"] for e in edits)
    L = [f"# Step 5 report: aligning the teacher's corrections ({tag})", "",
         f"- model {MODEL}, reasoning effort {REASONING_EFFORT}, prompt {PROMPT_VERSION}",
         f"- feedback lines: {n_lines} ({cached} from cache); tokens: {dict(usage)}",
         f"- teacher items: {len(items)} -> edits: {len(edits)} "
         f"(" + ", ".join(f"{k} {v}" for k, v in ops.most_common()) + ")",
         f"- extra comment edits for a separate error in a note: {sum(1 for e in edits if e['from'].startswith('note (separate'))}",
         f"- items with no problem found by the checks: {sum(1 for i in items if not i['problems'])} of {len(items)}", "",
         "## Problems found by the checks", "", "| Problem | Items |", "|---|---|",
         *[f"| {k} | {v} |" for k, v in probs.most_common()], "",
         "## All items", "", "| Teacher's piece | Edits as read by the model | Her note | Check |", "|---|---|---|---|"]
    for i in sorted(items, key=lambda i: i["item_id"]):
        L.append(f"| {i['piece']} | {i['reading']} | {i['notes']} | {'; '.join(i['problems'])} |".replace("\n", " "))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
