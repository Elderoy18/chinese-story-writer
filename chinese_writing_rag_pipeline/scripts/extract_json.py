#!/usr/bin/env python3
"""Convert every source document into an ordered list of non-empty paragraph
texts (JSON), the one input format parse_corpus.py reads.

    raw/basic data/<name>.docx      -> extracted/basic/<name>.json
    raw/iteration data/<name>.docx  -> extracted/iteration/<name>.json

Supported: .docx (paragraphs and table cells, in document order), .txt / .md
(one paragraph per blank-line-separated block). Anything else is skipped with a
warning. Needs only the standard library -- a .docx is a zip of XML.
"""
import json
import sys
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

SOURCES = {
    "raw/basic data": "extracted/basic",
    "raw/iteration data": "extracted/iteration",
}

# Text copied out of PDFs often carries look-alike radical code points
# (e.g. ⼈ U+2F08 for 人, ⻋ U+2EC9 for 车). They render the same but are
# different characters, so they break embedding similarity and the vocab
# trigger regexes. Kangxi radicals have an NFKC mapping; the simplified-form
# radicals below do not, so they are mapped by hand.
SIMPLIFIED_RADICALS = {
    "⻋": "车", "⻝": "食", "⻓": "长", "⻔": "门", "⻢": "马", "⻜": "飞",
    "⻛": "风", "⻅": "见", "⻉": "贝", "⻚": "页", "⻥": "鱼", "⻦": "鸟",
    "⻨": "麦", "⻬": "齐", "⻘": "青", "⻄": "西", "⻆": "角",
    "⻰": "龙", "⻳": "龟", "⻩": "黄", "⻮": "齿", "⻭": "齿",
}


def normalize_chars(text):
    out = []
    for ch in text:
        if ch in SIMPLIFIED_RADICALS:
            ch = SIMPLIFIED_RADICALS[ch]
        elif "⼀" <= ch <= "⿟":  # Kangxi Radicals block
            ch = unicodedata.normalize("NFKC", ch)
        out.append(ch)
    return "".join(out)


def _paragraph_text(p):
    parts = []
    for el in p.iter():
        if el.tag == W + "t":
            parts.append(el.text or "")
        elif el.tag == W + "tab":
            parts.append("\t")
        elif el.tag in (W + "br", W + "cr"):
            parts.append("\n")
    return "".join(parts)


def _walk(el, out):
    """Emit paragraphs in document order, descending into tables and content
    controls but never into a paragraph (its text is taken whole)."""
    for child in el:
        if child.tag == W + "p":
            out.append(_paragraph_text(child))
        else:
            _walk(child, out)


def read_docx(path):
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    out = []
    _walk(root.find(W + "body"), out)
    return out


def read_text(path):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return text.split("\n\n")


READERS = {".docx": read_docx, ".txt": read_text, ".md": read_text}


def extract(path):
    paras = (normalize_chars(p).strip() for p in READERS[path.suffix.lower()](path))
    return [p for p in paras if p]


def main():
    for src_dir, out_dir in SOURCES.items():
        src, out = Path(src_dir), Path(out_dir)
        if not src.is_dir():
            sys.exit(f"Missing source folder: {src}")
        out.mkdir(parents=True, exist_ok=True)
        for stale in out.glob("*.json"):  # outputs mirror the source folder exactly
            stale.unlink()
        for path in sorted(src.iterdir()):
            if path.name.startswith("~$"):  # Word lock file of an open document
                continue
            if path.suffix.lower() not in READERS:
                print(f"  skipped {path} (unsupported type)")
                continue
            paras = extract(path)
            out_path = out / f"{path.stem}.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(paras, f, ensure_ascii=False, indent=1)
            print(f"{path}: {len(paras)} paragraphs -> {out_path}")


if __name__ == "__main__":
    main()
