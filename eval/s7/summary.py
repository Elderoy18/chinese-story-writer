#!/usr/bin/env python3
"""One statistical summary of every stage scored on the 20-story test set (no API calls).

    python eval/s7/summary.py   -> eval/reports/S7_summary.md

Reads eval/s7/out/<stage>.json (written by evaluate.py) and the variant reports. Each
accuracy figure is per run, summarised as mean ± standard deviation (min-max) over the runs;
where a stage has two sets of 3 runs (S7-4), both sets are pooled for accuracy and consistency
is given per set (it needs a fixed number of runs). v2 is compared on the 6-story set only
(eval/reports/v1_vs_v2.md); evaluate.py can score it on the 20 stories (runs v2-S0, v2-r2,
v2-r3, after eval/v1_vs_v2/v2_repeat.py --test-set eval/test_set_h20.json) if needed.
"""
import json
import re
import statistics
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
OUT = REPO / "eval" / "s7" / "out"
REPORTS = REPO / "eval" / "reports"

STAGES = [  # (label, [out files], verdict)
    ("S0 (floor: no teacher input)", ["S0-h20"], "floor"),
    ("S6 (previous system)", ["S6-h20"], "baseline"),
    ("S7-0 new data", ["S7-0"], "neutral, kept"),
    ("S7-0b + revised critique cards", ["S7-0b"], "not accepted"),
    ("S7-1 + reasoning effort medium", ["S7-1"], "accepted"),
    ("S7-2 + rule citations, standard fixes", ["S7-2"], "accepted"),
    ("S7-3 + end-of-story scene check", ["S7-3"], "accepted"),
    ("S7-4 + rule-card triggers", ["S7-4", "S7-4-set2"], "accepted"),
    ("S7-5 + cards via corrected sentences (added)", ["S7-5"], "rejected"),
    ("S7-6 cards via corrected sentences (replacing)", ["S7-6"], "pending tie-break"),
]


def load(name):
    p = OUT / f"{name}.json"
    return json.load(open(p, encoding="utf-8")) if p.exists() else None


def stat(vals, pct=False, digits=2):
    vals = [v for v in vals if v is not None]
    if not vals:
        return "–"
    f = (lambda v: f"{100 * v:.0f}%") if pct else (lambda v: f"{v:.{digits}f}")
    sd = statistics.stdev(vals) if len(vals) > 1 else 0
    sd_s = f"{100 * sd:.0f}" if pct else f"{sd:.{digits}f}"
    return f"{f(statistics.mean(vals))} ± {sd_s} ({f(min(vals))}–{f(max(vals))})"


def per_run(ds, fn):
    return [fn(m) for d in ds for m in d["metrics"].values()]


def consistency(d):
    full = [p for p in d["places"] if p["n_runs"] == len(d["runs"])]
    info = sum(bool(p.get("info", {}).get("same_error") and p.get("info", {}).get("equivalent_fix")) for p in full)
    same = sum(bool(p.get("info", {}).get("same_error")) for p in full)
    lex = sum(p["lexical"] for p in full)
    n = len(full)
    return (f"{100 * info / n:.0f}%", f"{100 * same / n:.0f}%", f"{100 * lex / n:.0f}%",
            f"{100 * n / len(d['places']):.0f}%") if n else ("–",) * 4


def reach(d):
    if d["runs"][0].startswith("v2-"):
        return "n/a (no rule cards)"
    rows = list(d["attribution"].values())[0]
    want = [r for r in rows if r["cards_wanted"]]
    return f"{100 * sum(r['card_in_prompt'] for r in want) / len(want):.0f}%" if want else "–"


def variant_row(name):
    p = REPORTS / f"S7_variants_{name}.md"
    if not p.exists():
        return None
    t = p.read_text(encoding="utf-8")
    jac = re.search(r"Jaccard of retrieved chunk ids: mean ([\d.]+)", t)
    rows = re.findall(r"^\| (?:original run 2|\*\*b\.|\*\*c\.).*?\| (.*?) \| (.*?) \| (.*?) \|$", t, re.M)
    pick = lambda s: re.search(r"\((\d+%)\)", s).group(1) if re.search(r"\((\d+%)\)", s) else "–"
    return jac.group(1) if jac else "–", [(pick(a), pick(b), pick(c)) for a, b, c in rows]


