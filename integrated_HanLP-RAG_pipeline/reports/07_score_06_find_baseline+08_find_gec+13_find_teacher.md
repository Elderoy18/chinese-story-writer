# Step 7 report: scoring 06_find_baseline+08_find_gec+13_find_teacher

Finder: gpt-5.6-terra + HillZhang/real_learner_bart_CGEC + teacher patterns + HanLP checks (medium / beam search, 5 beams / deterministic), prompt 5856d40642 / n/a / n/a, 5 run(s) in total.
Answer key: 267 teacher error edits + 20 comment edits on 20 test stories (1 edits excluded: unplaceable/unplaced or rejected in review (0 items rejected)).

## Recall: how many of the teacher's corrections the finder points at

| | Found |
|---|---|
| run 06_find_baseline:1 | 140/267 (52%) |
| run 06_find_baseline:2 | 142/267 (53%) |
| run 06_find_baseline:3 | 141/267 (53%) |
| run 08_find_gec:1 | 117/267 (44%) |
| run 13_find_teacher:1 | 33/267 (12%) |
| average of one run | 114.6/267 (43%) |
| any of the 5 runs (union) | 204/267 (76%) |
| teacher comment edits (problem pointed at) | 15/20 (75%) |

Of the teacher edits found, the finder proposed **the same correction** for 83/204 (41%).

## Stability: in how many runs each teacher correction was found

| Found in | Teacher edits |
|---|---|
| 5 of 5 runs | 6 |
| 4 of 5 runs | 75 |
| 3 of 5 runs | 48 |
| 2 of 5 runs | 24 |
| 1 of 5 runs | 51 |
| 0 of 5 runs | 63 |

Edits found in some runs but not all (198) are the 'caught at random' problem in numbers.

## Recall by kind of edit

| Kind | Found (union) |
|---|---|
| insert | 36/48 (75%) |
| delete | 44/65 (68%) |
| replace | 124/154 (81%) |
| mengmu_san_qian | 84/114 (74%) |
| shennong_chang_baicao | 120/153 (78%) |

## Candidates: how many point at something the teacher corrected

| | Candidates | Match a teacher edit | Match nothing she marked |
|---|---|---|---|
| run 06_find_baseline:1 | 217 | 147/217 (68%) | 70 |
| run 06_find_baseline:2 | 218 | 144/218 (66%) | 74 |
| run 06_find_baseline:3 | 205 | 142/205 (69%) | 63 |
| run 08_find_gec:1 | 205 | 131/205 (64%) | 74 |
| run 13_find_teacher:1 | 88 | 47/88 (53%) | 41 |

High-confidence candidates matching a teacher edit: 567/860 (66%); low-confidence: 44/73 (60%).
Candidates that could not be located: 3.

Candidate types: grammar 232 (78% match), gec 205 (63% match), word_choice 204 (62% match), aspect 114 (71% match), reference 36 (58% match), connector 32 (50% match), other 22 (27% match), zero_redundant_pronoun 18 (27% match), first_mention_introduction 18 (61% match), perception_look_see 14 (50% match), location_with_zai 13 (46% match), word_class_choice 7 (85% match), other_vs_additional 5 (80% match), search_find 2 (50% match), no_le_mental_state 2 (50% match), no_le_speaking_word 2 (100% match), loose_clause_connection 2 (0% match), numeral_measure_word_order 1 (0% match), redundant_words 1 (100% match), zhe_durative 1 (100% match), resultative_complements 1 (100% match), no_le_with_mei 1 (100% match)

## Which finder found what

| Finder | Found (all its runs) | Found ONLY by this finder |
|---|---|---|
| 06_find_baseline | 169/267 (63%) | 67 |
| 08_find_gec | 117/267 (44%) | 21 |
| 13_find_teacher | 33/267 (12%) | 10 |
| found by all finders | 9/267 (3%) | |

### Found only by 06_find_baseline (67)

