# Step 2 report: paragraphs -> corpus

## Counts

| Story | Samples | Sentences | Feedback lines | Parts | Content flags |
|---|---|---|---|---|---|
| mengmu_san_qian | 51 | 502 | 400 | 479 | 47 |
| shennong_chang_baicao | 52 | 669 | 425 | 521 | 50 |
| pear_story | 4 | 83 | 88 | 123 | 0 |

Model stories: shennong_chang_baicao, mengmu_san_qian, chang_e_ben_yue, zhang_qian_chu_shi_xi_yu (84 sentences)

## Locating the teacher's quotes in the student's story

Each feedback line starts with the student text the teacher is commenting on. This is where it was found:

| Match | Lines | Meaning |
|---|---|---|
| exact | 912 | same characters |
| normalized | 1 | same once spaces and punctuation are ignored |
| fuzzy | 0 | close but not identical (similarity >= 0.6) -- **check** |
| not_found | 0 | not found -- **check** |

## Splitting the teacher's feedback

After the quote, each line is split into parts (on ；/;) and each part into pieces labelled
**fix** (Chinese correction), **note** (explanation, contains Latin letters) or **instruction** (starts with delete/add/...).

- parts: 1123; pieces: fix 979, note 612, instruction 158
- parts with no fix (note or instruction only): 270
- fixes with alternatives (A/B): 23
- pieces with bold characters: 22

### Parts to check (14)

- mengmu_samples#2 f3p0: Chinese after a note in the same part (may be an example, not a fix) -- [note] miss a Subj. | [fix] 孟子练习写字 | [note] 文字 is a general term, not for specific individual characters
- mengmu_samples#44 f1p0: Chinese after a note in the same part (may be an example, not a fix) -- [note] wrong conjunctions, 他只要跟朋友玩儿 | [fix] 妈妈就抱怨 | [note] 只要……就as long as
- mengmu_samples#44 f1p1: Chinese after a note in the same part (may be an example, not a fix) -- [note] or 他有的时候跟朋友玩儿 | [fix] 妈妈就有别的看法
- shennong_samples#1 f8p0: Chinese after a note in the same part (may be an example, not a fix) -- [instruction] add a condition before “这就要看……了“ | [note] e.g., 如果吃了夹竹桃 | [fix] 病能不能好？这就要看你吃没吃灵芝了 | [note] 不for habit/routine/willingness, 没for non-occurrence of an event
- shennong_samples#2 f3p0: Chinese after a note in the same part (may be an example, not a fix) -- [note] the component before “这就要看……了“ should be “not definite” condition, 他会不会生病 | [fix] 这就要看他吃了什么
- shennong_samples#4 f8p0: Chinese after a note in the same part (may be an example, not a fix) -- [note] “男人” is moving to神农(dynamic) while “灵芝” is next to神农(static), so it’s better not to combine the two | [fix] 一个男人正好过来 | [fix] 看到我的旁边长着一个灵芝
- shennong_samples#7 f5p0: Chinese after a note in the same part (may be an example, not a fix) -- [instruction] add a condition before “这就要看……了“ | [note] e.g., 蘑菇能不能吃 | [fix] 这就要看蘑菇像不像伞了
- shennong_samples#10 f3p0: Chinese after a note in the same part (may be an example, not a fix) -- [note] it is confusing to have花 | [fix] 夹竹桃 | [fix] 这个花 | [note] it looks like they refer to two different flowers, but actually the same. 吃一种叫夹竹桃的花的时候
- shennong_samples#29 f3p0: Chinese after a note in the same part (may be an example, not a fix) -- [fix] 爬了很多山 | [fix] 看到了很多植物 | [note] 看look vs.看到see | [fix] 写下了他学到的知识
- shennong_samples#35 f7p0: Chinese after a note in the same part (may be an example, not a fix) -- [note] the “if” in “not know if + clause” is not 如果, delete如果 | [fix] 有没有毒
- pear_story#4 f7p0: Chinese after a note in the same part (may be an example, not a fix) -- [note] 水果是……梨子 is not very precise, 我们地位低的水果 | [fix] 虽然是世界上最美丽的
- pear_story#4 f19p0: Chinese after a note in the same part (may be an example, not a fix) -- [note] the coherence needs to be improved, 但我没想到的是 | [fix] 他很久以前可能并不是这样碌碌无为 | [fix] 而是拿到了硕士和博士学位
- pear_story#4 f22p0: Chinese after a note in the same part (may be an example, not a fix) -- [note] instead of using “有……” structure, it is better to use short sentences: 学历很高 | [fix] 主修专业竞争力也很强。
- pear_story#4 f23p1: Chinese after a note in the same part (may be an example, not a fix) -- [note] “却” indicates unexpected semantic turn, “使” is more formal and better fit other formal words like “失业 | [fix] 被迫 | [fix] 转行” | [note] adding “并” will increase the coherence.

