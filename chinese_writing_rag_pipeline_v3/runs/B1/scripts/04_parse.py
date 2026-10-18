#!/usr/bin/env python3
"""Step 4 -- parse every piece of Chinese with HanLP.

    data/02_corpus/parse_units.jsonl, raw/custom_words.tsv
        ->  data/04_parse/parses.jsonl     one parsed unit per line
            reports/04_parse.md

Run with the pipeline's virtual environment (HanLP is installed there):

    .venv/Scripts/python scripts/04_parse.py

Model: HanLP's small ELECTRA multi-task model for Chinese
(CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH), downloaded on first use
into this folder (.models/hanlp, via HANLP_HOME), so the pipeline does not
depend on anything outside it. Tasks used:
  tok/fine  words (fine-grained, so error spans can be word-sized)
  pos/ctb   part of speech, Penn Chinese Treebank tags -- e.g. VV verb, AS
            aspect marker (了/着/过), M measure word, PN pronoun, NR proper noun,
            DEG/DEC 的, P preposition, AD adverb
  ner/msra  names: PERSON, LOCATION, ORGANIZATION, ...
  dep       dependency parse: each word's head word and relation
            (nsubj subject, dobj object, asp aspect marker, ...)

raw/custom_words.tsv is added as a dictionary so story names stay whole, and
each of its words carries our own label (character / object / place / group)
on the token as "story_entity" -- later steps use that instead of HanLP's
name tagger, which mislabels story objects (灵芝 tagged as a person).

Every token gets its start/end position in the unit's text, and, for a
student or model-story sentence, in the whole story -- so it lines up with
every other position in the pipeline. HanLP was trained on native Chinese;
on learner sentences its output is a best guess, never a judgement of
correctness.
"""
import json
import os
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("HANLP_HOME", str(ROOT / ".models" / "hanlp"))  # before importing hanlp

import hanlp  # noqa: E402

UNITS = ROOT / "data" / "02_corpus" / "parse_units.jsonl"
WORDS = ROOT / "raw" / "custom_words.tsv"
OUT = ROOT / "data" / "04_parse" / "parses.jsonl"
REPORT = ROOT / "reports" / "04_parse.md"

MODEL = "CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH"
TASKS = ["tok/fine", "pos/ctb", "ner/msra", "dep"]
BATCH = 64


def load_words():
    """{word: type} from the tab-separated word list."""
    out = {}
    for line in WORDS.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            word, kind = line.split("	")
            out[word.strip()] = kind.strip()
    return out


def token_offsets(text, tokens):
    """[start, end] of each token in text, or None if the tokens do not
    reproduce the text in order (then positions cannot be trusted)."""
    out, pos = [], 0
    for t in tokens:
        i = text.find(t, pos)
        if i < 0 or text[pos:i].strip():
            return None
        out.append([i, i + len(t)])
        pos = i + len(t)
    return out if not text[pos:].strip() else None


def main():
    units = [json.loads(l) for l in open(UNITS, encoding="utf-8")]
    words = load_words()

    t0 = time.time()
    nlp = hanlp.load(getattr(hanlp.pretrained.mtl, MODEL))
    nlp["tok/fine"].dict_combine = set(words)
    load_s = time.time() - t0

    t0 = time.time()
    parsed = []
    for b in range(0, len(units), BATCH):
        batch = units[b:b + BATCH]
        doc = nlp([u["text"] for u in batch], tasks=TASKS)
        for k, u in enumerate(batch):
            toks = doc["tok/fine"][k]
            offs = token_offsets(u["text"], toks)
            base = u["source"].get("start", 0) if u["kind"] != "teacher_fix" else None
            heads = doc["dep"][k]
            parsed.append({
                "unit_id": u["unit_id"], "kind": u["kind"], "text": u["text"], "source": u["source"],
                "tokens": [{
                    "i": i, "text": t, "pos": doc["pos/ctb"][k][i],
                    "start": offs[i][0] if offs else None, "end": offs[i][1] if offs else None,
                    "story_start": offs[i][0] + base if offs and base is not None else None,
                    "head": heads[i][0] - 1, "rel": heads[i][1],   # head -1 = root
                    "story_entity": words.get(t),                  # our label, or None
                } for i, t in enumerate(toks)],
                "entities": [{"text": e[0], "type": e[1], "tok_start": e[2], "tok_end": e[3]} for e in doc["ner/msra"][k]],
                "offsets_ok": offs is not None,
            })
        print(f"  {min(b + BATCH, len(units))}/{len(units)} units")
    parse_s = time.time() - t0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        for p in parsed:
            fh.write(json.dumps(p, ensure_ascii=False) + "\n")
    write_report(parsed, words, load_s, parse_s)
    print(f"{len(parsed)} units -> {OUT.relative_to(ROOT)}; report {REPORT.relative_to(ROOT)}")


