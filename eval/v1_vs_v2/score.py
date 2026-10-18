#!/usr/bin/env python3
"""v1 (eval stages S5, S6) vs v2 (chinese_writing_rag_pipeline_v2, round S0),
scored with metrics redefined from the teacher's critique of v2:

  1. partial sentences      -- the shown text is truncated / not a complete unit
  2. corrected version      -- the text after → must be grammatical and fully correct
  3. categories             -- no Other / Content; items in the right category
  4. false positives and incorrect corrections  (her top priority: "可以接受AI miss
     errors，但是不能出现false positives或incorrect corrections")
  5. end-of-story content   -- her flagged missing scenes caught; notes clear
     ("miss ... scene" / "need to ...")
  6. expressiveness         -- ideas that fit the story (especially 孟母)
  recall of her corrections is reported last.

    python eval/v1_vs_v2/score.py            # -> eval/reports/v1_vs_v2.md, eval/v1_vs_v2/items.jsonl

Stories: the 6 held-out stories of the v1 eval (eval/test_set.json). v2's test
split contains them with the same scene splits, and v1's retrieval snapshots
exclude them, so neither system saw her corrections on them. Nothing is
regenerated: both systems' existing outputs are scored.

Reference: her corrections on these stories as exact edits
(chinese_writing_rag_pipeline_v2/data/05_align/edits_test.jsonl; she accepted
232 of 234 rows of the alignment). Deterministic checks use them directly; the
judge (an LLM, blind to which system wrote an item) gets them as reference.
The judge is checked against her own tagged comments on v2's feedback
(chinese_writing_rag_pipeline_v3/data/06_s0v2_labels/comments.jsonl), which
cover 6 stories, 2 of them shared with this set.

LLM calls go through chinese_writing_rag_pipeline_v3/scripts/llm.py (cached in
eval/v1_vs_v2/cache; re-running is free unless a prompt changes).
"""
import difflib
import json
import re
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "chinese_writing_rag_pipeline_v3" / "scripts"))
from llm import cached_json_call, prompt_version  # noqa: E402

V1_RUNS = REPO / "eval" / "runs"
V2 = REPO / "chinese_writing_rag_pipeline_v2"
TEST_SET = REPO / "eval" / "test_set.json"
KEY = V2 / "data" / "05_align" / "edits_test.jsonl"
CORPUS = V2 / "data" / "02_corpus" / "corpus.json"
HER_S0_COMMENTS = REPO / "chinese_writing_rag_pipeline_v3" / "data" / "06_s0v2_labels" / "comments.jsonl"
CACHE = HERE / "cache"
ITEMS_OUT = HERE / "items.jsonl"
REPORT = REPO / "eval" / "reports" / "v1_vs_v2.md"

MODEL = "gpt-5.6-terra"
EFFORT = "medium"
SYSTEMS = ["v1-S5", "v1-S6", "v2-S0"]
VALIDATION_STORIES = ["mengmu_samples#4", "mengmu_samples#10", "mengmu_samples#12",
                      "shennong_samples#4", "shennong_samples#8", "shennong_samples#12"]
CATEGORIES = ["Grammar", "Vocabulary", "Coherence: reference", "Coherence: temporality", "Coherence: connectors"]

squash = lambda s: re.sub(r"[\s，。！？、；：,.!?;:“”‘’\"'（）()…—⟦⟧]", "", s or "")
TRUNC = re.compile(r"…|\.\.\.")


# ---------------------------------------------------------------- loading

def load_v1(stage, sample_id, scenes):
    run = json.load(open(V1_RUNS / stage / f"{sample_id.replace('#', '_')}.json", encoding="utf-8"))
    out = {"scenes": [], "content": []}
    for i, sc in enumerate(run["scenes"]):
        assert sc["text"] == scenes[i], (stage, sample_id, i)
        out["scenes"].append(parse_v1_scene(sc["feedback"], sc["text"]))
    out["content"] = bullets(section(run["content"]["feedback"], "Content"))
    return out


def section(md, heading_start):
    """Text of the first '## <heading_start>...' section of a markdown feedback."""
    m = re.search(rf"^##\s*{re.escape(heading_start)}.*?$(.*?)(?=^##\s|\Z)", md, re.S | re.M)
    return m.group(1) if m else ""


