# New feedback system (round B1) -- for review

This round was built only from the basic materials: the graded student stories, the model stories, the
required-scene lists and the coherence rules. None of the comments on earlier AI feedback were used yet.
The corrections of these 20 stories were not available to the system.

Per scene: Grammar and Vocab Corrections; Coherence (each line labelled Reference, Temporality or
Conjunction); Expressiveness; New Words (suggestions for words that are correct); Encouragement. After the
story: Content & completeness. Each correction is one line -- the student's words：the corrected words，what
is wrong and why. The corrected words are a complete phrase with every error in it fixed. A correction is
shown only if at least two of three independent runs of the system made it.

Each correction can be judged in `B1_labels.csv` (see `B1_labels_instructions.md`).

## mengmu_samples#4

### Scene 1

> 古代的时候，孟子和孟母住了在靠墓地的家。孩子才五岁就每天在墓地祭拜了。在那个城市，孟母从早到晚都找工作，可是找不到，害得孟母没有钱。难怪她跟孩子搬家，原来买不了房。他们搬了到别一个城市找工作。

**Grammar and Vocab Corrections**
- 古代的时候：在古代，Use 在古代 to say “in ancient times.”
- 他们搬了到别一个城市找工作：他们搬到了另一个城市找工作，With the result complement 到, put 了 after 到: 搬到了. Say 另一个城市, not 别一个城市.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 孟子和孟母住了在靠墓地的家：有一个孩子叫孟子，跟妈妈住在靠近墓地的家里，When characters first appear, introduce who they are: Mengzi is a child and Meng Mu is his mother. Also, 住 is a state, so it does not take 了, and 在 comes before the place.
- **Reference** 害得孟母没有钱：害得没有钱，孟母 is already the subject earlier in the same sentence. Do not repeat the name in the same sentence when the subject is still the same.
- **Temporality** 孩子才五岁就每天在墓地祭拜了：孩子才五岁就每天在墓地祭拜，每天 shows a routine, so do not use 了 for the verb.

**Expressiveness**
- After “在那个城市，孟母从早到晚都找工作，可是找不到，害得孟母没有钱”: You could add Meng Mu’s worried feeling after she cannot find work. For example: 孟母很着急，不知道怎么办。
- After “难怪她跟孩子搬家，原来买不了房”: You could add a short thought to show why she decides that moving is necessary. For example: 她想：“我们得去别的地方。”

**New Words**
- No suggestions.

**Encouragement** You clearly set the story in ancient times and introduced Meng Zi and his mother. You also tried to show a cause-and-effect chain: Meng Mu cannot find work, has no money, and then moves with her child.

### Scene 2

> 这个城市老是很吵，不是人吵架，就是都叫，害得孟子一直不能睡觉。在那儿，孟母也找不到工作。孟子和妈妈要又一个次搬了家。在第三个城市，孟母找到工作，在商店做衣服。

**Grammar and Vocab Corrections**
- 孟子和妈妈要又一个次搬了家：孟子和妈妈又搬了一次家，要 is not used with a completed action marked by 了. Put 又 before the verb, and use 一次, not 一个次, to say “one more time.”

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 孟母找到工作：孟母找到了工作，Finding a job is a completed action here, so 找到 needs the completion marker 了.

**Expressiveness**
- After “在那儿，孟母也找不到工作”: You could add Mengmu’s worried thought about needing to find a quieter place for Mengzi. For example: 孟母想：这里太吵了，我们还是搬家吧。
- After “在第三个城市，孟母找到工作，在商店做衣服”: You could describe one simple detail of the clothes in the shop. For example: 商店里有很多漂亮的衣服。

**New Words**
- 叫 (“就是都叫”)：喊 (“就是都喊”)，“喊” more clearly describes people making loud noises or shouting.

**Encouragement** You clearly explain why this city is difficult for Mengzi: the noise stops him from sleeping. You also move the story forward by showing that Mengmu finds a job in the third city.

### Scene 3

> 孟子在那个商店也找了到工作，可是不是做衣服的工作，而是喜欢的工作。孟子学习馆学了十五年，他的学习和他的旅行经验很重要，对他很多好处。他是大人的时候，他成为很有名的哲人。

**Grammar and Vocab Corrections**
- 孟子在那个商店也找了到工作：孟子在那个商店也找到了工作，找到 is the verb meaning “to find.” Put 了 after 找到 to show that he successfully found a job.
- 孟子学习馆学了十五年：孟子在学校学习了十五年，A place phrase needs 在 before it, and 学校 is the usual word for a school. Use 学习 for the action of studying.
- 对他很多好处：对他有很多好处，Use 有 to say that something has benefits for someone. 对他有很多好处 means “it has many benefits for him.”
- 他是大人的时候：他长大以后，Use 长大以后 to mean “after growing up.” 是大人的时候 is not a natural way to express this in Chinese.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “孟子在那个商店也找了到工作，可是不是做衣服的工作，而是喜欢的工作”: You could add that he felt happy because he had found work he liked. For example: 他很高兴，因为他喜欢这个工作。
- After “他是大人的时候，他成为很有名的哲人”: You could add that his mother was proud of his success. For example: 孟母听了以后，觉得很骄傲。

**New Words**
- No suggestions.

**Encouragement** You clearly show Mengzi’s development over time: he works, studies for many years, travels, and later becomes a famous philosopher. You also connect his study and travel experience to his success, which gives this ending a clear reason.

### Content & completeness (after the whole story)

- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Need to add: 孟母 and 孟子 moving from the market to a neighborhood near a school is not told; the place is not identified as a school.
- Wrong information: “难怪她跟孩子搬家，原来买不了房。” -- This gives being unable to buy a house as the reason for the move, but 孟母 moves because she worries that copying sacrifices will affect 孟子 badly.

## mengmu_samples#10

### Scene 1

> 孟子小的时候，从早到晚都跟朋友玩。孟子和他的朋友喜欢玩在墓地里，装祭拜。孟子五岁的时候，跟妈妈搬家。他们搬家不是因为孟子玩得太多，而是因为妈妈认为他们的家离墓地太近。

**Grammar and Vocab Corrections**
- 孟子和他的朋友喜欢玩在墓地里，装祭拜：孟子和他的朋友喜欢在墓地里玩，假装祭拜，A place phrase with 在 comes before the verb, so say 在墓地里玩. 装 cannot directly mean pretending to do an action; use 假装祭拜.
- 孟子五岁的时候，跟妈妈搬家：孟子才五岁，就跟妈妈搬家了，To say that someone was only a certain age when something happened, use 才 before the age and 就 before the action. 搬家 is a completed action here, so it takes 了.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 孟子小的时候，从早到晚都跟朋友玩：有一个小男孩叫孟子，他小的时候，从早到晚都跟朋友玩，This is Mengzi's first appearance in the story, so introduce him with a noun phrase that says who he is, such as “有一个小男孩叫孟子.”

**Expressiveness**
- After “他们搬家不是因为孟子玩得太多，而是因为妈妈认为他们的家离墓地太近”: You could add the mother's worried thought to show why living near the cemetery concerned her. For example: 妈妈想：“孟子老是装祭拜，这样不太好。”

**New Words**
- 认为 (“妈妈认为他们的家离墓地太近”)：觉得 (“妈妈觉得他们的家离墓地太近”)，“觉得” is a more natural everyday word for a mother's personal opinion in this situation.

**Encouragement** You clearly explain the reason for the move, and your use of “不是……而是……” makes the contrast easy to understand. You also include Mengzi’s age, which helps place this scene in the story.

### Scene 2

> 妈妈认为，住离墓地太近，害得孟子的心气。孟子和孟母搬到子思老师的家，跟子思老师住。孟母帮子思打扫房间和做饭。子思帮孟母教她的儿子。因为孟子现在没有朋友，他老是读书。

**Grammar and Vocab Corrections**
- 妈妈认为，住离墓地太近，害得孟子的心气：妈妈认为住在离墓地太近的地方，会影响孟子的心情，住 needs 在 before the place phrase, so say 住在离墓地太近的地方. 害得孟子的心气 is not a natural expression; living near a cemetery can 影响 a person's 心情.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 孟子和孟母搬到子思老师的家，跟子思老师住：孟子和孟母搬到子思老师的家，跟子思老师住了，These are two completed actions in a series. In a series of completed actions, only the last verb takes 了.
- **Conjunction** 因为孟子现在没有朋友，他老是读书：因为孟子现在没有朋友，所以他老是读书，Because this sentence gives a cause and its result, use the paired conjunction 因为……所以…….

**Expressiveness**
- After “子思帮孟母教她的儿子”: You could add that Meng Mu feels relieved because someone is helping her son study. For example: 孟母觉得很放心。
- After “因为孟子现在没有朋友，他老是读书”: You could add Meng Zi’s feeling about having no friends before showing that he reads often. For example: 孟子觉得有一点儿孤单。

**New Words**
- No suggestions.

**Encouragement** You clearly explain how Meng Mu helps Zi Si and how Zi Si helps teach Meng Zi. You also use a clear cause-and-effect sentence to show why Meng Zi reads so often.

### Scene 3

> 子思认为，对孩子来说，读书最重要，特别是学哲学。孟子不是练习写文章，就是看哲学书。孟子从五岁一直学哲学。他才五岁就学哲学，难怪他成为很有名的哲学家。

**Grammar and Vocab Corrections**
- Nothing to flag.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 难怪他成为很有名的哲学家：难怪他成为了很有名的哲学家，Becoming a famous philosopher is a completed change in the story, so 成为 needs 了 here.

**Expressiveness**
- After “他才五岁就学哲学，难怪他成为很有名的哲学家”: You could add that his mother felt happy because she saw that he was learning seriously. For example: 孟母看到他认真读书，心里很高兴。

**New Words**
- 看 (“看哲学书”)：读 (“读哲学书”)，“读” is more specific than “看” when talking about reading books.

**Encouragement** You clearly show that Mencius studied philosophy from a very young age. The pattern “不是……就是……” also makes his daily study activities sound varied and active.

### Content & completeness (after the whole story)

- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Need to add: They move from the market to a neighborhood near a school.
- Wrong information: “孟子和孟母搬到子思老师的家，跟子思老师住。” -- The story has them move to a neighborhood near a school, not to 子思老师's home to live with him; 子思老师 is not part of the required story.
- Wrong information: “孟母帮子思打扫房间和做饭。” -- 子思 and this work for him are not part of the story.
- Wrong information: “子思帮孟母教她的儿子。” -- 子思 is not part of the story; 孟子 begins studying after the move near the school.

## mengmu_samples#12

### Scene 1

> 古代，孟子跟孟母住在墓地的旁边。可是孟母注意，住在墓地的旁边影响孟子。他常常跟朋友们祭拜玩，所以孟母决定他们会搬家。这次，他们住在城市里的商店的旁边，从早到晚很吵。

**Grammar and Vocab Corrections**
- 可是孟母注意，住在墓地的旁边影响孟子：孟母注意到住在墓地的旁边影响孟子，可是 needs a contrast, but there is no contrast here. Use 注意到 when someone notices or realizes something.
- 他常常跟朋友们祭拜玩：他常常跟朋友们玩祭拜的游戏，玩 comes before the activity or game being played. 祭拜 is the activity, so say 玩祭拜的游戏.
- 孟母决定他们会搬家：孟母决定搬家，After 决定, say directly what the person decides to do. Do not use 他们会 here.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 古代：在古代，Use 在 before a time phrase when saying that something happened in that period.

**Expressiveness**
- After “这次，他们住在城市里的商店的旁边”: You could add a visual detail about the busy shops and people buying things. For example: 街上有很多人买东西。
- After “从早到晚很吵”: You could show Meng Mu’s concern that this environment may affect Meng Zi’s learning. For example: 孟母觉得这儿会影响孟子学习。

**New Words**
- 吵 (“从早到晚很吵”)：热闹 (“从早到晚都很热闹”)，“热闹” describes a busy, lively place with many people and sounds, while “吵” focuses more on unpleasant noise.

