# Step 13 report: the teacher finder (her patterns + HanLP checks)

Patterns kept only if she corrected the wording in at least 50% of the places it occurs in the train stories.

## Calibration on the train stories

Share of each part's flags that land on a correction she made (any kind / the same kind).

| Part | Flags on train | On one of her corrections | Of the same category |
|---|---|---|---|
| her patterns | 211 | 147/211 (70%) | 90/211 (43%) |
| zero_redundant_pronoun | 87 | 27/87 (31%) | 11/87 (13%) |
| first_mention_introduction | 71 | 40/71 (56%) | 34/71 (48%) |
| location_with_zai | 16 | 8/16 (50%) | 2/16 (12%) |
| no_le_mental_state | 12 | 7/12 (58%) | 7/12 (58%) |
| he_scope_coordination | 9 | 8/9 (89%) | 7/9 (78%) |
| numeral_measure_word_order | 5 | 3/5 (60%) | 2/5 (40%) |
| modal_and_control_verb_complements | 3 | 2/3 (67%) | 1/3 (33%) |
| no_le_speaking_word | 2 | 2/2 (100%) | 2/2 (100%) |

## Her wording patterns (21)

| Learner wording | Her correction | Category | Corrected / occurs in train | Her note |
|---|---|---|---|---|
| 看 | 看到 | perception_look_see | 37/71 | 了completed; 看look vs.看到see; 看look vs.看到see, no了 |
| 古代的时候 | 在古代 | location_with_zai | 18/30 |  |
| 是毒 | 有毒 | word_class_choice | 14/15 |  |
| 一看 | 一看到 | perception_look_see | 10/15 | 看look vs.看到see; 看look, 看到see |
| 可能 | ，这样可以 | loose_clause_connection | 9/14 |  |
| 毒的 | 有毒的 | word_class_choice | 9/11 |  |
| 别的人 | (delete) | other_vs_additional | 8/8 | “别的” is for “a different type”, and “all else except the spoken one”; “别的” is fo |
| 吃毒 | 吃到有毒的植物 | resultative_complements | 5/5 |  |
| 走去 | 走着 | zhe_durative | 5/5 | usually we do not say “走去”.; “骑自行车“ conflicts with ”走“; 走着durative |
| 在古代的时候 | 在古代 | redundant_words | 4/5 |  |
| 古代时候 | 古代 | redundant_words | 3/3 |  |
| 食品 | 植物 | near_synonym_precision | 3/3 | “食品” is usually for processed food; 食品is for processed food |
| 哲学人 | 哲学家 | fixed_expressions | 3/3 |  |
| 找了 | 找到了 | search_find | 3/5 | 找look for vs.找到find |
| 他的人民 | 他发现人们 | possessive_reference | 3/3 | “他的人民”implies that神农is a king |
| 看了 | 看到了 | perception_look_see | 3/3 | 看look vs.看到see |
| 搬家三次 | 搬了三次家 | numeral_measure_word_order | 2/2 | 了completed, V. + Num. + MW. + Obj.; 了completed，V. + Num. + MW. + Obj. |
| 受到 | 得到 | collocation_selection | 2/4 |  |
| 长大的时候 | 小时候 | incorrect_story_information | 2/2 |  |
| 在中国古代的时候 | 在古代中国， | location_with_zai | 2/2 |  |
| 尝尝 | 尝 | verb_reduplication_requests | 2/2 | V.V. is used to make requests or plans |

## Her insertion patterns (0)

| After | She adds | Category | Added / occurs without it in train | Her note |
|---|---|---|---|---|

## Test candidates (87)