### Feedback lines with no colon, not parsed (0)

None.

## Content flags

- miss_scene: 89
- wrong_information: 5
- coherence_problem: 3
- missing scenes listed: 240
- samples without the closing note: 7

## The teacher's required-scene lists (`story_scenes.md`)

**神农尝百草** (7 scenes)

1. in ancient times, people did not know which plants can be eaten, so people often got sick after eating some plants
2. 神农decided to find out which plants are safe to eat and which are not, so he climbed mountains to try different plants
3. 神农found茶and took a record
4. 神农tried 夹竹桃 and fainted
5. a person in blue stopped by and gave灵芝to 神农，神农felt better after eating灵芝
6. another person in brown came by and had a conversation with 神农
7. 神农takes record of灵芝and夹竹桃

**孟母三迁** (5 scenes)

1. 孟子and孟母lived near a graveyard, and 孟子 imitated how to offer sacrifices every day
2. 孟母 decided to move away from the neighborhood near the graveyard because she thought imitating how to offer sacrifices would have a bad impact on 孟子
3. 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
4. 孟母 moved from the market to the neighborhood near a school, 孟子started to study every day
5. 孟子becomes a famous philosopher

**嫦娥奔月** (9 scenes)

1. 嫦娥and后羿are fairy gods who can fly
2. there are 10 suns and it is too hot
3. 后羿shot 9 suns down
4. the sun god took away 后羿 and嫦娥’s power and they cannot fly
5. 后羿went to 王母’s palace to ask for her help
6. 王母 gave him two pills and told him that taking one pill can make one immortal and taking two pills can make one fly
7. 后羿returned and told嫦娥
8. when后羿 was asleep, 嫦娥 took two pills
9. 嫦娥 flies to the moon and cannot go back, she stays with a rabbit on the moon

**张骞出使西域** (13 scenes)

1. 匈奴 often intrudes 汉朝, grabbing the food and attacking the people
2. 汉武帝 ordered 张骞 to lead a delegation to go to 大月氏 to build an alliance to resist 匈奴together, because 大月氏 is a neighbor of 匈奴 and has been attached by 匈奴 in the past
3. 张骞 led a delegation of over 100 people, among whom 甘父 was the guide because he used to be a slave of 匈奴 and got to know the terrain very well
4. the delegation needs to go through the dessert and when they took a rest one day, 匈奴 suddenly attached them
5. 张骞 was captured and became a slave of匈奴, he had herded sheep for 匈奴 for ten years
6. one day, when 匈奴 was attacked and there was a chaos, 甘父 found 张骞 and took him to escape
7. 张骞, 甘父 and the rest of the delegation continued their mission and went west
8. they came to 大宛，another minority tribe, and 大宛’s king wanted to have trade with 汉朝, so he showed 张骞 and his delegation 大宛’s products and palace, equipped them with horses and food, and guided the way to大月氏
9. 张骞 and his delegation finally arrived at 大月氏 and met 大月氏’s queen, 张骞 told her about 汉武帝’s plan of alliance, but 大月氏’s queen rejected, because they have moved to a new place so 匈奴 did not attack them for a long time, and they don’t want to have any war anymore
10. 张骞 and his delegation had to go back to 长安，汉朝’s capital, and there were only 3 persons left when they arrived at 长安
11. 张骞 reported what he saw and learned along this journey, and because of this information, 汉朝 defeated 匈奴
12. 张骞 wrote down what he learned about the West and the route he took become 丝绸之路, and China and the West started to make trade, China’s silk and tea were exported to the West and the fruits and spices from the West were imported to China
13. the historians recorded 张骞’s story and his great contributions

