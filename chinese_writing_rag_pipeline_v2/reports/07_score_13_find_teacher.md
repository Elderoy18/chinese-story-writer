# Step 7 report: scoring 13_find_teacher

Finder: teacher patterns + HanLP checks (deterministic), prompt n/a, 1 run(s) in total.
Answer key: 267 teacher error edits + 20 comment edits on 20 test stories (1 edits excluded: unplaceable/unplaced or rejected in review (0 items rejected)).

## Recall: how many of the teacher's corrections the finder points at

| | Found |
|---|---|
| run 1 | 33/267 (12%) |
| average of one run | 33.0/267 (12%) |
| any of the 1 runs (union) | 33/267 (12%) |
| teacher comment edits (problem pointed at) | 12/20 (60%) |

Of the teacher edits found, the finder proposed **the same correction** for 12/33 (36%).

## Stability: in how many runs each teacher correction was found

| Found in | Teacher edits |
|---|---|
| 1 of 1 runs | 33 |
| 0 of 1 runs | 234 |

Edits found in some runs but not all (0) are the 'caught at random' problem in numbers.

## Recall by kind of edit

| Kind | Found (union) |
|---|---|
| insert | 4/48 (8%) |
| delete | 6/65 (9%) |
| replace | 23/154 (15%) |
| mengmu_san_qian | 16/114 (14%) |
| shennong_chang_baicao | 17/153 (11%) |

## Candidates: how many point at something the teacher corrected

| | Candidates | Match a teacher edit | Match nothing she marked |
|---|---|---|---|
| run 1 | 88 | 47/88 (53%) | 41 |

High-confidence candidates matching a teacher edit: 47/88 (53%); low-confidence: 0/0.
Candidates that could not be located: 0.

Candidate types: zero_redundant_pronoun 18 (27% match), first_mention_introduction 18 (61% match), perception_look_see 14 (50% match), location_with_zai 13 (46% match), word_class_choice 7 (85% match), other_vs_additional 5 (80% match), search_find 2 (50% match), no_le_mental_state 2 (50% match), no_le_speaking_word 2 (100% match), loose_clause_connection 2 (0% match), numeral_measure_word_order 1 (0% match), redundant_words 1 (100% match), zhe_durative 1 (100% match), resultative_complements 1 (100% match), no_le_with_mei 1 (100% match)

## Teacher corrections no run found (234)