def bullets(text):
    return [l.strip()[2:].strip() for l in text.splitlines()
            if l.strip().startswith("- ") and not re.match(r"-\s*(No|Nothing)\b", l.strip())]


def split_v1_item(body, scene_text):
    """'before：after，explanation' -> (before, after|None, explanation)."""
    cands = [m.start() for m in re.finditer("：", body)]
    idx = next((i for i in cands if squash(body[:i]) and squash(body[:i]) in squash(scene_text)), None)
    if idx is None:
        idx = cands[0] if cands else len(body)
    before, rest = body[:idx].strip(), body[idx + 1:].strip()
    if not rest or re.match(r"[A-Za-z“\"]", rest):
        return before, None, rest
    m = re.search(r"[，,]\s*(?=[A-Za-z“\"])", rest)
    if m:
        return before, rest[:m.start()].strip(), rest[m.end():].strip()
    return before, rest, ""


def parse_v1_scene(md, scene_text):
    items, expr = [], []
    for heading in ("Grammar & Vocabulary Corrections", "Grammar Corrections"):
        for b in bullets(section(md, heading)):
            before, after, expl = split_v1_item(b, scene_text)
            items.append({"section": "Grammar & Vocabulary", "strength": "error",
                          "before": before, "after": after, "explanation": expl, "shown": b})
        if section(md, heading):
            break
    for b in bullets(section(md, "Coherence")):
        m = re.match(r"Coherence\s*\(([^)]*)\)\s*[:：]\s*(.*)", b)
        if m:
            kind = {"reference": "reference", "temporality": "temporality",
                    "conjunction": "connectors"}.get(m.group(1).strip().lower(), m.group(1).strip().lower())
            before, after, expl = split_v1_item(m.group(2), scene_text)
            items.append({"section": f"Coherence: {kind}", "strength": "error",
                          "before": before, "after": after, "explanation": expl, "shown": b})
        elif b.lower().startswith("expressiveness"):
            expr.append(re.sub(r"^Expressiveness\s*[:：]\s*", "", b))
    if not items and "Incorrect phrase" in md:
        items = parse_s0_blocks(md)
    return {"items": items, "expressiveness": expr}


def parse_s0_blocks(md):
    """Stage S0's original format: blocks of 'Incorrect phrase: “X”' / 'Formula: ...' /
    'Correct: “Y”' / explanation, before '**Vocabulary Suggestions**'."""
    items = []
    for blk in re.split(r"\n\s*\n", md.split("Vocabulary Suggestions")[0]):
        m1 = re.search(r"Incorrect phrase:\s*“(.*?)”", blk)
        if not m1:
            continue
        m2 = re.search(r"Correct:\s*“(.*?)”", blk)
        items.append({"section": "Grammar & Vocabulary", "strength": "error", "before": m1.group(1).strip("。"),
                      "after": m2.group(1).strip("。") if m2 else None,
                      "explanation": blk[m2.end():].strip() if m2 else "", "shown": " ".join(blk.split())})
    return items


def load_v2(story):
    out = {"scenes": [], "content": story["content"]}
    for sc in story["scenes"]:
        items = []
        for c in sc["feedback"]["corrections"]:
            if "→" in c["correction"]:
                before, after = [x.strip() for x in c["correction"].split("→", 1)]
            else:
                before, after = c["correction"].strip(), None
            items.append({"section": c["section"], "strength": c["strength"], "before": before,
                          "after": after, "explanation": c["explanation"],
                          "shown": c["correction"] + " -- " + c["explanation"]})
        expr = [f"{e['idea']} e.g. {e['example']}" for e in sc["feedback"].get("expressiveness", [])]
        out["scenes"].append({"items": items, "expressiveness": expr})
    return out


def locate(before, scene_text, scene_offset):
    """Character span of the item's student words in the whole story text (None if not found)."""
    needle = TRUNC.sub("", before).replace("⟦", "").replace("⟧", "").strip()
    for part in sorted(re.split(r"\s*/\s*", needle), key=len, reverse=True):
        if part and part in scene_text:
            s = scene_text.index(part)
            return scene_offset + s, scene_offset + s + len(part)
    # v1 sometimes quotes the scene with its own earlier corrections applied
    # (e.g. 搬到了 for 搬到): take the stretch matching most of the quote.
    blocks = [b for b in difflib.SequenceMatcher(None, scene_text, needle, autojunk=False).get_matching_blocks() if b.size >= 2]
    if needle and sum(b.size for b in blocks) >= 0.7 * len(needle):
        return scene_offset + blocks[0].a, scene_offset + blocks[-1].a + blocks[-1].size
    return None


