# Step 7 report: scoring 14_judge

Finder: gpt-5.6-terra judge over LLM run 1 + GEC + teacher finder (medium), prompt 04f94e47e8, 1 run(s) in total.
Answer key: 267 teacher error edits + 20 comment edits on 20 test stories (1 edits excluded: unplaceable/unplaced or rejected in review (0 items rejected)).

## Recall: how many of the teacher's corrections the finder points at

| | Found |
|---|---|
| run 1 | 154/267 (58%) |
| average of one run | 154.0/267 (58%) |
| any of the 1 runs (union) | 154/267 (58%) |
| teacher comment edits (problem pointed at) | 13/20 (65%) |

Of the teacher edits found, the finder proposed **the same correction** for 48/154 (31%).

## Stability: in how many runs each teacher correction was found

| Found in | Teacher edits |
|---|---|
| 1 of 1 runs | 154 |
| 0 of 1 runs | 113 |

Edits found in some runs but not all (0) are the 'caught at random' problem in numbers.

## Recall by kind of edit

| Kind | Found (union) |
|---|---|
| insert | 25/48 (52%) |
| delete | 33/65 (51%) |
| replace | 96/154 (62%) |
| mengmu_san_qian | 60/114 (53%) |
| shennong_chang_baicao | 94/153 (61%) |

## Candidates: how many point at something the teacher corrected

| | Candidates | Match a teacher edit | Match nothing she marked |
|---|---|---|---|
| run 1 | 221 | 163/221 (74%) | 58 |

High-confidence candidates matching a teacher edit: 161/215 (75%); low-confidence: 2/6 (33%).
Candidates that could not be located: 0.

Candidate types: other 76 (78% match), le_completed 23 (60% match), zero_redundant_pronoun 20 (35% match), collocation_selection 14 (64% match), first_mention_introduction 13 (84% match), word_class_choice 10 (80% match), fixed_expressions 7 (85% match), near_synonym_precision 5 (60% match), modifier_de_structure 5 (100% match), location_with_zai 4 (100% match), haide_harmful_result 4 (75% match), verb_object_valency 4 (100% match), perception_look_see 4 (100% match), not_but_refutation 3 (66% match), other_vs_additional 3 (66% match), measure_word_choice 3 (66% match), no_le_mental_state 2 (50% match), no_le_speaking_word 2 (100% match), incorrect_story_information 2 (100% match), directional_complements 2 (100% match), modal_and_control_verb_complements 2 (100% match), search_find 2 (50% match), question_patterns 2 (100% match), specific_noun_choice 2 (50% match), numeral_measure_word_order 1 (0% match), adversative_connector 1 (100% match), conditional_jiu 1 (100% match), time_sequence_markers 1 (100% match), addition_repetition_connectors 1 (100% match), no_le_routine_state 1 (100% match), no_le_with_mei 1 (100% match)

## Teacher corrections no run found (113)

