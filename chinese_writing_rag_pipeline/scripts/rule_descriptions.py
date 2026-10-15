# -*- coding: utf-8 -*-
"""Human-readable names/descriptions for auto-derived tags, used to build
rule_card and ai_error_card chunks. Keep these short; the examples aggregated
under each card carry the real signal."""

GRAMMAR_RULE_DESC = {
    # Regex pattern searching - Total Corrections: 913
    # Corrections assigned a rule: Before - 296 /After - 913
    # Corrections feeding a rule: Before - 296 / After - 887
    # Rule cards: Before - 31 / After - 49
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
    "resultative_complement": "Resultative complement (V. + result, e.g. 擦干净, 写下, 吃到): the action verb alone vs. action + result -- 看 look vs. 看到 see, 找 look for vs. 找到 find, 听 vs. 听到, 注意 vs. 注意到.",
    "topic_comment_missing_subject": "Topic-comment sentences may legitimately omit an already-clear subject; not every omission is an error.",
    "repeated_wh_whichever": "Repeated wh-word construction ('哪一X就V哪一X') expressing 'whichever..., that one...'",
    "comparative_sentence": "Comparative sentence structures (比, 都, 最...不过了) and words that cannot be used inside a comparison.",
    "num_mw_noun_no_de": "Num. + MW. + noun does not take 的 (e.g. 一筐梨, not 一筐的梨).",
    "verb_object_collocation": "Collocation/valence errors: the verb cannot take that object or complement (想 + V. not N., 想让 Sb. V., 成为 + N.), an adjective does not go with that noun (良好 + 生活), or a verb conflicts with an adjacent verb.",
    "wrong_information_content": "Factual/content error: the sentence states something that contradicts the story's actual plot.",
    # patterns in the teacher's corrections that the regex taggers had no rule for.
    # Newly identified rule identification, check with 杨老师
    "aspect_zai_progressive": "在/正在 + V. marks an ongoing action (一直在学习); do not add 在 when the action is not ongoing.",
    "potential_complement": "Potential complement V.得/不 + result (睡不好, 想得起来) for whether an outcome can be achieved.",
    "degree_complement_de": "Degree complement V.得 + Adj. (病得很重, 搬得太频繁) rather than putting the degree word directly after the verb; 病/生病 cannot take 很 directly.",
    "bushi_jiushi_construction": "不是……就是…… means 'either ... or ...' (two alternatives that both happen); it is not 'not X but Y' (that is 不是……而是……). The subject goes before 不是.",
    "zhe_jiu_yao_kan": "这就要看……了 ('it depends on ...'): needs an uncertain condition before it (e.g. 会不会生病？) and an A-not-A / open question after 看.",
    "example_marker_tebie_bifang": "特别是 + N./clause singles out a typical example of what was just said; 比方说 introduces an example. Neither can replace 特别 (very) or stand without the general statement.",
    "a_not_a_question": "Embedded yes/no questions use A-not-A (有没有毒, 能不能吃, 知不知道) or 是……还是……; 'whether/if' in 'know if' is not 如果.",
    "adjective_predicate": "Adjectives are predicates on their own and normally take 很 (or another degree adverb) without 是 (他很聪明, not 他是聪明); 是……的 only for emphasis.",
    "dou_totality": "都 is required after totality expressions (从早到晚都, 每天都, 每人都, 什么都) and with 一直/也 in such sentences.",
    "he_connects_nouns_only": "和 links nouns/noun phrases only; it cannot link verb phrases, adjectives, or clauses (use 也, 又……又……, 而且, or a comma).",
    "attributive_modifier_de": "Modifiers come before the noun with 的 (一个叫孟子的小孩子, 住在离墓地很近的地方, 有毒的植物); no 的 after 很多 or in fixed phrases (好主意).",
    "adverbial_word_order": "Word order: subject first, then time/frequency/manner adverbials (常常, 都, 也, 先, 一共), then place (在 + Place), then the verb; duration and frequency after the verb (住了一个星期).",
    "time_expression": "Time expressions: 在古代 (not 古代的时候), 后来 vs. 以后 vs. 将来, 长大以后, Time + 以后; 'then' in a narrative is 然后/后来, not 以后 alone.",
    "missing_subject": "A required subject is missing (or must be restated after an aside), so the reader cannot tell who acts.",
    "reference_form": "Choosing the referring form: use a pronoun or zero form when the referent is clear instead of repeating the name, restore the name when the pronoun is ambiguous, and use 我/我们/你们 correctly inside quoted speech.",
    "word_choice": "Wrong or less suitable word: near-synonyms (别的 vs. 另外, 高兴 vs. 幸福, 食品 vs. 食物, 将来 vs. 后来), register, and words whose meaning does not fit the context.",
    "word_class_misuse": "A word used in the wrong part of speech: a noun used as a verb or adjective (经验, 毒 -> 有毒), an adjective used as a verb (合适 vs. 适合), 病 as a gradable adjective.",
    "you_zai_distinction": "又 for a repeated action that already happened (又搬家了) vs. 再 for one that has not happened yet (要再搬一次家).",
    "sentence_restructure": "The sentence needs rewriting as a whole; the teacher gives a reformulation rather than a single rule. (Not built into a rule card.)",
}

# Labels kept on correction_items for analysis but not aggregated into a rule_card:
# they are not one teachable rule.
NO_RULE_CARD = {"sentence_restructure"}

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
    "inappropriate_vocab_alternative": "AI's vocabulary suggestion offers an alternative that is wrong, too strong, too literary, or awkward in context (e.g. 饿叫, 携走, 低贱/卑微, 不良分子) -- every suggested alternative must itself be correct and natural at the student's level.",
    "unclassified": "Teacher's comment did not match a known pattern; needs manual review.",
}