- mengmu_samples#4: 他们搬了到[别一个→另外一个]城市找工作
- mengmu_samples#4: 不是[+常常有]人吵架
- mengmu_samples#4: 孟子和妈妈[-要]又一个次搬了家
- mengmu_samples#4: 孟母[找到→找到了]工作
- mengmu_samples#4: 孟子[学习馆→在学校]学了十五年
- mengmu_samples#4: 他[是大人的时候→长大以后]
- mengmu_samples#10: [装祭拜→装着祭拜的样子]
- mengmu_samples#10: 害得[孟子的心气→孟子受到不好的影响]
- mengmu_samples#12: [将来→后来]
- mengmu_samples#18: [以后→后来]孟子成为了中国有名的哲学家
- mengmu_samples#25: 所以他每天[-老是]从早到晚去墓地跟朋友们玩玩儿
- mengmu_samples#25: 他很聪明[-的人]
- mengmu_samples#32: 所以她决定了[-他们会]搬家找更好的地方
- mengmu_samples#32: 但是孟子老是跟这些卖东西的人[-常常]玩儿
- mengmu_samples#32: 你不是[+要]当数学家
- mengmu_samples#32: 而是[+要]当哲学家
- mengmu_samples#32: 在他们[+的]第三个家
- mengmu_samples#32: [他难怪→难怪后来他]成为有名的哲学家
- mengmu_samples#33: [-一天，]很久很久以前
- mengmu_samples#33: [-因为]他说我们老是搬家
- mengmu_samples#39: [-虽然]他没有朋友
- mengmu_samples#45: [他难怪抱怨→难怪他抱怨]
- mengmu_samples#45: [跟老师孟子→孟子跟老师]学最重要的文学
- mengmu_samples#45: 跟老师孟子[学→学习]最重要的文学
- shennong_samples#4: 也不知道什么植物对[-你的]身体有好处
- shennong_samples#4: 就[写了→写下了]这个植物对你有没有好处
- shennong_samples#4: 就写了这个植物[-对你]有没有好处
- shennong_samples#4: [-一个灵芝和]一个男人正好在我的旁边
- shennong_samples#12: 古代的人[-很]不知道什么植物能吃
- shennong_samples#12: [-也]什么植物不能吃
- shennong_samples#12: 吃不安全的植物对[-你的]身体有坏处
- shennong_samples#19: 他听说[-你]跟黄色的花做茶很有用
- shennong_samples#19: [-你的]头发疼死
- shennong_samples#19: [灵芝药的夹竹桃→可以做夹竹桃解药的灵芝]他吃完了
- shennong_samples#19: 也写一个[课文的→有关]植物
- shennong_samples#19: 也写一个课文的植物[+的文章]
- shennong_samples#26: 有一个[老男人→老人]叫神农
- shennong_samples#26: 神农在古代每一天看到了别的小镇人生病[还是→或者]不舒服
- shennong_samples#26: 他下一天开始爬[当地的山脉→当地的大山]
- shennong_samples#26: 他[一次→有一次]试一试有些植物的叶

### Found only by 08_find_gec (21)

