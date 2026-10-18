#!/usr/bin/env python3
"""Step 1 -- convert every basic-data Word document into a list of paragraphs.

    raw/basic_data/<name>.docx  ->  data/01_extracted/<name>.json
                                    reports/01_extract.md

Each paragraph keeps its text and the character ranges the teacher put in
bold (the Pear Story file marks inserted characters this way, e.g. 摆**了**).

Character positions are preserved end to end: the only change made to the text
is replacing look-alike radical code points with the ordinary character (one
character for one character), and trimming whitespace at the ends of a
paragraph (bold ranges are shifted to match). So a position computed later --
by step 2, or by HanLP on a sentence -- points at the same character as in the
Word file.

Standard library only: a .docx is a zip of XML.
"""
import json
import sys
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "raw" / "basic_data"
OUT_DIR = ROOT / "data" / "01_extracted"
REPORT = ROOT / "reports" / "01_extract.md"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# Text copied out of PDFs often carries look-alike radical code points
# (e.g. ⼈ U+2F08 for 人, ⻋ U+2EC9 for 车). They look the same but are different
# characters, so HanLP, embeddings and regexes all treat them as unknown.
# Kangxi radicals and CJK compatibility ideographs have a one-character NFKC
# mapping; the simplified-form radicals below do not, so they are mapped by hand.
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
    if "⼀" <= ch <= "⿟" or "豈" <= ch <= "﫿":  # Kangxi radicals, CJK compatibility ideographs
        n = unicodedata.normalize("NFKC", ch)
        if len(n) == 1:
            return n
    return ch


def run_is_bold(run):
    rpr = run.find(W + "rPr")
    if rpr is None:
        return False
    b = rpr.find(W + "b")
    return b is not None and b.get(W + "val", "true").lower() not in ("0", "false", "off")


def read_paragraph(p):
    """(text, [[start, end], ...] bold ranges) for one <w:p>."""
    text, bold = [], []
    for run in p.iter(W + "r"):
        is_bold = run_is_bold(run)
        for el in run:
            if el.tag == W + "t":
                piece = el.text or ""
            elif el.tag == W + "tab":
                piece = "\t"
            elif el.tag in (W + "br", W + "cr"):
                piece = "\n"
            else:
                continue
            start = sum(len(t) for t in text)
            text.append(piece)
            if is_bold and piece.strip():
                if bold and bold[-1][1] == start:
                    bold[-1][1] = start + len(piece)  # merge adjacent bold runs
                else:
                    bold.append([start, start + len(piece)])
    return "".join(text), bold


def walk(el, out):
    """Paragraphs in document order, descending into tables and content controls."""
    for child in el:
        if child.tag == W + "p":
            out.append(read_paragraph(child))
        else:
            walk(child, out)


def extract(path, changed):
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    raw = []
    walk(root.find(W + "body"), raw)

    paragraphs = []
    for text, bold in raw:
        norm = []
        for ch in text:
            n = normalize_char(ch)
            if n != ch:
                changed[f"{ch} (U+{ord(ch):04X}) -> {n}"] += 1
            norm.append(n)
        text = "".join(norm)
        lead = len(text) - len(text.lstrip())
        stripped = text.strip()
        if not stripped:
            continue
        end = len(stripped)
        bold = [[max(0, s - lead), min(end, e - lead)] for s, e in bold]
        bold = [[s, e] for s, e in bold if e > s]
        paragraphs.append({"i": len(paragraphs), "text": stripped, "bold": bold})
    return paragraphs


def main():
    if not SRC_DIR.is_dir():
        sys.exit(f"Missing source folder: {SRC_DIR}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for stale in OUT_DIR.glob("*.json"):  # outputs mirror the source folder exactly
        stale.unlink()

    rows, skipped, all_changed = [], [], Counter()
    for path in sorted(SRC_DIR.iterdir()):
        if path.name.startswith("~$"):  # Word lock file of an open document
            continue
        if path.suffix.lower() != ".docx":
            skipped.append(path.name)
            continue
        changed = Counter()
        paragraphs = extract(path, changed)
        all_changed.update(changed)
        out_path = OUT_DIR / f"{path.stem}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"source_file": path.name, "paragraphs": paragraphs}, f, ensure_ascii=False, indent=1)
        n_bold = sum(len(p["bold"]) for p in paragraphs)
        rows.append((path.name, len(paragraphs), n_bold, sum(changed.values()), paragraphs))
        print(f"{path.name}: {len(paragraphs)} paragraphs, {n_bold} bold ranges -> {out_path.relative_to(ROOT)}")

    write_report(rows, skipped, all_changed)
    print(f"Report: {REPORT.relative_to(ROOT)}")


def write_report(rows, skipped, changed):
    L = [
        "# Step 1 report: Word files -> paragraphs",
        "",
        "Each Word file in `raw/basic_data/` becomes `data/01_extracted/<name>.json`: its non-empty",
        "paragraphs in document order, each with the character ranges that are bold.",
        "",
        "| File | Paragraphs | Bold ranges | Characters normalized |",
        "|---|---|---|---|",
    ]
    for name, n, nb, nc, _ in rows:
        L.append(f"| {name} | {n} | {nb} | {nc} |")
    if skipped:
        L += ["", "Skipped (not .docx): " + ", ".join(skipped)]

    L += ["", "## Look-alike characters replaced", ""]
    L += [f"- {k}: {v}x" for k, v in changed.most_common()] or ["None."]

    L += ["", "## Bold text, for checking", "",
          "Every bold range found, shown as **bold** inside its paragraph (first 40 per file).", ""]
    for name, _, nb, _, paragraphs in rows:
        if not nb:
            continue
        L.append(f"### {name}")
        shown = 0
        for p in paragraphs:
            if not p["bold"] or shown >= 40:
                continue
            t, out, pos = p["text"], [], 0
            for s, e in p["bold"]:
                out += [t[pos:s], "**", t[s:e], "**"]
                pos = e
            out.append(t[pos:])
            L.append(f"- (paragraph {p['i']}) " + "".join(out).replace("\n", " "))
            shown += 1
        L.append("")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
