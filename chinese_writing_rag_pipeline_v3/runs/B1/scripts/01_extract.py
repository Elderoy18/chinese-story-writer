#!/usr/bin/env python3
"""Step 1 -- convert every raw document into paragraphs (and margin comments).

    raw/basic_data/*.docx, *.md      ->  data/01_extracted/basic_data/<name>.json
    raw/feedback_data/*.docx, *.md   ->  data/01_extracted/feedback_data/<name>.json
                                         reports/01_extract.md

Each output file:
    {"source_file", "folder", "kind": "docx" | "md",
     "paragraphs": [{"i", "text", "bold": [[start, end], ...]}],
     "comments":   [{"id", "author", "date", "text",
                     "anchor": {"start": {"p", "c"}, "end": {"p", "c"}, "text"}}]}

- bold: character ranges the teacher put in bold (the Pear Story file marks
  inserted characters this way, e.g. 摆**了**).
- comments: Word margin comments, with the exact text they are attached to.
  Most of her feedback-data documents are commented this way (e.g. "Show
  partial sentence: will cause confusion" on one AI correction). An anchor runs
  from paragraph p, character c (start) to paragraph p, character c (end,
  exclusive); its text is copied out so it can be read without the positions.
  A comment with no anchored text (a point comment) has an empty anchor text.

Character positions are preserved: the only change to the text is replacing
look-alike radical code points with the ordinary character, one character for
one (e.g. ⼈ U+2F08 -> 人), and trimming whitespace at the ends of a paragraph
(bold ranges and comment anchors are shifted to match). A position computed by
any later step points at the same character as in the Word file.

Markdown files are read as paragraphs separated by blank lines (no bold, no
comments). Standard library only: a .docx is a zip of XML.
"""
import json
import sys
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDERS = ["basic_data", "feedback_data"]
RAW = ROOT / "raw"
OUT = ROOT / "data" / "01_extracted"
REPORT = ROOT / "reports" / "01_extract.md"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# Look-alike code points from text copied out of PDFs. Kangxi radicals and CJK
# compatibility ideographs have a one-character NFKC mapping; these simplified
# radical forms do not, so they are mapped by hand.
SIMPLIFIED_RADICALS = {
    "⻋": "车", "⻝": "食", "⻓": "长", "⻔": "门", "⻢": "马", "⻜": "飞",
    "⻛": "风", "⻅": "见", "⻉": "贝", "⻚": "页", "⻥": "鱼", "⻦": "鸟",
    "⻨": "麦", "⻬": "齐", "⻘": "青", "⻄": "西", "⻆": "角",
    "⻰": "龙", "⻳": "龟", "⻩": "黄", "⻮": "齿", "⻭": "齿",
}


def normalize_char(ch):
    """One character in, one character out (positions must not move)."""
    if ch in SIMPLIFIED_RADICALS:
        return SIMPLIFIED_RADICALS[ch]
    if "⼀" <= ch <= "⿟" or "豈" <= ch <= "﫿":
        n = unicodedata.normalize("NFKC", ch)
        if len(n) == 1:
            return n
    return ch


def is_bold(run):
    rpr = run.find(W + "rPr")
    if rpr is None:
        return False
    b = rpr.find(W + "b")
    return b is not None and b.get(W + "val", "true").lower() not in ("0", "false", "off")


def read_paragraph(p):
    """One <w:p> -> (text, bold ranges, comment marks [(id, 'start'|'end', offset)])."""
    text, bold, marks = [], [], []
    pos = 0

    def visit(el, bold_run):
        nonlocal pos
        for child in el:
            tag = child.tag
            if tag == W + "r":
                visit(child, is_bold(child))
            elif tag in (W + "commentRangeStart", W + "commentRangeEnd"):
                marks.append((child.get(W + "id"), "start" if tag.endswith("Start") else "end", pos))
            elif tag in (W + "t", W + "tab", W + "br", W + "cr"):
                piece = (child.text or "") if tag == W + "t" else ("\t" if tag == W + "tab" else "\n")
                if bold_run and piece.strip():
                    if bold and bold[-1][1] == pos:
                        bold[-1][1] = pos + len(piece)  # merge adjacent bold runs
                    else:
                        bold.append([pos, pos + len(piece)])
                text.append(piece)
                pos += len(piece)
            elif tag in (W + "rPr", W + "pPr", W + "del", W + "delText"):
                continue  # formatting, and deleted text (tracked changes) is not part of the text
            else:
                visit(child, bold_run)  # hyperlinks, inserted text, smart tags, fields ...

    visit(p, False)
    return "".join(text), bold, marks


