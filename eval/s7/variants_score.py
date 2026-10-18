#!/usr/bin/env python3
"""Retrieval / generation / end-to-end consistency and accuracy at her corrections, from the
variant runs of eval/s7/variants.mjs.

    python eval/s7/variants_score.py S7-4 [--name S7-4]   -> eval/reports/S7_variants_<name>.md

For every target error (one of her corrections; the variant keeps it word for word and has
her other corrections in the scene applied) four outputs are compared, all at the target:
    original run 1 / original run 2  -- same input, same retrieval (reruns: model randomness)
    variant, fixed retrieval         -- different input, the ORIGINAL scene's chunks (generation)
    variant, own retrieval           -- different input, its own chunks (end-to-end)

Measures
  a. retrieval   Jaccard of retrieved chunk ids, original vs variant (own retrieval);
                 card reach for the target's rule card, original vs variant.
  b. generation  original run 1 vs variant-fixed: detection agreement (both flag the target or
                 both don't), lexical (identical Chinese corrected text), information (judge: same
                 error, equivalent fix).
  c. end-to-end  original run 1 vs variant-own, the same measures.
  reference      original run 1 vs run 2 (nothing changed): the noise floor for b and c.
  accuracy       per output: target caught; lexical accuracy (corrected text is hers);
                 information accuracy (judge: right fix, clean corrected text).
"""
import argparse
import json
import statistics
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "eval" / "v1_vs_v2"))
import evaluate as E  # noqa: E402
import score as S  # noqa: E402

RUNS = REPO / "eval" / "runs"


def items_at_target(md, scene_text, target):
    """The feedback items whose student words overlap the target span (scene positions)."""
    out = []
    for it in S.parse_v1_scene(md, scene_text)["items"]:
        span = S.locate(it["before"], scene_text, 0)
        if span and span[0] < max(target["end"], target["start"] + 1) and target["start"] < max(span[1], span[0] + 1):
            out.append({**it, "span": span})
    return out


def judge_target(scene_text, edits, it):
    """The item-level judge on one item at her correction: right fix and clean corrected text?"""
    v = S.judge_scene("", scene_text, edits, [it]).get(1) or {}
    return v.get("fix_right") == "yes" and v.get("after_fully_correct") != "no"


def lexical_hit(it, scene_text, edits):
    hers = E.her_versions(scene_text, it["span"], [{**e} for e in edits])
    mine = E.clean_after(it["after"])
    return bool(hers) and mine is not None and any(mine == h or (h and h in mine and len(mine) - len(h) <= 2) for h in hers)


def compare(a, b, scene_text, edits):
    """Two outputs at the target: (detection agree, lexical same, information same | None if not both flagged)."""
    if not a or not b:
        return (bool(a) == bool(b)), None, None
    lex = E.clean_after(a[0]["after"]) == E.clean_after(b[0]["after"])
    info = E.info_judge(scene_text, edits, [a[0], b[0]])
    return True, lex, bool(info.get("same_error") and info.get("equivalent_fix")) if info.get("same_error") is not None else None


