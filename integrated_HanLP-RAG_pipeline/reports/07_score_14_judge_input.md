# Step 7 report: scoring 14_judge_input

Finder: LLM run 1 + GEC + teacher finder (before judging) (-), prompt -, 1 run(s) in total.
Answer key: 267 teacher error edits + 20 comment edits on 20 test stories (1 edits excluded: unplaceable/unplaced or rejected in review (0 items rejected)).

## Recall: how many of the teacher's corrections the finder points at

| | Found |
|---|---|
| run 1 | 186/267 (70%) |
| average of one run | 186.0/267 (70%) |
| any of the 1 runs (union) | 186/267 (70%) |
| teacher comment edits (problem pointed at) | 14/20 (70%) |

Of the teacher edits found, the finder proposed **the same correction** for 64/186 (34%).

## Stability: in how many runs each teacher correction was found

| Found in | Teacher edits |
|---|---|
| 1 of 1 runs | 186 |
| 0 of 1 runs | 81 |

Edits found in some runs but not all (0) are the 'caught at random' problem in numbers.

## Recall by kind of edit

| Kind | Found (union) |
|---|---|
| insert | 31/48 (65%) |
| delete | 37/65 (57%) |
| replace | 118/154 (77%) |
| mengmu_san_qian | 75/114 (66%) |
| shennong_chang_baicao | 111/153 (73%) |

## Candidates: how many point at something the teacher corrected

| | Candidates | Match a teacher edit | Match nothing she marked |
|---|---|---|---|
| run 1 | 510 | 325/510 (64%) | 185 |

High-confidence candidates matching a teacher edit: 312/484 (64%); low-confidence: 13/26 (50%).
Candidates that could not be located: 0.

Candidate types: gec 205 (63% match), grammar 76 (80% match), word_choice 68 (57% match), aspect 39 (76% match), zero_redundant_pronoun 18 (27% match), first_mention_introduction 18 (61% match), perception_look_see 14 (50% match), reference 13 (61% match), location_with_zai 13 (46% match), connector 11 (54% match), other 10 (30% match), word_class_choice 7 (85% match), other_vs_additional 5 (80% match), search_find 2 (50% match), no_le_mental_state 2 (50% match), no_le_speaking_word 2 (100% match), loose_clause_connection 2 (0% match), numeral_measure_word_order 1 (0% match), redundant_words 1 (100% match), zhe_durative 1 (100% match), resultative_complements 1 (100% match), no_le_with_mei 1 (100% match)

## Teacher corrections no run found (81)

