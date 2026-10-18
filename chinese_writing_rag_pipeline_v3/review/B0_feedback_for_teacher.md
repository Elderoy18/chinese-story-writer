# New feedback system (round B0) -- for review

This round was built only from the basic materials: the graded student stories, the model stories,
the required-scene lists and the coherence rules. None of the comments on earlier AI feedback were
used yet. The corrections of these 20 stories were not available to the system.

Changes from the previous round, following the comments on it:

- Each correction shows the **whole sentence** (clause) before → after, with every error in it fixed,
  so the corrected version should be complete and correct.
- Each error inside a sentence is labelled with its own category (Grammar, Vocabulary, or Coherence:
  Reference / 了着在 / Connectors). There is no Content or Other category among the corrections.
- A correction is shown only if at least two of three independent runs of the system made it.
- Fewer vocabulary suggestions and expressiveness ideas, only where clearly useful.
- The content check lists each missing scene in the wording of the required-scene list.

Each correction can be judged in `B0_labels.csv` (see `B0_labels_instructions.md`).

## mengmu_samples#4

### Scene 1

> 古代的时候，孟子和孟母住了在靠墓地的家。孩子才五岁就每天在墓地祭拜了。在那个城市，孟母从早到晚都找工作，可是找不到，害得孟母没有钱。难怪她跟孩子搬家，原来买不了房。他们搬了到别一个城市找工作。

**Corrections**
- 古代的时候 → 在古代
  - **Vocabulary** 古代的时候 → 在古代: Use 在古代 to mean “in ancient times.”
- 孟子和孟母住了在靠墓地的家 → 孟子和孟母住在靠墓地的家
  - **Coherence: 了 / 着 / 在** 住了在 → 住在: 住 describes a continuing state here, so do not use 了 before 在.
- 孩子才五岁就每天在墓地祭拜了 → 他才五岁就每天在墓地祭拜
  - **Coherence: Reference** 孩子 → 他: 孟子 was just mentioned, so use the pronoun 他 to refer to him again.
  - **Coherence: 了 / 着 / 在** 祭拜了 → 祭拜: 每天 shows a routine action, so use no 了.
- 可是找不到，害得孟母没有钱 → 可是找不到，害得她没有钱
  - **Coherence: Reference** 孟母 → 她: 孟母 was just mentioned, so use 她 when referring to her again.
- 难怪她跟孩子搬家 → 难怪她跟他搬了家
  - **Coherence: Reference** 孩子 → 他: The child is Mengzi, who was mentioned earlier, so use 他 here.
  - **Coherence: 了 / 着 / 在** 搬 → 搬了: This refers to the completed action of moving house, so add 了.
- 他们搬了到别一个城市找工作 → 他们搬到了另一个城市找工作
  - **Coherence: 了 / 着 / 在** 搬了到 → 搬到了: Put 了 after 到 for the completed action: 搬到了.
  - **Vocabulary** 别一个 → 另一个: Use 另一个 to mean “another one.”

**Expressiveness**
- After “在那个城市，孟母从早到晚都找工作，可是找不到，害得孟母没有钱”: Add Meng Mu’s worry to show how the unsuccessful job search affects her. For example: 孟母觉得很着急。
- After “他们搬了到别一个城市找工作”: Add a short line of speech to show Meng Mu’s decision to keep trying. For example: 孟母说：“我们去别的城市找工作吧。”

**Encouragement** You clearly included a sequence of events: Meng Mu looks for work, cannot find it, and then moves with Meng Zi. The reason for the move is easy to follow in your retelling.

### Scene 2

> 这个城市老是很吵，不是人吵架，就是都叫，害得孟子一直不能睡觉。在那儿，孟母也找不到工作。孟子和妈妈要又一个次搬了家。在第三个城市，孟母找到工作，在商店做衣服。

**Corrections**
- 孟子和妈妈要又一个次搬了家 → 孟子和妈妈又搬了一次家
  - **Grammar** delete 要: 要 expresses a future intention, so it cannot be used with the completed action 搬了家 here.
  - **Grammar** 又一个次搬了 → 又搬了一次: Use 搬了一次家 for “moved house once.” 一次 follows the verb.
- 孟母找到工作 → 孟母找到了工作
  - **Coherence: 了 / 着 / 在** 找到 → 找到了: Finding a job is a completed event in the story, so use 了.

**Vocabulary suggestions**
- (suggestion) 叫 (“就是都叫”) → 喊 (“就是都喊”): “喊” more clearly describes people making loud noises or shouting.

**Expressiveness**
- After “在那儿，孟母也找不到工作”: You could add Mengmu’s worried thought about needing to find a quieter place for Mengzi. For example: 孟母想：这里太吵了，我们还是搬家吧。
- After “在第三个城市，孟母找到工作，在商店做衣服”: You could describe one simple detail of the clothes in the shop. For example: 商店里有很多漂亮的衣服。

**Encouragement** You clearly explain why this city is difficult for Mengzi: the noise stops him from sleeping. You also move the story forward by showing that Mengmu finds a job in the third city.

### Scene 3

> 孟子在那个商店也找了到工作，可是不是做衣服的工作，而是喜欢的工作。孟子学习馆学了十五年，他的学习和他的旅行经验很重要，对他很多好处。他是大人的时候，他成为很有名的哲人。

**Corrections**
- 孟子在那个商店也找了到工作 → 孟子在那个商店也找到了工作
  - **Coherence: 了 / 着 / 在** 找了到 → 找到了: 了 comes after the result complement 到. 找到了 marks that he successfully found a job.
- 孟子学习馆学了十五年 → 孟子在学校学了十五年
  - **Grammar** 孟子 → 孟子在: Use 在 before a place to say where an action happens.
  - **Vocabulary** 学习馆 → 学校: 学校 is the usual word for a school. 学习馆 is not the normal word here.
- 他的学习和他的旅行经验很重要，对他很多好处 → 他的学习和他的旅行经验很重要，对他有很多好处
  - **Grammar** 对他 → 对他有: Use 对……有……好处 to say that something has benefits for someone.
- 他是大人的时候，他成为很有名的哲人 → 他长大以后，他成为了很有名的哲人
  - **Vocabulary** 是大人的时候 → 长大以后: 长大以后 is the usual expression for “after growing up.”
  - **Coherence: 了 / 着 / 在** 成为 → 成为了: 成为了 marks the completed change of becoming a famous philosopher.

**Expressiveness**
- After “孟子学习馆学了十五年”: You could describe his daily study to show why those fifteen years mattered. For example: 他每天认真地看书。
- After “他成为很有名的哲人”: You could add how he felt after becoming well known. For example: 他觉得很高兴。

**Encouragement** You clearly show a long path from finding work to studying for fifteen years and becoming a famous philosopher. Including his travel experience also helps explain why he became successful.

### Content & completeness (after the whole story)

- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Need to add: 孟母 and 孟子 moving from the market to a neighborhood near a school is not told; the place is not identified as a school.
- Wrong information: “难怪她跟孩子搬家，原来买不了房。” -- This gives being unable to buy a house as the reason for the move, but 孟母 moves because she worries that copying sacrifices will affect 孟子 badly.

## mengmu_samples#10

### Scene 1

> 孟子小的时候，从早到晚都跟朋友玩。孟子和他的朋友喜欢玩在墓地里，装祭拜。孟子五岁的时候，跟妈妈搬家。他们搬家不是因为孟子玩得太多，而是因为妈妈认为他们的家离墓地太近。

**Corrections**
- 孟子和他的朋友喜欢玩在墓地里，装祭拜 → 孟子和他的朋友喜欢在墓地里玩，装作祭拜
  - **Grammar** 玩在墓地里 → 在墓地里玩: The place phrase 在墓地里 normally comes before the verb 玩.
  - **Grammar** 装 → 装作: Use 装作 before an action to mean “pretend to do something.”

**Expressiveness**
- After “孟子和他的朋友喜欢玩在墓地里，装祭拜”: You could add that the people who came to worship were upset when they saw the children pretending. For example: 来祭拜的人看见了，很生气。
- After “而是因为妈妈认为他们的家离墓地太近”: You could show the mother’s worry by adding her thought that living there might bring more trouble. For example: 妈妈想：住在这儿会有很多麻烦。

**Encouragement** You clearly set the scene with Mengzi’s age and his daily habit of playing with friends. You also used the contrast pattern “不是……而是……” to explain why his mother decided to move.

### Scene 2

> 妈妈认为，住离墓地太近，害得孟子的心气。孟子和孟母搬到子思老师的家，跟子思老师住。孟母帮子思打扫房间和做饭。子思帮孟母教她的儿子。因为孟子现在没有朋友，他老是读书。

**Corrections**
- 妈妈认为，住离墓地太近，害得孟子的心气 → 妈妈认为，住得离墓地太近，影响孟子的心情
  - **Grammar** 住离 → 住得离: Use 得 after 住 to describe the degree of distance: 住得离……太近。
  - **Vocabulary** 害得孟子的心气 → 影响孟子的心情: 心气 does not mean “mood” here. 墓地太近 can 影响 someone’s 心情.

**Expressiveness**
- After “子思帮孟母教她的儿子”: You could add Meng Mu’s happiness because her son now has someone to teach him. For example: 孟母觉得很高兴。
- After “因为孟子现在没有朋友，他老是读书”: You could describe Mengzi beginning to enjoy reading as he spends more time with books. For example: 后来，孟子觉得读书很有意思。

**Encouragement** You clearly explain how Mengzi’s new home changes his daily life. You also include helpful details about Meng Mu and Zisi taking care of the home and teaching Mengzi.

### Scene 3

> 子思认为，对孩子来说，读书最重要，特别是学哲学。孟子不是练习写文章，就是看哲学书。孟子从五岁一直学哲学。他才五岁就学哲学，难怪他成为很有名的哲学家。

**Corrections**
- 他才五岁就学哲学，难怪他成为很有名的哲学家 → 他才五岁就学哲学，难怪他成为了很有名的哲学家
  - **Coherence: 了 / 着 / 在** 成为 → 成为了: Becoming a famous philosopher is a completed result, so use 了.

**Vocabulary suggestions**
- (suggestion) 重要 (“读书最重要”) → 关键 (“读书最关键”): “关键” makes the idea stronger: reading is the thing that matters most for a child.
- (suggestion) 看 (“看哲学书”) → 读 (“读哲学书”): “读” is more precise than “看” when talking about reading books.

**Expressiveness**
- After “孟子不是练习写文章，就是看哲学书”: You could show Mengzi’s careful attitude while he studies. For example: 他每天都认真地读书。

**Encouragement** You clearly show that Mengzi spends a lot of time studying philosophy. The pattern “不是……就是……” is a strong way to describe his daily routine.

### Content & completeness (after the whole story)

- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Need to add: They move from the market to a neighborhood near a school.
- Wrong information: “孟子和孟母搬到子思老师的家，跟子思老师住。” -- The story has them move to a neighborhood near a school, not to 子思老师's home to live with him; 子思老师 is not part of the required story.
- Wrong information: “孟母帮子思打扫房间和做饭。” -- 子思 and this work for him are not part of the story.
- Wrong information: “子思帮孟母教她的儿子。” -- 子思 is not part of the story; 孟子 begins studying after the move near the school.

## mengmu_samples#12

### Scene 1

> 古代，孟子跟孟母住在墓地的旁边。可是孟母注意，住在墓地的旁边影响孟子。他常常跟朋友们祭拜玩，所以孟母决定他们会搬家。这次，他们住在城市里的商店的旁边，从早到晚很吵。

**Corrections**
- 可是孟母注意，住在墓地的旁边影响孟子 → 孟母注意到，住在墓地的旁边影响孟子
  - **Coherence: Connectors** delete 可是: 可是 means “but” and needs a contrast with the previous clause. There is no contrast here.
  - **Grammar** 注意 → 注意到: Use 注意到 when someone notices a fact or situation.
- 他常常跟朋友们祭拜玩，所以孟母决定他们会搬家 → 他常常跟朋友们玩祭拜的游戏，所以孟母决定搬家
  - **Grammar** 祭拜玩 → 玩祭拜的游戏: Use 玩 + activity + 的游戏 to say that children play a game involving an activity.
  - **Grammar** delete 他们会: 决定 is followed by the action that is decided. Say 决定搬家, not 决定他们会搬家.