**Encouragement** You clearly show the change from the cemetery to the city and connect Meng Mu’s decision to Meng Zi’s behaviour. The time phrase “从早到晚” also helps the reader imagine how constant the noise is.

### Scene 2

> 城市也有点儿危险。害得孟母只好一直陪孟子。孟子也没有朋友，难怪他老是看起来不高兴。住在商店的旁边不是适合孟子，而是让他觉得很伤心。

**Grammar and Vocab Corrections**
- Nothing to flag.

**Coherence: Reference / Temporality / Conjunction**
- **Conjunction** 住在商店的旁边不是适合孟子，而是让他觉得很伤心：住在商店的旁边不但不适合孟子，而且让他觉得很伤心，而是 presents a replacement or alternative, but being unsuitable and making him sad are both results. Use 不但……而且…… to add the second result.

**Expressiveness**
- After “害得孟母只好一直陪孟子”: Add Meng Mu’s worried thought that the noisy environment may make it hard for Meng Zi to study. For example: 孟母想：“这里太吵了，孟子没法儿好好学习。”
- After “孟子也没有朋友”: Add a small visual detail to show what Meng Zi does when he is alone. For example: 孟子常常一个人坐在家里，看着外面的商店。

**New Words**
- No suggestions.

**Encouragement** You clearly explain why Meng Mu is worried and connect Meng Zi having no friends with his unhappy feelings. Your use of “害得” also shows a good cause-and-effect link.

### Scene 3

> 所以，孟母和孟子搬到学校的旁边住。才五岁孟子开始学哲学。在学校，孟子不是看书，就是练习写字。将来，他成为中国的一个非常有名的哲学家。

**Grammar and Vocab Corrections**
- 才五岁孟子开始学哲学：孟子才五岁就开始学哲学了，Put the subject before the age phrase. 才五岁 is commonly followed by 就 to show that he started learning philosophy at such a young age.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 孟母和孟子搬到学校的旁边住：孟母和孟子搬到学校的旁边住了，This is a completed event in the story, so it needs 了. In a series of actions, put 了 on the last verb, 住.
- **Temporality** 将来，他成为中国的一个非常有名的哲学家：后来，他成为了中国一个非常有名的哲学家，This is a later completed event in a historical story, so use 后来 rather than 将来 and use 了 with 成为.

**Expressiveness**
- After “在学校，孟子不是看书，就是练习写字”: You could add Meng Mu’s happiness when she sees that Mengzi is studying seriously. For example: 孟母看到他认真学习，心里很高兴。
- After “将来，他成为中国的一个非常有名的哲学家”: You could add Meng Mu’s thought that moving next to the school was the right decision. For example: 孟母想：“这次搬家太对了！”

**New Words**
- No suggestions.

**Encouragement** You clearly show how Mengzi’s environment changes from the earlier scenes to studying at school. The pattern “不是……就是……” effectively shows that he spends his time reading and practising writing.

### Content & completeness (after the whole story)

- Need to add: 孟子 imitating buying and selling every day

## mengmu_samples#18

### Scene 1

> 古代的时候，有一个男孩名字叫孟子。孟子和孟子的妈妈两个人住在很穷的农村。他们住的地方旁边是个墓地，墓地老是有很多人祭拜。因为人们在祭拜，他们一直在哭。孟子和孟子的妈妈住在这里才一个星期就觉得受不了了，而且害得孟子的学习。

**Grammar and Vocab Corrections**
- 古代的时候：在古代，Use 在古代 to say “in ancient times.”
- 而且害得孟子的学习：而且影响了孟子的学习，害得 must be followed by a result clause, not a noun phrase such as 孟子的学习. Use 影响了孟子的学习 to say that it affected Mencius's studies.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 孟子和孟子的妈妈两个人住在很穷的农村：孟子和妈妈两个人住在很穷的农村，After 孟子 has been named in the same phrase, do not repeat his name before 妈妈. Say 孟子和妈妈.
- **Conjunction** 因为人们在祭拜，他们一直在哭：因为人们在祭拜，所以一直在哭，Use 因为 together with 所以 to show cause and result. Since 人们 is the subject in both parts of the same sentence, do not repeat it with 他们.

**Expressiveness**
- After “因为人们在祭拜，他们一直在哭”: Add Mengzi’s reaction to what he saw, such as finding the rituals interesting and wanting to copy them. For example: 孟子觉得祭拜很有趣，想学他们。
- After “孟子和孟子的妈妈住在这里才一个星期就觉得受不了了，而且害得孟子的学习”: Add Mengzi’s mother’s worry that staying there would cause even more problems. For example: 孟子的妈妈想：住在这里会有更多麻烦。

**New Words**
- 老是 (“墓地老是有很多人祭拜”)：经常 (“墓地经常有很多人祭拜”)，“经常” clearly describes that people came there often, without the slightly impatient feeling of “老是”.

**Encouragement** You clearly set the scene by introducing the cemetery and the people who came to mourn. You also included that the family stayed there for only a week and showed that the environment affected Mengzi’s learning.

### Scene 2

> 孟子的妈妈觉得孟子取得良好的教育是很重要的，所以孟子的妈妈认为这样的地方对儿子的教育不太好，就打算跟孟子搬家。孟子的妈妈带孟子不是搬到城市，而是搬到了孟子老师的家。

**Grammar and Vocab Corrections**
- 孟子取得良好的教育：孟子接受良好的教育，取得 is not used with 教育. A person 接受 education.
- 孟子的妈妈带孟子不是搬到城市，而是搬到了孟子老师的家：孟子的妈妈带孟子搬家，不是搬到城市，而是搬到了孟子的老师的家，搬家 must be stated after 带孟子, because it is the action being contrasted with 搬到城市. Also, 孟子的老师的家 means “the home of Mencius's teacher”; 孟子老师 would mean “Teacher Mencius.”

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “孟子的妈妈觉得孟子取得良好的教育是很重要的，所以孟子的妈妈认为这样的地方对儿子的教育不太好，就打算跟孟子搬家”: You could add the mother's specific worry that Mengzi might copy the mourning rituals he sees every day. For example: 她担心孟子会学别人祭拜。

**New Words**
- 打算 (“就打算跟孟子搬家”)：决定 (“就决定带着孟子搬家”)，“决定” shows that the mother has made a firm choice, while “打算” can sound less definite.

**Encouragement** You clearly explain Mengzi’s mother’s reason for moving: she cares about her son’s education. The contrast with “不是……而是……” also makes her choice easy to understand.

### Scene 3

> 孟子跟他的老师从早到晚学习，难怪他的成绩很快就进步了很多。孟子学习的时候，孟子的妈妈不是待在家里就是编织衣服赚钱。以后孟子成为了中国有名的哲学家。

**Grammar and Vocab Corrections**
- Nothing to flag.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “孟子跟他的老师从早到晚学习”: You could show his mother’s happy reaction when she sees that he is studying seriously. For example: 孟子的妈妈看见他认真学习，心里很高兴。
- After “以后孟子成为了中国有名的哲学家”: You could add that people connected his success with his mother’s three moves. For example: 人们都说，他的成功离不开妈妈三次搬家。

**New Words**
- 进步 (“成绩很快就进步了很多”)：提高 (“成绩很快就提高了很多”)，提高 is more precise when you are specifically talking about grades improving.

**Encouragement** You clearly show the result of Mengzi’s hard work by linking his all-day studying to his quickly improved grades. Your use of “难怪” makes the cause-and-effect relationship especially clear.

### Content & completeness (after the whole story)

- Need to add: 孟子 himself imitates how to offer sacrifices.
- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Need to add: The move from the market to a neighborhood near a school.
- Wrong information: “孟子的妈妈带孟子不是搬到城市，而是搬到了孟子老师的家。” -- The story has them move near the market after the graveyard, and later move from the market to a neighborhood near a school; they do not move to 孟子老师's home.

## mengmu_samples#25

### Scene 1

> 这是古代的故事。孟子小的时候，他的爸爸很早就去世了。从他的家到墓地很近，所以他每天老是从早到晚去墓地跟朋友们玩玩儿。

**Grammar and Vocab Corrections**
- 从早到晚去墓地跟朋友们玩玩儿：从早到晚去墓地跟朋友们玩儿，玩玩儿 means to play for a short time or just a little. It does not fit with 从早到晚, which means for the whole day.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 孟子小的时候，他的爸爸很早就去世了：有一个小男孩叫孟子，他小的时候，爸爸很早就去世了，This is Mengzi's first appearance in the story, so introduce him with a noun phrase that says who he is, not only with his name.

**Expressiveness**
- After “从他的家到墓地很近，所以他每天老是从早到晚去墓地跟朋友们玩玩儿”: Add the detail that he often saw people coming to worship at the cemetery, which helps explain what caught his attention there. For example: 他常常看到很多人来墓地祭拜。

**New Words**
- No suggestions.

**Encouragement** You clearly set the story in ancient times and explained why Mencius went to the cemetery so often. The cause-and-effect link from living nearby to playing there is easy to follow.

### Scene 2

> 他的妈妈觉得在墓地玩儿，害得，所以他们搬家。搬家对孟子有好的影响，他才五岁，可是每天不是写字就是帮妈妈的工作。

**Grammar and Vocab Corrections**
- 他的妈妈觉得在墓地玩儿，害得，所以他们搬家：他的妈妈觉得在墓地玩儿不好，所以他们搬家，害得 must be followed by the harmful result that it causes. Here no result is given, so use 不好 to say that playing in the cemetery is not good.
- 每天不是写字就是帮妈妈的工作：每天不是写字就是帮妈妈工作，帮妈妈 means “help Mother,” and 工作 can be the verb “work.” Do not use 的 between 妈妈 and 工作 here.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “他的妈妈觉得在墓地玩儿，害得，所以他们搬家”: You could add the mother’s worried thought to show why she decided to move. For example: 妈妈想：“这儿不适合孩子，我们搬家吧。”

**New Words**
- No suggestions.

**Encouragement** You clearly show that the move had a positive effect on Mencius. You also use “才五岁，可是” to highlight that he was very young but already did many things.

### Scene 3

> 他很聪明的人，难怪他成为有名的人。

**Grammar and Vocab Corrections**
- 他很聪明的人：他是很聪明的人，A noun phrase used as the predicate needs 是 here. Say 他是很聪明的人, meaning “He is a very smart person.”
- 成为有名的人：成为有名的哲学家，成为 needs a noun that names what he became. 有名的人 only means “a famous person”; here 孟子 became a famous philosopher.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “他很聪明的人，难怪他成为有名的人”: Add what kind of famous person he became to make the ending more specific. For example: 他后来成为了哲学家。

**New Words**
- No suggestions.

**Encouragement** You gave the story a clear ending by connecting Mencius’s later success with his personal qualities. Using “难怪” makes the conclusion sound natural and shows a clear cause-and-result link.

### Content & completeness (after the whole story)

- Need to add: 孟子 imitating how to offer sacrifices.
- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Missing scene: 孟母 moved from the market to the neighborhood near a school, 孟子started to study every day
- Wrong information: “从他的家到墓地很近，所以他每天老是从早到晚去墓地跟朋友们玩玩儿。” -- At the graveyard, 孟子 should imitate offering sacrifices, not play with friends.
- Wrong information: “他的妈妈觉得在墓地玩儿，害得，所以他们搬家。” -- 孟母 moves because she worries that 孟子's imitation of sacrifices will affect him badly, not because playing in the graveyard is harmful.

## mengmu_samples#32

### Scene 1

> 有一天孟子去了墓地玩儿，但是他妈妈觉得这是不合适的地方让孩子玩，所以她决定了他们会搬家找更好的地方。她恐怕儿子的童年不会幸福，而且住在这儿教育不太好。因为她望子成龙，所以她会一直搬家才能找到质量好的教育。然后他们搬到了离城市更近的地方。