def body_paragraphs(el, out):
    """Paragraphs in document order, descending into tables and content controls."""
    for child in el:
        if child.tag == W + "p":
            out.append(read_paragraph(child))
        else:
            body_paragraphs(child, out)


def read_docx(path, changed):
    z = zipfile.ZipFile(path)
    raw = []
    body_paragraphs(ET.fromstring(z.read("word/document.xml")).find(W + "body"), raw)

    paragraphs, marks_at = [], {}  # comment id -> {"start": (p, c), "end": (p, c)}
    for text, bold, marks in raw:
        norm = []
        for ch in text:
            n = normalize_char(ch)
            if n != ch:
                changed[f"{ch} (U+{ord(ch):04X}) -> {n}"] += 1
            norm.append(n)
        text = "".join(norm)
        stripped = text.strip()
        lead, end = len(text) - len(text.lstrip()), len(stripped)
        shift = lambda c: min(max(0, c - lead), end)
        if not stripped:
            # an empty paragraph can still carry a comment mark: attach it to the next paragraph's start
            for cid, kind, _ in marks:
                marks_at.setdefault(cid, {})[kind] = (len(paragraphs), 0) if kind == "start" else \
                    (max(0, len(paragraphs) - 1), len(paragraphs[-1]["text"]) if paragraphs else 0)
            continue
        i = len(paragraphs)
        for cid, kind, c in marks:
            marks_at.setdefault(cid, {})[kind] = (i, shift(c))
        bold = [[shift(s), shift(e)] for s, e in bold]
        paragraphs.append({"i": i, "text": stripped, "bold": [[s, e] for s, e in bold if e > s]})

    comments = []
    if "word/comments.xml" in z.namelist():
        for c in ET.fromstring(z.read("word/comments.xml")).iter(W + "comment"):
            cid = c.get(W + "id")
            body = "\n".join("".join(t.text or "" for t in p.iter(W + "t")) for p in c.iter(W + "p")).strip()
            body = "".join(normalize_char(ch) for ch in body)
            m = marks_at.get(cid, {})
            start, end = m.get("start"), m.get("end", m.get("start"))
            anchor = None
            if start is not None:
                anchor = {"start": {"p": start[0], "c": start[1]}, "end": {"p": end[0], "c": end[1]},
                          "text": anchor_text(paragraphs, start, end)}
            comments.append({"id": cid, "author": c.get(W + "author", ""), "date": c.get(W + "date", ""),
                             "text": body, "anchor": anchor})
    return paragraphs, comments


def anchor_text(paragraphs, start, end):
    (p0, c0), (p1, c1) = start, end
    if p0 >= len(paragraphs):
        return ""
    if p0 == p1:
        return paragraphs[p0]["text"][c0:c1]
    parts = [paragraphs[p0]["text"][c0:]]
    parts += [paragraphs[p]["text"] for p in range(p0 + 1, min(p1, len(paragraphs)))]
    if p1 < len(paragraphs):
        parts.append(paragraphs[p1]["text"][:c1])
    return "\n".join(parts)


def read_md(path, changed):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    paragraphs = []
    for block in text.split("\n\n"):
        norm = "".join(normalize_char(ch) for ch in block)
        changed.update(f"{a} (U+{ord(a):04X}) -> {b}" for a, b in zip(block, norm) if a != b)
        if norm.strip():
            paragraphs.append({"i": len(paragraphs), "text": norm.strip(), "bold": []})
    return paragraphs, []


