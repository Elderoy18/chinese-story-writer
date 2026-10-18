#!/usr/bin/env python3
"""Step 11 -- the teacher's error categories, and every aligned edit sorted
into one of them.

    data/05_align/edits_train.jsonl, edits_test.jsonl, raw/basic_data/Coherence reference temporality rules.md
        ->  data/11_categories/taxonomy.json                the category list (draft)
            data/11_categories/edits_<split>.jsonl          edits with their category
            reports/11_categories.md

    python scripts/11_categorize.py

1. Category list (one LLM call, high effort), built from the TRAIN edits only:
   all of her distinct notes with how often she wrote them, a sample of her
   corrections without a note, and her coherence rubric. Categories use her
   terminology, sit in her dimensions (grammar, word choice, coherence:
   reference / temporality / connectors, content), and say how a checker
   could find them: a fixed word pattern, the parse (HanLP), or only by
   judging meaning.
2. Sorting: every edit (train, and test for per-category scoring -- the list
   itself never sees test) goes to one category, optionally a second when one
   edit fixes two rules. The LLM sees the clause, the edit, her note and the
   edit's HanLP signature (e.g. "insert 了 | after 给/VV | before 神农/NR").
3. The list goes to the teacher together with the rule cards (step 12, one
   review sheet for both); once she has answered, the list is updated and the
   edits re-sorted.
"""
import importlib.util
import json
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from llm import api_key, cached_json_call, prompt_version

ROOT = Path(__file__).resolve().parent.parent
EDITS = ROOT / "data" / "05_align"
RUBRIC = ROOT / "raw" / "basic_data" / "Coherence reference temporality rules.md"
CORPUS = ROOT / "data" / "02_corpus" / "corpus.json"
OUT_DIR = ROOT / "data" / "11_categories"
CACHE = OUT_DIR / "cache"
REPORT = ROOT / "reports" / "11_categories.md"

MODEL = "gpt-5.6-terra"
BATCH = 25
WORKERS = 8
SECTIONS = ["grammar", "word_choice", "coherence_reference", "coherence_temporality", "coherence_connectors", "content", "other"]

spec = importlib.util.spec_from_file_location("score", ROOT / "scripts" / "07_score.py")
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)

# ---------------------------------------------------------------------------
# 1. The category list
# ---------------------------------------------------------------------------
TAXONOMY_SYSTEM = """You are building the list of error categories for a Chinese teacher's corrections of beginner learners' narrative writing (retellings of traditional stories). The list will be used to sort every correction she made, to write one explanation card per category, and to decide which errors a program can detect.

You receive: her coherence rubric; every distinct note she wrote on a correction, with how often; and a sample of her corrections that carry no note (learner text -> her correction).

Build categories that SHE would recognise:
- Use her own terminology and shorthand where she has one (了completed, 在+Place, 看look vs. 看到see, 害得 + harmful result, redundant).
- One category = one rule a learner can learn from one explanation. Split when the explanation differs (了 for a completed action vs. no 了 after mental-state verbs / routines / speaking verbs; first mention vs. ambiguous pronoun). Merge near-duplicates.
- Every note she wrote more than once must fit a category. Corrections that only change a word to a better word belong in word-choice categories (group by kind: near-synonyms, collocation, word class, etc., not one category per word).
- Put each category in one section: grammar | word_choice | coherence_reference | coherence_temporality | coherence_connectors | content | other. Coherence categories follow her rubric (reference: first mention / pronoun / zero form / repeat the name; temporality: 了 / 着 / 在 / zero particle / series of actions; connectors). content = wrong information about the story.
- Aim for 30 to 60 categories.

For each category give:
- id: short snake_case English
- name: a short name in her terms
- section
- definition: one or two sentences, in her words where possible
- her_notes: up to 5 of her notes that belong here, copied exactly ([] if none)
- detectable_by: pattern (a fixed word or word sequence finds it, e.g. 古代的时候) | parser (needs parts of speech or sentence structure, e.g. 了 right after a mental-state verb) | judgement (only by understanding the meaning, e.g. choosing between near-synonyms)"""