- mengmu_samples#10: 住离墓地太近[+的地方]
- mengmu_samples#10: [因为孟子现在没有朋友，他老是读书→孟子现在没有朋友，因为他老是读书]
- mengmu_samples#18: 所以[孟子的妈妈→她]认为这样的地方对儿子的教育不太好
- mengmu_samples#32: 所以她决定了他们会[搬家找更好的地方→搬家到更好的地方]
- mengmu_samples#32: 因为她[恐怕→怕/担心]儿子会成为跟他们很像
- mengmu_samples#32: 而是当哲学家[-，不能当卖东西的人]
- mengmu_samples#32: 所以他们又搬家[+了]
- mengmu_samples#32: 孟子[学了→学会了/学习了]怎么祭拜
- mengmu_samples#33: 可是[他六岁→才六岁]
- mengmu_samples#39: 孟子妈妈看了他的同学们对孟子[+有]不好的影响
- mengmu_samples#39: 所以[-孟子和孟子妈妈]搬家了
- shennong_samples#8: 神农想帮[别人→他们]
- shennong_samples#8: 一些植物[毒得很→毒性强得很]
- shennong_samples#8: 神农告诉别人[一些植物能吃，一些植物不能吃→哪些植物能吃，哪些植物不能吃]
- shennong_samples#19: 这也[+能]找植物
- shennong_samples#19: 这也找[+到]植物
- shennong_samples#35: 这个植物可以让[神农更好→身体更好]
- shennong_samples#42: 什么病人[吃→吃了以后]都会觉得身体更好
- shennong_samples#42: 他找到药以后[-他]写下怎么做药在书上
- shennong_samples#49: 他希望别人也可以吃[+到]好吃的植物
- shennong_samples#49: [+就]不会吃他喜欢的植物

### Found only by 13_find_teacher (10)

- mengmu_samples#4: [古代的时候→在古代]
- mengmu_samples#18: [古代的时候→在古代]
- mengmu_samples#32: [古代的时候→那时候]
- mengmu_samples#33: [-他]越来越喜欢祭拜
- mengmu_samples#33: 他[+也]越来越喜欢祭拜
- mengmu_samples#39: [-你]会成为高薪
- mengmu_samples#45: [古代的时候→在古代]
- mengmu_samples#45: [+原来]他想他的朋友
- shennong_samples#26: 跟[别的人→其他人]分享他的发现
- shennong_samples#49: [-他]连毒都能吃

## Teacher corrections no run found (63)

- mengmu_samples#4: [孩子→孟子]才五岁就每天在墓地祭拜了 — 孩子is vague and unclear
- mengmu_samples#4: 他的学习和[-他的]旅行经验很重要
- mengmu_samples#4: 他成为很有名的[哲人→哲学家]
- mengmu_samples#4: [-他]是大人的时候
- mengmu_samples#12: [古代，→在古代，]孟子跟孟母住在墓地的旁边
- mengmu_samples#12: [从早到晚→都]很吵
- mengmu_samples#12: 害得孟母[+不能出去工作，只好]只好一直陪孟子 — “害得“ + harmful result, 一直陪孟子itself is not harmful
- mengmu_samples#12: 住在商店的旁边不是适合孟子[+的环境]
- mengmu_samples#18: 而且害得孟子的学习[+不好] — 害得 + harmful result
- mengmu_samples#18: 而是搬到了孟子老师[的家→家里]
- mengmu_samples#25: 这是[+一个]古代的故事
- mengmu_samples#25: [从他的家到→他的家离]墓地很近
- mengmu_samples#32: 她[恐怕→怕]儿子的童年不会幸福 — 恐怕usually does not take Subj. except 我
- mengmu_samples#32: 所以她会一直搬家[-才能]找到质量好的教育
- mengmu_samples#32: 所以她会一直搬家才能[找到质量好的教育→想要让孟子受到良好的教育]
- mengmu_samples#32: 因为她恐怕儿子会成为跟他们很像[+的人] — 成为+ noun
- mengmu_samples#32: 你不是当[数学家→商人] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#32: 孟子学了[-怎么祭拜] — wrong information, it’s not about learning to offer sacrifices
- mengmu_samples#39: 他的同学们老是[对→跟]他开玩笑了
- mengmu_samples#39: 看过很多政治文章[-对他]害得
- mengmu_samples#39: [-他]开始能解决问题 — redundant
- mengmu_samples#45: [但是→这个]城市有才两个学校
- mengmu_samples#45: 他的妈妈[-不是不喜欢他们的城市] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#45: [-他们]从早到晚走路
- mengmu_samples#45: [+因为]他们从早到晚走路
- mengmu_samples#45: [+所以]孟子一直抱怨
- mengmu_samples#45: 跟老师孟子学[-最重要的]文学
- mengmu_samples#47: [她→孟子的妈妈]望子成龙 — otherwise the references are confusing
- mengmu_samples#47: 所以[-孟子的妈妈]安排他的生活 — otherwise the references are confusing
- mengmu_samples#47: 妈妈[教→教了]孟子很多技能 — 了completed
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
- shennong_samples#19: [这→这种]冰茶是药
- shennong_samples#19: 灵芝药的夹竹桃他[吃完了→吃了]
- shennong_samples#19: [-也]写一个课文的植物
- shennong_samples#26: 神农[-在古代]每一天看到了别的小镇人生病还是不舒服 — it implies that 神农can travel between 古代 and 现代modern times
- shennong_samples#26: 但是他的旅程[-有的时候]特别是危险
- shennong_samples#26: 你认为神农的故事真的吗？这就要看你相信中药对身体有好处[+了]
- shennong_samples#33: [人→人们]不知道他们能吃什么植物
- shennong_samples#33: 让肚子[-感觉]又暖和又清楚
- shennong_samples#33: 这就要看你的口味[+了]
- shennong_samples#35: 他们吃[+了]很多植物对药 — 了completed
- shennong_samples#35: 但是我觉得他们的吃的植物[-，]让他们病人
- shennong_samples#35: 他找到了[别的花→另外一种花] — “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- shennong_samples#35: [-比方说，]他会觉得更健康 — 比方说is used to express “for example”, delete it
- shennong_samples#35: 他[可以再走→又可以走了]
- shennong_samples#42: [原来→结果]他想错了 — “原来” is to explain the reason while “结果” is to describe an unexpected result
- shennong_samples#42: [-他]没有病 — redundant
- shennong_samples#49: 有很多人[吃植物以后→吃了植物以后]就吃坏肚子了 — 了completed
- shennong_samples#49: 不会吃他[喜欢→到好吃]的植物
- shennong_samples#49: 不会吃[-他]喜欢的植物
- shennong_samples#49: 他[吃→吃了]灵芝以后就觉得很好 — 了completed