**Vocabulary suggestions**
- (suggestion) 吵 (“从早到晚很吵”) → 热闹 (“从早到晚很热闹”): “吵” focuses on unpleasant noise, while “热闹” better describes the busy market atmosphere in this setting.

**Expressiveness**
- After “这次，他们住在城市里的商店的旁边，从早到晚很吵”: Add a detail about the many merchants selling things to show why the area is so busy. For example: 很多商人卖各种各样的东西。

**Encouragement** You clearly set the story in ancient times and introduced Mengzi and his mother’s first home. You also included the move to the busy city area, which moves the story forward well.

### Scene 2

> 城市也有点儿危险。害得孟母只好一直陪孟子。孟子也没有朋友，难怪他老是看起来不高兴。住在商店的旁边不是适合孟子，而是让他觉得很伤心。

**Corrections**
- 住在商店的旁边不是适合孟子，而是让他觉得很伤心 → 住在商店的旁边不适合孟子，也让他觉得很伤心
  - **Grammar** 不是适合 → 不适合: 适合 is a verb, so use 不 directly before it. Do not use 是 here.
  - **Coherence: Connectors** 而是 → 也: 而是 introduces an alternative after a negation. Here both “not suitable” and “makes him sad” are true, so use 也.

**Expressiveness**
- After “害得孟母只好一直陪孟子”: Add Meng Mu’s worried thought that the noisy environment may make it hard for Meng Zi to study. For example: 孟母想：“这里太吵了，孟子没法儿好好学习。”
- After “孟子也没有朋友”: Add a small visual detail to show what Meng Zi does when he is alone. For example: 孟子常常一个人坐在家里，看着外面的商店。

**Encouragement** You clearly explain why Meng Mu is worried and connect Meng Zi having no friends with his unhappy feelings. Your use of “害得” also shows a good cause-and-effect link.

### Scene 3

> 所以，孟母和孟子搬到学校的旁边住。才五岁孟子开始学哲学。在学校，孟子不是看书，就是练习写字。将来，他成为中国的一个非常有名的哲学家。

**Corrections**
- 才五岁孟子开始学哲学 → 孟子才五岁就开始学哲学
  - **Grammar** 才五岁孟子开始 → 孟子才五岁就开始: Put the subject before 才五岁. 才...就... expresses that he started unusually early.
- 将来，他成为中国的一个非常有名的哲学家 → 后来，他成为中国的一个非常有名的哲学家
  - **Coherence: Connectors** 将来 → 后来: 将来 means the future. For a later event in a past historical story, use 后来.

**Expressiveness**
- After “所以，孟母和孟子搬到学校的旁边住”: Add that Meng Mu feels relieved because the school environment can help Mengzi learn. For example: 孟母觉得很放心。
- After “在学校，孟子不是看书，就是练习写字”: Add that Mengzi enjoys studying in this new environment. For example: 他觉得学习很有意思。

**Encouragement** You clearly show the final move to the school and explain how Mengzi’s daily activities changed there. Your use of “不是……就是……” gives the scene a nice sense of his regular study routine.

### Content & completeness (after the whole story)

- Need to add: 孟子 imitating buying and selling every day

## mengmu_samples#18

### Scene 1

> 古代的时候，有一个男孩名字叫孟子。孟子和孟子的妈妈两个人住在很穷的农村。他们住的地方旁边是个墓地，墓地老是有很多人祭拜。因为人们在祭拜，他们一直在哭。孟子和孟子的妈妈住在这里才一个星期就觉得受不了了，而且害得孟子的学习。

**Corrections**
- 古代的时候，有一个男孩名字叫孟子 → 在古代，有一个男孩名字叫孟子
  - **Grammar** 古代的时候 → 在古代: Use 在古代 to introduce the time period in this story.
- 孟子和孟子的妈妈住在这里才一个星期就觉得受不了了，而且害得孟子的学习 → 孟子和孟子的妈妈在这里才住了一个星期就觉得受不了了，而且影响了孟子的学习
  - **Coherence: 了 / 着 / 在** 住在这里才一个星期 → 在这里才住了一个星期: Use 了 after 住 to show that the one-week stay was completed before they felt they could not bear it.
  - **Grammar** 害得孟子的学习 → 影响了孟子的学习: 害得 needs a following result complement. 影响了 can directly take 孟子的学习 as its object.

**Expressiveness**
- After “因为人们在祭拜，他们一直在哭”: You could describe the mourners’ expressions to make the cemetery feel more vivid. For example: 人们的脸上都很伤心。
- After “孟子和孟子的妈妈住在这里才一个星期就觉得受不了了，而且害得孟子的学习”: You could add Mengzi’s mother’s worried thought about his learning. For example: 孟子的妈妈想：住在这里会影响孟子的学习。

**Encouragement** You clearly introduced the setting near a cemetery and explained why it was unpleasant for Mengzi and his mother. You also connected the environment to Mengzi’s learning, which helps show why they wanted to move.

### Scene 2

> 孟子的妈妈觉得孟子取得良好的教育是很重要的，所以孟子的妈妈认为这样的地方对儿子的教育不太好，就打算跟孟子搬家。孟子的妈妈带孟子不是搬到城市，而是搬到了孟子老师的家。

**Corrections**
- 孟子的妈妈觉得孟子取得良好的教育是很重要的，所以孟子的妈妈认为这样的地方对儿子的教育不太好，就打算跟孟子搬家 → 孟子的妈妈觉得孟子接受良好的教育是很重要的，所以她认为这样的地方对儿子的教育不太好，就打算跟孟子搬家
  - **Vocabulary** 取得 → 接受: We say 接受教育, not 取得教育. 接受 means “receive” education.
  - **Coherence: Reference** 孟子的妈妈 → 她: Use a pronoun for a close re-mention of the same person.
- 孟子的妈妈带孟子不是搬到城市 → 孟子的妈妈带孟子不是搬到城市，而是搬到了孟子老师的家
  - **Grammar** 带 → 带着: Use 着 after 带 to show that Mother moved together with Mencius.

**Expressiveness**
- After “孟子的妈妈觉得孟子取得良好的教育是很重要的，所以孟子的妈妈认为这样的地方对儿子的教育不太好，就打算跟孟子搬家”: Add the mother’s worry and a short line of speech to show how strongly she feels about her son’s learning. For example: 孟子的妈妈很着急，她说：“我得再搬一次家。”

**Encouragement** You clearly explain the mother’s reason for wanting to move: she cares about Mencius receiving a good education. You also use the contrast pattern “不是……而是……” to show where they moved.

### Scene 3

> 孟子跟他的老师从早到晚学习，难怪他的成绩很快就进步了很多。孟子学习的时候，孟子的妈妈不是待在家里就是编织衣服赚钱。以后孟子成为了中国有名的哲学家。

**Corrections**
- *No corrections.*

**Vocabulary suggestions**
- (suggestion) 进步 (“成绩很快就进步了很多”) → 提高 (“成绩很快就提高了很多”): 提高 is more precise when you are specifically talking about grades improving.

**Expressiveness**
- After “孟子跟他的老师从早到晚学习”: You could show his mother’s happy reaction when she sees that he is studying seriously. For example: 孟子的妈妈看见他认真学习，心里很高兴。
- After “以后孟子成为了中国有名的哲学家”: You could add that people connected his success with his mother’s three moves. For example: 人们都说，他的成功离不开妈妈三次搬家。

**Encouragement** You clearly show the result of Mengzi’s hard work by linking his all-day studying to his quickly improved grades. Your use of “难怪” makes the cause-and-effect relationship especially clear.

### Content & completeness (after the whole story)

- Need to add: 孟子 himself imitates how to offer sacrifices.
- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Need to add: The move from the market to a neighborhood near a school.
- Wrong information: “孟子的妈妈带孟子不是搬到城市，而是搬到了孟子老师的家。” -- The story has them move near the market after the graveyard, and later move from the market to a neighborhood near a school; they do not move to 孟子老师's home.

## mengmu_samples#25

### Scene 1

> 这是古代的故事。孟子小的时候，他的爸爸很早就去世了。从他的家到墓地很近，所以他每天老是从早到晚去墓地跟朋友们玩玩儿。

**Corrections**
- 所以他每天老是从早到晚去墓地跟朋友们玩玩儿 → 所以他每天老是从早到晚去墓地跟朋友们玩儿
  - **Grammar** 玩玩儿 → 玩儿: Verb reduplication (玩玩儿) suggests doing something briefly or casually. It does not fit an action lasting from morning to evening.

**Expressiveness**
- After “所以他每天老是从早到晚去墓地跟朋友们玩玩儿”: You could add that he watched people paying respects at the cemetery and found it interesting. For example: 他看到很多人在墓地祭拜，觉得很有趣。

**Encouragement** You clearly set the story in ancient times and introduced Mencius’s family situation. You also used “所以” well to connect the home’s location with his daily visits to the cemetery.

### Scene 2

> 他的妈妈觉得在墓地玩儿，害得，所以他们搬家。搬家对孟子有好的影响，他才五岁，可是每天不是写字就是帮妈妈的工作。

**Corrections**
- 他的妈妈觉得在墓地玩儿，害得，所以他们搬家 → 他的妈妈觉得在墓地玩儿不好，所以他们搬家
  - **Vocabulary** 害得 → 不好: 害得 must introduce a harmful result. Use 不好 to express that playing in a cemetery is not good.
- 搬家对孟子有好的影响，他才五岁，可是每天不是写字就是帮妈妈的工作 → 搬家对孟子有好的影响，他才五岁，可是每天不是写字就是帮妈妈工作
  - **Grammar** delete 的: 帮妈妈工作 means “help Mother work.” Do not use 的 before 工作 in this verb phrase.

**Expressiveness**
- After “他的妈妈觉得在墓地玩儿，害得，所以他们搬家”: You could show that his mother was worried about what Mengzi was learning from the cemetery environment. For example: 妈妈很担心孟子会学坏。
- After “搬家对孟子有好的影响，他才五岁，可是每天不是写字就是帮妈妈的工作”: You could add his mother’s happy reaction when she sees him studying seriously. For example: 妈妈看到他认真学习，很高兴。

**Encouragement** You clearly connect the move to its effect on Mengzi. You also use a daily-habit pattern, “每天不是……就是……,” to make this part of the story more specific.

### Scene 3

> 他很聪明的人，难怪他成为有名的人。

**Corrections**
- 他很聪明的人 → 他是很聪明的人
  - **Grammar** 他很聪明的人 → 他是很聪明的人: A noun phrase such as “很聪明的人” needs 是 after the subject.

**Expressiveness**
- After “难怪他成为有名的人”: You could add a short reaction from other people to make his fame feel more vivid. For example: 大家都说：“孟子真聪明！”

**Encouragement** You clearly connect Mengzi’s intelligence with his later success. Using “难怪” also gives the ending a strong evaluative conclusion.

### Content & completeness (after the whole story)

- Need to add: 孟子 imitating how to offer sacrifices.
- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Missing scene: 孟母 moved from the market to the neighborhood near a school, 孟子started to study every day
- Wrong information: “从他的家到墓地很近，所以他每天老是从早到晚去墓地跟朋友们玩玩儿。” -- At the graveyard, 孟子 should imitate offering sacrifices, not play with friends.
- Wrong information: “他的妈妈觉得在墓地玩儿，害得，所以他们搬家。” -- 孟母 moves because she worries that 孟子's imitation of sacrifices will affect him badly, not because playing in the graveyard is harmful.

## mengmu_samples#32

### Scene 1

> 有一天孟子去了墓地玩儿，但是他妈妈觉得这是不合适的地方让孩子玩，所以她决定了他们会搬家找更好的地方。她恐怕儿子的童年不会幸福，而且住在这儿教育不太好。因为她望子成龙，所以她会一直搬家才能找到质量好的教育。然后他们搬到了离城市更近的地方。

**Corrections**
- 但是他妈妈觉得这是不合适的地方让孩子玩 → 但是他妈妈觉得这是不适合孩子玩的地方
  - **Vocabulary** 不合适的地方让孩子玩 → 不适合孩子玩的地方: Use 不适合 + person + verb to say that a place is unsuitable for someone to do something.