# ---------------------------------------------------------------- judge prompts

def _her_rules():
    rubric = (REPO / "Coherence reference temporality rules.md").read_text(encoding="utf-8").strip()
    more = json.load(open(REPO / "chinese_writing_rag_pipeline_v3" / "data" / "01_extracted" / "feedback_data" /
                          "more rules.json", encoding="utf-8"))
    rules = "\n".join(f"- {p['text']}" for p in more["paragraphs"] if p["text"].strip())
    return f"Her coherence rubric:\n{rubric}\n\nHer extra rules:\n{rules}"


RUBRIC = _her_rules()

JUDGE_SYSTEM = """You check feedback that an automatic system gave a learner of Chinese (early level) on one scene of a story they retold. You are strict in the way this learner's Chinese teacher is strict. Her priorities: a missed error is acceptable, but a false positive (marking correct words as an error) or an incorrect correction is a serious problem. The correction shown after → must be grammatical, correct Chinese the learner could copy; if the system fixed one error but left another error inside the text it shows, the shown correction is NOT fully correct.

You get the earlier scenes (context), the scene, the teacher's own corrections on this scene (reference: what she marked is an error; she may have missed some errors, and she sometimes gives alternatives separated by /), and the system's feedback items, numbered. For each item return:

- shown_complete: true if the student text the item shows (before →) is a complete, readable unit -- a whole clause, or a whole phrase that makes sense on its own. false if it is cut off (starts or ends mid-phrase or mid-word, marked with … or not) so the learner cannot tell what it says.
- is_error: true if the student's words the item points at really contain an error the teacher would mark. If she corrected these words, it is an error. If she did not, decide yourself; a change that only makes acceptable wording a bit nicer is NOT an error (false), even when the item calls itself a suggestion.
- fix_right: for an item with a correction (after →): "yes" if the change it makes correctly fixes the error at that place (any correct fix counts, not only hers), "no" if the change is wrong, introduces an error, or misses the point. "no_correction" if the item shows no corrected text.
- after_fully_correct: "yes" if the shown corrected text is grammatical, correct Chinese with no error left in it (including other errors in the shown text that the item did not fix), "no" otherwise, "no_correction" if there is none.
- right_categories: the category or categories this error belongs in (one, or two when both are reasonable):
    Grammar -- sentence structure, word order, particles and complements in the wrong place (e.g. 搬了到 -> 搬到了, 住了在 -> 住在, 玩在墓地 -> 在墓地玩), missing/extra structural words;
    Vocabulary -- the wrong word or collocation, wrong measure word, a word that does not fit the meaning;
    Coherence: reference -- how people/things are referred to across clauses: first mention, pronouns, repeated names, zero anaphora, unclear or extra 你/他/他们;
    Coherence: temporality -- time/aspect across the narrative: 了 for completed events, 着, 在 (ongoing), 过, sentence-final 了 for a change;
    Coherence: connectors -- 因为/所以/然后/但是/这样 etc. linking clauses.
  If is_error is false, give the category the item would belong in if it were an error.
- reason: one short sentence.

The teacher's written standards follow. Wording that breaks one of them IS an error she marks (is_error = true), even where general Chinese usage would allow it; an item that applies one of them where it does not fit is not.

""" + RUBRIC

JUDGE_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["items"],
    "properties": {"items": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["n", "shown_complete", "is_error", "fix_right", "after_fully_correct", "right_categories", "reason"],
        "properties": {
            "n": {"type": "integer"},
            "shown_complete": {"type": "boolean"},
            "is_error": {"type": "boolean"},
            "fix_right": {"type": "string", "enum": ["yes", "no", "no_correction"]},
            "after_fully_correct": {"type": "string", "enum": ["yes", "no", "no_correction"]},
            "right_categories": {"type": "array", "items": {"type": "string", "enum": CATEGORIES}},
            "reason": {"type": "string"},
        }}}},
}

