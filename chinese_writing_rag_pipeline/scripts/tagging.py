#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Heuristic, keyword-based taggers.

These are a first-pass, rule-based classification layer over free-text teacher
annotations. They are intentionally conservative (substring/regex matching on
the actual phrasing this teacher uses) rather than a learned classifier, so
that the tags are auditable and cheap to re-derive. They are meant to be
reviewed/refined by the teacher over time (see design doc, section "Tagging
accuracy & maintenance").
"""
import re

# ---------------------------------------------------------------------------
# 1) Grammar / linguistic-point tags, applied to teacher_correction_items and
#    to AI grammar-correction items. Order matters only for readability; all
#    matching tags are returned (multi-label).
# ---------------------------------------------------------------------------
GRAMMAR_RULE_PATTERNS = [
    ("aspect_le_completed", [r"了\s*\(?completed", r"了\s*change", r"delete了", r"add\s*了", r"了completed"]),
    ("aspect_zhe_durative", [r"着\s*durative", r"着\s*\(?durative"]),
    ("aspect_guo_experiential", [r"过.{0,15}experience", r"经历|经验.{0,10}过"]),
    ("directional_complement", [r"direction(?:al)?\s*complement"]),
    ("ba_construction", [r"[“\"]?把[”\"]?\s*(?:usually|is used|structure|Obj\.)", r"把.{0,15}disposal"]),
    ("bei_passive", [r"被.{0,15}passive", r"passive voice"]),
    ("measure_word", [r"\bMW\b", r"measure word", r"num\.\s*\+\s*MW", r"polite MW"]),
    ("location_zai_place", [r"在\s*\+\s*[Pp]lace", r"在\+[Pp]lace"]),
    ("preposition_cong_place", [r"从\s*\+\s*[Pp]lace", r"从\+[Pp]lace"]),
    ("preposition_dao_place", [r"到\s*\+\s*[Pp]lace", r"到\+\s*[Pp]lace"]),
    ("bushi_ershi_construction", [r"不是……而是……", r"不是\.\.\.而是\.\.\.", r"不是.{0,3}而是"]),
    ("cai_jiu_construction", [r"才\s*Num\.?\s*就", r"才.{0,4}就V"]),
    ("laoshi_negative_connotation", [r"老是.{0,20}(negative|complain)"]),
    ("gen_he_accompanying_zhe", [r"跟/和", r"accompanying phrase"]),
    ("jieguo_unexpected_result", [r"结果.{0,20}unexpected"]),
    ("you_ye_distinction", [r"又.{0,20}repeat", r"也.{0,20}similarit"]),
    ("haide_harmful_result", [r"害得.{0,25}harmful"]),
    ("wrong_character", [r"wrong character", r"错别字"]),
    ("redundancy_delete", [r"redundant"]),
    ("ambiguous_reference", [r"ambiguous", r"\bvague\b", r"unclear who", r"not identifying"]),
    ("character_introduction_first_mention", [r"first appear", r"briefly introduce"]),
    ("coherence_connectives", [r"loosely connected", r"lack.{0,10}conjunctions?", r"coherence"]),
    ("modal_verb_no_le", [r"modal\s*[Vv]erb"]),
    ("verb_reduplication", [r"V\.V\."]),
    ("adverbial_de_multisyllabic", [r"mono-?syllabic adverb", r"multi-?syllabic adv"]),
    ("resultative_complement", [r"resultative complement"]),
    ("topic_comment_missing_subject", [r"topic-comment", r"missing subj"]),
    ("repeated_wh_whichever", [r"repeated Wh", r"wh-?ever"]),
    ("comparative_sentence", [r"comparative sentence"]),
    ("num_mw_noun_no_de", [r"num\.\s*\+\s*MW\.?\s*\+\s*noun,?\s*no的"]),
    ("verb_object_collocation", [r"conflicts with", r"cannot be followed by an Obj", r"cannot be the Obj"]),
    ("wrong_information_content", [r"wrong information"]),
]

def tag_grammar_text(text):
    if not text:
        return []
    tags = []
    for tag, patterns in GRAMMAR_RULE_PATTERNS:
        for pat in patterns:
            if re.search(pat, text, flags=re.IGNORECASE):
                tags.append(tag)
                break
    return tags

# ---------------------------------------------------------------------------
# 2) AI-feedback-quality tags, applied to the teacher's "My comment" text that
#    critiques one AI feedback item. Multi-label. These map directly onto the
#    5 issue categories the teacher described.
# ---------------------------------------------------------------------------
AI_EVAL_PATTERNS = [
    # issue 4 in teacher's notes: feedback pointed at the wrong span
    ("misdirected_feedback", [
        r"feedback is not on the sentence", r"for another clause",
        r"not directed (?:at|to)", r"not on the sentence",
    ]),
    # issue 5: mis-categorization (grammar vs vocabulary vs wrong-character)
    ("miscategorized_error_type", [
        r"not a vocabulary (?:problem|issue)", r"not [“\"]?wrong characters?[”\"]?",
        r"vocabulary misuse", r"not a grammar issue", r"this is a [“\"]?vocabulary[”\"]? issue",
        r"already mentioned in", r"which is [“\"]?vocabulary suggestion[”\"]?",
    ]),
    # issue 3 (part b): AI said "no correction needed" in a self-contradicting / misleading way
    ("misleading_no_error_framing", [
        r"if no correction needed, then", r"if no error found, then", r"misleading",
    ]),
    # issue 1: AI's flagged-as-needing-fix item was actually fine / no revision needed
    ("false_positive_unneeded_correction", [
        r"no need to (?:revise|change)", r"is fine, ?too", r"perfectly fine",
        r"not necessary", r"original version is fine", r"no need to add",
    ]),
    # disfluency-specific false positive (transcription artifacts, not real errors)
    ("disfluency_false_positive", [r"disfluency"]),
    # AI's correction itself is linguistically wrong
    ("incorrect_correction", [
        r"revision (?:itself )?is incorrect", r"is incorrect, it should be",
        r"not completely correct", r"\bincorrect\.", r"^incorrect\.",
    ]),
    # correction/wording is right but the grammatical explanation is wrong or missing
    ("correct_fix_wrong_or_missing_explanation", [
        r"correct revision, but wrong explanation", r"revision is correct but the explanation is not",
        r"correct,? but (?:AI )?did not explain", r"revision is correct, but without explanation",
        r"correct,? but no explanation", r"explanation.{0,15}(?:is )?not given",
        r"explanation of.{0,30}(?:rule )?is not given",
    ]),
    # AI simply failed to catch an error that exists
    ("missed_error", [
        r"\bmiss(?:ed|es)?\b.{0,40}(?:error|revision|feedback|place)", r"did not capture",
        r"fails to revise", r"missed (?:other places|an error)",
    ]),
    # grammatically correct but semantically/pragmatically off (subtler than plain "incorrect")
    ("grammatical_but_semantically_off", [
        r"grammatically correct, but semantically incorrect", r"is a misunderstanding",
    ]),
    # teacher disputes the very grammar rule AI invoked
    ("disputed_rule_claim", [
        r"don.t think Chinese has", r"itself is not [“\"]?incorrect[”\"]?",
    ]),
    # clean endorsement of the AI item
    ("validated_correct", [
        r"^correct\.?$", r"^correct,?\s", r"^my comment: correct\.?$", r"^i agree\.?$",
    ]),
]

def tag_ai_eval_text(text):
    if not text:
        return []
    tags = []
    for tag, patterns in AI_EVAL_PATTERNS:
        for pat in patterns:
            if re.search(pat, text, flags=re.IGNORECASE):
                tags.append(tag)
                break
    # Fallback: bare "correct" endorsement with no caveat words -> validated_correct
    stripped = re.sub(r"^my comment:\s*", "", text.strip(), flags=re.IGNORECASE).strip()
    caveat_words = ["but", "however", "although", "not completely", "missed", "miss ",
                     "incorrect", "wrong", "misleading", "disfluency"]
    if not tags and stripped.lower().startswith("correct") and not any(w in stripped.lower() for w in caveat_words):
        tags.append("validated_correct")
    if not tags:
        tags.append("unclassified")
    return sorted(set(tags))

# ---------------------------------------------------------------------------
# 3) Content-coverage flag parsing (Miss N scene(s) / Wrong information / Coherence)
# ---------------------------------------------------------------------------
_NUM_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}

def split_correction(raw_text):
    """Best-effort split of a teacher correction-item line into
    original_span : corrected_span , explanation.
    The corpus consistently uses '：' or ':' to separate the original phrase
    from the correction+explanation; within the remainder, the explanation
    (when present) is reliably the part starting at/after the first English
    (ASCII-letter) word, split at the nearest preceding Chinese/ASCII comma.
    This is heuristic -- always keep raw_text as the source of truth."""
    parts = re.split(r"[:：]", raw_text, maxsplit=1)
    if len(parts) != 2:
        return {"original_span": None, "corrected_span": raw_text.strip(), "explanation": ""}
    original, rest = parts[0].strip(), parts[1].strip()
    m = re.search(r"[A-Za-z]", rest)
    if not m:
        return {"original_span": original, "corrected_span": rest, "explanation": ""}
    prefix = rest[: m.start()]
    comma_pos = max(prefix.rfind("，"), prefix.rfind(","))
    if comma_pos == -1:
        return {"original_span": original, "corrected_span": rest, "explanation": ""}
    corrected = rest[:comma_pos].strip()
    explanation = rest[comma_pos + 1 :].strip()
    return {"original_span": original, "corrected_span": corrected, "explanation": explanation}


def parse_content_flag(raw_text):
    """Return a structured record for one content_flags[] raw string."""
    if raw_text.startswith("Coherence problem"):
        return {
            "flag_type": "coherence_problem",
            "raw_text": raw_text,
            "detail": raw_text.split(":", 1)[1].strip() if ":" in raw_text else "",
        }
    if raw_text.startswith("Wrong information"):
        detail = raw_text.split(":", 1)[1].strip() if ":" in raw_text else ""
        items = [x.strip() for x in re.split(r"[；;]", detail) if x.strip()]
        return {
            "flag_type": "wrong_information",
            "raw_text": raw_text,
            "missing_or_wrong_items": items,
        }
    if raw_text.startswith("Miss"):
        m = re.match(r"^Miss (\w+) scenes?(?:\s*\(([^)]*)\))?:\s*(.*)$", raw_text)
        count = None
        qualifier = None
        detail = raw_text
        if m:
            count_word, qualifier, detail = m.groups()
            count = _NUM_WORDS.get(count_word.lower())
        items = [x.strip() for x in re.split(r"[；;]", detail) if x.strip()]
        return {
            "flag_type": "miss_scene",
            "raw_text": raw_text,
            "count": count,
            "qualifier": qualifier,  # e.g. "incomplete scenes", "wrong information"
            "missing_scene_items": items,
        }
    return {"flag_type": "content_note", "raw_text": raw_text}