- mengmu_samples#4: [孩子→孟子]才五岁就每天在墓地祭拜了 — 孩子is vague and unclear
- mengmu_samples#4: 不是[+常常有]人吵架
- mengmu_samples#4: 孟子和妈妈[-要]又一个次搬了家 — “要” is for future plan/desire, this already occurred
- mengmu_samples#4: 他的学习和[-他的]旅行经验很重要
- mengmu_samples#4: 他成为很有名的[哲人→哲学家]
- mengmu_samples#4: [-他]是大人的时候
- mengmu_samples#10: 害得[孟子的心气→孟子受到不好的影响] — 害得Sb. + V.
- mengmu_samples#12: [古代，→在古代，]孟子跟孟母住在墓地的旁边
- mengmu_samples#12: [从早到晚→都]很吵
- mengmu_samples#12: 害得孟母[+不能出去工作，只好]只好一直陪孟子 — “害得“ + harmful result, 一直陪孟子itself is not harmful
- mengmu_samples#12: 住在商店的旁边不是适合孟子[+的环境]
- mengmu_samples#18: 而且害得孟子的学习[+不好] — 害得 + harmful result
- mengmu_samples#18: 而是搬到了孟子老师[的家→家里]
- mengmu_samples#18: [以后→后来]孟子成为了中国有名的哲学家 — Time+以后
- mengmu_samples#25: 这是[+一个]古代的故事
- mengmu_samples#25: [从他的家到→他的家离]墓地很近
- mengmu_samples#25: 他很聪明[-的人]
- mengmu_samples#32: 她[恐怕→怕]儿子的童年不会幸福 — 恐怕usually does not take Subj. except 我
- mengmu_samples#32: 所以她会一直搬家[-才能]找到质量好的教育
- mengmu_samples#32: 所以她会一直搬家才能[找到质量好的教育→想要让孟子受到良好的教育]
- mengmu_samples#32: 但是孟子老是跟这些卖东西的人[-常常]玩儿 — redundant with老是
- mengmu_samples#32: 因为她恐怕儿子会成为跟他们很像[+的人] — 成为+ noun
- mengmu_samples#32: 你不是当[数学家→商人] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#32: 在他们[+的]第三个家
- mengmu_samples#32: 孟子学了[-怎么祭拜] — wrong information, it’s not about learning to offer sacrifices
- mengmu_samples#33: [-因为]他说我们老是搬家
- mengmu_samples#39: 他的同学们老是[对→跟]他开玩笑了
- mengmu_samples#39: 看过很多政治文章[-对他]害得
- mengmu_samples#39: [-他]开始能解决问题 — redundant
- mengmu_samples#45: [但是→这个]城市有才两个学校
- mengmu_samples#45: 他的妈妈[-不是不喜欢他们的城市] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#45: [-他们]从早到晚走路
- mengmu_samples#45: [+因为]他们从早到晚走路
- mengmu_samples#45: [+所以]孟子一直抱怨
- mengmu_samples#45: 跟老师孟子[学→学习]最重要的文学
- mengmu_samples#45: 跟老师孟子学[-最重要的]文学
- mengmu_samples#47: [她→孟子的妈妈]望子成龙 — otherwise the references are confusing
- mengmu_samples#47: 所以[-孟子的妈妈]安排他的生活 — otherwise the references are confusing
- mengmu_samples#47: 妈妈[教→教了]孟子很多技能 — 了completed
- shennong_samples#4: 就[写了→写下了]这个植物对你有没有好处
- shennong_samples#4: 会[-来]跟他的朋友聊到他吃的植物了
- shennong_samples#4: 一个灵芝和一个男人正好[在→过来，看到]我的旁边 — “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two
- shennong_samples#4: 一个灵芝和一个男人正好在我的旁边[+长着一个灵芝] — “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two
- shennong_samples#4: [你得小心吃植物→吃植物得小心]
- shennong_samples#4: 因为有的植物[-对你]的健康有坏处
- shennong_samples#8: [以后→后来] — Time+以后
- shennong_samples#8: 神农告诉[别人→人们]一些植物能吃 — “别(的)” is for “a different type”, and “all else except the spoken one”
- shennong_samples#12: 神农写他的[主意→发现]
- shennong_samples#12: [别人→另外一个人]看到他 — “别(的)” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- shennong_samples#12: [+也]会告诉他的朋友哪一个植物能不能吃
- shennong_samples#18: 你[帮→做]得真好
- shennong_samples#18: 你帮得[真好→很好]
- shennong_samples#19: 凉山很大[-的山]
- shennong_samples#19: [-你的]头发疼死
- shennong_samples#19: [这→这种]冰茶是药
- shennong_samples#19: 灵芝药的夹竹桃他[吃完了→吃了]
- shennong_samples#19: [-也]写一个课文的植物
- shennong_samples#26: 神农[-在古代]每一天看到了别的小镇人生病还是不舒服 — it implies that 神农can travel between 古代 and 现代modern times
- shennong_samples#26: 但是他的旅程[-有的时候]特别是危险
- shennong_samples#26: 一个爬山的男人正好看到神农[-的麻烦]
- shennong_samples#26: 你认为神农的故事真的吗？这就要看你相信[+不相信]中药对身体有好处
- shennong_samples#26: 你认为神农的故事真的吗？这就要看你相信中药对身体有好处[+了]
- shennong_samples#33: [人→人们]不知道他们能吃什么植物
- shennong_samples#33: 让肚子[-感觉]又暖和又清楚
- shennong_samples#33: 这就要看你的口味[+了]
- shennong_samples#33: [-他发现这个口味] — since it has no clear relationship with previous or following clauses
- shennong_samples#33: 一百岁[+的]时候
- shennong_samples#35: 他们吃[+了]很多植物对药 — 了completed
- shennong_samples#35: 但是我觉得他们的吃的植物[-，]让他们病人
- shennong_samples#35: 他们可以吃对药[+这样，]
- shennong_samples#35: 他不知道如果[这把花→这种花]对你的身体好
- shennong_samples#35: 他找到了[别的花→另外一种花] — “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- shennong_samples#35: [-比方说，]他会觉得更健康 — 比方说is used to express “for example”, delete it
- shennong_samples#35: 他[可以再走→又可以走了]
- shennong_samples#42: [原来→结果]他想错了 — “原来” is to explain the reason while “结果” is to describe an unexpected result
- shennong_samples#42: [-他]没有病 — redundant
- shennong_samples#49: 有很多人[吃植物以后→吃了植物以后]就吃坏肚子了 — 了completed
- shennong_samples#49: 不会吃他[喜欢→到好吃]的植物
- shennong_samples#49: 不会吃[-他]喜欢的植物
- shennong_samples#49: 可是夹竹桃的毒[很重→很强]
- shennong_samples#49: 他[吃→吃了]灵芝以后就觉得很好 — 了completed

