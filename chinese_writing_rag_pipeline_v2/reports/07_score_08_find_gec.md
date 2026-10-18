# Step 7 report: scoring 08_find_gec

Finder: HillZhang/real_learner_bart_CGEC (beam search, 5 beams), prompt n/a, 1 run(s) in total.
Answer key: 267 teacher error edits + 20 comment edits on 20 test stories (1 edits excluded: unplaceable/unplaced or rejected in review (0 items rejected)).

## Recall: how many of the teacher's corrections the finder points at

| | Found |
|---|---|
| run 1 | 117/267 (44%) |
| average of one run | 117.0/267 (44%) |
| any of the 1 runs (union) | 117/267 (44%) |
| teacher comment edits (problem pointed at) | 1/20 (5%) |

Of the teacher edits found, the finder proposed **the same correction** for 28/117 (24%).

## Stability: in how many runs each teacher correction was found

| Found in | Teacher edits |
|---|---|
| 1 of 1 runs | 117 |
| 0 of 1 runs | 150 |

Edits found in some runs but not all (0) are the 'caught at random' problem in numbers.

## Recall by kind of edit

| Kind | Found (union) |
|---|---|
| insert | 22/48 (46%) |
| delete | 21/65 (32%) |
| replace | 74/154 (48%) |
| mengmu_san_qian | 51/114 (45%) |
| shennong_chang_baicao | 66/153 (43%) |

## Candidates: how many point at something the teacher corrected

| | Candidates | Match a teacher edit | Match nothing she marked |
|---|---|---|---|
| run 1 | 205 | 131/205 (64%) | 74 |

High-confidence candidates matching a teacher edit: 131/205 (64%); low-confidence: 0/0.
Candidates that could not be located: 0.

Candidate types: gec 205 (63% match)

## Teacher corrections no run found (150)