EXPR_SYSTEM = """You check "expressiveness" ideas an automatic system gave a learner of Chinese (early level) for one scene of a story they retold from a traditional tale. A good idea adds a concrete detail, feeling, action or line of speech that fits this point of the learner's story and the traditional tale, and its Chinese example is correct and at the learner's level.

For each idea return:
- good: true only if none of the problems below apply.
- problem: "none", "redundant" (the learner already says or clearly implies it), "contradicts" (conflicts with what the learner wrote before or after, or with the situation), "off_story" (changes or invents plot against the traditional tale), "bad_example" (the Chinese example is ungrammatical, unnatural or far above the learner's level), or "vague" (too general to act on).
- reason: one short sentence."""

EXPR_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["ideas"],
    "properties": {"ideas": {"type": "array", "items": {
        "type": "object", "additionalProperties": False, "required": ["n", "good", "problem", "reason"],
        "properties": {"n": {"type": "integer"}, "good": {"type": "boolean"},
                       "problem": {"type": "string", "enum": ["none", "redundant", "contradicts", "off_story", "bad_example", "vague"]},
                       "reason": {"type": "string"}}}}},
}

CONTENT_SYSTEM = """You check the end-of-story content feedback an automatic system gave a learner of Chinese who retold a traditional tale. You get the tale's required scenes (numbered), the learner's whole story, the teacher's own content flags for this story, and the system's content notes (numbered).

Return:
- scenes: for each required scene, whether the TEACHER flagged it as missing or wrong ("missing", "wrong", "none" -- from her flags only), and whether the SYSTEM's notes say it is missing or wrong ("missing", "wrong", "none").
- notes: for each system note: correct (true if what it says is missing/wrong really is missing/wrong in the learner's story), clear (true if it plainly tells the learner which scene or event is missing or what they need to add/fix, e.g. "Miss the scene: ..." or "You need to ..."; false if the learner would have to work out what is meant), reason (one short sentence)."""

CONTENT_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["scenes", "notes"],
    "properties": {
        "scenes": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["n", "teacher", "system"],
            "properties": {"n": {"type": "integer"},
                           "teacher": {"type": "string", "enum": ["missing", "wrong", "none"]},
                           "system": {"type": "string", "enum": ["missing", "wrong", "none"]}}}},
        "notes": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["n", "correct", "clear", "reason"],
            "properties": {"n": {"type": "integer"}, "correct": {"type": "boolean"},
                           "clear": {"type": "boolean"}, "reason": {"type": "string"}}}},
    },
}


def her_corrections_text(edits):
    if not edits:
        return "(none on this scene)"
    lines, seen = [], set()
    for e in edits:
        line = e["teacher_line"]
        if line not in seen:
            seen.add(line)
            lines.append(f"- {line}")
    return "\n".join(lines)


def judge_scene(story_text_before, scene_text, edits, items):
    user = (f"Earlier scenes:\n{story_text_before or '(none)'}\n\nThis scene:\n{scene_text}\n\n"
            f"The teacher's corrections on this scene (student words：her correction, her note):\n{her_corrections_text(edits)}\n\n"
            "The system's feedback items:\n" +
            "\n".join(f"{i + 1}. [{it['section']}, {it['strength']}] {it['shown']}" for i, it in enumerate(items)))
    rec, _ = cached_json_call(CACHE, MODEL, EFFORT, JUDGE_SYSTEM, JUDGE_SCHEMA, "item_judgments", user)
    return {r["n"]: r for r in rec["output"]["items"]}


def judge_expr(title, story_text_before, scene_text, ideas):
    user = (f"Traditional tale: {title}\n\nEarlier scenes:\n{story_text_before or '(none)'}\n\nThis scene:\n{scene_text}\n\n"
            "Expressiveness ideas:\n" + "\n".join(f"{i + 1}. {x}" for i, x in enumerate(ideas)))
    rec, _ = cached_json_call(CACHE, MODEL, EFFORT, EXPR_SYSTEM, EXPR_SCHEMA, "expr_judgments", user)
    return {r["n"]: r for r in rec["output"]["ideas"]}


