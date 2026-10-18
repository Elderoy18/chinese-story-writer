#!/usr/bin/env python3
"""Step 2 -- turn the extracted BASIC data into one structured corpus.

    data/01_extracted/basic_data/*.json, raw/stories.json  ->  data/02_corpus/corpus.json
                                                               data/02_corpus/parse_units.jsonl
                                                               reports/02_corpus.md

Only the basic data is read here (graded samples, model stories, the required-scene
lists and the coherence rubric). The feedback data is parsed in its own later stage,
so the baseline built on this corpus contains none of it.

Documents are recognized by their headers, not their file names:
  - model stories doc : "Story N: <title>" followed by the story text
  - samples doc       : "Student N", the student's story, "Teacher feedback:",
                        one feedback line per paragraph, content flags
                        ("Miss ...", "Wrong information ...", "Coherence problem ...")
                        and the closing note. The story comes from the file name
                        (the "match" words in raw/stories.json).

What this step adds over the paragraphs:
  - sentences: every student story and model story is split into sentences,
    each with its start/end position in the story text.
  - feedback lines: the student text the teacher quoted is LOCATED in the story
    (start/end position), and the rest of the line is split into parts (one per
    "；"/";") and each part into pieces, each labelled fix (the teacher's Chinese
    correction), note (her explanation) or instruction (delete/add ...).
    Bold ranges from step 1 are carried onto the pieces.
  - scene_lists: the teacher's required scenes per story (story_scenes.md),
    with the stated number of scenes checked against the list.
  - rubric: her coherence rules and metric definitions (Coherence reference
    temporality rules.md), as sections (heading + text), for later prompts.
  - parse_units.jsonl: every piece of Chinese HanLP will parse later (student
    sentences, model-story sentences, teacher fixes), one per line, with a
    stable unit_id and its position in its source -- so the parser runs once
    and its output joins back to the corpus by unit_id.

Working out exactly which characters the teacher changed is NOT done here; it
is the next step, built on these located quotes and labelled pieces.

Standard library only.
"""
import json
import re
import sys
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "raw" / "stories.json"
IN_DIR = ROOT / "data" / "01_extracted" / "basic_data"
SCENE_LISTS = "story_scenes.json"                           # extracted from story_scenes.md
RUBRIC = "Coherence reference temporality rules.json"       # extracted from the .md
OUT_DIR = ROOT / "data" / "02_corpus"
REPORT = ROOT / "reports" / "02_corpus.md"

MODEL_HEADER = re.compile(r"^Story\s*#?\s*(\d+)\s*[:：]\s*(.+)$", re.I)
STUDENT_HEADER = re.compile(r"^Student\s*#?\s*(\d+)\s*[:：]?\s*(.*)$", re.I)
TEACHER_MARKER = re.compile(r"^Teacher feedback\s*[:：]?$", re.I)
FLAG_TYPES = (("Miss", "miss_scene"), ("Wrong information", "wrong_information"), ("Coherence problem", "coherence_problem"))
CLOSING_NOTE = re.compile(r"^Try to include more details")

SENTENCE_END = "。！？!?；;\n"
CLOSERS = "”’」』）)\"'"
PUNCT = re.compile(r"[\s，。！？、；：,.!?;:“”‘’\"'（）()「」『』《》…—\-]")
# Not \b: Python counts Chinese characters as word characters, so "delete我" has no boundary.
INSTRUCTION = re.compile(r"^(delete|add|remove|omit|insert)(?![A-Za-z])", re.I)
# "秋季期间 not very natural: ..." -- the quote, then an English note before the colon.
QUOTE_WITH_NOTE = re.compile(r"^(.*?[^\sA-Za-z.,])\s+([A-Za-z].*)$")
LATIN = re.compile(r"[A-Za-z]")
FUZZY_MIN = 0.6


class FormatError(Exception):
    pass


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
def load_registry():
    stories = json.load(open(REGISTRY, encoding="utf-8"))["stories"]
    dupes = [i for i, n in Counter(s["story_id"] for s in stories).items() if n > 1]
    if dupes:
        raise FormatError(f"{REGISTRY.name}: duplicate story_id {dupes}")
    return stories


def story_by_title(registry, title, where):
    for s in registry:
        if s["title"] == title:
            return s
    raise FormatError(f'{where}: story "{title}" is not in raw/stories.json -- add an entry for it')