## Candidates matching nothing the teacher marked (177 distinct; first 60)

Not necessarily wrong: these are for the teacher to judge.

- mengmu_samples#10 (high, numeral_measure_word_order): 孟子五岁[-的]时候 — Num. + MW. + N., no 的
- mengmu_samples#10 (high, gec): 跟妈妈搬家[+了] — model rewrite: 孟子五岁的时候，跟妈妈搬家了。
- mengmu_samples#10 (high, gec): 而是[-因为]妈妈认为他们的家离墓地太近 — model rewrite: 他们搬家不是因为孟子玩得太多，而是妈妈认为他们的家离墓地太近。
- mengmu_samples#10 (high, gec): 害[-得]孟子的心气 — model rewrite: 妈妈认为，住得离墓地太近，会伤害孟子的心气。
- mengmu_samples#10 (high, first_mention_introduction): 孟子和⟦孟母⟧搬到子思老师的家 — first appearance of 孟母: briefly introduce who this is
- mengmu_samples#10 (high, gec): 孟子和孟母搬到子思老师的家[-，跟子思老师]住 — model rewrite: 孟子和孟母搬到子思老师的家住。
- mengmu_samples#10 (high, perception_look_see): 就是[看→看到]哲学书 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- mengmu_samples#10 (high, zero_redundant_pronoun): 难怪[-他]成为很有名的哲学家 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#10 (high, aspect): 难怪他成为[+了]很有名的哲学家 — becoming a philosopher is a completed later event
- mengmu_samples#12 (high, first_mention_introduction): 孟子跟⟦孟母⟧住在墓地的旁边 — first appearance of 孟母: briefly introduce who this is
- mengmu_samples#12 (high, gec): 住在墓地的旁边[+会]影响孟子 — model rewrite: 可是孟母注意到，住在墓地的旁边会影响孟子。
- mengmu_samples#12 (high, gec): 害得孟母只好一直陪[+着]孟子 — model rewrite: 害得孟母只好一直陪着孟子。
- mengmu_samples#12 (high, grammar): 住在商店的旁边[不是适合→不但不适合]孟子 — 适合 takes 不, and this needs the paired 不但…而且 structure
- mengmu_samples#12 (high, connector): [而是→而且]让他觉得很伤心 — 不但 should pair with 而且, not 而是
- mengmu_samples#12 (high, grammar): 才五岁[+时]孟子开始学哲学 — a temporal phrase needs 时 here
- mengmu_samples#12 (high, gec): 他[+会]成为中国的一个非常有名的哲学家 — model rewrite: 将来，他会成为中国的一个非常有名的哲学家。
- mengmu_samples#18 (high, gec): [+所以]他们一直在哭 — model rewrite: 因为人们在祭拜，所以他们一直在哭。
- mengmu_samples#18 (high, word_choice): 而且[害得→影响了]孟子的学习 — 害得 needs a following result clause; 影响了 fits a noun object.
- mengmu_samples#18 (high, gec): 而且害得孟子[-的]学习 — model rewrite: 孟子和孟子的妈妈住在这里才一个星期就觉得受不了了，而且害得孟子学习。
- mengmu_samples#18 (high, word_choice): 孟子的妈妈觉得孟子[取得→接受]良好的教育是很重要的 — 取得 does not collocate with 教育; one receives education
- mengmu_samples#18 (high, gec): 孟子的妈妈觉得孟子[取得→受到]良好的教育是很重要的 — model rewrite: 孟子的妈妈觉得孟子受到良好的教育是很重要的，所以孟子妈妈认为这样的地方对儿子不太好，就打算让孟子搬家。
- mengmu_samples#18 (high, gec): 所以孟子的妈妈认为这样的地方对儿子[-的教育]不太好 — model rewrite: 孟子的妈妈觉得孟子受到良好的教育是很重要的，所以孟子妈妈认为这样的地方对儿子不太好，就打算让孟子搬家。
- mengmu_samples#18 (high, gec): 就打算[跟→让]孟子搬家 — model rewrite: 孟子的妈妈觉得孟子受到良好的教育是很重要的，所以孟子妈妈认为这样的地方对儿子不太好，就打算让孟子搬家。
- mengmu_samples#18 (high, gec): 孟子的妈妈[+不是]带孟子不是搬到城市 — model rewrite: 孟子的妈妈不是带孟子搬到城市，而是搬到了孟子老师的家。
- mengmu_samples#18 (high, grammar): 孟子的妈妈带孟子[不是→没有]搬到城市 — completed negative action needs 没有 rather than 不是
- mengmu_samples#18 (high, gec): 孟子的妈妈带孟子[-不是]搬到城市 — model rewrite: 孟子的妈妈不是带孟子搬到城市，而是搬到了孟子老师的家。
- mengmu_samples#18 (high, location_with_zai): 孟子的妈妈不是[待在家里就是→在家里就是待]编织衣服赚钱 — 在 + Place comes before the action: 在Place + V.
- mengmu_samples#18 (low, word_choice): 孟子的妈妈不是待在家里就是[编织衣服→织布]赚钱 — 织布 is the usual activity meant here; 编织衣服 is unnatural in this context
- mengmu_samples#25 (high, grammar): 所以他每天老是从早到晚[去→在]墓地跟朋友们玩玩儿 — duration takes place at the cemetery
- mengmu_samples#25 (high, location_with_zai): 他的妈妈[觉得在墓地→在墓地觉得]玩儿 — 在 + Place comes before the action: 在Place + V.
- mengmu_samples#25 (high, grammar): 他[+是个]很聪明的人 — a noun predicate needs 是个 here
- mengmu_samples#25 (high, gec): 他[+是]很聪明的人 — model rewrite: 他是很聪明的人，难怪他成为有名的人。
- mengmu_samples#25 (high, zero_redundant_pronoun): 难怪[-他]成为有名的人 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#32 (high, gec): 有一天孟子去[-了]墓地玩儿 — model rewrite: 有一天孟子去墓地玩儿，但是他妈妈觉得这是不合适让孩子玩的地方，所以她决定他们会搬家找更好的。
- mengmu_samples#32 (high, grammar): 而且[住在这儿→这儿的]教育不太好 — the location should modify 教育 with 的
- mengmu_samples#32 (high, zero_redundant_pronoun): 所以[-她]会一直搬家才能找到质量好的教育 — 她 repeats the subject of the clause before: zero form
- mengmu_samples#32 (high, aspect): 他们住才一月就又搬家[+了] — the completed move needs sentence-final 了.
- mengmu_samples#32 (high, other): 但是孟子[-老是]跟这些卖东西的人常常玩儿 — 老是 and 常常 are redundant together.
- mengmu_samples#32 (high, word_choice): 因为她恐怕儿子会[成为→变得]跟他们很像 — 变得 is needed before an adjective phrase such as 很像.
- mengmu_samples#32 (high, gec): 因为她恐怕儿子会[-成为]跟他们很像 — model rewrite: 但是孟子老是跟这些卖东西的人常常玩儿，害得妈妈着急得很，因为她担心儿子会跟他们很像。
- mengmu_samples#32 (low, grammar): 在他们第三个家[+里] — a modified 家 usually needs 里 for a location
- mengmu_samples#33 (high, word_choice): 很多墓地[得→需要]我祭拜 — 得 is not natural in this statement
- mengmu_samples#33 (high, gec): 很多墓地[+都]得我祭拜 — model rewrite: 他妈妈说，从早到晚，我一直祭拜，很多墓地都得我祭拜。
- mengmu_samples#33 (high, zero_redundant_pronoun): 很多墓地得[-我]祭拜 — 我 repeats the subject of the clause before: zero form
- mengmu_samples#33 (high, word_choice): 所以我们得[去→搬到]很多不同的地方 — moving house requires 搬到, not 去
- mengmu_samples#33 (high, gec): 每次搬家孟子[也→都]觉得新的地方不是太热就是太冷 — model rewrite: 每次搬家孟子都觉得新的地方不是太热就是太冷，不是大就是小。
- mengmu_samples#33 (high, gec): 不是[-太]大就是太小 — model rewrite: 每次搬家孟子都觉得新的地方不是太热就是太冷，不是大就是小。
- mengmu_samples#33 (high, gec): 不是太大就是[-太]小 — model rewrite: 每次搬家孟子都觉得新的地方不是太热就是太冷，不是大就是小。
- mengmu_samples#33 (high, zero_redundant_pronoun): 所以[-他]祭拜不是想帮妈妈工作 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#33 (high, gec): 而是[+因为]他很喜欢画画 — model rewrite: 他画画很厉害，他越来越喜欢祭拜，所以他祭拜不是想帮妈妈工作，而是因为他很喜欢画画。
- mengmu_samples#33 (high, zero_redundant_pronoun): 而是[-他]很喜欢画画 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#33 (high, word_choice): 而是他很喜欢[画画→祭拜] — it should match the stated reason for worshipping
- mengmu_samples#33 (high, gec): 孟子成为[+了]很著名的古代画家 — model rewrite: 孟子成为了很著名的古代画家。
- mengmu_samples#39 (high, gec): 因为每天只[+是]祭拜 — model rewrite: 虽然他没有朋友，因为每天只是祭拜。
- mengmu_samples#39 (high, gec): 成为[+了]一个哲学家 — model rewrite: 孟子才十一岁，就成为了一个哲学家。
- mengmu_samples#39 (high, connector): [而是→而要]学政治 — 不要 is paired with 而要
- mengmu_samples#39 (high, gec): 因为如果你懂政治[+的话] — model rewrite: 他常常建议你不要学金融，而是学政治，因为如果你懂政治的话，你会得到高薪。
- mengmu_samples#4 (high, first_mention_introduction): 孟子和⟦孟母⟧住了在靠墓地的家 — first appearance of 孟母: briefly introduce who this is
- mengmu_samples#4 (high, aspect): 孩子才五岁就每天在墓地祭拜[-了] — a habitual daily action does not take sentence-final 了 here.
- mengmu_samples#4 (low, reference): 在[那个城市→他们住的城市] — no city has been introduced for 那个城市 to refer to.