- mengmu_samples#4: 孟子和孟母住了[在靠墓地的家→在靠近墓地的地方] — 在+Place
- mengmu_samples#4: 孟子和孟母住[-了]在靠墓地的家
- mengmu_samples#4: [孩子→孟子]才五岁就每天在墓地祭拜了 — 孩子is vague and unclear
- mengmu_samples#4: 他们[搬了到→搬到了]别一个城市找工作
- mengmu_samples#4: 他们搬了到[别一个→另外一个]城市找工作 — “别（的）” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- mengmu_samples#4: 不是[+常常有]人吵架
- mengmu_samples#4: 就是[都叫→很多人都大声说话]
- mengmu_samples#4: 孟子和妈妈[-要]又一个次搬了家 — “要” is for future plan/desire, this already occurred
- mengmu_samples#4: 孟子和妈妈要[又一个次搬了家→又搬了一次家]
- mengmu_samples#4: 孟母[找到→找到了]工作 — 了completed
- mengmu_samples#4: 孟子[学习馆→在学校]学了十五年 — 在+Place
- mengmu_samples#4: 他的学习和[-他的]旅行经验很重要
- mengmu_samples#4: 对他[+有]很多好处
- mengmu_samples#4: 他[是大人的时候→长大以后]
- mengmu_samples#4: 他成为很有名的[哲人→哲学家]
- mengmu_samples#4: [-他]是大人的时候
- mengmu_samples#10: [装祭拜→装着祭拜的样子]
- mengmu_samples#10: 住[+在]离墓地太近
- mengmu_samples#10: 住离墓地太近[+的地方]
- mengmu_samples#10: [+会]害得孟子的心气
- mengmu_samples#10: 害得[孟子的心气→孟子受到不好的影响] — 害得Sb. + V.
- mengmu_samples#10: [因为孟子现在没有朋友，他老是读书→孟子现在没有朋友，因为他老是读书]
- mengmu_samples#10: 孟子[从五岁一直→从五岁开始]学哲学
- mengmu_samples#12: [古代，→在古代，]孟子跟孟母住在墓地的旁边
- mengmu_samples#12: 可是孟母[注意→注意到] — 注意action vs.注意到result
- mengmu_samples#12: 他常常跟朋友们[祭拜玩→祭拜着玩儿] — V.着玩儿 do something just for fun
- mengmu_samples#12: 所以孟母决定[-他们会]搬家
- mengmu_samples#12: [从早到晚→都]很吵
- mengmu_samples#12: 害得孟母[+不能出去工作，只好]只好一直陪孟子 — “害得“ + harmful result, 一直陪孟子itself is not harmful
- mengmu_samples#12: 住在商店的旁边不是适合孟子[+的环境]
- mengmu_samples#12: 才五岁孟子[+就]开始学哲学 — 才Num.就V.
- mengmu_samples#12: [将来→后来] — “将来“ refers to the absolute future
- mengmu_samples#18: 而且害得孟子的学习[+不好] — 害得 + harmful result
- mengmu_samples#18: 所以[孟子的妈妈→她]认为这样的地方对儿子的教育不太好 — replace孟子的妈妈with她
- mengmu_samples#18: 而是搬到了孟子老师[的家→家里]
- mengmu_samples#18: [以后→后来]孟子成为了中国有名的哲学家 — Time+以后
- mengmu_samples#25: 这是[+一个]古代的故事
- mengmu_samples#25: [从他的家到→他的家离]墓地很近
- mengmu_samples#25: 所以他每天[-老是]从早到晚去墓地跟朋友们玩玩儿
- mengmu_samples#25: 所以他每天老是从早到晚去墓地跟朋友们[玩玩儿→玩儿] — V.V. is used to make requests or plans
- mengmu_samples#25: 害得[+孟子学习不好] — 害得 + harmful result
- mengmu_samples#25: 可是每天不是写字就是帮妈妈[-的]工作 — 帮sb. do sth.
- mengmu_samples#25: 他很聪明[-的人]
- mengmu_samples#32: 但是他妈妈觉得这[是不合适的地方让孩子玩→不是适合孩子玩的地方]
- mengmu_samples#32: 所以她决定了[-他们会]搬家找更好的地方
- mengmu_samples#32: 所以她决定了他们会[搬家找更好的地方→搬家到更好的地方]
- mengmu_samples#32: 她[恐怕→怕]儿子的童年不会幸福 — 恐怕usually does not take Subj. except 我
- mengmu_samples#32: 所以她[-会]一直搬家才能找到质量好的教育 — 会will
- mengmu_samples#32: 所以她会一直搬家[-才能]找到质量好的教育
- mengmu_samples#32: 所以她会一直搬家才能[找到质量好的教育→想要让孟子受到良好的教育]
- mengmu_samples#32: 他们[住才一月→才住了一个月]就又搬家 — 了completed
- mengmu_samples#32: 但是孟子老是跟这些卖东西的人[-常常]玩儿 — redundant with老是
- mengmu_samples#32: 因为她[恐怕→怕/担心]儿子会成为跟他们很像 — 恐怕usually does not take Subj. except 我
- mengmu_samples#32: 因为她恐怕儿子会成为跟他们很像[+的人] — 成为+ noun
- mengmu_samples#32: 你不是[+要]当数学家 — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#32: 你不是当[数学家→商人] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#32: 而是[+要]当哲学家 — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#32: 而是当哲学家[-，不能当卖东西的人] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#32: 所以他们又搬家[+了] — 了completed
- mengmu_samples#32: 在他们[+的]第三个家
- mengmu_samples#32: 孟子[学了→学会了/学习了]怎么祭拜
- mengmu_samples#32: 孟子学了[-怎么祭拜] — wrong information, it’s not about learning to offer sacrifices
- mengmu_samples#32: [他难怪→难怪后来他]成为有名的哲学家
- mengmu_samples#33: [-一天，]很久很久以前
- mengmu_samples#33: [-因为]他说我们老是搬家
- mengmu_samples#33: [在哪的地方→在哪儿]
- mengmu_samples#33: 可是[他六岁→才六岁]
- mengmu_samples#39: [-虽然]他没有朋友 — there is no “even though” meaning here
- mengmu_samples#39: 他的同学们老是[对→跟]他开玩笑了
- mengmu_samples#39: 他的同学们老是对他开玩笑[-了] — no了for routine/habit
- mengmu_samples#39: 孟子妈妈看了他的同学们对孟子[+有]不好的影响
- mengmu_samples#39: 所以[-孟子和孟子妈妈]搬家了 — redundant
- mengmu_samples#39: [+就]成为一个哲学家 — 才Num.就V.
- mengmu_samples#39: 看过很多政治文章[-对他]害得
- mengmu_samples#39: 看过很多政治文章对他[害得，他有很多问题→害得他有很多问题] — 害得Sb. + harmful result
- mengmu_samples#39: 孟子[长大，→长大以后，]他开始能解决问题
- mengmu_samples#39: [-他]开始能解决问题 — redundant
- mengmu_samples#39: 他[常常建议你不是学金融→建议人们，不要学金融]
- mengmu_samples#39: 你会[成为高薪→得到高薪] — 成为 + profession/celebrity
- mengmu_samples#45: [但是→这个]城市有才两个学校
- mengmu_samples#45: 但是城市[有才→，只有]两个学校
- mengmu_samples#45: 他的妈妈[-不是不喜欢他们的城市] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#45: 而是[想孟子有→想让孟子接受]很好的教育 — 想 + V., cannot be followed by N.
- mengmu_samples#45: [-他们]从早到晚走路
- mengmu_samples#45: [+因为]他们从早到晚走路
- mengmu_samples#45: [+所以]孟子一直抱怨
- mengmu_samples#45: [他难怪抱怨→难怪他抱怨] — 难怪 + sentence
- mengmu_samples#45: 他的妈妈[找到孟子→给孟子找到]一个老师
- mengmu_samples#45: [跟老师孟子→孟子跟老师]学最重要的文学
- mengmu_samples#45: 跟老师孟子[学→学习]最重要的文学
- mengmu_samples#45: 跟老师孟子学[-最重要的]文学
- mengmu_samples#47: 所以他们常常搬[-了]家 — no了for routine/habit
- mengmu_samples#47: [她→孟子的妈妈]望子成龙 — otherwise the references are confusing
- mengmu_samples#47: 所以[-孟子的妈妈]安排他的生活 — otherwise the references are confusing
- mengmu_samples#47: 因为他们常常搬[-了]家 — no了for routine/habit
- mengmu_samples#47: 妈妈[教→教了]孟子很多技能 — 了completed
- mengmu_samples#47: [先她→她先]让孟子跟朋友玩儿 — Subj.先……
- mengmu_samples#47: 然后教他怎么买又便宜又[好质量→质量又好]的东西
- shennong_samples#4: 也不知道什么植物对[-你的]身体有好处 — not你的
- shennong_samples#4: 所以神农[去了吃→去吃了]每种植物
- shennong_samples#4: 就[写了→写下了]这个植物对你有没有好处
- shennong_samples#4: 就写了这个植物[-对你]有没有好处
- shennong_samples#4: 会[-来]跟他的朋友聊到他吃的植物了
- shennong_samples#4: 会来跟他的朋友聊到他吃的植物[-了] — no了
- shennong_samples#4: 就觉得这种植物对我的[脑→大脑]有坏处
- shennong_samples#4: [-一个灵芝和]一个男人正好在我的旁边 — “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two
- shennong_samples#4: 一个灵芝和一个男人正好[在→过来，看到]我的旁边 — “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two
- shennong_samples#4: 一个灵芝和一个男人正好在我的旁边[+长着一个灵芝] — “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two
- shennong_samples#4: [你得小心吃植物→吃植物得小心]
- shennong_samples#4: 因为有的植物[-对你]的健康有坏处
- shennong_samples#8: 神农想帮[别人→他们] — “别(的)” is for “a different type”, and “all else except the spoken one”
- shennong_samples#8: 一些植物[吃真好→真好吃]
- shennong_samples#8: 一些植物[毒得很→毒性强得很]
- shennong_samples#8: 麻烦[+告诉]我们可以吃什么植物？神农说
- shennong_samples#8: [以后→后来] — Time+以后
- shennong_samples#8: 神农告诉[别人→人们]一些植物能吃 — “别(的)” is for “a different type”, and “all else except the spoken one”
- shennong_samples#8: 神农告诉别人[一些植物能吃，一些植物不能吃→哪些植物能吃，哪些植物不能吃]
- shennong_samples#12: 古代的人[-很]不知道什么植物能吃
- shennong_samples#12: [-也]什么植物不能吃
- shennong_samples#12: 吃不安全的植物对[-你的]身体有坏处 — redundant
- shennong_samples#12: [+是]很麻烦的情况
- shennong_samples#12: 神农写[+下]他的主意
- shennong_samples#12: 神农写他的[主意→发现]
- shennong_samples#12: [别人→另外一个人]看到他 — “别(的)” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- shennong_samples#12: [+也]会告诉他的朋友哪一个植物能不能吃
- shennong_samples#12: 会告诉他的朋友[哪一个植物能不能吃→哪一个植物能吃，哪个植物不能吃]
- shennong_samples#18: 因为他的家人常常生病[-了] — no了for routine/habit
- shennong_samples#18: 他们去[+了]很多不一样的地方 — 了completed
- shennong_samples#18: 他们在很漂亮的河[+边，]找夹竹桃
- shennong_samples#18: 他们在很漂亮的河[找→看到]夹竹桃
- shennong_samples#18: 神农问他的哥哥：“我应该吃这种植物吗？”哥哥说：“这就要看你想要安全[还是接近知道了→还是想要知道夹竹桃有没有毒]
- shennong_samples#18: 我想知道[灵芝会帮他→灵芝有没有用]
- shennong_samples#18: 我想知道[灵芝会帮他→灵芝能不能帮他]
- shennong_samples#18: ”哥哥给[+了]神农灵芝 — 了completed
- shennong_samples#18: 你[帮→做]得真好
- shennong_samples#18: 你帮得[真好→很好]
- shennong_samples#19: 他[找→找到]很多植物 — 找look for vs.找到find
- shennong_samples#19: 凉山很大[-的山]
- shennong_samples#19: [这→在这儿]也找植物
- shennong_samples#19: 这也[+能]找植物
- shennong_samples#19: 这也找[+到]植物
- shennong_samples#19: 他找到[+一种]黄色的花 — “黄色的花“too general and too vague
- shennong_samples#19: 他听说[-你]跟黄色的花做茶很有用
- shennong_samples#19: 他听说你[跟→用]黄色的花做茶很有用
- shennong_samples#19: [-你的]头发疼死
- shennong_samples#19: 你的[头发疼死→头很疼]
- shennong_samples#19: [这→这种]冰茶是药
- shennong_samples#19: [灵芝药的夹竹桃→可以做夹竹桃解药的灵芝]他吃完了
- shennong_samples#19: 灵芝药的夹竹桃他[吃完了→吃了]
- shennong_samples#19: [-也]写一个课文的植物
- shennong_samples#19: 也[写→写下]一个课文的植物
- shennong_samples#19: 也写[一个→一篇]课文的植物
- shennong_samples#19: 也写一个[课文的→有关]植物
- shennong_samples#19: 也写一个课文的植物[+的文章]
- shennong_samples#26: 有一个[老男人→老人]叫神农 — “老男人“ has negative meaning
- shennong_samples#26: 神农[-在古代]每一天看到了别的小镇人生病还是不舒服 — it implies that 神农can travel between 古代 and 现代modern times
- shennong_samples#26: 神农在古代每一天[看到了→都看到]别的小镇人生病还是不舒服 — no了for routine/habit
- shennong_samples#26: 神农在古代每一天看到了[别的小镇人→别的小镇上的人]生病还是不舒服
- shennong_samples#26: 神农在古代每一天看到了别的小镇人生病[还是→或者]不舒服
- shennong_samples#26: 他[下一天→第二天，]开始爬当地的山脉
- shennong_samples#26: 他下一天开始爬[当地的山脉→当地的大山] — 山脉is for geography
- shennong_samples#26: 他[一次→有一次]试一试有些植物的叶
- shennong_samples#26: 他一次[试一试→试了试]有些植物的叶 — 了completed
- shennong_samples#26: 他一次试一试有些植物的[叶→叶子]
- shennong_samples#26: [吃得→吃起来]又新鲜又甜
- shennong_samples#26: 煮[+了]这些叶以后 — 了completed
- shennong_samples#26: 煮这些[叶→叶子]以后
- shennong_samples#26: 虽然他找到了很多[-的]新的植物
- shennong_samples#26: 但是他的旅程[-有的时候]特别是危险
- shennong_samples#26: 但是他的旅程有的时候特别[-是]危险 — ”特别是+N, + Clause” is used to single out a typical example
- shennong_samples#26: 一个爬山的男人正好看到神农[-的麻烦]
- shennong_samples#26: 神农最终[-他的]小镇回到
- shennong_samples#26: 神农最终他的[小镇回到→回到小镇]
- shennong_samples#26: 你认为神农的故事[+是]真的吗？这就要看你相信中药对身体有好处
- shennong_samples#26: 你认为神农的故事真的吗？这就要看你相信[+不相信]中药对身体有好处
- shennong_samples#26: 你认为神农的故事真的吗？这就要看你相信中药对身体有好处[+了]
- shennong_samples#33: [人→人们]不知道他们能吃什么植物
- shennong_samples#33: 告诉人什么植物[是安全什么是危险→是安全的，是危险的]
- shennong_samples#33: [+他]发现有的植物对身体非常好
- shennong_samples#33: 让肚子[-感觉]又暖和又清楚
- shennong_samples#33: 让肚子感觉又暖和又[清楚→舒服]
- shennong_samples#33: 这就要看你的口味[+了]
- shennong_samples#33: 什么[都花→花都]想吃
- shennong_samples#33: [-他发现这个口味] — since it has no clear relationship with previous or following clauses
- shennong_samples#33: 一百岁[+的]时候
- shennong_samples#33: 一吃就[开始死→开始不舒服] — “死“ is instant, so cannot be with “开始”
- shennong_samples#33: 但是[生病时候→即使他生病了，也]告诉人什么植物是药
- shennong_samples#35: 所以他们找到了很多植物[对药→来做药]
- shennong_samples#35: 他们吃[+了]很多植物对药 — 了completed
- shennong_samples#35: 但是我觉得他们[-的]吃的植物
- shennong_samples#35: 但是我觉得他们的吃的植物[-，]让他们病人
- shennong_samples#35: 让他们[病人→生病] — 让Sb. + V./Adj.
- shennong_samples#35: 所以他想找一个[植物对药→可以做药的植物]
- shennong_samples#35: 他们可以吃对药[+这样，]
- shennong_samples#35: 他想把花[放在茶里，对药→做成药]
- shennong_samples#35: 他不知道[-如果]这把花对你的身体好 — the “if” in “not know if + clause” is not 如果
- shennong_samples#35: 他不知道如果[这把花→这种花]对你的身体好
- shennong_samples#35: 他不知道如果这把花对[-你的]身体好
- shennong_samples#35: 他不知道如果这把花对你的身体[好→好不好] — the “if” in “not know if + clause” is not 如果
- shennong_samples#35: 这就要看[-如果]这把花毒不毒了 — the “if” in “not know if + clause” is not 如果, delete如果
- shennong_samples#35: 这就要看如果这把花[毒不毒了→有没有毒]
- shennong_samples#35: 他找到了[别的花→另外一种花] — “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- shennong_samples#35: 神农不知道他[吃不吃→要不要吃]灵芝或者夹竹桃
- shennong_samples#35: 这个植物可以让[神农更好→身体更好]
- shennong_samples#35: [-比方说，]他会觉得更健康 — 比方说is used to express “for example”, delete it
- shennong_samples#35: [吃灵芝以后→吃了灵芝以后] — 了completed
- shennong_samples#35: 他[可以再走→又可以走了]
- shennong_samples#42: 他需要当上[医→医生]
- shennong_samples#42: 什么病人[吃→吃了以后]都会觉得身体更好
- shennong_samples#42: 这[种一定是→一定是一种]做药的花
- shennong_samples#42: [原来→结果]他想错了 — “原来” is to explain the reason while “结果” is to describe an unexpected result
- shennong_samples#42: 神农[快→很快就]生病
- shennong_samples#42: 神农快生病[+了]
- shennong_samples#42: [快给→很快地给了]他一种红的灵芝 — 快V: to give order, 了completed
- shennong_samples#42: [-他]没有病 — redundant
- shennong_samples#42: 他[没有病→病好了]
- shennong_samples#42: 一回家就告诉[别人→家人]
- shennong_samples#42: 他找到药以后[-他]写下怎么做药在书上 — redundant
- shennong_samples#42: 他找到药以后他[写下怎么做药在书上→在书上写下怎么做药]
- shennong_samples#42: [那红灵芝→这样]对身体好处
- shennong_samples#42: 那红灵芝对身体[好处→有好处]
- shennong_samples#49: 有很多人[吃植物以后→吃了植物以后]就吃坏肚子了 — 了completed
- shennong_samples#49: 因为他们[吃了毒→吃了有毒的植物]
- shennong_samples#49: 他希望别人也可以吃[+到]好吃的植物 — with result
- shennong_samples#49: [+就]不会吃他喜欢的植物
- shennong_samples#49: 不会吃他[喜欢→到好吃]的植物
- shennong_samples#49: 不会吃[-他]喜欢的植物
- shennong_samples#49: 他是[第一人，找到了茶→第一个找到茶的人]
- shennong_samples#49: 他[一直都吃了→一直都在吃不同的植物]
- shennong_samples#49: 可是夹竹桃的毒[很重→很强]
- shennong_samples#49: 觉得他快[-会]死了
- shennong_samples#49: 可是正好[有别人→有人]找到他了 — “别(的)” is for “a different type”, and “all else except the spoken one”
- shennong_samples#49: 他[吃→吃了]灵芝以后就觉得很好 — 了completed
- shennong_samples#49: 他[测量起来了→写下来了]