## HanLP parse units (`parse_units.jsonl`)

- model_sentence: 84
- student_sentence: 1254
- teacher_fix: 1002

## Three samples in full, for checking

### mengmu_samples#1

Sentences:

- s0 [0-40] 在古代中国，有一位小孩子叫孟子，他妈妈在墓地工作，所以孟子老是在墓地跟朋友祭拜。
- s1 [40-67] 孟母觉得这样住对孟子将来没有好处，所以她想找新的工作。
- s2 [67-85] 为了找工作，孟母和孟子搬了很多次家。
- s3 [85-99] 孟子才九岁，已经搬了五次家。
- s4 [99-141] 孟母找工作很难，不是因为她的工作经验不够，而是因为她想在老师的家工作，让孟子多学习。
- s5 [141-160] 孟母终于在一位很有名的文学家找工作了。
- s6 [160-199] 孟子常常搬家，害得他没有时间交新朋友，所以他没有很多朋友，觉得每天学习没问题。
- s7 [199-251] 他每天在文学家的房子上学，从早到晚一直学习，他不是看书就是写文章，难怪他长大以后就成为了很有名的哲学家。
- s8 [251-284] 他对孩子的童年的看法是，说孩子童年多玩或者多学习重要，我都能理解。
- s9 [284-320] 可是我很感激我妈妈叫我多学习，因为我学习很多，我现在有良好的教育和生活。

Feedback:

- **f0** "有一位小孩子叫孟子" → exact [6-15] in s0
  - p0: [fix] 有一个叫孟子的小孩子 | [note] “位” is a polite MW.
- **f1** "孟母终于在一位很有名的文学家找工作了" → exact [141-159] in s5
  - p0: [fix] 作家的家里找到工作了 | [note] 找look for vs. 找到find
- **f2** "他每天在文学家的房子上学" → exact [199-211] in s7
  - p0: [fix] 房子里 | [note] 在+Place
- **f3** "他对孩子的童年的看法是，说孩子童年多玩或者多学习重要" → exact [251-277] in s8
  - p0: [fix] 在被问到对童年应该做什么的看法时 | [fix] 他说：孩子童年多玩重要和多学习重要
- **f4** "我现在有良好的教育和生活" → exact [307-319] in s9
  - p0: [fix] 幸福的生活 | [note] 良好 is usually not with生活

Content flags:

- [miss_scene] Miss one scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day

### shennong_samples#1

Sentences:

- s0 [0-20] 古代的人都不知道他什么能吃，什么不能吃。
- s1 [20-58] 神农看到很多人吃了麻烦的植物，比方说一个人生病了，一个孩子哭了，一个人晕了。
- s2 [58-71] 神农旅行了，吃过新的植物。
- s3 [71-87] 他找到了很多有用植物，特别是茶。
- s4 [87-105] 他吃了夹竹桃，夹竹桃一吃，就生病了。
- s5 [105-122] 一个人正好找了神农，他给神农灵芝。
- s6 [122-143] 一吃夹竹桃就死，这就要看你也吃不吃灵芝了。
- s7 [143-158] 神农没死了，因为他也吃了灵芝。

Feedback:

- **f0** "古代的人都不知道他什么能吃" → exact [0-13] in s0
  - p0: [instruction] Delete “他”