def main():
    rows, skipped, changed_all = [], [], Counter()
    for folder in FOLDERS:
        src, out = RAW / folder, OUT / folder
        if not src.is_dir():
            sys.exit(f"Missing source folder: {src}")
        out.mkdir(parents=True, exist_ok=True)
        for stale in out.glob("*.json"):  # outputs mirror the source folders exactly
            stale.unlink()
        for path in sorted(src.iterdir()):
            if path.name.startswith("~$"):  # Word lock file of an open document
                continue
            kind = path.suffix.lower().lstrip(".")
            if kind not in ("docx", "md"):
                skipped.append(f"{folder}/{path.name}")
                continue
            changed = Counter()
            paragraphs, comments = (read_docx if kind == "docx" else read_md)(path, changed)
            changed_all.update(changed)
            rec = {"source_file": path.name, "folder": folder, "kind": kind,
                   "paragraphs": paragraphs, "comments": comments}
            (out / f"{path.stem}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
            rows.append((rec, sum(changed.values())))
            print(f"{folder}/{path.name}: {len(paragraphs)} paragraphs, "
                  f"{sum(len(p['bold']) for p in paragraphs)} bold, {len(comments)} comments")
    write_report(rows, skipped, changed_all)
    print(f"Report: {REPORT.relative_to(ROOT)}")


def mark_bold(p):
    t, out, pos = p["text"], [], 0
    for s, e in p["bold"]:
        out += [t[pos:s], "**", t[s:e], "**"]
        pos = e
    return ("".join(out) + t[pos:]).replace("\n", " ")


def write_report(rows, skipped, changed):
    L = ["# Step 1 report: raw documents -> paragraphs and comments", "",
         "| Folder | File | Paragraphs | Characters | Bold ranges | Comments | Comments with no anchored text | Look-alike characters replaced |",
         "|---|---|---|---|---|---|---|---|"]
    for rec, nc in rows:
        cm = rec["comments"]
        L.append(f"| {rec['folder']} | {rec['source_file']} | {len(rec['paragraphs'])} | "
                 f"{sum(len(p['text']) for p in rec['paragraphs'])} | {sum(len(p['bold']) for p in rec['paragraphs'])} | "
                 f"{len(cm)} | {sum(1 for c in cm if not (c['anchor'] and c['anchor']['text'].strip()))} | {nc} |")
    if skipped:
        L += ["", "Skipped (not .docx or .md): " + ", ".join(skipped)]

    L += ["", "## Look-alike characters replaced", ""]
    L += [f"- {k}: {v}x" for k, v in changed.most_common()] or ["None."]

    L += ["", "## Comment authors", ""]
    for rec, _ in rows:
        if rec["comments"]:
            a = Counter(c["author"] for c in rec["comments"])
            L.append(f"- {rec['source_file']}: " + ", ".join(f"{k} ({v})" for k, v in a.most_common()))

    L += ["", "## Comments, for checking", "",
          "The first 8 comments of each file: the text it is attached to, then the comment.", ""]
    for rec, _ in rows:
        if not rec["comments"]:
            continue
        L.append(f"### {rec['source_file']}")
        for c in rec["comments"][:8]:
            a = (c["anchor"]["text"] if c["anchor"] else "").replace("\n", " / ")
            L.append(f"- on “{a[:90]}{'…' if len(a) > 90 else ''}”: {c['text'][:200].replace(chr(10), ' / ')}")
        L.append("")

    L += ["## Bold text, for checking", "", "Up to 10 paragraphs with bold per file.", ""]
    for rec, _ in rows:
        bold = [p for p in rec["paragraphs"] if p["bold"]]
        if bold:
            L.append(f"### {rec['source_file']}")
            L += [f"- (paragraph {p['i']}) {mark_bold(p)[:200]}" for p in bold[:10]]
            L.append("")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