**Grammar and Vocab Corrections**
- 这是不合适的地方让孩子玩：这是不适合孩子玩的地方，适合 is used with the person or activity that is suitable. To describe a place for an activity, say 适合孩子玩的地方.
- 她决定了他们会搬家找更好的地方：她决定搬家，找更好的地方，决定 is a mental-state verb, so it does not take 了 here. After 决定, use the action that was decided, such as 搬家, rather than 他们会搬家.
- 住在这儿教育不太好：这儿的教育不太好，To say that the education in a place is not good, use the place phrase with 的 before 教育.
- 她会一直搬家才能找到质量好的教育：她要一直搬家，才能找到质量好的教育，Use 要 or 得 before an action that is necessary for a result with 才能. 会 does not fit this necessary-condition meaning.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 有一天孟子去了墓地玩儿：有一天，有一个小男孩叫孟子，他去了墓地玩儿，On a character's first appearance, introduce who the character is, not only the name. After that introduction, 他 can refer to 孟子.

**Expressiveness**
- After “有一天孟子去了墓地玩儿”: You could explain that he watched people at the cemetery and began copying what they did. For example: 他看见别人祭拜，也跟着学。
- After “然后他们搬到了离城市更近的地方”: You could add that the new area was busy because many merchants were selling things. For example: 那儿有很多商人卖东西，很热闹。

**New Words**
- 城市 (“搬到了离城市更近的地方”)：市中心 (“搬到了离市中心更近的地方”)，“市中心” is more specific and creates a clearer picture of the new neighbourhood.

**Encouragement** You clearly explain Meng Mu’s concern for her son’s future and give a reason for the family’s move. You also move the story forward well by introducing their new home nearer the city.

### Scene 2

> 他们住才一月就又搬家。古代的时候，一般人不喜欢卖东西的人。但是孟子老是跟这些卖东西的人常常玩儿，害得妈妈着急得很，因为她恐怕儿子会成为跟他们很像。她告诉了孟子：他们不是朋友，而是不好的人。

**Grammar and Vocab Corrections**
- 古代的时候：在古代，Use 在古代 to mean “in ancient times.” 古代的时候 is not the usual expression here.
- 孟子老是跟这些卖东西的人常常玩儿：孟子老是跟这些卖东西的人玩儿，老是 and 常常 both mean that something happens often. Do not use both frequency words together here.
- 她恐怕儿子会成为跟他们很像：她恐怕儿子会变得跟他们很像，Become similar is 变得跟……很像. 成为 needs a noun phrase after it, not 跟他们很像.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 他们住才一月就又搬家：他们才住了一个月就又搬家了，To say they lived somewhere for only one month, put 才 before 住 and say 一个⽉. Both living there and moving are completed actions in this sentence, so use 了.
- **Temporality** 她告诉了孟子：她告诉孟子，A saying verb that introduces direct speech normally does not take 了. Use 她告诉孟子 before the quotation.

**Expressiveness**
- After “但是孟子老是跟这些卖东西的人常常玩儿”: You could add Mengzi’s own words to show that he finds the merchants’ activities interesting. For example: 孟子说：“妈妈，我觉得他们卖东西很好玩儿。”
- After “因为她恐怕儿子会成为跟他们很像”: You could add the mother’s thought about how spending time with the merchants may affect his study. For example: 她想：“他每天这样玩儿，就没有时间学习了。”

**New Words**
- No suggestions.

**Encouragement** You clearly show the cause of the mother’s worry: Mengzi often spends time with the merchants. You also include the mother speaking to him, which helps make the scene feel more direct.

### Scene 3

> 你不是当数学家，而是当哲学家，不能当卖东西的人。所以他们又搬家。在他们第三个家，孟子学了怎么祭拜。妈妈感觉这个地方适合他们，告诉了孟子：我们找到了最后的家。在这儿妈妈让儿子从早到晚学习，他难怪成为有名的哲学家。

**Grammar and Vocab Corrections**
- 在他们第三个家：在他们的第三个家，When a possessive pronoun modifies a numbered noun phrase, use 的: 他们的第三个家.
- 在这儿妈妈让儿子从早到晚学习，他难怪成为有名的哲学家：在这儿妈妈让儿子从早到晚学习。难怪他成为了有名的哲学家，难怪 comes before the clause it comments on, not after the subject. 成为 is a completed event here, so use 了; making this a new sentence also makes 他 a natural reference to 儿子.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 所以他们又搬家：所以他们又搬家了，搬家 is a completed event here. Add 了 to show that they moved again.
- **Temporality** 妈妈感觉这个地方适合他们，告诉了孟子：我们找到了最后的家：妈妈感觉这个地方适合他们，告诉孟子：我们找到了最后的家，A saying verb that introduces direct speech does not use 了. Say 告诉孟子：… here.

**Expressiveness**
- After “所以他们又搬家”: Add that their new home was close to a school, which explains why this environment was different. For example: 他们的新家离学校很近。
- After “在他们第三个家，孟子学了怎么祭拜”: Add the mother's happiness when she sees that this place is better for her son. For example: 妈妈看到孟子认真学习，心里很高兴。

**New Words**
- 卖东西的人 (“不能当卖东西的人”)：商人 (“不能当商人”)，“商人” is a more precise everyday word for people whose job is selling things.

**Encouragement** You clearly show the important final change: the family moves again and Mencius eventually becomes a philosopher. You also use contrast in “不是……而是……” to explain what his mother wants for him.

### Content & completeness (after the whole story)

- Need to add: 孟子 imitating how to offer sacrifices at the graveyard
- Need to add: the market as the new neighborhood and Mencius imitating buying and selling
- Need to add: the school as the new neighborhood
- Wrong information: “有一天孟子去了墓地玩儿” -- At the graveyard, 孟子 imitates offering sacrifices rather than simply going there to play.
- Wrong information: “在他们第三个家，孟子学了怎么祭拜。” -- Learning or imitating sacrifices happens at the graveyard before the family moves away, not in the third home after the moves.

## mengmu_samples#33

### Scene 1

> 一天，很久很久以前，孟子和他妈妈住在中国。孟子妈妈的工作是祭拜，孟子不高兴，因为他说我们老是搬家，为什么？他妈妈说，从早到晚，我一直祭拜，很多墓地得我祭拜。所以我们得去很多不同的地方。

**Grammar and Vocab Corrections**
- 很多墓地得我祭拜：有很多墓地需要我祭拜，得 cannot be used after 墓地 in this way. Use 需要 to say that many cemeteries need him to worship there.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 孟子和他妈妈住在中国：有一个小男孩叫孟子，他和妈妈住在中国，When a character first appears, introduce them with a noun phrase that says who they are. Do not introduce a new character with only a name.
- **Conjunction** 孟子不高兴，因为他说我们老是搬家，为什么：孟子不高兴，因为他们老是搬家。他问：“为什么我们老是搬家？”，The reason for Mengzi being unhappy is that they move often, not that he says something. Use a separate question sentence for what he asks.

**Expressiveness**
- After “孟子不高兴，因为他说我们老是搬家，为什么”: You could add that Mengzi feels moving house is troublesome, which makes his complaint more personal. For example: 我觉得搬家很麻烦。
- After “他妈妈说，从早到晚，我一直祭拜，很多墓地得我祭拜”: You could show that his mother explains this patiently, so the dialogue has more feeling. For example: 妈妈耐心地说：“所以我们得去很多不同的地方。”

**New Words**
- No suggestions.

**Encouragement** You clearly set the story in the past and introduced Mengzi and his mother. You also used dialogue to show why Mengzi is unhappy about moving.

### Scene 2

> 孟子想，难怪我们常常搬家，原来我妈妈很忙。可是常常搬家害得孟子很难找到朋友。每次搬家孟子也觉得新的地方不是太热就是太冷，不是太大就是太小。在哪的地方，他都不高兴。孟子想帮助妈妈祭拜，可是他六岁，所以不能祭拜。

**Grammar and Vocab Corrections**
- 在哪的地方，他都不高兴：不管在哪个地方，他都不高兴，在哪 cannot be followed by 的地方. To say that he is unhappy regardless of the place, say 不管在哪个地方.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “孟子想，难怪我们常常搬家，原来我妈妈很忙”: You could add a small detail that shows how hard his mother works each day. For example: 妈妈每天都很累。
- After “可是常常搬家害得孟子很难找到朋友”: You could include a short question to show Mengzi’s worry about moving so often. For example: 妈妈，我们什么时候不用搬家？

**New Words**
- 常常 (“难怪我们常常搬家”)：老是 (“难怪我们老是搬家”)，“老是” emphasizes that the moves happen repeatedly and feels more natural when Mengzi is unhappy about them.

**Encouragement** You clearly show Mengzi’s thoughts with “难怪……原来……”, which helps the reader understand why he realizes his mother is busy. You also give several reasons why moving makes him unhappy, so this scene has clear detail.

### Scene 3

> 四年后，孟子开始帮妈妈祭拜。他画画很厉害，他越来越喜欢祭拜，所以他祭拜不是想帮妈妈工作，而是他很喜欢画画。孟子成为很著名的古代画家。今天很多中国人很喜欢孟子。

**Grammar and Vocab Corrections**
- Nothing to flag.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 他画画很厉害，他越来越喜欢祭拜，所以他祭拜不是想帮妈妈工作，而是他很喜欢画画：他画画很厉害，越来越喜欢祭拜，所以祭拜不是想帮妈妈工作，而是很喜欢画画，In the same sentence, once 他 has been used for Mengzi, later references to the same person should normally be omitted.
- **Temporality** 孟子成为很著名的古代画家：孟子成为了很著名的古代画家，Becoming a famous painter is a completed event in the story, so 成为 needs 了.

**Expressiveness**
- After “四年后，孟子开始帮妈妈祭拜”: You could add a short line of speech to show that Mengzi wants to help his mother. For example: 孟子说：“妈妈，我想跟你一起祭拜。”
- After “今天很多中国人很喜欢孟子”: You could describe what people appreciate about his paintings. For example: 他们觉得他的画很漂亮。

**New Words**
- No suggestions.

**Encouragement** You clearly show the time passing with “四年后” and connect Mengzi’s interest in drawing to his future as a famous painter. The final sentence also gives the story a strong link to the present.

### Content & completeness (after the whole story)

- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Missing scene: 孟母 moved from the market to the neighborhood near a school, 孟子started to study every day
- Need to add: 孟子 becomes a famous philosopher, not a painter.
- Wrong information: “孟子成为很著名的古代画家。” -- 孟子 becomes a famous philosopher, not an ancient painter.

## mengmu_samples#39

### Scene 1

> 古代的时候人觉得祭拜非常重要，孟子很小的时候，从早到晚一直祭拜，因为他妈妈告诉他祭拜很重要。虽然他没有朋友，因为每天只祭拜。他的同学们老是对他开玩笑了。孟子妈妈看了他的同学们对孟子不好的影响，所以孟子和孟子妈妈搬家了。

**Grammar and Vocab Corrections**
- 孟子妈妈看了他的同学们对孟子不好的影响：孟子妈妈看出同学们对孟子有不好的影响，看了 means “looked at,” but here the mother realizes or notices the bad effect, so use 看出. Say 对孟子有不好的影响, not 对孟子不好的影响.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 孟子很小的时候，从早到晚一直祭拜：有一个小男孩叫孟子，他很小的时候，从早到晚一直祭拜，This is Mengzi's first appearance in the story, so introduce him with a noun phrase that says who he is, not only with his name.
- **Reference** 孟子和孟子妈妈搬家了：孟子和妈妈搬家了，孟子妈妈 has already been named earlier in this sentence. Do not repeat her full name again in the same sentence; 妈妈 is enough here.
- **Temporality** 他的同学们老是对他开玩笑了：他的同学们老是对他开玩笑，老是 describes a repeated habit, so do not use 了, which marks a completed action.
- **Conjunction** 虽然他没有朋友，因为每天只祭拜：因为他每天只祭拜，所以没有朋友，Although and because cannot be used together this way. Here, worshipping all day is the reason that he has no friends, so use 因为……所以…….