- mengmu_samples#4 [location_with_zai]: [古代的时候→在古代] — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- mengmu_samples#4 [search_find]: 孟子在那个商店也[找了→找到了]到工作 — her pattern: 找了 -> 找到了 (corrected 3/5 in train)
- mengmu_samples#4 [zero_redundant_pronoun]: [-他]成为很有名的哲人 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#4 [first_mention_introduction]: ⟦孟子⟧和孟母住了在靠墓地的家 — first appearance of 孟子: briefly introduce who this is
- mengmu_samples#4 [first_mention_introduction]: 孟子和⟦孟母⟧住了在靠墓地的家 — first appearance of 孟母: briefly introduce who this is
- mengmu_samples#10 [perception_look_see]: 就是[看→看到]哲学书 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- mengmu_samples#10 [location_with_zai]: 孟子和他的朋友喜欢[玩在墓地里→在墓地里玩] — 在 + Place comes before the action: 在Place + V.
- mengmu_samples#10 [zero_redundant_pronoun]: 难怪[-他]成为很有名的哲学家 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#10 [first_mention_introduction]: ⟦孟子⟧小的时候 — first appearance of 孟子: briefly introduce who this is
- mengmu_samples#10 [first_mention_introduction]: 孟子和⟦孟母⟧搬到子思老师的家 — first appearance of 孟母: briefly introduce who this is
- mengmu_samples#12 [first_mention_introduction]: ⟦孟子⟧跟孟母住在墓地的旁边 — first appearance of 孟子: briefly introduce who this is
- mengmu_samples#12 [first_mention_introduction]: 孟子跟⟦孟母⟧住在墓地的旁边 — first appearance of 孟母: briefly introduce who this is
- mengmu_samples#18 [location_with_zai]: [古代的时候→在古代] — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- mengmu_samples#18 [location_with_zai]: 孟子的妈妈不是[待在家里就是→在家里就是待]编织衣服赚钱 — 在 + Place comes before the action: 在Place + V.
- mengmu_samples#25 [location_with_zai]: 他的妈妈[觉得在墓地→在墓地觉得]玩儿 — 在 + Place comes before the action: 在Place + V.
- mengmu_samples#25 [zero_redundant_pronoun]: 难怪[-他]成为有名的人 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#25 [first_mention_introduction]: ⟦孟子⟧小的时候 — first appearance of 孟子: briefly introduce who this is
- mengmu_samples#32 [location_with_zai]: [古代的时候→在古代] — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- mengmu_samples#32 [no_le_mental_state]: 所以她决定[-了]他们会搬家找更好的地方 — no 了 after the mental-state verb 决定
- mengmu_samples#32 [zero_redundant_pronoun]: 所以[-她]会一直搬家才能找到质量好的教育 — 她 repeats the subject of the clause before: zero form
- mengmu_samples#32 [no_le_speaking_word]: 她告诉[-了]孟子：他们不是朋友 — no 了 after the speaking verb 告诉
- mengmu_samples#32 [no_le_speaking_word]: 告诉[-了]孟子：我们找到了最后的家 — no 了 after the speaking verb 告诉
- mengmu_samples#32 [first_mention_introduction]: 有一天⟦孟子⟧去了墓地玩儿 — first appearance of 孟子: briefly introduce who this is
- mengmu_samples#33 [zero_redundant_pronoun]: 很多墓地得[-我]祭拜 — 我 repeats the subject of the clause before: zero form
- mengmu_samples#33 [zero_redundant_pronoun]: [-他]越来越喜欢祭拜 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#33 [zero_redundant_pronoun]: 所以[-他]祭拜不是想帮妈妈工作 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#33 [zero_redundant_pronoun]: 而是[-他]很喜欢画画 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#33 [first_mention_introduction]: ⟦孟子⟧和他妈妈住在中国 — first appearance of 孟子: briefly introduce who this is
- mengmu_samples#39 [location_with_zai]: [古代的时候→在古代]人觉得祭拜非常重要 — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- mengmu_samples#39 [perception_look_see]: 孟子妈妈[看→看到]了他的同学们对孟子不好的影响 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- mengmu_samples#39 [perception_look_see]: 孟子妈妈[看了→看到了]他的同学们对孟子不好的影响 — her pattern: 看了 -> 看到了 (corrected 3/3 in train)
- mengmu_samples#39 [perception_look_see]: 而是[看→看到]政治文章 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- mengmu_samples#39 [zero_redundant_pronoun]: [-你]会成为高薪 — 你 repeats the subject of the clause before: zero form
- mengmu_samples#39 [first_mention_introduction]: ⟦孟子⟧很小的时候 — first appearance of 孟子: briefly introduce who this is
- mengmu_samples#45 [location_with_zai]: [古代的时候→在古代] — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- mengmu_samples#45 [zero_redundant_pronoun]: [-他]想他的朋友 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#45 [zero_redundant_pronoun]: 因为[-他]不要离开他的城市 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#45 [first_mention_introduction]: 一个男孩子跟⟦他⟧的妈妈住在中国 — the story starts with a pronoun: introduce the character first
- mengmu_samples#47 [zero_redundant_pronoun]: 难怪[-他]很聪明 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#47 [first_mention_introduction]: ⟦孟母⟧三迁 — first appearance of 孟母: briefly introduce who this is
- shennong_samples#4 [location_with_zai]: [古代的时候→在古代] — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- shennong_samples#4 [perception_look_see]: 这就要[看→看到]你的口味了 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#4 [other_vs_additional]: 一个[-别的人]问神农 — her pattern: 别的人 -> (delete) (corrected 8/8 in train)
- shennong_samples#4 [other_vs_additional]: 一个[-别的人]问神农 — her pattern: 别的人 -> (delete) (corrected 8/8 in train)
- shennong_samples#4 [zero_redundant_pronoun]: 所以[-神农]去了吃每种植物 — 神农 repeats the subject of the clause before: zero form
- shennong_samples#4 [first_mention_introduction]: ⟦他⟧的名字是神农 — the story starts with a pronoun: introduce the character first
- shennong_samples#8 [location_with_zai]: [古代的时候→在古代] — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- shennong_samples#8 [perception_look_see]: 一[看→看到]很多人正在吃一些植物 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#8 [perception_look_see]: [一看→一看到]很多人正在吃一些植物 — her pattern: 一看 -> 一看到 (corrected 10/15 in train)
- shennong_samples#8 [perception_look_see]: 这就要[看→看到]你想不想生病了 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#12 [no_le_mental_state]: 发现[-了]夹竹桃有毒 — no 了 after the mental-state verb 发现
- shennong_samples#12 [first_mention_introduction]: ⟦神农⟧ — first appearance of 神农: briefly introduce who this is
- shennong_samples#18 [perception_look_see]: 神农问他的哥哥：“我应该吃这种植物吗？”哥哥说：“这就要[看→看到]你想要安全还是接近知道了 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#18 [word_class_choice]: 夹竹桃[是毒→有毒]的 — her pattern: 是毒 -> 有毒 (corrected 14/15 in train)
- shennong_samples#18 [word_class_choice]: 夹竹桃是[毒的→有毒的] — her pattern: 毒的 -> 有毒的 (corrected 9/11 in train)
- shennong_samples#18 [zero_redundant_pronoun]: 特别是如果[-我们]已经吃了夹竹桃 — 我们 repeats the subject of the clause before: zero form
- shennong_samples#18 [first_mention_introduction]: ⟦神农⟧和他的家人住在古代 — first appearance of 神农: briefly introduce who this is
- shennong_samples#19 [location_with_zai]: [古代的时候→在古代] — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- shennong_samples#19 [word_class_choice]: 特别[是毒→有毒] — her pattern: 是毒 -> 有毒 (corrected 14/15 in train)
- shennong_samples#19 [first_mention_introduction]: ⟦他⟧叫神农 — the story starts with a pronoun: introduce the character first
- shennong_samples#26 [search_find]: [找了→找到了]各种各样的植物 — her pattern: 找了 -> 找到了 (corrected 3/5 in train)
- shennong_samples#26 [other_vs_additional]: 跟[-别的人]分享他的发现 — her pattern: 别的人 -> (delete) (corrected 8/8 in train)
- shennong_samples#26 [perception_look_see]: 你认为神农的故事真的吗？这就要[看→看到]你相信中药对身体有好处 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#33 [redundant_words]: [古代时候→古代] — her pattern: 古代时候 -> 古代 (corrected 3/3 in train)
- shennong_samples#33 [perception_look_see]: 这就要[看→看到]你的口味 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#33 [loose_clause_connection]: [可能→，这样可以]喜欢糖 — her pattern: 可能 -> ，这样可以 (corrected 9/14 in train)
- shennong_samples#33 [word_class_choice]: 不小心吃了[毒的→有毒的]花 — her pattern: 毒的 -> 有毒的 (corrected 9/11 in train)
- shennong_samples#33 [word_class_choice]: 什么植物[是毒→有毒] — her pattern: 是毒 -> 有毒 (corrected 14/15 in train)
- shennong_samples#33 [first_mention_introduction]: ⟦神农⟧出去试一试很多种植物 — first appearance of 神农: briefly introduce who this is
- shennong_samples#35 [word_class_choice]: 神农觉得这个植物可能特别[是毒→有毒] — her pattern: 是毒 -> 有毒 (corrected 14/15 in train)
- shennong_samples#35 [loose_clause_connection]: 神农觉得这个植物[可能→，这样可以]特别是毒 — her pattern: 可能 -> ，这样可以 (corrected 9/14 in train)
- shennong_samples#35 [perception_look_see]: 这就要[看→看到]如果这把花毒不毒了 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#35 [other_vs_additional]: [-别的人]给了神农一个灵芝 — her pattern: 别的人 -> (delete) (corrected 8/8 in train)
- shennong_samples#35 [zero_redundant_pronoun]: [-他]想把花放在茶里 — 他 repeats the subject of the clause before: zero form
- shennong_samples#35 [first_mention_introduction]: ⟦神农⟧先看到很多病人 — first appearance of 神农: briefly introduce who this is
- shennong_samples#42 [location_with_zai]: [古代的时候→在古代]有一个人叫神农 — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- shennong_samples#42 [perception_look_see]: 一[看→看到]别的人就想帮助他们 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#42 [perception_look_see]: [一看→一看到]别的人就想帮助他们 — her pattern: 一看 -> 一看到 (corrected 10/15 in train)
- shennong_samples#42 [other_vs_additional]: 一看[-别的人]就想帮助他们 — her pattern: 别的人 -> (delete) (corrected 8/8 in train)
- shennong_samples#42 [zhe_durative]: 神农三个月[走去→走着] — her pattern: 走去 -> 走着 (corrected 5/5 in train)
- shennong_samples#42 [zero_redundant_pronoun]: [-他]不知道什么东西能做药 — 他 repeats the subject of the clause before: zero form
- shennong_samples#49 [location_with_zai]: [古代的时候→在古代] — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- shennong_samples#49 [resultative_complements]: 如果他们还怕[吃毒→吃到有毒的植物] — her pattern: 吃毒 -> 吃到有毒的植物 (corrected 5/5 in train)
- shennong_samples#49 [word_class_choice]: 像星星的植物[是毒→有毒] — her pattern: 是毒 -> 有毒 (corrected 14/15 in train)
- shennong_samples#49 [zero_redundant_pronoun]: [-他]连毒都能吃 — 他 repeats the subject of the clause before: zero form
- shennong_samples#49 [no_le_with_mei]: 可是他还没吃[-了]一个叫夹竹桃的植物 — 没 + V., no 了
- shennong_samples#49 [zero_redundant_pronoun]: 觉得[-他]快会死了 — 他 repeats the subject of the clause before: zero form
