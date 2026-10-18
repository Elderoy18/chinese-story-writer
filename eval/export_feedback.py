#!/usr/bin/env python3
"""Write a stage's feedback as readable Markdown, one file per story:

    python eval/export_feedback.py S7-0b [S6-h20 ...]
        -> eval/runs/<stage>/feedback/<sample>.md

Each file shows every scene's text and the feedback the learner would see,
then the end-of-story content feedback -- as displayed: the rule citations
("[rule: ...]", "[teacher rule: ...]", "[vocab list]") and the internal
"## Scene check" section are removed, by the same rules as the app's
lib/rag/displayFeedback.ts. The run JSON files stay the full record
(raw feedback, prompts, retrieved chunks, usage); this is only for reading.
"""
import json
import re
import sys
from pathlib import Path

RUNS = Path(__file__).resolve().parent / "runs"

CITATION = re.compile(r"\s*\[(?:rule|teacher rule)\s*:[^\]\n]*\]|\s*\[vocab list\]", re.I)
SCENE_CHECK = re.compile(r"^##\s*Scene check[^\n]*\n.*?(?=^##\s|\Z)", re.M | re.S)


def for_display(md):
    """Same as feedbackForDisplay in lib/rag/displayFeedback.ts."""
    md = SCENE_CHECK.sub("", CITATION.sub("", md))
    return re.sub(r"\n{3,}", "\n\n", md).strip()


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
            L += [f"## Scene {sc['scene']}", "", f"> {sc['text']}", "", demote(for_display(sc["feedback"])), ""]
        L += ["## End of story", "", demote(for_display(r["content"]["feedback"])), ""]
        (out / f"{f.stem}.md").write_text("\n".join(L), encoding="utf-8")
    print(f"{stage}: {len(files)} stories -> {out.relative_to(RUNS.parent.parent)}")


if __name__ == "__main__":
    for stage in sys.argv[1:]:
        export(stage)