def judge_content(scene_list, story_text, flags, notes):
    user = ("Required scenes:\n" + "\n".join(f"{i + 1}. {s}" for i, s in enumerate(scene_list)) +
            f"\n\nThe learner's story:\n{story_text}\n\nThe teacher's content flags:\n" +
            ("\n".join(f"- {f['raw']}" for f in flags) or "(none)") +
            "\n\nThe system's content notes:\n" + ("\n".join(f"{i + 1}. {n}" for i, n in enumerate(notes)) or "(none)"))
    rec, _ = cached_json_call(CACHE, MODEL, EFFORT, CONTENT_SYSTEM, CONTENT_SCHEMA, "content_judgments", user)
    return rec["output"]


# ---------------------------------------------------------------- scoring

def overlaps(span, e):
    if span is None or e["start"] is None:
        return False
    s, t = span
    if e["start"] == e["end"]:
        return s <= e["start"] <= t
    return s < e["end"] and e["start"] < t


def build(system, sample, outputs, key_by_sample):
    """Judge every item / idea of one system on one story; return item records."""
    text, scenes = sample["text"], [x for x in sample["scenes"]]
    offsets, pos = [], 0
    for sc in scenes:
        pos = text.index(sc, pos)
        offsets.append(pos)
        pos += len(sc)
    recs = []
    for si, (sc, fb) in enumerate(zip(scenes, outputs["scenes"])):
        lo, hi = offsets[si], offsets[si] + len(sc)
        edits = [e for e in key_by_sample[sample["sample_id"]]
                 if (lo <= e["start"] <= hi if e["start"] is not None
                     else bool(e["original"]) and e["original"] in sc)]
        earlier = "".join(scenes[:si])
        verdicts = judge_scene(earlier, sc, edits, fb["items"]) if fb["items"] else {}
        for i, it in enumerate(fb["items"]):
            span = locate(it["before"], sc, lo)
            v = verdicts.get(i + 1)
            her = [e for e in edits if overlaps(span, e)]
            recs.append({"kind": "item", "system": system, "sample_id": sample["sample_id"], "scene": si + 1,
                         **it, "span": span, "at_her_place": bool(her),
                         "her_corrections": sorted({e["teacher_piece"] or "" for e in her}), "judge": v})
        if fb["expressiveness"]:
            ev = judge_expr(sample["title"], earlier, sc, fb["expressiveness"])
            for i, idea in enumerate(fb["expressiveness"]):
                recs.append({"kind": "expr", "system": system, "sample_id": sample["sample_id"], "scene": si + 1,
                             "idea": idea, "judge": ev.get(i + 1)})
    if sample.get("scene_list"):
        cv = judge_content(sample["scene_list"], text, sample["content_flags"], outputs["content"])
        recs.append({"kind": "content", "system": system, "sample_id": sample["sample_id"],
                     "notes": outputs["content"], "judge": cv})
    return recs


def item_flags(r):
    """Per-item verdicts used by the metrics. Her marking overrides the judge on is_error."""
    j = r["judge"] or {}
    is_error = r["at_her_place"] or j.get("is_error", False)
    has_after = r["after"] is not None
    truncated = bool(TRUNC.search(r["before"] or "") or TRUNC.search(r["after"] or ""))
    cats = set(j.get("right_categories", []))
    sec = r["section"]
    if sec == "Grammar & Vocabulary":
        cat_ok = bool(cats & {"Grammar", "Vocabulary"})
    elif sec.startswith("Coherence: 了") or sec == "Coherence: temporality":
        cat_ok = "Coherence: temporality" in cats
    else:
        cat_ok = sec in cats
    coarse = lambda c: "G&V" if c in ("Grammar", "Vocabulary") else c
    sec_c = "G&V" if sec in ("Grammar", "Vocabulary", "Grammar & Vocabulary") else (
        "Coherence: temporality" if sec.startswith("Coherence: 了") else sec)
    return {
        "false_positive": not is_error,
        "incorrect": is_error and j.get("fix_right") == "no",
        "after_not_correct": has_after and j.get("after_fully_correct") == "no",
        "truncated": truncated,
        "partial": truncated or not j.get("shown_complete", True),
        "invalid_category": sec in ("Other", "Content"),
        "miscategorized": not cat_ok,
        "miscategorized_coarse": sec_c not in {coarse(c) for c in cats},
        "unconfirmed": not r["at_her_place"],
        "comment_only": not has_after,
    }


