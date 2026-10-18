#!/usr/bin/env python3
"""Step 13 -- the teacher finder: her own patterns and HanLP checks of her
rules, as a third finder next to the LLM (step 6) and the GEC model (step 8).

    data/11_categories/edits_train.jsonl, data/04_parse/parses.jsonl, data/03_split/split.json
        ->  data/13_find_teacher/patterns.json        patterns mined from her train corrections
            data/13_find_teacher/candidates.jsonl     candidates on the test scenes (scored by step 7)
            data/13_find_teacher/run_info.json
            reports/13_find_teacher.md                what each part finds, on train and test

    python scripts/13_find_teacher.py
    python scripts/07_score.py 13_find_teacher
    python scripts/07_score.py 06_find_baseline 08_find_gec 13_find_teacher

No LLM: everything here is deterministic -- same input, same output.

Part A, her patterns (mined from the TRAIN edits only):
  wording   a learner wording she corrected (古代的时候 -> 在古代). Kept only if,
            across the train stories, she corrected it in at least
            MIN_PRECISION of the places it occurs and at least MIN_COUNT times
            -- so "delete 他们" (他们 is usually fine) is not kept.
  insertion a word after which she added the same thing (看 -> 看到, 找 -> 找到),
            kept by the same rule: she added it in at least MIN_PRECISION of
            the places the word occurs without it.
  Both must come from corrections in at least MIN_STORIES different stories.
  A match must start and end on HanLP word boundaries (so 他们 never matches
  inside 其他们...).

Part B, HanLP checks of her rules (one per rule card whose errors have a
regular grammatical shape; see the cards' edit shapes):
  no_le_speaking_word / no_le_mental_state / modal  了 (AS) right after a speaking,
                                mental-state or modal verb (her rubric's zero-particle cases)
  no_le_with_mei               没/没有 + V. + 了
  zero_redundant_pronoun       a clause repeating the subject of the clause before it
  location_with_zai            V. + 在 + Place for an activity verb (玩在墓地 -> 在墓地玩)
  he_scope_coordination        和 joining verbs / clauses
  numeral_measure_word_order   Num. + MW. + 的 + N. (一筐的梨)
  first_mention_introduction   a story character's first appearance as a bare name,
                               or a story that starts with a bare pronoun
Each check's precision is measured on the train stories (share of its flags
that land on a correction she made), so weak checks are visible before test.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent.parent
EDITS = ROOT / "data" / "11_categories"
PARSES = ROOT / "data" / "04_parse" / "parses.jsonl"
SPLIT = ROOT / "data" / "03_split" / "split.json"
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
OUT_DIR = ROOT / "data" / "13_find_teacher"
REPORT = ROOT / "reports" / "13_find_teacher.md"

MIN_PRECISION = 0.5
MIN_COUNT = 2
MIN_COUNT_ONE_CHAR = 3
MIN_STORIES = 2      # a pattern must come from corrections in at least 2 different stories

spec = importlib.util.spec_from_file_location("score", ROOT / "scripts" / "07_score.py")
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)

# Word lists from her coherence rubric (zero-particle cases) and common speaking verbs.
SPEAKING = {"说", "告诉", "问", "回答", "喊", "叫道", "对说"}
MENTAL = {"知道", "觉得", "喜欢", "想", "决定", "发现", "懂", "愿意", "记得", "认为", "希望", "担心", "害怕", "怕", "以为", "相信"}
MODAL = {"要", "能", "可以", "会", "需要", "应该", "得", "别", "不准", "叫", "让", "想要", "能够"}
# Verbs that normally take 在 + Place AFTER them (住在, 放在, 坐在...): not an error.
POSTURE = {"住", "放", "坐", "躺", "站", "生", "出生", "停", "写", "挂", "留", "落", "掉", "倒", "摆", "睡", "长", "活", "藏", "种", "埋", "跪", "躲", "生活", "装", "画"}
INTRO_CUES = ("叫", "名字", "有一个", "有一位", "一个", "一位", "有个")
CHARACTERS = {"孟子", "孟母", "神农", "嫦娥", "后羿", "王母", "张骞", "甘父", "汉武帝"}
PRONOUNS = {"他", "她", "它"}


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------
def load_sentences():
    """sample -> [sentence tokens], each token with story start/end."""
    out = defaultdict(list)
    for line in open(PARSES, encoding="utf-8"):
        u = json.loads(line)
        if u["kind"] != "student_sentence" or not u["offsets_ok"]:
            continue
        toks = [dict(t, s=t["story_start"], e=t["story_start"] + len(t["text"])) for t in u["tokens"]]
        out[u["source"]["sample_id"]].append(toks)
    return out


# ---------------------------------------------------------------------------
# Part A: mining her patterns
# ---------------------------------------------------------------------------
def bare_cjk(s):
    return re.sub(r"[^一-鿿]", "", s or "")


def mine_patterns(train_edits, sents, train_ids):
    texts = {sid: "".join(t["text"] for s in sents[sid] for t in s) for sid in train_ids}

    # wordings she replaced or deleted
    corr = defaultdict(list)
    for e in train_edits:
        if e["op"] in ("replace", "delete") and e["original"] and bare_cjk(e["original"]) == e["original"]:
            corr[e["original"]].append(e)
    by_sample = defaultdict(list)
    for e in train_edits:
        by_sample[e["sample_id"]].append(e)
    wording = []
    for orig, es in corr.items():
        need = MIN_COUNT_ONE_CHAR if len(orig) == 1 else MIN_COUNT
        if len(es) < need:
            continue
        # every place the wording occurs in train, and whether any of her edits covers it
        # (古代的时候 is also corrected inside longer stretches such as 在古代的时候)
        if len({e["sample_id"] for e in es}) < MIN_STORIES:
            continue  # her habit across learners, not one learner's repeated wording
        occurs = corrected = 0
        for sid in train_ids:
            for s in sents[sid]:
                for i, j in word_spans(s, orig):
                    occurs += 1
                    span = {"start": s[i]["s"], "end": s[j - 1]["e"]}
                    corrected += any(score.overlaps(span, e) for e in by_sample[sid])
        prec = corrected / max(occurs, 1)
        if corrected >= need and prec >= MIN_PRECISION:
            fix, _ = Counter(e["corrected"] for e in es).most_common(1)[0]
            cat, _ = Counter(e["category"] for e in es).most_common(1)[0]
            wording.append({"kind": "wording", "original": orig, "corrected": fix, "category": cat,
                            "times_corrected": corrected, "times_in_train": occurs, "precision": round(prec, 2),
                            "her_notes": sorted({e["teacher_note"] for e in es if e["teacher_note"]})[:3]})

    # things she inserted after a given word (left HanLP word)
    ins = defaultdict(list)
    for e in train_edits:
        h = e.get("hanlp") or {}
        if e["op"] == "insert" and h.get("left") and e["corrected"] and len(e["corrected"]) <= 2:
            ins[(h["left"]["text"], e["corrected"])].append(e)
        # 看 -> 看到 written as a replace is the same insertion
        if e["op"] == "replace" and e["corrected"].startswith(e["original"]) and 0 < len(e["corrected"]) - len(e["original"]) <= 2 \
                and len(e["original"]) <= 2:
            ins[(e["original"], e["corrected"][len(e["original"]):])].append(e)
    insertion = []
    for (left, added), es in ins.items():
        if len(es) < MIN_COUNT_ONE_CHAR:
            continue
        without = sum(1 for sid in train_ids for s in sents[sid] for i, t in enumerate(s)
                      if t["text"] == left and not (i + 1 < len(s) and s[i + 1]["text"].startswith(added)))
        prec = len(es) / max(without, 1)
        if prec >= MIN_PRECISION:
            cat, _ = Counter(e["category"] for e in es).most_common(1)[0]
            insertion.append({"kind": "insertion", "after": left, "insert": added, "category": cat,
                              "times_corrected": len(es), "times_in_train": without, "precision": round(min(prec, 1.0), 2),
                              "her_notes": sorted({e["teacher_note"] for e in es if e["teacher_note"]})[:3]})
    return sorted(wording, key=lambda p: -p["times_corrected"]), sorted(insertion, key=lambda p: -p["times_corrected"])


def word_spans(sent, phrase):
    """(start token, end token) of every place a phrase covers whole HanLP words."""
    out = []
    for i in range(len(sent)):
        acc, j = "", i
        while j < len(sent) and len(acc) < len(phrase):
            acc += sent[j]["text"]
            j += 1
        if acc == phrase:
            out.append((i, j))
    return out


def word_matches(sentences, phrase):
    return sum(len(word_spans(s, phrase)) for s in sentences)


def apply_patterns(sentences, wording, insertion):
    out = []
    for s in sentences:
        for p in wording:
            for i, j in word_spans(s, p["original"]):
                out.append(cand(s[i]["s"], s[j - 1]["e"], p["original"], p["corrected"], p["category"],
                                f"her pattern: {p['original']} -> {p['corrected'] or '(delete)'} "
                                f"(corrected {p['times_corrected']}/{p['times_in_train']} in train)", "pattern"))
        for p in insertion:
            for i, t in enumerate(s):
                if t["text"] == p["after"] and not (i + 1 < len(s) and s[i + 1]["text"].startswith(p["insert"])):
                    out.append(cand(t["e"], t["e"], "", p["insert"], p["category"],
                                    f"her pattern: {p['after']} + {p['insert']} "
                                    f"(added {p['times_corrected']}/{p['times_in_train']} in train)", "pattern"))
    return out


# ---------------------------------------------------------------------------
# Part B: HanLP checks of her rules
# ---------------------------------------------------------------------------
def cand(start, end, original, corrected, category, why, source, op=None):
    op = op or ("insert" if not original else "delete" if corrected == "" else "replace")
    return {"start": start, "end": end, "original": original, "corrected": corrected, "op": op,
            "type": category, "why": why, "source": source}


def clauses(s):
    out, cur = [], []
    for t in s:
        if t["pos"] == "PU":
            if cur:
                out.append(cur)
            cur = []
        else:
            cur.append(t)
    if cur:
        out.append(cur)
    return out


def check_sentence(s):
    out = []
    for i, t in enumerate(s):
        prev = s[i - 1] if i else None
        # 了 after speaking / mental-state / modal verbs
        if t["text"] == "了" and t["pos"] == "AS" and prev is not None:
            for words, cat, label in ((SPEAKING, "no_le_speaking_word", "speaking verb"),
                                      (MENTAL, "no_le_mental_state", "mental-state verb"),
                                      (MODAL, "modal_and_control_verb_complements", "modal verb")):
                if prev["text"] in words:
                    out.append(cand(t["s"], t["e"], "了", "", cat, f"no 了 after the {label} {prev['text']}", "hanlp"))
                    break
        # 没 + V. + 了
        if t["text"] in ("没", "没有") and t["pos"] in ("AD", "VE"):
            for k in range(i + 1, min(i + 4, len(s) - 1)):
                if s[k]["pos"] == "VV" and s[k + 1]["text"] == "了" and s[k + 1]["pos"] == "AS":
                    out.append(cand(s[k + 1]["s"], s[k + 1]["e"], "了", "", "no_le_with_mei", "没 + V., no 了", "hanlp"))
                    break
        # V. + 在 + Place for an activity verb
        if t["text"] == "在" and t["pos"] == "P" and prev is not None and prev["pos"] == "VV" and prev["text"] not in POSTURE:
            place = []
            for u in s[i + 1:]:
                if u["pos"] in ("PU", "VV", "VA", "VC", "VE"):
                    break
                place.append(u)
            if place:
                orig = prev["text"] + "在" + "".join(u["text"] for u in place)
                out.append(cand(prev["s"], place[-1]["e"], orig, "在" + "".join(u["text"] for u in place) + prev["text"],
                                "location_with_zai", "在 + Place comes before the action: 在Place + V.", "hanlp"))
        # 和 joining verbs or clauses
        if t["text"] == "和" and prev is not None and i + 1 < len(s):
            nxt = s[i + 1]
            if prev["pos"] in ("VV", "VA") and nxt["pos"] in ("VV", "VA") or prev["pos"] == "PU":
                out.append(cand(t["s"], t["e"], "和", "", "he_scope_coordination", "和 cannot connect verb phrases / clauses",
                                "hanlp", op="comment"))
        # Num. + MW. + 的 + N.
        if t["pos"] == "CD" and i + 3 < len(s) and s[i + 1]["pos"] == "M" and s[i + 2]["text"] == "的" and s[i + 3]["pos"] == "NN"                 and s[i + 3]["text"] not in ("时候", "时"):  # 五岁的时候: 的 is needed (……的时候)
            out.append(cand(s[i + 2]["s"], s[i + 2]["e"], "的", "", "numeral_measure_word_order", "Num. + MW. + N., no 的", "hanlp"))
    # a clause repeating the subject of the clause before it
    cl = clauses(s)
    subj = lambda c: next((u for u in c[:4] if u["pos"] in ("PN", "NR") and u["rel"] in ("nsubj", "top")), None)
    for a, b in zip(cl, cl[1:]):
        sa, sb = subj(a), subj(b)
        if sa and sb and sa["text"] == sb["text"]:
            out.append(cand(sb["s"], sb["e"], sb["text"], "", "zero_redundant_pronoun",
                            f"{sb['text']} repeats the subject of the clause before: zero form", "hanlp"))
    return out


def check_story(sentences):
    """First appearance of each story character (and a story that opens with a bare pronoun)."""
    out, seen, named_anyone = [], set(), False
    for s in sentences:
        for c in clauses(s):
            text = "".join(u["text"] for u in c)
            for u in c:
                if u["text"] in PRONOUNS and not named_anyone and not seen:
                    out.append(cand(u["s"], u["e"], u["text"], None, "first_mention_introduction",
                                    "the story starts with a pronoun: introduce the character first", "hanlp", op="comment"))
                    named_anyone = True
                if u["text"] in CHARACTERS and u["text"] not in seen:
                    seen.add(u["text"])
                    named_anyone = True
                    if not any(cue in text for cue in INTRO_CUES):
                        out.append(cand(u["s"], u["e"], u["text"], None, "first_mention_introduction",
                                        f"first appearance of {u['text']}: briefly introduce who this is", "hanlp", op="comment"))
    return out


def run_finder(sentences, wording, insertion):
    found = apply_patterns(sentences, wording, insertion)
    for s in sentences:
        found += check_sentence(s)
    found += check_story(sentences)
    return found


# ---------------------------------------------------------------------------
def main():
    split = json.load(open(SPLIT, encoding="utf-8"))
    train_ids = split["train"]
    sents = load_sentences()
    train_edits = [json.loads(l) for l in open(EDITS / "edits_train.jsonl", encoding="utf-8")]
    train_edits = [e for e in train_edits if e["start"] is not None]
    texts = {s["sample_id"]: s["text"] for s in json.load(open(CORPUS, encoding="utf-8"))["samples"]}

    wording, insertion = mine_patterns(train_edits, sents, train_ids)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "patterns.json").write_text(json.dumps({"wording": wording, "insertion": insertion}, ensure_ascii=False, indent=1),
                                           encoding="utf-8")

    # calibration on train: how often each part's flags land on a correction she made there
    by_sample = defaultdict(list)
    for e in train_edits:
        by_sample[e["sample_id"]].append(e)
    train_stats = defaultdict(lambda: [0, 0, 0])  # flags, on any of her edits, on one of the same category
    for sid in train_ids:
        for c in run_finder(sents[sid], wording, insertion):
            key = c["type"] if c["source"] == "hanlp" else "her patterns"
            hits = [e for e in by_sample[sid] if score.overlaps(c, e)]
            train_stats[key][0] += 1
            train_stats[key][1] += bool(hits)
            train_stats[key][2] += any(e["category"] == c["type"] or e["second_category"] == c["type"] for e in hits)

    # the test scenes
    rows = []
    for t in split["test"]:
        sid = t["sample_id"]
        for k, c in enumerate(run_finder(sents[sid], wording, insertion)):
            scene = next((sc["scene"] for sc in t["scenes"] if sc["start"] <= c["start"] < sc["end"] + 1), None)
            rows.append({"cand_id": f"{sid}/teacher/c{k}", "sample_id": sid, "story_id": t["story_id"], "scene": scene, "run": 1,
                         **{x: c[x] for x in ("op", "start", "end", "original", "corrected", "type", "why")},
                         "corrected": c["corrected"] or "", "before": "", "after": "", "confidence": "high", "source": c["source"]})
    with open(OUT_DIR / "candidates.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    (OUT_DIR / "run_info.json").write_text(json.dumps({
        "model": "teacher patterns + HanLP checks", "reasoning_effort": "deterministic", "prompt_version": "n/a", "n_runs": 1,
        "min_precision": MIN_PRECISION, "patterns": {"wording": len(wording), "insertion": len(insertion)}}, indent=1), encoding="utf-8")

    write_report(wording, insertion, train_stats, rows, texts)
    print(f"patterns: {len(wording)} wording, {len(insertion)} insertion; test candidates: {len(rows)} -> data/13_find_teacher/candidates.jsonl")
    print(f"Report: {REPORT.relative_to(ROOT)}")


def write_report(wording, insertion, train_stats, rows, texts):
    pct = lambda a, b: f"{a}/{b} ({100 * a / b:.0f}%)" if b else "0/0"
    L = ["# Step 13 report: the teacher finder (her patterns + HanLP checks)", "",
         f"Patterns kept only if she corrected the wording in at least {MIN_PRECISION:.0%} of the places it occurs in the train stories.", "",
         "## Calibration on the train stories", "",
         "Share of each part's flags that land on a correction she made (any kind / the same kind).", "",
         "| Part | Flags on train | On one of her corrections | Of the same category |", "|---|---|---|---|"]
    for k, (n, a, s) in sorted(train_stats.items(), key=lambda kv: -kv[1][0]):
        L.append(f"| {k} | {n} | {pct(a, n)} | {pct(s, n)} |")
    L += ["", f"## Her wording patterns ({len(wording)})", "",
          "| Learner wording | Her correction | Category | Corrected / occurs in train | Her note |", "|---|---|---|---|---|"]
    L += [f"| {p['original']} | {p['corrected'] or '(delete)'} | {p['category']} | {p['times_corrected']}/{p['times_in_train']} | "
          f"{'; '.join(p['her_notes'])[:80]} |" for p in wording]
    L += ["", f"## Her insertion patterns ({len(insertion)})", "",
          "| After | She adds | Category | Added / occurs without it in train | Her note |", "|---|---|---|---|---|"]
    L += [f"| {p['after']} | {p['insert']} | {p['category']} | {p['times_corrected']}/{p['times_in_train']} | "
          f"{'; '.join(p['her_notes'])[:80]} |" for p in insertion]
    L += ["", f"## Test candidates ({len(rows)})", "", *[f"- {c['sample_id']} [{c['type']}]: {score.show(texts[c['sample_id']], c)} — {c['why']}"
                                                         for c in rows]]
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
