# Step 14 report: the judging step

- 359 flagged places (LLM run 1 + GEC + teacher finder), judged one scene at a time; tokens {'prompt_tokens': 149968, 'completion_tokens': 79709, 'total_tokens': 229677}
- kept 221, dropped 138

## What was kept

| Flagged places | Kept |
|---|---|
| on a correction she made | 161/205 (79%) |
| on nothing she marked | 60/154 (39%) |

Dropping a place she corrected is a loss; dropping a place she did not mark is usually the judge doing its job (her answers on `review/09_extra_flags.csv` will show how often those were real errors).

## Places she corrected that the judge dropped

- mengmu_samples#10: 孟子从五岁【一直】学哲学 — judge: 从五岁一直学哲学 is acceptable without 起 or an endpoint.
- mengmu_samples#18: 【古代的时候】 — judge: Natural temporal expression for a beginner.
- mengmu_samples#18: 所以孟子【的】妈妈认为这样的地方对儿子的教育不太好 — judge: 孟子的妈妈 is a natural possessive phrase.
- mengmu_samples#25: 所以他每天【老是】从早到晚去墓地跟朋友们玩玩儿 — judge: 每天老是 is acceptable emphasis here.
- mengmu_samples#25: 所以他每天老是从早到晚去墓地跟朋友们玩【玩】儿 — judge: 玩玩儿 is a valid reduplicated verb form.
- mengmu_samples#25: 害得【，所以】他们搬家 — judge: After correcting 害得 to 不好, 所以 correctly marks cause and result.
- mengmu_samples#25: 可是每天不是写字就是帮妈妈【的】工作 — judge: 帮妈妈的工作 is acceptable and not merely redundant.
- mengmu_samples#32: 所以她决定了他们会搬家找更好的【地方】 — judge: 地方 adds necessary meaning as the destination.
- mengmu_samples#32: 因为她【恐怕】儿子会成为跟他们很像 — judge: 恐怕 naturally expresses her worry or fear.
- mengmu_samples#32: 而是当哲学家【^】 — judge: 当哲学家 is complete without 的.
- mengmu_samples#32: 孟子学【^】了怎么祭拜 — judge: 学了怎么祭拜 is grammatical and complete.
- mengmu_samples#32: 【他难怪】成为有名的哲学家 — judge: This word order was accepted in her similar past correction.
- mengmu_samples#33: 孟子妈妈的工作是祭拜【^】 — judge: 祭拜 can describe the work without a stated object
- mengmu_samples#33: 可是他【^】六岁 — judge: “他六岁” is grammatically acceptable and supports the contrast.
- mengmu_samples#39: 【古代的时候】人觉得祭拜非常重要 — judge: Natural time expression; no correction needed.
- mengmu_samples#39: 孟子妈妈看了他的同学们对孟子【^】不好的影响 — judge: The noun phrase does not require 有.
- mengmu_samples#39: 所以孟子和孟子【^】妈妈搬家了 — judge: 孟子妈妈 is an acceptable kinship phrase.
- mengmu_samples#39: 而是【看】政治文章 — judge: 看政治文章 describes habitual reading, not successful seeing
- mengmu_samples#4: 【古代的时候】 — judge: Acceptable time expression.
- mengmu_samples#4: 孟子和孟母住了在【靠】墓地的家 — judge: 靠墓地的家 is understandable and acceptable.
- mengmu_samples#4: 他们搬了【到】别一个城市找工作 — judge: Deleting 到 would make 搬了别一个城市 ungrammatical.
- mengmu_samples#45: 【古代的时候】 — judge: Natural time expression; not an error.
- mengmu_samples#45: 但是城市【^】有才两个学校 — judge: Adding 只 is not the minimal correction.
- mengmu_samples#45: 【他难怪】抱怨 — judge: The flagged text is not in the current scene; 孟子一直抱怨 is acceptable.
- shennong_samples#12: 会告诉他的朋友哪一【个】植物能不能吃 — judge: 个 can classify an individual plant.
- shennong_samples#18: 他们去【^】很多不一样的地方 — judge: Bare 去 can describe their general journey activity.
- shennong_samples#18: 神农问他的哥哥：“我应该吃这种植物吗？”哥哥说：“这就要看你想要安全还是接近【知道了】 — judge: Sentence-final 了 is acceptable in this 看…还是…了 structure.
- shennong_samples#19: 他找到【^】黄色的花 — judge: 找到黄色的花 is acceptable without a classifier or 了.
- shennong_samples#26: 有一个【老男人】叫神农 — judge: Understandable elderly-man introduction; replacing it is stylistic.
- shennong_samples#26: 他一次试一试有些植物的【叶】 — judge: 叶 is an acceptable word for leaves.
- shennong_samples#26: 煮这些【叶】以后 — judge: 叶 is acceptable here; 叶子 is only an alternative.
- shennong_samples#35: 【别的人】给了神农一个灵芝 — judge: 该文字不在当前场景中。
- shennong_samples#35: 这个植物可以让神农【^】更好 — judge: 让神农更好 is grammatical and natural.
- shennong_samples#4: 所以神农去了【吃】每种植物 — judge: 吃 is required as the action.
- shennong_samples#4: 一【个】灵芝和一个男人正好在我的旁边 — judge: 个 is an acceptable general classifier here.
- shennong_samples#42: 一回家就告诉【^】别人 — judge: 一……就…… can omit 了
- shennong_samples#42: 那【^】红灵芝对身体好处 — judge: 那红灵芝 is acceptable without a classifier
- shennong_samples#49: 他希望别人也可以吃【^】好吃的植物 — judge: Generic 吃好吃的植物 does not require 到.
- shennong_samples#49: 【^】不会吃他喜欢的植物 — judge: 就 may be omitted after 如果.
- shennong_samples#49: 他是第一【人，】找到了茶 — judge: No missing word at this position.
- shennong_samples#49: 找到【了】茶 — judge: 找到了 correctly marks a completed finding.
- shennong_samples#49: 找到了茶【^】 — judge: 人 is already present in 第一个人 after the needed correction.
- shennong_samples#8: 神农想帮【^】别人 — judge: 帮别人 is correct and natural.
- shennong_samples#8: 一些【植物】不能吃 — judge: The noun is needed and the sentence is grammatical.