- **f1** "神农看到很多人吃了麻烦的植物" → exact [20-34] in s1
  - p0: [note] better to briefly introduce “神农” when this character first appears
  - p1: [fix] 有害的植物
- **f2** "神农旅行了，吃过新的植物" → exact [58-70] in s2
  - p0: [note] it is loosely connected with the previous sentence, better add “为了帮助人们找到能吃的植物”, 神农决定去旅行尝试新的植物，“过” is to express “experience”, now the experience has not yet been experienced
- **f3** "他找到了很多有用植物" → exact [71-81] in s3
  - p0: [fix] 有用的植物
- **f4** "夹竹桃一吃，就生病了" → exact [94-104] in s4
  - p0: [fix] 他就生病了 | [note] otherwise it is ambiguous who gets sick
- **f5** "一个人正好找了神农" → exact [105-114] in s5
  - p0: [fix] 找到了 | [note] 找look for vs.找到find
- **f6** "他给神农灵芝" → exact [115-121] in s5
  - p0: [fix] 给了 | [note] 了completed
- **f7** "一吃夹竹桃就死" → exact [122-129] in s6
  - p0: [note] it is unclear what the subject is, add “神农说：一吃夹竹桃就不舒服”, it is not “死”
- **f8** "这就要看你也吃不吃灵芝了" → exact [130-142] in s6
  - p0: [instruction] add a condition before “这就要看……了“ | [note] e.g., 如果吃了夹竹桃 | [fix] 病能不能好？这就要看你吃没吃灵芝了 | [note] 不for habit/routine/willingness, 没for non-occurrence of an event
- **f9** "神农没死了" → exact [143-148] in s7
  - p0: [instruction] delete了 | [note] 没+ V.

Content flags:

- [miss_scene] Miss three scenes: 神农became better after eating灵芝；another person came by and had a conversation with 神农；神农takes record of灵芝and夹竹桃

### pear_story#1

Sentences:

- s0 [0-7] 今天天气很好。
- s1 [7-22] 张先生在梨子树口摆着一张梯子。
- s2 [22-45] 张先生爬上去梯子，摘下来一些梨子，爬下来梯子。
- s3 [45-64] 他有三个筐，在第三个筐里放着那些梨子。
- s4 [64-90] 他又爬上去梯子的时候，马先生跟他的驴走去筐的后边来。
- s5 [90-108] 马先生不喜欢梨子，而小王很喜欢梨子。
- s6 [108-139] 小王骑自行车到张先生的梨子树，一看，这么多梨子，就拿一筐水果。
- s7 [139-164] 可是那筐水果太重，他的自行车太小，他也丢三落四的。
- s8 [164-189] 小王在马路骑自行车一看到别个人，一下子就撞自行车。
- s9 [189-198] 小王和那筐梨子倒。
- s10 [198-206] 他擦腿，疼死了。
- s11 [206-219] 三个孩子看到小王，去帮他。
- s12 [219-245] 一个孩子在马路看到小王的帽子，拿上去，把帽子给小王。
- s13 [245-259] 小王说谢谢，给孩子三个梨子。
- s14 [259-292] 孩子一直走去张先生的树，吃梨子，觉得这些梨子比别的水果最好不过了。
- s15 [292-308] 张先生一爬下来梯子，就看到孩子。
- s16 [308-341] 他呢，觉得他们偷他的梨子，孩子呢，觉得张先生把一筐梨子送了给小王。

Feedback:

- **f0** "张先生在梨子树口摆着一张梯子" → exact [7-21] in s1
  - p0: [fix] 张先生在梨子树口摆了一张梯子 (bold: 了) | [note] Subj. V. 了 (completed) Obj., or 梨子树口摆着一张梯子，Place + V. 着 + Obj.
- **f1** "爬上去梯子" → exact [25-30] in s2
  - p0: [fix] 爬上梯子去 | [note] V. + directional complement + Place + 来/去