def story_by_filename(registry, stem, where):
    hits = [s for s in registry if any(m in stem for m in s["match"])]
    if len(hits) != 1:
        raise FormatError(
            f'{where}: file name "{stem}" matches {len(hits)} stories in raw/stories.json '
            f'({", ".join(s["story_id"] for s in hits) or "none"}); it must match exactly one'
        )
    return hits[0]


def sample_id(story, num):
    return f"{story.get('sample_id_prefix', story['story_id'])}#{num}"


# ---------------------------------------------------------------------------
# Sentences
# ---------------------------------------------------------------------------
def split_sentences(text):
    """[{sid, start, end, text}] -- ends at 。！？；/newline, keeping closing quotes."""
    out, start, i = [], 0, 0
    while i < len(text):
        if text[i] in SENTENCE_END:
            j = i + 1
            while j < len(text) and text[j] in CLOSERS:
                j += 1
            add_sentence(out, text, start, j)
            start = i = j
        else:
            i += 1
    add_sentence(out, text, start, len(text))
    return out


def add_sentence(out, text, start, end):
    seg = text[start:end]
    lead = len(seg) - len(seg.lstrip())
    s, e = start + lead, start + len(seg.rstrip())
    if e > s:
        out.append({"sid": f"s{len(out)}", "start": s, "end": e, "text": text[s:e]})


def sentences_covering(sentences, start, end):
    return [s["sid"] for s in sentences if s["start"] < end and s["end"] > start]


# ---------------------------------------------------------------------------
# Locating a quote in the story text
# ---------------------------------------------------------------------------
def squeeze(text):
    """Text without spaces/punctuation, plus the original index of each kept character."""
    keep = [(i, ch) for i, ch in enumerate(text) if not PUNCT.match(ch)]
    return "".join(ch for _, ch in keep), [i for i, _ in keep]


def locate(quote, text, after=0):
    """Where the teacher's quote sits in the story text.
    exact -> same characters; normalized -> same once spaces/punctuation are
    ignored; fuzzy -> best window with similarity >= FUZZY_MIN. Prefers the
    first match at or after `after` (the teacher comments in story order)."""
    hits = [m.start() for m in re.finditer(re.escape(quote), text)]
    if hits:
        s = next((h for h in hits if h >= after), hits[0])
        return {"start": s, "end": s + len(quote), "match": "exact", "score": 1.0}

    q, _ = squeeze(quote)
    t, idx = squeeze(text)
    if not q:
        return {"start": None, "end": None, "match": "not_found", "score": 0.0}
    hits = [m.start() for m in re.finditer(re.escape(q), t)]
    if hits:
        after_sq = next((k for k, i in enumerate(idx) if i >= after), 0)
        k = next((h for h in hits if h >= after_sq), hits[0])
        return {"start": idx[k], "end": idx[k + len(q) - 1] + 1, "match": "normalized", "score": 1.0}

    best, best_k, n = 0.0, None, len(q)
    for k in range(0, max(1, len(t) - n + 1)):
        r = SequenceMatcher(None, q, t[k:k + n], autojunk=False).ratio()
        if r > best:
            best, best_k = r, k
    if best_k is not None and best >= FUZZY_MIN:
        end_k = min(best_k + n, len(t)) - 1
        return {"start": idx[best_k], "end": idx[end_k] + 1, "match": "fuzzy", "score": round(best, 3)}
    return {"start": None, "end": None, "match": "not_found", "score": round(best, 3)}


# ---------------------------------------------------------------------------
# Splitting a feedback line
# ---------------------------------------------------------------------------
def quote_and_note(left):
    """Left of the colon -> (quote, note). Usually all quote; in some lines the
    teacher writes an English note after it ("秋季期间 not very natural")."""
    left = left.strip()
    m = QUOTE_WITH_NOTE.match(left)
    if m and LATIN.search(m.group(2)):
        return m.group(1).strip().strip("“”\"'"), m.group(2).strip()
    return left, None