def pct(a, b):
    return f"{a}/{b} ({100 * a / b:.0f}%)" if b else "–"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage")
    ap.add_argument("--name")
    args = ap.parse_args()
    name = args.name or args.stage
    vdir = RUNS / args.stage / "variants"
    ids = json.load(open(vdir / "_index.json", encoding="utf-8"))["ids"]
    V = [json.load(open(vdir / f"{i}.json", encoding="utf-8")) for i in ids if (vdir / f"{i}.json").exists()]
    V = [v for v in V if v.get("fixed") and v.get("own")]
    test_set = json.load(open(REPO / "eval" / "test_set_h20.json", encoding="utf-8"))
    key = E.load_key(test_set)
    snapshot = json.load(open(RUNS / args.stage / "stage.json", encoding="utf-8"))["snapshot"]
    cards = {json.loads(l)["chunk_id"] for l in open(REPO / "eval" / "snapshots" / snapshot / "chunks.jsonl", encoding="utf-8")
             if '"chunk_type": "rule_card"' in l}
    offs = {s["sample_id"]: E.scene_offsets(s["raw_text"], s["scenes"]) for s in test_set["samples"]}

    def one(v):
        lo = offs[v["sample_id"]][v["scene"] - 1][0]
        orig_edits = [{**e, "start": e["start"] - lo, "end": e["end"] - lo} for e in key[v["sample_id"]]
                      if e["start"] is not None and e["teacher_line"] == v["her_line"]]
        var_edits = [{**e, "teacher_line": e["her_line"], "teacher_piece": e["her_piece"], "teacher_note": e["her_note"]}
                     for e in v["target_edits_variant"]]
        runs = [json.load(open(RUNS / r / f"{v['sample_id'].replace('#', '_')}.json", encoding="utf-8"))["scenes"][v["scene"] - 1]
                for r in (args.stage, f"{args.stage}-r2")]
        o1, o2 = (items_at_target(r["feedback"], v["original_scene"], v["target_original"]) for r in runs)
        fx = items_at_target(v["fixed"]["text"], v["variant_scene"], v["target_variant"])
        ow = items_at_target(v["own"]["text"], v["variant_scene"], v["target_variant"])
        out = {"rerun": compare(o1, o2, v["original_scene"], orig_edits),
               "generation": compare(o1, fx, v["original_scene"], orig_edits),
               "end_to_end": compare(o1, ow, v["original_scene"], orig_edits)}
        A, B = set(v["original_retrieved"]), set(v["own"]["retrieved"])
        out["jaccard"] = len(A & B) / len(A | B)
        want = [f"rule_card:{r}" for r in v["rules"] if f"rule_card:{r}" in cards]
        out["card"] = (bool(want), any(w in A for w in want), any(w in B for w in want))
        acc = {}
        for label, its, text, edits in (("original", o1, v["original_scene"], orig_edits), ("fixed", fx, v["variant_scene"], var_edits),
                                        ("own", ow, v["variant_scene"], var_edits)):
            if not its:
                acc[label] = (False, False, False)
                continue
            acc[label] = (True, lexical_hit(its[0], text, edits), judge_target(text, edits, its[0]))
        out["acc"] = acc
        return out

    E.load_refused()
    with ThreadPoolExecutor(8) as pool:
        res = list(pool.map(one, V))
    E.save_refused()

    def block(kind):
        rows = [r[kind] for r in res]
        both = [x for x in rows if x[1] is not None]
        return (pct(sum(x[0] for x in rows), len(rows)), pct(sum(x[1] for x in both), len(both)),
                pct(sum(bool(x[2]) for x in both if x[2] is not None), sum(x[2] is not None for x in both)))

    jac = [r["jaccard"] for r in res]
    with_card = [r["card"] for r in res if r["card"][0]]
    L = [f"# Variant consistency: {name}", "",
         f"{len(res)} target errors (her corrections on the 20 test stories that share a scene with at least one other "
         f"of her corrections). Each variant = the scene with her OTHER corrections applied; the target error is kept "
         f"word for word. Stage `{args.stage}`, snapshot `{snapshot}`; one run per variant and mode.", "",
         "## a. Retrieval (original scene vs variant, each doing its own retrieval)", "",
         f"- Jaccard of retrieved chunk ids: mean {statistics.mean(jac):.2f}, median {statistics.median(jac):.2f}, "
         f"min {min(jac):.2f}; identical sets {pct(sum(j == 1 for j in jac), len(jac))}",
         f"- Card reach for the target's rule card: original {pct(sum(c[1] for c in with_card), len(with_card))}, "
         f"variant {pct(sum(c[2] for c in with_card), len(with_card))}; same outcome in both "
         f"{pct(sum(c[1] == c[2] for c in with_card), len(with_card))}",
         "", "## b, c. Consistency at the target error", "",
         "| Compared with original run 1 | Same decision (flag / no flag) | Lexical (both flagged: identical text) | Information (both flagged: same error, equivalent fix) |",
         "|---|---|---|---|"]
    for kind, label in (("rerun", "original run 2 -- nothing changed (noise floor)"),
                        ("generation", "**b. variant, fixed retrieval** -- generation only"),
                        ("end_to_end", "**c. variant, own retrieval** -- end-to-end")):
        d, lx, inf = block(kind)
        L.append(f"| {label} | {d} | {lx} | {inf} |")
    L += ["", "## Accuracy at the target error", "",
          "| Output | Target caught | Lexical accuracy (her fix) | Information accuracy (right fix, clean text) |", "|---|---|---|---|"]
    for label, k in (("original scene, run 1", "original"), ("variant, fixed retrieval (generation)", "fixed"),
                     ("variant, own retrieval (end-to-end)", "own")):
        a = [r["acc"][k] for r in res]
        L.append(f"| {label} | {pct(sum(x[0] for x in a), len(a))} | {pct(sum(x[1] for x in a), len(a))} | {pct(sum(x[2] for x in a), len(a))} |")
    L += ["", "Reading: if b is close to the noise floor, the model is consistent when only the surrounding text changes; "
          "if c is clearly below b, retrieval changes with the input are what make the answer change."]
    out = REPO / "eval" / "reports" / f"S7_variants_{name}.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
