# -*- coding: utf-8 -*-
"""Human-readable names/descriptions for auto-derived tags, used to build
rule_card and ai_error_card chunks. Keep these short; the examples aggregated
under each card carry the real signal."""

GRAMMAR_RULE_DESC = {
    "aspect_le_completed": "Aspect marker 了 for completed actions / change of state -- when it must be added, and when it must NOT be added (e.g. habitual/routine actions take no 了).",
    "aspect_zhe_durative": "Aspect marker 着 marking an ongoing/durative action (e.g. two simultaneous actions, Place + V.着 + Obj.).",
    "aspect_guo_experiential": "Aspect marker 过 for a past experience; misused when the experience has not actually happened yet.",
    "directional_complement": "Directional complement word order: V. + directional complement (上/下/进/出) + Place + 来/去; 来/去 cannot directly take an object.",
    "ba_construction": "把-construction (disposal construction): used only for a deliberately initiated action on an object; typically ends with 了.",
    "bei_passive": "被-passive voice: marks something being done TO the subject; the following verb must fit an inanimate/passive-compatible sense.",
    "measure_word": "Measure word (MW) usage: num. + MW + noun; specific 的-marked nouns are usually not paired with 着-durative existential sentences.",
    "location_zai_place": "在 + Place phrase required before a verb of location/position.",
    "preposition_cong_place": "从 + Place ('from a place'); the object of 从 must be an actual place, not a person/abstract noun.",
    "preposition_dao_place": "到 + Place ('to a place').",
    "bushi_ershi_construction": "不是……而是…… ('not X but Y') used to refute a conventional assumption and assert the correct fact; subject placement rules.",
    "cai_jiu_construction": "才 Num. 就 V. construction expressing 'only/as early as Num., already V.'",
    "laoshi_negative_connotation": "老是 ('always/keeps on') carries a negative, complaining connotation -- wrong when the sentence is neutral/positive.",
    "gen_he_accompanying_zhe": "跟/和 + noun requires both nouns to perform the SAME action independently; when one entity is led/carried by another, use V.着 (e.g. 牵着驴) instead.",
    "jieguo_unexpected_result": "结果 introduces an unexpected result, not a plain sequential outcome.",
    "you_ye_distinction": "又 (repetition of a prior action) vs. 也 (similarity to another party's action).",
    "haide_harmful_result": "害得 must be followed by a clearly harmful/negative consequence, not a neutral one.",
    "wrong_character": "错别字 -- a wrong/miswritten Chinese character (as opposed to a word-choice/vocabulary problem).",
    "redundancy_delete": "Redundant word/phrase that should simply be deleted (repeated subject, repeated adverb, etc.).",
    "ambiguous_reference": "Ambiguous or vague referent (pronoun 他/她 unclear, vague noun like 人/事情/别人 needing specificity).",
    "character_introduction_first_mention": "A character should be briefly introduced on first mention (name + who they are) rather than assumed known.",
    "coherence_connectives": "Discourse coherence: sentences are loosely strung together without connectives/transitions.",
    "modal_verb_no_le": "Modal verbs (叫/让/想/要 etc.) are not followed by aspect marker 了.",
    "verb_reduplication": "Verb reduplication (V.V., e.g. 玩玩, 想想) used for light/tentative requests or plans.",
    "adverbial_de_multisyllabic": "地-marked adverbials: only multi-syllabic (2+ character) adverbs take 地 before a verb; monosyllabic adverbs do not.",
    "resultative_complement": "Resultative complement (V. + result, e.g. 擦干净) describing the outcome of an action.",
    "topic_comment_missing_subject": "Topic-comment sentences may legitimately omit an already-clear subject; not every omission is an error.",
    "repeated_wh_whichever": "Repeated wh-word construction ('哪一X就V哪一X') expressing 'whichever..., that one...'",
    "comparative_sentence": "Comparative sentence structures (比, 都, 最...不过了) and words that cannot be used inside a comparison.",
    "num_mw_noun_no_de": "Num. + MW. + noun does not take 的 (e.g. 一筐梨, not 一筐的梨).",
    "verb_object_collocation": "Verb-object collocation/valence errors: the verb cannot take that object, or conflicts with an adjacent verb.",
    "wrong_information_content": "Factual/content error: the sentence states something that contradicts the story's actual plot.",
}

AI_EVAL_DESC = {
    "missed_error": "AI failed to catch an error the teacher flagged (issue #1: AI often misses needed corrections).",
    "incorrect_correction": "AI's proposed correction is itself linguistically wrong (issue #2a: sometimes AI 'fixes' a correct original into something wrong).",
    "correct_fix_wrong_or_missing_explanation": "AI's corrected text happens to be right, but the grammatical explanation is wrong or absent (issue #2b).",
    "false_positive_unneeded_correction": "AI flagged/changed something that was already correct and needed no revision (issue #1/#3, over-correction).",
    "disfluency_false_positive": "AI's feedback targets a spoken-transcript disfluency (repetition/pause/filler) that should simply be removed in cleanup, not treated as a grammar error.",
    "misleading_no_error_framing": "AI says 'no correction needed' but still narrates a 'rule violated', which is self-contradictory and misleading (issue #3).",
    "misdirected_feedback": "AI labels span A as incorrect but the explanation/fix actually concerns a different span B (issue #4).",
    "miscategorized_error_type": "AI filed the issue under the wrong category, e.g. a vocabulary problem listed as grammar, or a vocabulary-misuse case labeled 错别字 (issue #5).",
    "grammatical_but_semantically_off": "AI's fix is grammatically valid but semantically/pragmatically wrong given the story context.",
    "disputed_rule_claim": "Teacher disputes the existence/applicability of the grammar rule AI invoked.",
    "validated_correct": "Teacher confirms this AI feedback item is fully correct (both fix and explanation) -- a positive calibration example.",
    "unclassified": "Teacher's comment did not match a known pattern; needs manual review.",
}