**Expressiveness**
- After “他的同学们老是对他开玩笑了”: You could add how Mencius felt when his classmates kept teasing him. For example: 孟子觉得很难过。
- After “孟子妈妈看了他的同学们对孟子不好的影响”: You could show that his mother was worried after noticing this negative influence. For example: 孟子妈妈很着急。

**New Words**
- 觉得 (“人觉得祭拜非常重要”)：重视 (“古代的时候人很重视祭拜”)，“重视” is more precise because it directly describes treating worship as important.

**Encouragement** You clearly explain the reason Mencius kept worshipping: his mother told him it was important. You also use cause and effect well to connect the classmates’ influence with the family’s move.

### Scene 2

> 孟子才十一岁，成为一个哲学家。孟子不是祭拜，而是看政治文章，难怪他成为了哲学家。不过，看过很多政治文章对他害得，他有很多问题。

**Grammar and Vocab Corrections**
- 看过很多政治文章对他害得：看过很多政治文章对他有害，有害 means “to be harmful.” 害得 must be followed by a result, such as 害得他生病.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 孟子才十一岁，成为一个哲学家：孟子才十一岁，成为了一个哲学家，Becoming a philosopher is a completed event in the story, so use 了 after 成为.

**Expressiveness**
- After “孟子才十一岁，成为一个哲学家”: You could show his mother’s happiness to highlight how proud she is of his learning. For example: 孟子妈妈心里很高兴。
- After “不过，看过很多政治文章对他害得，他有很多问题”: You could add one short inner thought to show his curiosity about the questions. For example: 他常常想：“为什么会这样？”

**New Words**
- No suggestions.

**Encouragement** You clearly connect Mengzi’s reading with his becoming a philosopher. You also add that he has many questions, which makes him sound curious and thoughtful.

### Scene 3

> 他一直问问题，但是不能解决那些问题。孟子长大，他开始能解决问题。他常常建议你不是学金融，而是学政治，因为如果你懂政治，你会成为高薪。后来孟子成为教授，他教学生很厉害。

**Grammar and Vocab Corrections**
- 他常常建议你不是学金融，而是学政治：他常常建议你不要学金融，而是学政治，After 建议, use 不要 to advise someone not to do something. 不是……而是…… does not work directly before the verbs here.
- 你会成为高薪：你会得到高薪，高薪 is a high salary, not a person or job that someone can become. Use 得到高薪 to say someone receives a high salary.
- 他教学生很厉害：他教学生教得很好，When a verb has an object and you want to describe how the action is done, repeat the verb before 得. 教得很好 means “teaches very well.”

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 孟子长大：孟子长大了，Growing up is a completed change here, so use 了 after 长大.
- **Temporality** 孟子成为教授：孟子成为了教授，Becoming a professor is a completed event in the story, so it needs 了.

**Expressiveness**
- After “他一直问问题，但是不能解决那些问题”: Add how Mengzi feels when he cannot find the answers. For example: 他觉得很困惑。
- After “后来孟子成为教授，他教学生很厉害”: Add a short line showing what he tells his students about studying politics. For example: 他对学生说：“你们要好好学政治。”

**New Words**
- 一直 (“他一直问问题”)：老是 (“他老是问问题”)，“老是” emphasizes that he asks questions repeatedly, which fits this ongoing habit.
- 问题 (“不能解决那些问题”)：难题 (“不能解决那些难题”)，“难题” makes it clearer that these are difficult problems he cannot solve yet.

**Encouragement** You clearly show Mengzi’s development from someone with many unanswered questions to someone who can solve problems. You also give him a later role as a professor and explain that he teaches students well.

### Content & completeness (after the whole story)

- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Need to add: The move from the market to a neighborhood near a school, and that 孟子 studies every day.
- Wrong information: “孟子妈妈看了他的同学们对孟子不好的影响，所以孟子和孟子妈妈搬家了。” -- The story says 孟母 moved because she thought 孟子 copying sacrifices would have a bad influence, not because of his classmates.

## mengmu_samples#45

### Scene 1

> 古代的时候，一个男孩子跟他的妈妈住在中国。他叫孟子。他们住在墓地的旁边，所以孟子老是祭拜。孟子不是祭拜，就是跟朋友聊天。他很喜欢他的城市，但是城市有才两个学校，都很小。

**Grammar and Vocab Corrections**
- 古代的时候：在古代，Use 在古代 to mean “in ancient times.” 古代的时候 is not the usual expression here.
- 他很喜欢他的城市，但是城市有才两个学校，都很小：他很喜欢他的城市，但是只有两个学校，都很小，才 must come before 有, or you can use 只有. After 城市 has already been mentioned in the same sentence, do not repeat it; the omitted subject is understood.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “他们住在墓地的旁边，所以孟子老是祭拜”: Add his thought to explain why he wanted to copy the people at the cemetery. For example: 他觉得祭拜很有趣。
- After “孟子不是祭拜，就是跟朋友聊天”: Add a small action detail to show that he did not treat the worship seriously. For example: 他一边笑，一边祭拜。

**New Words**
- No suggestions.

**Encouragement** You clearly introduce Mengzi, his mother, and where they live. You also use “不是……就是……” well to show what Mengzi often does.

### Scene 2

> 他的妈妈不是不喜欢他们的城市，而是想孟子有很好的教育。他们搬家到有很多学校的城市。他们从早到晚走路，孟子一直抱怨。

**Grammar and Vocab Corrections**
- 而是想孟子有很好的教育：而是想让孟子接受很好的教育，想 cannot directly take a person followed by an action or situation. Use 想让 to say that someone wants another person to do or have something; 接受很好的教育 is the natural expression here.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 他们搬家到有很多学校的城市：他们搬到了有很多学校的城市，This move is a completed event in the story, so 搬 needs 了. Say 搬到了 for “moved to.”

**Expressiveness**
- After “孟子一直抱怨”: You could add a short thought to show that Mengzi does not understand why they need to move. For example: 孟子心想：“为什么我们要搬家？”

**New Words**
- No suggestions.

**Encouragement** You clearly show the mother’s goal by using the contrast “不是……而是……”. The time phrase “从早到晚” also makes the journey feel long and difficult.

### Scene 3

> 他难怪抱怨，他想他的朋友，因为他不要离开他的城市。他的妈妈找到孟子一个老师。跟老师孟子学最重要的文学，所以他成为哲学家。

**Grammar and Vocab Corrections**
- 他难怪抱怨：难怪他抱怨，难怪 normally comes before the person or event that it explains. Say 难怪他抱怨, meaning “No wonder he complained.”
- 因为他不要离开他的城市：因为他不想离开他的城市，不要 usually means “do not” as a command or “do not need.” To say that someone does not want to do something, use 不想 before the verb.
- 他的妈妈找到孟子一个老师：他的妈妈给孟子找到了一个老师，Use 给 to show that the teacher was found for 孟子. 找到了 also shows that the mother successfully completed the action.
- 跟老师孟子学最重要的文学：孟子跟老师学最重要的文学，The subject 孟子 comes before the phrase 跟老师. This says that Mencius studies important literature with a teacher.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “他的妈妈找到孟子一个老师”: You could show that his mother felt happy because Mengzi now had a teacher to help him learn. For example: 妈妈很高兴。
- After “跟老师孟子学最重要的文学，所以他成为哲学家”: You could add Mengzi’s positive reaction to studying literature. For example: 孟子觉得文学很有意思。

**New Words**
- No suggestions.

**Encouragement** You clearly explain why Mengzi complained: he did not want to leave his friends and city. You also connect his learning with his later success as a philosopher.

### Content & completeness (after the whole story)

- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Need to add: They move from the market neighborhood to a neighborhood near a school.
- Wrong information: “他的妈妈不是不喜欢他们的城市，而是想孟子有很好的教育。” -- This gives a different reason for the move. In the story, 孟母 moves away from the graveyard because she thinks 孟子 copying sacrifices will affect him badly.

## mengmu_samples#47

### Scene 1

> 这个男孩子叫孟子，孟子是古代的人。孟子的妈妈觉得住在哪儿对童年很重要，所以他们常常搬了家。她望子成龙，所以孟子的妈妈安排他的生活。

**Grammar and Vocab Corrections**
- Nothing to flag.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 孟子是古代的人：是古代的人，孟子 was already named earlier in the same sentence. In the next clause of the same sentence, omit the repeated subject.
- **Reference** 她望子成龙，所以孟子的妈妈安排他的生活：她望子成龙，所以安排他的生活，她 and 孟子的妈妈 refer to the same person in one sentence. After the first subject, omit the repeated subject.
- **Temporality** 他们常常搬了家：他们常常搬家，常常 describes a repeated routine, so do not use 了. Use 搬家 for something that happens regularly.

**Expressiveness**
- After “孟子的妈妈觉得住在哪儿对童年很重要，所以他们常常搬了家”: You could add the mother’s hope that a better environment would help Mengzi grow up well. For example: 她希望孟子在好的环境里长大。

**New Words**
- 童年 (“住在哪儿对童年很重要”)：成长 (“住在哪儿对成长很重要”)，“成长” focuses more specifically on how the environment affects a child’s development.

**Encouragement** You clearly introduce Mengzi and explain his mother’s important reason for moving. Using “望子成龙” also shows that you understand her hopes for her son.

### Scene 2

> 因为他们常常搬了家，中国人说，孟母三迁。孟子没有爸爸，所以，他的妈妈更重要。从这儿到那儿，妈妈教孟子很多技能。先她让孟子跟朋友玩儿，然后教他怎么买又便宜又好质量的东西。

**Grammar and Vocab Corrections**
- 先她让孟子跟朋友玩儿：她先让孟子跟朋友玩儿，The subject comes before 先 in this sentence. Say 她先让……, not 先她让…….
- 教他怎么买又便宜又好质量的东西：教了他怎么买又便宜又质量好的东西，质量好, not 好质量, means “good quality.” These are completed actions in sequence, so the last verb, 教, takes 了.

**Coherence: Reference / Temporality / Conjunction**
- **Conjunction** 因为他们常常搬了家，中国人说，孟母三迁：因为他们常常搬家，所以中国人说：“孟母三迁。”，A cause and result should use 因为……所以…… together here. 常常 describes a routine, so 搬家 does not take 了.

**Expressiveness**
- After “然后教他怎么买又便宜又好质量的东西”: You could add that Mengzi copied the merchants by collecting money and bargaining. For example: 孟子也学着商人收钱、讨价还价。

**New Words**
- No suggestions.

**Encouragement** You clearly connect Mengzi’s mother’s importance with the family’s repeated moves. You also include a concrete skill he learned, which makes the story more specific.

### Scene 3

> 最后，她让孟子学写作。他不是写作就是看书，难怪他很聪明。现在在中国，孟子很有名。

**Grammar and Vocab Corrections**
- Nothing to flag.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “他不是写作就是看书，难怪他很聪明”: You could add his mother’s happy reaction when she sees that he has started studying seriously. For example: 孟子的妈妈很高兴，觉得这儿很适合孩子。
- After “现在在中国，孟子很有名”: You could mention that he later became a philosopher to explain why people still know him. For example: 后来，孟子成了哲学家。

**New Words**
- No suggestions.

**Encouragement** You used the pattern “不是……就是……” well to show Mengzi’s regular activities. You also connected his studying to his intelligence and later fame with “难怪,” which makes the ending flow clearly.

### Content & completeness (after the whole story)

- Missing scene: 孟子and孟母lived near a graveyard, and 孟子 imitated how to offer sacrifices every day
- Need to add: the move to a neighborhood near the market
- Need to add: 孟母 moving from the market to a neighborhood near a school

## shennong_samples#4

### Scene 1