def pct(a, b):
    return f"{a}/{b} ({100 * a / b:.0f}%)" if b else "–"


def per_scene(a, n):
    return f"{a} ({a / n:.2f}/scene)" if n else "–"


def metrics(recs, key_by_sample, sample_ids, n_scenes):
    items = [r for r in recs if r["kind"] == "item"]
    f = [item_flags(r) for r in items]
    n = len(items)
    corr = [x for r, x in zip(items, f) if not x["comment_only"]]
    m = {}
    m["items"] = n
    m["fp"] = sum(x["false_positive"] for x in f)
    m["fp_unmatched"] = sum(x["unconfirmed"] for x in f)
    m["incorrect"] = sum(x["incorrect"] for x in f)
    m["clean"] = sum(not x["false_positive"] and not x["incorrect"] and not x["after_not_correct"] for x in f)
    m["after_bad"] = sum(x["after_not_correct"] for x in f)
    m["with_after"] = len(corr)
    m["partial"] = sum(x["partial"] for x in f)
    m["truncated"] = sum(x["truncated"] for x in f)
    m["invalid_cat"] = sum(x["invalid_category"] for x in f)
    m["miscat"] = sum(x["miscategorized"] for x in f)
    m["miscat_coarse"] = sum(x["miscategorized_coarse"] for x in f)
    by_strength = defaultdict(lambda: [0, 0])
    for r, x in zip(items, f):
        by_strength[r["strength"]][0] += x["false_positive"]
        by_strength[r["strength"]][1] += 1
    m["fp_by_strength"] = dict(by_strength)
    # recall: her error edits covered by any located item
    key = [e for s in sample_ids for e in key_by_sample[s] if e["op"] in ("replace", "delete", "insert")]
    spans = defaultdict(list)
    for r in items:
        if r["span"]:
            spans[r["sample_id"]].append(r["span"])
    m["recall"] = (sum(any(overlaps(sp, e) for sp in spans[e["sample_id"]]) for e in key), len(key))
    m["unlocated"] = sum(r["span"] is None for r in items)
    # expressiveness
    ex = [r for r in recs if r["kind"] == "expr"]
    m["expr"] = {}
    for story in ("mengmu", "shennong"):
        e = [r for r in ex if r["sample_id"].startswith(story)]
        m["expr"][story] = (sum(bool(r["judge"] and r["judge"]["good"]) for r in e), len(e),
                            Counter(r["judge"]["problem"] for r in e if r["judge"] and not r["judge"]["good"]))
    # content
    ct = [r for r in recs if r["kind"] == "content"]
    her_flagged = caught = sys_flag_wrong = notes = notes_ok = notes_clear = notes_regex = 0
    for r in ct:
        for s in r["judge"]["scenes"]:
            if s["teacher"] != "none":
                her_flagged += 1
                caught += s["system"] != "none"
        for i, nt in enumerate(r["notes"]):
            notes += 1
            jv = next((x for x in r["judge"]["notes"] if x["n"] == i + 1), None)
            notes_ok += bool(jv and jv["correct"])
            notes_clear += bool(jv and jv["clear"])
            notes_regex += bool(re.search(r"\bmiss|\bneed", nt, re.I))
    m["content"] = {"her_flagged": her_flagged, "caught": caught, "notes": notes, "notes_correct": notes_ok,
                    "notes_clear": notes_clear, "notes_miss_need": notes_regex}
    m["n_scenes"] = n_scenes
    return m


# ---------------------------------------------------------------- validation against her comments