def write_report(parsed, words, load_s, parse_s):
    kinds = Counter(p["kind"] for p in parsed)
    toks = [t for p in parsed for t in p["tokens"]]
    bad = [p for p in parsed if not p["offsets_ok"]]
    pos = Counter(t["pos"] for p in parsed if p["kind"] == "student_sentence" for t in p["tokens"])
    aspect = Counter(t["text"] for p in parsed if p["kind"] == "student_sentence" for t in p["tokens"] if t["pos"] == "AS")
    persons = Counter(e["text"] for p in parsed if p["kind"] != "teacher_fix" for e in p["entities"] if e["type"] == "PERSON")
    split_words = Counter(w for p in parsed for w in words
                          if w in p["text"] and w not in {t["text"] for t in p["tokens"]})

    L = ["# Step 4 report: HanLP parse", "",
         f"- model: {MODEL}; tasks: {', '.join(TASKS)}; custom dictionary: {len(words)} words",
         f"- load {load_s:.0f}s, parse {parse_s:.0f}s",
         f"- units: " + ", ".join(f"{k} {v}" for k, v in kinds.items()) + f"; tokens: {len(toks)}",
         f"- units whose tokens do not reproduce the text (positions unusable): {len(bad)}", ""]
    L += [f"  - {p['unit_id']}: {p['text']} -> {' / '.join(t['text'] for t in p['tokens'])}" for p in bad[:20]]

    L += ["", "## Dictionary words HanLP still split", "",
          *([f"- {w}: {n} units" for w, n in split_words.most_common()] or ["None -- every dictionary word stayed whole."])]

    L += ["", "## Student sentences: parts of speech (top 20)", "",
          ", ".join(f"{k} {v}" for k, v in pos.most_common(20)), "",
          "Aspect markers (AS) found in student sentences: " + ", ".join(f"{k} {v}" for k, v in aspect.most_common()), "",
          "## Names tagged PERSON in student and model sentences (top 25)", "",
          ", ".join(f"{k} {v}" for k, v in persons.most_common(25)), "",
          "Anything here that is not a character (or a character missing) shows where the name tagger needs help.", "",
          "## Story words labelled from our own list (`story_entity`)", "",
          ", ".join(f"{k} {v}" for k, v in Counter((t["text"], t["story_entity"]) for p in parsed for t in p["tokens"]
                                                      if t["story_entity"]).most_common(25)), "",
          "## Example parses, for checking", "",
          "Each word as word/POS, then its grammatical link (relation → head word).", ""]
    picks = [p for p in parsed if p["kind"] == "student_sentence"][:6] + \
            [p for p in parsed if p["kind"] == "model_sentence"][:2] + \
            [p for p in parsed if p["kind"] == "teacher_fix"][:4]
    for p in picks:
        tk = p["tokens"]
        L.append(f"**{p['unit_id']}** ({p['kind']}): {p['text']}")
        L.append("- words: " + "  ".join(f"{t['text']}/{t['pos']}" for t in tk))
        L.append("- links: " + "  ".join(f"{t['text']} {t['rel']}→{tk[t['head']]['text'] if t['head'] >= 0 else 'ROOT'}" for t in tk))
        if p["entities"]:
            L.append("- names: " + ", ".join(f"{e['text']} ({e['type']})" for e in p["entities"]))
        L.append("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