> 古代的时候，有一个男人，他的名字是神农。他看到了有很多人不知道哪个植物好吃，也不知道什么植物对你的身体有好处。这个问题神农觉得很糟糕，所以神农去了吃每种植物。他吃了一种植物以后，就写了这个植物对你有没有好处。有的时候，神农吃了很好吃的植物。有的时候，他吃了很危险的植物。他吃完了每种植物以后，会来跟他的朋友聊到他吃的植物了。

**Grammar and Vocab Corrections**
- 古代的时候：在古代，Use 在古代 to mean “in ancient times.” 古代的时候 is not the usual expression here.
- 哪个植物：哪种植物，Use 种 as the measure word for types of plants. Say 哪种植物, not 哪个植物.
- 什么植物对你的身体有好处：什么植物对身体有好处，This sentence is about people in general, not about the reader specifically. Say 对身体有好处 for “be good for the body.”
- 所以神农去了吃每种植物：所以去吃了每种植物，The subject 神农 has already appeared in the same sentence, so do not repeat it. Also, when 去 is followed by another action, put 了 after the main action: 去吃了.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 有的时候，神农吃了很好吃的植物：有的时候，神农吃很好吃的植物，有的时候 describes a repeated or habitual action, so do not use 了 after 吃.
- **Temporality** 有的时候，他吃了很危险的植物：有的时候，他吃很危险的植物，有的时候 describes a repeated or habitual action, so do not use 了 after 吃.
- **Temporality** 会来跟他的朋友聊到他吃的植物了：会来跟他的朋友聊到他吃的植物，会 is a modal verb, so the action after it does not take the completion particle 了 here.

**Expressiveness**
- After “这个问题神农觉得很糟糕”: Show Shen Nong’s concern by adding a short thought about wanting to help the people. For example: 神农想：“我要帮助他们。”
- After “他吃了一种植物以后，就写了这个植物对你有没有好处”: Add the detail that he recorded his findings in a book. For example: 他把这些写在书上。

**New Words**
- No suggestions.

**Encouragement** You clearly introduce Shen Nong and explain the problem that people did not know which plants were safe. Your repeated “有的时候” structure also shows that he tried both good and dangerous plants.

### Scene 2

> 一个人问神农，哪个植物好吃。神农说，这就要看你的口味了。要是你喜欢吃甜的，有很多甜的水果，比方说苹果、西瓜和梨。一个别的人问神农，哪个植物对你的身体有好处。神农说，有很多种植物对你的身体有好处，比方说小白菜、黄瓜、茶和菠菜。一个别的人问神农，哪个植物对你的身体有坏处。

**Grammar and Vocab Corrections**
- 哪个植物好吃：哪种植物好吃，Use 种 as the measure word when asking which kind of plant: 哪种植物.
- 一个别的人：另外一个人，另外一个人 means “another person.” 一个别的人 is not the natural expression here.
- 哪个植物对你的身体有坏处：哪种植物对身体有坏处，Use 哪种植物 to ask which kind of plant. For a general statement about health, say 对身体有坏处 without 你的.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “一个别的人问神农，哪个植物对你的身体有坏处”: Let Shennong answer with a clear warning that poisonous plants should not be eaten, using oleander as an example from the story. For example: 神农说：“有毒的植物对身体有坏处，像夹竹桃，不能吃。”

**New Words**
- No suggestions.

**Encouragement** You clearly show that different people have different questions about plants. Your concrete examples of sweet fruit and healthy vegetables make Shennong’s answers easy to understand.

### Scene 3

> 神农说，有一天，我吃了一个黄色的花，名字是夹竹桃。我一吃夹竹桃，就觉得这种植物对我的脑有坏处。可是，一个灵芝和一个男人正好在我的旁边，我说，麻烦你把那个植物给我吃一下。我一吃这个灵芝就好了。所以，你得小心吃植物，因为有的植物对你的健康有坏处，特别是夹竹桃。因为夹竹桃有毒。

**Grammar and Vocab Corrections**
- 一个黄色的花：一朵黄色的花，花 takes the measure word 朵, not 个. Say 一朵花.
- 我一吃这个灵芝就好了：我一吃这个灵芝，身体就好了，身体 needs to be the subject of 好了. Saying 我好了 here incorrectly makes the whole person, rather than the person's health, become good.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “神农说，有一天，我吃了一个黄色的花，名字是夹竹桃”: Describe the flower’s appearance to make the dangerous plant seem beautiful at first. For example: 那朵花又黄又大，像星星一样漂亮。
- After “我一吃夹竹桃，就觉得这种植物对我的脑有坏处”: Add how scared Shennong felt when the plant made him ill. For example: 我想：我会死吗？

**New Words**
- No suggestions.

**Encouragement** You clearly included the important contrast between poisonous oleander and helpful lingzhi. Your final warning about being careful with plants also gives this scene a strong message.

### Content & completeness (after the whole story)

- Need to add: 神农 finding 茶
- Need to add: 神农 fainting after eating 夹竹桃
- Wrong information: “我一吃夹竹桃，就觉得这种植物对我的脑有坏处。” -- In the story, eating 夹竹桃 makes 神农 faint; it is not described as only harming his brain.

## shennong_samples#8

### Scene 1

> 古代的时候，有一个人叫神农。一天，神农正在路上走，一看很多人正在吃一些植物。一些人一吃植物就生病了，神农想帮别人。所以想知道哪些植物能吃，哪些植物不能吃。

**Grammar and Vocab Corrections**
- 古代的时候：在古代，Use 在古代 to say that something happened in ancient times.
- 神农正在路上走，一看很多人正在吃一些植物：神农正在路上走，看到很多人正在吃一些植物了，一看 cannot mean that Shennong saw people here. Use 看到 for a completed action of seeing, and use 了 because the people are in the middle of eating.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “一些人一吃植物就生病了”: Add Shennong’s worried reaction when he sees that people are getting sick. For example: 神农看着他们，心里很着急。
- After “所以想知道哪些植物能吃，哪些植物不能吃”: Add a determined thought to show why Shennong wants to find the answer. For example: 他想：我不能让大家再生病了。

**New Words**
- 生病 (“一吃植物就生病了”)：中毒 (“一吃植物就中毒了”)，“中毒” is more precise when someone becomes ill because they have eaten a poisonous plant.

**Encouragement** You clearly introduce Shennong and explain the problem that motivates him. You also use the pattern “哪些……，哪些……” well to show the contrast between edible and inedible plants.

### Scene 2

> 然后，神农开始尝很多植物，比方说他吃过生姜、芥兰和菠菜。一些植物吃真好，特别是黄瓜。但是，一些植物毒得很，特别是夹竹桃。

**Grammar and Vocab Corrections**
- 一些植物吃真好：一些植物很好吃，Use 很好吃 to say that a plant tastes good. 吃 is not used before 真好 in this sentence.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “但是，一些植物毒得很，特别是夹竹桃”: You could add Shen Nong’s concern that eating these plants can make people ill. For example: 神农想：吃了这些植物，人会生病。

**New Words**
- No suggestions.

**Encouragement** You clearly contrast plants that are good to eat with poisonous plants. The specific examples, especially 黄瓜 and 夹竹桃, make this part of the story easy to follow.

### Scene 3

> 一个人对神农说，麻烦我们可以吃什么植物？神农说，这就要看你想不想生病了。以后，神农告诉别人一些植物能吃，一些植物不能吃。

**Grammar and Vocab Corrections**
- 麻烦我们可以吃什么植物：请问，我们可以吃什么植物，麻烦 cannot introduce a direct question by itself. Use 请问 to politely ask a question.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 你想不想生病了：你想不想生病，想 is a mental-state verb, so it normally does not take 了 here. The sentence asks whether someone wants to become ill in general.

**Expressiveness**
- After “以后，神农告诉别人一些植物能吃，一些植物不能吃”: You could add one warning in Shennong’s own words to make his advice more vivid and specific. For example: 神农还说：“特别是新鲜的夹竹桃，吃了可能会死。”

**New Words**
- No suggestions.

**Encouragement** You clearly show that Shennong uses what he learned to help other people. The contrast between plants people can eat and plants they cannot eat is easy to understand.

### Content & completeness (after the whole story)

- Missing scene: 神农found茶and took a record
- Missing scene: 神农tried 夹竹桃 and fainted
- Missing scene: a person in blue stopped by and gave灵芝to 神农，神农felt better after eating灵芝
- Missing scene: 神农takes record of灵芝and夹竹桃

## shennong_samples#12

### Scene 1

> 很久以前，古代的人很不知道什么植物能吃，也什么植物不能吃。所以很多人常常吃不安全的植物，吃不安全的植物对你的身体有坏处，很麻烦的情况。但是一个人，神农，要解决这个问题。

**Grammar and Vocab Corrections**
- 古代的人很不知道什么植物能吃，也什么植物不能吃：古代的人不知道什么植物能吃，也不知道什么植物不能吃，很 cannot modify 不知道 here. Repeat 知道 after 也 to say that people also did not know which plants could not be eaten.
- 吃不安全的植物对你的身体有坏处，很麻烦的情况：吃不安全的植物对你的身体有坏处，这是一个很麻烦的情况，很麻烦的情况 is a noun phrase and cannot stand alone after the comma. Use 这是一个 to introduce and describe the situation.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 但是一个人，神农，要解决这个问题：但是有一个人叫神农，要解决这个问题，When a character appears for the first time, introduce them with a noun phrase that says who they are. 有一个人叫神农 introduces Shennong naturally.

**Expressiveness**
- After “所以很多人常常吃不安全的植物”: You could add that people often became ill after eating these plants, showing why the problem was serious. For example: 很多人吃了以后，常常生病。
- After “但是一个人，神农，要解决这个问题”: You could add Shennong’s thought to make his goal more personal and clear. For example: 他想：“我要找出哪些植物能吃，哪些不能吃。”

**New Words**
- No suggestions.

**Encouragement** You clearly introduce the problem people faced and then bring in Shennong as the person who wants to help. This gives your scene a clear beginning and purpose.

### Scene 2

> 他又聪明又努力，旅行很远找到很多植物。比方说，灵芝和夹竹桃。他一吃各种各样的植物就知道能不能吃这些植物。然后，神农写他的主意。他喜欢植物的味道，特别是花。神农遇到了一个黄色的花，一吃就觉得不舒服。

**Grammar and Vocab Corrections**
- 旅行很远找到很多植物：旅行到很远的地方，找到了很多植物，Chinese normally says 旅行到很远的地方 for travelling far away. The final action in this completed series needs 了, so say 找到了很多植物.
- 然后，神农写他的主意：然后，神农写下了他的主意，Use 写下 to mean “write down” an idea. This is a completed action, so 写下 needs 了.
- 植物的味道，特别是花：植物，特别是花，花 is a kind of plant, not a kind of 味道. Say that he likes plants, especially flowers.
- 一个黄色的花：一朵黄色的花，Flowers use the measure word 朵, not 个.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “神农遇到了一个黄色的花，一吃就觉得不舒服”: You could describe the flower’s appearance to make this moment easier to picture. For example: 那朵花像星星一样，又大又漂亮。

**New Words**
- 不舒服 (“一吃就觉得不舒服”)：难受 (“一吃就觉得难受”)，“难受” gives a stronger, more vivid sense of how bad Shen Nong feels.

**Encouragement** You clearly connect Shen Nong’s plant research with his discovery of 灵芝 and 夹竹桃. You also show the important result of eating the yellow flower, which moves the story forward.

### Scene 3

> 发现了夹竹桃有毒。别人看到他，很快给他吃一个灵芝。神农一吃就觉得比较好。然后，他继续写他发现的信息。会告诉他的朋友哪一个植物能不能吃。

**Grammar and Vocab Corrections**
- 会告诉他的朋友哪一个植物能不能吃：会告诉他的朋友哪一种植物能吃，哪一种植物不能吃，With 哪一种植物, say separately which plants can be eaten and which cannot be eaten. Do not use 能不能 after 哪一种植物 in this sentence.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 别人看到他：有一个人看到他，别人 is vague when this person appears for the first time. Introduce the new character with a noun phrase such as 有一个人.