def validate(recs_v2):
    """Her tagged comments on v2 S0 vs the judge, item by item (her comments are not exhaustive)."""
    comments = [json.loads(l) for l in open(HER_S0_COMMENTS, encoding="utf-8")]
    items = [r for r in recs_v2 if r["kind"] == "item"]
    rows = defaultdict(lambda: [0, 0])  # tag -> [judge agrees, her tagged items matched]
    unmatched = 0
    tag_to_flag = {"false_positive": "false_positive", "incorrect_correction": None, "partial_sentence": "partial",
                   "miscategorized": "miscategorized"}
    for c in comments:
        if c["section"] not in ("Grammar", "Vocabulary", "Coherence", "Content", "Other"):
            continue
        b, a = squash(c["before"]), squash(c["after"])
        cands = [r for r in items if r["sample_id"] == c["sample_id"] and r["scene"] == c["scene"]
                 and b and (b == squash(r["before"]) or (b in squash(r["before"]) and a and a in squash(r["after"] or "")))]
        if not cands:
            unmatched += 1
            continue
        x = item_flags(cands[0])
        for tag in c["tags"]:
            if tag not in tag_to_flag:
                continue
            if tag == "incorrect_correction":
                hit = x["incorrect"] or x["after_not_correct"] or x["false_positive"]
            else:
                hit = x[tag_to_flag[tag]]
            rows[tag][0] += hit
            rows[tag][1] += 1
    return rows, unmatched, len(comments)


# ---------------------------------------------------------------- main

def main():
    ts = {s["sample_id"]: s for s in json.load(open(TEST_SET, encoding="utf-8"))["samples"]}
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    csamples = {s["sample_id"]: s for s in corpus["samples"]}
    scene_lists = {s["story_id"]: s for s in corpus["scene_lists"]}
    v2 = {d["sample_id"]: d for d in json.load(open(V2 / "runs" / "S0" / "feedback.json", encoding="utf-8"))}
    key_by_sample = defaultdict(list)
    for l in open(KEY, encoding="utf-8"):
        e = json.loads(l)
        key_by_sample[e["sample_id"]].append(e)

    def sample(sid, scenes):
        cs = csamples[sid]
        sl = scene_lists.get(cs["story_id"])
        return {"sample_id": sid, "text": cs["text"], "scenes": scenes, "content_flags": cs["content_flags"],
                "scene_list": sl["scenes"] if sl else None, "title": sl["title"] if sl else cs["story_id"]}

    jobs = []
    for sid, s in ts.items():
        smp = sample(sid, s["scenes"])
        jobs.append(("v1-S5", smp, load_v1("S5", sid, s["scenes"])))
        jobs.append(("v1-S6", smp, load_v1("S6", sid, s["scenes"])))
        jobs.append(("v2-S0", smp, load_v2(v2[sid])))
    for sid in VALIDATION_STORIES:
        if sid not in ts:
            smp = sample(sid, [x["text"] for x in v2[sid]["scenes"]])
            jobs.append(("v2-S0-val", smp, load_v2(v2[sid])))

    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(lambda j: build(j[0], j[1], j[2], key_by_sample), jobs))
    recs = [r for rs in results for r in rs]
    with open(ITEMS_OUT, "w", encoding="utf-8") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    sids = list(ts)
    M = {s: metrics([r for r in recs if r["system"] == s], key_by_sample, sids, 18) for s in SYSTEMS}
    val_recs = [r for r in recs if r["system"] in ("v2-S0", "v2-S0-val") and r["sample_id"] in VALIDATION_STORIES]
    val, val_unmatched, val_total = validate(val_recs)
    write_report(M, val, val_unmatched, val_total, recs)
    print(f"wrote {REPORT.relative_to(REPO)} and {ITEMS_OUT.relative_to(REPO)}")