## Candidates matching nothing the teacher marked (252 distinct; first 60)

Not necessarily wrong: these are for the teacher to judge.

- mengmu_samples#10 (high, numeral_measure_word_order): 孟子五岁[-的]时候 — Num. + MW. + N., no 的
- mengmu_samples#10 (high, aspect): 跟妈妈搬[+了]家 — a completed move needs 了
- mengmu_samples#10 (high, aspect): 跟妈妈搬家[+了] — a completed past move needs 了
- mengmu_samples#10 (high, gec): 而是[-因为]妈妈认为他们的家离墓地太近 — model rewrite: 他们搬家不是因为孟子玩得太多，而是妈妈认为他们的家离墓地太近。
- mengmu_samples#10 (high, gec): 害[-得]孟子的心气 — model rewrite: 妈妈认为，住得离墓地太近，会伤害孟子的心气。
- mengmu_samples#10 (high, first_mention_introduction): 孟子和⟦孟母⟧搬到子思老师的家 — first appearance of 孟母: briefly introduce who this is
- mengmu_samples#10 (high, gec): 孟子和孟母搬到子思老师的家[-，跟子思老师]住 — model rewrite: 孟子和孟母搬到子思老师的家住。
- mengmu_samples#10 (high, perception_look_see): 就是[看→看到]哲学书 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- mengmu_samples#10 (high, zero_redundant_pronoun): 难怪[-他]成为很有名的哲学家 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#10 (high, aspect): 难怪他成为[+了]很有名的哲学家 — becoming a philosopher is a completed later event
- mengmu_samples#12 (high, first_mention_introduction): 孟子跟⟦孟母⟧住在墓地的旁边 — first appearance of 孟母: briefly introduce who this is
- mengmu_samples#12 (high, grammar): 住在墓地的旁边[+会]影响孟子 — a living situation needs 会 before its effect
- mengmu_samples#12 (high, word_choice): 他们住在城市里的[商店→集市]的旁边 — the story location is beside a market, not one shop
- mengmu_samples#12 (high, gec): 害得孟母只好一直陪[+着]孟子 — model rewrite: 害得孟母只好一直陪着孟子。
- mengmu_samples#12 (low, connector): 孟子[-也]没有朋友 — 也 needs a clear parallel/additive reference
- mengmu_samples#12 (high, grammar): 住在商店的旁边[不是适合→不但不适合]孟子 — 适合 takes 不, and this needs the paired 不但…而且 structure
- mengmu_samples#12 (high, grammar): 住在商店的旁边不[-是]适合孟子 — 不适合, not 不是适合
- mengmu_samples#12 (high, connector): [而是→而且]让他觉得很伤心 — 不但 should pair with 而且, not 而是
- mengmu_samples#12 (high, connector): [-而是]让他觉得很伤心 — 而是 cannot introduce this result clause
- mengmu_samples#12 (high, grammar): 才五岁[+时]孟子开始学哲学 — a temporal phrase needs 时 here
- mengmu_samples#12 (high, gec): 他[+会]成为中国的一个非常有名的哲学家 — model rewrite: 将来，他会成为中国的一个非常有名的哲学家。
- mengmu_samples#18 (high, gec): [+所以]他们一直在哭 — model rewrite: 因为人们在祭拜，所以他们一直在哭。
- mengmu_samples#18 (high, word_choice): 而且[害得→影响了]孟子的学习 — 害得 needs a following result clause; 影响了 fits a noun object.
- mengmu_samples#18 (high, grammar): 而且害[得→了]孟子的学习 — 害得 needs a result complement; 害了 can take 学习 as its object.
- mengmu_samples#18 (high, gec): 而且害得孟子[-的]学习 — model rewrite: 孟子和孟子的妈妈住在这里才一个星期就觉得受不了了，而且害得孟子学习。
- mengmu_samples#18 (high, word_choice): 孟子的妈妈觉得孟子[取得→接受]良好的教育是很重要的 — 取得 does not collocate with 教育; one receives education
- mengmu_samples#18 (high, gec): 孟子的妈妈觉得孟子[取得→受到]良好的教育是很重要的 — model rewrite: 孟子的妈妈觉得孟子受到良好的教育是很重要的，所以孟子妈妈认为这样的地方对儿子不太好，就打算让孟子搬家。
- mengmu_samples#18 (high, gec): 所以孟子的妈妈认为这样的地方对儿子[-的教育]不太好 — model rewrite: 孟子的妈妈觉得孟子受到良好的教育是很重要的，所以孟子妈妈认为这样的地方对儿子不太好，就打算让孟子搬家。
- mengmu_samples#18 (high, gec): 就打算[跟→让]孟子搬家 — model rewrite: 孟子的妈妈觉得孟子受到良好的教育是很重要的，所以孟子妈妈认为这样的地方对儿子不太好，就打算让孟子搬家。
- mengmu_samples#18 (high, gec): 孟子的妈妈[+不是]带孟子不是搬到城市 — model rewrite: 孟子的妈妈不是带孟子搬到城市，而是搬到了孟子老师的家。
- mengmu_samples#18 (high, grammar): 孟子的妈妈带孟子[不是→没有]搬到城市 — completed negative action needs 没有 rather than 不是
- mengmu_samples#18 (high, grammar): 孟子的妈妈带孟子[+搬家]不是搬到城市 — a verb is needed after 带孟子 before the contrast
- mengmu_samples#18 (high, gec): 孟子的妈妈带孟子[-不是]搬到城市 — model rewrite: 孟子的妈妈不是带孟子搬到城市，而是搬到了孟子老师的家。
- mengmu_samples#18 (high, reference): 而是搬到了孟子[+的]老师的家 — 孟子的老师 means Mencius's teacher
- mengmu_samples#18 (high, location_with_zai): 孟子的妈妈不是[待在家里就是→在家里就是待]编织衣服赚钱 — 在 + Place comes before the action: 在Place + V.
- mengmu_samples#18 (low, word_choice): 孟子的妈妈不是待在家里就是[编织衣服→织布]赚钱 — 织布 is the usual activity meant here; 编织衣服 is unnatural in this context
- mengmu_samples#18 (low, word_choice): 孟子的妈妈不是待在家里就是[编织→做]衣服赚钱 — 做衣服 is the usual expression; 编织 normally needs a specific item such as 毛衣.
- mengmu_samples#25 (high, grammar): 所以他每天老是从早到晚[去→在]墓地跟朋友们玩玩儿 — duration takes place at the cemetery
- mengmu_samples#25 (high, location_with_zai): 他的妈妈[觉得在墓地→在墓地觉得]玩儿 — 在 + Place comes before the action: 在Place + V.
- mengmu_samples#25 (high, aspect): 所以他们搬家[+了] — the completed move needs 了.
- mengmu_samples#25 (high, grammar): 他[+是个]很聪明的人 — a noun predicate needs 是个 here
- mengmu_samples#25 (high, grammar): 他[很→是]聪明的人 — a noun predicate needs 是
- mengmu_samples#25 (high, gec): 他[+是]很聪明的人 — model rewrite: 他是很聪明的人，难怪他成为有名的人。
- mengmu_samples#25 (high, zero_redundant_pronoun): 难怪[-他]成为有名的人 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#25 (high, aspect): 难怪他[成为→成了]有名的人 — completed story event needs 了
- mengmu_samples#25 (high, aspect): 难怪他[成为→会成为]有名的人 — future result needs 会 in this context
- mengmu_samples#32 (high, gec): 有一天孟子去[-了]墓地玩儿 — model rewrite: 有一天孟子去墓地玩儿，但是他妈妈觉得这是不合适让孩子玩的地方，所以她决定他们会搬家找更好的。
- mengmu_samples#32 (high, grammar): 而且[住在这儿→这儿的]教育不太好 — the location should modify 教育 with 的
- mengmu_samples#32 (high, grammar): 而且[住在这儿教育→这儿的教育]不太好 — the location needs to modify 教育 with 的
- mengmu_samples#32 (high, zero_redundant_pronoun): 所以[-她]会一直搬家才能找到质量好的教育 — 她 repeats the subject of the clause before: zero form
- mengmu_samples#32 (high, aspect): 他们住才一月就又搬家[+了] — the completed move needs sentence-final 了.
- mengmu_samples#32 (high, other): 但是孟子[-老是]跟这些卖东西的人常常玩儿 — 老是 and 常常 are redundant together.
- mengmu_samples#32 (high, word_choice): 因为她恐怕儿子会[成为→变得]跟他们很像 — 变得 is needed before an adjective phrase such as 很像.
- mengmu_samples#32 (high, gec): 因为她恐怕儿子会[-成为]跟他们很像 — model rewrite: 但是孟子老是跟这些卖东西的人常常玩儿，害得妈妈着急得很，因为她担心儿子会跟他们很像。
- mengmu_samples#32 (high, reference): 她告诉了孟子：他们不是[+你的]朋友 — specifies whose friends they are not
- mengmu_samples#32 (low, grammar): 在他们第三个家[+里] — a modified 家 usually needs 里 for a location
- mengmu_samples#33 (high, grammar): [很多墓地得我祭拜→我得去很多墓地祭拜] — subject and modal 得 need to come before the verb
- mengmu_samples#33 (high, word_choice): 很多墓地[得→需要]我祭拜 — 得 is not natural in this statement
- mengmu_samples#33 (high, gec): 很多墓地[+都]得我祭拜 — model rewrite: 他妈妈说，从早到晚，我一直祭拜，很多墓地都得我祭拜。
- mengmu_samples#33 (high, zero_redundant_pronoun): 很多墓地得[-我]祭拜 — 我 repeats the subject of the clause before: zero form