- mengmu_samples#4: [古代的时候→在古代]
- mengmu_samples#4: [孩子→孟子]才五岁就每天在墓地祭拜了 — 孩子is vague and unclear
- mengmu_samples#4: 他们搬了到[别一个→另外一个]城市找工作 — “别（的）” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- mengmu_samples#4: 不是[+常常有]人吵架
- mengmu_samples#4: 孟子和妈妈[-要]又一个次搬了家 — “要” is for future plan/desire, this already occurred
- mengmu_samples#4: 孟母[找到→找到了]工作 — 了completed
- mengmu_samples#4: 孟子在那个商店也[找了到→找到了]工作
- mengmu_samples#4: 孟子[学习馆→在学校]学了十五年 — 在+Place
- mengmu_samples#4: 他的学习和[-他的]旅行经验很重要
- mengmu_samples#4: 他[是大人的时候→长大以后]
- mengmu_samples#4: 他成为很有名的[哲人→哲学家]
- mengmu_samples#4: [-他]是大人的时候
- mengmu_samples#10: [装祭拜→装着祭拜的样子]
- mengmu_samples#10: 害得[孟子的心气→孟子受到不好的影响] — 害得Sb. + V.
- mengmu_samples#12: [古代，→在古代，]孟子跟孟母住在墓地的旁边
- mengmu_samples#12: [从早到晚→都]很吵
- mengmu_samples#12: 害得孟母[+不能出去工作，只好]只好一直陪孟子 — “害得“ + harmful result, 一直陪孟子itself is not harmful
- mengmu_samples#12: 住在商店的旁边不是适合孟子[+的环境]
- mengmu_samples#12: [将来→后来] — “将来“ refers to the absolute future
- mengmu_samples#18: [古代的时候→在古代]
- mengmu_samples#18: 而且害得孟子的学习[+不好] — 害得 + harmful result
- mengmu_samples#18: 而是搬到了孟子老师[的家→家里]
- mengmu_samples#18: [以后→后来]孟子成为了中国有名的哲学家 — Time+以后
- mengmu_samples#25: 这是[+一个]古代的故事
- mengmu_samples#25: [从他的家到→他的家离]墓地很近
- mengmu_samples#25: 所以他每天[-老是]从早到晚去墓地跟朋友们玩玩儿
- mengmu_samples#25: 他很聪明[-的人]
- mengmu_samples#32: 所以她决定了[-他们会]搬家找更好的地方
- mengmu_samples#32: 她[恐怕→怕]儿子的童年不会幸福 — 恐怕usually does not take Subj. except 我
- mengmu_samples#32: 所以她会一直搬家[-才能]找到质量好的教育
- mengmu_samples#32: 所以她会一直搬家才能[找到质量好的教育→想要让孟子受到良好的教育]
- mengmu_samples#32: [古代的时候→那时候]
- mengmu_samples#32: 但是孟子老是跟这些卖东西的人[-常常]玩儿 — redundant with老是
- mengmu_samples#32: 因为她恐怕儿子会成为跟他们很像[+的人] — 成为+ noun
- mengmu_samples#32: 你不是[+要]当数学家 — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#32: 你不是当[数学家→商人] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#32: 而是[+要]当哲学家 — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#32: 在他们[+的]第三个家
- mengmu_samples#32: 孟子学了[-怎么祭拜] — wrong information, it’s not about learning to offer sacrifices
- mengmu_samples#32: [他难怪→难怪后来他]成为有名的哲学家
- mengmu_samples#33: [-一天，]很久很久以前
- mengmu_samples#33: [-因为]他说我们老是搬家
- mengmu_samples#33: [-他]越来越喜欢祭拜 — redundant
- mengmu_samples#33: 他[+也]越来越喜欢祭拜 — no logic relationship, add也before越来越
- mengmu_samples#39: [-虽然]他没有朋友 — there is no “even though” meaning here
- mengmu_samples#39: 他的同学们老是[对→跟]他开玩笑了
- mengmu_samples#39: 看过很多政治文章[-对他]害得
- mengmu_samples#39: [-他]开始能解决问题 — redundant
- mengmu_samples#39: [-你]会成为高薪 — redundant
- mengmu_samples#45: [古代的时候→在古代]
- mengmu_samples#45: [但是→这个]城市有才两个学校
- mengmu_samples#45: 他的妈妈[-不是不喜欢他们的城市] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- mengmu_samples#45: [-他们]从早到晚走路
- mengmu_samples#45: [+因为]他们从早到晚走路
- mengmu_samples#45: [+所以]孟子一直抱怨
- mengmu_samples#45: [他难怪抱怨→难怪他抱怨] — 难怪 + sentence
- mengmu_samples#45: [+原来]他想他的朋友
- mengmu_samples#45: [跟老师孟子→孟子跟老师]学最重要的文学
- mengmu_samples#45: 跟老师孟子[学→学习]最重要的文学
- mengmu_samples#45: 跟老师孟子学[-最重要的]文学
- mengmu_samples#47: [她→孟子的妈妈]望子成龙 — otherwise the references are confusing
- mengmu_samples#47: 所以[-孟子的妈妈]安排他的生活 — otherwise the references are confusing
- mengmu_samples#47: 妈妈[教→教了]孟子很多技能 — 了completed
- shennong_samples#4: 也不知道什么植物对[-你的]身体有好处 — not你的
- shennong_samples#4: 就[写了→写下了]这个植物对你有没有好处
- shennong_samples#4: 就写了这个植物[-对你]有没有好处
- shennong_samples#4: 会[-来]跟他的朋友聊到他吃的植物了
- shennong_samples#4: [一个别的人→另外一个人]问神农 — “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- shennong_samples#4: [一个别的人→第三个人]问神农
- shennong_samples#4: [-一个灵芝和]一个男人正好在我的旁边 — “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two
- shennong_samples#4: 一个灵芝和一个男人正好[在→过来，看到]我的旁边 — “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two
- shennong_samples#4: 一个灵芝和一个男人正好在我的旁边[+长着一个灵芝] — “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two
- shennong_samples#4: [你得小心吃植物→吃植物得小心]
- shennong_samples#4: 因为有的植物[-对你]的健康有坏处
- shennong_samples#8: 一[看→看到]很多人正在吃一些植物 — 一……就
- shennong_samples#8: [以后→后来] — Time+以后
- shennong_samples#8: 神农告诉[别人→人们]一些植物能吃 — “别(的)” is for “a different type”, and “all else except the spoken one”
- shennong_samples#12: 古代的人[-很]不知道什么植物能吃
- shennong_samples#12: [-也]什么植物不能吃
- shennong_samples#12: 吃不安全的植物对[-你的]身体有坏处 — redundant
- shennong_samples#12: 神农写他的[主意→发现]
- shennong_samples#12: [别人→另外一个人]看到他 — “别(的)” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- shennong_samples#12: [+也]会告诉他的朋友哪一个植物能不能吃
- shennong_samples#18: 夹竹桃[是毒的→有毒的]
- shennong_samples#18: 你[帮→做]得真好
- shennong_samples#18: 你帮得[真好→很好]
- shennong_samples#19: 凉山很大[-的山]
- shennong_samples#19: 他听说[-你]跟黄色的花做茶很有用
- shennong_samples#19: [-你的]头发疼死
- shennong_samples#19: [这→这种]冰茶是药
- shennong_samples#19: [灵芝药的夹竹桃→可以做夹竹桃解药的灵芝]他吃完了
- shennong_samples#19: 灵芝药的夹竹桃他[吃完了→吃了]
- shennong_samples#19: [-也]写一个课文的植物
- shennong_samples#19: 也写一个[课文的→有关]植物
- shennong_samples#19: 也写一个课文的植物[+的文章]
- shennong_samples#26: 有一个[老男人→老人]叫神农 — “老男人“ has negative meaning
- shennong_samples#26: 神农[-在古代]每一天看到了别的小镇人生病还是不舒服 — it implies that 神农can travel between 古代 and 现代modern times
- shennong_samples#26: 神农在古代每一天看到了别的小镇人生病[还是→或者]不舒服
- shennong_samples#26: 他下一天开始爬[当地的山脉→当地的大山] — 山脉is for geography
- shennong_samples#26: 他[一次→有一次]试一试有些植物的叶
- shennong_samples#26: 他一次[试一试→试了试]有些植物的叶 — 了completed
- shennong_samples#26: [吃得→吃起来]又新鲜又甜
- shennong_samples#26: 煮[+了]这些叶以后 — 了completed
- shennong_samples#26: 虽然他找到了很多[-的]新的植物
- shennong_samples#26: 但是他的旅程[-有的时候]特别是危险
- shennong_samples#26: 一个爬山的男人正好看到神农[-的麻烦]
- shennong_samples#26: 跟[别的人→其他人]分享他的发现
- shennong_samples#26: 你认为神农的故事真的吗？这就要看你相信[+不相信]中药对身体有好处
- shennong_samples#26: 你认为神农的故事真的吗？这就要看你相信中药对身体有好处[+了]
- shennong_samples#33: 古代[+的]时候
- shennong_samples#33: [人→人们]不知道他们能吃什么植物
- shennong_samples#33: 告诉人什么植物[是安全什么是危险→是安全的，是危险的]
- shennong_samples#33: [+他]发现有的植物对身体非常好
- shennong_samples#33: 让肚子[-感觉]又暖和又清楚
- shennong_samples#33: 这就要看你的口味[+了]
- shennong_samples#33: [-他发现这个口味] — since it has no clear relationship with previous or following clauses
- shennong_samples#33: 一百岁[+的]时候
- shennong_samples#33: 不小心吃了[+有]毒的花
- shennong_samples#33: 但是[生病时候→即使他生病了，也]告诉人什么植物是药
- shennong_samples#33: 什么植物[是毒→有毒]
- shennong_samples#35: 所以他们找到了很多植物[对药→来做药]
- shennong_samples#35: 他们吃[+了]很多植物对药 — 了completed
- shennong_samples#35: 但是我觉得他们的吃的植物[-，]让他们病人
- shennong_samples#35: 让他们[病人→生病] — 让Sb. + V./Adj.
- shennong_samples#35: 所以他想找一个[植物对药→可以做药的植物]
- shennong_samples#35: 他们可以吃对药[+这样，]
- shennong_samples#35: 他不知道如果[这把花→这种花]对你的身体好
- shennong_samples#35: 他不知道如果这把花对[-你的]身体好
- shennong_samples#35: 这就要看如果这把花[毒不毒了→有没有毒]
- shennong_samples#35: 他找到了[别的花→另外一种花] — “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- shennong_samples#35: 神农不知道他[吃不吃→要不要吃]灵芝或者夹竹桃
- shennong_samples#35: [别的人→另外一个人]给了神农一个灵芝 — “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- shennong_samples#35: [-比方说，]他会觉得更健康 — 比方说is used to express “for example”, delete it
- shennong_samples#35: 他[可以再走→又可以走了]
- shennong_samples#42: [原来→结果]他想错了 — “原来” is to explain the reason while “结果” is to describe an unexpected result
- shennong_samples#42: 神农[快→很快就]生病
- shennong_samples#42: [-他]没有病 — redundant
- shennong_samples#42: 他[没有病→病好了]
- shennong_samples#42: 一回家就告诉[别人→家人]
- shennong_samples#42: [那红灵芝→这样]对身体好处
- shennong_samples#49: 有很多人[吃植物以后→吃了植物以后]就吃坏肚子了 — 了completed
- shennong_samples#49: 因为他们[吃了毒→吃了有毒的植物]
- shennong_samples#49: 如果他们[还怕吃毒→吃到有毒的植物]
- shennong_samples#49: 不会吃他[喜欢→到好吃]的植物
- shennong_samples#49: 不会吃[-他]喜欢的植物
- shennong_samples#49: [-他]连毒都能吃 — delete the second他
- shennong_samples#49: 可是夹竹桃的毒[很重→很强]
- shennong_samples#49: 可是正好[有别人→有人]找到他了 — “别(的)” is for “a different type”, and “all else except the spoken one”
- shennong_samples#49: 他[吃→吃了]灵芝以后就觉得很好 — 了completed
- shennong_samples#49: 他[测量起来了→写下来了]