- 所以她决定了他们会搬家找更好的地方 → 所以她决定搬家找更好的地方
  - **Coherence: 了 / 着 / 在** 决定了 → 决定: 决定 is a mental-state verb, so it normally takes no 了 here.
  - **Grammar** delete 他们会: After 决定, use the action directly: 决定搬家.

**Expressiveness**
- After “所以她决定了他们会搬家找更好的地方”: You could add a short line of speech to show the mother’s determination to find a better environment for Mencius. For example: 她说：“我得给孟子找一个更好的地方。”
- After “然后他们搬到了离城市更近的地方”: You could describe the busy new neighborhood to make the move feel more vivid. For example: 那里有很多商人卖东西，街上很热闹。

**Encouragement** You clearly explain the mother’s reason for moving, using a logical sequence with “所以” and “因为.” Your use of “望子成龙” effectively shows her hopes for her son’s future.

### Scene 2

> 他们住才一月就又搬家。古代的时候，一般人不喜欢卖东西的人。但是孟子老是跟这些卖东西的人常常玩儿，害得妈妈着急得很，因为她恐怕儿子会成为跟他们很像。她告诉了孟子：他们不是朋友，而是不好的人。

**Corrections**
- 他们住才一月就又搬家 → 他们才住了一个月就又搬家了
  - **Coherence: 了 / 着 / 在** 住才 → 才住了: Put 才 before the verb in this duration pattern. Use 了 for the completed period of living there.
  - **Grammar** 一月 → 一个月: Months need the measure word 个 here.
  - **Coherence: 了 / 着 / 在** 搬家 → 搬家了: In a sequence of completed actions, the final action takes 了.
- 古代的时候 → 在古代
  - **Grammar** 古代的时候 → 在古代: Use 在古代 to mean “in ancient times.”
- 但是孟子老是跟这些卖东西的人常常玩儿 → 但是孟子老是跟他们玩儿
  - **Coherence: Reference** 这些卖东西的人 → 他们: The sellers were just mentioned, so use the pronoun 他们 to refer back to them.
  - **Grammar** delete 常常: 老是 and 常常 both mean “often”; use only one of them.
- 因为她恐怕儿子会成为跟他们很像 → 因为她恐怕儿子会变得跟他们很像
  - **Vocabulary** 成为 → 变得: 成为 needs a noun after it. Use 变得 before an adjective phrase such as 跟他们很像.
- 她告诉了孟子 → 她告诉孟子
  - **Coherence: 了 / 着 / 在** 告诉了 → 告诉: A saying verb that introduces direct speech normally does not take 了.

**Expressiveness**
- After “但是孟子老是跟这些卖东西的人常常玩儿”: Add that he copied the merchants’ actions, such as taking money, to show why his mother was worried. For example: 他还学着他们收钱。
- After “因为她恐怕儿子会成为跟他们很像”: Add the mother’s thought that this environment could distract Mengzi from studying. For example: 她想：住在这儿会影响他的学习。

**Encouragement** You clearly show the mother’s worry and give a reason for it with “因为”. The phrase “害得妈妈着急得很” also makes the consequence of Mengzi’s behavior easy to understand.

### Scene 3

> 你不是当数学家，而是当哲学家，不能当卖东西的人。所以他们又搬家。在他们第三个家，孟子学了怎么祭拜。妈妈感觉这个地方适合他们，告诉了孟子：我们找到了最后的家。在这儿妈妈让儿子从早到晚学习，他难怪成为有名的哲学家。

**Corrections**
- 所以他们又搬家 → 所以他们又搬家了
  - **Coherence: 了 / 着 / 在** 又搬家 → 又搬家了: This is a completed move in the story, so add 了 at the end.
- 在他们第三个家 → 在他们的第三个家
  - **Grammar** 他们第三个家 → 他们的第三个家: Use 的 between a possessive pronoun and a numbered noun phrase.

**Vocabulary suggestions**
- (suggestion) 感觉 (“妈妈感觉这个地方适合他们”) → 觉得 (“妈妈觉得这个地方适合他们”): “觉得” is more natural for expressing a personal opinion, while “感觉” often focuses on a physical feeling or impression.

**Expressiveness**
- After “在他们第三个家，孟子学了怎么祭拜”: Add a detail that the school was close to their new home, showing why the environment helped Mencius learn. For example: 学校就在他们家旁边。
- After “妈妈感觉这个地方适合他们”: Add a short quote to show that his mother was happy with this move. For example: 孟母高兴地说：“这次搬家太对了！”

**Encouragement** You clearly show the mother’s goal for Mencius: she wants him to study and eventually become a philosopher. You also give the story a clear ending by connecting his hard work with his later success.

### Content & completeness (after the whole story)

- Need to add: 孟子 imitating how to offer sacrifices at the graveyard
- Need to add: the market as the new neighborhood and Mencius imitating buying and selling
- Need to add: the school as the new neighborhood
- Wrong information: “有一天孟子去了墓地玩儿” -- At the graveyard, 孟子 imitates offering sacrifices rather than simply going there to play.
- Wrong information: “在他们第三个家，孟子学了怎么祭拜。” -- Learning or imitating sacrifices happens at the graveyard before the family moves away, not in the third home after the moves.

## mengmu_samples#33

### Scene 1

> 一天，很久很久以前，孟子和他妈妈住在中国。孟子妈妈的工作是祭拜，孟子不高兴，因为他说我们老是搬家，为什么？他妈妈说，从早到晚，我一直祭拜，很多墓地得我祭拜。所以我们得去很多不同的地方。

**Corrections**
- *No corrections.*

**Vocabulary suggestions**
- (suggestion) 不高兴 (“孟子不高兴”) → 烦 (“孟子很烦”): “烦” more vividly shows that he is annoyed by having to move again and again.

**Expressiveness**
- After “孟子不高兴，因为他说我们老是搬家，为什么”: He could add that Mengzi misses having one stable home. For example: 孟子说：“我想一直住在一个家。”
- After “他妈妈说，从早到晚，我一直祭拜，很多墓地得我祭拜”: He could describe the cemetery with a simple visual detail. For example: 墓地里有很多墓碑。

**Encouragement** You clearly show Mengzi’s unhappiness and give a reason for it with “因为.” You also use dialogue to make the scene more lively.

### Scene 2

> 孟子想，难怪我们常常搬家，原来我妈妈很忙。可是常常搬家害得孟子很难找到朋友。每次搬家孟子也觉得新的地方不是太热就是太冷，不是太大就是太小。在哪的地方，他都不高兴。孟子想帮助妈妈祭拜，可是他六岁，所以不能祭拜。

**Corrections**
- 在哪的地方 → 在哪儿
  - **Grammar** 在哪的地方 → 在哪儿: Use 在哪儿 to mean “where.” 哪的地方 is not a grammatical way to ask or refer to a place.

**Vocabulary suggestions**
- (suggestion) 很难 (“很难找到朋友”) → 不容易 (“不容易找到朋友”): “不容易” sounds more natural for saying that making friends is difficult because of frequent moving.

**Expressiveness**
- After “可是常常搬家害得孟子很难找到朋友”: Add how Mengzi feels when he has to leave friends behind. For example: 他觉得很孤单。
- After “孟子想帮助妈妈祭拜，可是他六岁，所以不能祭拜”: Add a short thought showing that he wants to be useful to his mother. For example: 他想：“我也想帮妈妈。”

**Encouragement** You clearly show Mengzi’s thoughts and explain why frequent moving is difficult for him. The paired pattern “不是太热就是太冷，不是太大就是太小” adds vivid detail about how he feels about each new place.

### Scene 3

> 四年后，孟子开始帮妈妈祭拜。他画画很厉害，他越来越喜欢祭拜，所以他祭拜不是想帮妈妈工作，而是他很喜欢画画。孟子成为很著名的古代画家。今天很多中国人很喜欢孟子。

**Corrections**
- 他越来越喜欢祭拜，所以他祭拜不是想帮妈妈工作，而是他很喜欢画画 → 他越来越喜欢祭拜，所以他祭拜不是想帮妈妈工作，而是很喜欢画画
  - **Coherence: Reference** delete 他: The subject is already clear from the first part of the sentence. Do not repeat it after 而是 when it is the same person.

**Expressiveness**
- After “他画画很厉害”: You could add how Mengzi feels when he draws, to show why he enjoys helping with the rituals. For example: 他觉得画画很有意思，也很高兴。
- After “孟子成为很著名的古代画家”: You could add a short thought showing that his success comes from his enjoyment of drawing. For example: 孟子想：“我很喜欢画画。”

**Encouragement** You clearly show the time change with “四年后” and explain Mengzi’s motivation with “不是……而是……”. The ending also gives his story a clear result: he becomes a famous painter.

### Content & completeness (after the whole story)

- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Missing scene: 孟母 moved from the market to the neighborhood near a school, 孟子started to study every day
- Need to add: 孟子 becomes a famous philosopher, not a painter.
- Wrong information: “孟子成为很著名的古代画家。” -- 孟子 becomes a famous philosopher, not an ancient painter.

## mengmu_samples#39

### Scene 1

> 古代的时候人觉得祭拜非常重要，孟子很小的时候，从早到晚一直祭拜，因为他妈妈告诉他祭拜很重要。虽然他没有朋友，因为每天只祭拜。他的同学们老是对他开玩笑了。孟子妈妈看了他的同学们对孟子不好的影响，所以孟子和孟子妈妈搬家了。

**Corrections**
- 虽然他没有朋友 → 他没有朋友
  - **Coherence: Connectors** delete 虽然: 虽然 normally needs a contrasting result such as 但是 or 可是. Here the following clause gives a reason, so 虽然 should be deleted.
- 他的同学们老是对他开玩笑了 → 他的同学们老是对他开玩笑
  - **Coherence: 了 / 着 / 在** delete 了: 老是 describes a habitual action. Habitual actions normally use no aspect particle.
- 孟子妈妈看了他的同学们对孟子不好的影响 → 孟子妈妈看到了他的同学们对他的不好的影响
  - **Grammar** 看了 → 看到了: Use 看到 to say that someone perceived or noticed an effect.
  - **Coherence: Reference** 孟子 → 他: 孟子 has just been referred to as 他, so use the close pronoun instead of repeating the name.
- 所以孟子和孟子妈妈搬家了 → 孟子和孟子妈妈搬家了
  - **Coherence: Connectors** delete 所以: The previous action already leads directly to this one, so 所以 is unnecessary here.

**Vocabulary suggestions**
- (suggestion) 一直 (“从早到晚一直祭拜”) → 不停 (“从早到晚不停地祭拜”): “不停地” makes the repeated action feel more continuous and vivid.

**Expressiveness**
- After “古代的时候人觉得祭拜非常重要”: You could describe that Mencius copied the people he saw performing the rituals. For example: 孟子学着别人祭拜。
- After “他的同学们老是对他开玩笑了”: You could add Mencius’s feeling when his classmates made fun of him. For example: 孟子觉得很难过。

**Encouragement** You clearly explain why Mencius spent so much time performing rituals and connect this to his mother’s decision to move. You also include the classmates’ influence, which gives this scene a clear problem.

### Scene 2

> 孟子才十一岁，成为一个哲学家。孟子不是祭拜，而是看政治文章，难怪他成为了哲学家。不过，看过很多政治文章对他害得，他有很多问题。

**Corrections**
- 不过，看过很多政治文章对他害得，他有很多问题 → 不过，看过很多政治文章对他有害，他有很多问题
  - **Vocabulary** 害得 → 有害: 有害 means “harmful.” 害得 must be followed by a result or complement.

**Expressiveness**
- After “不过，看过很多政治文章对他害得，他有很多问题”: You could show one of Mengzi’s thoughts to make his many questions feel more personal. For example: 他常常想：“为什么会这样？”

**Encouragement** You clearly stated the important ending that Mengzi became a philosopher. You also used “难怪” to connect his reading with his later success.

### Scene 3

> 他一直问问题，但是不能解决那些问题。孟子长大，他开始能解决问题。他常常建议你不是学金融，而是学政治，因为如果你懂政治，你会成为高薪。后来孟子成为教授，他教学生很厉害。

**Corrections**
- 孟子长大，他开始能解决问题 → 孟子长大了，他开始能解决问题
  - **Coherence: 了 / 着 / 在** 长大 → 长大了: Growing up is completed before he begins to solve problems, so use 了.
- 他常常建议你不是学金融，而是学政治，因为如果你懂政治，你会成为高薪 → 他常常建议你不要学金融，而是学政治，因为如果你懂政治，你会有高薪
  - **Grammar** 不是学金融 → 不要学金融: After 建议, use 不要 to advise someone not to do something.
  - **Vocabulary** 成为高薪 → 有高薪: 高薪 means a high salary. A person can have a high salary, but cannot become a high salary.

**Expressiveness**
- After “后来孟子成为教授，他教学生很厉害”: Describe how the students respond to show why he is such a good teacher. For example: 学生都认真听他讲课。

**Encouragement** You clearly show Mengzi’s progress from asking questions without answers to being able to solve them. You also give the scene a clear ending by explaining that he becomes a skilled professor.

### Content & completeness (after the whole story)

- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Need to add: The move from the market to a neighborhood near a school, and that 孟子 studies every day.
- Wrong information: “孟子妈妈看了他的同学们对孟子不好的影响，所以孟子和孟子妈妈搬家了。” -- The story says 孟母 moved because she thought 孟子 copying sacrifices would have a bad influence, not because of his classmates.

## mengmu_samples#45

### Scene 1

> 古代的时候，一个男孩子跟他的妈妈住在中国。他叫孟子。他们住在墓地的旁边，所以孟子老是祭拜。孟子不是祭拜，就是跟朋友聊天。他很喜欢他的城市，但是城市有才两个学校，都很小。

**Corrections**
- 古代的时候 → 在古代
  - **Grammar** 古代的时候 → 在古代: Use 在古代 to introduce the historical time setting.
- 他叫孟子 → 叫孟子
  - **Coherence: Reference** delete 他: The same subject continues from the previous sentence, so the pronoun can be omitted.
- 他很喜欢他的城市，但是城市有才两个学校，都很小 → 他很喜欢他的城市，但是城市才有两个学校，都很小
  - **Grammar** 有才 → 才有: 才 comes before 有: 才有两个学校 means “there are only two schools.”

**Vocabulary suggestions**
- (suggestion) 男孩子 (“一个男孩子”) → 小男孩 (“一个小男孩”): “小男孩” is more specific and vivid because it clearly shows that Mencius is young.

**Expressiveness**
- After “所以孟子老是祭拜”: You could add that he found the activity interesting, which helps explain why he copied it so often. For example: 他觉得祭拜很有趣。
- After “孟子不是祭拜，就是跟朋友聊天”: You could describe his behaviour while copying the worshippers to make the scene more vivid. For example: 他一边祭拜一边笑。

**Encouragement** You clearly introduce Mencius, his mother, and their home beside the cemetery. You also use “不是……就是……” to show what he often did.

### Scene 2

> 他的妈妈不是不喜欢他们的城市，而是想孟子有很好的教育。他们搬家到有很多学校的城市。他们从早到晚走路，孟子一直抱怨。

**Corrections**
- 他的妈妈不是不喜欢他们的城市，而是想孟子有很好的教育 → 他的妈妈不是不喜欢他们的城市，而是想让孟子接受很好的教育
  - **Grammar** 想 → 想让: Use 想让 + person + verb to say that someone wants another person to do something.
  - **Vocabulary** 有 → 接受: We usually say 接受教育 (“receive an education”), not 有教育.

**Expressiveness**
- After “他们搬家到有很多学校的城市”: You could describe how the new city feels busy because it has many schools. For example: 那个城市很热闹，有很多学生。
- After “孟子一直抱怨”: You could add a short line of speech to show what Mengzi complains about during the walk. For example: 孟子说：“妈妈，我走不动了！”

**Encouragement** You clearly explain the mother’s positive reason for moving: she wants Mengzi to have a good education. You also add Mengzi’s reaction to the move, which makes the scene more lively.

### Scene 3

> 他难怪抱怨，他想他的朋友，因为他不要离开他的城市。他的妈妈找到孟子一个老师。跟老师孟子学最重要的文学，所以他成为哲学家。

**Corrections**
- 他难怪抱怨 → 难怪他抱怨
  - **Grammar** 他难怪 → 难怪他: 难怪 normally comes before the person and action it explains.
- 因为他不要离开他的城市 → 因为他不想离开他的城市
  - **Vocabulary** 不要 → 不想: 不想 means “do not want to.” 不要 is usually used for commands or refusals.
- 他的妈妈找到孟子一个老师 → 他的妈妈给孟子找到了一个老师
  - **Grammar** 妈妈 → 妈妈给: Use 给 to show that the teacher is found for 孟子.
  - **Coherence: 了 / 着 / 在** 找到 → 找到了: 了 marks that the mother completed the action of finding a teacher.
- 跟老师孟子学最重要的文学 → 孟子跟老师学最重要的文学
  - **Grammar** 跟老师孟子 → 孟子跟老师: The subject 孟子 should come before 跟老师.
- 所以他成为哲学家 → 所以后来他成为哲学家
  - **Coherence: Connectors** 所以 → 所以后来: 后来 shows that becoming a philosopher happened after his period of study.

**Encouragement** You clearly explain why Mencius complains: he misses his friends and does not want to leave his city. You also give the story a clear ending by showing that learning with a teacher leads to him becoming a philosopher.

### Content & completeness (after the whole story)

- Missing scene: 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day
- Need to add: They move from the market neighborhood to a neighborhood near a school.
- Wrong information: “他的妈妈不是不喜欢他们的城市，而是想孟子有很好的教育。” -- This gives a different reason for the move. In the story, 孟母 moves away from the graveyard because she thinks 孟子 copying sacrifices will affect him badly.

## mengmu_samples#47

### Scene 1

> 这个男孩子叫孟子，孟子是古代的人。孟子的妈妈觉得住在哪儿对童年很重要，所以他们常常搬了家。她望子成龙，所以孟子的妈妈安排他的生活。

**Corrections**
- 孟子的妈妈觉得住在哪儿对童年很重要，所以他们常常搬了家 → 孟子的妈妈觉得住在哪儿对童年很重要，所以他们常常搬家
  - **Coherence: 了 / 着 / 在** 搬了家 → 搬家: 常常 describes a habitual action, so use the zero aspect form rather than 了.
- 她望子成龙，所以孟子的妈妈安排他的生活 → 她望子成龙，所以她安排他的生活
  - **Coherence: Reference** 孟子的妈妈 → 她: The mother has just been mentioned as 她, so use the pronoun again for this close reference.

**Vocabulary suggestions**
- (suggestion) 男孩子 (“这个男孩子叫孟子”) → 小男孩 (“这个小男孩叫孟子”): “小男孩” is a more natural and vivid way to introduce a young child in this story.

**Expressiveness**
- After “她望子成龙，所以孟子的妈妈安排他的生活”: You could add the mother's hope that Mengzi would grow up in a good environment for learning. For example: 她希望孟子在一个适合学习的地方长大。

**Encouragement** You clearly introduce Mengzi and explain his mother's important goal for him. Using “望子成龙” shows that you understand why she cared so much about his environment.

### Scene 2

> 因为他们常常搬了家，中国人说，孟母三迁。孟子没有爸爸，所以，他的妈妈更重要。从这儿到那儿，妈妈教孟子很多技能。先她让孟子跟朋友玩儿，然后教他怎么买又便宜又好质量的东西。

**Corrections**
- 因为他们常常搬了家 → 因为他们常常搬家
  - **Coherence: 了 / 着 / 在** 搬了家 → 搬家: 常常 describes a repeated routine, so use the verb without 了.
- 先她让孟子跟朋友玩儿，然后教他怎么买又便宜又好质量的东西 → 她先让孟子跟朋友玩儿，然后教了他怎么买又便宜又质量好的东西
  - **Grammar** 先她 → 她先: The subject comes before 先: 她先让……
  - **Coherence: 了 / 着 / 在** 教他 → 教了他: In a sequence of completed actions, the last action takes 了.
  - **Grammar** 又便宜又好质量的东西 → 又便宜又质量好的东西: Use 质量好 to describe an item's quality; it comes after 又 in this parallel description.

**Expressiveness**
- After “因为他们常常搬了家，中国人说，孟母三迁”: You could add that people later praised Mengzi’s mother for teaching her child well. For example: 后来，人们都说孟母很会教孩子。
- After “从这儿到那儿，妈妈教孟子很多技能”: You could include the mother’s hope that Mengzi would learn useful things in each new place. For example: 她希望孟子学到有用的东西。

**Encouragement** You clearly introduce the main characters and explain why Mengzi’s mother matters. You also connect the repeated moves to the well-known phrase “孟母三迁,” which gives your retelling a strong cultural focus.

### Scene 3

> 最后，她让孟子学写作。他不是写作就是看书，难怪他很聪明。现在在中国，孟子很有名。

**Corrections**
- 最后，她让孟子学写作 → 最后，她让孟子学写作了
  - **Coherence: 了 / 着 / 在** 写作 → 写作了: This is the last action in a completed series, so use 了 to mark completion.

**Expressiveness**
- After “最后，她让孟子学写作”: You could add Mengzi’s mother’s happy reaction when she sees him studying. For example: 孟子的妈妈看见他学习，很高兴。

**Encouragement** You clearly show how Mengzi’s daily reading and writing led to his intelligence. Your final sentence also connects his childhood learning to his lasting fame in China.

### Content & completeness (after the whole story)

- Missing scene: 孟子and孟母lived near a graveyard, and 孟子 imitated how to offer sacrifices every day
- Need to add: the move to a neighborhood near the market
- Need to add: 孟母 moving from the market to a neighborhood near a school

## shennong_samples#4

### Scene 1

> 古代的时候，有一个男人，他的名字是神农。他看到了有很多人不知道哪个植物好吃，也不知道什么植物对你的身体有好处。这个问题神农觉得很糟糕，所以神农去了吃每种植物。他吃了一种植物以后，就写了这个植物对你有没有好处。有的时候，神农吃了很好吃的植物。有的时候，他吃了很危险的植物。他吃完了每种植物以后，会来跟他的朋友聊到他吃的植物了。

**Corrections**
- 他看到了有很多人不知道哪个植物好吃，也不知道什么植物对你的身体有好处 → 他看到了有很多人不知道哪种植物好吃，也不知道什么植物对他们的身体有好处
  - **Grammar** 哪个植物 → 哪种植物: Use 种, not 个, as the measure word for types of plants.
  - **Coherence: Reference** 你的身体 → 他们的身体: The people are the subject here, so use 他们的 to refer back to them. 你 would address the reader.
- 所以神农去了吃每种植物 → 所以去吃每种植物
  - **Coherence: Reference** delete 神农: 神农 was just mentioned, so the subject can be omitted here.
  - **Coherence: 了 / 着 / 在** 去了 → 去: Before another verb expressing purpose, use 去吃, not 去了吃.
- 他吃了一种植物以后，就写了这个植物对你有没有好处 → 他吃了一种植物以后，就写了它对人的身体有没有好处
  - **Coherence: Reference** 这个植物 → 它: The plant was just mentioned, so use the pronoun 它 to refer back to it.
  - **Coherence: Reference** 你 → 人: This is a general statement about people, not an address to the reader.
- 有的时候，神农吃了很好吃的植物 → 有的时候，神农吃很好吃的植物
  - **Coherence: 了 / 着 / 在** 吃了 → 吃: 有的时候 describes a repeated or habitual action, so use the zero aspect form 吃.
- 有的时候，他吃了很危险的植物 → 有的时候，他吃很危险的植物
  - **Coherence: 了 / 着 / 在** 吃了 → 吃: 有的时候 describes a repeated situation, so use the verb without 了.
- 他吃完了每种植物以后，会来跟他的朋友聊到他吃的植物了 → 他吃完了每种植物以后，会来跟他的朋友聊到他吃的植物
  - **Coherence: 了 / 着 / 在** delete 了: 会 expresses a future or modal action, so do not add sentence-final 了 here.

**Expressiveness**
- After “这个问题神农觉得很糟糕”: You could add his determination to help people find safe plants. For example: 他想帮助大家找到可以吃的植物。
- After “有的时候，他吃了很危险的植物”: You could add a short thought showing why he continued despite the danger. For example: 他想：“我一定要知道哪些植物不能吃。”

**Encouragement** You clearly introduce Shennong and explain the important problem he noticed. You also use the contrast between safe and dangerous plants to make his work easy to understand.

### Scene 2

> 一个人问神农，哪个植物好吃。神农说，这就要看你的口味了。要是你喜欢吃甜的，有很多甜的水果，比方说苹果、西瓜和梨。一个别的人问神农，哪个植物对你的身体有好处。神农说，有很多种植物对你的身体有好处，比方说小白菜、黄瓜、茶和菠菜。一个别的人问神农，哪个植物对你的身体有坏处。

**Corrections**
- 一个别的人问神农 → 另外一个人问神农
  - **Vocabulary** 一个别的人 → 另外一个人: “另外一个人” means “another person.” “别的” is not used in this expression.
- 神农说，有很多种植物对你的身体有好处 → 神农说，有很多种植物对身体有好处
  - **Coherence: Reference** delete 你的: This is a general statement about what is good for the body. Do not use 你的 here.
- 一个别的人问神农，哪个植物对你的身体有坏处 → 另外一个人问神农，哪个植物对身体有坏处
  - **Vocabulary** 一个别的人 → 另外一个人: 另外一个人 means “another person.” 别的 is not used this way before a measure word.
  - **Coherence: Reference** delete 你的: This is a general statement about what is harmful to the body. Do not use 你的 here.

**Expressiveness**
- After “神农说，有很多种植物对你的身体有好处，比方说小白菜、黄瓜、茶和菠菜”: You could add that Shennong wants to record this useful knowledge so that other people can know it too. For example: 神农想把这些写在书上。
- After “一个别的人问神农，哪个植物对你的身体有坏处”: You could show Shennong’s important warning that poisonous plants should not be eaten. For example: 神农说：“有毒的植物不能吃。”

**Encouragement** You use dialogue well to show people asking Shennong for advice. Your examples of healthy plants, especially 茶, clearly connect to Shennong’s knowledge about plants.

### Scene 3

> 神农说，有一天，我吃了一个黄色的花，名字是夹竹桃。我一吃夹竹桃，就觉得这种植物对我的脑有坏处。可是，一个灵芝和一个男人正好在我的旁边，我说，麻烦你把那个植物给我吃一下。我一吃这个灵芝就好了。所以，你得小心吃植物，因为有的植物对你的健康有坏处，特别是夹竹桃。因为夹竹桃有毒。

**Corrections**
- 我吃了一个黄色的花 → 我吃了一朵黄色的花
  - **Grammar** 一个 → 一朵: Flowers use the measure word 朵, not 个.
- 我一吃这个灵芝就好了 → 我一吃这个灵芝身体就好了
  - **Grammar** 就好了 → 身体就好了: After the first action, 身体 should be the subject of the result: 身体就好了.
- 因为夹竹桃有毒 → 夹竹桃有毒
  - **Coherence: Connectors** delete 因为: 因为 introduces a reason and normally needs a following result clause. Here it should be removed.

**Vocabulary suggestions**
- (suggestion) 有坏处 (“有的植物对你的健康有坏处”) → 有害 (“有的植物对你的健康有害”): “有害” is a more direct everyday word for something that can harm health.

**Expressiveness**
- After “我一吃夹竹桃，就觉得这种植物对我的脑有坏处”: You could add Shennong’s frightened thought when he starts to feel unwell. For example: 我想：我会死吗？

**Encouragement** You clearly contrast the dangerous 夹竹桃 with the helpful 灵芝. Your final warning also gives the scene a clear lesson for the listener.

### Content & completeness (after the whole story)

- Need to add: 神农 finding 茶
- Need to add: 神农 fainting after eating 夹竹桃
- Wrong information: “我一吃夹竹桃，就觉得这种植物对我的脑有坏处。” -- In the story, eating 夹竹桃 makes 神农 faint; it is not described as only harming his brain.

## shennong_samples#8

### Scene 1

> 古代的时候，有一个人叫神农。一天，神农正在路上走，一看很多人正在吃一些植物。一些人一吃植物就生病了，神农想帮别人。所以想知道哪些植物能吃，哪些植物不能吃。

**Corrections**
- 古代的时候 → 在古代
  - **Vocabulary** 古代的时候 → 在古代: Use 在古代 to mean “in ancient times.”
- 所以想知道哪些植物能吃，哪些植物不能吃 → 所以他想知道哪些植物能吃，哪些植物不能吃
  - **Coherence: Reference** 所以 → 所以他: Use a pronoun to refer back to 神农 in a new clause.

**Expressiveness**
- After “一些人一吃植物就生病了”: You could add Shen Nong’s worried reaction when he sees that people are getting sick. For example: 他看见大家生病，心里很着急。

**Encouragement** You clearly introduce Shen Nong and set the scene with a time and situation. You also explain the cause of his goal well: people get sick after eating plants, so he wants to find out which ones are safe.

### Scene 2

> 然后，神农开始尝很多植物，比方说他吃过生姜、芥兰和菠菜。一些植物吃真好，特别是黄瓜。但是，一些植物毒得很，特别是夹竹桃。

**Corrections**
- 一些植物吃真好 → 一些植物吃起来真好
  - **Grammar** 吃 → 吃起来: Use “吃起来” to describe how food tastes. “吃真好” is not a complete taste-description structure.

**Expressiveness**
- After “但是，一些植物毒得很，特别是夹竹桃”: You could add Shen Nong’s concern that eating these plants can make people ill. For example: 神农想：吃了这些植物，人会生病。

**Encouragement** You clearly contrast plants that are good to eat with poisonous plants. The specific examples, especially 黄瓜 and 夹竹桃, make this part of the story easy to follow.

### Scene 3

> 一个人对神农说，麻烦我们可以吃什么植物？神农说，这就要看你想不想生病了。以后，神农告诉别人一些植物能吃，一些植物不能吃。

**Corrections**
- 一个人对神农说，麻烦我们可以吃什么植物 → 一个人对神农说，请问我们可以吃什么植物
  - **Vocabulary** 麻烦 → 请问: 请问 is used to politely introduce a question. 麻烦 does not work by itself in this position.

**Expressiveness**
- After “以后，神农告诉别人一些植物能吃，一些植物不能吃”: Add a concrete contrast between lingzhi and oleander so the listener can understand which plants are safe and which are dangerous. For example: 像伞一样的植物是灵芝，可以吃；像星星一样的花是夹竹桃，不能吃。

**Encouragement** You used dialogue to show that someone asks Shennong for help. You also clearly contrasted plants that can be eaten with plants that cannot.

### Content & completeness (after the whole story)

- Missing scene: 神农found茶and took a record
- Missing scene: 神农tried 夹竹桃 and fainted
- Missing scene: a person in blue stopped by and gave灵芝to 神农，神农felt better after eating灵芝
- Missing scene: 神农takes record of灵芝and夹竹桃

## shennong_samples#12

### Scene 1

> 很久以前，古代的人很不知道什么植物能吃，也什么植物不能吃。所以很多人常常吃不安全的植物，吃不安全的植物对你的身体有坏处，很麻烦的情况。但是一个人，神农，要解决这个问题。

**Corrections**
- 古代的人很不知道什么植物能吃，也什么植物不能吃 → 古代的人不知道什么植物能吃，也不知道什么植物不能吃
  - **Grammar** delete 很: 很 cannot modify 不知道. Use 不知道 directly.
  - **Grammar** 也 → 也不知道: The second part also needs the verb 不知道.
- 吃不安全的植物对你的身体有坏处 → 吃不安全的植物对他们的身体有坏处
  - **Coherence: Reference** 你的 → 他们的: This refers back to 很多人, so use 他们的 rather than the reader-directed 你的.

**Expressiveness**
- After “但是一个人，神农，要解决这个问题”: You could add Shennong’s determination to find out which plants are safe to eat and which ones are poisonous. For example: 他想：“我要找出什么植物能吃，什么植物不能吃。”

**Encouragement** You clearly introduce the problem people faced and explain why it was serious. You also bring in Shennong as the person who will solve the problem, which gives the scene a clear direction.

### Scene 2

> 他又聪明又努力，旅行很远找到很多植物。比方说，灵芝和夹竹桃。他一吃各种各样的植物就知道能不能吃这些植物。然后，神农写他的主意。他喜欢植物的味道，特别是花。神农遇到了一个黄色的花，一吃就觉得不舒服。

**Corrections**
- 旅行很远找到很多植物 → 去很远的地方旅行，找到了很多植物
  - **Grammar** 旅行很远 → 去很远的地方旅行: Use 去很远的地方旅行 to say that someone travels to a faraway place.
  - **Coherence: 了 / 着 / 在** 找到 → 找到了: Use 了 on the final action in this completed sequence of events.
- 然后 → 
  - **Coherence: Connectors** delete 然后: This connector is not needed here.
- 神农遇到了一个黄色的花，一吃就觉得不舒服 → 神农遇到了一朵黄色的花，一吃就觉得不舒服
  - **Grammar** 一个 → 一朵: 朵 is the measure word for flowers.

**Expressiveness**
- After “神农遇到了一个黄色的花”: Describe the flower’s shape and appearance to make the setting more vivid. For example: 那朵花像星星一样，又大又漂亮。
- After “一吃就觉得不舒服”: Add Shen Nong’s worried thought when his stomach starts to hurt. For example: 他想：我会死吗？

**Encouragement** You clearly named two important plants, 灵芝 and 夹竹桃, and explained that Shen Nong tested many different plants. You also included his immediate bad reaction after eating the yellow flower, which makes this scene easy to follow.

### Scene 3

> 发现了夹竹桃有毒。别人看到他，很快给他吃一个灵芝。神农一吃就觉得比较好。然后，他继续写他发现的信息。会告诉他的朋友哪一个植物能不能吃。

**Corrections**
- 别人看到他，很快给他吃一个灵芝 → 别人看到他，很快给他吃了一个灵芝
  - **Coherence: 了 / 着 / 在** 给他吃 → 给他吃了: Use 了 because giving him the lingzhi is a completed action in the story.
- 会告诉他的朋友哪一个植物能不能吃 → 他会告诉他的朋友哪一种植物能吃，哪一种植物不能吃
  - **Coherence: Reference** 会告诉 → 他会告诉: Use 他 to refer back to 神农 at the start of this new clause.
  - **Grammar** 哪一个植物能不能吃 → 哪一种植物能吃，哪一种植物不能吃: Do not combine 哪一个 with 能不能. State separately which kinds of plants can be eaten and which cannot.

**Expressiveness**
- After “神农一吃就觉得比较好”: You could add that Shennong felt relieved when his stomach stopped hurting. For example: 他的肚子不疼了，他觉得很高兴。
- After “然后，他继续写他发现的信息”: You could add that he wanted other people to know which plants were safe. For example: 他想让别人知道什么植物可以吃。

**Encouragement** You clearly explained the important discovery that oleander is poisonous and lingzhi helps Shennong feel better. You also included how Shennong shares what he learns with his friends.

### Content & completeness (after the whole story)

- Need to add: He found 茶.
- Need to add: 神农 tries 夹竹桃 and faints.
- Missing scene: another person in brown came by and had a conversation with 神农

## shennong_samples#18

### Scene 1

> 神农和他的家人住在古代，所以不知道什么植物能吃。因为他的家人常常生病了，所以神农和他的哥哥一起去旅行找可以吃的植物。他们去很多不一样的地方，比方说高山、山谷和沙漠。

**Corrections**
- 因为他的家人常常生病了 → 因为他的家人常常生病
  - **Coherence: 了 / 着 / 在** delete 了: 常常 shows a repeated habit or condition, so do not use 了.

**Vocabulary suggestions**
- (suggestion) 旅行 (“一起去旅行找可以吃的植物”) → 寻找 (“一起寻找可以吃的植物”): “寻找” makes their purpose of looking for edible plants clearer than the more general “旅行”.
- (suggestion) 不一样 (“很多不一样的地方”) → 不同 (“很多不同的地方”): “不同” is a slightly more precise everyday way to describe the variety of places.

**Expressiveness**
- After “所以神农和他的哥哥一起去旅行找可以吃的植物”: You could add a short line showing Shen Nong’s determination to find plants that can help his family. For example: 神农说：“我们一定要找到可以吃的植物。”
- After “他们去很多不一样的地方，比方说高山、山谷和沙漠”: You could add that they kept going even though the journey was difficult. For example: 路很远，可是他们还是一直走。

**Encouragement** You clearly explain why Shen Nong starts searching for plants, which gives the scene a strong cause-and-effect structure. You also make the journey more interesting by naming several different places.

### Scene 2

> 他们在很漂亮的河找夹竹桃。神农问他的哥哥：“我应该吃这种植物吗？”哥哥说：“这就要看你想要安全还是接近知道了。“神农一吃夹竹桃就生病了。哥哥说：“太麻烦了。

**Corrections**
- 他们在很漂亮的河找夹竹桃 → 他们在很漂亮的河边找夹竹桃
  - **Grammar** 河 → 河边: A location with 河 normally needs a location word such as 边. 在河边 means “by the river.”
- 哥哥说：“这就要看你想要安全还是接近知道了。“ → 哥哥说：“这就要看你想要安全还是想知道”
  - **Vocabulary** 接近 → 想: 接近 cannot modify 知道 here. 想知道 means “want to know.”
  - **Coherence: 了 / 着 / 在** delete 了: 想知道 is a mental-state expression and normally takes no 了 here.
  - **Grammar** “ → ”: Use a closing quotation mark at the end of the quoted speech.

**Vocabulary suggestions**
- (suggestion) 生病了 (“神农一吃夹竹桃就生病了”) → 中毒了 (“神农一吃夹竹桃就中毒了。”): “中毒了” is more precise because he becomes ill after eating a poisonous plant.

**Expressiveness**
- After “他们在很漂亮的河找夹竹桃”: You could describe the yellow flowers to make the place and the plant easier to imagine. For example: 河边有黄黄的花，花瓣像星星。
- After “神农一吃夹竹桃就生病了”: You could add Shennong’s worried reaction to show how painful and frightening this moment is. For example: 神农说：“我的肚子好疼，我怎么办？”

**Encouragement** You clearly show the cause and result: Shennong eats the oleander and then becomes ill. The question-and-answer dialogue with his brother also makes the scene feel more like a story.

### Scene 3

> 夹竹桃是毒的，我想知道灵芝会帮他。”哥哥给神农灵芝。神农吃完了以后开始痊愈了。神农说：“谢谢哥哥，你帮得真好。灵芝我们可以吃，特别是如果我们已经吃了夹竹桃。“

**Corrections**
- 夹竹桃是毒的 → 夹竹桃是有毒的
  - **Vocabulary** 是 → 是有: Use 有毒 to say that something is poisonous.
- 哥哥给神农灵芝 → 哥哥给了神农灵芝
  - **Coherence: 了 / 着 / 在** 给 → 给了: Giving the lingzhi is a completed action, so use 了.

**Vocabulary suggestions**
- (suggestion) 真好 (“你帮得真好”) → 及时 (“你帮得很及时”): “及时” specifically highlights that the brother helped at the right moment.

**Expressiveness**
- After “神农吃完了以后开始痊愈了”: Add Shennong’s feeling of luck after the medicine works. For example: 神农觉得自己很幸运。
- After “神农说：“谢谢哥哥，你帮得真好”: Add the brother’s reaction to show that he is relieved Shennong is better. For example: 哥哥看到神农好了，也放心了。

**Encouragement** You clearly show the cause and result: Lingzhi helps Shennong recover after eating oleander. You also use direct speech to show Shennong thanking his brother.

### Content & completeness (after the whole story)

- Missing scene: 神农found茶and took a record
- Missing scene: another person in brown came by and had a conversation with 神农
- Missing scene: 神农takes record of灵芝and夹竹桃
- Wrong information: “哥哥给神农灵芝。” -- In the story, a person who stops by gives 灵芝 to 神农, rather than his accompanying brother.

## shennong_samples#19

### Scene 1

> 古代的时候，一个男人觉得植物很有意思。他叫神农。有的植物吃了以后他的肚子疼死了，可是有的吃了以后很舒服。他找很多植物。

**Corrections**
- 古代的时候，一个男人觉得植物很有意思 → 在古代，一个男人觉得植物很有意思
  - **Vocabulary** 古代的时候 → 在古代: Use 在古代 to say “in ancient times” in this story setting.
- 他找很多植物 → 他找了很多植物
  - **Coherence: 了 / 着 / 在** 找 → 找了: This is a completed action in the sequence, so use 了.

**Expressiveness**
- After “可是有的吃了以后很舒服”: Add Shen Nong’s thought that he wants to find out which plants are safe to eat and which are poisonous. For example: 他想知道哪些植物可以吃，哪些不能吃。
- After “他找很多植物”: Add a small detail showing how hard he worked to find plants in many places. For example: 他走啊走啊，去了很多高山。

**Encouragement** You clearly introduce Shen Nong and explain why plants interest him. The contrast between plants that cause stomach pain and plants that make him feel well helps show his reason for searching for more plants.

### Scene 2

> 凉山很大的山，这也找植物。一天，他找到黄色的花。他听说你跟黄色的花做茶很有用。比方说，你的头发疼死，这冰茶是药。他一喝茶就很不舒服。

**Corrections**
- 这也找植物 → 他也找植物
  - **Coherence: Reference** 这 → 他: Use 他 to refer back to the man, 神农. 这 means “this” and cannot refer to him.
- 一天，他找到黄色的花 → 一天，他找到了黄色的花
  - **Coherence: 了 / 着 / 在** 找到 → 找到了: Finding the flower is a completed event in the story, so use 了.
- 他听说你跟黄色的花做茶很有用 → 他听说用黄色的花做茶很有用
  - **Coherence: Reference** delete 你: 你 refers to the listener, but no listener has been introduced. The sentence is about making tea with the flowers in general.
  - **Vocabulary** 跟 → 用: Use 用 to say that flowers are the material used to make tea.
- 你的头发疼死 → 你的头疼死了
  - **Vocabulary** 头发 → 头: 头发 means “hair”; hair cannot hurt. Use 头 for a headache.
  - **Coherence: 了 / 着 / 在** 疼死 → 疼死了: Add 了 to show that the painful state has occurred.
- 他一喝茶就很不舒服 → 他一喝茶就很不舒服了
  - **Coherence: 了 / 着 / 在** 不舒服 → 不舒服了: Use 了 to show that he became uncomfortable after drinking the tea.

**Vocabulary suggestions**
- (suggestion) 大 (“很大的山”) → 高 (“很高的山”): “高” describes a mountain’s height more precisely, while “大” is more general.

**Expressiveness**
- After “一天，他找到黄色的花”: Describe the flowers so the listener can picture why Shennong notices them. For example: 那些花像星星一样，又大又漂亮。
- After “他一喝茶就很不舒服”: Add Shennong’s worried feeling after he becomes ill. For example: 他心里很害怕。

**Encouragement** You introduced a mountain setting and showed Shennong looking for plants. You also tried to explain why a plant might be useful by giving an example with “比方说”.

### Scene 3

> 糟糕，这黄色的花是夹竹桃，特别是毒。正好在这儿，灵芝药的夹竹桃他吃完了，也写一个课文的植物。谢谢神农。

**Corrections**
- 糟糕，这黄色的花是夹竹桃，特别是毒 → 糟糕，这黄色的花是夹竹桃，特别有毒
  - **Grammar** 是毒 → 有毒: Use 有毒 to say that something is poisonous. 是毒 is not a grammatical predicate here.
- 正好在这儿，灵芝药的夹竹桃他吃完了，也写一个课文的植物 → 正好在这儿，他把灵芝和夹竹桃吃完了，也写了一篇关于植物的课文
  - **Grammar** 灵芝药的夹竹桃他 → 他把灵芝和夹竹桃: Use 和 to join the two plants. Put the subject before the object, and use 把 before an object that is eaten completely.
  - **Coherence: 了 / 着 / 在** 写 → 写了: The writing is a completed past action, so it needs 了.
  - **Grammar** 一个 → 一篇: 篇 is the measure word for a written text or passage.
  - **Grammar** 课文的植物 → 关于植物的课文: Use 关于植物的课文 for “a text about plants.” The topic comes before 课文.

**Expressiveness**
- After “糟糕，这黄色的花是夹竹桃，特别是毒”: Add Shennong’s worried thought to show how frightened he feels after discovering the flower is poisonous. For example: 他想：“我会死吗？”

**Encouragement** You clearly identify the yellow flower as the dangerous plant in this scene. Ending with thanks to Shennong also shows that you understand he helps people.

### Content & completeness (after the whole story)

- Missing scene: another person in brown came by and had a conversation with 神农
- Missing scene: 神农takes record of灵芝and夹竹桃
- Wrong information: “糟糕，这黄色的花是夹竹桃，特别是毒。” -- This makes the flower used to make 茶 into 夹竹桃. In the required story, 茶 is found first, and 夹竹桃 is a separate plant tried afterwards.

## shennong_samples#26

### Scene 1

> 很久以前，有一个老男人叫神农。神农在古代每一天看到了别的小镇人生病还是不舒服，所以他决定开始找新的药。他下一天开始爬当地的山脉，找了各种各样的植物。神农试一试每个植物，知道有什么好处。

**Corrections**
- 有一个老男人叫神农 → 有一个叫神农的老男人
  - **Grammar** 一个老男人叫神农 → 一个叫神农的老男人: When introducing someone by name, use “一个叫……的＋noun”.
- 神农在古代每一天看到了别的小镇人生病还是不舒服 → 他在古代每一天看到别的小镇人生病还是不舒服
  - **Coherence: Reference** 神农 → 他: Shennong was just introduced, so use the pronoun “他” to refer to him again.
  - **Coherence: 了 / 着 / 在** 看到了 → 看到: “每一天” describes a routine, so use zero aspect: 每一天看到.
- 他下一天开始爬当地的山脉 → 他第二天开始爬当地的山脉
  - **Vocabulary** 下一天 → 第二天: Use “第二天” to mean “the next day” in a story.
- 神农试一试每个植物 → 神农试了试每种植物
  - **Coherence: 了 / 着 / 在** 试一试 → 试了试: This is a completed action in the past, so use 了: 试了试.
  - **Grammar** 每个植物 → 每种植物: Use 种 as the measure word when referring to each type of plant.

**Vocabulary suggestions**
- (suggestion) 药 (“找新的药”) → 草药 (“找新的草药”): “草药” is more precise because Shennong is looking for useful plants that can be used as medicine.

**Expressiveness**
- After “神农试一试每个植物，知道有什么好处”: You could add that he carefully wrote down what he discovered about each plant. For example: 他把每个植物的好处都写在书上。

**Encouragement** You clearly explain why Shennong begins his search: he sees that many people are ill. You also use “各种各样的植物” well to show that he searches widely.

### Scene 2

> 比方说，他一次试一试有些植物的叶，吃得又新鲜又甜。煮这些叶以后，他一喝就知道他发现新的茶叶。虽然他找到了很多的新的植物，但是他的旅程有的时候特别是危险。比方说，他一吃灵芝就开始生病。

**Corrections**
- 比方说，他一次试一试有些植物的叶，吃得又新鲜又甜 → 比方说，有一次，他试了一些植物的叶，吃起来又新鲜又甜
  - **Grammar** 他一次 → 有一次，他: Use 有一次 at the beginning to say that something happened once.
  - **Grammar** 试一试有些 → 试了一些: For a completed past action, use 试了. 一些 is the usual quantifier before the noun here.
  - **Grammar** 吃得 → 吃起来: Use 吃起来 to describe how food tastes. 吃得 describes how a person performs the action of eating.
- 煮这些叶以后，他一喝就知道他发现新的茶叶 → 煮了这些叶以后，他一喝就知道他发现了新的茶叶
  - **Coherence: 了 / 着 / 在** 煮这些叶 → 煮了这些叶: Boiling happened before the later action, so use 了 for the completed action.
  - **Coherence: 了 / 着 / 在** 发现新的茶叶 → 发现了新的茶叶: Finding the new tea leaves is a completed event, so it takes 了.
- 虽然他找到了很多的新的植物，但是他的旅程有的时候特别是危险 → 虽然他找到了很多的新的植物，但是他的旅程有的时候特别危险
  - **Vocabulary** 特别是 → 特别: 特别 directly modifies an adjective such as 危险. 特别是 is normally used to introduce a specific item or case.

**Expressiveness**
- After “煮这些叶以后，他一喝就知道他发现新的茶叶”: You could add that Shennong felt happy about finding a useful new plant. For example: 他觉得很高兴。
- After “比方说，他一吃灵芝就开始生病”: You could describe how sick Shennong felt, for example by mentioning his stomach pain. For example: 他的肚子疼得不得了。

**Encouragement** You clearly show Shennong testing plants and discovering tea step by step. You also include the danger in his journey, which makes the scene more interesting.

### Scene 3

> 一个爬山的男人正好看到神农的麻烦，然后给了他一些药。神农最终他的小镇回到，跟别的人分享他的发现。你认为神农的故事真的吗？这就要看你相信中药对身体有好处。

**Corrections**
- 神农最终他的小镇回到 → 神农最终回到他的小镇
  - **Grammar** 他的小镇回到 → 回到他的小镇: The verb and its location should be ordered as 回到 + place.
- 跟别的人分享他的发现 → 跟别的人分享了他的发现
  - **Coherence: 了 / 着 / 在** 分享 → 分享了: In a series of completed actions, the last action takes 了.
- 你认为神农的故事真的吗 → 你认为神农的故事是真的吗
  - **Grammar** 故事 → 故事是: Use 是 before 真 when asking whether a story is true.
- 这就要看你相信中药对身体有好处 → 这就要看你相不相信中药对身体有好处
  - **Coherence: Connectors** 相信 → 相不相信: After 要看, use a yes-or-no condition such as 相不相信.

**Expressiveness**
- After “一个爬山的男人正好看到神农的麻烦”: You could describe the man’s clothes to help the reader picture this important helper. For example: 他穿着蓝色的衣服。
- After “然后给了他一些药”: You could add Shen Nong’s relief after taking the medicine. For example: 神农吃了以后，觉得好多了。

**Encouragement** You clearly included the helper who gives Shen Nong medicine and the ending where Shen Nong shares what he discovered. Your final question also connects the story to the value of traditional Chinese medicine.

### Content & completeness (after the whole story)

- Need to add: He needs to try 夹竹桃 and faint; the story names 灵芝 instead and only says that he becomes ill.
- Need to add: The helper needs to give 灵芝, and 神农 needs to eat it and feel better.
- Missing scene: another person in brown came by and had a conversation with 神农
- Missing scene: 神农takes record of灵芝and夹竹桃
- Wrong information: “比方说，他一吃灵芝就开始生病。” -- 灵芝 is the plant that helps 神农 feel better after 夹竹桃 makes him faint; it does not make him sick.

## shennong_samples#33

### Scene 1

> 古代时候，人不知道他们能吃什么植物，常常一吃就死。但是不知道为什么，没有办法。所以有一天，神农出去试一试很多种植物，告诉人什么植物是安全什么是危险。

**Corrections**
- 古代时候 → 在古代
  - **Grammar** 古代时候 → 在古代: Use 在古代 to mean “in ancient times.”
- 告诉人什么植物是安全什么是危险 → 告诉人什么植物是安全的，什么植物是危险的了
  - **Grammar** 什么植物是安全什么是危险 → 什么植物是安全的，什么植物是危险的: Use 的 after 安全 and 危险 here, and repeat 什么植物 to make the two alternatives clear.
  - **Coherence: 了 / 着 / 在** 危险 → 危险了: This is the final action in a series, so add 了 to show that Shennong completed telling the people.

**Vocabulary suggestions**
- (suggestion) 试一试 (“出去试一试很多种植物”) → 尝 (“出去尝很多种植物”): “尝” is more precise because Shennong is tasting plants to find out whether they are safe.

**Expressiveness**
- After “但是不知道为什么，没有办法”: Add Shennong’s determination to help people know which plants are safe. For example: 神农想：“我要帮大家找到安全的植物。”
- After “所以有一天，神农出去试一试很多种植物，告诉人什么植物是安全什么是危险”: Add a small detail about where he searched for plants to make his action easier to picture. For example: 他走到山上，看了很多植物。

**Encouragement** You clearly explain the problem people had and give Shennong a helpful purpose. Your use of “所以” also connects the problem to his action well.

### Scene 2

> 发现有的植物对身体非常好，特别是茶，让肚子感觉又暖和又清楚。他告诉朋友：“你吃哪种植物，这就要看你的口味。比方说，你爱吃甜的，可能喜欢糖。”他最喜欢吃花，除了夹竹桃以外，什么都花想吃。

**Corrections**
- 让肚子感觉又暖和又清楚 → 让肚子感觉又暖和又舒服
  - **Vocabulary** 清楚 → 舒服: 清楚 means “clear” and does not describe a bodily feeling here. 舒服 means “comfortable.”
- 什么都花想吃 → 什么花都想吃
  - **Grammar** 什么都花 → 什么花都: With 什么 + noun, the noun comes before 都: 什么花都想吃.

**Vocabulary suggestions**
- (suggestion) 好 (“对身体非常好”) → 有用 (“对身体非常有用”): “有用” is more precise here because it highlights that these plants can help people’s health.

**Expressiveness**
- After “发现有的植物对身体非常好，特别是茶，让肚子感觉又暖和又清楚”: You could add what Shen Nong learned tea could be used for, not just how it made him feel. For example: 茶放在水里很好喝，也可以治病。

**Encouragement** You clearly connect plants, especially tea, with helping the body. You also tried to make Shen Nong speak directly, which makes the retelling feel more like a story.

### Scene 3

> 他发现这个口味，一百岁时候，不小心吃了毒的花。一吃就开始死。但是生病时候告诉人什么植物是药，什么植物是毒。

**Corrections**
- 他发现这个口味，一百岁时候，不小心吃了毒的花 → 他发现这个口味，一百岁的时候，不小心吃了有毒的花
  - **Grammar** 一百岁时候 → 一百岁的时候: Use 的时候 after an age to mean “when someone was ... years old.”
  - **Vocabulary** 毒的花 → 有毒的花: Use 有毒 to describe a poisonous plant or flower.
- 什么植物是毒 → 什么植物有毒
  - **Vocabulary** 是毒 → 有毒: Use 有毒 to say that a plant is poisonous.

**Expressiveness**
- After “一吃就开始死”: You could show Shennong's fear by adding the thought he has when the poisonous flower makes him very ill. For example: 他想：“我会死吗？”

**Encouragement** You clearly include the important danger of eating a poisonous flower. You also explain Shennong’s useful purpose: telling people which plants are medicine and which are poisonous.

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

**Corrections**
- 所以他们找到了很多植物对药 → 所以他们找到了很多植物做药
  - **Vocabulary** 对 → 做: 做药 means “make medicine.” 对药 does not fit this meaning.
- 神农先看到很多病人 → 神农先看到了很多病人
  - **Coherence: 了 / 着 / 在** 看到 → 看到了: This is a completed event in the story, so use 了.
- 但是我觉得他们的吃的植物 → 但是我觉得他们吃的植物
  - **Grammar** 他们的吃的植物 → 他们吃的植物: Use the verb phrase before 的 to describe the noun: 他们吃的植物.
- 神农觉得这个植物可能特别是毒 → 神农觉得这个植物可能特别有毒
  - **Vocabulary** 是毒 → 有毒: Use 有毒 to say that a plant is poisonous.
- 所以他想找一个植物对药 → 所以他想找一种植物做药
  - **Grammar** 一个 → 一种: Use 种 as the measure word for a type of plant.
  - **Vocabulary** 对 → 做: 做药 means “make medicine.”
- 正好，他找到了一把花，他想把花放在茶里，对药 → 正好，他找到了一把花，他想把花放在茶里，做药
  - **Vocabulary** 对药 → 做药: 做药 means “make medicine.” 对药 does not fit here.

**Expressiveness**
- After “神农先看到很多病人”: You could describe how the sick people looked to make the problem feel more real. For example: 他看到病人都很难受。
- After “所以他想找一个植物对药，他们可以吃对药”: You could add Shen Nong’s determination to find plants that can help sick people. For example: 他想：我一定要找到可以做药的植物。

**Encouragement** You clearly set the story in ancient times and explained that people became ill after eating plants. You also showed Shen Nong’s goal of finding plants that could help people.

### Scene 2

> 他不知道如果这把花对你的身体好，这就要看如果这把花毒不毒了。神农想找别的植物，但是这很麻烦。正好，他找到了别的花。他一吃花，很快就生病了。他的肚子疼死了。神农不知道他吃不吃灵芝或者夹竹桃。

**Corrections**
- 他不知道如果这把花对你的身体好，这就要看如果这把花毒不毒了 → 他不知道这把花对他的身体好不好，这就要看这把花毒不毒
  - **Grammar** delete 如果: Use an A-not-A question after 不知道, not 如果, to mean “whether.”
  - **Coherence: Reference** 你的 → 他的: The flower is being tested on Shennong's body, so use 他的 rather than “your.”
  - **Grammar** 好 → 好不好: After 不知道, 好不好 forms the question “whether it is good.”
  - **Grammar** delete 如果: After 看, use the A-not-A form 毒不毒 to mean “whether it is poisonous.”
  - **Coherence: 了 / 着 / 在** delete 了: 毒不毒 describes a state here; it does not need 了.
- 神农不知道他吃不吃灵芝或者夹竹桃 → 神农不知道吃不吃灵芝或者夹竹桃
  - **Coherence: Reference** delete 他: When the subject is still 神农 within the same clause, omit the pronoun.

**Vocabulary suggestions**
- (suggestion) 麻烦 (“但是这很麻烦”) → 困难 (“但是这很困难。”): “困难” more clearly emphasizes that finding other plants is hard to do, while “麻烦” can also mean bothersome.

**Expressiveness**
- After “正好，他找到了别的花”: You could describe the flower so the reader can picture what Shennong sees. For example: 那朵花是黄色的，像星星一样。
- After “他的肚子疼死了”: You could add Shennong’s fear when the pain becomes very strong. For example: 他想：我会死吗？

**Encouragement** You clearly show the cause-and-effect sequence: Shennong eats the flower, then quickly becomes ill and has a stomachache. You also include his uncertainty about whether he ate 灵芝 or 夹竹桃, which gives the scene suspense.

### Scene 3

> 别的人给了神农一个灵芝。这个植物可以让神农更好。比方说，他会觉得更健康。吃灵芝以后，他可以再走。现在他觉得更好。最后，神农找到了很多植物，他可以用对药。这些植物让神农很高兴。神农想跟很多人分享他的新药。

**Corrections**
- 吃灵芝以后 → 吃了灵芝以后
  - **Coherence: 了 / 着 / 在** 吃 → 吃了: Eating the lingzhi is completed before the later action, so use 了.
- 他可以用对药 → 他可以用来做药
  - **Grammar** 用 → 用来: Use 用来 before a verb to express the purpose of using something.
  - **Vocabulary** 对 → 做: 做药 means “make medicine”; 对药 is not the correct expression here.

**Vocabulary suggestions**
- (suggestion) 最后 (“最后，神农找到了很多植物”) → 后来 (“后来，神农找到了很多植物”): “后来” is more precise here because it simply shows what happened after he recovered, without suggesting that this is the final event of the whole story.

**Expressiveness**
- After “别的人给了神农一个灵芝”: You could describe what the lingzhi looks like, as it is like a small umbrella in the story. For example: 灵芝像一把小伞。
- After “最后，神农找到了很多植物，他可以用对药”: You could add that Shennong writes down the useful plants so that other people can learn about them. For example: 他把这些植物写在书上。

**Encouragement** You clearly show that Shennong recovers after eating lingzhi and can continue his journey. You also connect his plant discoveries to his wish to share medicine with many people.

### Content & completeness (after the whole story)

- Missing scene: 神农found茶and took a record
- Need to add: The flower is 夹竹桃, and 神农 faints.
- Missing scene: another person in brown came by and had a conversation with 神农
- Missing scene: 神农takes record of灵芝and夹竹桃
- Wrong information: “神农不知道他吃不吃灵芝或者夹竹桃。” -- In the story, 神农 does eat 夹竹桃; it is the plant that makes him faint.

## shennong_samples#42

### Scene 1

> 古代的时候有一个人叫神农。他需要当上医，一看别的人就想帮助他们。但是，他有一个问题，他不知道什么东西能做药。神农听说一个远远的地方有一种植物，什么病人吃都会觉得身体更好。神农三个月走去，找到有植物的地方，他看到一个很漂亮的植物，又香又好看。

**Corrections**
- 神农三个月走去，找到有植物的地方，他看到一个很漂亮的植物，又香又好看 → 神农走了三个月，找到有这种植物的地方，他看到了一棵很漂亮的植物，又香又好看
  - **Grammar** 三个月走去 → 走了三个月: A duration such as 三个月 normally comes after the verb: 走了三个月.
  - **Coherence: Reference** 植物 → 这种植物: This refers back to the particular plant mentioned earlier, so use 这种植物 to identify it.
  - **Coherence: 了 / 着 / 在** 看到 → 看到了: This is the final action in a series, so use 了 to mark its completion.
  - **Grammar** 一个 → 一棵: 棵 is the measure word used for plants.

**Vocabulary suggestions**
- (suggestion) 东西 (“什么东西能做药”) → 植物 (“什么植物能做药”): “植物” is more precise because Shennong is trying to identify plants that can be used as medicine.

**Expressiveness**
- After “神农听说一个远远的地方有一种植物，什么病人吃都会觉得身体更好”: Add Shennong’s thought to show that he is curious but not completely sure the plant can really help people. For example: 他想：这种植物真的能做药吗？
- After “神农三个月走去，找到有植物的地方，他看到一个很漂亮的植物，又香又好看”: Add a visual detail about the flowers to make the place and plant easier to imagine. For example: 那儿开着黄色的、像星星一样的花。

**Encouragement** You clearly introduce Shennong’s goal of helping other people and the problem he needs to solve. You also include his long journey and describe the plant as beautiful and fragrant.

### Scene 2

> 他觉得，这种一定是做药的花。原来他想错了。吃了以后，神农快生病。 这时一个穿着蓝色衣服的人帮神农，快给他一种红的灵芝。神农吃了以后，他没有病，想起来以前一个人告诉他，灵芝对身体有好处。

**Corrections**
- 吃了以后，神农快生病 → 吃了以后，神农快生病了
  - **Coherence: 了 / 着 / 在** 生病 → 生病了: Add 了 because becoming ill is a completed change in the story.
- 这时一个穿着蓝色衣服的人帮神农，快给他一种红的灵芝 → 这时一个穿着蓝色衣服的人帮神农，很快给了他一种红的灵芝
  - **Coherence: 了 / 着 / 在** 快给 → 很快给了: Use 很快 for “quickly,” and add 了 because giving the lingzhi is a completed action.
- 神农吃了以后，他没有病 → 神农吃了以后，他没有病了
  - **Coherence: 了 / 着 / 在** 病 → 病了: Add sentence-final 了 to show the new state: he is no longer ill.

**Expressiveness**
- After “吃了以后，神农快生病”: Add Shennong’s worried thought to show how frightened he is when he becomes ill. For example: 他想：“我会死吗？”
- After “神农吃了以后，他没有病，想起来以前一个人告诉他，灵芝对身体有好处”: Add his gratitude to show that he understands the blue-clothed person has helped him. For example: 他很感谢那个人。

**Encouragement** You clearly included an important twist: Shennong first thinks the flower can be medicine, but then learns he was wrong. You also connected Lingzhi’s benefit for the body to Shennong getting better.

### Scene 3

> 啊，他怎么忘记了？他把灵芝放在包里。一回家就告诉别人。他找到药以后他写下怎么做药在书上。所以人们都知道，那红灵芝对身体好处。

**Corrections**
- 一回家就告诉别人 → 他一回家就告诉了别人
  - **Coherence: Reference** 一回家 → 他一回家: Use a pronoun to refer back to the close, previously mentioned character in a new clause.
  - **Coherence: 了 / 着 / 在** 告诉 → 告诉了: This is the completed final action in the sequence, so use 了.
- 他找到药以后他写下怎么做药在书上 → 他找到药以后，他在书上写下了怎么做药
  - **Grammar** 写下怎么做药在书上 → 在书上写下怎么做药: Put the location phrase 在书上 before the verb 写下.
  - **Coherence: 了 / 着 / 在** 写下 → 写下了: Writing it down is a completed action in the story, so use 了.
- 所以人们都知道，那红灵芝对身体好处 → 所以人们都知道，那红灵芝对身体有好处
  - **Grammar** 对身体好处 → 对身体有好处: Use 有好处 to say that something is good for the body.

**Vocabulary suggestions**
- (suggestion) 放 (“他把灵芝放在包里”) → 装进 (“他把灵芝装进包里。”): “装进” is more precise because it specifically describes putting something inside a bag.

**Expressiveness**
- After “所以人们都知道，那红灵芝对身体好处”: Add Shennong’s feeling of happiness because his discovery can help many people. For example: 神农觉得很高兴，因为他能帮助很多人。
- After “他找到药以后他写下怎么做药在书上”: You could add that he also recorded which plants were unsafe to eat, showing why his book was useful. For example: 他也写下了哪些植物不能吃。

**Encouragement** You give the scene a clear ending: Shennong takes the lingzhi home, shares the news, and writes about it in a book. You also show that his discovery helps other people.

### Content & completeness (after the whole story)

- Need to add: People do not know which plants are safe to eat, and people get sick after eating some plants.
- Missing scene: 神农found茶and took a record
- Need to add: The plant is 夹竹桃, and 神农 faints after eating it.
- Need to add: A record of both 灵芝 and 夹竹桃, especially 夹竹桃
- Wrong information: “吃了以后，神农快生病。” -- In the story, 神农 eats 夹竹桃 and faints; this changes it to nearly becoming sick after an unnamed plant.

## shennong_samples#49

### Scene 1

> 古代的时候，有很多人不知道什么植物能吃，什么植物不能吃。有很多人吃植物以后就吃坏肚子了，因为他们吃了毒。那个时候，有一个老人叫神农，他什么植物都觉得好吃，不怕生病，不怕毒。他希望别人也可以吃好吃的植物。可是他知道，如果他们还怕吃毒，不会吃他喜欢的植物。

**Corrections**
- 古代的时候 → 在古代
  - **Vocabulary** 古代的时候 → 在古代: Use 在古代 to introduce a time period in this story.
- 有很多人吃植物以后就吃坏肚子了，因为他们吃了毒 → 有很多人吃植物以后就吃坏肚子了，因为他们吃的植物有毒
  - **Vocabulary** 吃了毒 → 吃的植物有毒: Plants can be 有毒; 吃毒 is not the natural way to describe eating poisonous plants.
- 可是他知道，如果他们还怕吃毒，不会吃他喜欢的植物 → 可是他知道，如果他们还怕吃有毒的植物，不会吃他喜欢的植物
  - **Vocabulary** 吃毒 → 吃有毒的植物: Say 吃有毒的植物 for eating poisonous plants. 吃毒 is not natural here.

**Vocabulary suggestions**
- (suggestion) 好吃 (“好吃的植物”) → 美味 (“美味的植物”): “美味” gives a more vivid sense that the plants taste especially good.

**Expressiveness**
- After “有很多人吃植物以后就吃坏肚子了，因为他们吃了毒”: You could add that people felt worried because they did not know which plants were safe. For example: 人们都很怕生病。
- After “他希望别人也可以吃好吃的植物”: You could explain that Shennong wanted to discover which plants people could safely eat. For example: 他想找出什么植物能吃。

**Encouragement** You clearly introduce the problem people had with poisonous plants and explain why Shennong wanted to help. You also give Shennong a clear motivation: he wants other people to enjoy good plants too.

### Scene 2

> 所以，他上山下山找植物，吃了很多样子的植物。他是第一人，找到了茶。他把所有的植物写下来了。他一直都吃了，他连毒都能吃。可是他还没吃了一个叫夹竹桃的植物。他找到了那个像星星的植物，觉得很漂亮，马上就吃下了。

**Corrections**
- 他是第一人 → 他是第一个人
  - **Grammar** 第一人 → 第一个人: Use the measure word 个 in 第一个人 to mean “the first person.”
- 他一直都吃了 → 他一直都吃
  - **Coherence: 了 / 着 / 在** 吃了 → 吃: 一直 describes an ongoing or habitual action, so do not use the completion marker 了 here.
- 可是他还没吃了一个叫夹竹桃的植物 → 可是他还没吃一个叫夹竹桃的植物
  - **Coherence: 了 / 着 / 在** 吃了 → 吃: With 没, do not use the completion marker 了 after the verb.

**Expressiveness**
- After “他是第一人，找到了茶”: You could add that tea tasted good when put in water, showing why this discovery was useful. For example: 他发现茶放在水里很好喝。
- After “他找到了那个像星星的植物，觉得很漂亮，马上就吃下了”: You could add that he did not know this beautiful plant was poisonous before he ate it. For example: 那时，他不知道这种植物有毒。

**Encouragement** You clearly show Shennong’s brave work of travelling through the mountains and trying many plants. The detail that the plant looked like a star and was beautiful makes this moment in the story more vivid.

### Scene 3

> 可是夹竹桃的毒很重，让他肚子很痛。他在地上躺着，觉得他快会死了。可是正好有别人找到他了，给了他一个像伞的植物，叫灵芝。他吃灵芝以后就觉得很好，不再生病了。他测量起来了，像星星的植物是毒，像伞的植物是药。

**Corrections**
- 他在地上躺着，觉得他快会死了 → 他在地上躺着，觉得快要死了
  - **Coherence: Reference** delete 他: The subject is the same as in the first part of the clause, so use a zero subject here.
  - **Grammar** 快会 → 快要: Use 快要 to express that something is about to happen.
- 可是正好有别人找到他了，给了他一个像伞的植物，叫灵芝 → 可是正好有一个人找到他，给了他一个像伞的植物，叫灵芝
  - **Coherence: Reference** 别人 → 一个人: For a person mentioned for the first time, use a noun phrase such as “一个人”. “别人” usually refers to other people already understood from the context.
  - **Coherence: 了 / 着 / 在** 找到了 → 找到: In a series of completed actions, put 了 on the final action. Here, “给了” is the final action.
- 他吃灵芝以后就觉得很好 → 他吃了灵芝以后就觉得很好
  - **Coherence: 了 / 着 / 在** 吃灵芝以后 → 吃了灵芝以后: The eating is completed before he feels better, so add 了 after 吃.
- 他测量起来了，像星星的植物是毒，像伞的植物是药 → 他测量起来了，像星星的植物有毒，像伞的植物是药
  - **Vocabulary** 是毒 → 有毒: Use 有毒 to say that a plant is poisonous. “是毒” is not the usual expression.

**Vocabulary suggestions**
- (suggestion) 重 (“夹竹桃的毒很重”) → 强 (“夹竹桃的毒很强”): “强” is a more natural everyday word for describing how powerful a poison is.

**Expressiveness**
- After “可是夹竹桃的毒很重，让他肚子很痛”: You could describe how the pain looked on his face or in his body. For example: 他脸色很白，一直用手捂着肚子。
- After “他吃灵芝以后就觉得很好，不再生病了”: You could add his surprise that the umbrella-shaped plant helped him so quickly. For example: 他很惊讶，说：“这个植物真有用！”

**Encouragement** You clearly show the cause-and-effect sequence: the poisonous plant makes Shennong ill, and the lingzhi helps him feel better. You also make a useful contrast between the star-shaped poisonous plant and the umbrella-shaped medicinal plant.

### Content & completeness (after the whole story)

- Missing scene: another person in brown came by and had a conversation with 神农
