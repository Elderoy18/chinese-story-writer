#!/usr/bin/env python3
"""Write a stage's feedback as readable Markdown, one file per story:

    python eval/export_feedback.py S7-0b [S6-h20 ...]
        -> eval/runs/<stage>/feedback/<sample>.md

Each file shows every scene's text and the feedback the learner would see,
then the end-of-story content feedback. The run JSON files stay the record
(prompts, retrieved chunks, usage); this is only for reading.
"""
import json
import sys
from pathlib import Path

RUNS = Path(__file__).resolve().parent / "runs"


def demote(md):
    """The feedback's own '## Section' headings go one level below the scene heading."""
    return "\n".join("#" + l if l.startswith("#") else l for l in md.strip().splitlines())


def export(stage):
    out = RUNS / stage / "feedback"
    out.mkdir(exist_ok=True)
    files = sorted(f for f in (RUNS / stage).glob("*.json") if f.name != "stage.json")
    for f in files:
        r = json.load(open(f, encoding="utf-8"))
        L = [f"# {r['sample_id']} -- {stage}", "",
             f"Model {r['model']} ({r['reasoning_effort']}), snapshot {r['snapshot']}, {r['created'][:10]}", ""]
        for sc in r["scenes"]:
            L += [f"## Scene {sc['scene']}", "", f"> {sc['text']}", "", demote(sc["feedback"]), ""]
        L += ["## End of story", "", demote(r["content"]["feedback"]), ""]
        (out / f"{f.stem}.md").write_text("\n".join(L), encoding="utf-8")
    print(f"{stage}: {len(files)} stories -> {out.relative_to(RUNS.parent.parent)}")


if __name__ == "__main__":
    for stage in sys.argv[1:]:
        export(stage)