**Expressiveness**
- After “发现了夹竹桃有毒”: You could add Shen Nong’s frightened thought when he realizes that the flower is poisonous. For example: 他想：“我会死吗？”
- After “神农一吃就觉得比较好”: You could describe his physical relief to make the recovery feel clearer. For example: 他的肚子不那么疼了。

**New Words**
- 好 (“觉得比较好”)：舒服 (“觉得比较舒服”)，“舒服” is more precise because it describes how Shen Nong feels after taking the medicine.

**Encouragement** You clearly tell the important sequence: Shen Nong finds the poison, takes lingzhi, feels better, and shares what he learned. Including both 夹竹桃 and 灵芝 shows that you understand the key contrast in this scene.

### Content & completeness (after the whole story)

- Need to add: He found 茶.
- Need to add: 神农 tries 夹竹桃 and faints.
- Missing scene: another person in brown came by and had a conversation with 神农

## shennong_samples#18

### Scene 1

> 神农和他的家人住在古代，所以不知道什么植物能吃。因为他的家人常常生病了，所以神农和他的哥哥一起去旅行找可以吃的植物。他们去很多不一样的地方，比方说高山、山谷和沙漠。

**Grammar and Vocab Corrections**
- Nothing to flag.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 神农和他的家人住在古代：有一个叫神农的人和他的家人住在古代，This is the first mention of 神农, so introduce him with a noun phrase that says who he is, not only with his name.
- **Temporality** 常常生病了：常常生病，常常 shows a repeated habit or routine, so 生病 does not take 了.
- **Temporality** 他们去很多不一样的地方：他们去了很多不一样的地方，This describes a completed past action in the story, so 去 needs 了.

**Expressiveness**
- After “因为他的家人常常生病了，所以神农和他的哥哥一起去旅行找可以吃的植物”: Add Shennong’s worried thought to show why finding plants matters so much to him. For example: 神农心里很着急，想快点找到可以吃的植物。
- After “他们去很多不一样的地方，比方说高山、山谷和沙漠”: Add that the journey was long and tiring to make their search feel more challenging. For example: 他们走了很久，觉得很累。

**New Words**
- No suggestions.

**Encouragement** You clearly explain the problem first—Shennong’s family often gets sick—and then give a reason for his journey. Listing the mountains, valleys, and desert also makes the search feel wide-ranging.

### Scene 2

> 他们在很漂亮的河找夹竹桃。神农问他的哥哥：“我应该吃这种植物吗？”哥哥说：“这就要看你想要安全还是接近知道了。“神农一吃夹竹桃就生病了。哥哥说：“太麻烦了。

**Grammar and Vocab Corrections**
- 他们在很漂亮的河找夹竹桃：他们在很漂亮的河边找夹竹桃，To say an action happens by a river, use 河边. 在很漂亮的河边 comes before the verb 找.
- 这就要看你想要安全还是接近知道了：这就要看你想要安全，还是想知道，接近 cannot be used before 知道 this way. Say 想知道 for “want to know,” and do not use 了 with the mental-state verb 想知道.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “神农一吃夹竹桃就生病了”: Add a physical detail to show how seriously ill Shennong feels after eating the plant. For example: 他觉得肚子很疼。
- After “哥哥说：“太麻烦了”: Add Shennong’s worried thought to show his fear while he is sick. For example: 他想：“我会死吗？”

**New Words**
- No suggestions.

**Encouragement** You used dialogue to show Shennong asking his brother for advice, which makes the scene more story-like. You also clearly showed the consequence of eating the oleander: Shennong became ill immediately.

### Scene 3

> 夹竹桃是毒的，我想知道灵芝会帮他。”哥哥给神农灵芝。神农吃完了以后开始痊愈了。神农说：“谢谢哥哥，你帮得真好。灵芝我们可以吃，特别是如果我们已经吃了夹竹桃。“

**Grammar and Vocab Corrections**
- 夹竹桃是毒的：夹竹桃有毒，Use 有毒 to say that a plant is poisonous. 是毒的 is not natural Chinese here.
- 神农吃完了以后开始痊愈了：神农吃完了以后痊愈了，痊愈 means to recover completely, so it cannot happen after 开始. Use 痊愈了 for a completed recovery.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 哥哥给神农灵芝：哥哥给了神农灵芝，Giving the lingzhi is a completed action, so 给 needs 了.

**Expressiveness**
- After “夹竹桃是毒的”: Add a physical detail to show how badly Shennong reacted after eating the poisonous plant. For example: 神农的肚子疼得很厉害。
- After “神农吃完了以后开始痊愈了”: Add Shennong’s feeling of relief as he realizes that the lingzhi has helped him. For example: 神农觉得好多了，也放心了。

**New Words**
- No suggestions.

**Encouragement** You clearly show the important connection between the poisonous oleander and the lingzhi that helps Shennong recover. Your dialogue also explains when lingzhi can be useful.

### Content & completeness (after the whole story)

- Missing scene: 神农found茶and took a record
- Missing scene: another person in brown came by and had a conversation with 神农
- Missing scene: 神农takes record of灵芝and夹竹桃
- Wrong information: “哥哥给神农灵芝。” -- In the story, a person who stops by gives 灵芝 to 神农, rather than his accompanying brother.

## shennong_samples#19

### Scene 1

> 古代的时候，一个男人觉得植物很有意思。他叫神农。有的植物吃了以后他的肚子疼死了，可是有的吃了以后很舒服。他找很多植物。

**Grammar and Vocab Corrections**
- 古代的时候：在古代，Use 在古代 to mean “in ancient times.” 古代的时候 is not the correct expression here.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 他找很多植物：他找了很多植物，This is a completed action in the story, so 找 needs 了.

**Expressiveness**
- After “有的植物吃了以后他的肚子疼死了，可是有的吃了以后很舒服”: You could add his question about why different plants have such different effects. For example: 他想：“有的植物有毒吗？”
- After “他找很多植物”: You could show that Shennong was determined to continue even though some plants made him ill. For example: 可是他不怕，还想继续找。

**New Words**
- No suggestions.

**Encouragement** You clearly introduce Shennong and explain why plants interested him. The contrast between plants that hurt his stomach and plants that made him feel well makes his reason for searching easy to understand.

### Scene 2

> 凉山很大的山，这也找植物。一天，他找到黄色的花。他听说你跟黄色的花做茶很有用。比方说，你的头发疼死，这冰茶是药。他一喝茶就很不舒服。

**Grammar and Vocab Corrections**
- 凉山很大的山，这也找植物：凉山是很大的山，他也在这里找植物，Use 是 to say that Liangshan is a big mountain. 神农 is the person who looks for plants, so use 他 as the subject, and put 在这里 before 找植物.
- 你跟黄色的花做茶：用黄色的花泡茶，Use 用 to say what is used to make tea. 泡茶 is the usual verb for making tea, not 跟……做茶.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 他找到黄色的花：他找到了黄色的花，This is a completed event in the story, so 找到 needs 了.
- **Conjunction** 比方说，你的头发疼死，这冰茶是药：如果你的头疼死了，这种茶就是药，This sentence gives a condition, so use 如果, not 比方说. 头发 means “hair”; use 头疼 for a headache, and add 了 for the resulting state.

**Expressiveness**
- After “一天，他找到黄色的花”: Describe the flowers so the reader can picture why they caught Shennong’s attention. For example: 那些花又大又漂亮，像星星一样。
- After “他一喝茶就很不舒服”: Add Shennong’s worried thought to show how scared he feels. For example: 他想：我会死吗？

**New Words**
- No suggestions.

**Encouragement** You used “一天” to move the story forward clearly. You also gave the scene a clear cause-and-result sequence: Shennong tries something and then feels unwell.

### Scene 3

> 糟糕，这黄色的花是夹竹桃，特别是毒。正好在这儿，灵芝药的夹竹桃他吃完了，也写一个课文的植物。谢谢神农。

**Grammar and Vocab Corrections**
- 这黄色的花是夹竹桃，特别是毒：这黄色的花是夹竹桃，特别有毒，Use 有毒 to say that something is poisonous. 特别 is followed by 有毒 here, not 是毒.
- 灵芝药的夹竹桃他吃完了：他吃完灵芝和夹竹桃，Use 和 to join the two plant names, and put the subject 他 before the verb. In this series of completed actions, the final verb takes 了, so do not put 了 after 吃完.
- 也写一个课文的植物：也写了一篇关于植物的课文，A written text uses the measure word 篇. Say 关于植物的课文 for “a text about plants,” and use 了 because writing is the final completed action.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “灵芝药的夹竹桃他吃完了”: Add that Shennong soon feels better after taking the medicinal plant. For example: 神农很快觉得好多了。
- After “也写一个课文的植物”: Add Shennong’s thought about recording the plants so that other people can avoid danger. For example: 他想：我一定要写下来。

**New Words**
- No suggestions.

**Encouragement** You included the key contrast between the poisonous夹竹桃 and the helpful灵芝. You also remembered that Shennong writes about the plants, which shows why his discovery matters.

### Content & completeness (after the whole story)

- Missing scene: another person in brown came by and had a conversation with 神农
- Missing scene: 神农takes record of灵芝and夹竹桃
- Wrong information: “糟糕，这黄色的花是夹竹桃，特别是毒。” -- This makes the flower used to make 茶 into 夹竹桃. In the required story, 茶 is found first, and 夹竹桃 is a separate plant tried afterwards.

## shennong_samples#26

### Scene 1

> 很久以前，有一个老男人叫神农。神农在古代每一天看到了别的小镇人生病还是不舒服，所以他决定开始找新的药。他下一天开始爬当地的山脉，找了各种各样的植物。神农试一试每个植物，知道有什么好处。

**Grammar and Vocab Corrections**
- 他下一天开始爬当地的山脉：第二天，他开始爬当地的山脉，Use 第二天 to mean “the next day” in a story. Put this time phrase at the beginning of the sentence.
- 找了各种各样的植物：找到了各种各样的植物，找 means “to look for,” while 找到 means “to find.” Here he found the plants before trying them.
- 神农试一试每个植物：神农试了每一种植物，This is a completed action in the story, so use 了 instead of 试一试. Use 一种 as the measure word for kinds of plants.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 每一天看到了别的小镇人生病还是不舒服：每天看见别的小镇人生病或者不舒服，每天 describes a routine, so do not use 了 with the verb. In a statement, use 或者, not 还是, for “or.”

**Expressiveness**
- After “所以他决定开始找新的药”: You could add Shen Nong’s thought to show that he wants to help the sick people. For example: 他想：“我要帮助生病的人。”
- After “神农试一试每个植物，知道有什么好处”: You could add that he records what he learns, which shows why his careful testing is important. For example: 他把这些都写在书上。

**New Words**
- No suggestions.

**Encouragement** You clearly set the story in the past and introduced Shen Nong at the start. You also explained why he decided to look for medicine and described his actions in a clear sequence.

### Scene 2

> 比方说，他一次试一试有些植物的叶，吃得又新鲜又甜。煮这些叶以后，他一喝就知道他发现新的茶叶。虽然他找到了很多的新的植物，但是他的旅程有的时候特别是危险。比方说，他一吃灵芝就开始生病。

**Grammar and Vocab Corrections**
- 他一次试一试有些植物的叶，吃得又新鲜又甜：他试了一些植物的叶子，吃起来又新鲜又甜，Use 试了 with 一些 to say that he tried some leaves. 吃得 cannot describe the taste of the leaves; use 吃起来 to mean “taste when eaten.”
- 很多的新的植物：很多新的植物，When 很多 and 新 both modify a noun, say 很多新的植物. Do not put 的 after 很多 here.
- 有的时候特别是危险：有的时候特别危险，特别 is an adverb that goes directly before an adjective. Do not use 是 between 特别 and 危险.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 他一喝就知道他发现新的茶叶：他一喝就知道发现了新的茶叶，The second 他 has the same referent in the same sentence, so it should be omitted. 发现 is a completed discovery here, so it needs 了.
- **Temporality** 煮这些叶以后：煮了这些叶以后，Boiling the leaves is a completed action before the next action, so it needs 了 before 以后.