- mengmu_samples#4: [古代的时候→在古代]
- mengmu_samples#4: [孩子→孟子]才五岁就每天在墓地祭拜了 — 孩子is vague and unclear
- mengmu_samples#4: 不是[+常常有]人吵架
- mengmu_samples#4: 他的学习和[-他的]旅行经验很重要
- mengmu_samples#4: 他成为很有名的[哲人→哲学家]
- mengmu_samples#10: 孟子[从五岁一直→从五岁开始]学哲学
- mengmu_samples#12: [古代，→在古代，]孟子跟孟母住在墓地的旁边
- mengmu_samples#12: [从早到晚→都]很吵
- mengmu_samples#12: 害得孟母[+不能出去工作，只好]只好一直陪孟子 — “害得“ + harmful result, 一直陪孟子itself is not harmful
- mengmu_samples#12: 住在商店的旁边不是适合孟子[+的环境]
- mengmu_samples#18: [古代的时候→在古代]
- mengmu_samples#18: 而且害得孟子的学习[+不好] — 害得 + harmful result
- mengmu_samples#18: 所以[孟子的妈妈→她]认为这样的地方对儿子的教育不太好 — replace孟子的妈妈with她
- mengmu_samples#18: 而是搬到了孟子老师[的家→家里]
- mengmu_samples#18: [以后→后来]孟子成为了中国有名的哲学家 — Time+以后
- mengmu_samples#25: 这是[+一个]古代的故事
- mengmu_samples#25: [从他的家到→他的家离]墓地很近
- mengmu_samples#25: 所以他每天[-老是]从早到晚去墓地跟朋友们玩玩儿
- mengmu_samples#25: 所以他每天老是从早到晚去墓地跟朋友们[玩玩儿→玩儿] — V.V. is used to make requests or plans
- mengmu_samples#25: 可是每天不是写字就是帮妈妈[-的]工作 — 帮sb. do sth.
- mengmu_samples#25: 他很聪明[-的人]
- mengmu_samples#32: 所以她决定了他们会[搬家找更好的地方→搬家到更好的地方]
- mengmu_samples#32: 她[恐怕→怕]儿子的童年不会幸福 — 恐怕usually does not take Subj. except 我
- mengmu_samples#32: 所以她会一直搬家[-才能]找到质量好的教育
- mengmu_samples#32: 所以她会一直搬家才能[找到质量好的教育→想要让孟子受到良好的教育]
- mengmu_samples#32: 但是孟子老是跟这些卖东西的人[-常常]玩儿 — redundant with老是
- mengmu_samples#32: 因为她[恐怕→怕/担心]儿子会成为跟他们很像 — 恐怕usually does not take Subj. except 我
- mengmu_samples#32: 因为她恐怕儿子会成为跟他们很像[+的人] — 成为+ noun
- mengmu_samples#32: 你不是当[数学家→商人] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#32: 而是当哲学家[-，不能当卖东西的人] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#32: 在他们[+的]第三个家
- mengmu_samples#32: 孟子[学了→学会了/学习了]怎么祭拜
- mengmu_samples#32: 孟子学了[-怎么祭拜] — wrong information, it’s not about learning to offer sacrifices
- mengmu_samples#32: [他难怪→难怪后来他]成为有名的哲学家
- mengmu_samples#33: [-因为]他说我们老是搬家
- mengmu_samples#33: 可是[他六岁→才六岁]
- mengmu_samples#39: [古代的时候人→在古代，人们]觉得祭拜非常重要 — “人“ is too general and too vague, and does not stand alone
- mengmu_samples#39: 他的同学们老是[对→跟]他开玩笑了
- mengmu_samples#39: 孟子妈妈看了他的同学们对孟子[+有]不好的影响
- mengmu_samples#39: 所以[-孟子和孟子妈妈]搬家了 — redundant
- mengmu_samples#39: 看过很多政治文章[-对他]害得
- mengmu_samples#39: [-他]开始能解决问题 — redundant
- mengmu_samples#45: [古代的时候→在古代]
- mengmu_samples#45: [但是→这个]城市有才两个学校
- mengmu_samples#45: 他的妈妈[-不是不喜欢他们的城市] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#45: [-他们]从早到晚走路
- mengmu_samples#45: [+因为]他们从早到晚走路
- mengmu_samples#45: [+所以]孟子一直抱怨
- mengmu_samples#45: [他难怪抱怨→难怪他抱怨] — 难怪 + sentence
- mengmu_samples#45: 跟老师孟子[学→学习]最重要的文学
- mengmu_samples#45: 跟老师孟子学[-最重要的]文学
- mengmu_samples#47: [她→孟子的妈妈]望子成龙 — otherwise the references are confusing
- mengmu_samples#47: 所以[-孟子的妈妈]安排他的生活 — otherwise the references are confusing
- mengmu_samples#47: 妈妈[教→教了]孟子很多技能 — 了completed
- shennong_samples#4: 就[写了→写下了]这个植物对你有没有好处
- shennong_samples#4: 会[-来]跟他的朋友聊到他吃的植物了
- shennong_samples#4: [-一个灵芝和]一个男人正好在我的旁边 — “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two
- shennong_samples#4: 一个灵芝和一个男人正好[在→过来，看到]我的旁边 — “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two
- shennong_samples#4: 一个灵芝和一个男人正好在我的旁边[+长着一个灵芝] — “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two
- shennong_samples#4: [你得小心吃植物→吃植物得小心]
- shennong_samples#4: 因为有的植物[-对你]的健康有坏处
- shennong_samples#8: 神农想帮[别人→他们] — “别(的)” is for “a different type”, and “all else except the spoken one”
- shennong_samples#8: [以后→后来] — Time+以后
- shennong_samples#8: 神农告诉[别人→人们]一些植物能吃 — “别(的)” is for “a different type”, and “all else except the spoken one”
- shennong_samples#8: 神农告诉别人[一些植物能吃，一些植物不能吃→哪些植物能吃，哪些植物不能吃]
- shennong_samples#12: 神农写他的[主意→发现]
- shennong_samples#12: [别人→另外一个人]看到他 — “别(的)” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- shennong_samples#12: [+也]会告诉他的朋友哪一个植物能不能吃
- shennong_samples#18: 他们去[+了]很多不一样的地方 — 了completed
- shennong_samples#18: 你[帮→做]得真好
- shennong_samples#18: 你帮得[真好→很好]
- shennong_samples#19: 凉山很大[-的山]
- shennong_samples#19: 这也[+能]找植物
- shennong_samples#19: 这也找[+到]植物
- shennong_samples#19: 他找到[+一种]黄色的花 — “黄色的花“too general and too vague
- shennong_samples#19: [-你的]头发疼死
- shennong_samples#19: [这→这种]冰茶是药
- shennong_samples#19: 灵芝药的夹竹桃他[吃完了→吃了]
- shennong_samples#19: [-也]写一个课文的植物
- shennong_samples#26: 有一个[老男人→老人]叫神农 — “老男人“ has negative meaning
- shennong_samples#26: 神农[-在古代]每一天看到了别的小镇人生病还是不舒服 — it implies that 神农can travel between 古代 and 现代modern times
- shennong_samples#26: 他一次试一试有些植物的[叶→叶子]
- shennong_samples#26: 煮这些[叶→叶子]以后
- shennong_samples#26: 但是他的旅程[-有的时候]特别是危险
- shennong_samples#26: 一个爬山的男人正好看到神农[-的麻烦]
- shennong_samples#26: 你认为神农的故事真的吗？这就要看你相信[+不相信]中药对身体有好处
- shennong_samples#26: 你认为神农的故事真的吗？这就要看你相信中药对身体有好处[+了]
- shennong_samples#33: [人→人们]不知道他们能吃什么植物
- shennong_samples#33: 让肚子[-感觉]又暖和又清楚
- shennong_samples#33: 这就要看你的口味[+了]
- shennong_samples#33: [-他发现这个口味] — since it has no clear relationship with previous or following clauses
- shennong_samples#35: 他们吃[+了]很多植物对药 — 了completed
- shennong_samples#35: 但是我觉得他们的吃的植物[-，]让他们病人
- shennong_samples#35: 他们可以吃对药[+这样，]
- shennong_samples#35: 他不知道如果[这把花→这种花]对你的身体好
- shennong_samples#35: 他找到了[别的花→另外一种花] — “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- shennong_samples#35: [别的人→另外一个人]给了神农一个灵芝 — “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- shennong_samples#35: 这个植物可以让[神农更好→身体更好]
- shennong_samples#35: [-比方说，]他会觉得更健康 — 比方说is used to express “for example”, delete it
- shennong_samples#35: 他[可以再走→又可以走了]
- shennong_samples#42: 一看[别的人→病人]就想帮助他们 — “别的” is for “a different type”, and “all else except the spoken one”
- shennong_samples#42: [原来→结果]他想错了 — “原来” is to explain the reason while “结果” is to describe an unexpected result
- shennong_samples#42: [-他]没有病 — redundant
- shennong_samples#42: 一回家就告诉[别人→家人]
- shennong_samples#42: 他找到药以后[-他]写下怎么做药在书上 — redundant
- shennong_samples#42: [那红灵芝→这样]对身体好处
- shennong_samples#49: 有很多人[吃植物以后→吃了植物以后]就吃坏肚子了 — 了completed
- shennong_samples#49: 他希望别人也可以吃[+到]好吃的植物 — with result
- shennong_samples#49: [+就]不会吃他喜欢的植物
- shennong_samples#49: 不会吃他[喜欢→到好吃]的植物
- shennong_samples#49: 不会吃[-他]喜欢的植物
- shennong_samples#49: 可是夹竹桃的毒[很重→很强]
- shennong_samples#49: 他[吃→吃了]灵芝以后就觉得很好 — 了completed