def main():
    L = ["# S7 statistical summary (20 test stories, 60 scenes)", "",
         "Each cell: mean ± standard deviation (lowest–highest) over the runs (3 per stage; S7-4: 6, two sets "
         "of 3). Judged against her answer key (`eval/test_set_h20.json`) by the judge of `eval/v1_vs_v2/score.py`. "
         "Made by `eval/s7/summary.py`.", "",
         "## Accuracy (her order of priority)", "",
         "| Stage | Verdict | False positives / scene | Incorrect corrections / scene | Items fully right | Corrected text not fully correct | Recall |",
         "|---|---|---|---|---|---|---|"]
    data = {}
    for label, names, verdict in STAGES:
        ds = [d for d in (load(n) for n in names) if d]
        if not ds:
            L.append(f"| {label} | {verdict} | not scored yet | | | | |")
            continue
        data[label] = (names, ds, verdict)
        L.append(f"| {label} | {verdict} | "
                 f"{stat(per_run(ds, lambda m: m['fp'] / m['n_scenes']))} | "
                 f"{stat(per_run(ds, lambda m: m['incorrect'] / m['n_scenes']))} | "
                 f"{stat(per_run(ds, lambda m: m['clean'] / m['items']), pct=True)} | "
                 f"{stat(per_run(ds, lambda m: m['after_bad'] / m['with_after'] if m['with_after'] else None), pct=True)} | "
                 f"{stat(per_run(ds, lambda m: m['recall'][0] / m['recall'][1]), pct=True)} |")
    L += ["", "## Display, categories, content, expressiveness", "",
          "| Stage | Partial sentences | Wrong category | Her flagged scenes caught | Notes in her wording | Good ideas 孟母 | Good ideas 神农 |",
          "|---|---|---|---|---|---|---|"]
    for label, (names, ds, _) in data.items():
        L.append(f"| {label} | {stat(per_run(ds, lambda m: m['partial'] / m['items']), pct=True)} | "
                 f"{stat(per_run(ds, lambda m: m['miscat_coarse'] / m['items']), pct=True)} | "
                 f"{stat(per_run(ds, lambda m: m['content']['caught'] / m['content']['her_flagged'] if m['content']['her_flagged'] else None), pct=True)} | "
                 f"{stat(per_run(ds, lambda m: m['content']['notes_miss_need'] / m['content']['notes'] if m['content']['notes'] else None), pct=True)} | "
                 f"{stat(per_run(ds, lambda m: m['expr']['mengmu'][0] / m['expr']['mengmu'][1] if m['expr']['mengmu'][1] else None), pct=True)} | "
                 f"{stat(per_run(ds, lambda m: m['expr']['shennong'][0] / m['expr']['shennong'][1] if m['expr']['shennong'][1] else None), pct=True)} |")
    L += ["", "## Retrieval and consistency across the 3 runs of a set (same input, same retrieval)", "",
          "| Stage (set) | Card reach | Information consistency | Same error identified | Lexical consistency | Places flagged in every run |",
          "|---|---|---|---|---|---|"]
    for label, (names, ds, _) in data.items():
        for n, d in zip(names, ds):
            info, same, lex, every = consistency(d)
            L.append(f"| {label}{' (set 2)' if n.endswith('set2') else ''} | {reach(d)} | {info} | {same} | {lex} | {every} |")
    L += ["", "## Variant inputs: the same error in a different context (156 target errors)", "",
          "Retrieval Jaccard = chunks shared by the original scene and its variant. Consistency at the target "
          "error vs original run 1: same flag decision / lexical / information.", "",
          "| Stage | Retrieval Jaccard | Rerun (noise floor) | b. Generation only (fixed retrieval) | c. End-to-end (own retrieval) |",
          "|---|---|---|---|---|"]
    for label, names, _ in STAGES:
        v = variant_row(names[0])
        if v:
            jac, rows = v
            cell = lambda r: f"{r[0]} / {r[1]} / {r[2]}"
            L.append(f"| {label} | {jac} | {cell(rows[0])} | {cell(rows[1])} | {cell(rows[2])} |")
    L += ["", "## Reading the numbers", "",
          "- Run-to-run noise is large: S7-4's two sets of 3 runs (identical prompts) gave false positives "
          "0.43 and 0.59 per scene. Differences in false positives smaller than ~0.1 per scene between stages "
          "measured with 3 runs each are not evidence either way.",
          "- Consistency differences of a few points are also within noise (identical-prompt stages S7-2 / S7-3 "
          "differed by 6 points).",
          "- Card reach and retrieval Jaccard are deterministic (no model randomness)."]
    out = REPORTS / "S7_summary.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
