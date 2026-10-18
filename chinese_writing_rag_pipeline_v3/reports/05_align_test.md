# Step 5 report: aligning the teacher's corrections (test)

- model gpt-5.6-terra, reasoning effort medium, prompt 93779976b8
- feedback lines: 184 (0 from cache); tokens: {'prompt_tokens': 184451, 'completion_tokens': 26653, 'total_tokens': 211104}
- teacher items: 234 -> edits: 271 (replace 159, delete 58, insert 33, comment 21)
- extra comment edits for a separate error in a note: 2
- items with no problem found by the checks: 221 of 234

## Problems found by the checks

| Problem | Items |
|---|---|
| edits do not reproduce her fix | 11 |
| model unsure | 4 |

## All items

| Teacher's piece | Edits as read by the model | Her note | Check |
|---|---|---|---|
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧小的时候 | better to briefly introduce “孟子” when this character first appears |  |
| 在墓地玩 | 孟子和他的朋友喜欢[玩在墓地里→在墓地玩] | 在Place V. |  |
| 装着祭拜的样子 | [装祭拜→装着祭拜的样子] |  |  |
| 住在离墓地太近的地方，会害得孟子受到不好的影响 | 住[+在]离墓地太近 ; 住离墓地太近[+的地方，会] ; 害得孟子的[心气→受到不好的影响] | 害得Sb. + V. | edits do not reproduce her fix |
| 孟子现在没有朋友，因为他老是读书 | [因为孟子现在没有朋友，他老是读书→孟子现在没有朋友，因为他老是读书] |  |  |
| 从五岁开始 | 孟子[从五岁一直→从五岁开始]学哲学 |  |  |
| 在古代 | [古代，→在古代，]孟子跟孟母住在墓地的旁边 |  |  |
| (separate error in a note) | ⟦孟子⟧跟孟母住在墓地的旁边 | better to briefly introduce “孟子” when this character first appears |  |
| 注意到 | 可是孟母[注意→注意到] | 注意action vs.注意到result |  |
| 祭拜着玩儿 | 他常常跟朋友们[祭拜玩→祭拜着玩儿] | V.着玩儿 do something just for fun |  |
| 决定搬家 | 所以孟母决定[-他们会]搬家 |  |  |
| 都很吵 | [从早到晚→都]很吵 |  |  |
| add something like “不能出去工作”, “害得“ + harmful result, 一直陪孟子itself is not harmful | 害得孟母只好[+不能出去工作]一直陪孟子 | “害得“ + harmful result, 一直陪孟子itself is not harmful |  |
| 不是适合孟子的环境 | 住在商店的旁边不是适合孟子[+的环境] |  |  |
| 就开始 | 才五岁孟子[+就]开始学哲学 | 才Num.就V. |  |
| 后来 | [将来→后来] | “将来“ refers to the absolute future |  |
| 在古代 | [古代的时候→在古代] |  |  |
| 害得孟子的学习不好 | 而且害得孟子的学习[+不好] | 害得 + harmful result |  |
| replace孟子的妈妈with她 | 所以[孟子的妈妈→她]认为这样的地方对儿子的教育不太好 | replace孟子的妈妈with她 |  |
| 家里 | 而是搬到了孟子老师的[家→家里] |  |  |
| 后来 | [以后→后来]孟子成为了中国有名的哲学家 | Time+以后 |  |
| 这是一个古代的故事 | 这是[+一个]古代的故事 |  |  |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧小的时候 | better to briefly introduce “孟子” when this character first appears |  |
| 他的家离墓地很近 | [从他的家到墓地很近→他的家离墓地很近] |  |  |
| delete老是 | 所以他每天[-老是]从早到晚去墓地跟朋友们玩玩儿 |  |  |
| 玩儿 | 所以他每天老是从早到晚去墓地跟朋友们[玩玩儿→玩儿] | V.V. is used to make requests or plans |  |
| 害得孟子学习不好 | [害得→害得孟子学习不好] | 害得 + harmful result |  |
| 帮妈妈工作 | 可是每天不是写字就是帮妈妈[-的]工作 | 帮sb. do sth. |  |
| 很聪明 | 他很聪明[-的人] |  |  |
| better to briefly introduce “孟子” when this character first appears | 有一天⟦孟子⟧去了墓地玩儿 | better to briefly introduce “孟子” when this character first appears |  |
| 这不是适合孩子玩的地方 | 但是他妈妈觉得[这是不合适的地方让孩子玩→这不是适合孩子玩的地方] |  |  |
| 不是要当商人，而是要当哲学家 | 你不是[+要]当数学家 ; 你不是当[数学家→商人] ; 而是[+要]当哲学家 ; 而是当哲学家[-，不能当卖东西的人] | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong ; “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong ; “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong |  |
| 又搬家了 | 所以他们又搬家[+了] | 了completed |  |
| 在他们的第三个家，学会了/学习了 | 在他们[+的]第三个家 ; [孟子学了怎么祭拜→学会了/学习了] | wrong information, it’s not about learning to offer sacrifices |  |
| 告诉 | 告诉[-了]孟子：我们找到了最后的家 | no了for speaking word |  |
| 难怪后来他成为…… | [他难怪→难怪后来他]成为有名的哲学家 |  |  |
| 决定is a mental state verb, no了 | 所以她⟦决定了⟧他们会搬家找更好的地方 | 决定is a mental state verb, no了 |  |
| delete他们会 | 所以她决定了[-他们会]搬家找更好的地方 |  |  |
| 搬家到更好的地方 | 所以她决定了他们会[搬家找更好的地方→搬家到更好的地方] |  |  |
| 怕/担心 | 她[恐怕→怕]儿子的童年不会幸福 | 恐怕usually does not take Subj. except 我 | edits do not reproduce her fix |
| delete会 | 所以她[-会]一直搬家才能找到质量好的教育 | 会will |  |
| delete才能 | 所以她会一直搬家[-才能]找到质量好的教育 |  |  |
| 想要让孟子受到良好的教育 | 所以她会一直搬家才能[找到质量好的教育→想要让孟子受到良好的教育] |  |  |
| 才住了一个月 | 他们[住才一月→才住了一个月]就又搬家 | 了completed |  |
| 那时候 | [古代的时候→那时候] |  |  |
| delete常常 | 但是孟子老是跟这些卖东西的人[-常常]玩儿 | redundant with老是 |  |
| 怕/担心 | 因为她[恐怕→怕]儿子会成为跟他们很像 | 恐怕usually does not take Subj. except 我 | edits do not reproduce her fix; model unsure |
| 跟他们一样/很像的人 | 因为她恐怕儿子会成为[跟他们很像→跟他们一样的人] | 成为+ noun | edits do not reproduce her fix |
| 告诉 | 她告诉[-了]孟子：他们不是朋友 | no了for speaking word |  |
| delete一天 | [-一天，]很久很久以前 |  |  |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧和他妈妈住在中国 | better to briefly introduce “孟子” when this character first appears |  |
| wrong information, it’s not his mother’s job | ⟦孟子妈妈的工作是祭拜⟧ | wrong information, it’s not his mother’s job |  |
| delete因为 | [-因为]他说我们老是搬家 |  |  |
| 在哪儿 | [在哪的地方→在哪儿] |  |  |
| 才六岁 | 可是他[+才]六岁 |  |  |
| delete the second他 | [-他]越来越喜欢祭拜 | redundant |  |
| no logic relationship, add也before越来越 | 他[+也]越来越喜欢祭拜 | no logic relationship, add也before越来越 |  |
| wrong information, 哲学家 | 孟子成为很著名的⟦古代画家⟧ | wrong information, 哲学家 |  |
| 在古代，人们 | [古代的时候人→在古代，人们]觉得祭拜非常重要 | “人“ is too general and too vague, and does not stand alone |  |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧很小的时候 | better to briefly introduce “孟子” when this character first appears |  |
| delete虽然 | [-虽然]他没有朋友 | there is no “even though” meaning here |  |
| delete the second你 | [-你]会成为高薪 | redundant |  |
| 得到高薪 | 你会[成为高薪→得到高薪] | 成为 + profession/celebrity |  |
| 跟他开玩笑 | 他的同学们老是[对→跟]他开玩笑了 ; 他的同学们老是对他开玩笑[-了] | no了for routine/habit |  |
| 看到 | 孟子妈妈[看了→看到]他的同学们对孟子不好的影响 | 看look vs.看到see |  |
| 有不好的影响 | 孟子妈妈看了他的同学们[对孟子不好的影响→有不好的影响] |  |  |
| delete孟子和孟子妈妈, redundant | 所以[-孟子和孟子妈妈]搬家了 | redundant |  |
| 就成为 | [+就]成为一个哲学家 | 才Num.就V. |  |
| “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong, 祭拜is not conventionally related to哲学家 | ⟦孟子不是祭拜，而是看政治文章⟧ | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong, 祭拜is not conventionally related to哲学家 |  |
| delete对他 | 看过很多政治文章[-对他]害得 |  |  |
| 害得他有很多问题 | 看过很多政治文章对他[害得，他有很多问题→害得他有很多问题] | 害得Sb. + harmful result |  |
| 长大以后 | 孟子[长大→长大以后] |  |  |
| delete他 | [-他]开始能解决问题 | redundant |  |
| 建议人们，不要学金融 | 他常常建议[你不是→人们，不要]学金融 |  |  |
| 在古代 | [古代的时候→在古代] |  |  |
| (separate error in a note) | ⟦孟子⟧和孟母住了在靠墓地的家 | better to briefly introduce “孟子” when this character first appears |  |
| 住在靠近墓地的地方/墓地附近 | 孟子和孟母住了[在靠墓地的家→在靠近墓地的地方] | 在+Place | edits do not reproduce her fix; model unsure |
| delete了 | 孟子和孟母住[-了]在靠墓地的家 | 在+Place |  |
| 孟子 | [孩子→孟子]才五岁就每天在墓地祭拜了 | 孩子is vague and unclear |  |
| delete the second他的 | 他的学习和[-他的]旅行经验很重要 |  |  |
| 对他有很多好处 | [对他很多好处→对他有很多好处] |  |  |
| 长大以后，哲学家 | 他[是大人的时候，他成为很有名的哲人→长大以后，哲学家] |  |  |
| delete the first他 | [-他]是大人的时候 |  |  |
| wrong information, 搬家因为孟母觉得it is not good to imitate how to offer sacrifices | ⟦难怪她跟孩子搬家，原来买不了房⟧ | wrong information, 搬家因为孟母觉得it is not good to imitate how to offer sacrifices |  |
| 搬到了，另外一个城市 | 他们[搬了到→搬到了]别一个城市找工作 ; 他们搬了到[别一个→另外一个]城市找工作 | “别（的）” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other” |  |
| 不是常常有人吵架，就是很多人都大声说话 | 不是[人→常常有人]吵架 ; 就是[都叫→很多人都大声说话] |  |  |
| wrong information, 搬家因为孟母觉得it is not good to imitate how to buy and sell | ⟦在那儿，孟母也找不到工作⟧ | wrong information, 搬家因为孟母觉得it is not good to imitate how to buy and sell |  |
| 又搬了一次家 | 孟子和妈妈[-要]又一个次搬了家 ; 孟子和妈妈要[又一个次搬了家→又搬了一次家] | “要” is for future plan/desire, this already occurred |  |
| 找到了 | 孟母[找到→找到了]工作 | 了completed |  |
| 找到了 | 孟子在那个商店也[找了到→找到了]工作 |  |  |
| 在学校 | 孟子[学习馆→在学校]学了十五年 | 在+Place |  |
| 在古代 | [古代的时候→在古代] |  |  |
| 这个城市，只有 | [但是城市有才→这个城市，只有]两个学校 |  |  |
| delete不是不喜欢他们的城市 | 他的妈妈[-不是不喜欢他们的城市，]而是想孟子有很好的教育 | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong |  |
| 想让孟子接受…… | 而是[想孟子有很好的教育→想让孟子接受很好的教育] | 想 + V., cannot be followed by N. |  |
| delete他们 | [-他们]从早到晚走路 |  |  |
| 因为从早到晚走路，所以孟子一直抱怨 | [+因为]他们从早到晚走路 ; [+所以]孟子一直抱怨 |  | edits do not reproduce her fix |
| 难怪他抱怨 | [他难怪抱怨→难怪他抱怨] | 难怪 + sentence |  |
| 原来他想他的朋友，不想离开他的城市 | [+原来]他想他的朋友 ; [因为他不要→不想]离开他的城市 |  |  |
| 给孟子找到…… | 他的妈妈[找到孟子一个老师→给孟子找到一个老师] |  |  |
| 孟子跟老师学习文学 | [跟老师孟子→孟子跟老师]学最重要的文学 ; 跟老师孟子[学→学习]最重要的文学 ; 跟老师孟子学[-最重要的]文学 |  |  |
| “这个“ is specific, not for a character who first appears | ⟦这个⟧男孩子叫孟子 | “这个“ is specific, not for a character who first appears |  |
| 搬家 | 所以他们常常搬[-了]家 | no了for routine/habit |  |
| 孟子的妈妈望子成龙，所以安排他的生活 | [她→孟子的妈妈]望子成龙 ; 所以[-孟子的妈妈]安排他的生活 | otherwise the references are confusing ; otherwise the references are confusing |  |
| 搬家 | 因为他们常常搬[-了]家 | no了for routine/habit |  |
| 教了 | 妈妈[教→教了]孟子很多技能 | 了completed |  |
| 她先让…… | [先她让→她先让]孟子跟朋友玩儿 | Subj.先…… |  |
| 质量又好 | 然后教他怎么买又便宜[又好质量→质量又好]的东西 |  |  |
| delete很 | 古代的人[-很]不知道什么植物能吃 |  |  |
| delete也 | [-也]什么植物不能吃 |  |  |
| delete你的 | 吃不安全的植物对[-你的]身体有坏处 | redundant |  |
| 是很麻烦的情况 | [+是]很麻烦的情况 |  |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧ | better to briefly introduce “神农” when this character first appears |  |
| 写下，他的发现 | 神农写[+下]他的主意 ; 神农写他的[主意→发现] |  |  |
| it is unclear that夹竹桃refers to黄色的花 | 发现了⟦夹竹桃⟧有毒 | it is unclear that夹竹桃refers to黄色的花 |  |
| 另外一个人 | [别人→另外一个人]看到他 | “别(的)” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other” |  |
| 也会告诉他的朋友哪一个植物能吃，哪个植物不能吃 | [+也]会告诉他的朋友哪一个植物能不能吃 ; 会告诉他的朋友[哪一个植物能不能吃→哪一个植物能吃，哪个植物不能吃] |  |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧和他的家人住在古代 | better to briefly introduce “神农” when this character first appears |  |
| 常常生病 | 因为他的家人常常生病[-了] | no了for routine/habit |  |
| 去了 | 他们去[+了]很多不一样的地方 | 了completed |  |
| 河边，看到 | 他们[在很漂亮的河找→在很漂亮的河边，看到]夹竹桃 |  |  |
| 还是想要知道夹竹桃有没有毒 | 神农问他的哥哥：“我应该吃这种植物吗？”哥哥说：“这就要看你想要安全[还是接近知道了→还是想要知道夹竹桃有没有毒] |  |  |
| 有毒的 | 夹竹桃[是毒的→有毒的] |  |  |
| 灵芝有没有用/能不能帮他 | 我想知道灵芝[会帮他→有没有用/能不能帮他] |  | model unsure |
| 给了 | ”哥哥给[+了]神农灵芝 | 了completed |  |
| 你做得很好 | 你[帮得真好→做得很好] |  |  |
| 找到 | 他[找→找到]很多植物 | 找look for vs.找到find |  |
| 很大，在这儿也能找到植物 | 凉山[很大的山，这也找→很大，在这儿也能找到]植物 |  |  |
| 一种黄色的花 | 他找到[+一种]黄色的花 | “黄色的花“too general and too vague |  |
| delete你 | 他听说[-你]跟黄色的花做茶很有用 |  |  |
| 用…… | 他听说你[跟→用]黄色的花做茶很有用 |  |  |
| 头很疼，这种冰茶 | 你的[头发疼死→头很疼] ; [这→这种]冰茶是药 |  |  |
| 有毒 | [特别是毒→有毒] | 特别是+N，+ Clause |  |
| 可以做夹竹桃解药的灵芝他吃了 | [灵芝药的夹竹桃→可以做夹竹桃解药的灵芝]他吃完了 ; 灵芝药的夹竹桃他[吃完了→吃了] |  |  |
| 写下一篇有关植物的文章 | [-也]写一个课文的植物 ; 也[写→写下]一个课文的植物 ; 也写[一个课文的植物→一篇有关植物的文章] |  |  |
| 老人 | 有一个[老男人→老人]叫神农 | “老男人“ has negative meaning |  |
| delete “在古代”, it implies that 神农can travel between 古代 and 现代modern times | 神农[-在古代]每一天看到了别的小镇人生病还是不舒服 | it implies that 神农can travel between 古代 and 现代modern times |  |
| 都看到 | 神农在古代每一天[看到了→都看到]别的小镇人生病还是不舒服 | no了for routine/habit |  |
| 别的小镇上的人 | 神农在古代每一天看到了[别的小镇人→别的小镇上的人]生病还是不舒服 |  |  |
| 生病或者不舒服 | 神农在古代每一天看到了别的小镇人生病[还是→或者]不舒服 |  |  |
| 其他人 | 跟[别的人→其他人]分享他的发现 |  |  |
| 是真的吗 | 你认为神农的故事[+是]真的吗？这就要看你相信中药对身体有好处 |  |  |
| 相信不相信中药对身体有好处了 | 你认为神农的故事真的吗？这就要看你[相信中药对身体有好处→相信不相信中药对身体有好处了] |  |  |
| 第二天，当地的大山 | 他[下一天→第二天，]开始爬当地的山脉 ; 他下一天开始爬[当地的山脉→当地的大山] | 山脉is for geography |  |
| 有一次 | 他[一次→有一次]试一试有些植物的叶 |  |  |
| 试了试 | 他一次[试一试→试了试]有些植物的叶 | 了completed |  |
| 叶子 | 他一次试一试有些植物的[叶→叶子] |  |  |
| 吃起来 | [吃得→吃起来]又新鲜又甜 |  |  |
| 煮了 | 煮[+了]这些叶以后 | 了completed |  |
| 叶子 | 煮这些[叶→叶子]以后 |  |  |
| 很多新的植物 | 虽然他找到了很多[-的]新的植物 |  |  |
| 特别危险 | 但是他的旅程[-有的时候]特别是危险 ; 但是他的旅程有的时候特别[-是]危险 | ”特别是+N, + Clause” is used to single out a typical example |  |
| wrong information, 灵芝is a medicine | 他一吃⟦灵芝⟧就开始生病 | wrong information, 灵芝is a medicine |  |
| delete “的麻烦” | 一个爬山的男人正好看到神农[-的麻烦] |  |  |
| 回到小镇 | 神农最终[-他]的小镇回到 ; 神农最终他的[小镇回到→回到小镇] |  |  |
| 古代的时候，人们 | [古代时候，人→古代的时候，人们]不知道他们能吃什么植物 |  |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧出去试一试很多种植物 | better to briefly introduce “神农” when this character first appears |  |
| 是安全的，是危险的 | 告诉人什么植物是安全[+的]什么是危险 ; 告诉人什么植物是安全[+，]什么是危险 ; 告诉人什么植物是安全什么是危险[+的] |  |  |
| add他in the beginning | [+他]发现有的植物对身体非常好 |  |  |
| delete 感觉 | 让肚子[-感觉]又暖和又清楚 |  |  |
| 又暖和又舒服 | 让肚子感觉又暖和又[清楚→舒服] |  |  |
| 这就要看……了 | 这就要看你的口味[+了] |  | edits do not reproduce her fix |
| 什么花都想吃 | [什么都花想吃→什么花都想吃] |  |  |
| delete “他发现这个口味”, since it has no clear relationship with previous or following clauses | [-他发现这个口味] | since it has no clear relationship with previous or following clauses |  |
| 一百岁的时候，有毒的花 | 一百岁[+的]时候 ; 不小心吃了[毒的花→有毒的花] |  |  |
| 开始不舒服 | 一吃就[开始死→开始不舒服] | “死“ is instant, so cannot be with “开始” |  |
| 但是即使他生病了，也告诉……，有毒 | 但是[生病时候→即使他生病了，也]告诉人什么植物是药 ; 什么植物[是毒→有毒] |  |  |
| 来做药 | 所以他们找到了很多[植物对药→来做药] |  |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧先看到很多病人 | better to briefly introduce “神农” when this character first appears |  |
| 吃了很多植物 | 他们[吃很多植物对药→吃了很多植物] | 了completed |  |
| 另外一个人 | [别的人→另外一个人]给了神农一个灵芝 | “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other” |  |
| 身体更好 | 这个植物可以让[神农更好→身体更好] |  |  |
| 比方说is used to express “for example”, delete it | [-比方说，]他会觉得更健康 | 比方说is used to express “for example”, delete it |  |
| 吃了 | [吃→吃了]灵芝以后 | 了completed |  |
| 又可以走了 | 他[可以再走→又可以走了] |  |  |
| 他们吃的植物让他们生病 | 但是我觉得他们[-的]吃的植物 ; 但是我觉得他们的吃的植物[-，]让他们病人 ; 让他们[病人→生病] | 让Sb. + V./Adj. |  |
| 可能毒性特别强 | 神农觉得这个植物[可能特别是毒→可能毒性特别强] | ”特别是+N, + Clause” is used to single out a typical example |  |
| 找一个可以做药的植物 | 所以他想[找一个植物对药→找一个可以做药的植物] |  |  |
| 这样，他们可以…… | 所以他想找一个植物对药[，他们→这样，他们]可以吃对药 |  |  |
| 做成药 | 他想把花[放在茶里，对药→做成药] |  |  |
| 不知道这种花对身体好不好 | [他不知道如果这把花对你的身体好→他不知道这种花对身体好不好] | the “if” in “not know if + clause” is not 如果 |  |
| 有没有毒 | 这就要看[-如果]这把花毒不毒了 ; 这就要看如果这把花[毒不毒了→有没有毒] | the “if” in “not know if + clause” is not 如果, delete如果 |  |
| 另外一种花 | 他找到了[别的花→另外一种花] | “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other” |  |
| 要不要吃…… | 神农不知道他[吃不吃→要不要吃]灵芝或者夹竹桃 |  |  |
| 对身体有好处 | 也不知道什么植物对[-你的]身体有好处 | not你的 |  |
| 很严重better，usually糟糕for情况situations | 这个问题神农觉得很⟦糟糕⟧ | 很严重better，usually糟糕for情况situations |  |
| 去吃了 | 所以神农[去了吃→去吃了]每种植物 |  |  |
| 写下了 | 就[写了→写下了]这个植物对你有没有好处 |  |  |
| delete“对你” | 就写了这个植物[-对你]有没有好处 |  |  |
| 吃到了 | 神农[吃了→吃到了]很好吃的植物 ; 他[吃了→吃到了]很危险的植物 | V + resultative ; V + resultative |  |
| 会跟…… | 会[-来]跟他的朋友聊到他吃的植物了 ; 会来跟他的朋友聊到他吃的植物[-了] | no了 |  |
| 另外一个人 | [一个别的人→另外一个人]问神农 | “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other” |  |
| 第三个人 | [一个别的人→第三个人]问神农 |  |  |
| 大脑 | 就觉得这种植物对我的[脑→大脑]有坏处 |  |  |
| 一个男人正好过来，看到我的旁边长着一个灵芝 | [一个灵芝和一个男人正好在我的旁边→一个男人正好过来，看到我的旁边长着一个灵芝] | “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two |  |
| 吃植物得小心 | [你得小心吃植物→吃植物得小心] |  |  |
| delete“对你” | 因为有的植物[-对你]的健康有坏处 |  |  |
| 医生 | 他需要当上[医→医生] |  |  |
| 看到 | 一[看→看到]别的人就想帮助他们 | 看look vs.看到see |  |
| 病人 | 一看[别的人→病人]就想帮助他们 | “别的” is for “a different type”, and “all else except the spoken one” |  |
| delete the second他 | 他找到药以后[-他]写下怎么做药在书上 | redundant |  |
| 在书上写下…… | 他找到药以后他[写下怎么做药在书上→在书上写下怎么做药] |  |  |
| 这样，有好处 | [那红灵芝→这样，]对身体好处 ; 那红灵芝对身体[+有]好处 |  | model unsure |
| 吃了以后 | 什么病人[吃→吃了以后]都会觉得身体更好 |  |  |
| 走了三个月 | 神农[三个月走去→走了三个月] |  |  |
| 这一定是一种做药的花 | [这种→这一定是一种]一定是做药的花 |  | edits do not reproduce her fix |
| 结果 | [原来→结果]他想错了 | “原来” is to explain the reason while “结果” is to describe an unexpected result |  |
| 很快就生病了 | 神农[快生病→很快就生病了] |  |  |
| 很快地给了 | [快给→很快地给了]他一种红的灵芝 | 快V: to give order, 了completed |  |
| delete他 | [-他]没有病 | redundant |  |
| 病好了 | 他[没有病→病好了] |  |  |
| 家人 | 一回家就告诉[别人→家人] |  |  |
| 吃了植物以后 | 有很多人[吃植物以后→吃了植物以后]就吃坏肚子了 | 了completed |  |
| 吃了有毒的植物 | 因为他们[吃了毒→吃了有毒的植物] |  |  |
| 吃到 | 他希望别人也可以[吃→吃到]好吃的植物 | with result |  |
| 写下来了 | 他[测量起来了→写下来了] |  |  |
| 吃到有毒的植物，就不会吃到好吃的植物 | [如果他们还怕吃毒→吃到有毒的植物] ; [+就]不会吃他喜欢的植物 ; 不会吃他[喜欢→到好吃]的植物 |  | edits do not reproduce her fix |
| delete他 | 不会吃[-他]喜欢的植物 |  |  |
| 他是第一个找到茶的人 | 他是[第一人，找到了茶→第一个找到茶的人] |  |  |
| 一直都在吃不同的植物 | 他[一直都吃了→一直都在吃不同的植物] |  |  |
| delete the second他 | [-他]连毒都能吃 |  |  |
| 没吃过 | 可是他[还没吃了→没吃过]一个叫夹竹桃的植物 | 了is not in “没+V.”, “过” expresses “experience” |  |
| 很强 | 可是夹竹桃的毒[很重→很强] |  |  |
| 快要死了 | 觉得他快[-会]死了 |  | edits do not reproduce her fix |
| 有人 | 可是正好[有别人→有人]找到他了 | “别(的)” is for “a different type”, and “all else except the spoken one” |  |
| 吃了 | 他[吃→吃了]灵芝以后就觉得很好 | 了completed |  |
| 看到，一……就 | [一看→一看到]很多人正在吃一些植物 |  | edits do not reproduce her fix |
| 帮他们 | 神农想帮[别人→他们] | “别(的)” is for “a different type”, and “all else except the spoken one” |  |
| 真好吃 | 一些植物[吃真好→真好吃] |  |  |
| 毒性强得很 | 一些植物[毒得很→毒性强得很] |  |  |
| 麻烦告诉我们…… | [麻烦我们可以→麻烦告诉我们]吃什么植物？神农说 |  |  |
| 后来 | [以后→后来] | Time+以后 |  |
| 告诉人们 | 神农告诉[别人→人们]一些植物能吃 | “别(的)” is for “a different type”, and “all else except the spoken one” |  |
| 哪些，哪些 | 神农告诉别人[一些→哪些]植物能吃 ; [一些→哪些]植物不能吃 |  |  |
