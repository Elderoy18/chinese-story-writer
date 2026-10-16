#!/usr/bin/env python3
"""Step 8 -- an offline grammatical error correction (GEC) model as a finder,
on the same test stories as the baseline, scored the same way (step 7).

    data/02_corpus/corpus.json, data/03_split/split.json
        ->  data/08_find_gec/candidates.jsonl, run_info.json

    .venv/Scripts/python scripts/08_find_gec.py

Model: HillZhang/real_learner_bart_CGEC (Apache-2.0) -- Chinese BART-large
fine-tuned on ~1.3M learner sentences (HSK essays + Lang-8); NaSGEC paper,
Findings of ACL 2023. Downloaded on first use (~1.5 GB) to the Hugging Face
cache. Runs on the CPU.

The model rewrites each sentence; a character diff between the student's
sentence and the rewrite gives the edits, which already have exact positions.
Edits that only touch punctuation, spaces or letter case are dropped, as are
deletions of characters the model's vocabulary cannot represent ([UNK]): those
are artefacts of its tokenizer, not corrections.

Beam search is deterministic, so one run is enough: the same input always
gives the same output.
"""
import json
import re
import time
from difflib import SequenceMatcher
from pathlib import Path

import torch
from transformers import BartForConditionalGeneration, BertTokenizer

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
SPLIT = ROOT / "data" / "03_split" / "split.json"
OUT_DIR = ROOT / "data" / "08_find_gec"

MODEL = "HillZhang/real_learner_bart_CGEC"
NUM_BEAMS = 5
BATCH = 8
PUNCT = re.compile(r"^[\s，。！？、；：,.!?;:“”‘’\"'（）()…—\-《》]*$")


def main():
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    split = json.load(open(SPLIT, encoding="utf-8"))
    samples = {s["sample_id"]: s for s in corpus["samples"]}

    units = []  # (sample, scene, sentence)
    for t in split["test"]:
        s = samples[t["sample_id"]]
        sents = {x["sid"]: x for x in s["sentences"]}
        for sc in t["scenes"]:
            units += [(s, sc["scene"], sents[i]) for i in sc["sentence_ids"]]

    t0 = time.time()
    tok = BertTokenizer.from_pretrained(MODEL)
    model = BartForConditionalGeneration.from_pretrained(MODEL).eval()
    load_s = time.time() - t0

    t0 = time.time()
    rewrites = []
    for b in range(0, len(units), BATCH):
        texts = [u[2]["text"] for u in units[b:b + BATCH]]
        enc = tok(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
        enc.pop("token_type_ids", None)
        with torch.no_grad():
            out = model.generate(**enc, num_beams=NUM_BEAMS, max_new_tokens=max(len(t) for t in texts) + 32)
        rewrites += [d.replace(" ", "") for d in tok.batch_decode(out, skip_special_tokens=True)]
        print(f"  {min(b + BATCH, len(units))}/{len(units)} sentences")
    gen_s = time.time() - t0

    unk = {ch for s, _, x in units for ch in set(x["text"]) if tok.convert_tokens_to_ids(ch) == tok.unk_token_id}
    rows, dropped, changed = [], 0, 0
    for (s, scene, x), rw in zip(units, rewrites):
        src = x["text"]
        changed += rw != src
        for k, (op, i1, i2, j1, j2) in enumerate(SequenceMatcher(None, src, rw, autojunk=False).get_opcodes()):
            if op == "equal":
                continue
            orig, corr = src[i1:i2], rw[j1:j2]
            noise = (PUNCT.match(orig) and PUNCT.match(corr)) or orig.lower() == corr.lower() or \
                    (not corr and set(orig) <= unk | set("“”‘’"))
            if noise:
                dropped += 1
                continue
            rows.append({
                "cand_id": f"{s['sample_id']}/scene{scene}/{x['sid']}/e{k}", "sample_id": s["sample_id"],
                "story_id": s["story_id"], "scene": scene, "run": 1,
                "op": {"insert": "insert", "delete": "delete"}.get(op, "replace"),
                "start": x["start"] + i1, "end": x["start"] + i2, "original": orig, "corrected": corr,
                "before": src[max(0, i1 - 4):i1], "after": src[i2:i2 + 4],
                "type": "gec", "confidence": "high", "why": f"model rewrite: {rw}",
            })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "candidates.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT_DIR / "rewrites.jsonl", "w", encoding="utf-8") as fh:
        for (s, scene, x), rw in zip(units, rewrites):
            fh.write(json.dumps({"sample_id": s["sample_id"], "sid": x["sid"], "original": x["text"], "rewrite": rw},
                                ensure_ascii=False) + "\n")
    info = {"model": MODEL, "reasoning_effort": f"beam search, {NUM_BEAMS} beams", "prompt_version": "n/a",
            "n_runs": 1, "load_seconds": round(load_s), "generate_seconds": round(gen_s),
            "sentences": len(units), "sentences_changed": changed, "noise_edits_dropped": dropped}
    (OUT_DIR / "run_info.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(units)} sentences ({changed} rewritten) in {gen_s:.0f}s; {len(rows)} edits "
          f"({dropped} punctuation/tokenizer artefacts dropped) -> data/08_find_gec/candidates.jsonl")


if __name__ == "__main__":
    main()
