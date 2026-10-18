# Step 5 report: aligning the teacher's corrections (train)

- model gpt-5.6-terra, reasoning effort medium, prompt 93779976b8
- feedback lines: 729 (0 from cache); tokens: {'prompt_tokens': 734706, 'completion_tokens': 119924, 'total_tokens': 854630}
- teacher items: 954 -> edits: 1143 (replace 660, delete 200, insert 143, comment 130, unplaceable 10)
- extra comment edits for a separate error in a note: 17
- items with no problem found by the checks: 882 of 954

## Problems found by the checks

| Problem | Items |
|---|---|
| edits do not reproduce her fix | 35 |
| model unsure | 22 |
| edit edge inside a HanLP word | 13 |
| could not place | 10 |
| not found in the text | 3 |
| no edit returned | 2 |

## All items

| Teacher's piece | Edits as read by the model | Her note | Check |
|---|---|---|---|
| 有一个叫孟子的小孩子 | 有[一位小孩子叫孟子→一个叫孟子的小孩子] | “位” is a polite MW. |  |
| 作家的家里找到工作了 | 孟母终于[在一位很有名的文学家找工作了→作家的家里找到工作了] | 找look for vs. 找到find |  |
| 房子里 | 他每天在文学家的[房子上→房子里]学 | 在+Place | edit edge inside a HanLP word |
| 在被问到对童年应该做什么的看法时，他说：孩子童年多玩重要和多学习重要 | [他对孩子的童年的看法是，说→在被问到对童年应该做什么的看法时，他说：]孩子童年多玩或者多学习重要 ; 说孩子童年多玩[或者→重要和]多学习重要 |  |  |
| 幸福的生活 | (unplaced replace: 良好的生活→幸福的生活) | 良好 is usually not with生活 | not found in the text: 我现在有[良好的生活]。 |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧小的时候 | better to briefly introduce “孟子” when this character first appears |  |
| delete他 | [-他]跟他的妈妈住在一个小房子 |  |  |
| 住在一个小房子里 | 他跟他的妈妈住在一个小房子[+里] | 在Place |  |
| 这个小房子 | [小房子→这个小房子]离一个墓地不太远 | otherwise unclear which house |  |
| 一年搬了三次家 | [一天三次搬家了→一年搬了三次家] | V. + Num. + MW. + Obj. |  |
| 有好处/有好的影响 | 搬家[对孟子好处影响→对孟子有好处] |  | edits do not reproduce her fix |
| delete the second他 | [-他]难怪成为了一个很聪明的哲学家 |  |  |
| 难怪后来…… | 他难怪[+后来]成为了一个很聪明的哲学家 |  |  |
| delete the first他 | [-他]住在学校的旁边影响了他 |  |  |
| no了for routine/habit | 孟子一直跟他的朋友⟦去了⟧墓地祭拜 | no了for routine/habit |  |
| 不想让他跟朋友去墓地 | 他的妈妈[不想跟他的朋友去墓地→不想让他跟朋友去墓地] | otherwise it means his mother didn’t want to go with his friend to the graveyard. |  |
| 他们才在那儿住了一个星期，就又搬家了 | 他们才[一个星期住在那儿→在那儿住了一个星期] ; 孟子跟他的妈妈[已经→就又]搬家了 | 在Place住 |  |
| delete孟子跟他的妈妈 | [-孟子跟他的妈妈]已经搬家了 |  |  |
| 他们搬到了一个在购物中心旁边的房子 | 他们[去了→搬到了]一个房子 ; 他们去了[一个房子，在购物中心的旁边→一个在购物中心旁边的房子] |  |  |
| 睡不好觉 | 害得孟子[不可以睡觉好→睡不好觉] |  |  |
| 又应该搬家了 | 妈妈觉得他们[应该又搬家了→又应该搬家了] | 又+ modal V. |  |
| 搬到了学校旁边 | 他们[不是住在购物中心的旁边，而是住在学校的旁边→搬到了学校旁边] | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong |  |
| delete现在 | 他小的时候[-现在]读书最重要 |  |  |
| 在古代 | [古代的时候→在古代] |  |  |
| (separate error in a note) | ⟦孟子⟧和他的妈妈住在离墓地很近 | better to briefly introduce “孟子” when this character first appears |  |
| 住在离墓地很近的地方 | 孟子和他的妈妈[住在离墓地很近→住在离墓地很近的地方] | 住在+Place |  |
| 又生气又紧张 | 害得他的妈妈[很生气紧张→又生气又紧张] |  |  |
| 一直没在读书 | 而是因为住在那里以后孟子一直[在没读书→没在读书] |  |  |
| 搬到…… | 所以孟子的妈妈[搬家→搬到]很安全很安静的公寓 |  |  |
| 给孟子的压力 | [家教对→给]孟子的压力很大 |  |  |
| 不是学习历史，就是学习哲学 | 从早到晚他[学习不是历史，就是哲学→不是学习历史，就是学习哲学] |  |  |
| 有名的 | 难怪他成为[名的→有名的]哲学家 |  |  |
| 在古代，有一个叫孟子的男孩子和他的妈妈住在一起 | [古代的时候→在古代] ; 有[一个男孩子叫孟子和他的妈妈→一个叫孟子的男孩子和他的妈妈住在一起] |  |  |
| delete她 | [-她]搬家搬了三次了 |  |  |
| wrong information, it’s not about房租 | 不是⟦房租太贵了⟧ | wrong information, it’s not about房租 |  |
| 在古代，孟子一家人住在中国 | [古代的时候→在古代] ; [一个家人→孟子一家人]住在中国 |  |  |
| (separate error in a note) | ⟦一个家人⟧住在中国 | better to briefly introduce “孟子” when this character first appears |  |
| delete觉得 | [-觉得]害得孟子的身体 |  |  |
| 害得孟子的身体不好 | 觉得害得孟子的身体[+不好] | 害得+harmful result |  |
| 妈妈带孟子搬家了 | [-所以]妈妈跟孟子一起搬家 ; 所以妈妈[跟孟子一起→带孟子]搬家 ; 所以妈妈跟孟子一起搬家[+了] | 了completed |  |
| 新家在市场附近 | [下个家→新家]在很忙的地方 ; 下个家在[很忙的地方→市场附近] | “忙“ is for people |  |
| 又搬家了 | 所以他们[再搬家→又搬家了] | 又for something already occurred |  |
| 在新的房子里 | 在新的房子[+里] | 在+Place |  |
| 在古代 | [古代的时候→在古代] |  |  |
| (separate error in a note) | ⟦孟子⟧跟妈妈一起住在西安 | better to briefly introduce “孟子” when this character first appears |  |
| 很爱孩子 | 孟子的妈妈[爱她的小孩子→很爱孩子] |  |  |
| delete她的 | 孟子的妈妈爱[-她的]小孩子 |  |  |
| “每天“ and ”老是” are redundant, delete老是or replace每天with老是，and delete the second老是 | 她以为孟子每天出去跟别的小孩子在马路上[-老是]玩游戏 | “每天“ and ”老是” are redundant, delete老是or replace每天with老是，and delete the second老是 | model unsure |
| delete the second他 | 而是[-他]祭拜 |  |  |
| 搬家对他有好处 | [可是他知道他们帮助了→搬家对他有好处] |  |  |
| 在搬家的十年里 | [搬家十年→在搬家的十年里] |  |  |
| 一直在学习 | 孟子[一直学了→一直在学习]很多东西 | 一直在+V., emphasizing always ongoing |  |
| replace the second孟子with他 | [孟子→他]每个地方才住了一年 | replace the second孟子with他 |  |
| 带给孟子的不是悲伤的童年，而是幸福的童年 | 搬家带给[-了]孟子不是悲伤的童年 ; 搬家带给了孟子[+的]不是悲伤的童年 ; 而是[很高兴→幸福]的童年 | 高兴is for short-term and can change quickly，幸福is for long-term, life-related happiness |  |
| 了解了 | 旅行的时候孟子[经验→了解了]很多的看法 | “经验” is a noun., 了completed |  |
| 新知识 | 孟子不是学[新的东西→新知识] |  |  |
| 学习新知识，很聪明的人 | 孟子从早到晚[学了新的东西→学习新知识] ; 难怪他成为很聪明[+的人] |  |  |
| 旅行了很长时间 | 孟子跟他的妈妈[旅行很多时间→旅行了很长时间] | 了completed |  |
| 在古代，“她”，有一个妈妈和她的儿子住在一起，儿子叫孟子 | [古代的时候→在古代] ; 有一个妈妈和[他→她]的儿子 ; 有一个妈妈和他的儿子[+住在一起] ; [这个小孩子→儿子]叫孟子 | “这个小孩子” is unclear and ambiguous |  |
| 带孟子搬到城市了 | 所以她带孟子[-到一个]城市搬家了 ; 所以她带孟子到一个[城市搬家了→搬到城市了] |  |  |
| delete马虎地 | 在马路上[-马虎地]玩 | 马虎 is used to describe “careless, so there are a lot of errors” |  |
| 搬到城市外了 | 所以他们[到城市的外边搬家了→搬到城市外了] |  |  |
| delete和 | 孟子才四岁就开始学文学[-和]写汉字 | 和cannot connect verb phrases |  |
| 得到老师的帮助 | 每天[受到→得到]老师的帮助 |  |  |
| 知识 | 学了很多[东西→知识] |  |  |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧一直祭拜 | better to briefly introduce “孟子” when this character first appears |  |
| 就开始…… | [+就]开始祭拜 | 才 Num.就V. |  |
| 一个写文章非常好的作家 | 他成为了[一个人写文章老是好→一个写文章非常好的作家] |  |  |
| 孟子和他的妈妈常常在祭拜以后一起去买东西 | [常常祭拜以后→常常在祭拜以后] ; [孟子和他的妈妈一起→孟子和他的妈妈常常在祭拜以后一起]去买东西 |  |  |
| 孟子练习写字 | [+孟子]练习写文字 ; 练习写[文字→字] | miss a Subj. ; 文字 is a general term, not for specific individual characters |  |
| 写字，想要他练习 | 不是他喜欢学习[写文字→写字] ; [而是他的爸爸喜欢→想要]他练习 |  |  |
| wrong information, his father did not appear in this story | 而是⟦他的爸爸⟧喜欢他练习 | wrong information, his father did not appear in this story |  |
| wrong information, his father did not appear in this story | ⟦他爸爸说⟧ | wrong information, his father did not appear in this story |  |
| 都没有空 | 所以孟子[从早到晚没有空→都没有空] |  |  |
| 病得很重 | 一天孟子[病了很重→病得很重] |  |  |
| 吃了 | 原来他昨天吃[+了]一张纸 | 了completed |  |
| 长大以后，他还想得起来不要吃纸 | [是大人的时候→长大以后] ; 他还想[+得]起来 ; 他还想起来[-，]别吃纸 ; [别→不要]吃纸 |  |  |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧和他的妈妈一直在搬家 | better to briefly introduce “孟子” when this character first appears |  |
| 他们一共搬了两次家 | [一共他们→他们一共]搬了两次家 |  |  |
| 死去的家人 | 孟子和孟母从早到晚都在墓地帮别人祭拜他们的[死家人→死去的家人] |  |  |
| 碰到麻烦 | 可是他们[老是有问题→碰到麻烦] |  |  |
| delete他们的 | 可是[-他们的]收入也很低 |  |  |
| 好工作 | 孟母找到了[良好的工作→好工作] | 良好is not with工作 |  |
| delete她, redundant | [-她]挣不少钱 | redundant |  |
| 接受教育 | 孟母一直觉得[受到教育→接受教育]很重要 |  |  |
| be more specific, 什么经验？ | 原来他的⟦经验很多⟧ | be more specific, 什么经验？ |  |
| 很多人认为 | [很多人想→很多人认为]孟子做哲学家是本质的 | 想 + V., cannot be followed by N. |  |
| 孟子成为哲学家是有天赋 | 很多人想孟子[做→成为]哲学家是本质的 ; 很多人想孟子做哲学家是[本质的→有天赋] |  |  |
| better to briefly introduce “孟子” when this character first appears | 很多人想⟦孟子⟧做哲学家是本质的 | better to briefly introduce “孟子” when this character first appears |  |
| 成为有名的哲学家，有做哲学家的天赋 | 但是他[做厉害的哲学家→成为有名的哲学家]的原因不是因为他本质上是哲学家 ; 但是他做厉害的哲学家的原因不是因为他[本质上是哲学家→有做哲学家的天赋] |  |  |
| 搬了两次家 | 他们[搬了家两次→搬了两次家] | V. + Num. + MW. + Obj. |  |
| add原来 | [+原来]他成长在学校的旁边 |  |  |
| 他在学校旁边长大 | [他成长在学校的旁边→他在学校旁边长大] |  |  |
| 在什么地方成长 | 孟母觉得孩子[成长在什么地方→在什么地方成长]很重要 | 在Place + V. |  |
| 对……没有好处 | 孟母觉得这个环境[不对孩子的成长有好处→对孩子的成长没有好处] |  | edits do not reproduce her fix |
| delete他 | [-他]就不会成为好的大人 | redundant |  |
| 就不会成才 | 他就不会[成为好的大人→成才] |  |  |
| 害得+harmful result, 搬家itself is not harmful | 这个想法⟦害得她跟孟子搬家⟧ | 害得+harmful result, 搬家itself is not harmful |  |
| 他们的新家 | [他们新的家→他们的新家]在商店的旁边 |  |  |
| delete the two在 | 孟子不是[-在]看商店的员工 ; 就是[-在]跟其他的孩子玩商店的游戏 | here is not emphasizing “ongoing” ; here is not emphasizing “ongoing” |  |
| 又搬了一次家 | 所以他们[再搬家一次→又搬了一次家] | 了completed, 又for something already occurred |  |
| 一直 | 所以孟子[老是→一直]在学习 | “老是“ for something negative, used to complain |  |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧生活在古代 | better to briefly introduce “孟子” when this character first appears |  |
| 看到 | 孟母[一看→看到]孟子祭拜 | 看look vs.看到see |  |
| “老是“ for something negative, used to complain | 孟母⟦老是⟧搬家 | “老是“ for something negative, used to complain |  |
| 这样in this way | ⟦孟母老是搬家，所以孟子会跟别的教授学哲学⟧ | 这样in this way | model unsure |
| 学习很厉害 | 他学习[-得]很厉害 | V.得很厉害for something negative, with a high degree |  |
| 害得孩子的生活不稳定 | 有的人觉得常常搬家害得孩子的生活[+不稳定] | 害得 + harmful result |  |
| 打过交道 | 他跟很多人[打交道→打过交道] | “过” for “have done, experience” |  |
| 所以，取得了很多生活经验 | [结果他取得生活经验→所以，取得了很多生活经验] | “结果” for unexpected result, 了completed |  |
| 在古代，有一个孩子和他的妈妈住在一起 | [古代的时候→在古代] ; 有一个孩子和他的妈妈[+住在一起] |  |  |
| 很淘气 | 孟子[是淘气的孩子→很淘气] |  |  |
| add他, wrong information, not “eating the sacrifices” | 因为[+他]老是去墓地吃祭品 |  |  |
| (separate error in a note) | 因为老是去墓地⟦吃祭品⟧ | wrong information, not “eating the sacrifices” |  |
| 我们 | 所以[他们→我们]要搬家 | in quoted speech |  |
| add a Subj., wrong information, not “eating the sacrifices” | (unplaced unplaceable: 在新家，一直去墓地吃祭品→) | add a Subj., wrong information, not “eating the sacrifices” | could not place: teacher requests an unspecified subject and indicates the sentence’s information is wrong without supplying a replacement; model unsure |
| delete the second你, redundant | [-你]就太淘气了 | redundant |  |
| 就那么淘气 | 你就[太→那么]淘气了 |  |  |
| 都饿得很 | 因为我[从早到晚→都]饿得很 |  |  |
| 食物 | 妈妈说：我知道我们没有[食品→食物] | 食品is for processed food |  |
| 你应该学习 | 你[可以→应该]学习 |  |  |
| delete年 | 他才四[-年]岁 |  | edit edge inside a HanLP word |
| 孟子跟朋友看别人祭拜 | [-从早到晚]孟子跟小朋友看祭拜 ; 从早到晚孟子跟[-小]朋友看祭拜 ; 从早到晚孟子跟小朋友看[+别人]祭拜 |  | edit edge inside a HanLP word |
| 让她…… | [害得→让]她很不高兴 | 害得 + harmful result，不高兴is not that “harmful” |  |
| 学习/读书 | 妈妈让他[学读书→学习/读书] |  |  |
| 不在家读书，老是出去玩 | 可是他不[-是]在家读书 ; [-而是]老是出去玩 | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong ; “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong | edit edge inside a HanLP word |
| loosely connected, unclear between-sentence relationship | ⟦妈妈让孟子每天上课，孟子长得很乖，很聪明⟧ | loosely connected, unclear between-sentence relationship |  |
| 一个小城市 | 孟子和孟母住在[小的城→一个小城市] |  |  |
| (separate error in a note) | ⟦孟子⟧和孟母住在小的城 | better to briefly introduce “孟子” when this character first appears |  |
| 看到 | 孟子跟朋友[看→看到]很多的大人在墓地祭拜 | 看look vs.看到see |  |
| delete the second孟子决定 | [-孟子决定]他可以学习和高兴 |  |  |
| delete他应该 | 孟子决定[-他应该]学哲学 |  |  |
| 这样又能学习又能每天都很高兴 | 孟子决定[他可以学习和高兴→这样又能学习又能每天都很高兴] |  |  |
| 住在那儿很高兴 | 孟母和孟子[住了很高兴→住在那儿很高兴] |  |  |
| loosely connected with the preceding sentence | ⟦孟子从早到晚想玩玩儿，所以他和朋友坐墓地在祭拜⟧ | loosely connected with the preceding sentence |  |
| delete the second他 | (unplaced unplaceable: 他→) | replace孟子with他 | could not place: the quote contains only one 他, so “delete the second 他” cannot be located; the note conflicts with the instruction; model unsure |
| 都想玩儿 | 孟子从早到晚[+都]想玩玩儿 ; 孟子从早到晚想[玩玩儿→玩儿] | V.V. is used to make requests or plans |  |
| 坐在墓地祭拜 | 所以他和朋友[坐墓地在祭拜→坐在墓地祭拜] |  |  |
| 这个小城市 | 孟母觉得孟子不喜欢[他的小的城→这个小城市] | “他的……” indicates that孟子owns this city |  |
| 在新城市，想玩 | 在[新的城→新城市] ; [-孟子老是]想玩玩 ; 孟子老是想[玩玩→玩] | V.V. is used to make requests or plans |  |
| 玩 | 在家不是学习就是[玩玩→玩] | V.V. is used to make requests or plans |  |
| 害得孟子+harmful result, 常常玩 | 孟母觉得⟦学习害得孟子⟧ ; 所以孟子⟦常常玩玩⟧ | 害得孟子+harmful result, 常常玩 ; 害得孟子+harmful result, 常常玩 |  |
| “所以” is not appropriate, since here is not a cause-effect relationship | ⟦所以⟧孟子常常玩玩 | “所以” is not appropriate, since here is not a cause-effect relationship |  |
| no logic relationship, fractured | ⟦不是学习害得，而是常常搬家⟧ | no logic relationship, fractured |  |
| 学习/一直学习 | 难怪他不喜欢[常常学习→学习/一直学习] |  | model unsure |
| no logic relationship with the preceding or following sentences | ⟦孟子是孩子⟧ | no logic relationship with the preceding or following sentences |  |
| 在古代 | [古代的时候→在古代] |  |  |
| (separate error in a note) | ⟦孟子⟧的妈妈跟孟子一起住在中国 | better to briefly introduce “孟子” when this character first appears |  |
| 就开始 | 孟子才三岁[+就]开始搬家 | 才Num.就V. |  |
| (separate error in a note) | ⟦以后每年搬家⟧ | 后来每年都搬家 |  |
| 知识 | 但是他学到了很多[学习→知识] |  |  |
| 工作，新朋友 | 孟子的妈妈每天从早到晚[-做]工作 ; 所以孟子每天不是去上课就是跟[新人→新朋友]一起聊天 | 新人means newly married couple |  |
| 了解了 | 孟子[看→了解了]很多不同的文化 | 了completed |  |
| 每次搬家都学到了很多知识，后来他变得越来越聪明 | [他们搬家每次学到了比较多→每次搬家都学到了很多知识] ; [结果→后来]他成为很聪明的人 ; 结果他[成为很聪明的人→变得越来越聪明] | “结果” is for unexpected result ; 成为 + profession/celebrity |  |
| 成为 | 难怪他长大以后[当→成为]很有名的哲学家 |  |  |
| 在古代，跟妈妈住 | [在古代的时候→在古代] ; [他一直住跟他的妈妈→跟妈妈住] |  |  |
| delete别的人 | 孟轲老是看看[-别的人] |  |  |
| 老是去看 | 孟轲[老是看看→老是去看]别的人 |  |  |
| 出家门的时候 | 难怪孟轲的妈妈[出家→出家门]的时候看看她的儿子做一样的事情 | 出家become a monk |  |
| 看到 | 难怪孟轲的妈妈出家的时候[看看→看到]她的儿子做一样的事情 | 看look vs.看到see |  |
| delete the second他们 | [-他们]住离一个学校很近 |  |  |
| 住在一个离学校很近的地方 | 他们[住离一个学校很近→住在一个离学校很近的地方] |  |  |
| 变得很聪明 | 才几个星期就[成为很明智→变得很聪明] | 成为 + N. (profession/celebrity) |  |
| 他没有当医生，而是成为哲学家 | 他[那不是→没有]成为医生 ; 他那不是[成为医生→当医生] ; 而是成为[哲学人→哲学家] | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong |  |
| 哲学家，很聪明也很重要 | [哲学人→哲学家]很聪明和重要 ; 哲学人很聪明[和→也很]重要 | 和cannot connect Adj. |  |
| 在古代 | [古代的时候→在古代] |  |  |
| better to briefly introduce “孟子” when this character first appears | 可是小孩子⟦孟子⟧老是祭拜的时候行为不端 | better to briefly introduce “孟子” when this character first appears |  |
| 在祭拜的时候 | 可是小孩子孟子[老是祭拜的时候→在祭拜的时候]行为不端 |  |  |
| delete可是 | [-可是]孟子的妈妈一直很控制他 |  |  |
| 害得 + harmful result, “不高兴” is not that “harmful” | ⟦害得他不高兴⟧ | 害得 + harmful result, “不高兴” is not that “harmful” |  |
| 无聊？add所以 | 因为他这么[无→无聊] ; [+所以]他们常常搬家 | 无聊？add所以 ; 无聊？add所以 | model unsure |
| 只有 | 孟子[才有→只有]一个朋友 |  |  |
| 然后孟子失去了这个朋友 | [他然后没有朋友→然后孟子失去了这个朋友] | “他“ is ambiguous |  |
| 思考 | 他整天不是[思维→思考]就是读书 | “思维“ is a noun |  |
| 在古代 | [古代的时候→在古代] |  |  |
| (separate error in a note) | ⟦孟子⟧和孟母住在一起 | better to briefly introduce “孟子” when this character first appears |  |
| 害得孟子受到了不好的影响 | 害得[对孟子有→孟子受到了]不好的影响 | 害得+Sb.+V. |  |
| 就跟孟母搬了三次家 | [+就]跟孟母一起搬家三次 ; 跟孟母[-一起]搬家三次 ; 跟孟母一起[搬家三次→搬了三次家] | 才 Num.就V. ; 了completed，V. + Num. + MW. + Obj. |  |
| 为了住在更好的房子里 | 他们搬家不是为了[-孟母要]住在更好的房子 ; 他们搬家不是为了孟母要住在更好的房子[+里] | delete孟母 ; 在+Place |  |
| 还是从早到晚都努力学习 | [虽然一直学习很厉害，孟子从早到晚努力学习→孟子还是从早到晚都努力学习] |  |  |
| 在古代 | [在古代的时候→在古代] |  |  |
| (separate error in a note) | ⟦孟子⟧不是跟朋友玩 | better to briefly introduce “孟子” when this character first appears |  |
| 看书、写文章 | 从早到晚[看和写文章→看书、写文章] | 和cannot connect verb phrases |  |
| 一直 | 他写汉字[老是→一直]写得很好 | “老是“ for something negative, used to complain |  |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧长大的时候一直搬家 | better to briefly introduce “孟子” when this character first appears |  |
| 小时候 | 孟子[长大的时候→小时候]一直搬家 |  |  |
| 才搬了三次 | 可是[搬才→才搬]三次就找到好的地方 ; 可是搬[+了]才三次就找到好的地方 | 才V. + Num. ; 了completed | edits do not reproduce her fix |
| 会害得你学习不好 | 孟子说：我为什么老是学习？不能跟别人玩？他的妈妈说：跟别人玩[+会]害得你不学习好 ; 孟子说：我为什么老是学习？不能跟别人玩？他的妈妈说：跟别人玩害得你[不学习好→学习不好] |  |  |
| 成为有名的哲学家 | 所以他成为[聪明也有名字的人→有名的哲学家] |  |  |
| 在古代，孟子和孟母住在墓地边 | [古代的时候→在古代]住了孟子和孟母 ; 古代的时候[住了孟子和孟母→孟子和孟母住在墓地边] |  |  |
| (separate error in a note) | 古代的时候住了⟦孟子⟧和孟母 | better to briefly introduce “孟子” when this character first appears |  |
| 孟母是孟子的妈妈 | 孟母[-不是孟子的爸爸，而]是孟子的妈妈 | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong | edit edge inside a HanLP word |
| 生活了五年后 | 在那里生活[+了]五年后 | 了completed |  |
| no cause-effect relationship, so “所以” is inappropriate | ⟦所以⟧他们最后搬到了寺庙 | no cause-effect relationship, so “所以” is inappropriate |  |
| wrong information, it’s not a temple but a school | 所以他们最后搬到了⟦寺庙⟧ | wrong information, it’s not a temple but a school |  |
| “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong, 画画儿 is not a conventional activity related to 寺庙 | ⟦不是画画儿，而是祭拜⟧ | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong, 画画儿 is not a conventional activity related to 寺庙 |  |
| wrong information, 哲学家 | 孟子长大了以后⟦成为一名画家⟧ | wrong information, 哲学家 |  |
| 在古代 | [在古代的时候→在古代] |  |  |
| 搬得太频繁了 | 你可能认为孟母[搬家搬得乱→搬得太频繁了] |  |  |
| 他也理解…… | [也他→他也]就理解他妈妈的做法 ; 也他[-就]理解他妈妈的做法 | Subj.也 |  |
| 学习社会经验 | 他[学社会→学习社会经验] |  |  |
| 想让 | 孟母一直想[+让]她的孩子受到良好的教育 | 想 + V., cannot be followed by N. |  |
| 儿子 | 难怪她的[男孩子→儿子]成为孟子 | 男孩子boys, not have the meaning of son |  |
| 哲学家 | 难怪她的男孩子成为[孟子→哲学家孟子] |  |  |
| delete the second她 | 而是[-她]望子成龙 | Subj.不是……而是…… |  |
| 他们第一次搬家是在墓地住 | [第一次他们搬家，→他们第一次搬家是]他们在墓地住 |  | edits do not reproduce her fix |
| delete the second他们 | [-他们]在墓地住 | redundant |  |
| 很影响 | 墓地的人[真→很]影响孟子 | “真” is usually used in conversation |  |
| 没有一个快乐的童年 | 所以孟子没有[好的→一个快乐的]童年 |  |  |
| 第二次搬家是在城市住 | 第二次[，他们→搬家是]在城市住 |  |  |
| 听到 | 他们[听→听到]饭馆和商店 | 听listen vs.听到hear |  |
| 在饭馆和商店人们说话的声音 | 他们听[饭馆和商店→在饭馆和商店人们说话的声音] |  |  |
| delete他 | [-他]想找工作 |  |  |
| add就 | [+就]他想找工作 | 才Num.就V. |  |
| 在农村住 | 他们在农村[-上]住 |  |  |
| 日程schedule | ⟦每天孟母安排孟子的爱好⟧ | 日程schedule |  |
| 在古代 | [古代的时候→在古代]有一个男人叫孟子 |  |  |
| 孟子的妈妈 | [他的→孟子的]妈妈告诉他：你不能祭拜 | “他的” is ambiguous |  |
| delete你不是祭拜 | [-你不是祭拜] |  |  |
| 而是要多学习 | [而是学习很多→而是要多学习] |  |  |
| 每个人都…… | 这样每个人[+都]会知道你最聪明 |  |  |
| 去了 | [去→去了]一个最好的学校 | 了completed |  |
| no “semantic turn” relationship, so可是is inappropriate | ⟦可是⟧他很聪明 | no “semantic turn” relationship, so可是is inappropriate |  |
| 虽然孟子的生活不快乐，可是妈妈很开心 | [不是孟子幸福的生活就是孟子的妈妈开心→虽然孟子的生活不快乐，可是妈妈很开心] |  |  |
| 不是……就是……is used for “either…or…” | ⟦不是孟子幸福的生活就是孟子的妈妈开心⟧ | 不是……就是……is used for “either…or…” |  |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧和他的妈妈原来住在墓地的旁边 | better to briefly introduce “孟子” when this character first appears |  |
| 一直哭 | 但是孟子一直哭[-了] | it’s not about “completion”, no了 |  |
| 他的妈妈 | [她→他的妈妈]认为搬家对孟子有好处 | “她” is ambiguous |  |
| 搬家到 | 所以他们[搬家去→搬家到]商店的旁边 |  |  |
| add那儿 | 但是[+那儿]什么时候都太吵了 |  |  |
| 很难安静学习 | 孟子[学习很难→很难安静学习] |  |  |
| “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong, 商店is not conventionally related to对教育有好处 | ⟦不是商店而是学校⟧ | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong, 商店is not conventionally related to对教育有好处 |  |
| 决定is a mental state verb, no了 | 她决定[-了]以后搬出去学校的旁边 | 决定is a mental state verb, no了 |  |
| 搬到 | 她决定了以后[搬出去→搬到]学校的旁边 |  |  |
| 小镇上 | 在古代[的一个小镇→小镇上]住着一个小男孩和他的妈妈 |  |  |
| 才住了 | 孟子和孟母[才住在→才住了]两个月 | 了completed |  |
| 想让儿子开始打工，这样可以…… | 孟母想[+让]儿子开始打工可能减轻她的负担 ; 孟母想儿子开始打工[可能→这样可以]减轻她的负担 | 想 + V., cannot be followed by N. |  |
| delete他 | [-他]跟别的孩子画画儿很幸福 | redundant |  |
| add觉得 | 他跟别的孩子画画儿[+觉得]很幸福 |  |  |
| 打工的工作，在墓地祭拜 | 孟母找到[一个打工→打工的工作] ; 在墓地[-做]祭拜 |  |  |
| 在那儿 | [那里→在那儿]孟子会不是画画 |  |  |
| delete会 | 那里孟子[-会]不是画画 | 会will |  |
| 冬天的衣服 | 就是做[冬天衣服→冬天的衣服] |  |  |
| 很高的工资，工作很厉害 | 难怪老板给他们[很好工资→很高的工资] ; 原来他们[打工→工作]很厉害 |  |  |
| 不打算搬家 | 现在孟子和孟母不[-是]打算搬家 | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong | edit edge inside a HanLP word |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧出生以后 | better to briefly introduce “孟子” when this character first appears |  |
| delete the second孟子 | [-孟子]和孟子的妈妈一直住在墓地的旁边 |  |  |
| delete孟子的 | 孟子和[-孟子的]妈妈一直住在墓地的旁边 |  |  |
| delete所以他们 | [-所以他们]祭拜 | there is no cause-effect relationship |  |
| 跟孩子玩游戏 | 结果孟子常常[玩游戏跟孩子→跟孩子玩游戏] |  |  |
| delete孟子的妈妈, redundant | [-孟子的妈妈]告诉孟子 | redundant |  |
| 这样我们可以住在安静的地方 | [所以→这样]我们可能住在家安静 ; 所以我们[可能→可以]住在家安静 ; 所以我们可能住在[家安静→安静的地方] |  |  |
| 搬到安静的地方以后，一直 | 他们[搬家安静以后→搬到安静的地方以后] ; 孟子从早到晚[老是→一直]学哲学 | “老是“ for something negative, used to complain |  |
| 就成为 | 孟子[+就]成为很厉害的哲学家 | 才Num.就V. |  |
| 在古代 | [古代时候→在古代]有一个男孩名叫孟子 |  |  |
| (separate error in a note) | 古代时候有一个男孩名叫⟦孟子⟧ | better to briefly introduce “孟子” when this character first appears |  |
| 他后来成为了哲学家 | 他[+后来]成为哲学家 ; 他成为[+了]哲学家 |  |  |
| 一直管儿子的教育 | 孟母一直管[-事儿，]儿子的教养 ; 儿子的[教养→教育] | 管事V.+Obj. compound, not followed by another Obj. | edit edge inside a HanLP word |
| 搬了两次家 | 所以她[搬家二次→搬了两次家] | 了completed, V. + Num. + MW. + Obj. |  |
| delete她 | 也[-她]感到孩子教育的好地方 |  |  |
| delete也 | [-也]她感到孩子教育的好地方 |  |  |
| 就找到了让孩子接受良好教育的环境 | 也她[感到孩子教育的好地方→就找到了让孩子接受良好教育的环境] |  |  |
| 孟母搬家是为了让孟子接受良好的教育 | [在孟母搬家的故事中，不是为了学问，就是为了以她搬家又搬着找合适的地方→孟母搬家是为了让孟子接受良好的教育] | 不是……就是……is used for “either…or…”，here “学问” and “合适的地方” are actually the same purpose, to have a good environment for education |  |
| 聪明的哲学家 | 难怪孟子成为[一个大好聪明哲学→聪明的哲学家] |  |  |
| 一开始 | [起头→一开始] |  |  |
| delete和 | 孟子在墓地[-和]祭拜跟其他孩子 |  |  |
| 跟其他孩子祭拜 | 孟子在墓地和[祭拜跟其他孩子→跟其他孩子祭拜] |  |  |
| 想让…… | 孟母[想她的儿子→想让她的儿子]在更好的地方长大 | 想 + V., cannot be followed by N. |  |
| 不是教导孩子学习知识，而是教导孩子拥有野心 | 但这个地方不是[教育意义→教导孩子学习知识] ; 而是[教导野心→教导孩子拥有野心] |  |  |
| 孟子 | 孟母发现[孩子们→孟子]老是用功工作 | “孩子们” is ambiguous |  |
| 坏习馆 | 他在这个地方学到了[害得习惯→坏习馆] | 害得 + clause (harmful result) |  |
| 在这个重视创新的知识的城市 | 最后[在这个城市，重要创新和知识的地方→在这个重视创新的知识的城市] |  |  |
| delete能 | 他[-能]从早到晚都在努力学习哲学 |  |  |
| 成为了大哲学家 | 也[成为大哲学→成为了大哲学家] |  |  |
| 在古代，才十二岁的男孩子 | [古代的时候→在古代] ; [-有一个]才十二岁小男孩子叫孟子 ; 有一个[才十二岁小男孩子→才十二岁的男孩子]叫孟子 |  |  |
| 他跟别的孩子祭拜 | 在当地的墓地找到了[他跟别的孩子→他跟别的孩子祭拜] |  |  |
| 从童年开始，一直 | 他[从童年老是→从童年开始，一直]讨论重要的生活问题 | “老是“ for something negative, used to complain |  |
| 害得他的价值观出现问题 | 当商人会害得他的价值观[+出现问题] | 害得+ N. + Harmful result |  |
| 别人 | 原来他想给[别的人→别人]建议 |  |  |
| 拿了墓地的东西 | 妈妈认为他们[拿东西→拿了墓地的东西] | “东西” is too general and vague |  |
| 问 | 所以她问[-了] | no 了for speaking word |  |
| 你们 | [他们→你们]为什么拿水果？孟子说他们不是拿东西 | in quoted speech |  |
| 用水果祭拜祖先 | 而是[给祖先水果祭拜→用水果祭拜祖先] |  |  |
| 常常 | 他说他[老是→常常]来墓地请祖先给他建议 | “老是“ for something negative, used to complain |  |
| 这一天 | [这个天→这一天]他请他们给他建议怎么减轻他的家庭的负担 |  |  |
| delete给他 &他的, too many他 | 这个天他请他们[-给他]建议怎么减轻他的家庭的负担 ; 这个天他请他们给他建议怎么减轻[-他的]家庭的负担 | too many他 ; too many他 |  |
| 他们 | 这个天[他请他们→他们]给他建议怎么减轻他的家庭的负担 |  |  |
| 接受教育 | 妈妈告诉他应该[发现教育→接受教育] |  |  |
| 学完以后，商人 | [教育做完→学完]以后孟子考虑 ; 教育做完以后[+，]孟子考虑 ; 不是当哲学家就是当[商家→商人] |  |  |
| 商人 | 父母希望他当[商家→商人] |  |  |
| 在古代 | [在古代的时候→在古代] |  |  |
| 在教育方面很厉害 | 孟子的妈妈[不是轻松的妈妈，而且她是厉害的妈妈→在教育方面很厉害] | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong |  |
| delete有一天 | [-有一天]孟子才四岁 |  |  |
| 害得孟子整天都很郁闷 | 孟母害得孟子[玩儿→整天都很郁闷] | 害得 + N/sb. + Harmful result, 玩儿is not harmful |  |
| 每天都不高兴 | 难怪孟子[不是高兴的孩子，就是安静的孩子→每天都不高兴] | 不是……就是……is used for “either…or…”, “高兴” and “安静” cannot form “either…or…” relationship |  |
| 孟母 | [她→孟母]跟孟子搬家去墓地做祭拜 | “她” is ambiguous |  |
| 孟子 | [他→孟子]成为一个有名的哲学家 ; 他[+后来]成为一个有名的哲学家 | “他” is ambiguous, 后来成为 ; “他” is ambiguous, 后来成为 |  |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧没有星期日 | better to briefly introduce “孟子” when this character first appears |  |
| 妈妈就抱怨 | 他[-有的时候]只要跟朋友玩儿 ; [-可是]孟子的妈妈有别的看法 ; 可是孟子的[妈妈有别的看法→妈妈就抱怨] | wrong conjunctions, 他只要跟朋友玩儿 ; wrong conjunctions, 他只要跟朋友玩儿 ; 只要……就as long as |  |
| 妈妈就有别的看法 | 他有的时候[-只要]跟朋友玩儿 ; [-可是]孟子的妈妈有别的看法 ; 可是孟子的[妈妈有别的看法→妈妈就有别的看法] | or 他有的时候跟朋友玩儿 |  |
| 觉得常常搬家害得他老是交不到新朋友 | 觉得[交新朋友老是害得→常常搬家害得他老是交不到新朋友] | 害得 + N/sb. + Harmful result |  |
| 决定is a mental state verb, no了 | 孟子决定[-了]祭拜 | 决定is a mental state verb, no了 |  |
| no logic relationship with the preceding sentence | ⟦他从早到晚看古代的文章⟧ | no logic relationship with the preceding sentence |  |
| 不再搬家，而是待在这儿学习很多文章 | 他[不是在→不再]搬家 ; 而是[学→待在这儿学习]多文章 ; 而是学[+很]多文章 | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong, 搬家is not conventionally related to看文章 |  |
| 成为很聪明的哲学家 | 成为[很聪明→很聪明的哲学家] |  |  |
| 在古代中国，女人 | 在[中国古代的时候→古代中国，]有一个很漂亮的女儿 ; 在中国古代的时候[-有一个很漂亮的]女儿 ; 在中国古代的时候有一个很漂亮的[女儿→女人] | 女儿daughter |  |
| 穿着 | 她[穿→穿着]很漂亮的衣服 | 着durative |  |
| 儿子 | 她有一个很小的[孩子→儿子] |  |  |
| delete他 | [-他]叫孟子 |  |  |
| 去城市买东西 | 她跟孟子常常[去买东西在城市→去城市买东西] |  |  |
| 孟子 | [他→孟子]看起来一个很聪明的孩子 | “他“ is ambiguous |  |
| 看起来是…… | 他看起来[+是]一个很聪明的孩子 |  |  |
| 学文学和哲学 | 学[中文字→文学]和哲学 |  |  |
| 常常一起去墓地祭拜 | 他们[一起常常去祭拜，会去墓地→常常一起去墓地祭拜] |  |  |
| delete我觉得 | [-我觉得]看起来他妈妈的中国教育 | redundant with看起来 |  |
| delete中国 | 成为他一个很重要和聪明的[-中国]哲学 |  | model unsure |
| 让他成为一个很重要的哲学家 | [成为他→让他成为]一个很重要和聪明的中国哲学 ; 成为他一个很重要[-和聪明的]中国哲学 ; 成为他一个很重要和聪明的中国[哲学→哲学家] |  | edits do not reproduce her fix |
| delete this sentence | [-他叫孟子。] |  |  |
| 为了给孟子提供更好的学习环境，…… | [每次搬家她都辛苦地工作，为了给孟子提供更好的学习环境→为了给孟子提供更好的学习环境，每次搬家她都辛苦地工作] | “为了……” cannot be in the latter clause |  |
| “而” is not appropriate, because here is no “semantic turn” | ⟦而⟧追求知识是很重要的 | “而” is not appropriate, because here is no “semantic turn” |  |
| 在古代中国，有一个叫孟子的孩子 | [在中国古代的时候有一个孩子名字是孟子→在古代中国，有一个叫孟子的孩子] |  |  |
| delete他们死了 | [-他们死了]害得孟子很不幸福 |  |  |
| 他才三岁，可是一直待在墓地里 | 他才三岁[的以后→，可是一直]待在墓地里 | Time + 以后 |  |
| 有一天 | [一个天时候→有一天] |  |  |
| delete the second孟子 | [-孟子]觉得他们画得很漂亮 | redundant |  |
| delete他 | 所以[-他]问他的妈妈怎么画 | redundant |  |
| 他的 | (unplaced unplaceable: 他的→他的) | redundant | could not place: the supplied fix already exactly matches the learner text, so no distinct edit is identifiable; model unsure |
| 不是在画画儿，而是在祭拜 | 他的妈妈告诉孟子他们[不是做画画儿，就是做祭拜→不是在画画儿，而是在祭拜] |  |  |
| 不是……就是…… is “either…or…” | 他的妈妈告诉孟子他们⟦不是做画画儿，就是做祭拜⟧ | 不是……就是…… is “either…or…” |  |
| 孟子想 | 孟子[知道→想]难怪他的奶奶爷爷死了 |  |  |
| 没祭拜过 | 原来他的父母都[没做过而祭拜→没祭拜过] |  |  |
| 没祭拜过的孩子会失去父母 | 他认为[没做过祭拜的孩子的父母老是死了→没祭拜过的孩子会失去父母] | “老是“ means always, ”死” cannot be done multiple times |  |
| 长大以后，哲学家 | [长大的时候→长大以后] ; 孟子成为中国最重要的[哲学人→哲学家] |  |  |
| 写了 | 他[写→写了]太多的文章 | 了completed |  |
| delete the second他, redundant | [-他]建议孩子们常常做祭拜 | redundant |  |
| 祭拜 | 他建议孩子们常常[做祭拜→祭拜] |  |  |
| 在古代 | [在古代时候→在古代] |  |  |
| (separate error in a note) | ⟦孟子⟧跟他妈妈常常搬家 | better to briefly introduce “孟子” when this character first appears |  |
| 在第一个地方 | 在第一个[房子→地方] |  |  |
| 不适合 | 而是她觉得墓地[不合适→不适合]孩子们玩 |  |  |
| 很近 | 第二个房子离购物中心[近→很近] | usually Adj. takes 很 |  |
| wrong information, 搬家因为孟母觉得it is not good to imitate how to buy and sell | ⟦难怪我们没有钱⟧ | wrong information, 搬家因为孟母觉得it is not good to imitate how to buy and sell |  |
| 在第三个地方 | [在第三个房子→在第三个地方] |  |  |
| 就开始…… | [+就]开始学哲学 | 才 Num.就V. |  |
| 长大以后，哲学家 | [大人的时候→长大以后] ; 他成为很有名的[老师→哲学家] |  |  |
| delete 他们 | 因为[-他们]觉得祭拜有很多好处 | redundant |  |
| 对生活有很多好处 | 因为他们觉得祭拜[有很多好处，对他们的生活→对生活有很多好处] |  |  |
| 和妈妈住在一起 | [也有他的妈妈→和妈妈住在一起] |  |  |
| 搬了很多次家 | 因为他的妈妈已经[搬家很多次→搬了很多次家] |  |  |
| 他们在中国各地都住过 | 他们在[到处的中国→中国各地都]住 ; (unplaced insert: →过) | Place到处都 + Clause ; “过” experience, have done | not found in the text: 各地都住[]; edits do not reproduce her fix |
| delete当 | 他现在是[-当]医生 | redundant with是 |  |
| delete the second他 | [-他]能帮很多人 | redundant |  |
| delete在中国 | [-在中国]不太安全 |  |  |
| be specific, what不太好的事情？ | 也有很多人老是做⟦不太好的事情⟧ | be specific, what不太好的事情？ |  |
| delete试一试 | 孟子的妈妈不是工作就是[-试一试]帮助她的儿子孟子 |  |  |
| 辅导儿子孟子 | 孟子的妈妈不是工作就是试一试[帮助她的儿子孟子→辅导儿子孟子] |  |  |
| 最喜欢的事情 | 她没有时间做她[最喜欢的兴趣→最喜欢的事情] |  |  |
| 减少工作 | 她[会工作少→减少工作] |  |  |
| delete和 | [-和]她也会做她最喜欢的兴趣爱好 | 和cannot connect clauses |  |
| delete the second and third 她 | 和[-她]也会做她最喜欢的兴趣爱好 ; 和她也会做[-她]最喜欢的兴趣爱好 | redundant ; redundant |  |
| 也会发展最喜欢的兴趣爱好 | 和她也会[做→发展]她最喜欢的兴趣爱好 |  | edits do not reproduce her fix |
| 在这个城市生活，也想成为医生 | 他[喜欢在这个城市成为医生→在这个城市生活，也想成为医生] |  |  |
| 他一直帮很多病人 | 他一直[跟很多人的病帮他们→帮很多病人] |  |  |
| 孟子不是喜欢这个城市，而是喜欢这个城市的人 | [不是孟子→孟子不是]喜欢这个城市 ; 而是[-他]喜欢这个城市的人 | Subj. before “不是……而是……” |  |
| 去墓地 | 小孟[-自己出去]墓地 |  | edits do not reproduce her fix |
| 就是去教室 | 不是去墓地就是[教堂→去教室] | 教堂church |  |
| 独一无二的人才 | 但是孟母知道小孟会是独一无二[+的人才] |  |  |
| 搬了三次家以后 | 他们[搬家三次→搬了三次家]以后 | 了completed, V. + Num. + MW. + Obj. |  |
| 待在家里 | 从早到晚小孟[待着→待在家里]学哲学和读写 |  |  |
| 在哪儿？ | [小孟在→小孟在哪儿？] |  |  |
| 很爱他 | 孟母[爱你→很爱他] | “你” refers to the reader of this story |  |
| 很穷 | 孟子的家人[-不是富有的，而是他们]很穷 |  |  |
| “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong | 孟子的家人⟦不是富有的，而是他们很穷⟧ | “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong |  |
| 孟母 | [妈妈→孟母]老是工作了 | “妈妈” here is ambiguous |  |
| 老是工作 | 妈妈老是工作[-了] | no了for routine/habit |  |
| 才 + Num. to express “small, few”, but here搬了三次家 is a large quantity | 他们⟦才搬了三次家⟧ | 才 + Num. to express “small, few”, but here搬了三次家 is a large quantity |  |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧从小到大一直搬家 | better to briefly introduce “孟子” when this character first appears |  |
| wrong information, 搬了三次家 | 可是⟦搬了十次家⟧ | wrong information, 搬了三次家 |  |
| 叫孟子搬家 | 孟子的妈妈叫[-了]孟子搬家 | 叫/让 is a modal verb, no了 |  |
| 一直学习中文 | 孟子[跟老师老是学习中文→一直学习中文] | “老是“ for something negative, used to complain |  |
| 他不是……，就是…… | [不是学习中文，他就是跟老师说中文→他不是学习中文，就是跟老师说中文] | Subj. at the beginning of 不是……就是…… |  |
| wrong information, 妈妈做衣服 | ⟦他的妈妈祭拜⟧ | wrong information, 妈妈做衣服 |  |
| 有名的哲学家 | 他[成为有名的→成为有名的哲学家] | 成为+N |  |
| 来祭拜的人 | [人→来祭拜的人]一直在墓地大声哭 | “人“ is too general and too vague, and does not stand alone |  |
| 很难过 | 孟母看出来孟子[+很]老是难过 | usually Adj. takes 很 | edits do not reproduce her fix |
| miss information: 孟子 imitated how to offer sacrifices | ⟦孟母看出来孟子老是难过⟧ | miss information: 孟子 imitated how to offer sacrifices |  |
| 怕/担心 | 孟母[恐怕→怕]孟子住在墓地的旁边对孟子有影响 | 恐怕usually does not take Subj. except 我 | edits do not reproduce her fix |
| 搬到了城市 | 他们[搬到→搬到了]城市 | 了completed |  |
| 要再搬一次家 | 我们[要搬家再一次→要再搬一次家] | 再V. + Num. + MW. + N. |  |
| 学业很难 | 而是因为[学校很难→学业很难] |  |  |
| 我心里是不想再搬一次家的 | 我心里[+是]不让我们搬家再一次 ; 我心里[不让我们→不想]搬家再一次 ; 我心里不让我们[搬家再一次→再搬一次家] ; 我心里不让我们搬家再一次[+的] |  | edits do not reproduce her fix |
| better to briefly introduce “孟子” when this character first appears | ⟦孟子⟧的妈妈一直想她的儿子在很好的地方长大 | better to briefly introduce “孟子” when this character first appears |  |
| 想让…… | 孟子的妈妈一直[想她的儿子在很好的地方长大→想让她的儿子在很好的地方长大] | 想 + V., cannot be followed by N. |  |
| 住在离墓地很近的地方 | 他[离墓地住很近→住在离墓地很近的地方] |  |  |
| 选择对孟子成长特别好的环境 | 原来他妈妈选择[+对孟子成长]特别好的地方孟子长大 ; 原来他妈妈选择特别好的[地方孟子长大→环境] |  |  |
| 看到 | 他妈妈[看→看到]他跟别的孩子在墓地里祭拜 | 看look vs.看到see |  |
| 一看到这样 | 她[一看这→一看到这样] | 看look vs.看到see |  |
| delete自己 | 就[-自己]觉得我不想我的儿子在这个地方长大 |  |  |
| delete我 | 就自己觉得[-我]不想我的儿子在这个地方长大 |  |  |
| 我的 | 就自己觉得[我不想我的→我的]儿子在这个地方长大 |  | model unsure |
| 就觉得儿子不应该在这个地方长大 | [就自己觉得我不想我的儿子→就觉得儿子不应该]在这个地方长大 |  |  |
| “害得“ is followed by something harmful, 搬家is not harmful | ⟦这害得孟母决定搬家⟧ | “害得“ is followed by something harmful, 搬家is not harmful |  |
| 适合孟子成长 | 孟母希望这个地方[对孟子长大很合适→适合孟子成长] |  |  |
| 又觉得 | 孟母[也→又]觉得在市场的旁边对孟子不合适的地方长大 | “又“ emphasizes repeating vs. ”也“ emphasizes similarity |  |
| 不适合孟子成长 | 孟母也觉得在市场的旁边[对孟子不合适的地方长大→不适合孟子成长] |  |  |
| 学做住在他们附近的人做的事情 | 孟母看孟子老是[+学]做他们住很近的人做的事情 ; 孟母看孟子老是做[他们住很近的人→住在他们附近的人]做的事情 |  |  |
| “害得“ is followed by something harmful, 搬家is not harmful | 这⟦害得孟母离学校很近搬家⟧ | “害得“ is followed by something harmful, 搬家is not harmful |  |
| 搬家到离学校很近的地方 | 这害得孟母[离学校很近搬家→搬家到离学校很近的地方] |  |  |
| 不是孟子不好，而是他需要在一个好环境中成长 | 最后孟母觉得不是孟子不好[-的男孩] ; 而是他需要[很好的地方→在一个好环境中]长大 ; 而是他需要很好的地方[长大→成长] |  |  |
| 张先生在梨子树口摆了一张梯子 | 张先生在梨子树口[摆着→摆了]一张梯子 | Subj. V. 了 (completed) Obj., or 梨子树口摆着一张梯子，Place + V. 着 + Obj. |  |
| 爬上梯子去 | 张先生[爬上去梯子→爬上梯子去] | V. + directional complement + Place + 来/去 |  |
| 小王和那筐梨子倒了 | 小王和那筐梨子倒[+了] | 了completed/change |  |
| 他擦了一下腿/擦着腿 | 他[擦→擦了一下]腿 | either 了completed or 着 durative | edits do not reproduce her fix; model unsure |
| 在马路上 | 一个孩子在马路[+上]看到小王的帽子 | 在+ place |  |
| 拿起来pick up，拿上去means “bring it up” | ⟦拿上去⟧ | 拿起来pick up，拿上去means “bring it up” |  |
| 给了孩子三个梨子 | [给→给了]孩子三个梨子 | 了completed |  |
| 走到张先生的树下 | 孩子一直[走去张先生的树→走到张先生的树下] | 走到place来/去，cannot say “走去/来Place” |  |
| 吃着梨子 | [吃梨子→吃着梨子] | 着 durative |  |
| 比别的水果都好/最好不过了 | 觉得这些梨子[比别的水果最好不过了→比别的水果都好] | 最好不过了cannot be used in comparative sentences, it means “the best option”. | edits do not reproduce her fix |
| 一爬下梯子来 | 张先生一[爬下来梯子→爬下梯子来] | V. + directional complement + Place + 来/去 |  |
| 偷了 | 觉得他们偷[+了]他的梨子 | 了completed |  |
| 送给了小王 | 觉得张先生把一筐梨子[送了给→送给了]小王 |  |  |
| 爬下梯子来 | [爬下来梯子→爬下梯子来] | V. + directional complement + Place + 来/去 |  |
| 在第三个筐里放着一些梨子 | 在第三个筐里放着[那些→一些]梨子 | the Obj. in “Place + V. 着 + Obj.” is usually “number + MW + noun”, not specific “that/this/those/these/the + noun”. |  |
| 又一次爬上梯子的时候 | 他又[+一次]爬上去梯子的时候 ; 他又爬上[-去]梯子的时候 |  |  |
| 马先生牵着驴走到筐的后边来 | 马先生[跟他的驴→牵着驴]走去筐的后边来 ; 马先生跟他的驴[走去→走到]筐的后边来 | “跟/和+noun.” is used for multiple nouns that have the same action, we can say: 马先生和张先生走……，because both 马先生and 张先生 “walk”, but here “驴” does not walk by itself, but walked by 马先生, so you need to use the accompanying phrase “V.着” |  |
| 走到place来/去，cannot say “走去/来Place” | 马先生跟他的驴⟦走去筐⟧的后边来 | 走到place来/去，cannot say “走去/来Place” |  |
| 到张先生的梨子树下 | 小王骑自行车到张先生的梨子树[+下] | 到 + place |  |
| 就拿了一筐梨子 | 就拿[+了]一筐水果 ; 就拿一筐[水果→梨子] | 了completed ; “水果” is more generic and here it should be “梨子”，otherwise it will cause ambiguity, what “fruits” other than “pears”? |  |
| 在马路上 | 小王在马路[+上]骑自行车一看到别个人 | 在+ place |  |
| 骑着自行车 | 小王在马路骑[+着]自行车一看到别个人 | “着” is for “durative” |  |
| 另外一个人/一个女孩子 | 小王在马路骑自行车一看到[别个人→另外一个人/一个女孩子] | there is no “别个人”. |  |
| 自行车一下子就撞到石头了 | [一下子就撞自行车→自行车一下子就撞到石头了] | “撞自行车” means to hit the bike, in fact, it is: the bike hit the rock. |  |
| 农民 | 一个[农人→农民]爬着一个树 |  |  |
| 一棵树 | 一个农人爬着[一个树→一棵树] |  |  |
| delete他 | [-他]把树上的梨子摘下来 | otherwise redundant. |  |
| 一个男人牵着一只驴从农民身边经过 | 一个[男生→男人]和一只驴从农人经过了 ; 一个男生[和→牵着]一只驴从农人经过了 ; 一个男生和一只驴从[农人→农民身边]经过了 ; 一个男生和一只驴从农人经过[-了] | “跟/和+noun.” is used for multiple nouns that have the same action, we can say: 一个男生和一个女生走……，because both 男生and 女生 “walk”, but here “驴” does not walk by itself, but walked by 男生, so you need to use the accompanying phrase “V.着” |  |
| 从 + place，农民is not a place, 农民身边 is a place | 一个男生和一只驴从⟦农人⟧经过了 | 从 + place，农民is not a place, 农民身边 is a place |  |
| the  word “经过” implies ongoing process, so no了(completed). | 一个男生和一只驴从农人⟦经过了⟧ | the  word “经过” implies ongoing process, so no了(completed). |  |
| 农民在梯子上/登梯子的时候 | (unplaced unplaceable: 农人登梯子上的时候→) |  | could not place: the slash gives two alternative rewrites, so no single exact edit can be selected; model unsure |
| 一看到 | 男孩[一看→一看到]哪一筐有更多梨子就往自己的自行车上放梨子的筐 | 看look, 看到see |  |
| 哪一筐有更多梨子就往自己的自行车上放哪一筐 | 男孩一看哪一筐有更多梨子就往自己的自行车上放[梨子的筐→哪一筐] | the structure “repeated Wh-Q” expressing “wh-ever…, will do that…”. |  |
| 接着一下子就骑车逃跑了 | [+接着]一下子就骑车逃跑 ; 一下子就骑车逃跑[+了] |  |  |
| add “接着” otherwise it is broken from the preceding clause | [+接着]一下子就骑车逃跑 | add “接着” otherwise it is broken from the preceding clause |  |
| add了 change. | 一下子就骑车逃跑[+了] | add了 change. |  |
| 一个很漂亮的女孩 | 就看到[很漂亮的女孩→一个很漂亮的女孩] | first appearing noun should not be specific |  |
| 把帽子弄掉了 | 把帽子弄掉[+了] | “把”usually ends with了 |  |
| 又一下子撞到了一个大石头 | 一下子[撞了一个大石→撞到了一个大石头] | 撞到+Obj. | edits do not reproduce her fix |
| add “又” to make it smooth, 撞到+Obj. | [+又]一下子撞了一个大石 | add “又” to make it smooth, 撞到+Obj. |  |
| 筐里的梨子撒在地上了 | [-被]筐里的梨子坐在地上了 ; 被筐里的梨子[坐→撒]在地上了 | 被 means passive voice “be done” ; 坐”sit” is used for animate Obj. |  |
| 骑自行车的男孩 | [自行车的男孩→骑自行车的男孩]给三个男孩子们每一个人一个梨子 |  |  |
| 给三个男孩子 | 自行车的男孩给[三个男孩子们→三个男孩子]每一个人一个梨子 | “们”cannot be used with num. |  |
| 天刚刚亮起来 | 天[+刚刚]亮起来 | align with preceding “早得很” | edit edge inside a HanLP word |
| 在树顶的梯子上站着拿一些梨 | 一个戴围巾的男人[站着在树顶的梯子上→在树顶的梯子上站着]拿一些梨 | 在Place V1.着V2 |  |
| 扶起自行车 | [帮他拿他的自行车→扶起自行车] | “拿” is usually used for smaller items |  |
| 帮了他以后 | 帮[+了]他后 ; 帮他[后→以后] | 了completed |  |
| 他们走了/走过去了 | (unplaced unplaceable: 走去→走了/走过去了) | usually we do not say “走去”. | could not place: teacher provides two alternative corrections without choosing one; model unsure |
| 拿起 | 他[拿上→拿起]这顶帽子 |  |  |
| 送了 | 他送[+了]三个梨给他们 | 了completed |  |
| “他” is a bit ambiguous | ⟦他⟧送三个梨给他们 | “他” is a bit ambiguous |  |
| 看到一筐梨没有了 | [看到没有一筐的梨→看到一筐梨没有了] |  |  |
| 这筐梨 | 他不知道这筐[-的]梨在哪儿 | no的 |  |
| 这三个男孩子每人都有一个梨 | 可是他看到这三个男孩子[+每人]都有一个梨 |  |  |
| delete “就”, add “看到” | [-就]筐里放着差不多十个梨 ; [+看到]就筐里放着差不多十个梨 |  |  |
| 他用他的围巾把梨擦干净 | 他用他的围巾[擦，把梨干净→把梨擦干净] | 把Obj. V. Resultative complement |  |
| delete “就” | [-就]一个男人遛一只驴走过去 |  |  |
| 一个男人牵着一只驴 | 就[一个男人遛一只驴→一个男人牵着一只驴]走过去 | 着durative，“遛“ for 狗only. |  |
| 拿了很多梨 | 这个戴围巾的男人[拿多梨→拿了很多梨] | 了completed, 很多+noun |  |
| here “他” is a bit ambiguous, it can refer to the boy or the man wearing the scarf. | ⟦他⟧停在树下 | here “他” is a bit ambiguous, it can refer to the boy or the man wearing the scarf. |  |
| 一筐梨 | 所以他偷走[一筐的梨→一筐梨] | num. + MW. + noun, no的 |  |
| 骑自行车离开 | [骑自行车走去→骑自行车离开] | “骑自行车“ conflicts with ”走“ |  |
| 梨从筐里撒出去 | 他[-把]梨从筐里倒出去 ; 他把梨从筐里[倒→撒]出去 |  |  |
| “把“ is used for initiated actions (“disposal”), here it is not he who threw those pears, but the pears fell themselves. 倒 means “pour” if it is an initiated action, and means “fall” if it is not an initiated action, and followed by 下去/下来。 | ⟦他把梨从筐里倒出去⟧ | “把“ is used for initiated actions (“disposal”), here it is not he who threw those pears, but the pears fell themselves. 倒 means “pour” if it is an initiated action, and means “fall” if it is not an initiated action, and followed by 下去/下来。 |  |
| 掉下去 | 他的帽子也[倒下去→掉下去] |  |  |
| 从香甜的睡梦中 | “咕噜咕噜”某个人肚子叫的声音把我从香甜的睡梦[+中]吵醒了！这个人如蜗牛一般爬上我住的树木 |  |  |
| 从 + Place | “咕噜咕噜”某个人肚子叫的声音把我⟦从香甜的睡梦⟧吵醒了！这个人如蜗牛一般爬上我住的树木 | 从 + Place |  |
| 整个秋季期间 | [+整个]秋季期间 |  |  |
| Time + 期间：usually special, long period, “秋季” itself is not “special” enough, “整个/今年秋季” would highlight this particular, special period. | ⟦秋季期间⟧ | Time + 期间：usually special, long period, “秋季” itself is not “special” enough, “整个/今年秋季” would highlight this particular, special period. |  |
| 今天清晨 | 今天[-的]清晨 |  |  |
| 先打了个大哈欠 | 先打了[+个]大哈欠 |  |  |
| 优质的梨子 | 然后忙着偷走[优秀→优质]的梨子 |  |  |
| “优秀“ cannot be used for items/things, usually for people. | 然后忙着偷走⟦优秀的梨子⟧ | “优秀“ cannot be used for items/things, usually for people. |  |
| 拼了几个小时之后 | 拼[+了]几个小时之后他就休息了 |  |  |
| completed | ⟦拼几个小时之后⟧他就休息了 | completed |  |
| 我的爸爸妈妈 | 然后突然一口气吃掉了[我家长→我的爸爸妈妈]！他到底以为自己是谁啊？难道以为自己是上帝吗？我生气极了！下午就继续爬上树 |  |  |
| “家长“ is used in the context related to “education”, usually referring to parents who deal with children’s education. | 然后突然一口气吃掉了我⟦家长⟧！他到底以为自己是谁啊？难道以为自己是上帝吗？我生气极了！下午就继续爬上树 | “家长“ is used in the context related to “education”, usually referring to parents who deal with children’s education. |  |
| 下午他还继续爬上树 | 然后突然一口气吃掉了我家长！他到底以为自己是谁啊？难道以为自己是上帝吗？我生气极了！下午[就→他还]继续爬上树 |  |  |
| miss the Subj., otherwise readers will understand the Subj. here as “我”, which is incorrect. “还“ indicates “surprising, anger” tone, as opposed to “就” with the natural continuation tone. | 然后突然一口气吃掉了我家长！他到底以为自己是谁啊？难道以为自己是上帝吗？我生气极了！下午⟦就⟧继续爬上树 | miss the Subj., otherwise readers will understand the Subj. here as “我”, which is incorrect. “还“ indicates “surprising, anger” tone, as opposed to “就” with the natural continuation tone. |  |
| 每天都是这样 | 每天[就是→都是]这样 |  |  |
| 没有什么前途 | 这个坏人好像没有什么[-有希望的]前途 |  |  |
| “前途” itself means “hopeful future”, so “有希望” is a little bit redundant. | (none) |  | no edit returned |
| “寄托在偷梨子上” feels better, “寄托在……身上” usually for people, that is, a specific person carries the hope and can help the Subj. to realize the goal/objective. | 就⟦把希望寄托在梨子身上⟧ | “寄托在偷梨子上” feels better, “寄托在……身上” usually for people, that is, a specific person carries the hope and can help the Subj. to realize the goal/objective. |  |
| 他很久以前可能并不是这样碌碌无为，而是拿到了硕士和博士学位 | 但我没想到[+是]他可能很久以前并不是这样 ; 但我没想到他[可能很久以前→很久以前可能]并不是这样 ; 但我没想到他可能很久以前并不是这样[+碌碌无为] ; [得到了→而是拿到了]硕士和博士学位 | the coherence needs to be improved, 但我没想到的是 |  |
| 每天都爬上 | 他这个没有礼貌的人每天[+都]爬上本树 |  |  |
| 精疲力尽 | 我兄弟说：“他并不一直如此[精辟力尽→精疲力尽] | use the wrong character. I’m not very sure if “精疲力尽” is the most appropriate word here, since it means “exhausted”, and the pear thief is just busy stealing pears, and I did not see signs of him being “exhausted”. |  |
| 偷梨子？usually 吃梨子 does not lead to 精疲力尽. | ⟦整天只能吃梨子⟧ | 偷梨子？usually 吃梨子 does not lead to 精疲力尽. |  |
| 主修专业竞争力也很强。 | [有高的学历和厉害的主修→学历很高。主修专业竞争力也很强。] | instead of using “有……” structure, it is better to use short sentences: 学历很高 |  |
| 实行的改革经济的一系列政策，却使他失业并被迫转行 | 但政府实行的改革经济[+的]一系列政策就让他失业 ; 但政府实行的改革经济一系列政策[就让→却使]他失业 ; 但政府实行的改革经济一系列政策就让他失业[，→并]被迫转行 |  |  |
| 被迫，转行” | (unplaced unplaceable: 被迫转行→) | “却” indicates unexpected semantic turn, “使” is more formal and better fit other formal words like “失业 ; adding “并” will increase the coherence. | could not place: the supplied fix fragment is malformed and conflicts with the full correction; model unsure |
| 不断 | 政府[不短→不断]采取限制工作的措施 | use the wrong character |  |
| 限制就业 is better | 政府不短采取⟦限制工作⟧的措施 | 限制就业 is better |  |
| 回去做以前的工作 | 让每天拿梨子的这个人没办法回去[+做]以前的工作 |  |  |
| 但我只思考了几分钟 | 我怎么能还要发火呢？但[+我]只能思考几分钟 ; 我怎么能还要发火呢？但[只能思考几分钟，就被他拿起来了→只思考了几分钟]！我变成了地上的堆梨一族 |  | edits do not reproduce her fix |
| the Subj. here cannot be omitted, because the preceding “我怎么能…” is an inserted “narrator comment”, which is temporarily detached from the main storyline. When it goes back to the main story, the Subj. should be restated. | 我怎么能还要发火呢？但⟦只能思考几分钟⟧ | the Subj. here cannot be omitted, because the preceding “我怎么能…” is an inserted “narrator comment”, which is temporarily detached from the main storyline. When it goes back to the main story, the Subj. should be restated. |  |
| “堆梨” is a self-created word, and it is a bit ambiguous. For me, “堆梨一族” means a group of people who pile pears together, as “堆” here is usually understood as a verb. Perhaps “梨堆的一员”. | 就被他拿起来了！我变成了地上的⟦堆梨一族⟧ | “堆梨” is a self-created word, and it is a bit ambiguous. For me, “堆梨一族” means a group of people who pile pears together, as “堆” here is usually understood as a verb. Perhaps “梨堆的一员”. |  |
| 这样的事情会发生 | 我完全没想到[什么事情会立刻发生→这样的事情会发生] | as “being picked up” already occurred, so it is not unknown “什么事情”, but a certain “这样的事情”. |  |
| 自然规律 as a fixed expression | 我以前以为人类的问题是人们不尊重⟦世界上自然的规定⟧ | 自然规律 as a fixed expression |  |
| 圣经所依据的法律：“据说”can only be used at sentence initial, separate from other parts, followed by the information that is heard. | ⟦圣经据说的法律⟧ | 圣经所依据的法律：“据说”can only be used at sentence initial, separate from other parts, followed by the information that is heard. |  |
| 本+N. is usually used in formal advertisement/news, also it indicates the author owns the tree, which is not the fact: the author is a pear, who does not own the whole pear tree. 爬上这棵树。 | 他这个没有礼貌的人每天爬上[本树→这棵树] | 本+N. is usually used in formal advertisement/news, also it indicates the author owns the tree, which is not the fact: the author is a pear, who does not own the whole pear tree. 爬上这棵树。 |  |
| 连自己制定的规定 | 但[人类连人类划定的规定→人类连自己制定的规定]也不尊重！虽然我认为自己的树木不是任何人的所有权 | do not repeat “人类” twice, 制定规定 as a fixed expression. |  |
| 不归任何人所有/任何人都没有我的树木的所有权 | 但人类连人类划定的规定也不尊重！虽然我认为自己的树木[不是任何人的所有权→不归任何人所有] |  | edits do not reproduce her fix |
| 但据人类法律规定，我归之前说的那个坏人所有 | [+但]据人类法律规定 ; 我[是那个以前说的坏人的所有权→归之前说的那个坏人所有] |  |  |
| 可 | [但→可]这个小孩儿完全不在乎不尊重 | because earlier “但“ is already used, here use “可” as alternative. |  |
| 人类创造的文明 | 我无话可说！[人类创造文明→人类创造的文明]到底从哪里由此而来啊 | the Subj. should be a noun “文明”, not a verb phrase “人类创造文明” |  |
| 到底从何而来：由此而来 means “come from this”, but here should be a question “come from where”. | 我无话可说！人类创造文明到底[从哪里由此而来→从何而来]啊 | 到底从何而来：由此而来 means “come from this”, but here should be a question “come from where”. |  |
| 看起来一点儿都不文明 | [看起→看起来]一点文明都没有 ; 看起[一点→一点儿]文明都没有 ; 看起一点[+不]文明都没有 | “文明” can be an Adj., meaning “civilized”. | edits do not reproduce her fix |
| 下面发生的事情 | [下个→下面]发生的事情还更奇怪 |  |  |
| replace “他” with “这个小男孩”，otherwise “他” is ambiguous, who? 一个女孩儿，“某个” refers to a specific person/thing, only not identifying the name. Here he saw “one girl”, not “a specific girl”. | [他→这个小男孩]突然看到了某个女孩儿 ; 他突然看到了[某个→一个]女孩儿 | replace “他” with “这个小男孩”，otherwise “他” is ambiguous, who? 一个女孩儿，“某个” refers to a specific person/thing, only not identifying the name. Here he saw “one girl”, not “a specific girl”. ; replace “他” with “这个小男孩”，otherwise “他” is ambiguous, who? 一个女孩儿，“某个” refers to a specific person/thing, only not identifying the name. Here he saw “one girl”, not “a specific girl”. |  |
| 这个奇怪的男孩 | [这奇怪的→这个奇怪的]男孩一看到她 | 这/那 + Measure word + noun. |  |
| 我们这堆梨都在地上乱糟糟/乱七八糟地滚来滚去 | 我们[梨堆一族→这堆梨]都乱地滚来滚去地上 ; 我们梨堆一族都[+在地上]乱地滚来滚去地上 ; 我们梨堆一族都[乱地→乱糟糟地]滚来滚去地上 ; 我们梨堆一族都乱地滚来滚去[-地上] | 在place滚来滚去，multi-syllabic adv. + 地（mono-syllabic adv. cannot be used with 地） ; 在place滚来滚去，multi-syllabic adv. + 地（mono-syllabic adv. cannot be used with 地） ; 在place滚来滚去，multi-syllabic adv. + 地（mono-syllabic adv. cannot be used with 地） | edits do not reproduce her fix |
| 我的兄弟姐妹 | 来偷走我[+的]兄弟姐妹 |  |  |
| 他们过来用心地帮忙整理梨子，扶起自行车 | [+他们过来]用心得来帮忙整理梨子 ; 用心[得来→地]帮忙整理梨子 ; [拿起骑车→扶起自行车] | since the preceding phrase has “我们”, the Subj. 他们 should be stated ; adv.地V ; “骑车” is a verb phrase, cannot be the Obj. of “扶起”，“拿起” is usually used for smaller items. |  |
| 那三个男孩/那些男孩 | (unplaced unplaceable: 那些三个男孩→那三个男孩/那些男孩) | “些” cannot be used with num. | could not place: teacher gives two alternative replacements; model unsure |
| 拿着梨子 | 但那些三个男孩不知不觉[和梨子→拿着梨子]走过了被偷走的有梨子所有权的第一个人 | “和+noun.” is used for multiple nouns that have the same action, we can say: 那三个男孩和拿走梨子的小男孩走过了……，because both 三个男孩 and 小男孩 “walk past…”, but here “梨子” do not walk, so you need to use the accompanying phrase “V.着” |  |
| “被偷走的有梨子所有权的第一个人” is too long, 第一个被偷走梨子的人 is clear enough. | 但那些三个男孩不知不觉和梨子走过了⟦被偷走的有梨子所有权的第一个人⟧ | “被偷走的有梨子所有权的第一个人” is too long, 第一个被偷走梨子的人 is clear enough. |  |
| 人类就是这么奇怪呢/人类多么奇怪啊 | 人类[就多么→就是这么]奇怪呢 ; 人类[就→]多么奇怪呢 ; 人类就多么奇怪[呢→啊] |  | edits do not reproduce her fix; model unsure |
| 所有权 | 这个坏人好像以为自己有我们家的[所有全→所有权]！但并不是这样 |  |  |
| use the wrong character | 这个坏人好像以为自己有我们家的所有⟦全⟧！但并不是这样 | use the wrong character |  |
| 他甚至不应该有我的“梨树”家的使用权 | [我树家→他]甚至不应该是他的使用权 ; 我树家甚至不应该[是他的→有我的“梨树”家的]使用权 |  |  |
| Subj.有……的使用权，“树家” is a self-created word and vague, better to use “梨树”家，use “” to highlight the metaphor usage of “the pear tree as home”. | ⟦我树家甚至不应该是他的使用权⟧ | Subj.有……的使用权，“树家” is a self-created word and vague, better to use “梨树”家，use “” to highlight the metaphor usage of “the pear tree as home”. |  |
| 虽然是世界上最美丽的 | 虽然是世界上最美丽的[-梨子] | 水果是……梨子 is not very precise, 我们地位低的水果 |  |
| 把我们只算作小吃而已：只/不过/才(+num.) + 而已，Subj.算是Obj., “算是”usually is not used in “把” | 但人类总是会[把我们算是小吃而已→把我们只算作小吃而已]” | 把我们只算作小吃而已：只/不过/才(+num.) + 而已，Subj.算是Obj., “算是”usually is not used in “把” |  |
| 马虎地V., use the wrong character | 他怎么能随便⟦马虎得⟧掉我家庭呢？一点都不合理 | 马虎地V., use the wrong character |  |
| 摘掉我的家人：掉itself cannot be followed by an Obj., Subj. 掉 + directional + place, but掉can be resultative complement following another main action verb | 他怎么能随便马虎得⟦掉我家庭⟧呢？一点都不合理 | 摘掉我的家人：掉itself cannot be followed by an Obj., Subj. 掉 + directional + place, but掉can be resultative complement following another main action verb |  |
| 这肯定不是上帝创造世界的目的 | [这个→这]肯定不是上帝创造世界的目的 |  |  |
| delete “个”, 这个 + Noun. | 这[-个]肯定不是上帝创造世界的目的 | 这个 + Noun. | edit edge inside a HanLP word |
| Delete “他” | 古代的人都不知道[-他]什么能吃 |  |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧看到很多人吃了麻烦的植物 | better to briefly introduce “神农” when this character first appears |  |
| 有害的植物 | 神农看到很多人吃了[麻烦的→有害的]植物 |  |  |
| it is loosely connected with the previous sentence, better add “为了帮助人们找到能吃的植物”, 神农决定去旅行尝试新的植物，“过” is to express “experience”, now the experience has not yet been experienced | ⟦神农旅行了，吃过新的植物⟧ | it is loosely connected with the previous sentence, better add “为了帮助人们找到能吃的植物”, 神农决定去旅行尝试新的植物，“过” is to express “experience”, now the experience has not yet been experienced |  |
| 有用的植物 | 他找到了很多[有用植物→有用的植物] |  |  |
| 他就生病了 | [夹竹桃一吃→他] | otherwise it is ambiguous who gets sick |  |
| 找到了 | 一个人正好[找了→找到了]神农 | 找look for vs.找到find |  |
| 给了 | 他给[+了]神农灵芝 | 了completed |  |
| it is unclear what the subject is, add “神农说：一吃夹竹桃就不舒服”, it is not “死” | [一吃夹竹桃就死→神农说：一吃夹竹桃就不舒服] | it is unclear what the subject is, add “神农说：一吃夹竹桃就不舒服”, it is not “死” |  |
| add a condition before “这就要看……了“ | [+如果吃了夹竹桃，]这就要看你也吃不吃灵芝了 | e.g., 如果吃了夹竹桃 |  |
| 病能不能好？这就要看你吃没吃灵芝了 | [+病能不能好？]这就要看你也吃不吃灵芝了 ; 这就要看你[-也]吃不吃灵芝了 ; 这就要看你也[吃不吃→吃没吃]灵芝了 | 不for habit/routine/willingness, 没for non-occurrence of an event |  |
| delete了 | 神农没死[-了] | 没+ V. |  |
| 关于神农的 | 这是[一个神农的→关于神农的]古代故事 |  |  |
| (separate error in a note) | 这是一个⟦神农⟧的古代故事 | better to briefly introduce “神农” when this character first appears |  |
| 糟糕is usually for情况situations, 太穷了better? Delete他们, redundant | 他的朋友太⟦糟糕⟧了 ; [-他们]常常饿死了 | 糟糕is usually for情况situations, 太穷了better? Delete他们, redundant ; 糟糕is usually for情况situations, 太穷了better? Delete他们, redundant |  |
| delete他 | 所以[-他]看什么就吃什么 | this is ambiguous, as the topic is他的朋友 |  |
| 看到什么 | 所以他[看什么→看到什么]就吃什么 | 看look vs.看到see |  |
| 花is also a type of植物 | 比方说他吃⟦植物和花⟧ | 花is also a type of植物 |  |
| 夹竹桃，这个花 | 他吃[花→一种叫夹竹桃的花]的时候生病了 | it is confusing to have花 ; it looks like they refer to two different flowers, but actually the same. 吃一种叫夹竹桃的花的时候 |  |
| 看上去像伞 | 灵芝[看上伞→看上去像伞] |  |  |
| 植物 | 神农不喜欢[菜→植物] |  |  |
| it is problematic in coherence, if 灵芝is medicine, it should not be他一吃肚子就疼死了 | 所以⟦他一吃，肚子就疼死了⟧ | it is problematic in coherence, if 灵芝is medicine, it should not be他一吃肚子就疼死了 |  |
| 人们不知道什么植物可以吃 | [神农和他的城市不知道什么植物他们可以吃→人们不知道什么植物可以吃] |  |  |
| delete他们 | 神农和他的城市不知道什么植物[-他们]可以吃 |  |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧和他的城市不知道什么植物他们可以吃 | better to briefly introduce “神农” when this character first appears |  |
| 有毒的植物 | 他们吃[毒植物→有毒的植物] |  |  |
| 常常生病 | 他们常常生病[-了] | no了for routine/habit |  |
| add a condition “会不会生病“ before “这就要看……了”, the condition is “not definite” | [+会不会生病，]这就要看什么植物你吃了 | the condition is “not definite” |  |
| 你吃了什么植物了 | 这就要看[什么植物你吃了→你吃了什么植物了] |  |  |
| 不希望看到人们生病 | 神农[不喜欢→不希望]看他的城市生病了 ; 神农不喜欢[看→看到]他的城市生病了 ; 神农不喜欢看[他的城市→人们]生病了 ; 神农不喜欢看他的城市生病[-了] | 看look vs.看到see ; no了 |  |
| loose connection between the two clauses, 决定去旅行找到能吃的植物 | ⟦所以他决定去旅行⟧ | loose connection between the two clauses, 决定去旅行找到能吃的植物 |  |
| it is problematic in coherence, 灵芝is medicine, it should not be一吃就生病 | 所以⟦神农吃了，一吃就生病⟧ | it is problematic in coherence, 灵芝is medicine, it should not be一吃就生病 |  |
| 回到家 | 神农[回→回到]他的家 |  | edits do not reproduce her fix |
| delete他的, redundant | 神农回[-他的]家 | redundant |  |
| delete他 | [-他]看到了药 | redundant |  |
| 有毒植物 | 正好看到了[毒植物→有毒植物] |  |  |
| what is the connection between 看到了药and正好看到了有毒植物? | 他⟦看到了药，正好看到了毒植物⟧ | what is the connection between 看到了药and正好看到了有毒植物? |  |
| 写下 | 一回家就[写→写下]什么植物他们能和不能吃 |  |  |
| delete他们 | 一回家就写什么植物[-他们]能和不能吃 | redundant |  |
| 什么植物能吃，什么植物不能吃 | (unplaced replace: 什么植物能和不能吃→什么植物能吃，什么植物不能吃) |  | not found in the text: 一回家就写[什么植物能和不能吃] |
| 知道，没有毒 | 现在他们[懂→知道]什么植物不毒 ; 现在他们懂什么植物[不毒→没有毒] |  |  |
| 植物 | 没有人知道什么[食品→植物]能吃 | “食品” is usually for processed food |  |
| 看到 | 所以神农一[看→看到]病人就想找药 | 看look vs.看到see |  |
| better to briefly introduce “神农” when this character first appears | 所以⟦神农⟧一看病人就想找药 | better to briefly introduce “神农” when this character first appears |  |
| 找到一种植物 | 他[找有的花→找到一种植物] | 找look for vs.找到find |  |
| 有的，有的 | 他找[有的花→有的，有的] | some, some | model unsure |
| 吃到，一种有毒的花，就生病了 | 他正好[吃一毒的花，会生病了→吃到，一种有毒的花，就生病了] | 会means “will”, for future |  |
| 就好了 | [不病→就好了] | “病” is not a normal Adj., so it cannot be with 很 or 不 |  |
| 拿着花说 | 他[拿说→拿着花说] | 着durative |  |
| add a condition “会不会生病？” before “这就要看……了”, 这就要看吃了什么植物了 | [+会不会生病？]这就要看什么植物吃了 ; 这就要[看什么植物吃了→看吃了什么植物了] |  |  |
| 植物 | 有的[食品→植物]很有用 | “食品” is usually for processed food |  |
| 在岩石上，写下 | 他在岩石[+上]写什么植物可以吃 ; 他在岩石[+，]写什么植物可以吃 ; 他在岩石[写→写下]什么植物可以吃 |  | edits do not reproduce her fix |
| 植物 | 那我们现在知道什么[菜→植物]能吃 |  |  |
| 教了我们 | 因为神农[我们教了→教了我们] |  |  |
| 看到了 | 然后他们[看了→看到了]很多植物 | 看look vs.看到see |  |
| 这个植物 | 因为我们不知道[植物→这个植物]是什么 |  |  |
| add a condition “要不要吃？” before “这就要看……了” | [+要不要吃？]这就要看你饿不饿了 |  |  |
| 有没有毒 | 我们也不在乎植物[是毒→有没有毒] |  |  |
| 特别是肚子，很疼 | 特别是[肚子疼→肚子，很疼] |  |  |
| 旅行中，发现了 | 在他的旅行[+中] ; 神农发现[+了]很多植物 | 了completed |  |
| 一个陌生人 | 正好[有一些陌生人→一个陌生人]帮他把灵芝给他 |  |  |
| 用灵芝 | 所以他[把→用]灵芝治好了他的朋友们 |  |  |
| 找一些对身体有好处的植物 | 所以神农去[找一些植物，对身体有好处→找一些对身体有好处的植物] |  |  |
| 找到了 | 神农[找了→找到了]一个很漂亮的花 | 找look for vs.找到find |  |
| 有没有毒 | 不知道[如果有毒→有没有毒] | the “if” in “not know if + clause” is not 如果 |  |
| 给他 | 正好有一个人[帮他→给他]吃一个灵芝 |  |  |
| 另外一个人 | [一个别的人→另外一个人]跟神农说 | “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other” |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧看到很多人生病了 | better to briefly introduce “神农” when this character first appears |  |
| 什么能吃，什么不能吃 | 因为他们不知道[什么能不能吃→什么能吃，什么不能吃] |  |  |
| use神农instead of他to avoid ambiguity | 所以⟦他⟧走路走了很长的时间找药 | use神农instead of他to avoid ambiguity |  |
| delete他 | [-他]一吃就生病了 |  |  |
| 告诉人们 | 所以他回家[告诉他的人→告诉人们] |  |  |
| add a condition “要不要吃“ before “这就要看……了” | [+要不要吃，]这就要看对你的身体有没有好处了 | add a condition “要不要吃“ before “这就要看……了” |  |
| 有毒 | 有的花[是毒→有毒] |  |  |
| 病得很重 | 神农看他的朋友[很生病→病得很重] | “生病” is not an Adj., so it cannot be with 很 or 不 |  |
| delete the second他and the second神农 | [-他]想帮他们 ; 所以[-神农]去了大山 | redundant ; redundant |  |
| 特别是+N, + clause | 这个大山⟦特别是的⟧ | 特别是+N, + clause |  |
| 神农是晚上去的 | [晚上神农去了→神农是晚上去的] |  |  |
| 一走就到了 | 神农一走[-路]就走到了 ; 神农一走路就[-走]到了 |  | edit edge inside a HanLP word |
| 爬得很累 | 爬得很[麻烦→累] |  |  |
| 可是找到的是有毒的植物 | 可是[他找到毒的植物→找到的是有毒的植物] |  |  |
| 夹竹桃is not a person’s name, but a plant’s name | 所以他的朋友⟦夹竹桃⟧帮他 | 夹竹桃is not a person’s name, but a plant’s name |  |
| 把灵芝拿给生病的朋友 | 然后神农[给生病朋友灵芝→把灵芝拿给生病的朋友] | avoid “生病的朋友“ and “灵芝” close to each other |  |
| delete他们的 | [-他们的]身体越来越好 | redundant |  |
| better to briefly introduce “神农” when this character first appears | 一个叫⟦神农⟧的老人去旅行 | better to briefly introduce “神农” when this character first appears |  |
| 就尝试更多植物 | 就[测试更→尝试更多]植物 |  |  |
| 很多植物 | [很多的东西→很多植物]麻烦得很 | no的 |  |
| 麻烦is usually not used to describe植物 | 很多的东西⟦麻烦⟧得很 | 麻烦is usually not used to describe植物 |  |
| 这就要看他吃了什么 | (none) |  | no edit returned |
| (separate error in a note) | ⟦他有时候病了⟧ | the component before “这就要看……了“ should be “not definite” condition, 他会不会生病 |  |
| 他尝试各种植物尝试了很多年 | [很多年的时候，他测试别的植物→他尝试各种植物尝试了很多年] | “别的” is for “a different type”, and “all else except the spoken one” |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧看到人一吃百草就生病 | better to briefly introduce “神农” when this character first appears |  |
| 人们，一些植物 | 神农看到[人一吃百草→人们一吃一些植物]就生病 | “百草“ is a general term for “different plants” |  |
| 他问 | 他问[-了] | no了for speaking word introducing quoted speech |  |
| 你们是正好生病还是吃了这些植物所以生病 | [人→你们]正好生病还是百草让他们生病了 ; 人[+是]正好生病还是百草让他们生病了 ; 人正好生病还是[百草让他们生病了→吃了这些植物所以生病] |  |  |
| 一爬上山 | 他[一爬山→一爬上山]就找到花 |  |  |
| 肚子就疼 | 他一吃黄色的花就[有麻烦→肚子就疼] | “有麻烦“ is too vague |  |
| 另外一个人 | [别的人→另外一个人]看到神农疼死了 | “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other” |  |
| 起来了 | 神农[起床了→起来了] |  |  |
| 蓝衣男人问 | [他问→蓝衣男人问]：“你为什么疼死了？“神农说：”这就要看我吃什么 | otherwise “他” refers to神农 |  |
| 吃了什么了，吃坏肚子了 | 他问：“你为什么疼死了？“神农说：”这就要看我[+了]吃什么 ; 他问：“你为什么疼死了？“神农说：”这就要看我吃什么[+了] ; [-我觉得]我吃坏了 ; 我觉得我吃坏[+肚子]了 |  | edits do not reproduce her fix |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧看到有的植物不能吃 | better to briefly introduce “神农” when this character first appears |  |
| wrong information, 灵芝is medicine | 一个人一吃⟦灵芝⟧就死了 | wrong information, 灵芝is medicine |  |
| 因为神农想知道……，所以…… | 因为[他→神农]想知道什么植物能吃 ; [+所以]他看到什么植物就吃什么 | the first他is a bit ambiguous |  |
| wrong information, 夹竹桃 is a poison | ⟦夹竹桃很好吃，也对你的健康有好处⟧ | wrong information, 夹竹桃 is a poison |  |
| 他 | 但是[你→他]也吃过有毒的植物 |  |  |
| 给了 | [给→给了]他一些药 | 了completed |  |
| 没死 | 所以他[没死了→没死] | no了in “没+V.” |  |
| delete他 | [-他]写下了哪些植物有毒 | redundant |  |
| delete你的 | 哪些植物对[-你的]健康有好处 |  |  |
| 人们 | [别的人→人们]觉得他很聪明 | “别的” is for “a different type”, and “all else except the spoken one” |  |
| “麻烦，那些植物有没有毒？”：麻烦问一下 | 一个人问他：“[麻烦→麻烦问一下] |  | edits do not reproduce her fix |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧住在一个中国小镇 | better to briefly introduce “神农” when this character first appears |  |
| 一看到 | 神农[一看→一看到]朋友就想找药 | 看look vs.看到see |  |
| 尝了 | 他[尝→尝了]很多植物 | 了completed |  |
| 吃了以后 | 神农吃[+了]以后 | 了completed |  |
| (separate error in a note) | ⟦神农吃以后⟧ | miss the result of eating |  |
| 特别是is used to single out a typical example, but夹竹桃is not an example of灵芝 | ⟦特别是夹竹桃⟧对身体更不好 | 特别是is used to single out a typical example, but夹竹桃is not an example of灵芝 |  |
| delete但 | [-但]如果灵芝和夹竹桃一起吃 | wrong information, 灵芝is a medicine |  |
| what does the first他们refer to? what does the second他们refer to? 灵芝和夹竹桃混在一起以后变成了药 | ⟦他们混在以后给他们药⟧ | what does the first他们refer to? what does the second他们refer to? 灵芝和夹竹桃混在一起以后变成了药 |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧是很聪明的人 | better to briefly introduce “神农” when this character first appears |  |
| 看到很麻烦的情况 | 他[看得很麻烦的事情→看到很麻烦的情况] |  |  |
| 有毒，家人 | 神农现在知道哪个植物[是毒→有毒] ; 可以告诉[他的家→家人] |  |  |
| 看到了 | 他看[+到]了很多人吃毒的植物 | 看look vs.看到see |  |
| 有毒的植物 | 他看了很多人吃[+有]毒的植物 |  | edit edge inside a HanLP word |
| 常常生病 | 因为他们常常生病[-了] | no了for routine/habit |  |
| 什么植物 | 所以神农想弄清楚什么[菜→植物]健康 |  |  |
| 到了山上 | 他[到山→到了山上]以后 | 了completed, 山上is a place |  |
| delete the second他, redundant | [-他]喝了茶 | redundant |  |
| 放了很多夹竹桃 | 那杯茶他[放多的→放了很多]夹竹桃 |  |  |
| (separate error in a note) | ⟦那杯茶他放多的夹竹桃⟧ | wrong information, he directly ate夹竹桃 |  |
| 肚子/头就疼死了 | 他一喝那杯茶[，就疼死了→，肚子/头就疼死了] |  | model unsure |
| 比方说is used to express “for example”, delete it | [-比方说，]他又不能思考清楚又不能问帮忙 | 比方说is used to express “for example”, delete it |  |
| 又想不清楚又不能找别人帮忙 | 他又[不能思考清楚→想不清楚]又不能问帮忙 ; 他又不能思考清楚又不能[问帮忙→找别人帮忙] | the “ask” in “ask for help” is not问 |  |
| 给了 | 那个人给[+了]他灵芝 | 了completed |  |
| 特别有用 | 灵芝[特别是帮忙→特别有用] | ”特别是+N, + Clause” is used to single out a typical example |  |
| 植物 | 大家不知道[什么菜→植物]能吃 |  |  |
| 植物 | 神农想帮大家找到好吃的[菜→植物] |  |  |
| (separate error in a note) | ⟦神农⟧想帮大家找到好吃的菜 | better to briefly introduce “神农” when this character first appears |  |
| 比方说is used to express “for example”, delete it | [-比方说，]他吃一个麻烦的植物 | 比方说is used to express “for example”, delete it |  |
| 吃了很多奇怪的植物 | 他[吃一个麻烦的植物→吃了很多奇怪的植物] | 麻烦is not used to describe植物 |  |
| 什么植物？一种绿色的植物 | [植物→什么植物？一种绿色的植物]他觉得好吃得很 |  |  |
| 有毒 | 什么植物[是毒→有毒] |  |  |
| add a subject | (unplaced unplaceable: →) |  | could not place: teacher requests a subject but does not specify which subject; model unsure |
| 有毒 | 夹竹桃[是毒→有毒] |  |  |
| 看到 | 他正好[看→看到]神农 | 看look vs.看到see |  |
| delete他 | [-他]正好看神农 |  |  |
| 写了一本有关植物的书 | 神农写[+了一本]植物的书 ; 神农写植物[+有关]的书 |  | edits do not reproduce her fix |
| 这样 | [因为→这样]大家知道什么植物不能吃 | not “because” |  |
| 有毒的 | 特别是[毒的→有毒的]植物 |  |  |
| delete the second他 | [-他]想帮忙 | redundant |  |
| 就想帮忙 | 他[+就]想帮忙 |  |  |
| 去学 | 他走了很远的路[去了→去]学哪些植物可以入药 |  |  |
| 写了一本哪些植物是药哪些植物有毒的书 | 后来神农[写书了哪些植物是药，哪些植物是毒→写了一本哪些植物是药哪些植物有毒的书] |  |  |
| 有毒还是有药性 | 但是如果他想知道这些植物有毒[或→还是]有药性 |  |  |
| 特别危险的 | 吃不知名的植物是[特别是危险的→特别危险的] | ”特别是+N, + Clause” is used to single out a typical example |  |
| 会遇到麻烦 | 因此[时而他到了→会遇到]麻烦 | no了for habit/routine |  |
| 夹竹桃的毒特别厉害 | 夹竹桃[是特别是毒→的毒特别厉害] | ”特别是+N, + Clause” is used to single out a typical example |  |
| 正好是能做药的植物 | 因为灵芝[是正好药→正好是能做药的]植物 |  |  |
| 给了 | 神农的朋友[给→给了]他这植物 | 了completed |  |
| 灵芝 | 神农的朋友给他[这植物→灵芝] |  |  |
| delete和, 和cannot link clauses | [-和]他没病了 | 和cannot link clauses |  |
| 病好了 | 和他[没病了→病好了] | 没 +V., no了, the verb is an action verb |  |
| “所以” is not appropriate because here is not a result, 后来 | ⟦所以⟧神农告诉他有些植物是好的 | “所以” is not appropriate because here is not a result, 后来 |  |
| 有毒的 | 有些是[坏的→有毒的] |  |  |
| 知不知道 | 这就要看你[知道→知不知道]该吃哪一个了 |  |  |
| 找吃的东西很麻烦 | [很麻烦地找吃的东西→找吃的东西很麻烦] |  |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧很常走去找饭 | better to briefly introduce “神农” when this character first appears |  |
| 常常走着找能吃的植物 | 神农[很常→常常]走去找饭 ; 神农很常[走去找→走着找]饭 ; 神农很常走去找[饭→能吃的植物] ; [-他]累死了 | 常常cannot be with很 ; 走着durative ; 饭refers to rice/cooked food ; delete他 |  |
| 有毒的花 | [是毒的花→有毒的花] |  |  |
| 看到 | 一个人[看→看到]一个灵芝 | 看look vs.看到see |  |
| 是不是有用了。比方说is used to express “for example”, delete it | 他应该给神农吃吧？朋友说：“这就要看灵芝[是不是特别了→是不是有用了] ; [-比方说] | 是不是有用了。比方说is used to express “for example”, delete it ; 是不是有用了。比方说is used to express “for example”, delete it |  |
| 可能有毒 | [可能是毒的→可能有毒] |  |  |
| 给了 | ”他们给[+了]神农灵芝 | 了completed |  |
| 比方说is used to express “for example”, delete it | [-比方说] | 比方说is used to express “for example”, delete it |  |
| 带回家了/带走了 | 他把灵芝[带回走了→带回家了/带走了] | but not both回and走 |  |
| 什么植物能吃，什么植物不能吃 | 中国人不知道[什么植物可能还是不可能吃→什么植物能吃，什么植物不能吃] |  |  |
| 吃到很好吃的植物，吃了以后生病了 | 有的人[吃很好吃的植物→吃到很好吃的植物] ; 有的人[吃的生病→吃了以后生病了] |  |  |
| 有一位叫神农的老人想学习植物的知识 | [老的人→有一位叫神农的老人]叫神农 ; 老的人[叫神农，想学习→想学习植物的知识] |  |  |
| 爬了很多山，看到了很多植物 | 他[爬山→爬了很多山] ; [看很多植物→看到了很多植物] | 看look vs.看到see |  |
| 写下了他学到的知识 | 然后[写他学了什么→写下了他学到的知识] |  |  |
| 找到了 | 他[找了→找到了]第一个菜 | 找look for vs.找到find |  |
| 植物 | 他找了[第一个菜→植物] |  |  |
| 学到了什么能吃，什么不能吃 | 他[学了什么可能和不可能吃→学到了什么能吃，什么不能吃] |  |  |
| delete the second他 | [-他]学了什么可能和不可能吃 | redundant |  |
| 神农去爬山 | 神农[+去]爬山 |  |  |
| 好主意 | 神农就想到了一个好[-的]主意 |  |  |
| 马上让他更有精神了 | 这就要看[夹竹桃能不能马上给他活力→马上让他更有精神]了 |  |  |
| 结果他晕倒了 | 结果他[-也]晕倒了 |  |  |
| delete也 | 结果他[-也]晕倒了 |  |  |
| 原来……otherwise “原来” will have both “it turns out” and “originally” meaning | 夹竹桃里面⟦原来⟧也有毒 | 原来……otherwise “原来” will have both “it turns out” and “originally” meaning | model unsure |
| 吃了以后 | 所以神农吃[+了]以后就生病了 | 了completed |  |
| 觉得身体又健康了 | [-感]觉得身体健康 ; 感觉得[身体健康→身体又健康了] |  | edit edge inside a HanLP word |
| 有一个叫神农的老先生 | [一个老先生叫神农→有一个叫神农的老先生] |  |  |
| 快乐是快乐 | 他的生活[高兴是高兴→快乐是快乐] | 高兴is for short-term and can change quickly |  |
| 他的朋友邻居 | 但是[他的人民→他的朋友邻居]不知道什么植物能吃 | “他的人民”implies that神农is a king |  |
| 身体就坏了 | [一吃就身体坏了→身体就坏了] | Subj. + 就 |  |
| 有两个人 | [别的人→有两个人]正好在走路呢 | “别的” is for “a different type”, and “all else except the spoken one” |  |
| +吗 | 神农问他们：“麻烦你们能给我拿个蘑菇[+吗]？”神农告诉他们 |  | edits do not reproduce her fix |
| 有的植物 | [几棵→有的]植物可以是药 |  |  |
| 朋友邻居 | 然后神农回家告诉[他的人民→朋友邻居]什么植物能吃 |  |  |
| 可能有毒 | 他说：“很多植物[可以是毒→可能有毒] |  |  |
| 帮了 | ”神农[帮→帮了]很多人 | 了completed |  |
| 这是一个古代的故事 | [在照片的历史是一个很古代的历史→这是一个古代的故事] |  |  |
| 在照片上可以看到 | 在照片[+上]可以看一个很老的人 ; 在照片可以[看→看到]一个很老的人 | 看look vs.看到see |  |
| 老人 | 在照片可以看[一个很老的人→老人] |  |  |
| please introduce神农 | 在照片可以看⟦一个很老的人⟧ | please introduce神农 |  |
| 生病了 | 他看到很多人[很病了→生病了] | “病” is not a normal Adj., so it cannot be with 很 or 不 |  |
| 吃了 | [吃一个植物以后→吃了] | 了completed |  |
| 吃到有毒植物的地方，就帮助他 | 正好两个人在他[吃毒→吃到有毒植物]的地方 ; [他们→就]帮助老人 ; 他们帮助[老人→他] |  |  |
| 看到了 | 神农[看了→看到了]很多生病的人 | 看look vs.看到see |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧看了很多生病的人 | better to briefly introduce “神农” when this character first appears |  |
| 什么植物不能吃 | 他们不知道什么植物[-能吃]不能吃 |  |  |
| 能做药的植物 | 所以神农走了很长的时间找到[植物药→能做药的植物] |  |  |
| 可是头疼起来了 | 可是[有很多麻烦→头疼起来了] | “有很多麻烦” is too vague |  |
| 是有毒的 | 夹竹桃是[+有]毒的 |  |  |
| 请人给他灵芝 | 神农[问→请]人帮他给他灵芝 ; 神农问人[-帮他]给他灵芝 | the “ask” in “ask for help” is not问 |  |
| 看起来像伞，他一吃灵芝身体就好了 | 灵芝看起来[+像]伞 ; [灵芝→他]一吃就正好 ; 灵芝一吃[+灵芝]就正好 ; 灵芝一吃就[正好→身体就好了] |  | edits do not reproduce her fix |
| 看到 | 他[看→看到]很多病人 | 看look vs.看到see |  |
| 一……就 | 他一看[+就]觉得担心 |  | edits do not reproduce her fix |
| 植物 | 他决定到中国去找各种各样的[菜→植物]吃 |  |  |
| 有毒的 | 但是他也知道[+有]毒的植物 |  |  |
| 吃了夹竹桃以后 | [吃着夹竹桃的以后→吃了夹竹桃以后] ; 他[病得很→病得很厉害] | 着durative vs.了completed ; “病” is not a normal Adj., so it cannot be with 很 or 不 |  |
| 走过 | 一个农民正好[走路在那儿→走过] |  |  |
| 看到 | 他一[看→看到]神农就帮他 | 看look vs.看到see |  |
| 好了 | 神农[身体好的以后→身体好了] | 了completed |  |
| 很多植物不能吃 | 但是[不多植物可能吃→很多植物不能吃] |  |  |
| 他的朋友 | 他[+的]朋友帮他 |  |  |
| 给了 | 他们给[+了]神农灵芝 | 了completed |  |
| 有毒 | 夹竹桃[很毒→有毒] |  |  |
| 穿上 | 他[穿→穿上]灰色衣服以后 |  |  |
| 让耳朵变小 | 灵芝[是小耳朵的药→让耳朵变小] |  |  |
| 很多人 | [人山人海→很多人]死了 | “人山人海” is to describe a scene where there are a lot of people in a space |  |
| 问那些病人吃了什么，觉得他们吃的植物可能有毒 | 他问那些[生病人→病人]觉得这儿应该有毒 ; 他问那些生病人[+吃了什么，]觉得这儿应该有毒 ; 他问那些生病人觉得[这儿应该→他们吃的植物可能]有毒 ; 他问那些生病人觉得这儿应该有毒[-，什么都可以是毒] |  |  |
| 回到了 | 他[回了→回到了]他的城市 |  |  |
| delete “然后” | [-然后] |  |  |
| delete the second的 | 那家咖啡馆的菜[-的] |  |  |
| “所以” is inappropriate because here is not a result, delete it, add “为了找到没有毒的植物” | [-所以]他去了又空又高的山 ; [+为了找到没有毒的植物，]所以他去了又空又高的山 | “所以” is inappropriate because here is not a result, delete it, add “为了找到没有毒的植物” ; “所以” is inappropriate because here is not a result, delete it, add “为了找到没有毒的植物” |  |
| 什么都没有吃 | 可是他[没有吃了→什么都没有吃] | no了in “没+V.” |  |
| 怕有毒 | 因为他[怕毒→怕有毒] |  |  |
| 可以麻烦你给我吃的吗 | 我可以麻烦你给我吃的[+吗]？小鸟就飞去了别的地方 |  |  |
| 飞回来，他才上山 | [-直到]小鸟扑飞回上山 ; 直到小鸟[-扑]飞回上山 ; 直到小鸟扑飞回[+来]上山 ; 直到小鸟扑飞回[上山→，他才上山] |  | edits do not reproduce her fix |
| “所以” is inappropriate because here is not a result, delete it, add “在山上” | [-所以，]他吃一个香香的花 ; 他[+在山上]吃一个香香的花 | “所以” is inappropriate because here is not a result, delete it, add “在山上” ; “所以” is inappropriate because here is not a result, delete it, add “在山上” |  |
| 吃了 | 他[吃→吃了]一个香香的花 | 了completed |  |
| 还是很饿 | 但是他觉得[也饿→还是很饿] |  |  |
| 这个图书馆只有木头做的书 | [+这个]图书馆只有木的书 ; 图书馆只有[木的→木头做的]书 |  |  |
| delete “然后”, add “因为” | [-然后]他认识他在山上吃的花 ; [+因为]然后他认识他在山上吃的花 |  |  |
| delete the second他, redundant | 然后他认识[-他]在山上吃的花 | redundant |  |
| 头不疼了 | 神农吃了那个花以后[头越来越好→头不疼了] |  |  |
| “很久以前“ and ”在古代” are redundant, only keep one | (unplaced unplaceable: 很久以前，在古代→) | “很久以前“ and ”在古代” are redundant, only keep one | could not place: teacher says to retain either phrase but does not specify which one; model unsure |
| delete还 | [-还]有的有毒 |  |  |
| 有些花 | 还[有的→有些花]有毒 |  |  |
| 躺在地上的时候 | 他[在地上躺的时候→躺在地上的时候] |  |  |
| 有一个人 | 有[一位人→一个人]来了 |  |  |
| 刚尝的花 | 但是他刚[尝尝→尝]的花 | V.V. is used to make requests or plans |  |
| delete时候 | 在古代[-时候]中国人不知道什么植物可以吃 |  |  |
| 一个叫神农的中国老人 | [一个中国老人的名字是神农→一个叫神农的中国老人] |  |  |
| delete他 | [-他]决定找出什么植物可以吃 |  |  |
| 其他人 | 告诉[别的人→其他人] | “别的” is for “a different type”, and “all else except the spoken one” |  |
| 写下 | 他[写好→写下]了什么植物能吃 |  |  |
| 跳了跳 | 他[跳跳了→跳了跳] | V.V. is used to make requests or plans |  |
| 吃了 | 但是吃[+了]像伞一样的植物以后 | 了completed |  |
| 就不疼了 | 肚子[还没疼死了→就不疼了] |  |  |
| use他to replace神农，otherwise it is ambiguous, as if there are three persons referred here, in fact there are only two | [神农→他]可能会死 | use他to replace神农，otherwise it is ambiguous, as if there are three persons referred here, in fact there are only two |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧发现一件很奇怪的事情 | better to briefly introduce “神农” when this character first appears |  |
| delete他 | 虽然有的[-他]邻居一吃了植物就生病 |  |  |
| 尝了 | 神农[尝→尝了]花儿以后就发现这个花儿不但可以被用做茶 | 了completed |  |
| 远行 | 神农在他[远走→远行]的过程中碰见了一个长得像太阳的花儿 | “远走” indicates leave something behind and go to a place far away |  |
| 吃了 | [吃像伞的植物以后→吃了] | 了completed |  |
| 把这个对身体有好处的植物叫做灵芝 | [叫了这个对身体有好处的植物灵芝→把这个对身体有好处的植物叫做灵芝] |  |  |
| 过了几分钟，穿紫色衣服 | [过几个分钟→过了几分钟] ; [-一个]穿紫色的男孩儿看到了神农 ; 一个[穿紫色的→穿紫色衣服的]男孩儿看到了神农 |  |  |
| 对人们的健康 | 而且今天也继续对[别人的→人们的]健康有好处 | “别(的)” is for “a different type”, and “all else except the spoken one” |  |
| 什么植物是能吃的，什么植物是不能吃的 | 人们不知道[什么植物是不是能吃的→什么植物是能吃的，什么植物是不能吃的] |  |  |
| 因吃有毒植物生病的人 | 到处都是[人们因吃有毒植物生病了→因吃有毒植物生病的人] |  |  |
| 想尝什么植物，就尝什么植物 | 神农[什么想尝→想尝什么植物] ; 就[什么→什么植物]尝 |  | edits do not reproduce her fix |
| 看到 | 他一[看→看到]花 | 看look vs.看到see | edit edge inside a HanLP word |
| 很漂亮 | 就觉得[-是]很漂亮的 ; 就觉得是很漂亮[-的] | 是Adj.的 is to emphasize ; 是Adj.的 is to emphasize |  |
| 这朵花漂亮是漂亮 | [+这朵花]漂亮是漂亮 | here needs a subject |  |
| delete然后 | [-然后]下躺了 |  |  |
| 躺下 | 然后[下躺→躺下]了 |  |  |
| 然后 | [以后→然后]一个穿着蓝色衣服的人找到了神农 |  |  |
| 几个小时 | 神农的身体[一些→几个]小时以后变得越来越健康 |  |  |
| 另外一个穿着棕色衣服的人，那个人问 | 然后[另外一个人→另外一个穿着棕色衣服的人]看见他 ; [穿着棕色的人→那个人]问神农：“发生什么事了？”神农解释了 | otherwise it will be ambiguous, as if there are two persons to see and ask 神农 ; otherwise it will be ambiguous, as if there are two persons to see and ask 神农 |  |
| 叫夹竹桃 | 另外一个植物[-是]叫夹竹桃 |  |  |
| delete他们的 | [-他们的]儿子们不听父亲的话 |  |  |
| delete了 | 决定[-了]吃外面的植物 | “决定“ is a mental state verb, no了 |  |
| delete儿子们 | 结果[-儿子们]都病倒了 |  |  |
| 只是 | [都→只是]为了找到治病的方法 |  |  |
| 茶叶 | 他意识到[叶子→茶叶]可以帮助他们赚钱 |  |  |
| 哪些植物适合和茶叶放在一起，能做成味道最好的食谱 | 于是他记下了[哪些植物和茶叶很合，在一起味道最好的食谱→哪些植物适合和茶叶放在一起，能做成味道最好的食谱] |  |  |
| delete the second 他 | [-他]偶然看到了一朵美丽的黄花 | redundant |  |
| 高兴 | 神农[很幸福→很高兴] | 幸福is for long-term, life-related happiness |  |
| 一看到东西就吃了 | 所以[东西一看→一看到东西]就吃了 | 看look vs.看到see |  |
| 长着 | 在地上[开着→长着]很多植物 |  |  |
| 无论什么植物 | 可是一位叫神农的老人觉得无论[+什么]植物 |  |  |
| 一看到植物就吃了 | [植物一看→一看到植物]就吃了 | 看look vs.看到see |  |
| “这个植物“ is not unclear, which one? Delete 是，Adj. can be predicate, without是 | ⟦这个植物⟧的味道是最好 ; 这个植物的味道[-是]最好 | “这个植物“ is not unclear, which one? ; Adj. can be predicate, without是 |  |
| 除了知道这个植物很好吃以外，我也不知道叫什么 | 神农问他：这个植物是什么？蓝衣男人说：“[这个植物除了很好吃→除了知道这个植物很好吃]以外 ; 我也不知道[+叫什么] |  |  |
| 有一个叫神农的老人 | 在古代有[一个神农→一个叫神农的老人] |  |  |
| 什么不能吃 | [还→什么]不能吃 |  |  |
| 步行去找很多 | 所以他[走路旅行→步行去]找足多不同的植物 ; 所以他走路旅行找[足多→很多]不同的植物 |  |  |
| 也发现了一种叫夹竹桃的花 | [还花的名字是夹竹桃→也发现了一种叫夹竹桃的花] |  |  |
| 吃了 | 他吃[+了]一片花瓣 | 了completed |  |
| 给神农吃灵芝 | 一个农民[帮→给]神农吃灵芝 |  |  |
| 后来 | [以后→后来]他知道灵芝没有毒 | Time+以后 |  |
| “它“ is unclear, it seems that it refers to夹竹桃，which is a poison, not a medicine | ⟦它⟧可以做药 | “它“ is unclear, it seems that it refers to夹竹桃，which is a poison, not a medicine |  |
| 越来越多，没有那么多菜 | 所以越来越[+多]餐馆儿没有那么多盘菜就关门了 ; 所以越来越餐馆儿没有那么多[-盘]菜就关门了 |  |  |
| 环球旅行 | 有一位餐馆的老板决定[世界旅行→环球旅行]找新植物做饭 |  |  |
| please introduce 神农 | ⟦有一位餐馆的老板决定世界旅行找新植物做饭⟧ | please introduce 神农 |  |
| 好一点儿了 | [身体有一点好→身体好一点儿了] |  |  |
| delete了 | 他发现[-了]黄色花有毒 | 发现is a mental state verb, no了 |  |
| 如果用……，就可以做饭，不再有毒了 | 如果[+用]跟蘑菇一样的植物 ; [+就]做饭可以 ; [没再→不再]有毒了 |  | edits do not reproduce her fix |
| 后来 | [后面→后来]这就是老板最好的菜 |  |  |
| 大山小山，能做饭的 | 他走过[有大有小山→大山小山] ; 找到了很多[对做好饭→能做饭]的植物 |  |  |
| 但是跟牛奶一起喝 | [跟牛奶喝→但是跟牛奶一起喝] |  |  |
| 是他从自己的尝试中学到的 | 今天的奶茶是[从他对茶学到→他从自己的尝试中学到]的 |  |  |
| 一种新的黄色的花，想赶快吃下去 | 老板第一次看到[一黄色新的花→一种新的黄色的花] ; [赶快想→想赶快]吃下去 |  |  |
| delete刚才 | [-刚才] |  |  |
| 在地上 | 就[在地方→在地上]躺着 |  |  |
| 味道 | [口味→味道]太好 | 口味is for a person |  |
| 走过来 | 但是为什么我越来越累了？ 一个男人[去过来→走过来] |  |  |
| 不能动 | 老板[不可→不能]动 |  |  |
| 让男人 | 得[问→让]男人给他地方上像蘑菇一样的植物吃了 | the “ask” in “ask sb. to do” is not问 |  |
| 把地上……给他吃了 | 得问男人[给他地方上像蘑菇一样的植物吃了→把地上像蘑菇一样的植物给他吃了] | to avoid “他” and “地上像……的植物” too close to each other | edits do not reproduce her fix |
| 有点儿甜，也有点儿咸 | [+有]一点儿甜一点儿咸 ; 一点儿甜[一点儿咸→也有点儿咸] |  | edits do not reproduce her fix |
| delete他要回家 | [-他要回家] |  |  |
| 这样 | [所以→这样]王朋也可以吃一个蘑菇 |  |  |
| delete the second王朋 | [-王朋]不再哭了 | delete the second王朋 |  |
| delete the second我们 | 我们不知道[-我们]可以吃什么植物 | redundant |  |
| 很多人 | 很多[-的]人吃了有毒的饭 | no的 |  |
| 有毒的植物 | 很多的人吃了有毒的[饭→植物] |  |  |
| delete the second我们 | 所以我们现在知道[-我们]可以吃什么植物 | redundant |  |
| 找到可以吃的植物 | 神农开始[找我们可以吃的植物→找到可以吃的植物] |  |  |
| delete我们 | 神农开始找[-我们]可以吃的植物 |  |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧开始找我们可以吃的植物 | better to briefly introduce “神农” when this character first appears |  |
| 吃到result, 写下 | 他⟦一吃新的植物就写了植物有没有毒⟧ | 吃到result, 写下 |  |
| 能不能吃 | 这个植物[你能吃吗→能不能吃] |  |  |
| delete the last two植物的 | 这就要看植物的大小、[-植物的]长短、植物的颜色了 ; 这就要看植物的大小、植物的长短、[-植物的]颜色了 |  |  |
| 很多中国的 | 他找到了[很多的中国的→很多中国的]植物 |  |  |
| 中国最有名的 | 中国[-的]最有名的植物——茶 |  |  |
| 吃到有毒的植物 | 特别是[他吃毒→吃到有毒的植物]的时候 |  |  |
| 有毒植物他吃了很多次 | [毒→有毒植物]他吃很多次 ; 毒他吃[+了]很多次 | 了completed |  |
| 有人 | 因为[别的人→有人]正好在他的旁边 | “别的” is for “a different type”, and “all else except the spoken one” |  |
| 灰色头发的叫神农的老人的故事 | 有一个[关于灰色的头发老老的人叫神农的故事→灰色头发的叫神农的老人的故事] |  |  |
| 在空气新鲜的山里走路，很多人在吃植物 | 神农在[新鲜空气的山→空气新鲜的山里]走路看到几种的植物 ; 神农在新鲜空气的山走路[-看到几种的植物，也看到了]很多人吃植物 ; 也看到了[+，]很多人吃植物 ; 也看到了很多人[+在]吃植物 | 在ongoing |  |
| 开着的…… | 找到了开着[+的]黄色的像星星一样的花 |  |  |
| 躺在地上/在地上躺着 | 看到了神农[躺着地上→躺在地上] |  | edits do not reproduce her fix |
| 几分钟过去，感觉越来越好 | 几分钟[过来→过去] ; [神农→感觉]越来越好 |  |  |
| 谢谢那个穿蓝色衣服的人 | [穿上一件蓝色的衣服的人→那个穿蓝色衣服的人] | 穿上is for a dynamic, ongoing action |  |
| 发现 | 这个像伞一样的植物有毒吗？神农发现[-了]那个植物是灵芝 | no了 |  |
| 他对植物可以做药还是有毒特别关心 | 他[特别关心关于可以做药还是有毒的植物→对植物可以做药还是有毒特别关心] |  |  |
| 吃了以后生病了，吃了以后没事儿 | 有些人[吃生病了→吃了以后生病了] ; 有些人[吃得好→吃了以后没事儿] |  |  |
| 发现is a mental state verb, no了 | 神农发现[-了]大家都不知道什么植物能吃 | 发现is a mental state verb, no了 |  |
| 跑遍大山小山 | 他[跑遍→跑遍大山小山]尝尝各种各样的植物 | 跑遍 + place |  |
| 尝了 | 他跑遍[尝尝→尝了]各种各样的植物 | V.V. is used to make requests or plans |  |
| 有一天，像太阳一样的黄色的花 | 有[一时→一天，]找到了一株黄色的花像太阳一样的 ; 有一时[找到了一株黄色的花像太阳一样的→像太阳一样的黄色的花] |  |  |
| “这种植物” is unclear, sine preceding sentence has two types of plants | ⟦这种植物⟧原来是茶 | “这种植物” is unclear, sine preceding sentence has two types of plants |  |
| delete这些植物 | [-这些植物]对身体好处 |  |  |
| 对身体有好处 | 这些植物对身体[+有]好处 |  |  |
| 在笔记本上 | 就在笔记本[+上]写下来观测结果 |  |  |
| 走到一个漂亮的地方的时候 | 有一天神农[走过去→走到一个]漂亮的地方的时候 |  |  |
| 有一个问题better | 但是他有一个[麻烦→问题] | 有一个问题better |  |
| 会让他生病 | 他都不知道什么植物[让他生病了→会让他生病] | not occur yet, no了 |  |
| 看到 | 他一[看→看到]植物就吃 | 看look vs.看到see |  |
| delete the second他 | [-他]吃了以后 | redundant |  |
| 会死吗 | 我会死[-了]吗？医生回答：不见得 | no 了 |  |
| 吃了 | 神农[吃→吃了]灵芝以后 | 了completed |  |
| 古代，很多人每天都吃很多植物 | [古代的生活→古代，]很多的人吃很多的植物 ; 古代的生活很多[-的]人吃很多的植物 ; 古代的生活很多的人[+每天都]吃很多的植物 ; 古代的生活很多的人吃很多[-的]植物 |  |  |
| 一些人 | 可是一些[-的]人一吃植物 | no的 |  |
| it does not make sense to ask about the man in purple | 他问：⟦穿着紫色衣服的男人怎么了⟧？我一会儿死了一会儿身体最好的 | it does not make sense to ask about the man in purple |  |
| 一会儿很难受一会儿觉得好一点儿了 | 他问：穿着紫色衣服的男人怎么了？我一会儿[死了→很难受]一会儿身体最好的 ; 他问：穿着紫色衣服的男人怎么了？我一会儿死了一会儿[身体最好的→觉得好一点儿了] |  |  |
| 紫衣人 | [紫色人→紫衣人]告诉他：你吃了灵芝 |  |  |
| 你是身体就好了 | [一吃就你的身体最好的→你是身体就好了] | Subj.+就 | model unsure |
| delete和 | [-和]这个花是毒 | 和cannot connect clauses |  |
| 有毒 | 和这个花[是毒→有毒] |  |  |
| 特别是 | [特别很→特别是]新鲜的时候 |  |  |
| 是药 | 可是这个灵芝可能[是啊→是药] |  |  |
| 吃下去很多植物 | 神农[加→吃]下去很多的植物 ; 神农加下去很多[-的]植物 |  |  |
| 看看是毒还是药 | 看看[如果→是]毒还是药 | the “if” in “see if + clause” is not 如果 |  |
| 是很有名的人，对这个时代的医学有贡献 | 我觉得神农[+是]很有名的人 ; [因为他作用这个时代的医学→对这个时代的医学有贡献] |  |  |
| 他们吃的植物有毒 |  [因为他们吃毒→他们吃的植物有毒] |  |  |
| 决定 | 一个老人决定[-了] | “决定” is a mental state verb, no了 |  |
| 走到很远的地方，尝试很多植物 | [坐路很远→走到很远的地方] ; [吃很多的植物→尝试很多植物] |  |  |
| delete如果 | 看看[-如果]能吃还是不能吃 | the “if” in “see if + clause” is not 如果 |  |
| 是药还是毒 | [药还是毒→是药还是毒] |  |  |
| 都写下了这些植物的用处 | [就在植物用上写了→都写下了这些植物的用处] |  |  |
| 开在山上/在山上开着 | [开着山上→开在山上] |  | edits do not reproduce her fix |
| no了for speaking word | 神农说：我死了吗？他一说[-了] | no了for speaking word |  |
| 一个穿着蓝色衣服的人就来了 | [就穿着蓝色的衣服的人来→一个穿着蓝色衣服的人就来了] | Subj.+就 |  |
| 给了 | [给→给了]他一个灵芝 | 了completed |  |
| 好了以后 | 神农的肚子[最好→好了]以后 |  |  |
| better to briefly introduce “神农” when this character first appears | ⟦神农⟧看到很多人随便吃各种植物 | better to briefly introduce “神农” when this character first appears |  |
| 这样人们 | [所以人→这样人们]以后不会生病 |  |  |
| 神农开始了旅程，在旅程中 | 神农[出发在一个旅程→开始了旅程] ; 他[在这个旅程→在旅程中]尝了很多植物 |  |  |
| delete他 | [-他]在这个旅程尝了很多植物 | redundant |  |
| 就病得很重 | 这朵花他一吃就[很生病→病得很重] | “生病”cannot be with “很” |  |
| 快要死了 | 快要死[+了] |  |  |
| 给了 | 给[+了]他一个灵芝 | 了completed |  |
| 知识 | 神农写下来他所有学到的[事情→知识] |  |  |
| better to briefly introduce “神农” when this character first appears | 所以⟦神农⟧去旅行 | better to briefly introduce “神农” when this character first appears |  |
| 学习植物的知识 | [学习植物→学习植物的知识] |  |  |
| delete你的 | 喝茶对[-你的]身体有好处 |  |  |
| delete吃 | 可是[-吃]夹竹桃有毒 |  |  |
| 吃了 | 神农[吃→吃了]一个夹竹桃 | 了completed |  |
| 然后 | [他以后→然后他]正好看一个灵芝 | Time+以后 |  |
| 他正好看到 | 他以后正好[看→看到]一个灵芝 | 看look vs.看到see | edits do not reproduce her fix |
| 身体就好了 | 他一吃灵芝[就身体好了→身体就好了] | Subj. + 就 |  |
| delete是 | 你应该特别[-是]小心 | Adj. can be predicate |  |
| add a condition before “这就要看……了“ | (unplaced unplaceable: →) | e.g., 蘑菇能不能吃 | could not place: teacher requests an unspecified condition before the quoted clause; model unsure |
| 这就要看蘑菇像不像伞了 | 这就要看蘑菇[看不看像伞→像不像伞了] | e.g., 蘑菇能不能吃 |  |
| 他发现人们 | [他的人民→他发现人们]又饿又病 | “他的人民”implies that神农is a king |  |
| 能安全地吃 | 每个人都不知道哪些植物能安全[+地]吃 |  |  |
| 找能吃的植物 | [找植物能吃→找能吃的植物] |  |  |
| 另外一种白花 | 然后他又找到了[别的→另外一种]白花 | “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other” |  |
| it does not answer the previous Q “什么植物可以吃?” | ⟦这就要看你吃什么植物了⟧ | it does not answer the previous Q “什么植物可以吃?” |  |
| 关于植物有没有毒，我学到了 | [对植物我学到了→关于植物有没有毒，我学到了] |  |  |
| 写下来 | 我会[写起来→写下来] |  |  |
| 什么植物能吃，什么植物不能吃 | 让每个人都知道[什么植物能不能吃→什么植物能吃，什么植物不能吃] |  |  |