## Candidates matching nothing the teacher marked (58 distinct; first 60)

Not necessarily wrong: these are for the teacher to judge.

- mengmu_samples#10 (high, numeral_measure_word_order): 孟子五岁[-的]时候 — 五岁的时候 does not take 的.
- mengmu_samples#10 (high, zero_redundant_pronoun): 难怪[-他]成为很有名的哲学家 — The subject is already clear from the close preceding clause.
- mengmu_samples#10 (high, le_completed): 难怪他成为[+了]很有名的哲学家 — Becoming a famous philosopher is a completed change of state.
- mengmu_samples#12 (high, first_mention_introduction): 孟子跟[孟母→他的妈妈]住在墓地的旁边 — introduce the mother by her relationship
- mengmu_samples#12 (high, collocation_selection): 住在商店的旁边[不是适合→不但不适合]孟子 — 适合 takes 不, and the sentence needs the paired connector.
- mengmu_samples#12 (high, other): [而是→而且]让他觉得很伤心 — 不但 should pair with 而且, not 而是.
- mengmu_samples#18 (high, haide_harmful_result): 而且[害得→影响了]孟子的学习 — 害得 needs a harmful result clause, not a noun object.
- mengmu_samples#18 (high, collocation_selection): 孟子的妈妈觉得孟子[取得→接受]良好的教育是很重要的 — 取得 does not naturally collocate with 教育.
- mengmu_samples#25 (high, other): 他[+是个]很聪明的人 — A noun predicate needs 是个 here.
- mengmu_samples#25 (low, zero_redundant_pronoun): 难怪[-他]成为有名的人 — Repeated subject can be omitted in a close continuation.
- mengmu_samples#32 (high, zero_redundant_pronoun): 所以[-她]会一直搬家才能找到质量好的教育 — The subject is already clear from the close context.
- mengmu_samples#32 (high, other): 但是孟子[-老是]跟这些卖东西的人常常玩儿 — 老是 and 常常 redundantly express frequency.
- mengmu_samples#32 (high, near_synonym_precision): 因为她恐怕儿子会[成为→变得]跟他们很像 — 成为 cannot directly take an adjective phrase.
- mengmu_samples#33 (high, zero_redundant_pronoun): 很多墓地得[-我]祭拜 — the subject is already clear from the preceding clause
- mengmu_samples#33 (high, other): 所以我们得[去→搬到]很多不同的地方 — the explanation should match the earlier claim of moving house
- mengmu_samples#33 (high, zero_redundant_pronoun): 所以[-他]祭拜不是想帮妈妈工作 — repeated subject is redundant
- mengmu_samples#33 (high, zero_redundant_pronoun): 而是[-他]很喜欢画画 — subject should not repeat after 而是
- mengmu_samples#33 (low, not_but_refutation): 而是他很喜欢[画画→祭拜] — the alternative reason should relate to worshipping
- mengmu_samples#39 (high, word_class_choice): [而是→而要]学政治 — 不要 is paired with 而要.
- mengmu_samples#4 (high, first_mention_introduction): 孟子和[孟母→他的妈妈]住了在靠墓地的家 — The mother should be introduced by her relationship.
- mengmu_samples#4 (high, other): 在[那个→一个]城市 — No city has been introduced for 那个 to refer to.
- mengmu_samples#4 (high, zero_redundant_pronoun): [-他]成为很有名的哲人 — The subject is already clear from the close preceding clause.
- mengmu_samples#4 (high, le_completed): 他成为[+了]很有名的哲人 — Becoming a philosopher is a completed change of state in the narrative.
- mengmu_samples#45 (high, other): 所以孟子老是[祭拜→模仿别人办丧事] — This contradicts the story action.
- mengmu_samples#45 (high, other): 孟子不是[祭拜→模仿别人办丧事] — This contradicts the story action.
- mengmu_samples#45 (high, le_completed): 他们搬家到[+了]有很多学校的城市 — The move is a completed narrative action.
- mengmu_samples#45 (high, le_completed): 所以他成为[+了]哲学家 — Becoming a philosopher is a completed change of state.
- mengmu_samples#47 (high, zero_redundant_pronoun): 难怪[-他]很聪明 — Repeated subject in close continuation should be omitted.
- shennong_samples#12 (high, collocation_selection): [旅行很远→走了很远]找到很多植物 — 旅行很远 is not a natural travel expression here.
- shennong_samples#12 (high, other): 旅行很远[找到→找到了]很多植物 — The completed narrative event needs 了.
- shennong_samples#12 (high, other): 神农遇到了一[个→朵]黄色的花 — 朵 is the appropriate measure word for an individual flower.
- shennong_samples#12 (high, no_le_mental_state): 发现[-了]夹竹桃有毒 — Discovery verb should not take 了 here.
- shennong_samples#12 (high, le_completed): 很快给他吃[+了]一个灵芝 — Completed narrative action needs 了.
- shennong_samples#19 (high, other): 凉山[+是一座]很大的山 — A copula and measure word are needed for the noun predicate.
- shennong_samples#19 (low, other): 这[冰→杯]茶是药 — The context calls for a cup of tea, not iced tea.
- shennong_samples#26 (high, search_find): [找了→找到了]各种各样的植物 — He later tests the plants, so the sentence gives a successful finding result.
- shennong_samples#26 (high, le_completed): 神农试[一→了]试每个植物 — The testing is a completed narrative action.
- shennong_samples#26 (high, le_completed): 他一喝就知道他发现[+了]新的茶叶 — The discovery is a completed narrative event.
- shennong_samples#33 (high, zero_redundant_pronoun): 人不知道[-他们]能吃什么植物 — The repeated generic subject is unnecessary.
- shennong_samples#33 (low, near_synonym_precision): [所以→于是]有一天 — 于是 better connects the resulting narrative action.
- shennong_samples#33 (high, collocation_selection): 神农出去[试一试→尝一尝]很多种植物 — Plants are tasted to test whether they are edible.
- shennong_samples#35 (high, collocation_selection): 他们吃很多植物[对→当]药 — Plants can be eaten 当药, not 对药.
- shennong_samples#35 (high, zero_redundant_pronoun): [-他]想把花放在茶里 — The same subject continues and need not be repeated.
- shennong_samples#35 (high, other): 神农不知道他吃不吃灵芝[或者→还是]夹竹桃 — 间接选择问句用还是。
- shennong_samples#35 (high, le_completed): 现在他觉得更好[+了] — 了 marks the resulting change of state.
- shennong_samples#35 (high, other): 他可以[用对药→用来做药] — 用对药 does not express using plants to make medicine.
- shennong_samples#4 (high, fixed_expressions): [古代的时候→在古代] — Use the established time expression.
- shennong_samples#4 (high, zero_redundant_pronoun): 所以[-神农]去了吃每种植物 — The subject is already clear.
- shennong_samples#4 (high, other_vs_additional): [一个别的人→另外一个人]问神农 — Another additional person should be 另外一个人.
- shennong_samples#42 (high, zero_redundant_pronoun): [-他]不知道什么东西能做药 — The subject is already clear from the close preceding clause.
- shennong_samples#42 (high, other): 快给他[一种→一个]红的灵芝 — He gives one lingzhi, not a type of lingzhi.
- shennong_samples#42 (high, le_completed): 他怎么忘记了？他把灵芝放[+了]在包里 — completed narrative action needs 了
- shennong_samples#49 (high, other): 吃了很多[样子→种]的植物 — “样子” does not mean kinds of plants here.
- shennong_samples#49 (high, other): 他把所有的植物[+的名字]写下来了 — One writes down the plants’ names, not the plants themselves.
- shennong_samples#49 (high, measure_word_choice): 可是他还没吃了一[个→种]叫夹竹桃的植物 — 夹竹桃 is a type of plant, so 种 is needed.
- shennong_samples#49 (high, zero_redundant_pronoun): 觉得[-他]快会死了 — Repeated subject is unnecessary after 觉得.
- shennong_samples#49 (high, specific_noun_choice): [不再生病→肚子不痛]了 — The established symptom is stomach pain.
- shennong_samples#49 (high, word_class_choice): 像星星的植物[是毒→有毒] — Plants are described as 有毒.