## Candidates matching nothing the teacher marked (41 distinct; first 60)

Not necessarily wrong: these are for the teacher to judge.

- mengmu_samples#10 (high, numeral_measure_word_order): 孟子五岁[-的]时候 — Num. + MW. + N., no 的
- mengmu_samples#10 (high, first_mention_introduction): 孟子和⟦孟母⟧搬到子思老师的家 — first appearance of 孟母: briefly introduce who this is
- mengmu_samples#10 (high, perception_look_see): 就是[看→看到]哲学书 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- mengmu_samples#10 (high, zero_redundant_pronoun): 难怪[-他]成为很有名的哲学家 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#12 (high, first_mention_introduction): 孟子跟⟦孟母⟧住在墓地的旁边 — first appearance of 孟母: briefly introduce who this is
- mengmu_samples#18 (high, location_with_zai): 孟子的妈妈不是[待在家里就是→在家里就是待]编织衣服赚钱 — 在 + Place comes before the action: 在Place + V.
- mengmu_samples#25 (high, location_with_zai): 他的妈妈[觉得在墓地→在墓地觉得]玩儿 — 在 + Place comes before the action: 在Place + V.
- mengmu_samples#25 (high, zero_redundant_pronoun): 难怪[-他]成为有名的人 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#32 (high, zero_redundant_pronoun): 所以[-她]会一直搬家才能找到质量好的教育 — 她 repeats the subject of the clause before: zero form
- mengmu_samples#33 (high, zero_redundant_pronoun): 很多墓地得[-我]祭拜 — 我 repeats the subject of the clause before: zero form
- mengmu_samples#33 (high, zero_redundant_pronoun): 所以[-他]祭拜不是想帮妈妈工作 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#33 (high, zero_redundant_pronoun): 而是[-他]很喜欢画画 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#4 (high, first_mention_introduction): 孟子和⟦孟母⟧住了在靠墓地的家 — first appearance of 孟母: briefly introduce who this is
- mengmu_samples#4 (high, zero_redundant_pronoun): [-他]成为很有名的哲人 — 他 repeats the subject of the clause before: zero form
- mengmu_samples#45 (high, first_mention_introduction): 一个男孩子跟⟦他⟧的妈妈住在中国 — the story starts with a pronoun: introduce the character first
- mengmu_samples#47 (high, first_mention_introduction): ⟦孟母⟧三迁 — first appearance of 孟母: briefly introduce who this is
- mengmu_samples#47 (high, zero_redundant_pronoun): 难怪[-他]很聪明 — 他 repeats the subject of the clause before: zero form
- shennong_samples#12 (high, no_le_mental_state): 发现[-了]夹竹桃有毒 — no 了 after the mental-state verb 发现
- shennong_samples#18 (high, perception_look_see): 神农问他的哥哥：“我应该吃这种植物吗？”哥哥说：“这就要[看→看到]你想要安全还是接近知道了 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#18 (high, zero_redundant_pronoun): 特别是如果[-我们]已经吃了夹竹桃 — 我们 repeats the subject of the clause before: zero form
- shennong_samples#19 (high, location_with_zai): [古代的时候→在古代] — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- shennong_samples#19 (high, first_mention_introduction): ⟦他⟧叫神农 — the story starts with a pronoun: introduce the character first
- shennong_samples#26 (high, search_find): [找了→找到了]各种各样的植物 — her pattern: 找了 -> 找到了 (corrected 3/5 in train)
- shennong_samples#26 (high, perception_look_see): 你认为神农的故事真的吗？这就要[看→看到]你相信中药对身体有好处 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#33 (high, perception_look_see): 这就要[看→看到]你的口味 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#33 (high, loose_clause_connection): [可能→，这样可以]喜欢糖 — her pattern: 可能 -> ，这样可以 (corrected 9/14 in train)
- shennong_samples#35 (high, loose_clause_connection): 神农觉得这个植物[可能→，这样可以]特别是毒 — her pattern: 可能 -> ，这样可以 (corrected 9/14 in train)
- shennong_samples#35 (high, zero_redundant_pronoun): [-他]想把花放在茶里 — 他 repeats the subject of the clause before: zero form
- shennong_samples#35 (high, perception_look_see): 这就要[看→看到]如果这把花毒不毒了 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#4 (high, location_with_zai): [古代的时候→在古代] — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- shennong_samples#4 (high, first_mention_introduction): ⟦他⟧的名字是神农 — the story starts with a pronoun: introduce the character first
- shennong_samples#4 (high, zero_redundant_pronoun): 所以[-神农]去了吃每种植物 — 神农 repeats the subject of the clause before: zero form
- shennong_samples#4 (high, perception_look_see): 这就要[看→看到]你的口味了 — her pattern: 看 -> 看到 (corrected 37/71 in train)
- shennong_samples#4 (high, other_vs_additional): 一个[-别的人]问神农 — her pattern: 别的人 -> (delete) (corrected 8/8 in train)
- shennong_samples#42 (high, location_with_zai): [古代的时候→在古代]有一个人叫神农 — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- shennong_samples#42 (high, zero_redundant_pronoun): [-他]不知道什么东西能做药 — 他 repeats the subject of the clause before: zero form
- shennong_samples#49 (high, location_with_zai): [古代的时候→在古代] — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- shennong_samples#49 (high, zero_redundant_pronoun): 觉得[-他]快会死了 — 他 repeats the subject of the clause before: zero form
- shennong_samples#49 (high, word_class_choice): 像星星的植物[是毒→有毒] — her pattern: 是毒 -> 有毒 (corrected 14/15 in train)
- shennong_samples#8 (high, location_with_zai): [古代的时候→在古代] — her pattern: 古代的时候 -> 在古代 (corrected 18/30 in train)
- shennong_samples#8 (high, perception_look_see): 这就要[看→看到]你想不想生病了 — her pattern: 看 -> 看到 (corrected 37/71 in train)