def split_quote(line, story_text):
    """(quote, quote_note, body, body_offset). The quote ends at a colon; when the
    student's own text contains a colon (他说：...), take the first colon whose
    left side is found in the story."""
    colons = [m.start() for m in re.finditer("[：:]", line)]
    if not colons:
        return None
    for c in colons:
        if locate(line[:c].strip(), story_text)["match"] in ("exact", "normalized"):
            return line[:c].strip(), None, line[c + 1:], c + 1
    for c in colons:
        quote, note = quote_and_note(line[:c])
        if note and locate(quote, story_text)["match"] in ("exact", "normalized"):
            return quote, note, line[c + 1:], c + 1
    c = colons[0]
    return line[:c].strip(), None, line[c + 1:], c + 1


def piece_kind(text):
    if INSTRUCTION.match(text):
        return "instruction"
    if LATIN.search(text):
        return "note"
    return "fix"


def split_body(body, offset, bold):
    """Parts (split on ；/;), each a list of pieces (split on the full-width ，).
    Consecutive note pieces are merged back into one note, since English notes
    use ，too. Every piece keeps its position in the paragraph and its bold ranges."""
    parts = []
    for pm in re.finditer(r"[^；;]+", body):
        pieces = []
        for km in re.finditer(r"[^，]+", pm.group()):
            raw = km.group()
            lead = len(raw) - len(raw.lstrip())
            text = raw.strip()
            if not text:
                continue
            start = offset + pm.start() + km.start() + lead
            kind = piece_kind(text)
            if pieces and kind == "note" and pieces[-1]["kind"] == "note":
                prev = pieces[-1]
                prev["text"] += "，" + text
                prev["end"] = start + len(text)
                continue
            pieces.append({"kind": kind, "text": text, "start": start, "end": start + len(text)})
        for p in pieces:
            p["bold"] = [[max(s, p["start"]) - p["start"], min(e, p["end"]) - p["start"]]
                         for s, e in bold if s < p["end"] and e > p["start"]]
            if p["kind"] == "fix":
                p["alternatives"] = [a.strip() for a in p["text"].split("/") if a.strip()]
        if pieces:
            kinds = [p["kind"] for p in pieces]
            check = []
            if "fix" in kinds and "note" in kinds and kinds.index("note") < len(kinds) - 1 - kinds[::-1].index("fix"):
                check.append("Chinese after a note in the same part (may be an example, not a fix)")
            parts.append({"pid": f"p{len(parts)}", "raw": pm.group().strip(), "pieces": pieces, "check": check})
    return parts


def parse_flag(text, ftype):
    body = re.split(r"[:：]", text, maxsplit=1)
    scenes = []
    if ftype == "miss_scene" and len(body) == 2:
        scenes = [s.strip() for s in re.split(r"[；;]", body[1]) if s.strip()]
    return {"type": ftype, "raw": text, "scenes": scenes}


# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------
def split_blocks(paras, header, where):
    blocks = []
    for p in paras:
        m = header.match(p["text"])
        if m:
            blocks.append((m, []))
        elif blocks:
            blocks[-1][1].append(p)
        else:
            raise FormatError(f'{where}: text before the first header: "{p["text"][:60]}"')
    dupes = [n for n, c in Counter(m.group(1) for m, _ in blocks).items() if c > 1]
    if dupes:
        raise FormatError(f"{where}: header number(s) used twice: {dupes}")
    return blocks


def parse_model_doc(paras, registry, where):
    out = []
    for m, body in split_blocks(paras, MODEL_HEADER, where):
        title = m.group(2).strip()
        story = story_by_title(registry, title, where)
        if not body:
            raise FormatError(f'{where}: "Story {m.group(1)}: {title}" has no story text')
        text = "\n".join(p["text"] for p in body)
        out.append({"story_id": story["story_id"], "title": title, "text": text, "sentences": split_sentences(text)})
    return out