TAXONOMY_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["categories"],
    "properties": {"categories": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["id", "name", "section", "definition", "her_notes", "detectable_by"],
        "properties": {
            "id": {"type": "string"}, "name": {"type": "string"},
            "section": {"type": "string", "enum": SECTIONS},
            "definition": {"type": "string"},
            "her_notes": {"type": "array", "items": {"type": "string"}},
            "detectable_by": {"type": "string", "enum": ["pattern", "parser", "judgement"]},
        }}}},
}


def signature(e):
    """The edit in HanLP terms: 'insert 了 | after 给/VV | before 神农/NR'."""
    h = e.get("hanlp") or {}
    w = lambda t: f"{t['text']}/{t['pos']}" if t else "-"
    core = {"insert": f"insert {e['corrected']}", "delete": f"delete {e['original']}",
            "comment": f"comment on {e['original']}"}.get(e["op"], f"replace {e['original']} -> {e['corrected']}")
    words = " ".join(w(t) for t in h.get("words", []))
    return f"{core} | words {words or '-'} | after {w(h.get('left'))} | before {w(h.get('right'))}"


def build_taxonomy(train):
    notes = Counter(e["teacher_note"].strip() for e in train if e["teacher_note"].strip())
    unnoted = [e for e in train if not e["teacher_note"].strip() and e["op"] != "comment"]
    sample = unnoted[::max(1, len(unnoted) // 150)][:150]
    user = "\n".join([
        "HER COHERENCE RUBRIC:", RUBRIC.read_text(encoding="utf-8"), "",
        f"HER NOTES ({len(notes)} distinct; count, note):",
        *[f"{c} | {n}" for n, c in notes.most_common()], "",
        f"A SAMPLE OF HER CORRECTIONS WITHOUT A NOTE ({len(sample)} of {len(unnoted)}):",
        *[f"- {e['original'] or '∅'} -> {e['corrected'] or '∅'}   ({signature(e)})" for e in sample],
    ])
    rec, _ = cached_json_call(CACHE, MODEL, "high", TAXONOMY_SYSTEM, TAXONOMY_SCHEMA, "taxonomy", user)
    cats = rec["output"]["categories"]
    if not any(c["id"] == "other" for c in cats):
        cats.append({"id": "other", "name": "other", "section": "other", "definition": "Fits no other category.",
                     "her_notes": [], "detectable_by": "judgement"})
    return cats


# ---------------------------------------------------------------------------
# 2. Sorting the edits
# ---------------------------------------------------------------------------
ASSIGN_SYSTEM = """You sort a Chinese teacher's corrections of learner writing into her list of error categories.

For each correction you see: the learner's clause with the edit marked ([+X] add X, [-X] delete X, [A→B] replace A with B, ⟦X⟧ a comment about X), her note if she wrote one, and the edit's grammatical signature (parts of speech: VV verb, NN noun, NR name, PN pronoun, AS aspect marker, AD adverb, P preposition, M measure word, DEG/DEC 的).

Give each correction:
- category: the id of the category it belongs to. Her note, when present, is the strongest evidence of what she was correcting.
- second: the id of a second category ONLY if the same edit clearly fixes two different rules (e.g. adds 了 AND moves a frequency phrase); otherwise "".
- confidence: high, or low if two categories fit about equally.
Use "other" only if no category fits."""

ASSIGN_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["items"],
    "properties": {"items": {"type": "array", "items": {
        "type": "object", "additionalProperties": False, "required": ["edit_id", "category", "second", "confidence"],
        "properties": {"edit_id": {"type": "string"}, "category": {"type": "string"}, "second": {"type": "string"},
                       "confidence": {"type": "string", "enum": ["high", "low"]}}}}},
}


def assign(edits, cats, texts):
    catalog = "CATEGORIES:\n" + "\n".join(f"- {c['id']} ({c['section']}): {c['name']} -- {c['definition']}" for c in cats)
    batches = [edits[i:i + BATCH] for i in range(0, len(edits), BATCH)]

    def run(batch):
        lines = [catalog, "", "CORRECTIONS:"]
        for e in batch:
            shown = score.show(texts[e["sample_id"]], e) if e["start"] is not None else f"{e['original']} → {e['corrected']}"
            lines.append(f"[{e['edit_id']}] {shown}" + (f"  || her note: {e['teacher_note']}" if e["teacher_note"] else "")
                         + f"  || {signature(e)}")
        rec, _ = cached_json_call(CACHE, MODEL, "medium", ASSIGN_SYSTEM, ASSIGN_SCHEMA, "assignment", "\n".join(lines))
        return rec

    with ThreadPoolExecutor(WORKERS) as pool:
        recs = list(pool.map(run, batches))
    ids = {c["id"] for c in cats}
    got = {it["edit_id"]: it for rec in recs for it in rec["output"]["items"]}
    out = []
    for e in edits:
        it = got.get(e["edit_id"], {"category": "other", "second": "", "confidence": "low"})
        cat = it["category"] if it["category"] in ids else "other"
        sec = it["second"] if it["second"] in ids and it["second"] != cat else ""
        out.append({**e, "category": cat, "second_category": sec, "category_confidence": it["confidence"],
                    "category_unknown_id": it["category"] if it["category"] not in ids else "",
                    "signature": signature(e)})
    return out


# ---------------------------------------------------------------------------
def main():
    load = lambda split: [e for e in map(json.loads, open(EDITS / f"edits_{split}.jsonl", encoding="utf-8"))
                          if e["op"] != "unplaceable"]
    train, test = load("train"), load("test")
    texts = {s["sample_id"]: s["text"] for s in json.load(open(CORPUS, encoding="utf-8"))["samples"]}
    api_key()

    cats = build_taxonomy(train)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "taxonomy.json").write_text(json.dumps(
        {"prompt_version": prompt_version(TAXONOMY_SYSTEM, TAXONOMY_SCHEMA), "categories": cats},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(cats)} categories")

    done = {}
    for split, edits in (("train", train), ("test", test)):
        done[split] = assign(edits, cats, texts)
        with open(OUT_DIR / f"edits_{split}.jsonl", "w", encoding="utf-8") as fh:
            for e in done[split]:
                fh.write(json.dumps(e, ensure_ascii=False) + "\n")
        print(f"{split}: {len(edits)} edits sorted")

    write_report(cats, done, texts)
    print(f"Report: {REPORT.relative_to(ROOT)}")


def write_report(cats, done, texts):
    tr, te = Counter(e["category"] for e in done["train"]), Counter(e["category"] for e in done["test"])
    L = ["# Step 11 report: the teacher's error categories", "",
         f"- {len(cats)} categories, built from the train edits only; train edits {len(done['train'])}, test edits {len(done['test'])}",
         f"- sorted with low confidence: train {sum(e['category_confidence'] == 'low' for e in done['train'])}, "
         f"test {sum(e['category_confidence'] == 'low' for e in done['test'])}; with a second category: "
         f"train {sum(bool(e['second_category']) for e in done['train'])}",
         f"- unknown ids returned (sorted to other): {sum(bool(e['category_unknown_id']) for s in done.values() for e in s)}", ""]
    for sec in SECTIONS:
        cs = [c for c in cats if c["section"] == sec]
        if not cs:
            continue
        L += [f"## {sec} ({sum(tr[c['id']] for c in cs)} train / {sum(te[c['id']] for c in cs)} test edits)", "",
              "| Category | Found by | Train | Test | Definition |", "|---|---|---|---|---|"]
        for c in sorted(cs, key=lambda c: -tr[c["id"]]):
            L.append(f"| **{c['name']}** (`{c['id']}`) | {c['detectable_by']} | {tr[c['id']]} | {te[c['id']]} | {c['definition']} |")
        L.append("")
    det = Counter()
    for e in done["train"]:
        det[next(c["detectable_by"] for c in cats if c["id"] == e["category"])] += 1
    L += ["## How the train edits could be found", "",
          *[f"- {k}: {v} edits ({100 * v // len(done['train'])}%)" for k, v in det.most_common()], "",
          "## Examples per category (train, first 4)", ""]
    for c in sorted(cats, key=lambda c: -tr[c["id"]]):
        ex = [e for e in done["train"] if e["category"] == c["id"]][:4]
        if ex:
            L.append(f"**{c['name']}** (`{c['id']}`)")
            L += [f"- {score.show(texts[e['sample_id']], e) if e['start'] is not None else e['original']}"
                  + (f" — {e['teacher_note']}" if e["teacher_note"] else "") for e in ex] + [""]
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