**Expressiveness**
- After “虽然他找到了很多的新的植物，但是他的旅程有的时候特别是危险”: You could describe the beautiful place and its yellow flowers before the danger happens. For example: 有一天，他到了一个很美的地方，那儿开着又黄又大的花。
- After “比方说，他一吃灵芝就开始生病”: You could show Shennong’s fear by adding what he thinks when he feels very ill. For example: 他想：“我会死吗？”

**New Words**
- No suggestions.

**Encouragement** You clearly use the tea discovery as an example of Shennong finding useful plants. You also add a contrast between his successful discoveries and the dangers of his journey.

### Scene 3

> 一个爬山的男人正好看到神农的麻烦，然后给了他一些药。神农最终他的小镇回到，跟别的人分享他的发现。你认为神农的故事真的吗？这就要看你相信中药对身体有好处。

**Grammar and Vocab Corrections**
- 神农最终他的小镇回到，跟别的人分享他的发现：神农最终回到他的小镇，跟别的人分享了他的发现，回到 comes before the place, so say 回到他的小镇. These are a series of finished actions, so the last verb, 分享, takes 了.
- 你认为神农的故事真的吗：你认为神农的故事是真的吗，Use 是 to link 故事 with the description 真的. Say 故事是真的吗？
- 这就要看你相信中药对身体有好处：这就要看你相不相信中药对身体有没有好处了，After 要看, use an either-or question to show the condition: whether you believe Chinese medicine is good for the body. The final 了 completes this concluding statement.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “一个爬山的男人正好看到神农的麻烦，然后给了他一些药”: Add that Shennong felt much better after taking the medicine, so the reader can see that it helped him. For example: 他吃了药以后，很快觉得好多了。
- After “神农最终他的小镇回到，跟别的人分享他的发现”: Add that he wrote the two plants in his book to show how he kept a record of what he learned. For example: 他把夹竹桃和灵芝写到了书上。

**New Words**
- No suggestions.

**Encouragement** You included the important rescue, with a man noticing Shennong’s problem and giving him medicine. You also gave the story a clear ending by bringing Shennong back to his town and reflecting on his discovery.

### Content & completeness (after the whole story)

- Need to add: He needs to try 夹竹桃 and faint; the story names 灵芝 instead and only says that he becomes ill.
- Need to add: The helper needs to give 灵芝, and 神农 needs to eat it and feel better.
- Missing scene: another person in brown came by and had a conversation with 神农
- Missing scene: 神农takes record of灵芝and夹竹桃
- Wrong information: “比方说，他一吃灵芝就开始生病。” -- 灵芝 is the plant that helps 神农 feel better after 夹竹桃 makes him faint; it does not make him sick.

## shennong_samples#33

### Scene 1

> 古代时候，人不知道他们能吃什么植物，常常一吃就死。但是不知道为什么，没有办法。所以有一天，神农出去试一试很多种植物，告诉人什么植物是安全什么是危险。

**Grammar and Vocab Corrections**
- 古代时候：在古代，Use 在古代 to mean “in ancient times.” 古代时候 is not the usual way to make this time expression.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 人不知道他们能吃什么植物：人不知道能吃什么植物，人 already refers to the people in this sentence, so 他们 is an unnecessary repeated reference. The subject of 能吃 can be left out because it is clear.
- **Reference** 神农出去：有一个叫神农的人出去，This is the first mention of this character, so introduce him with a noun phrase that says who he is, rather than using only his name.
- **Temporality** 告诉人：告诉了人，This telling is a completed action in the story. In this series of actions, the final verb takes 了.

**Expressiveness**
- After “古代时候，人不知道他们能吃什么植物，常常一吃就死”: You could add the reason that some plants were poisonous, making the danger clearer. For example: 有些植物有毒。
- After “但是不知道为什么，没有办法”: You could add Shen Nong’s thought to show why he decides to test the plants. For example: 神农想：“我要知道什么植物能吃。”

**New Words**
- No suggestions.

**Encouragement** You clearly introduce the problem people faced and explain Shen Nong’s purpose. The contrast between safe and dangerous plants makes his goal easy to understand.

### Scene 2

> 发现有的植物对身体非常好，特别是茶，让肚子感觉又暖和又清楚。他告诉朋友：“你吃哪种植物，这就要看你的口味。比方说，你爱吃甜的，可能喜欢糖。”他最喜欢吃花，除了夹竹桃以外，什么都花想吃。

**Grammar and Vocab Corrections**
- 让肚子感觉又暖和又清楚：让肚子感觉又暖和又舒服，清楚 means “clear” and does not describe how a stomach feels. Use 舒服 to say that the stomach feels comfortable.
- 除了夹竹桃以外，什么都花想吃：除了夹竹桃以外，什么花都想吃，When 什么 modifies 花, it must come before 花. 什么花都 means “every kind of flower.”

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “发现有的植物对身体非常好，特别是茶，让肚子感觉又暖和又清楚”: Add Shennong’s thought that tea could also be used as medicine. For example: 他想：“茶也可以做药。”

**New Words**
- No suggestions.

**Encouragement** You included a specific example, 茶, and described its effect on the stomach. You also used direct speech to make Shennong’s explanation to his friend more lively.

### Scene 3

> 他发现这个口味，一百岁时候，不小心吃了毒的花。一吃就开始死。但是生病时候告诉人什么植物是药，什么植物是毒。

**Grammar and Vocab Corrections**
- 一百岁时候：一百岁的时候，Use 的 before 时候 after an age phrase: 一百岁的时候 means “when [he] was one hundred years old.”
- 吃了毒的花：吃了有毒的花，毒 is a noun meaning “poison.” Use 有毒的 to describe a flower that is poisonous.
- 一吃就开始死：他一吃就开始死了，This sentence needs a subject before the 一……就…… structure. Use 了 because starting to die is a completed change in the story.
- 生病时候告诉人：生病的时候告诉了人，Use 的 in 生病的时候. Use 了 after 告诉 because this is a completed action in the story.
- 什么植物是毒：什么植物有毒，Say a plant 有毒, meaning that it is poisonous. 是毒 would mean that the plant itself is poison.

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “一吃就开始死”: Describe how sick and weak Shennong feels after eating the poisonous flower. For example: 他疼得躺在地上，觉得很难受。
- After “但是生病时候告诉人什么植物是药，什么植物是毒”: Add Shennong’s thought that other people should not make the same dangerous mistake. For example: 他想：别人不能再吃错了。

**New Words**
- No suggestions.

**Encouragement** You clearly show the danger of eating the poisonous flower and then explain Shennong’s helpful purpose. The contrast between medicine and poison is an important part of this scene.

### Content & completeness (after the whole story)

- Missing scene: 神农tried 夹竹桃 and fainted
- Missing scene: a person in blue stopped by and gave灵芝to 神农，神农felt better after eating灵芝
- Missing scene: another person in brown came by and had a conversation with 神农
- Missing scene: 神农takes record of灵芝and夹竹桃
- Wrong information: “他最喜欢吃花，除了夹竹桃以外，什么都花想吃。” -- This says 神农 does not want to eat 夹竹桃, but in the story he tries 夹竹桃.
- Wrong information: “古代时候，人不知道他们能吃什么植物，常常一吃就死。” -- The story says people often became sick after eating some plants, not that they usually died.
- Wrong information: “一吃就开始死。” -- After trying 夹竹桃, 神农 faints in the story; he does not start dying.

## shennong_samples#35

### Scene 1

> 在古代，很多医生不知道怎么用药。所以他们找到了很多植物对药。神农先看到很多病人，他们吃很多植物对药。但是我觉得他们的吃的植物，让他们病人。神农觉得这个植物可能特别是毒。所以他想找一个植物对药，他们可以吃对药。正好，他找到了一把花，他想把花放在茶里，对药。

**Grammar and Vocab Corrections**
- 他们找到了很多植物对药：他们找到了很多能当药的植物，Use 当药 for plants that can be used as medicine. 对药 is not the correct expression here.
- 他们吃很多植物对药：他们把很多植物当药吃了，Say 把植物当药吃, meaning “eat plants as medicine.” 对药 is not used for “as medicine.”
- 但是我觉得他们的吃的植物，让他们病人：但是我觉得他们吃的植物让他们生病了，Use 他们吃的植物, without 的 after 他们. To say that something causes illness, say 让他们生病了.
- 所以他想找一个植物对药，他们可以吃对药：所以他想找一种植物给病人当药吃，Use 当药 to mean “as medicine,” and 一种植物 for one kind of plant. 病人 makes clear who will eat the medicine; 他们 is unclear here.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 神农先看到很多病人：有一个医生叫神农，他先看到了很多病人，When a character appears for the first time, introduce who they are, not only their name. 看见 is a completed event here, so say 看到了.
- **Reference** 这个植物可能特别是毒：有一种植物可能特别有毒，这个植物 is unclear because no particular plant has been introduced yet, so introduce it as 有一种植物. Say 特别有毒, not 特别是毒.
- **Reference** 正好，他找到了一把花，他想把花放在茶里，对药：正好，他找到了一把花，想把花放在茶里做药，When the same person does two actions in one sentence, omit the second 他. Also, use 做药, not 对药, for making medicine.

**Expressiveness**
- After “在古代，很多医生不知道怎么用药”: You could explain that people became ill after eating poisonous plants, showing why this was a serious problem. For example: 很多人吃了有毒的植物，常常生病。
- After “神农先看到很多病人”: You could add Shen Nong’s concern when he saw the sick people. For example: 他觉得很难过，也很担心。

**New Words**
- No suggestions.

**Encouragement** You clearly introduce the problem at the beginning of the story: doctors did not know which plants could be used as medicine. You also show Shen Nong’s goal of finding plants that people could safely use.

### Scene 2

> 他不知道如果这把花对你的身体好，这就要看如果这把花毒不毒了。神农想找别的植物，但是这很麻烦。正好，他找到了别的花。他一吃花，很快就生病了。他的肚子疼死了。神农不知道他吃不吃灵芝或者夹竹桃。

**Grammar and Vocab Corrections**
- 他不知道如果这把花对你的身体好，这就要看如果这把花毒不毒了：他不知道这把花对人的身体好不好，这要看有没有毒，Do not use 如果 after 不知道 or 要看 when asking whether something is true. Use a yes-or-no form such as 好不好 or 有没有毒; 了 is not used for this state question.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 神农不知道他吃不吃灵芝或者夹竹桃：神农不知道该不该吃灵芝或者夹竹桃，The subject is already 神农 in this sentence, so do not repeat it with 他. Use the zero form, and 该不该 shows that he is deciding whether to eat the plants.

**Expressiveness**
- After “正好，他找到了别的花”: You could describe the flower so the reader can picture what Shennong sees. For example: 那朵花是黄色的，像星星一样。
- After “他的肚子疼死了”: You could add Shennong’s fear when the pain becomes very strong. For example: 他想：我会死吗？

**New Words**
- 麻烦 (“但是这很麻烦”)：困难 (“但是这很困难。”)，“困难” more clearly emphasizes that finding other plants is hard to do, while “麻烦” can also mean bothersome.

**Encouragement** You clearly show the cause-and-effect sequence: Shennong eats the flower, then quickly becomes ill and has a stomachache. You also include his uncertainty about whether he ate 灵芝 or 夹竹桃, which gives the scene suspense.

### Scene 3

> 别的人给了神农一个灵芝。这个植物可以让神农更好。比方说，他会觉得更健康。吃灵芝以后，他可以再走。现在他觉得更好。最后，神农找到了很多植物，他可以用对药。这些植物让神农很高兴。神农想跟很多人分享他的新药。

**Grammar and Vocab Corrections**
- 比方说，他会觉得更健康：他会觉得更健康，比方说 means “for example,” but this sentence is not giving an example. It directly states the result, so delete 比方说.
- 最后，神农找到了很多植物，他可以用对药：最后，神农找到了很多植物，可以用来做药，神农 is already the subject in this sentence, so do not repeat 他. 用对药 is not a Chinese verb phrase; 用来做药 means “use them to make medicine.”

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 别的人给了神农一个灵芝：有一个人给了神农一个灵芝，别的人 means people other than a person or group already mentioned, but there is no such person or group here. Introduce this new person with 有一个人.
- **Temporality** 吃灵芝以后：吃了灵芝以后，Eating the lingzhi is completed before the later action of being able to walk again. Use 了 with 吃 to show that the eating has finished.

**Expressiveness**
- After “现在他觉得更好”: You could add Shennong’s thought that he is relieved because he can continue walking and looking for plants. For example: 他想：“我可以再找植物了！”
- After “神农想跟很多人分享他的新药”: You could add a short line of speech to show that he wants to help other people learn which plants are medicine. For example: 他说：“这些植物可以做药！”

**New Words**
- 更好 (“现在他觉得更好”)：好多了 (“现在他觉得好多了。”)，“好多了” more vividly shows that his condition improved a lot after eating the lingzhi.

**Encouragement** You clearly show the sequence of Shennong receiving lingzhi, feeling better, and being able to walk again. You also give the scene a strong ending by showing that he wants to share his new medicine with many people.

### Content & completeness (after the whole story)

- Missing scene: 神农found茶and took a record
- Need to add: The flower is 夹竹桃, and 神农 faints.
- Missing scene: another person in brown came by and had a conversation with 神农
- Missing scene: 神农takes record of灵芝and夹竹桃
- Wrong information: “神农不知道他吃不吃灵芝或者夹竹桃。” -- In the story, 神农 does eat 夹竹桃; it is the plant that makes him faint.

## shennong_samples#42

### Scene 1

> 古代的时候有一个人叫神农。他需要当上医，一看别的人就想帮助他们。但是，他有一个问题，他不知道什么东西能做药。神农听说一个远远的地方有一种植物，什么病人吃都会觉得身体更好。神农三个月走去，找到有植物的地方，他看到一个很漂亮的植物，又香又好看。

**Grammar and Vocab Corrections**
- 神农三个月走去：神农走了三个月，A duration such as 三个月 comes after the action verb. Use 了 with 走 because the three-month journey was completed.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 他有一个问题，他不知道什么东西能做药：他有一个问题，不知道什么东西能做药，The second 他 refers to 神农 again in the same sentence. After the subject has already been mentioned, omit the repeated pronoun.
- **Temporality** 什么病人吃都会觉得身体更好：什么病人吃了都会觉得身体更好，Eating happens before the patient feels better, so 吃 needs 了 to show that this action is completed.
- **Temporality** 找到有植物的地方：找到了有植物的地方，Finding the place is a completed action in the story, so 找到 needs 了.

**Expressiveness**
- After “他看到一个很漂亮的植物，又香又好看”: You could add the flowers’ yellow, star-like appearance to make the place easier to picture. For example: 那儿开着黄色的、像星星一样的花。

**New Words**
- No suggestions.

**Encouragement** You clearly introduce Shennong’s wish to help sick people and the problem he needs to solve. You also give the plant sensory detail by saying that it is fragrant and pretty.

### Scene 2

> 他觉得，这种一定是做药的花。原来他想错了。吃了以后，神农快生病。 这时一个穿着蓝色衣服的人帮神农，快给他一种红的灵芝。神农吃了以后，他没有病，想起来以前一个人告诉他，灵芝对身体有好处。

**Grammar and Vocab Corrections**
- 快给他一种红的灵芝：很快给了他一种红的灵芝，Use 很快, not 快, to mean “quickly” in this statement. Give the last verb in this completed series of actions the particle 了.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 神农吃了以后，他没有病：神农吃了以后，没有病，When the subject is the same within one sentence, Chinese normally omits the repeated pronoun. 神农 is already the subject, so do not add 他.
- **Temporality** 吃了以后，神农快生病：吃了以后，神农很快生病了，很快 means that the action happened soon. Use 了 because getting sick is a completed event in the story.

**Expressiveness**
- After “他觉得，这种一定是做药的花”: You could describe the flower’s yellow, star-like appearance to make the scene more vivid. For example: 花是黄色的，像星星一样。
- After “神农吃了以后，他没有病”: You could add Shennong’s thanks to show his relief after the medicine helps him. For example: 他对那个人说：“谢谢你！”

**New Words**
- 帮 (“一个穿着蓝色衣服的人帮神农”)：救 (“一个穿着蓝色衣服的人救神农”)，“救” is more precise because the man helps Shennong when he is ill.

**Encouragement** You clearly show the important change from thinking the flower was medicine to realizing he was wrong. You also connect the lingzhi to information Shennong had heard before, which makes the story flow well.

### Scene 3

> 啊，他怎么忘记了？他把灵芝放在包里。一回家就告诉别人。他找到药以后他写下怎么做药在书上。所以人们都知道，那红灵芝对身体好处。

**Grammar and Vocab Corrections**
- 他找到药以后他写下怎么做药在书上：他找到药以后，在书上写下了怎么做药，A place phrase with 在 comes before the verb in Chinese, so say 在书上写下. Since the writing was completed, 写下 takes 了.
- 那红灵芝对身体好处：那种红灵芝对身体有好处，Use a measure word such as 种 after 那 when referring to a type of 灵芝. 好处 needs 有 here: 对身体有好处 means “to be good for the body.”

**Coherence: Reference / Temporality / Conjunction**
- Nothing to flag.

**Expressiveness**
- After “他把灵芝放在包里”: You could add Shen Nong’s relieved thought when he remembers that he brought the lingzhi home. For example: 他想：“还好，我把灵芝带回来了。”
- After “一回家就告诉别人”: You could add a short line of speech to show what he tells people about the lingzhi. For example: 他说：“灵芝对身体有好处，可以做药！”

**New Words**
- No suggestions.

**Encouragement** You clearly show the order of events with “一回家就” and use “所以” to explain the result. You also connect this ending well to Shen Nong sharing his discovery with other people.

### Content & completeness (after the whole story)

- Need to add: People do not know which plants are safe to eat, and people get sick after eating some plants.
- Missing scene: 神农found茶and took a record
- Need to add: The plant is 夹竹桃, and 神农 faints after eating it.
- Need to add: A record of both 灵芝 and 夹竹桃, especially 夹竹桃
- Wrong information: “吃了以后，神农快生病。” -- In the story, 神农 eats 夹竹桃 and faints; this changes it to nearly becoming sick after an unnamed plant.

## shennong_samples#49

### Scene 1

> 古代的时候，有很多人不知道什么植物能吃，什么植物不能吃。有很多人吃植物以后就吃坏肚子了，因为他们吃了毒。那个时候，有一个老人叫神农，他什么植物都觉得好吃，不怕生病，不怕毒。他希望别人也可以吃好吃的植物。可是他知道，如果他们还怕吃毒，不会吃他喜欢的植物。

**Grammar and Vocab Corrections**
- 古代的时候：在古代，Use 在古代 to say “in ancient times.” 古代的时候 is not the usual expression here.
- 什么植物能吃，什么植物不能吃：什么植物是能吃的，什么植物是不能吃的，When saying which plants are edible and which are not, use 是能吃的 and 是不能吃的.
- 因为他们吃了毒：因为他们吃的植物有毒，The intended meaning is that the plants they ate were poisonous. Say that the plants have poison, rather than saying they ate poison.
- 他们还怕吃毒：他们还怕中毒，中毒 means “to be poisoned.” 怕吃毒 does not express the intended meaning naturally.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 有一个老人叫神农，他什么植物都觉得好吃：有一个老人叫神农，什么植物都觉得好吃，After introducing 神农 in the same sentence, omit the repeated subject pronoun. The omitted subject still clearly refers to 神农.

**Expressiveness**
- After “他希望别人也可以吃好吃的植物”: You could add Shennong’s thought that everyone should know which plants are safe to eat. For example: 他想：大家应该知道什么植物能吃。
- After “可是他知道，如果他们还怕吃毒，不会吃他喜欢的植物”: You could show his decision to test plants himself so that he can help other people. For example: 所以，他决定自己试一试各种植物。

**New Words**
- No suggestions.

**Encouragement** You clearly explain the problem people faced with plants and give Shennong a kind reason for wanting to help them. The contrast with “可是” also makes his motivation easy to follow.

### Scene 2

> 所以，他上山下山找植物，吃了很多样子的植物。他是第一人，找到了茶。他把所有的植物写下来了。他一直都吃了，他连毒都能吃。可是他还没吃了一个叫夹竹桃的植物。他找到了那个像星星的植物，觉得很漂亮，马上就吃下了。

**Grammar and Vocab Corrections**
- 吃了很多样子的植物：吃了很多种植物，样子 means appearance. Use 种 to count different kinds of plants.
- 他是第一人，找到了茶：他是第一个找到茶的人，To say someone was the first person to do an action, use 第一个 + verb + 的人.
- 他一直都吃了：他一直都在吃，一直 describes an action continuing over time, so use 在 to show the ongoing action. Do not use 了 here.
- 他连毒都能吃：他连有毒的植物都能吃，毒 is poison, not the plant that he eats. Say 有毒的植物 for poisonous plants.
- 可是他还没吃了一个叫夹竹桃的植物：可是他还没吃过一种叫夹竹桃的植物，了 cannot be used after 没. Use 没吃过 to say that he had not tried it, and use 种 for a kind of plant.

**Coherence: Reference / Temporality / Conjunction**
- **Temporality** 找到了那个像星星的植物：找到那个像星星的植物，In this series of actions, only the final action takes 了. The final verb 吃下了 already shows that the actions were completed.

**Expressiveness**
- After “他找到了那个像星星的植物，觉得很漂亮，马上就吃下了”: You could add that the flowers were yellow to make the plant easier to picture. For example: 花是黄色的。

**New Words**
- No suggestions.

**Encouragement** You clearly show Shennong’s active work with the vivid phrase “上山下山找植物.” You also include important story steps: finding tea, writing about plants, and then discovering the star-like plant.

### Scene 3

> 可是夹竹桃的毒很重，让他肚子很痛。他在地上躺着，觉得他快会死了。可是正好有别人找到他了，给了他一个像伞的植物，叫灵芝。他吃灵芝以后就觉得很好，不再生病了。他测量起来了，像星星的植物是毒，像伞的植物是药。

**Grammar and Vocab Corrections**
- 正好有别人找到他了：正好有人找到他，Use 有人 for an unspecified person. 别人 means “other people” and needs a clear group that they are other than.
- 像星星的植物是毒：像星星的植物有毒，Use 有毒 to say that a plant is poisonous. 是毒 is not the usual way to express this.

**Coherence: Reference / Temporality / Conjunction**
- **Reference** 觉得他快会死了：觉得快要死了，The person who feels this is also the person who is about to die, so do not repeat 他 here. Use 快要 to say that something is about to happen.
- **Temporality** 吃灵芝以后：吃了灵芝以后，Eating the lingzhi is completed before the next event, so use 了 with 吃.

**Expressiveness**
- After “可是正好有别人找到他了”: You could describe the helper’s blue clothes to make this person easier for the listener to picture. For example: 那个人穿着蓝色的衣服。
- After “他吃灵芝以后就觉得很好，不再生病了”: You could add a short question from Shennong to show that he wants to learn about the helpful plant. For example: 神农问：“这是什么植物？”

**New Words**
- 痛 (“让他肚子很痛”)：疼 (“让他肚子很疼”)，“疼” is a more natural everyday word for a physical ache in the stomach.

**Encouragement** You clearly show the important cause-and-effect sequence: the oleander hurts Shennong, and lingzhi helps him feel better. You also contrast the star-shaped poisonous plant with the umbrella-shaped medicinal plant well.

### Content & completeness (after the whole story)

- Missing scene: another person in brown came by and had a conversation with 神农