## Candidates matching nothing the teacher marked (74 distinct; first 60)

Not necessarily wrong: these are for the teacher to judge.

- mengmu_samples#10 (high, gec): 跟妈妈搬家[+了] — model rewrite: 孟子五岁的时候，跟妈妈搬家了。
- mengmu_samples#10 (high, gec): 而是[-因为]妈妈认为他们的家离墓地太近 — model rewrite: 他们搬家不是因为孟子玩得太多，而是妈妈认为他们的家离墓地太近。
- mengmu_samples#10 (high, gec): 害[-得]孟子的心气 — model rewrite: 妈妈认为，住得离墓地太近，会伤害孟子的心气。
- mengmu_samples#10 (high, gec): 孟子和孟母搬到子思老师的家[-，跟子思老师]住 — model rewrite: 孟子和孟母搬到子思老师的家住。
- mengmu_samples#12 (high, gec): 住在墓地的旁边[+会]影响孟子 — model rewrite: 可是孟母注意到，住在墓地的旁边会影响孟子。
- mengmu_samples#12 (high, gec): 害得孟母只好一直陪[+着]孟子 — model rewrite: 害得孟母只好一直陪着孟子。
- mengmu_samples#12 (high, gec): 他[+会]成为中国的一个非常有名的哲学家 — model rewrite: 将来，他会成为中国的一个非常有名的哲学家。
- mengmu_samples#18 (high, gec): [+所以]他们一直在哭 — model rewrite: 因为人们在祭拜，所以他们一直在哭。
- mengmu_samples#18 (high, gec): 而且害得孟子[-的]学习 — model rewrite: 孟子和孟子的妈妈住在这里才一个星期就觉得受不了了，而且害得孟子学习。
- mengmu_samples#18 (high, gec): 孟子的妈妈觉得孟子[取得→受到]良好的教育是很重要的 — model rewrite: 孟子的妈妈觉得孟子受到良好的教育是很重要的，所以孟子妈妈认为这样的地方对儿子不太好，就打算让孟子搬家。
- mengmu_samples#18 (high, gec): 所以孟子的妈妈认为这样的地方对儿子[-的教育]不太好 — model rewrite: 孟子的妈妈觉得孟子受到良好的教育是很重要的，所以孟子妈妈认为这样的地方对儿子不太好，就打算让孟子搬家。
- mengmu_samples#18 (high, gec): 就打算[跟→让]孟子搬家 — model rewrite: 孟子的妈妈觉得孟子受到良好的教育是很重要的，所以孟子妈妈认为这样的地方对儿子不太好，就打算让孟子搬家。
- mengmu_samples#18 (high, gec): 孟子的妈妈[+不是]带孟子不是搬到城市 — model rewrite: 孟子的妈妈不是带孟子搬到城市，而是搬到了孟子老师的家。
- mengmu_samples#18 (high, gec): 孟子的妈妈带孟子[-不是]搬到城市 — model rewrite: 孟子的妈妈不是带孟子搬到城市，而是搬到了孟子老师的家。
- mengmu_samples#25 (high, gec): 他[+是]很聪明的人 — model rewrite: 他是很聪明的人，难怪他成为有名的人。
- mengmu_samples#32 (high, gec): 有一天孟子去[-了]墓地玩儿 — model rewrite: 有一天孟子去墓地玩儿，但是他妈妈觉得这是不合适让孩子玩的地方，所以她决定他们会搬家找更好的。
- mengmu_samples#32 (high, gec): 他们住才一月就又搬家[+了] — model rewrite: 他们才住了一月就又搬家了。
- mengmu_samples#32 (high, gec): 因为她恐怕儿子会[-成为]跟他们很像 — model rewrite: 但是孟子老是跟这些卖东西的人常常玩儿，害得妈妈着急得很，因为她担心儿子会跟他们很像。
- mengmu_samples#33 (high, gec): 很多墓地[+都]得我祭拜 — model rewrite: 他妈妈说，从早到晚，我一直祭拜，很多墓地都得我祭拜。
- mengmu_samples#33 (high, gec): 每次搬家孟子[也→都]觉得新的地方不是太热就是太冷 — model rewrite: 每次搬家孟子都觉得新的地方不是太热就是太冷，不是大就是小。
- mengmu_samples#33 (high, gec): 不是[-太]大就是太小 — model rewrite: 每次搬家孟子都觉得新的地方不是太热就是太冷，不是大就是小。
- mengmu_samples#33 (high, gec): 不是太大就是[-太]小 — model rewrite: 每次搬家孟子都觉得新的地方不是太热就是太冷，不是大就是小。
- mengmu_samples#33 (high, gec): 而是[+因为]他很喜欢画画 — model rewrite: 他画画很厉害，他越来越喜欢祭拜，所以他祭拜不是想帮妈妈工作，而是因为他很喜欢画画。
- mengmu_samples#33 (high, gec): 孟子成为[+了]很著名的古代画家 — model rewrite: 孟子成为了很著名的古代画家。
- mengmu_samples#39 (high, gec): 因为每天只[+是]祭拜 — model rewrite: 虽然他没有朋友，因为每天只是祭拜。
- mengmu_samples#39 (high, gec): 成为[+了]一个哲学家 — model rewrite: 孟子才十一岁，就成为了一个哲学家。
- mengmu_samples#39 (high, gec): 因为如果你懂政治[+的话] — model rewrite: 他常常建议你不要学金融，而是学政治，因为如果你懂政治的话，你会得到高薪。
- mengmu_samples#4 (high, gec): 孟母从早到晚都[+在]找工作 — model rewrite: 在那个城市，孟母从早到晚都在找工作，可是找不到，害得孟母没有钱。
- mengmu_samples#4 (high, gec): 可是不是做衣服的工作[-，而是喜欢的工作] — model rewrite: 孟子在那个商店也找了到工作，可是不是做衣服的工作。
- mengmu_samples#4 (high, gec): 他成为[+了]很有名的哲人 — model rewrite: 他是大人的时候，他成为了很有名的哲人。
- mengmu_samples#45 (high, gec): 所以孟子老是祭拜[+他们] — model rewrite: 他们住在墓地的旁边，所以孟子老是祭拜他们。
- mengmu_samples#45 (high, gec): 他们搬[-家]到有很多学校的城市 — model rewrite: 他们搬到了有很多学校的城市。
- mengmu_samples#45 (high, gec): 他们搬家到[+了]有很多学校的城市 — model rewrite: 他们搬到了有很多学校的城市。
- mengmu_samples#45 (high, gec): 他的妈妈找到孟子[一个→的]老师 — model rewrite: 他的妈妈找到一个教孟子的老师。
- mengmu_samples#45 (high, gec): 所以他成为[+了]哲学家 — model rewrite: 跟老师孟子学最重要的文学，所以他成为了哲学家。
- mengmu_samples#47 (high, gec): 妈妈教孟子很多[技能→东西] — model rewrite: 从这儿到那儿，妈妈教孟子很多东西。
- mengmu_samples#47 (high, gec): 然后教他怎么买又便宜[+质量]又好质量的东西 — model rewrite: 先让孟子跟朋友玩儿，然后教他怎么买又便宜质量又好的东西。
- shennong_samples#12 (high, gec): 也什[么→麼]植物不能吃 — model rewrite: 很久以前，古代的人很不知道什么植物能吃，也什麼植物不能吃。
- shennong_samples#12 (high, gec): 所以很多人常常吃不安全的[植→食]物 — model rewrite: 所以很多人常常吃不安全的食物，吃不健康的食品对你的身体有坏处，这是很麻烦的情况。
- shennong_samples#12 (high, gec): 吃不[安全→健康]的植物对你的身体有坏处 — model rewrite: 所以很多人常常吃不安全的食物，吃不健康的食品对你的身体有坏处，这是很麻烦的情况。
- shennong_samples#12 (high, gec): 吃不安全的[植物→食品]对你的身体有坏处 — model rewrite: 所以很多人常常吃不安全的食物，吃不健康的食品对你的身体有坏处，这是很麻烦的情况。
- shennong_samples#12 (high, gec): 旅行很远[+还]找到很多植物 — model rewrite: 他又聪明又努力，旅行很远还找到很多植物。
- shennong_samples#12 (high, gec): 神农遇到了一[个→种]黄色的花 — model rewrite: 神农遇到了一种黄色的花，一吃就觉得不舒服。
- shennong_samples#12 (high, gec): 发现[-了]夹竹桃有毒 — model rewrite: 发现夹竹桃有毒。
- shennong_samples#12 (high, gec): 很快给他吃[+了]一个灵芝 — model rewrite: 别人看到他，很快给他吃了一个灵芝。
- shennong_samples#12 (high, gec): 神农一吃就觉得比较好[+吃] — model rewrite: 神农一吃就觉得比较好吃。
- shennong_samples#18 (high, gec): 特别是如果我们[-已经]吃了夹竹桃 — model rewrite: 灵芝我们可以吃，特别是如果我们吃了夹竹桃。
- shennong_samples#19 (high, gec): 可是有的吃了[以→之]后很舒服 — model rewrite: 有的植物吃了以后他的肚子疼死了，可是有的吃了之后很舒服。
- shennong_samples#19 (high, gec): 凉山[+是一座]很大的山 — model rewrite: 凉山是一座很大的山，这里也能找到植物。
- shennong_samples#19 (high, gec): 他一喝茶就[+觉得]很不舒服 — model rewrite: 他一喝茶就觉得很不舒服。
- shennong_samples#26 (high, gec): 找[-了]各种各样的植物 — model rewrite: 他第一天开始爬当地的山脉，找各种各样的植物。
- shennong_samples#26 (high, gec): 神农试[一→了]试每个植物 — model rewrite: 神农试了试每个植物，知道有什么好处。
- shennong_samples#26 (high, gec): 他一喝就知道他发现[+了]新的茶叶 — model rewrite: 煮这些叶子以后，他一喝就知道他发现了新的茶叶。
- shennong_samples#26 (high, gec): 你认为神农的故事真的吗？这就要看你[+是否]相信中药对身体有好处 — model rewrite: 这就要看你是否相信中药对身体有好处。
- shennong_samples#33 (high, gec): 神农出去试[一→了]试很多种植物 — model rewrite: 所以有一天，神农出去试了试很多种植物，告诉人什么植物是安全什么是危险。
- shennong_samples#33 (high, gec): 什么[-植物]是毒 — model rewrite: 但是生病时候告诉人什么植物是药，什么是毒。
- shennong_samples#35 (high, gec): 他们吃很多植物[-对]药 — model rewrite: 神农先看到很多病人，他们吃很多植物药。
- shennong_samples#35 (high, gec): 所以他想找一[个→种]植物对药 — model rewrite: 所以他想找一种植物对药，他们可以吃对药。
- shennong_samples#35 (high, gec): 这就要看如果这把[花→烟]毒不毒了 — model rewrite: 他不知道这把花对你的身体好不好，这就要看这把烟毒不毒了。
- shennong_samples#35 (high, gec): 现在他觉得更好[+了] — model rewrite: 现在他觉得更好了。