def parse_samples_doc(paras, story, source_doc, where):
    samples = []
    for m, body in split_blocks(paras, STUDENT_HEADER, where):
        num = m.group(1)
        marker = next((i for i, p in enumerate(body) if TEACHER_MARKER.match(p["text"])), None)
        if marker is None:
            raise FormatError(f'{where}: Student {num} has no "Teacher feedback:" line')
        glued = [m.group(2)] if m.group(2) else []
        text = "\n".join(glued + [p["text"] for p in body[:marker]])
        if not text:
            raise FormatError(f"{where}: Student {num} has no story text")
        sentences = split_sentences(text)

        feedback, flags, closing, unparsed, after = [], [], None, [], 0
        for p in body[marker + 1:]:
            line = p["text"]
            if CLOSING_NOTE.match(line):
                closing = line
                continue
            ftype = next((t for prefix, t in FLAG_TYPES if line.startswith(prefix)), None)
            if ftype:
                flags.append(parse_flag(line, ftype))
                continue
            split = split_quote(line, text)
            if split is None:
                unparsed.append(line)
                continue
            quote, quote_note, body_text, offset = split
            loc = locate(quote, text, after)
            if loc["start"] is not None:
                after = loc["start"]
                loc["sentence_ids"] = sentences_covering(sentences, loc["start"], loc["end"])
                loc["story_text"] = text[loc["start"]:loc["end"]]
            feedback.append({
                "fid": f"f{len(feedback)}",
                "raw": line,
                "quote": quote,
                "quote_note": quote_note,
                "location": loc,
                "parts": split_body(body_text, offset, p["bold"]),
            })

        samples.append({
            "sample_id": sample_id(story, num),
            "story_id": story["story_id"],
            "source_doc": source_doc,
            "sample_num": int(num),
            "text": text,
            "sentences": sentences,
            "feedback": feedback,
            "content_flags": flags,
            "closing_note": closing,
            "unparsed_lines": unparsed,
        })
    return samples


# ---------------------------------------------------------------------------
# The teacher's required-scene lists (story_scenes.md)
# ---------------------------------------------------------------------------
NUMBER_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen".split())}


def parse_scene_lists(registry, paras):
    """'**Story N: <title>**' then '<Number> scenes: a; b；c' -> [{story_id, title, scenes}].
    The stated number of scenes is checked against the list."""
    text = "\n\n".join(p["text"] for p in paras)
    out = []
    for m in re.finditer(r"\*\*Story\s*\d+\s*[:：]\s*(.+?)\*\*\s*\n+\s*(\w+)\s+scenes?\s*[:：]\s*(.+)", text):
        title, count, body = m.group(1).strip(), m.group(2).lower(), m.group(3).strip()
        story = story_by_title(registry, title, SCENE_LISTS)
        scenes = [s.strip() for s in re.split(r"[;；]", body) if s.strip()]
        if NUMBER_WORDS.get(count) != len(scenes):
            raise FormatError(f'{SCENE_LISTS}: "{title}" says {count} scenes but lists {len(scenes)}')
        out.append({"story_id": story["story_id"], "title": title, "scenes": scenes})
    return out


def parse_rubric(paras):
    """Her coherence rubric as sections: a '#'/'##' heading starts a section; the
    paragraphs under it are its text."""
    sections = []
    for p in paras:
        t = p["text"]
        if t.startswith("#"):
            sections.append({"heading": t.lstrip("#").strip(), "text": ""})
        elif sections:
            sections[-1]["text"] = (sections[-1]["text"] + "\n\n" + t).strip()
        else:
            raise FormatError(f'{RUBRIC}: text before the first heading: "{t[:60]}"')
    return sections


# ---------------------------------------------------------------------------
# HanLP parse units
# ---------------------------------------------------------------------------
def parse_units(corpus):
    """Every piece of Chinese the parser will need, keyed by a stable unit_id."""
    for m in corpus["model_stories"]:
        for s in m["sentences"]:
            yield {"unit_id": f"model:{m['story_id']}/{s['sid']}", "kind": "model_sentence", "text": s["text"],
                   "source": {"story_id": m["story_id"], "start": s["start"], "end": s["end"]}}
    for smp in corpus["samples"]:
        for s in smp["sentences"]:
            yield {"unit_id": f"{smp['sample_id']}/{s['sid']}", "kind": "student_sentence", "text": s["text"],
                   "source": {"sample_id": smp["sample_id"], "start": s["start"], "end": s["end"]}}
        for f in smp["feedback"]:
            for part in f["parts"]:
                for k, piece in enumerate(part["pieces"]):
                    if piece["kind"] != "fix":
                        continue
                    for a, alt in enumerate(piece["alternatives"]):
                        yield {"unit_id": f"{smp['sample_id']}/{f['fid']}/{part['pid']}/k{k}/a{a}", "kind": "teacher_fix",
                               "text": alt, "source": {"sample_id": smp["sample_id"], "fid": f["fid"], "pid": part["pid"], "piece": k}}