def write_report(M, val, val_unmatched, val_total, recs):
    S = SYSTEMS
    row = lambda label, f: f"| {label} | " + " | ".join(f(M[s]) for s in S) + " |"
    L = ["# v1 vs v2, scored on the teacher's critique", "",
         "Stories: the 6 held-out stories of the v1 eval (mengmu #10, #32, #45; shennong #8, #19, #33), 18 scenes, "
         "the same scene splits in both systems. v1 = eval stages S5 and S6 (`eval/runs/`); v2 = "
         "`chinese_writing_rag_pipeline_v2/runs/S0`. Nothing was regenerated.", "",
         f"Judge: {MODEL} ({EFFORT}), blind to the system, given her corrections on each scene as reference. "
         f"Prompt versions: items {prompt_version(JUDGE_SYSTEM, JUDGE_SCHEMA)}, expressiveness "
         f"{prompt_version(EXPR_SYSTEM, EXPR_SCHEMA)}, content {prompt_version(CONTENT_SYSTEM, CONTENT_SCHEMA)}. "
         "Where she corrected a place, the item counts as a real error whatever the judge says.", "",
         "| | " + " | ".join(S) + " |", "|---|" + "---|" * len(S),
         row("Correction items shown", lambda m: str(m["items"])),
         "| **4. False positives and incorrect corrections** (her top priority) | | | |",
         row("False positives (judged)", lambda m: per_scene(m["fp"], m["n_scenes"])),
         row("&nbsp;&nbsp;worst case: every item at a place she did not mark", lambda m: per_scene(m["fp_unmatched"], m["n_scenes"])),
         row("Incorrect corrections (real error, wrong fix)", lambda m: per_scene(m["incorrect"], m["n_scenes"])),
         row("Items fully right (real error, right fix, clean corrected text)", lambda m: pct(m["clean"], m["items"])),
         "| **2. Corrected version** | | | |",
         row("Corrected text after → not fully correct", lambda m: pct(m["after_bad"], m["with_after"])),
         "| **1. Partial sentences** | | | |",
         row("Shown text partial (truncated or judged incomplete)", lambda m: pct(m["partial"], m["items"])),
         row("&nbsp;&nbsp;of which truncated with …", lambda m: pct(m["truncated"], m["items"])),
         "| **3. Categories** | | | |",
         row("In Other / Content", lambda m: pct(m["invalid_cat"], m["items"])),
         row("Wrong category (as shown)", lambda m: pct(m["miscat"], m["items"])),
         row("Wrong category, Grammar and Vocabulary merged", lambda m: pct(m["miscat_coarse"], m["items"])),
         "| **5. End-of-story content** | | | |",
         row("Scenes she flagged, caught", lambda m: pct(m["content"]["caught"], m["content"]["her_flagged"])),
         row("Content notes that are correct", lambda m: pct(m["content"]["notes_correct"], m["content"]["notes"])),
         row("Content notes that are clear (judged)", lambda m: pct(m["content"]["notes_clear"], m["content"]["notes"])),
         row("Content notes worded 'miss…' / 'need…'", lambda m: pct(m["content"]["notes_miss_need"], m["content"]["notes"])),
         "| **6. Expressiveness** | | | |",
         row("Good ideas: 孟母", lambda m: pct(*m["expr"]["mengmu"][:2])),
         row("Good ideas: 神农", lambda m: pct(*m["expr"]["shennong"][:2])),
         "| **Recall (last)** | | | |",
         row("Her corrections covered by an item", lambda m: pct(*m["recall"])),
         row("Items whose student words could not be located", lambda m: str(m["unlocated"])),
         ""]
    L += ["## False positives by strength (v2 marks some items as suggestions)", ""]
    for s in S:
        L.append(f"- {s}: " + ", ".join(f"{k} {pct(v[0], v[1])}" for k, v in M[s]["fp_by_strength"].items()))
    L += ["", "## Expressiveness problems (judged)", ""]
    for s in S:
        L.append(f"- {s}: 孟母 {dict(M[s]['expr']['mengmu'][2])}; 神农 {dict(M[s]['expr']['shennong'][2])}")
    L += ["", "## How far to trust the judge", "",
          f"Her tagged comments on v2's feedback (6 stories, {val_total} comments) were matched to v2's items. "
          "For each kind of problem she named, the share the judge also caught (her comments are not exhaustive, "
          "so this measures whether the judge sees what she sees, not how much else it flags):", ""]
    for tag, (hit, tot) in sorted(val.items()):
        L.append(f"- {tag}: {pct(hit, tot)}")
    L.append(f"- comments on correction items that could not be matched to an item: {val_unmatched}")
    L += ["", "## Every false positive and incorrect correction", ""]
    for s in S:
        L += [f"### {s}", ""]
        for r in recs:
            if r["system"] != s or r["kind"] != "item":
                continue
            x = item_flags(r)
            bad = [k for k in ("false_positive", "incorrect", "after_not_correct", "partial", "miscategorized") if x[k]]
            if x["false_positive"] or x["incorrect"] or x["after_not_correct"]:
                L.append(f"- {r['sample_id']} scene {r['scene']} [{r['section']}] `{r['shown'][:120]}` -- "
                         f"{', '.join(bad)} -- {(r['judge'] or {}).get('reason', '')}")
        L.append("")
    REPORT.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
