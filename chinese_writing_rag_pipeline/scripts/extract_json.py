#!/usr/bin/env python3
"""Extract each docx into an ordered list of non-empty paragraph texts (JSON)."""
import json
import sys
from docx import Document

FILES = {
    "student_examples_corrections": "raw/c69f060a-Student_Examples_Corrections.docx",
    "pear_story_corrections": "raw/c8085f66-Pear_Story_Corrections.docx",
    "mengmu_samples": "raw/82003636-___samples_with_Teacher_feedback.docx",
    "shennong_samples": "raw/40ac8d32-___samples_with_Teacher_feedback.docx",
    "model_stories": "raw/cbc2c76a-4_stories_model_story.docx",
}

def main():
    for key, path in FILES.items():
        doc = Document(path)
        paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        out_path = f"extracted/{key}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(paras, f, ensure_ascii=False, indent=1)
        print(f"{key}: {len(paras)} paragraphs -> {out_path}")

if __name__ == "__main__":
    main()