# ---------------------------------------------------------------------------
def main():
    registry = load_registry()
    files = sorted(IN_DIR.glob("*.json"))
    if not files:
        sys.exit(f"No files in {IN_DIR} -- run 01_extract.py first")

    corpus = {"model_stories": [], "samples": []}
    special = {}
    for path in files:
        doc = json.load(open(path, encoding="utf-8"))
        if path.name in (SCENE_LISTS, RUBRIC):
            special[path.name] = doc["paragraphs"]
            continue
        paras, where = doc["paragraphs"], doc["source_file"]
        if any(STUDENT_HEADER.match(p["text"]) for p in paras):
            story = story_by_filename(registry, path.stem, where)
            samples = parse_samples_doc(paras, story, path.stem, where)
            corpus["samples"].extend(samples)
            print(f"{where}: {len(samples)} samples -> {story['story_id']}")
        elif any(MODEL_HEADER.match(p["text"]) for p in paras):
            models = parse_model_doc(paras, registry, where)
            corpus["model_stories"].extend(models)
            print(f"{where}: {len(models)} model stories")
        else:
            raise FormatError(f'{where}: no "Student N" or "Story N: <title>" headers found')

    dupes = [i for i, n in Counter(s["sample_id"] for s in corpus["samples"]).items() if n > 1]
    if dupes:
        raise FormatError(f"two samples docs share a story and student numbers: {dupes[:5]}")
    rank = {s["story_id"]: i for i, s in enumerate(registry)}
    corpus["samples"].sort(key=lambda s: (rank[s["story_id"]], s["sample_num"]))
    for name in (SCENE_LISTS, RUBRIC):
        if name not in special:
            raise FormatError(f"{name} missing from {IN_DIR}")
    corpus["scene_lists"] = parse_scene_lists(registry, special[SCENE_LISTS])
    corpus["rubric"] = parse_rubric(special[RUBRIC])
    print(f"rubric: {len(corpus['rubric'])} sections")
    print(f"{SCENE_LISTS}: " + ", ".join(f"{s['story_id']} {len(s['scenes'])}" for s in corpus["scene_lists"]))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "corpus.json", "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=1)
    units = list(parse_units(corpus))
    with open(OUT_DIR / "parse_units.jsonl", "w", encoding="utf-8") as f:
        for u in units:
            f.write(json.dumps(u, ensure_ascii=False) + "\n")

    write_report(corpus, units)
    print(f"Wrote data/02_corpus/corpus.json, data/02_corpus/parse_units.jsonl ({len(units)} units)")
    print(f"Report: {REPORT.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def write_report(corpus, units):
    samples = corpus["samples"]
    fb = [(s, f) for s in samples for f in s["feedback"]]
    parts = [(s, f, p) for s, f in fb for p in f["parts"]]
    pieces = [k for _, _, p in parts for k in p["pieces"]]
    match = Counter(f["location"]["match"] for _, f in fb)

    L = ["# Step 2 report: paragraphs -> corpus", ""]
    L += ["## Counts", "", "| Story | Samples | Sentences | Feedback lines | Parts | Content flags |", "|---|---|---|---|---|---|"]
    for sid in dict.fromkeys(s["story_id"] for s in samples):
        ss = [s for s in samples if s["story_id"] == sid]
        L.append(f"| {sid} | {len(ss)} | {sum(len(s['sentences']) for s in ss)} | {sum(len(s['feedback']) for s in ss)} | "
                 f"{sum(len(f['parts']) for s in ss for f in s['feedback'])} | {sum(len(s['content_flags']) for s in ss)} |")
    L += ["", f"Model stories: {', '.join(m['story_id'] for m in corpus['model_stories'])} "
              f"({sum(len(m['sentences']) for m in corpus['model_stories'])} sentences)", ""]

    L += ["## Locating the teacher's quotes in the student's story", "",
          "Each feedback line starts with the student text the teacher is commenting on. This is where it was found:", "",
          "| Match | Lines | Meaning |", "|---|---|---|",
          f"| exact | {match['exact']} | same characters |",
          f"| normalized | {match['normalized']} | same once spaces and punctuation are ignored |",
          f"| fuzzy | {match['fuzzy']} | close but not identical (similarity >= {FUZZY_MIN}) -- **check** |",
          f"| not_found | {match['not_found']} | not found -- **check** |", ""]
    for kind in ("fuzzy", "not_found"):
        rows = [(s, f) for s, f in fb if f["location"]["match"] == kind]
        if rows:
            L += [f"### {kind} ({len(rows)})", ""]
            for s, f in rows:
                loc = f["location"]
                found = f' → story has "{loc["story_text"]}"' if loc.get("story_text") else ""
                L.append(f'- {s["sample_id"]} {f["fid"]} (score {loc["score"]}): teacher quoted "{f["quote"]}"{found}')
            L.append("")

    kinds = Counter(k["kind"] for k in pieces)
    L += ["## Splitting the teacher's feedback", "",
          "After the quote, each line is split into parts (on ；/;) and each part into pieces labelled",
          "**fix** (Chinese correction), **note** (explanation, contains Latin letters) or **instruction** (starts with delete/add/...).", "",
          f"- parts: {len(parts)}; pieces: fix {kinds['fix']}, note {kinds['note']}, instruction {kinds['instruction']}",
          f"- parts with no fix (note or instruction only): {sum(1 for _, _, p in parts if not any(k['kind'] == 'fix' for k in p['pieces']))}",
          f"- fixes with alternatives (A/B): {sum(1 for k in pieces if k['kind'] == 'fix' and len(k['alternatives']) > 1)}",
          f"- pieces with bold characters: {sum(1 for k in pieces if k['bold'])}", ""]
    flagged = [(s, f, p) for s, f, p in parts if p["check"]]
    L += [f"### Parts to check ({len(flagged)})", ""]
    for s, f, p in flagged:
        L.append(f'- {s["sample_id"]} {f["fid"]}{p["pid"]}: {p["check"][0]} -- ' +
                 " | ".join(f'[{k["kind"]}] {k["text"]}' for k in p["pieces"]))
    unparsed = [(s, u) for s in samples for u in s["unparsed_lines"]]
    L += ["", f"### Feedback lines with no colon, not parsed ({len(unparsed)})", ""]
    L += [f"- {s['sample_id']}: {u}" for s, u in unparsed] or ["None."]

    ftypes = Counter(fl["type"] for s in samples for fl in s["content_flags"])
    L += ["", "## Content flags", "", *[f"- {t}: {n}" for t, n in ftypes.most_common()],
          f"- missing scenes listed: {sum(len(fl['scenes']) for s in samples for fl in s['content_flags'])}",
          f"- samples without the closing note: {sum(1 for s in samples if not s['closing_note'])}", ""]

    L += ["## The teacher's required-scene lists (`story_scenes.md`)", ""]
    for sl in corpus.get("scene_lists", []):
        L += [f"**{sl['title']}** ({len(sl['scenes'])} scenes)", ""] + [f"{i + 1}. {s}" for i, s in enumerate(sl["scenes"])] + [""]

    uk = Counter(u["kind"] for u in units)
    L += ["## The teacher's coherence rubric", ""]
    for sec in corpus.get("rubric", []):
        L += [f"**{sec['heading']}** ({len(sec['text'])} characters)", ""]
    L += ["## HanLP parse units (`parse_units.jsonl`)", "",
          *[f"- {k}: {n}" for k, n in uk.items()], ""]

    L += ["## Three samples in full, for checking", ""]
    for s in [samples[0], next(x for x in samples if x["story_id"] == "shennong_chang_baicao"),
              next(x for x in samples if x["story_id"] == "pear_story")]:
        L += [f"### {s['sample_id']}", "", "Sentences:", ""]
        L += [f"- {x['sid']} [{x['start']}-{x['end']}] {x['text']}" for x in s["sentences"]]
        L += ["", "Feedback:", ""]
        for f in s["feedback"]:
            loc = f["location"]
            L.append(f'- **{f["fid"]}** "{f["quote"]}" → {loc["match"]} [{loc["start"]}-{loc["end"]}] in {", ".join(loc.get("sentence_ids", []))}')
            for p in f["parts"]:
                L.append(f"  - {p['pid']}: " + " | ".join(
                    f'[{k["kind"]}] {k["text"]}' + (f' (bold: {", ".join(k["text"][a:b] for a, b in k["bold"])})' if k["bold"] else "")
                    for k in p["pieces"]))
        L += ["", "Content flags:", ""] + [f"- [{fl['type']}] {fl['raw']}" for fl in s["content_flags"]] + [""]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except FormatError as e:
        sys.exit(f"FORMAT ERROR: {e}")