- **f2** "爬下来梯子" → exact [39-44] in s2
  - p0: [fix] 爬下梯子来 | [note] V. + directional complement + Place + 来/去
- **f3** "在第三个筐里放着那些梨子" → exact [51-63] in s3
  - p0: [fix] 在第三个筐里放着一些梨子 | [note] the Obj. in “Place + V. 着 + Obj.” is usually “number + MW + noun”, not specific “that/this/those/these/the + noun”.
- **f4** "又爬上去梯子的时候" → exact [65-74] in s4
  - p0: [fix] 又一次爬上梯子的时候
- **f5** "马先生跟他的驴走去筐的后边来" → exact [75-89] in s4
  - p0: [fix] 马先生牵着驴走到筐的后边来 | [note] “跟/和+noun.” is used for multiple nouns that have the same action, we can say: 马先生和张先生走……，because both 马先生and 张先生 “walk”, but here “驴” does not walk by itself, but walked by 马先生, so you need to use the accompanying phrase “V.着”
  - p1: [note] 走到place来/去，cannot say “走去/来Place”
- **f6** "小王骑自行车到张先生的梨子树" → exact [108-122] in s6
  - p0: [fix] 到张先生的梨子树下 (bold: 下) | [note] 到 + place
- **f7** "就拿一筐水果" → exact [132-138] in s6
  - p0: [fix] 就拿了一筐梨子 (bold: 了) | [note] 了completed, “水果” is more generic and here it should be “梨子”，otherwise it will cause ambiguity, what “fruits” other than “pears”?
- **f8** "小王在马路骑自行车一看到别个人" → exact [164-179] in s8
  - p0: [fix] 在马路上 (bold: 上) | [note] 在+ place
  - p1: [fix] 骑着自行车 (bold: 着) | [note] “着” is for “durative”
  - p2: [fix] 另外一个人/一个女孩子 | [note] there is no “别个人”.
- **f9** "一下子就撞自行车" → exact [180-188] in s8
  - p0: [fix] 自行车一下子就撞到石头了 | [note] “撞自行车” means to hit the bike, in fact, it is: the bike hit the rock.
- **f10** "小王和那筐梨子倒" → exact [189-197] in s9
  - p0: [fix] 小王和那筐梨子倒了 (bold: 了) | [note] 了completed/change
- **f11** "他擦腿" → exact [198-201] in s10
  - p0: [fix] 他擦了一下腿/擦着腿 | [note] either 了completed or 着 durative
- **f12** "一个孩子在马路看到小王的帽子，拿上去" → exact [219-237] in s12
  - p0: [fix] 在马路上 (bold: 上) | [note] 在+ place
  - p1: [note] 拿起来pick up，拿上去means “bring it up”
- **f13** "给孩子三个梨子" → exact [251-258] in s13
  - p0: [fix] 给了孩子三个梨子 (bold: 了) | [note] 了completed
- **f14** "孩子一直走去张先生的树，吃梨子" → exact [259-274] in s14
  - p0: [fix] 走到张先生的树下 (bold: 到, 下) | [note] 走到place来/去，cannot say “走去/来Place”
  - p1: [fix] 吃着梨子 | [note] 着 durative
- **f15** "觉得这些梨子比别的水果最好不过了" → exact [275-291] in s14
  - p0: [fix] 比别的水果都好/最好不过了 | [note] 最好不过了cannot be used in comparative sentences, it means “the best option”.
- **f16** "一爬下来梯子" → exact [295-301] in s15
  - p0: [fix] 一爬下梯子来 | [note] V. + directional complement + Place + 来/去
- **f17** "他呢，觉得他们偷他的梨子" → exact [308-320] in s16
  - p0: [fix] 偷了 | [note] 了completed
- **f18** "孩子呢，觉得张先生把一筐梨子送了给小王" → exact [321-340] in s16
  - p0: [fix] 送给了小王

Content flags:


