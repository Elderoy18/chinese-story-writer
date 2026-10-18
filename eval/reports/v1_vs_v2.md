# v1 vs v2, scored on the teacher's critique

Stories: the 6 held-out stories of the v1 eval (mengmu #10, #32, #45; shennong #8, #19, #33), 18 scenes, the same scene splits in both systems. v1 = eval stages S5 and S6 (`eval/runs/`); v2 = `chinese_writing_rag_pipeline_v2/runs/S0`. Nothing was regenerated.

Judge: gpt-5.6-terra (medium), blind to the system, given her corrections on each scene as reference. Prompt versions: items 03f3eb7978, expressiveness 3be25f3186, content 47505bee5c. Where she corrected a place, the item counts as a real error whatever the judge says.

| | v1-S5 | v1-S6 | v2-S0 |
|---|---|---|---|
| Correction items shown | 78 | 87 | 101 |
| **4. False positives and incorrect corrections** (her top priority) | | | |
| False positives (judged) | 8 (0.44/scene) | 11 (0.61/scene) | 14 (0.78/scene) |
| &nbsp;&nbsp;worst case: every item at a place she did not mark | 23 (1.28/scene) | 28 (1.56/scene) | 25 (1.39/scene) |
| Incorrect corrections (real error, wrong fix) | 12 (0.67/scene) | 8 (0.44/scene) | 37 (2.06/scene) |
| Items fully right (real error, right fix, clean corrected text) | 49/78 (63%) | 64/87 (74%) | 31/101 (31%) |
| **2. Corrected version** | | | |
| Corrected text after → not fully correct | 16/78 (21%) | 12/87 (14%) | 54/95 (57%) |
| **1. Partial sentences** | | | |
| Shown text partial (truncated or judged incomplete) | 3/78 (4%) | 3/87 (3%) | 39/101 (39%) |
| &nbsp;&nbsp;of which truncated with … | 0/78 (0%) | 0/87 (0%) | 39/101 (39%) |
| **3. Categories** | | | |
| In Other / Content | 0/78 (0%) | 0/87 (0%) | 8/101 (8%) |
| Wrong category (as shown) | 2/78 (3%) | 5/87 (6%) | 37/101 (37%) |
| Wrong category, Grammar and Vocabulary merged | 2/78 (3%) | 5/87 (6%) | 21/101 (21%) |
| **5. End-of-story content** | | | |
| Scenes she flagged, caught | 15/15 (100%) | 14/15 (93%) | 12/15 (80%) |
| Content notes that are correct | 27/27 (100%) | 29/29 (100%) | 25/26 (96%) |
| Content notes that are clear (judged) | 27/27 (100%) | 29/29 (100%) | 26/26 (100%) |
| Content notes worded 'miss…' / 'need…' | 22/27 (81%) | 24/29 (83%) | 0/26 (0%) |
| **6. Expressiveness** | | | |
| Good ideas: 孟母 | 17/23 (74%) | 19/26 (73%) | 19/26 (73%) |
| Good ideas: 神农 | 20/24 (83%) | 21/25 (84%) | 17/25 (68%) |
| **Recall (last)** | | | |
| Her corrections covered by an item | 65/88 (74%) | 64/88 (73%) | 75/88 (85%) |
| Items whose student words could not be located | 1 | 2 | 1 |

## False positives by strength (v2 marks some items as suggestions)

- v1-S5: error 8/78 (10%)
- v1-S6: error 11/87 (13%)
- v2-S0: error 8/74 (11%), suggestion 6/27 (22%)

## Expressiveness problems (judged)

- v1-S5: 孟母 {'bad_example': 1, 'redundant': 5}; 神农 {'redundant': 2, 'off_story': 2}
- v1-S6: 孟母 {'redundant': 7}; 神农 {'redundant': 3, 'contradicts': 1}
- v2-S0: 孟母 {'off_story': 2, 'bad_example': 1, 'redundant': 4}; 神农 {'redundant': 4, 'off_story': 2, 'bad_example': 2}

## How far to trust the judge

Her tagged comments on v2's feedback (6 stories, 104 comments) were matched to v2's items. For each kind of problem she named, the share the judge also caught (her comments are not exhaustive, so this measures whether the judge sees what she sees, not how much else it flags):

- false_positive: 4/6 (67%)
- incorrect_correction: 17/19 (89%)
- miscategorized: 18/24 (75%)
- partial_sentence: 26/26 (100%)
- comments on correction items that could not be matched to an item: 29

## Every false positive and incorrect correction

### v1-S5

- mengmu_samples#10 scene 1 [Coherence: reference] `Coherence (Reference): 孟子小的时候：有一个小男孩叫孟子。孟子小的时候，This is the first mention of the main character, so use a brief introduct` -- after_not_correct -- 孟子首次出现时需要先作简短介绍，但改后文字以逗号结尾，仍不是完整句子。
- mengmu_samples#10 scene 2 [Grammar & Vocabulary] `老是读书：一直读书，老是 has a negative, complaining tone; 一直 neutrally describes an ongoing study habit.` -- incorrect -- 老是读书 is acceptable here, and the teacher's own correction retains 老是读书.
- mengmu_samples#10 scene 2 [Coherence: connectors] `Coherence (Conjunction): 因为孟子现在没有朋友，他一直读书：因为孟子现在没有朋友，所以他一直读书，use 因为……所以…… to connect the cause with its result.` -- incorrect, after_not_correct -- The teacher's correction shows that studying too much is the cause of having no friends, whereas the system keeps the causal relation reversed.
- mengmu_samples#10 scene 3 [Coherence: reference] `Coherence (Reference): 孟子从五岁一直学哲学：他从五岁一直在学习哲学，Use a pronoun for a close re-occurrence: 孟子 was named in the immediately p` -- after_not_correct -- 他 is appropriate for the close re-reference, but 从五岁一直 still needs 开始 as the teacher marked.
- mengmu_samples#10 scene 3 [Coherence: temporality] `Coherence (Temporality): 一直学哲学：一直在学习哲学，Use 一直在 + verb for an action presented as continuously ongoing over a period of t` -- incorrect -- 一直学哲学 is not itself wrong; the actual problem is 从五岁缺少开始, which this change does not fix.
- mengmu_samples#32 scene 1 [Coherence: reference] `Coherence (Reference): 他妈妈：孟子的妈妈，This is the mother’s first mention, so use a full noun phrase to introduce her clearly ` -- false_positive -- “他妈妈” clearly introduces the mother through the immediately preceding mention of 孟子, so changing it to “孟子的妈妈” is unnecessary.
- mengmu_samples#32 scene 2 [Grammar & Vocabulary] `住才一月：才住一个月，才 should come before the verb, and a duration is normally expressed with a measure word as in 一个⽉.` -- incorrect, after_not_correct -- The duration needs a measure word and 才 must precede 住, but the proposed correction still lacks the required completed-action 了.
- mengmu_samples#32 scene 2 [Grammar & Vocabulary] `害得妈妈着急得很：让妈妈很着急，害得 requires a clearly harmful consequence; being anxious is an emotional reaction, so 让 is the appropria` -- false_positive -- 害得妈妈着急得很 is a valid 害得 construction and anxiety can be the harmful result.
- mengmu_samples#32 scene 2 [Coherence: connectors] `Coherence (Conjunction): 一般人不喜欢卖东西的人。但是孟子老是跟这些卖东西的人常常玩儿：一般人不喜欢卖东西的人，但是孟子老是跟这些卖东西的人常常玩儿，use 但是 to mark the contrast betwe` -- incorrect, after_not_correct -- 但是 can correctly begin the second sentence, and the proposed version still retains the redundant combination 老是 and 常常.
- mengmu_samples#45 scene 1 [Grammar & Vocabulary] `老是祭拜：常常祭拜，老是 has a negative or complaining tone, while this sentence describes a neutral repeated activity.` -- false_positive -- “老是” can carry a negative tone, but it is still acceptable here and the teacher did not mark it.
- mengmu_samples#45 scene 1 [Grammar & Vocabulary] `有才两个学校：才有两个学校，才 should come before the verb to mean “there are only two schools.”` -- incorrect, after_not_correct -- The teacher requires “只有两个学校,” not “才有两个学校,” for this meaning.
- mengmu_samples#45 scene 1 [Coherence: reference] `Coherence (Reference): 但是城市才有两个学校：但是那里才有两个学校，follow the close re-occurrence rule: after mentioning his city, use a prono` -- after_not_correct -- “那里” correctly avoids repeating the nearby place reference, but the corrected clause still uses disallowed “才有” instead of “只有”.
- mengmu_samples#45 scene 2 [Coherence: connectors] `Coherence (Conjunction): 他们从早到晚走路，孟子一直抱怨：他们从早到晚走路，所以孟子一直抱怨，add 所以 to show the cause-and-effect relation: the long walk c` -- after_not_correct -- Adding 所以 correctly marks the causal link, but the correction leaves 他们, which the teacher requires deleting so that 孟子 is the walker and complainer.
- mengmu_samples#45 scene 3 [Grammar & Vocabulary] `跟老师孟子学最重要的文学：孟子跟老师学最重要的文学，place the subject before the 跟老师 phrase.` -- after_not_correct -- 系统正确调整了主语位置，但保留的“学最重要的文学”不是老师所要求的自然表达，未改成“学习文学”。
- mengmu_samples#45 scene 3 [Coherence: reference] `Coherence (Reference): 他成为哲学家：孟子后来成为了哲学家，repeat the name after another character, 老师, has appeared, because the pronoun ` -- false_positive -- 孟子刚刚是上一句的主语，老师只是跟短语中的对象，代词他不会自然地指向老师。
- shennong_samples#8 scene 1 [Grammar & Vocabulary] `一看很多人：一看到很多人，“看” means to look, while “看到” means to see or notice something; the sentence describes what 神农 noticed.` -- after_not_correct, partial -- 看到 correctly replaces 看 here, but the full sentence still needs 就 in the 一……就…… structure.
- shennong_samples#8 scene 3 [Grammar & Vocabulary] `这就要看你想不想生病了：什么植物能吃，这就要看这种植物有没有毒了，this pattern must answer an uncertain condition and use an open or A-not-A question aft` -- false_positive -- “这就要看你想不想生病了”是合语法的警告性回答，不需要改成判断植物有没有毒。
- shennong_samples#8 scene 3 [Grammar & Vocabulary] `以后，神农告诉别人一些植物能吃，一些植物不能吃：后来，神农告诉别人一些植物能吃，一些植物不能吃，when a new sentence means “afterwards,” use 后来 rather than 以后.` -- after_not_correct -- 句首表示后续情节应使用“后来”，但改后仍有“别人”和“一些植物”应改为“人们”和“哪些植物”的问题。
- shennong_samples#8 scene 3 [Coherence: temporality] `Coherence (Temporality): 后来，神农告诉别人一些植物能吃，一些植物不能吃：后来，神农告诉了别人一些植物能吃，一些植物不能吃，use 了 for the completed action of telling peop` -- after_not_correct -- 这里叙述后来完成的“告诉”事件，加“了”可以正确标示完成，但改句仍保留“别人”和“一些植物”的错误。
- shennong_samples#19 scene 1 [Coherence: reference] `Coherence (Reference): 一个男人觉得植物很有意思。他叫神农：有一位叫神农的男人觉得植物很有意思，follow the first-mention rule: introduce a new character with` -- false_positive -- 先说一个男人、下一句再说明他叫神农，指称清楚且符合首次出现后命名的表达。
- shennong_samples#19 scene 2 [Grammar & Vocabulary] `找到黄色的花：找到了一朵黄色的花，This is a completed discovery, so use 了; a single flower also needs the measure word 朵.` -- incorrect, after_not_correct -- “一朵黄色的花”虽通顺，但仍没有解决老师指出的“黄色的花”过于笼统的问题，应说“一种黄色的花”。
- shennong_samples#19 scene 3 [Grammar & Vocabulary] `灵芝药的夹竹桃：灵芝和夹竹桃，The original phrase does not form a valid noun phrase: 的 must connect a modifier to a noun, but 灵芝药 canno` -- incorrect -- 灵芝药的夹竹桃 is an invalid and unintended noun phrase, while 灵芝和夹竹桃 changes the meaning to eating both plants rather than identifying lingzhi as an antidote.
- shennong_samples#19 scene 3 [Grammar & Vocabulary] `写一个课文的植物：写下这些植物，Use 写下 when recording plants or information. 课文 cannot be used as a modifier before 植物 here.` -- incorrect -- 课文的植物 is wrong here, but 写下这些植物 changes the intended meaning instead of correcting it to writing an article about plants.
- shennong_samples#33 scene 1 [Grammar & Vocabulary] `试一试很多种植物：尝一尝很多种植物，尝 is the appropriate verb for tasting or eating plants; 试一试 usually means trying out or testing someth` -- false_positive -- “试一试很多种植物”可以表示试验这些植物，并非用词错误；“尝一尝”只是另一种可行说法。
- shennong_samples#33 scene 1 [Coherence: connectors] `Coherence (Conjunction): 但是不知道为什么，没有办法：人们不知道为什么，也没有办法，but does not express contrast here; 也 links two related problems.` -- false_positive -- 这里“但是”可以表达“人们常因吃植物而死”与“却不知道原因”的转折，并非错误。
- shennong_samples#33 scene 2 [Grammar & Vocabulary] `让肚子感觉又暖和又清楚：让肚子感觉又暖和又舒服，清楚 does not describe a physical feeling in the stomach; 舒服 correctly describes a pleasant bodily` -- after_not_correct -- 清楚不能形容肚子的身体感受，改成舒服是对的，但教师还要求删掉感觉。
- shennong_samples#33 scene 3 [Coherence: reference] `Coherence (Reference): 这个口味：一种味道，This is a first mention in the current scene, so the demonstrative needs an established` -- incorrect -- 原来的整句与上下文没有清楚关系，单把“这个口味”改为“一种味道”不能解决这个问题。
- shennong_samples#33 scene 3 [Coherence: temporality] `Coherence (Temporality): 他发现：他发现了，Use 了 for the completed action of discovering something.` -- incorrect, after_not_correct, partial -- “发现”是心理动词，可以不用“了”，而且“他发现了”本身缺少宾语。
- shennong_samples#33 scene 3 [Coherence: connectors] `Coherence (Conjunction): 但是：虽然他生病了，但是他，Contrast needs the paired pattern 虽然……但是…… when the character tells people despit` -- incorrect, after_not_correct, partial -- 这里需要表达“即使生病也告诉”的让步关系，但“虽然他生病了，但是他”本身不完整，且不能直接修好原句。

### v1-S6

- mengmu_samples#10 scene 1 [Grammar & Vocabulary] `跟妈妈：妈妈带着他，When a mother moves home together with her child, use 带着 to show that the mother takes the child with her; 跟孟子` -- false_positive -- 跟妈妈搬家 is an acceptable way to say that Mengzi moved together with his mother.
- mengmu_samples#10 scene 2 [Coherence: temporality] `Coherence (Temporality): 孟子和孟母搬到子思老师的家：孟子和孟母搬到了子思老师的家，Use 了 for the completed moving action in this past narrative.` -- false_positive -- 这里后面还有“跟子思老师住”的动作，按动作序列规则不必在前一个“搬到”上加“了”。
- mengmu_samples#10 scene 2 [Coherence: connectors] `Coherence (Conjunction): 因为孟子现在没有朋友，：因为孟子现在没有朋友，所以，Use 因为……所以…… to mark the cause-and-effect relation between having no ` -- incorrect, after_not_correct, partial -- 原句的因果关系说反了：孟子没有朋友是因为他老是读书，而不只是缺少“所以”。
- mengmu_samples#10 scene 3 [Coherence: reference] `Coherence (Reference): 孟子从五岁一直学哲学：他从五岁一直学哲学，Use a pronoun for a close re-occurrence when the same character was named in` -- after_not_correct -- Close re-occurrence should use 他, but the corrected clause still has the teacher-marked temporal problem of 从五岁一直学哲学.
- mengmu_samples#32 scene 2 [Grammar & Vocabulary] `害得妈妈着急得很：让妈妈很着急，害得 requires a clearly harmful consequence, while being worried is better expressed with 让.` -- false_positive -- “害得妈妈着急得很”可以表示这件事造成妈妈焦急，是正确的害得结构。
- mengmu_samples#32 scene 3 [Grammar & Vocabulary] `成为有名的哲学家：成为了有名的哲学家，Becoming a philosopher is presented as a completed change of state, so it needs 了.` -- false_positive, miscategorized -- 成为有名的哲学家 is not itself erroneous; the problem is the placement and use of 难怪 in the larger clause, not a missing 了.
- mengmu_samples#45 scene 1 [Grammar & Vocabulary] `城市有才两个学校：城市才有两所学校，restrictive 才 must come before the verb 有, and 所 is the usual measure word for schools.` -- incorrect, after_not_correct -- 这里应说“这个城市只有两个学校”；“才有”改变了原本的限制意义，且没有补出“这个城市”。
- mengmu_samples#45 scene 2 [Coherence: temporality] `Coherence (Temporality): 他们搬家到有很多学校的城市：他们搬家到了有很多学校的城市，Use 了 for the completed move in this past narrative.` -- incorrect, after_not_correct -- The completed move needs perfective marking, but 搬家到了 is not a good correction here; use 搬到了有很多学校的城市 (or 搬了家到……).
- mengmu_samples#45 scene 3 [Grammar & Vocabulary] `想他的朋友：想念朋友，想 followed directly by a person usually means “think about”; 想念 expresses missing someone.` -- false_positive -- The teacher explicitly accepts 想他的朋友 here, so replacing it with 想念 is only an optional wording change.
- mengmu_samples#45 scene 3 [Grammar & Vocabulary] `找到孟子一个老师：给孟子找一个老师，when someone finds or seeks something for a recipient, place 给 + recipient before the verb.` -- after_not_correct -- 给孟子 correctly places the recipient before the verb, but 给孟子找一个老师 still lacks the completed-event marking needed in this past narration.
- shennong_samples#8 scene 1 [Coherence: reference] `Coherence (Reference): 有一个人叫神农：有一个叫神农的男人，For a first mention, introduce the character with a full noun phrase that gives` -- false_positive -- 有一个人叫神农 is already a clear and grammatical first introduction; adding 男人 is optional, not required.
- shennong_samples#8 scene 1 [Coherence: connectors] `Coherence (Conjunction): 神农想帮别人。所以想知道哪些植物能吃，哪些植物不能吃：神农想帮别人，所以想知道哪些植物能吃，哪些植物不能吃，Use “所以” to join the cause and result in ` -- incorrect, after_not_correct, miscategorized -- The actual error is 别人, which should be 他们 here; the proposed change leaves that error unchanged.
- shennong_samples#8 scene 2 [Coherence: temporality] `Coherence (Temporality): 神农开始尝很多植物，比方说他吃过生姜、芥兰和菠菜：神农开始尝很多植物，比方说吃了生姜、芥兰和菠菜，Use 了 for the completed examples of tasting; 吃` -- false_positive -- “吃过” can correctly state that Shennong had tried these plants, so replacing it with “吃了” is only a stylistic change.
- shennong_samples#8 scene 3 [Grammar & Vocabulary] `这就要看你想不想生病了：这就要看是哪种植物了，this pattern must state the uncertain condition that answers the question. Here, which plants are` -- false_positive -- “这就要看你想不想生病了”语法上成立，虽然意思不如谈植物种类那么直接。
- shennong_samples#8 scene 3 [Coherence: temporality] `Coherence (Temporality): 神农告诉人们一些植物能吃：神农告诉了人们一些植物能吃，告诉 is a completed narrative action here, so it needs 了 to mark compl` -- after_not_correct -- 这是已完成的叙事动作，需要“告诉了”，但改后仍保留“一些植物能吃”这一处教师标出的表达问题。
- shennong_samples#19 scene 2 [Coherence: reference] `Coherence (Reference): 黄色的花：一些黄色的花，This is the first mention of these flowers, so introduce them as an indefinite group ` -- incorrect, after_not_correct -- 一些 only makes the flowers indefinite; it does not solve the teacher's problem that 黄色的花 is too vague and should be introduced as 一种黄色的花.
- shennong_samples#19 scene 2 [Coherence: temporality] `Coherence (Temporality): 找到黄色的花：找到了一些黄色的花，Use 了 after 找到 because this is a completed discovery in the story.` -- after_not_correct -- Adding 了 correctly marks the completed discovery, but 一些黄色的花 still leaves the vague first introduction uncorrected.
- shennong_samples#19 scene 2 [Coherence: connectors] `Coherence (Conjunction): 头疼得要死，这杯冰茶是药：头疼得要死的时候，这杯冰茶是药，Use 的时候 to connect the headache condition with the tea’s use.` -- false_positive, after_not_correct -- The teacher did not require 的时候 here, and 这杯冰茶 still does not match the intended general kind of tea, which should be 这种冰茶.
- shennong_samples#19 scene 3 [Grammar & Vocabulary] `灵芝药的夹竹桃：灵芝和夹竹桃，“的” makes one noun modify another and cannot join two separate plants; use “和” to coordinate the two noun` -- incorrect, after_not_correct -- The intended meaning is that he ate lingzhi which can be used as an antidote to oleander, not that he ate two coordinated plants.
- shennong_samples#33 scene 1 [Grammar & Vocabulary] `告诉人：告诉人们，Use 人们 rather than the generic noun 人 when referring to the people whom 神农 tells.` -- false_positive -- 这里的告诉人可泛指告诉世人，原文并非一定错误，改成人们只是可选改写。
- shennong_samples#33 scene 1 [Coherence: reference] `Coherence (Reference): 他们能吃什么植物：什么植物能吃，Use zero form for the same referent within one sentence: after 人们 has been named,` -- false_positive -- 他们承接前面的人的指代清楚，教师也没有要求删去；改写还改变了原句的表达结构。
- shennong_samples#33 scene 2 [Grammar & Vocabulary] `让肚子感觉又暖和又清楚：让肚子感觉又暖和又舒服，清楚 describes clear thoughts, vision, or explanation, not a physical feeling in the stomach; 舒服 d` -- incorrect, after_not_correct -- 清楚不适合形容肚子的感觉，而且“让肚子感觉又暖和又舒服”仍应删去“感觉”。
- shennong_samples#33 scene 3 [Coherence: reference] `Coherence (Reference): 这个口味：一种花，"这个" needs a clear earlier referent, but no specific taste has been introduced; introduc` -- incorrect -- The teacher deleted the whole irrelevant and unclear “他发现这个口味” clause; replacing the noun phrase with “一种花” does not repair that problem.

### v2-S0

- mengmu_samples#10 scene 1 [Grammar] `而是因为妈妈认为他们… → 而是妈妈认为他们… -- It would be more natural to say 而是妈妈认为…… because 而是 already introduces the contrasting reason` -- false_positive, after_not_correct, partial, miscategorized -- “而是因为妈妈认为……”在“不是因为……而是因为……”结构中是正确的，且所示文字在“他们”处被截断。
- mengmu_samples#10 scene 2 [Grammar] `…子思老师的家，跟子思老师住 → …子思老师的家住 -- It would be more natural to delete 跟子思老师 because 搬到子思老师的家 already shows where they will liv` -- false_positive, partial -- 跟子思老师住 is grammatical and usefully expresses living with him, so deleting it is only an optional stylistic change.
- mengmu_samples#10 scene 2 [Coherence: reference] `孟子和⟦孟母⟧搬到子思老师… -- 孟母 appears for the first time, so please introduce her briefly, for example 孟子的妈妈孟母.` -- false_positive, partial -- 孟母 is already clearly identifiable from 妈妈 in the preceding sentence and is a conventional way to refer to Mencius's mother.
- mengmu_samples#10 scene 2 [Coherence: connectors] `他老是读书 → 所以他老是读书 -- It would be more natural to add 所以 to show that having no friends is the reason for reading books oft` -- incorrect, after_not_correct -- The teacher’s correction reverses the causal relation—he has no friends because he always studies—so merely adding 所以 preserves the relation she marked as wrong.
- mengmu_samples#10 scene 3 [Grammar] `难怪他成为很有名的哲学… → 难怪他成为了很有名的哲学… -- Becoming a famous philosopher is a completed event, so use 了 after 成为.` -- after_not_correct, partial, miscategorized -- 成为 a completed change in this narrative should take 了, but the displayed corrected text is cut off.
- mengmu_samples#10 scene 3 [Vocabulary] `就是看哲学书 → 就是看到哲学书 -- The person actually sees the philosophy books, so use 看到see, not 看look.` -- false_positive, after_not_correct -- 看哲学书 is correct for regularly reading philosophy books; 看到 means catching sight of or managing to see them and does not fit here.
- mengmu_samples#10 scene 3 [Coherence: reference] `难怪他成为很有名的… → 难怪成为很有名的… -- 孟子 is already clear from the previous sentence, so 他 is redundant. Chinese uses zero form here` -- false_positive, after_not_correct, partial -- 孟子 was named in the immediately preceding sentence, so 他 is the appropriate close reference in this new sentence, not redundant.
- mengmu_samples#32 scene 1 [Vocabulary] `所以她会一直搬家才能… → 所以她要一直搬家才能… -- 会 does not naturally form the conditional pattern with 才能 here; use 要...才能 instead.` -- after_not_correct, partial, miscategorized -- 这里“要……才能……”比“会……才能……”合适，但所示文本被截断，无法构成完整正确句。
- mengmu_samples#32 scene 1 [Coherence: reference] `所以她会一直搬家才… → 所以会一直搬家才… -- 她 is already clear from the previous clause, so delete it; Chinese uses zero form here.` -- incorrect, after_not_correct, partial -- 前文刚提到“她”，这里继续用“她”清楚且可接受，并非必须省略。
- mengmu_samples#32 scene 1 [Coherence: 了 / 着 / 在] `所以她决定了他们会搬家找… → 所以她决定他们会搬家找… -- 决定 is a mental-state verb here, so use no 了.` -- after_not_correct, partial -- “决定”是心理动词，此处不应加“了”，但改后仍保留“他们会搬家找……”等未改问题。
- mengmu_samples#32 scene 1 [Coherence: connectors] `有一天孟子去了墓地玩儿 → 有一天孟子去墓地玩儿 -- It would be more natural to delete 了 and use a sequence phrase such as 后来 to show how this s` -- incorrect, after_not_correct, miscategorized -- 叙述“有一天”发生并完成的事件时，“去了”正确，不应删除“了”。
- mengmu_samples#32 scene 1 [Other] `…搬家找更好的地方 → …搬家找更好的 -- It would be more natural to delete 地方 because 更好的 already expresses the thing she wants to find.` -- incorrect, partial, miscategorized -- “找更好的地方”本身正确，“地方”并不需要删除。
- mengmu_samples#32 scene 2 [Grammar] `…一月就又搬家 → …一月就又搬家了 -- Add sentence-final 了 because the move was completed: 又搬家了.` -- incorrect, after_not_correct, partial -- The excerpt is cut off, and adding only sentence-final 了 leaves the required 才住了一个月 word order and duration expression unfixed.
- mengmu_samples#32 scene 2 [Vocabulary] `他们住才一月就又搬家 → 他们才住一月就又搬家 -- use 才住 because 才 goes before the verb to show the short duration “only lived for one month.”` -- incorrect, after_not_correct, miscategorized -- 才 should precede 住, but the correction still needs 住了一个月 and does not provide a fully correct completed-event sentence.
- mengmu_samples#32 scene 2 [Vocabulary] `因为她恐怕儿子会成为跟… → 因为她担心儿子会成为跟… -- It would be more natural to say 担心 here, because it directly expresses that the mother wo` -- after_not_correct, partial -- 担心 correctly replaces 恐怕 before a stated subject, but the displayed clause is cut off and still contains the unresolved 成为跟… structure.
- mengmu_samples#32 scene 2 [Vocabulary] `…她恐怕儿子会成为跟他们很像 → …她恐怕儿子会变得跟他们很像 -- use 变得 before the adjective phrase 很像. 成为 is used for becoming a person, role, or thi` -- after_not_correct, partial -- 变得 correctly replaces 成为 before the adjective-like phrase 跟他们很像, but 恐怕儿子 remains incorrect.
- mengmu_samples#32 scene 2 [Coherence: 了 / 着 / 在] `她告诉了孟子：他们不… → 她告诉孟子：他们不… -- 告诉 introduces quoted speech, so use no 了 for the speaking word: 她告诉孟子：……` -- after_not_correct, partial -- Quoted-speech 告诉 takes no 了 here, but the shown corrected text is cut off.
- mengmu_samples#32 scene 2 [Other] `但是孟子老是跟这些卖东西… → 但是孟子跟这些卖东西… -- 老是 is redundant because 常常 already expresses that Mengzi played with them often.` -- after_not_correct, partial, miscategorized -- 老是 and 常常 are redundant together, so deleting 老是 is a valid fix, but the displayed text is incomplete.
- mengmu_samples#32 scene 3 [Vocabulary] `而是当哲学家 → 而要当哲学家 -- Use the matching contrast 不要……而要…… here. It is more natural than pairing 不要 with 而是.` -- incorrect, miscategorized -- The contrast needs the intended 不是要……而是要…… structure; changing only 而是 to 而要 does not properly repair it.
- mengmu_samples#32 scene 3 [Vocabulary] `而是当哲学家 → 而是当哲学家的 -- It would be more natural to add 的 here to make the description sound more complete.` -- incorrect, after_not_correct -- 当哲学家 is already a complete predicate, while 当哲学家的 incorrectly leaves 的 without a following noun.
- mengmu_samples#32 scene 3 [Vocabulary] `…他们第三个家 → …他们第三个家里 -- A modified location with 家 normally uses 里. Say 在他们第三个家里.` -- incorrect, after_not_correct, partial, miscategorized -- 在他们第三个家 is missing the required possessive 的, and adding 里 does not fix that error.
- mengmu_samples#32 scene 3 [Vocabulary] `他难怪成为有名的哲… → 难怪他成为有名的哲… -- Put 难怪 before the subject it explains. Say 难怪他成为有名的哲学家.` -- incorrect, after_not_correct, partial, miscategorized -- 难怪 should precede the subject here, but the correction still omits 后来 required for the later result.
- mengmu_samples#32 scene 3 [Coherence: 了 / 着 / 在] `孟子学了怎么祭拜 → 孟子学会了怎么祭拜 -- It would be more natural to say 学会了怎么祭拜. 学会 shows that Mencius learned this skill successfully.` -- incorrect, after_not_correct, miscategorized -- The problem is the incorrect information 怎么祭拜, which 学会了 does not correct.
- mengmu_samples#32 scene 3 [Coherence: 了 / 着 / 在] `告诉了孟子：我们找… → 告诉孟子：我们找… -- 告诉 introduces quoted speech, so use no 了 after it.` -- after_not_correct, partial -- 告知 followed by quoted speech takes zero aspect marking here, so removing 了 is correct, but the displayed quotation is cut off.
- mengmu_samples#32 scene 3 [Coherence: connectors] `你不是当数学家 → 你不要当数学家 -- For advice or prohibition, use 不要, not 不是. 不是……而是…… is used to correct a mistaken idea, not to give` -- incorrect, after_not_correct -- The intended correction is 不是要当商人，而是要当哲学家, not a prohibition against being a mathematician.
- mengmu_samples#32 scene 3 [Coherence: connectors] `…以他们又搬家 → …以他们又搬家了 -- It would be more natural to add 了 because this move was completed. 又 shows that they moved again.` -- after_not_correct, partial, miscategorized -- Adding sentence-final 了 correctly marks the completed additional move, but the displayed text is cut off.
- mengmu_samples#45 scene 1 [Vocabulary] `但是城市有才两个学校 → 但是城市只有才两个学校 -- It would be more natural to use 只 to mean “only” for the small number of schools.` -- incorrect, after_not_correct -- 只有 should replace 有才, but 只有才两个学校 is still incorrect and 城市 should be 这个城市.
- mengmu_samples#45 scene 1 [Vocabulary] `但是城市有才两个学校 → 但是城市有两个学校 -- It would be more natural to delete 才 here; 只 already expresses “only.”` -- incorrect, after_not_correct -- Deleting 才 loses the intended meaning of “only” and still leaves the reference problem with 城市.
- mengmu_samples#45 scene 1 [Coherence: reference] `一个男孩子跟⟦他⟧的妈妈住在中… -- This character appears for the first time, so please introduce the boy briefly with a noun phrase be` -- false_positive, partial -- 一个男孩子 already introduces the boy, and 他的妈妈 is natural within that same noun phrase.
- mengmu_samples#45 scene 2 [Vocabulary] `而是想孟子有很好的… → 而是想让孟子有很好的… -- 想 cannot be followed directly by a new subject and verb. Use 想让孟子… to show what the mother w` -- after_not_correct, partial, miscategorized -- 想不能直接接“孟子有……”这样的主谓结构，需用让来引出该结构。
- mengmu_samples#45 scene 2 [Vocabulary] `而是想孟子有很好的教育 → 而是想孟子接受很好的教育 -- 接受 normally collocates with 教育. Say 让孟子接受很好的教育.` -- incorrect, after_not_correct -- 接受教育搭配可以，但“想孟子接受……”仍缺少让，想不能直接接新主语。
- mengmu_samples#45 scene 2 [Coherence: 了 / 着 / 在] `他们搬家到有很多学校… → 他们搬到有很多学校… -- It would be more natural to say 搬到…, not 搬家到…. Here 搬 already means “move house.”` -- false_positive, after_not_correct, partial, miscategorized -- “搬家到一个城市”本身可以说，改成“搬到”只是可接受但非必要的改写。
- mengmu_samples#45 scene 2 [Coherence: 了 / 着 / 在] `他们搬家到有很多学校的… → 他们搬家到了有很多学校的… -- It would be more natural to add 了completed because moving to the city is a completed act` -- after_not_correct, partial -- 这里叙述的是已经完成的搬家事件，加了可标示完成；“搬家到了……”可以成立。
- mengmu_samples#45 scene 3 [Grammar] `…妈妈找到孟子一个老师 → …妈妈找到孟子的老师 -- It would be more natural to use 的 because 孟子 describes the noun 老师: 孟子的老师.` -- incorrect, partial -- 找到孟子一个老师 needs 给孟子, while 孟子的老师 changes the intended meaning.
- mengmu_samples#45 scene 3 [Vocabulary] `跟老师孟子学最重要的文… → 孟子跟老师学最重要的文… -- Put the subject 孟子 before 跟老师. Say 孟子跟老师学最重要的文学.` -- after_not_correct, partial, miscategorized -- 孟子 must be placed before 跟老师, but 最重要的文学 remains an unsuitable expression here.
- mengmu_samples#45 scene 3 [Coherence: reference] `他想他的朋友 → 想他的朋友 -- 他 is already clear from the close continuation, so delete it; Chinese uses zero form here.` -- incorrect -- The pronoun 他 is acceptable and is retained in the teacher's correction.
- mengmu_samples#45 scene 3 [Coherence: reference] `因为他不要离开他的… → 因为不要离开他的… -- 他 is already clear from the previous clause, so it is redundant. Chinese uses zero form here.` -- incorrect, after_not_correct, partial -- The problem is 不要 rather than 他, and deleting 他 leaves the wrong wording unchanged.
- mengmu_samples#45 scene 3 [Other] `他的妈妈找到孟子一个老师 → 他的妈妈找到给孟子找了一个老师孟子一个老师 -- Use 给 to mark 孟子 as the person receiving the teacher. Say 给孟子找了一个老师.` -- incorrect, after_not_correct, miscategorized -- 给孟子找到一个老师 is needed, but the proposed correction is ungrammatical and repeats material.
- shennong_samples#8 scene 1 [Grammar] `哪些植物不能吃 → 哪些不能吃 -- It would be more natural to omit the repeated 植物: 哪些植物能吃，哪些不能吃。` -- false_positive, miscategorized -- Repeating 植物 here is acceptable and does not need to be omitted.
- shennong_samples#8 scene 1 [Vocabulary] `一看很多人正在吃… → 一看到很多人正在吃… -- Shennong actually sees the people eating plants, so use 看到see, not 看look.` -- incorrect, after_not_correct, partial -- 看到 correctly improves 看, but the required 一……就 connector structure is still missing.
- shennong_samples#8 scene 1 [Coherence: 了 / 着 / 在] `神农想帮别人 → 神农想帮助别人 -- It would be more natural to say 帮助别人 here.` -- incorrect, after_not_correct, miscategorized -- 别人 incorrectly refers to the concrete people already mentioned; 帮助 does not fix this, and 帮他们 is needed.
- shennong_samples#8 scene 2 [Vocabulary] `一些植物毒得很 → 一些植物有毒得很 -- It would be more natural to say 有毒. Here you need the adjective form 有毒 to describe the plants.` -- incorrect, after_not_correct -- 毒不能和得很搭配；有毒得很仍然保留不合适的得很结构。
- shennong_samples#8 scene 3 [Vocabulary] `这就要看你想不想生病… → 这就要看你想不想生病… -- Here 看 means “depends on” in 要看……, so do not change it to 看到.` -- false_positive, after_not_correct, partial -- 要看你想不想生病了 is already correct, and the displayed text is cut off.
- shennong_samples#8 scene 3 [Other] `麻烦我们可以吃什… → 请问我们可以吃什… -- Use 请问 to politely introduce a question. 麻烦 cannot directly introduce this question.` -- after_not_correct, partial, miscategorized -- 麻烦 cannot directly introduce this question in the intended way; 请问 is a correct replacement, but the displayed correction is cut off.
- shennong_samples#19 scene 1 [Grammar] `他找很多植物 → 他找了很多植物 -- This is a completed past action, so add 了 after 找: 找了很多植物。` -- incorrect, after_not_correct, miscategorized -- The issue is that 找 means “look for”; the intended meaning requires 找到, and adding 了 does not fix this.
- shennong_samples#19 scene 1 [Vocabulary] `可是有的吃了以后很舒服 → 可是有的吃了之后很舒服 -- It would be more natural to say 之后 here for the time after eating: 吃了之后。` -- false_positive -- “吃了以后” is already correct; “吃了之后” is only an acceptable alternative.
- shennong_samples#19 scene 1 [Coherence: reference] `⟦他⟧叫神农 -- This character appears for the first time, so please introduce 神农 briefly with an identifying noun phrase, not` -- false_positive -- “他” correctly refers to the immediately preceding “一个男人,” and “他叫神农” naturally introduces his name.
- shennong_samples#19 scene 2 [Grammar] `…跟黄色的花做茶很有用 → …跟黄色的花做的茶很有用 -- It would be more natural to say 用黄色的花做的茶, using 的 to link 做 to 茶.` -- incorrect, after_not_correct, partial, miscategorized -- 表示材料应说“用黄色的花”，不能保留“跟黄色的花”。
- shennong_samples#19 scene 2 [Grammar] `你的头发疼死 → 你的头发疼死了 -- Use 了 for this change of state: 头疼死了.` -- incorrect, after_not_correct, miscategorized -- “头发疼”不表示头痛，加“了”没有改正“头发”这个词的错误。
- shennong_samples#19 scene 2 [Grammar] `他一喝茶就很不舒服 → 他一喝茶就觉得很不舒服 -- It would be more natural to say 他一喝茶就觉得很不舒服.` -- false_positive -- “他一喝茶就很不舒服”本来就语法正确，“觉得”只是可选的表达。
- shennong_samples#19 scene 2 [Vocabulary] `他听说你跟黄色的花做茶… → 他听说用黄色的花做茶… -- Use 用 to show the material used to make tea: 用黄色的花做茶.` -- after_not_correct, partial -- 这里应删除无所指的“你”，并用“用”表示做茶的材料。
- shennong_samples#19 scene 2 [Vocabulary] `你的头发疼死 → 你的头疼死 -- 头发 means “hair,” but a headache is 头疼. Delete 发.` -- incorrect, after_not_correct -- 虽然删掉“发”改成了头痛，但“你的头疼死”仍不完整自然，且保留了不必要的泛指“你”。
- shennong_samples#19 scene 2 [Vocabulary] `这冰茶是药 → 这杯茶是药 -- Use 杯 as the measure word for a cup of tea: 这杯茶.` -- incorrect -- “这杯茶”本身正确，但把原来的“冰茶”改成了普通“茶”，没有按原意改成“这种冰茶”。
- shennong_samples#19 scene 3 [Grammar] `也写一个课文的植物 → 也写一个关于植物的书 -- 课文的植物 does not mean “a book about plants.” Use 关于植物的书 for a book whose topic is plants.` -- incorrect, after_not_correct, miscategorized -- 课文的植物 is not a valid way to express an article about plants, and 一个关于植物的书 also uses the wrong measure word for 书.
- shennong_samples#19 scene 3 [Vocabulary] `也写一个课文的植… → 也写了一个课文的植… -- Use 了 after 写 for this completed past action: 写了.` -- after_not_correct, partial, miscategorized -- The final action in this action sequence needs 了, but the displayed fragment is cut off and still retains the erroneous phrase 课文的植物.
- shennong_samples#19 scene 3 [Vocabulary] `也写一个课文的植物 → 也写一本课文的植物 -- Use 本 for a book. 个 does not normally collocate with 课文 here.` -- incorrect, after_not_correct -- 个 is not appropriate for a written article/book here, but 一本课文的植物 is still not a grammatical expression.
- shennong_samples#19 scene 3 [Coherence: reference] `…芝药的夹竹桃他吃完了 → …芝药的夹竹桃他把它吃完了 -- It would be more natural to say 他把它吃完了. 把它 clearly marks 灵芝 as the object that he finishe` -- incorrect, after_not_correct, partial, miscategorized -- The phrase is cut off and its real problem is the malformed expression 灵芝药的夹竹桃, which adding 把它 does not repair.
- shennong_samples#19 scene 3 [Coherence: connectors] `灵芝药的夹竹桃他吃完了 → 有灵芝他吃完了 -- 灵芝药的夹竹桃 does not say that lingzhi is present. Use 有灵芝 to introduce that there is lingzhi here.` -- incorrect, after_not_correct, miscategorized -- 灵芝药的夹竹桃 is malformed, and 有灵芝他吃完了 does not clearly or correctly express that he ate the lingzhi remedy.
- shennong_samples#33 scene 1 [Grammar] `…么植物是安全什么是危险 → …么植物是安全的什么是危险 -- 安全 describes 植物, so use 的: 安全的植物.` -- after_not_correct, partial -- “安全” here needs the structural particle 的, but the displayed correction still leaves the later “危险” without 的 (and lacks separation).
- shennong_samples#33 scene 1 [Grammar] `…全什么是危险 → …全什么是危险的 -- 危险 describes 植物, so use 的: 危险的植物.` -- after_not_correct, partial -- “危险” also needs 的 here, but the displayed correction still contains the earlier uncorrected “安全” without 的.
- shennong_samples#33 scene 1 [Vocabulary] `所以有一天 → 于是有一天 -- Use 于是 to introduce the resulting action naturally here, not 所以.` -- false_positive, miscategorized -- “所以有一天” is acceptable in this narrative context; “于是” is only an optional stylistic alternative.
- shennong_samples#33 scene 1 [Vocabulary] `神农出去试一试很多种植物 → 神农出去尝一尝很多种植物 -- 试一试 does not naturally collocate with plants in this situation. Use 尝一尝 to mean tasting p` -- incorrect -- “试一试很多种植物” can mean testing different plants and is acceptable here, although “尝一尝” is more specific.
- shennong_samples#33 scene 1 [Coherence: reference] `人不知道他们能吃什么植物 → 人不知道自己能吃什么植物 -- With generic 人, use 自己 to refer back to the same people, not 他们.` -- after_not_correct -- For the same generic people as the subject, “自己” is the appropriate reference, but the correction still leaves the concrete-group use of “人” instead of “人们”.
- shennong_samples#33 scene 2 [Vocabulary] `…感觉又暖和又清楚 → …感觉又暖和又舒服 -- 清楚 describes whether something is clear, not how the stomach feels. Use 舒服 for a warm, comforta` -- after_not_correct, partial -- 清楚 cannot describe the stomach's physical feeling, but the correction still leaves the teacher-marked unnecessary 感觉.
- shennong_samples#33 scene 2 [Vocabulary] `这就要看你的口味 → 这就要看你的口味 -- Here 看 means “depend on,” in the phrase 看你的口味. Do not change it to 看到, which means “see/catch sig` -- incorrect, after_not_correct, miscategorized -- This fixed structure requires sentence-final 了, so repeating the original text does not correct it.
- shennong_samples#33 scene 2 [Coherence: connectors] `可能喜欢糖 → ，这样可以吃糖喜欢糖 -- Use ，这样可以 to show how the example connects to the previous clause: if someone likes sweet food, th` -- false_positive, after_not_correct -- 可能喜欢糖 is already an acceptable continuation of the example, while the proposed replacement is ungrammatical.
- shennong_samples#33 scene 3 [Grammar] `一百岁时候 → 的一百岁时候 -- Use the established time expression 一百岁的时候, with 的 before 时候.` -- incorrect, after_not_correct -- 一百岁的时候 needs 的 before 时候, but 的一百岁时候 is not a grammatical time expression.
- shennong_samples#33 scene 3 [Grammar] `一吃就开始死 → 一吃就死了 -- Death is a completed event here, so use 死了 rather than 开始死.` -- incorrect -- 开始 cannot modify the instantaneous event 死, but 一吃就死了 changes the intended poisoning-and-feeling-unwell event into actual death.
- shennong_samples#33 scene 3 [Grammar] `但是生病时候告诉人什… → 但是生病的时候告诉人什… -- Use 的 before 时候 in this time phrase: 生病的时候.` -- incorrect, after_not_correct, partial -- 生病的时候 needs 的, but the correction leaves the incomplete contrast structure 但是…… and the shown text is cut off.
- shennong_samples#33 scene 3 [Vocabulary] `什么植物是毒 → 什么是毒 -- It would be more natural to say 什么是毒 after 什么植物是药; the omitted noun 植物 is already clear.` -- incorrect -- 什么植物是毒 incorrectly uses 毒 as the predicate meaning “poisonous”; 什么是毒 is grammatical but changes the intended meaning rather than fixing it.