## Places she did not mark that the judge kept (first 40)

- mengmu_samples#10: 孟子五岁【的】时候 → 的→ (numeral_measure_word_order) — 五岁的时候 does not take 的.
- mengmu_samples#10: 难怪【他】成为很有名的哲学家 → 他→ (zero_redundant_pronoun) — The subject is already clear from the close preceding clause.
- mengmu_samples#10: 难怪他成为【^】很有名的哲学家 → →了 (le_completed) — Becoming a famous philosopher is a completed change of state.
- mengmu_samples#12: 孟子跟【孟母】住在墓地的旁边 → 孟母→他的妈妈 (first_mention_introduction) — introduce the mother by her relationship
- mengmu_samples#12: 住在商店的旁边【不是适合】孟子 → 不是适合→不但不适合 (collocation_selection) — 适合 takes 不, and the sentence needs the paired connector.
- mengmu_samples#12: 【而是】让他觉得很伤心 → 而是→而且 (other) — 不但 should pair with 而且, not 而是.
- mengmu_samples#18: 而且【害得】孟子的学习 → 害得→影响了 (haide_harmful_result) — 害得 needs a harmful result clause, not a noun object.
- mengmu_samples#18: 孟子的妈妈觉得孟子【取得】良好的教育是很重要的 → 取得→接受 (collocation_selection) — 取得 does not naturally collocate with 教育.
- mengmu_samples#25: 他【^】很聪明的人 → →是个 (other) — A noun predicate needs 是个 here.
- mengmu_samples#25: 难怪【他】成为有名的人 → 他→ (zero_redundant_pronoun) — Repeated subject can be omitted in a close continuation.
- mengmu_samples#32: 所以【她】会一直搬家才能找到质量好的教育 → 她→ (zero_redundant_pronoun) — The subject is already clear from the close context.
- mengmu_samples#32: 但是孟子【老是】跟这些卖东西的人常常玩儿 → 老是→ (other) — 老是 and 常常 redundantly express frequency.
- mengmu_samples#32: 因为她恐怕儿子会【成为】跟他们很像 → 成为→变得 (near_synonym_precision) — 成为 cannot directly take an adjective phrase.
- mengmu_samples#33: 很多墓地得【我】祭拜 → 我→ (zero_redundant_pronoun) — the subject is already clear from the preceding clause
- mengmu_samples#33: 所以我们得【去】很多不同的地方 → 去→搬到 (other) — the explanation should match the earlier claim of moving house
- mengmu_samples#33: 所以【他】祭拜不是想帮妈妈工作 → 他→ (zero_redundant_pronoun) — repeated subject is redundant
- mengmu_samples#33: 而是【他】很喜欢画画 → 他→ (zero_redundant_pronoun) — subject should not repeat after 而是
- mengmu_samples#33: 而是他很喜欢【画画】 → 画画→祭拜 (not_but_refutation) — the alternative reason should relate to worshipping
- mengmu_samples#33: 孟子成为【^】很著名的古代画家 → 很著名的古代画家→很著名的古代哲学家 (incorrect_story_information) — Mencius was a philosopher, not a painter
- mengmu_samples#39: 【而是】学政治 → 而是→而要 (word_class_choice) — 不要 is paired with 而要.
- mengmu_samples#4: 孟子和【孟母】住了在靠墓地的家 → 孟母→他的妈妈 (first_mention_introduction) — The mother should be introduced by her relationship.
- mengmu_samples#4: 在【那个城市】 → 那个→一个 (other) — No city has been introduced for 那个 to refer to.
- mengmu_samples#4: 【他】成为很有名的哲人 → 他→ (zero_redundant_pronoun) — The subject is already clear from the close preceding clause.
- mengmu_samples#4: 他成为【^】很有名的哲人 → →了 (le_completed) — Becoming a philosopher is a completed change of state in the narrative.
- mengmu_samples#45: 所以孟子老是【祭拜】 → 祭拜→模仿别人办丧事 (other) — This contradicts the story action.
- mengmu_samples#45: 孟子不是【祭拜】 → 祭拜→模仿别人办丧事 (other) — This contradicts the story action.
- mengmu_samples#45: 他们搬家到【^】有很多学校的城市 → →了 (le_completed) — The move is a completed narrative action.
- mengmu_samples#45: 所以他成为【^】哲学家 → →了 (le_completed) — Becoming a philosopher is a completed change of state.
- mengmu_samples#47: 难怪【他】很聪明 → 他→ (zero_redundant_pronoun) — Repeated subject in close continuation should be omitted.
- shennong_samples#12: 【旅行很远】找到很多植物 → 旅行很远→走了很远 (collocation_selection) — 旅行很远 is not a natural travel expression here.
- shennong_samples#12: 旅行很远【找到】很多植物 → 找到→找到了 (other) — The completed narrative event needs 了.
- shennong_samples#12: 神农遇到了一【个】黄色的花 → 个→朵 (other) — 朵 is the appropriate measure word for an individual flower.
- shennong_samples#12: 发现【了】夹竹桃有毒 → 了→ (no_le_mental_state) — Discovery verb should not take 了 here.
- shennong_samples#12: 很快给他吃【^】一个灵芝 → →了 (le_completed) — Completed narrative action needs 了.
- shennong_samples#19: 凉山【^】很大的山 → →是一座 (other) — A copula and measure word are needed for the noun predicate.
- shennong_samples#19: 这【冰】茶是药 → 冰→杯 (other) — The context calls for a cup of tea, not iced tea.
- shennong_samples#26: 【找了】各种各样的植物 → 找了→找到了 (search_find) — He later tests the plants, so the sentence gives a successful finding result.
- shennong_samples#26: 神农【试一试】每个植物 → 一→了 (le_completed) — The testing is a completed narrative action.
- shennong_samples#26: 他一喝就知道他发现【^】新的茶叶 → →了 (le_completed) — The discovery is a completed narrative event.
- shennong_samples#33: 人不知道【他们】能吃什么植物 → 他们→ (zero_redundant_pronoun) — The repeated generic subject is unnecessary.

## Example decisions with what the judge saw (first 8)

**mengmu_samples#10 P0** 【孟子】小的时候
- proposed by the teacher's pattern/rule: ⟦孟子⟧小的时候
- her past correction (first_mention_introduction, sim 1.0): ⟦孟子⟧小的时候 — better to briefly introduce “孟子” when this character first appears
- her past correction (first_mention_introduction, sim 0.833): ⟦孟子⟧出生以后 — better to briefly introduce “孟子” when this character first appears
- her past correction (loose_clause_connection, sim 0.802): ⟦孟子是孩子⟧ — no logic relationship with the preceding or following sentences
- cards: first_mention_introduction, loose_clause_connection
- **decision: keep** 孟子→有一个孩子叫孟子，他 (first_mention_introduction) — First mention needs an identifying noun phrase.

**mengmu_samples#10 P1** 孟子和他的朋友喜欢【玩在墓地里】
- proposed by the AI checker: 孟子和他的朋友喜欢[玩在墓地里→在墓地里玩]
- proposed by the correction model: 孟子和他的朋友喜欢[-玩]在墓地里
- proposed by the teacher's pattern/rule: 孟子和他的朋友喜欢[玩在墓地里→在墓地里玩]
- proposed by the correction model: 孟子和他的朋友喜欢玩在墓地里[+玩]
- her past correction (loose_clause_connection, sim 0.82): ⟦孟子从早到晚想玩玩儿，所以他和朋友坐墓地在祭拜⟧ — loosely connected with the preceding sentence
- her past correction (no_le_routine_state, sim 0.818): 孟子一直跟他的朋友⟦去了⟧墓地祭拜 — no了for routine/habit
- her past correction (perception_look_see, sim 0.788): 孟子跟朋友[看→看到]很多的大人在墓地祭拜 — 看look vs.看到see
- cards: location_with_zai, loose_clause_connection
- **decision: keep** 玩在墓地里→在墓地里玩 (location_with_zai) — Location should precede the action.

**mengmu_samples#10 P2** 【装】祭拜
- proposed by the AI checker: [装→装作]祭拜
- her past correction (conditional_jiu, sim 0.658): [+就]开始祭拜 — 才 Num.就V.
- her past correction (verb_object_valency, sim 0.63): 在墓地[-做]祭拜
- her past correction (zero_redundant_pronoun, sim 0.621): 而是[-他]祭拜
- cards: conditional_jiu, verb_object_valency
- **decision: keep** 装→装作 (other) — 装作 is needed before a verb phrase.

**mengmu_samples#10 P3** 孟子五岁【的】时候
- proposed by the teacher's pattern/rule: 孟子五岁[-的]时候
- her past correction (redundant_words, sim 0.771): [-有一天]孟子才四岁
- her past correction (first_mention_introduction, sim 0.741): ⟦孟子⟧小的时候 — better to briefly introduce “孟子” when this character first appears
- her past correction (conditional_jiu, sim 0.702): 孟子才三岁[+就]开始搬家 — 才Num.就V.
- cards: numeral_measure_word_order, redundant_words
- **decision: keep** 的→ (numeral_measure_word_order) — 五岁的时候 does not take 的.

**mengmu_samples#10 P4** 跟妈妈搬家【^】
- proposed by the correction model: 跟妈妈搬家[+了]
- her past correction (redundant_words, sim 0.8): 跟孟母[-一起]搬家三次
- her past correction (numeral_measure_word_order, sim 0.795): 跟孟母一起[搬家三次→搬了三次家] — 了completed，V. + Num. + MW. + Obj.
- her past correction (conditional_jiu, sim 0.781): [+就]跟孟母一起搬家三次 — 才 Num.就V.
- cards: redundant_words, numeral_measure_word_order
- **decision: drop** → (other) — The completed-event 了 is optional here.

**mengmu_samples#10 P5** 而是【因为】妈妈认为他们的家离墓地太近
- proposed by the correction model: 而是[-因为]妈妈认为他们的家离墓地太近
- her past correction (modal_and_control_verb_complements, sim 0.689): 他的妈妈[不想跟他的朋友去墓地→不想让他跟朋友去墓地] — otherwise it means his mother didn’t want to go with his friend to the graveyard.
- her past correction (location_with_zai, sim 0.682): 孟子和他的妈妈住在离墓地很近[+的地方] — 住在+Place
- her past correction (specific_noun_choice, sim 0.651): 妈妈认为他们[拿东西→拿了墓地的东西] — “东西” is too general and vague
- cards: modal_and_control_verb_complements, location_with_zai
- **decision: drop** 因为→因为 (other) — 不是因为……而是因为…… is a valid paired structure.

**mengmu_samples#10 P6** 住【^】离墓地太近
- proposed by the AI checker: 住[+得]离墓地太近
- proposed by the correction model: 住[+得]离墓地太近
- her past correction (location_with_zai, sim 0.834): 他[离墓地住很近→住在离墓地很近的地方]
- her past correction (demonstrative_reference, sim 0.748): [小房子→这个小房子]离一个墓地不太远 — otherwise unclear which house
- her past correction (redundant_words, sim 0.63): [-他们]在墓地住 — redundant
- cards: location_with_zai, demonstrative_reference
- **decision: keep** 住离墓地太近→住在离墓地太近的地方 (location_with_zai) — 住 needs a clear 在-place construction.

**mengmu_samples#10 P7** 【害得】孟子的心气
- proposed by the AI checker: [害得→伤了]孟子的心气
- proposed by the correction model: [+会伤]害得孟子的心气
- proposed by the correction model: 害[-得]孟子的心气
- her past correction (haide_harmful_result, sim 0.826): 害得[-对]孟子有不好的影响 — 害得+Sb.+V.
- her past correction (haide_harmful_result, sim 0.793): 害得对孟子[有→受到了]不好的影响 — 害得+Sb.+V.
- her past correction (haide_harmful_result, sim 0.789): 觉得害得孟子的身体[+不好] — 害得+harmful result
- cards: haide_harmful_result
- **decision: keep** 害得孟子的心气→害得孟子的心气不好 (haide_harmful_result) — 害得 requires a harmful result.

