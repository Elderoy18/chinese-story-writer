# -*- coding: utf-8 -*-
"""Human-readable names/descriptions for auto-derived tags, used to build
rule_card and ai_error_card chunks. Keep these short; the examples aggregated
under each card carry the real signal."""

GRAMMAR_RULE_DESC = {
    # Regex pattern searching - Total Corrections: 913
    # Corrections assigned a rule: Before - 296 /After - 913
    # Corrections feeding a rule: Before - 296 / After - 887
    # Rule cards: Before - 31 / After - 49
    "aspect_le_completed": "Aspect marker 了 for completed actions / change of state. If the focus is not completion, do not use 了. Mental-state verbs (觉得, 知道, 认为, 决定) take no 了, and neither do speaking words that introduce quoted speech (告诉, 说, 问); habitual/routine actions take no 了.",
    "aspect_zhe_durative": "Aspect marker 着 for a durative, relatively static state: not the main action but an accompanying state or action in the background (e.g. 牵着驴, 拿着花说, Place + V.着 + Obj.). Two simultaneous main actions use 一边……一边……, not 着.",
    "aspect_guo_experiential": "Aspect marker 过 for a past experience that has an impact on the present, often with a follow-up statement resulting from it; misused when the experience has not actually happened yet, and usually not used for routine everyday activities (eating, sleeping, drinking).",
    "directional_complement": "Directional complement word order. When the object is a place, 来/去 cannot take it directly: V. + directional complement + Place + 来/去 (爬上梯子去). When the object is an item, 来/去 can take it: V. + directional complement + 来/去 + Obj. (拿出来一个梨, 放上去一筐梨), or V. + directional complement + Obj. + 来/去 (拿出一个梨来).",
    "ba_construction": "把-construction: the subject does something to the object, causing the object to change, so the verb must be one that can cause a change. When the object's location changes because of the subject's action (a place, an object and a change of location), 把 must be used.",
    "bei_passive": "被-passive: the subject is the recipient of the action, not the performer, and usually something bad is done to the subject (negative connotation). The verb does not have to be one with an inanimate subject (e.g. 被打了).",
    "measure_word": "Measure word (MW) usage: num. + MW + noun, and 这/那 + MW + noun. In an existential Place + V.着 + Obj. sentence ('there is ...'), the object is usually generic (num. + MW + noun), not a definite noun such as 那些梨子.",
    "location_zai_place": "在 + Place phrase required before a verb of location/position.",
    "preposition_cong_place": "从 + Place ('from a place'). If the object of 从 is a person or an abstract noun, add a place marker such as 那儿 or 中 (从王朋那儿来, 从经验中得到).",
    "preposition_dao_place": "到 + Place ('to a place').",
    "bushi_ershi_construction": "不是……而是…… ('not X but Y') refutes something conventional or wrong and affirms the correct, often unexpected, fact. When both parts share one subject, the subject comes before 不是 (他不是……，而是……).",
    "cai_jiu_construction": "才 + Num. ... 就 + V.: the action happened early or after only a small amount (才五岁就开始学习, 才吃了两口饭就饱了).",
    "laoshi_negative_connotation": "老是 ('always/keeps on') carries a negative, complaining connotation -- wrong when the sentence is neutral/positive.",
    "gen_he_accompanying_zhe": "跟/和 + noun requires both nouns to perform the SAME action independently; when one entity is led/carried by another, use V.着 (e.g. 牵着驴) instead.",
    "jieguo_unexpected_result": "结果 introduces an unexpected result, usually a bad one, not a plain sequential outcome.",
    "you_ye_distinction": "又 (repetition of a prior action) vs. 也 (similarity to another party's action).",
    "haide_harmful_result": "害得 must be followed by the person affected and then the harmful result: ……害得 + someone + VP/clause (害得孟子学习不好). The result must be clearly harmful, not neutral.",
    "wrong_character": "错别字 -- a wrong/miswritten Chinese character (as opposed to a word-choice/vocabulary problem).",
    "redundancy_delete": "Redundant word/phrase that should simply be deleted (repeated subject, repeated adverb, etc.).",
    "ambiguous_reference": "Ambiguous or vague referent (pronoun 他/她 unclear, vague noun like 人/事情/别人 needing specificity).",
    "character_introduction_first_mention": "A character should be briefly introduced on first mention (name + who they are) rather than assumed known.",
    "coherence_connectives": "Discourse coherence: sentences are loosely strung together without connectives/transitions.",
    "modal_verb_no_le": "Modal verbs (叫, 让, 想, 要, 会, 能, 需要, 得, 可以, 不准, etc.) are not followed by aspect marker 了.",
    "verb_reduplication": "Verb reduplication (V.V., e.g. 玩玩, 想想) and V一V (试一试, 尝一尝) are for brief, light, tentative requests or plans, not for actions actually carried out (an executed action uses e.g. 尝试).",
    "adverbial_de_multisyllabic": "地-marked adverbials: only multi-syllabic (2+ character) adverbs take 地 before a verb; monosyllabic adverbs do not.",
    "resultative_complement": "Resultative complement (V. + result, e.g. 擦干净, 写下, 吃到). Many Chinese verbs denote only the attempt or process, not the result (看 look vs. 看到 see, 找 look for vs. 找到 find, 听 vs. 听到, 注意 vs. 注意到); when the result is meant, a resultative complement must be added.",
    "topic_comment_missing_subject": "Topic chain: when a series of clauses share the same topic, the later clauses can and should omit it; not every omitted subject is an error.",
    "repeated_wh_whichever": "Repeated wh-word construction for 'wh-ever ..., then ...'. The position of the second wh-word depends on its role: whenever -- 什么时候……，就什么时候……; wherever as subject -- 哪儿……，哪儿就……, as object -- 哪儿……，就V哪儿; whatever/whichever/whoever as subject -- 什么/哪MW./谁……，什么/哪MW./谁就……, as object -- 什么/哪MW./谁……，就V什么/哪MW./谁; however -- 怎么V.……，就怎么V.",
    "comparative_sentence": "The comparative sentence structure is A比B……. 都 (both/all) is not a comparative structure, and 最……不过了 is not one either: it means 'the best option' and only a few adjectives can enter it (好, 合适, 理想).",
    "num_mw_noun_no_de": "Num. + MW. + noun does not take 的 (e.g. 一筐梨, not 一筐的梨).",
    "verb_object_collocation": "Collocation/valence errors: the verb cannot take that object or complement (想 + V. not N., 想让 Sb. V., 成为 + N.), an adjective does not go with that noun (良好 + 生活), or a verb conflicts with an adjacent verb.",
    "wrong_information_content": "Factual/content error: the sentence states something that contradicts the story's actual plot.",
    # patterns in the teacher's corrections that the regex taggers had no rule for.
    # Newly identified rule identification, check with 杨老师
    "aspect_zai_progressive": "在/正在 + V. marks the ongoing foreground action in focus (一直在学习), in contrast to 着, which marks a background state; do not add 在 when the action is not ongoing.",
    "potential_complement": "Potential complement V.得/不 + result (睡不好, 想得起来): whether an outcome can be achieved, i.e. (in)ability or (im)possibility.",
    "degree_complement_de": "Some adjectives (e.g. 病) name states that have no degrees -- one is either sick or not -- so they cannot take degree words such as 很, 太, 有点儿 (*很病). Use a degree/descriptive complement with 得 instead (病得很重).",
    "bushi_jiushi_construction": "不是……就是…… means 'either ... or ...' (two alternatives that both happen); it is not 'not X but Y' (that is 不是……而是……). The subject goes before 不是.",
    "zhe_jiu_yao_kan": "这就要看……了 ('it depends on ...') gives a flexible response to a question or uncertain condition instead of a direct answer. The part after 看 must be a question form: A-not-A (吃不吃), a wh-word, or A还是B.",
    "example_marker_tebie_bifang": "特别是 + N./clause singles out a typical example of what was just said; 比方说 introduces an example. Neither can replace 特别 (very) or stand without the general statement.",
    "a_not_a_question": "Embedded yes/no questions use A-not-A (有没有毒, 能不能吃, 知不知道) or 是……还是……; 'whether/if' in 'know if' is not 如果.",
    "adjective_predicate": "Adjectives are predicates on their own and normally take 很 (or another degree adverb) without 是 (他很聪明, not 他是聪明); 是……的 only for emphasis.",
    "dou_totality": "都 is required after totality expressions (从早到晚都, 每天都, 每人都, 什么都).",
    "he_connects_nouns_only": "和 links nouns, noun phrases and pronouns only; it cannot link verb phrases, adjectives, or clauses (use 也, 又……又……, 而且, or a comma).",
    "attributive_modifier_de": "Modifiers come before the noun with 的 (一个叫孟子的小孩子, 住在离墓地很近的地方, 有毒的植物); no 的 after 很多 or in fixed phrases (好主意).",
    "adverbial_word_order": "Word order: subject first, then time/frequency/manner adverbials (常常, 都, 也, 先, 一共), then place (在 + Place), then the verb; duration and frequency after the verb (住了一个星期).",
    "time_expression": "Time expressions: 在古代 (not 古代的时候), 后来 vs. 以后 vs. 将来, 长大以后, Time + 以后; 'then' in a narrative is 然后/后来, not 以后 alone.",
    "missing_subject": "A required subject is missing (or must be restated after an aside), so the reader cannot tell who acts.",
    "reference_form": "Choosing the referring form: within one clause, use the zero form; close by in a different clause, with no other character in between, use a pronoun; restore the name when the pronoun would be ambiguous; and use 我/我们/你们 correctly inside quoted speech.",
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
    "false_positive_unneeded_correction": "AI flagged/changed something that was already correct and needed no revision (issue #1/#3).",
    "overcorrection": "AI's fix changes more than the error needs, or alters the student's intended meaning or own expression (e.g. drops their 把 construction or 去, turns 'one basket missing' into 'no pears at all'). Keep the student's wording and meaning as much as possible; change only what is wrong.",
    "wrong_or_missing_explanation": "The explanation is wrong, vague, or missing (it names the wrong rule, or a rule that does not apply), whether or not the fix itself is right. If the fix is right, correct_fix_wrong_or_missing_explanation also applies.",
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
