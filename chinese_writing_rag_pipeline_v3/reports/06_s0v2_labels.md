# Step 6 report: her comments on the previous system's feedback (S0)

- 104 comments on 6 stories: Story 1 = mengmu_samples#4, Story 2 = mengmu_samples#10, Story 3 = mengmu_samples#12, Story 4 = shennong_samples#4, Story 5 = shennong_samples#8, Story 6 = shennong_samples#12
- model gpt-5.6-terra (medium), prompt 27ecaadea9

## What her comments say (a comment can carry several tags)

| Tag | Comments | Meaning |
|---|---|---|
| miscategorized | 29 | the item is in the wrong section or category (e.g. should be Grammar, not Vocabulary) |
| partial_sentence | 26 | the feedback shows a partial / truncated sentence that confuses |
| incorrect_correction | 23 | the correction (after →) is wrong, ungrammatical, or still contains an error |
| missed_error | 20 | she points out an error the system did not flag |
| bad_suggestion | 13 | a vocabulary suggestion is unnecessary, inappropriate, or changes the meaning |
| explanation_needed | 12 | the correction is right but the explanation is missing, wrong or should be improved |
| alternative | 9 | she offers an alternative correction or wording, without saying the item is wrong |
| false_positive | 7 | the flagged text is not an error / no correction needed / the original is fine |
| other | 4 | anything else |
| duplicate | 3 | the item repeats another item |
| bad_expressiveness | 3 | an expressiveness idea is unnecessary, redundant, or inappropriate |
| content_problem | 3 | the end-of-story content check missed a scene, is wrong, or is unclear |

## By section

| Section | false_positive | incorrect_correction | partial_sentence | miscategorized | duplicate | missed_error | explanation_needed | bad_suggestion | bad_expressiveness | content_problem | alternative | other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Grammar | 1 | 5 | 11 | 4 | 1 | 3 | 6 | 2 |  |  | 3 |  |
| Vocabulary | 4 | 13 | 6 | 9 | 2 | 8 | 6 | 11 |  |  | 3 | 1 |
| Coherence | 2 | 4 | 7 | 12 |  | 8 |  |  |  |  | 3 | 2 |
| Content |  |  | 1 | 1 |  |  |  |  |  |  |  |  |
| Other |  | 1 | 1 | 3 |  |  |  |  |  |  |  | 1 |
| Expressiveness |  |  |  |  |  |  |  |  | 3 |  |  |  |
| Content & completeness |  |  |  |  |  | 1 |  |  |  | 3 |  |  |

## The previous system (S0), measured on these 6 stories (18 scenes)

- lines shown in correction sections (approximate count of '→' lines, vocabulary suggestions included): 133
- comments saying **not an error**: 7 -> 0.39 per scene
- comments saying the **correction is wrong**: 23 -> 1.28 per scene
- comments about **partial sentences**: 26; **miscategorized**: 29; **duplicates**: 3; **missed errors** she added: 20

These are lower bounds: she commented on what she noticed, not necessarily every item.

## Every comment

- mengmu_samples#4 scene 1 [Grammar] `古代的时候` → `在古代` — **explanation_needed** — Explain that 古代的时候 is redundant because both 古代 and 的时候 express time.
- mengmu_samples#4 scene 1 [Grammar] `…天在墓地祭拜了` → `…天在墓地祭拜` — **partial_sentence** — The displayed correction is a partial sentence and may cause confusion.
- mengmu_samples#4 scene 1 [Grammar] `…母从早到晚都找工作` → `…母从早到晚都在找工作` — **partial_sentence** — The feedback uses a partial sentence, which may cause confusion.
- mengmu_samples#4 scene 1 [Grammar] `他们搬了到别一个城市找…` → `他们搬了别一个城市找…` — **duplicate, incorrect_correction, miscategorized** — The two items repeat the same error, and the second should be treated as an error rather than a suggestion.
- mengmu_samples#4 scene 1 [Vocabulary] `…和孟母住了在靠墓地的家` → `…和孟母住了在靠近墓地的家` — **false_positive, incorrect_correction, miscategorized** — The vocabulary change is only a suggestion, while the corrected sentence still has a misleading grammar error.
- mengmu_samples#4 scene 1 [Vocabulary] `他们搬了到别一个城市找工…` → `他们搬了到另一个城市找工…` — **partial_sentence** — The displayed sentence is truncated and may cause confusion.
- mengmu_samples#4 scene 1 [Vocabulary] `墓地` → `墓园: a slightly more formal word for a ce` — **bad_suggestion** — The vocabulary alternatives are inappropriate and unnecessary because the original words are better.
- mengmu_samples#4 scene 1 [Coherence] `孩子` → `孟子` — **missed_error** — The feedback missed that 孩子 is an unclear reference and should be 孟子.
- mengmu_samples#4 scene 2 [Grammar] `…要又一个次搬了家` → `…要又一个次搬家` — **incorrect_correction** — The corrected sentence is still grammatically incorrect and may mislead students.
- mengmu_samples#4 scene 2 [Vocabulary] `孟母找到工作` → `孟母找到了工作` — **missed_error** — The feedback missed that generic 人 should be changed to 人们 when used as the subject.
- mengmu_samples#4 scene 2 [Vocabulary] `孟母找到工作` → `孟母找到了工作` — **miscategorized** — This item should be classified as Grammar or Coherence (temporality), not Vocabulary.
- mengmu_samples#4 scene 2 [Coherence] `孟子和妈妈要又一个次搬了家` → `孟子和妈妈要再一次搬了家` — **incorrect_correction** — The corrected sentence is still grammatically wrong; it should be 要再搬一次家.
- mengmu_samples#4 scene 2 [Expressiveness] `Add a small detail about the noise and M` → `` — **bad_expressiveness** — The suggested detail about Mengzi being tired is redundant because the original already implies it.
- mengmu_samples#4 scene 3 [Grammar] `孟子学习馆学了十…` → `孟子在学习馆学了十…` — **partial_sentence** — The feedback displays a truncated sentence, which may confuse the learner.
- mengmu_samples#4 scene 3 [Vocabulary] `…在那个商店也找了到工作` → `…在那个商店也找到了到工作` — **incorrect_correction, miscategorized, explanation_needed** — This should be a Grammar item: the correction still has an extra 到, and the issue is the placement of 了 rather than 找到 versus 找.
- mengmu_samples#4 scene 3 [Coherence] `他成为很有名的哲人` → `他成为了很有名的哲人` — **miscategorized** — This suggestion should be placed under Coherence (temporality), not Vocabulary.
- mengmu_samples#4 scene 3 [Vocabulary] `好处` → `` — **bad_suggestion, incorrect_correction** — The suggested wording does not fit the context and cannot directly replace the target word, since 好处的哲人 is incorrect.
- mengmu_samples#4 scene 3 [Coherence] `他成为很有名的…` → `成为很有名的…` — **missed_error** — The feedback missed that the second 他的 is redundant in “他的学习和他的旅行经验.”
- mengmu_samples#4 scene 3 [Content & completeness] `After they leave the graveyard area` → `` — **content_problem, missed_error** — The feedback misses the scene where Mengmu moves a third time to live near a school.
- mengmu_samples#10 scene 1 [Other] `跟妈妈搬家` → `跟妈妈搬家了` — **miscategorized, other** — This is an error rather than a suggestion and should be placed under Grammar or temporal Coherence.
- mengmu_samples#10 scene 2 [Coherence] `…子思老师的家，跟子思老师住` → `…子思老师的家住` — **incorrect_correction, partial_sentence, miscategorized, alternative** — The correction is incomplete and still ungrammatical; it should be 搬到子思老师的家 and belong in Coherence.
- mengmu_samples#10 scene 2 [Vocabulary] `害得孟子的心气` → `伤了孟子的心气` — **incorrect_correction, explanation_needed** — The proposed correction is still unnatural, and the explanation should state that 害得 requires a person followed by a harmful result.
- mengmu_samples#10 scene 2 [Vocabulary] `教` → `教导` — **missed_error** — The feedback missed a vocabulary suggestion to change 教 to 教导.
- mengmu_samples#10 scene 2 [Coherence] `他老是读书` → `所以他老是读书` — **missed_error, alternative, other** — The teacher says 所以 is required rather than optional, 老是 should be changed to 一直 in Vocabulary, and 只好 could be added before 一直读书.
- mengmu_samples#10 scene 3 [Grammar] `孟子从五岁一直学哲学` → `孟子从五岁起一直学哲学` — **alternative** — She suggests 从五岁开始 as an alternative way to express starting from an age.
- mengmu_samples#10 scene 3 [Grammar] `难怪他成为很有名的哲学…` → `难怪他成为了很有名的哲学…` — **partial_sentence** — The displayed correction is a partial sentence and may cause confusion.
- mengmu_samples#10 scene 3 [Vocabulary] `就是看哲学书` → `就是看到哲学书` — **false_positive, incorrect_correction, alternative** — The original wording is correct, and the AI should use 读哲学书 rather than 看到哲学书.
- mengmu_samples#10 scene 3 [Content & completeness] `add that 孟母 moves them near a school bef` → `` — **content_problem** — The feedback should also explain why Mengmu decides to move away from the market area.
- mengmu_samples#12 scene 1 [Grammar] `Grammar` → `` — **missed_error** — The feedback missed adding 在 before 古代 and 都 in 从早到晚都很吵.
- mengmu_samples#12 scene 1 [Vocabulary] `所以孟母决定他们会搬家` → `所以孟母决定搬家` — **miscategorized** — The deletion of 他们 belongs under Coherence (reference), while the deletion of 会 belongs under Grammar because 决定 already implies a future plan.
- mengmu_samples#12 scene 1 [Coherence] `孟子跟孟母住在墓…` → `` — **partial_sentence** — The displayed partial sentence is confusing.
- mengmu_samples#12 scene 1 [Coherence] `孟子跟孟母住在墓…` → `` — **partial_sentence** — The referenced sentence is truncated, which may confuse the learner.
- mengmu_samples#12 scene 1 [Coherence] `可是孟母注意` → `可是孟母注意到` — **miscategorized** — The teacher says this item should be in Vocabulary rather than Coherence.
- mengmu_samples#12 scene 2 [Grammar] `…母只好一直陪孟子` → `…母只好一直陪着孟子` — **partial_sentence** — The displayed partial sentence is confusing.
- mengmu_samples#12 scene 2 [Grammar] `…母只好一直陪孟子` → `…母只好一直陪着孟子` — **explanation_needed** — Add that 着 marks a durative action.
- mengmu_samples#12 scene 2 [Vocabulary] `而是让他觉得很伤…` → `而且让他觉得很伤…` — **partial_sentence** — The displayed sentence is truncated, which may cause confusion.
- mengmu_samples#12 scene 2 [Vocabulary] `不高兴` → `难过; 孤单` — **incorrect_correction, explanation_needed** — The suggested words need 很 and cannot directly replace 不高兴 as presented.
- mengmu_samples#12 scene 2 [Expressiveness] `每天有很多商人卖东西，很热闹` → `` — **bad_expressiveness** — The suggested lively market detail does not fit the preceding statement that the city is dangerous.
- mengmu_samples#12 scene 2 [Expressiveness] `他觉得很孤单，也很想朋友` → `` — **bad_expressiveness** — The suggested detail conflicts with the preceding statement that Mengzi has no friends.
- mengmu_samples#12 scene 3 [Vocabulary] `他成为中国的一…` → `他会成为中国的一…` — **partial_sentence, incorrect_correction** — The displayed sentence is truncated and confusing, and adding 会 is wrong because Mengzi had already become a philosopher.
- mengmu_samples#12 scene 3 [Vocabulary] `格外` → `` — **bad_suggestion** — “格外” is inappropriate because it describes a temporary state, whereas “philosopher” is a stable identity.
- mengmu_samples#12 scene 3 [Coherence] `了 / 着 / 在` → `` — **miscategorized** — She says this category should be labeled “Temporality.”
- mengmu_samples#12 scene 3 [Coherence] `才五岁孟子开始学哲…` → `才五岁时孟子开始学哲…` — **partial_sentence, false_positive** — The sentence is truncated and confusing, and 才五岁 is already correct without 时.
- shennong_samples#4 scene 1 [Grammar] `写了` → `写下了` — **missed_error, alternative** — The teacher notes that 写了 should be 写下了 and suggests using 吃到了 for both plant-eating sentences.
- shennong_samples#4 scene 1 [Grammar] `古代的时候` → `在古代` — **explanation_needed** — The correction is right, but the explanation should say that 古代的时候 is redundant because both parts indicate time.
- shennong_samples#4 scene 1 [Grammar] `也不知道什么植物对你…` → `也不了解什么植物对你…` — **partial_sentence** — The displayed sentence is truncated and may cause confusion.
- shennong_samples#4 scene 1 [Grammar] `所以神农去了吃每种植物` → `所以神农去吃每种植物` — **incorrect_correction, miscategorized** — The correction should move 了 to 去吃了 rather than delete it, and this item belongs in Grammar.
- shennong_samples#4 scene 1 [Vocabulary] `所以神农去了吃每种植物` → `所以神农去了每种植物` — **incorrect_correction, miscategorized** — The suggested correction is still ungrammatical, and 去了吃 should be treated as an error rather than a suggestion.
- shennong_samples#4 scene 1 [Coherence] `他的名字是神农: 神农` → `` — **false_positive** — The reference correction should be deleted because the man was already introduced as 有一个男人.
- shennong_samples#4 scene 1 [Coherence] `所以神农去了吃每种植…` → `所以去了吃每种植…` — **partial_sentence, incorrect_correction** — The feedback shows a confusing truncated sentence, and its corrected version is still grammatically wrong and misleading.
- shennong_samples#4 scene 1 [Coherence] `跟他的朋友聊到他吃的植物了` → `…跟他的朋友聊他吃的植物了` — **miscategorized** — This feedback item should be in the Grammar section, not Coherence.
- shennong_samples#4 scene 1 [Coherence] `…到他吃的植物了` → `…到他吃的植物` — **partial_sentence, miscategorized** — The item is a confusing partial sentence and should be placed in Grammar.
- shennong_samples#4 scene 1 [Content] `…多人不知道哪个植物好吃` → `…多人不知道哪种植物好吃` — **partial_sentence, miscategorized** — The displayed sentence fragment is confusing, and the measure-word correction should be under Vocabulary rather than Content.
- shennong_samples#4 scene 2 [Vocabulary] `这就要看你的口味了` → `这就要看你的口味了` — **false_positive, explanation_needed** — The item should not be marked because the original and correction are identical, and the explanation wrongly treats this as a 看-versus-看到 issue rather than the fixed structure “这就要看……了”.
- shennong_samples#4 scene 2 [Vocabulary] `一个别的人问神农` → `一个另外一个人问神农` — **incorrect_correction, alternative** — The correction is still grammatically wrong; it should be “另外一个人,” not “一个另外一个人.”
- shennong_samples#4 scene 2 [Vocabulary] `哪个植物对你的身…` → `哪种植物对你的身…` — **partial_sentence** — The feedback displays a truncated sentence, which may cause confusion.
- shennong_samples#4 scene 2 [Vocabulary] `一个别的人问神农` → `一个另外一个人问神农` — **incorrect_correction** — The correction is still ungrammatical; it should be 另外一个人, not 一个另外一个人.
- shennong_samples#4 scene 2 [Vocabulary] `哪个植物对你的身…` → `哪种植物对你的身…` — **duplicate, other** — The same 种 replacement is labelled as a suggestion here but as an error earlier.
- shennong_samples#4 scene 2 [Coherence] `` → `` — **missed_error** — The feedback missed that “你的” unnecessarily introduces a listener and that repeating “一个别的人” makes the people unclear.
- shennong_samples#4 scene 3 [Grammar] `名字是夹竹桃` → `它的名字是夹竹桃` — **false_positive, incorrect_correction** — The original zero-anaphora phrasing is correct, and adding 它的 is unnecessary in this clause.
- shennong_samples#4 scene 3 [Grammar] `…种植物对我的脑有坏处` → `…种植物对我的大脑有坏处` — **partial_sentence** — The displayed sentence is partial and may confuse the learner.
- shennong_samples#4 scene 3 [Vocabulary] `一个灵芝和一个男…` → `一株灵芝和一个男…` — **partial_sentence, missed_error** — The displayed sentence is truncated and confusing, and the sentence should separate the moving man from the stationary lingzhi.
- shennong_samples#4 scene 3 [Vocabulary] `小心` → `当心` — **bad_suggestion** — “当心” is inappropriate because it warns against a danger, while eating a plant is not itself the danger.
- shennong_samples#4 scene 3 [Coherence] `No corrections` → `` — **missed_error** — The feedback missed that 你的 unnecessarily introduces the listener and may cause confusion.
- shennong_samples#4 scene 3 [Other] `因为夹竹桃有毒` → `夹竹桃有毒` — **incorrect_correction, miscategorized** — The correction is wrong because 因为 is needed, and this item belongs in Coherence (connectors).
- shennong_samples#4 scene 3 [Content & completeness] `After 神农 eats 夹竹桃 and before he receives` → `` — **content_problem** — The content check missed the tea and plant-recording scenes and the conversation between Shennong and the man in brown.
- shennong_samples#8 scene 1 [Grammar] `古代的时候` → `在古代` — **explanation_needed** — Explain that 古代 already expresses a time, so adding 的时候 is redundant.
- shennong_samples#8 scene 1 [Coherence] `哪些植物不能吃` → `哪些不能吃` — **miscategorized** — This suggestion belongs in Coherence (reference), not Grammar.
- shennong_samples#8 scene 1 [Vocabulary] `一看很多人正在吃…` → `一看到很多人正在吃…` — **incorrect_correction, miscategorized, missed_error** — Delete 一 because 一V requires a following 就-clause, and this belongs in Grammar.
- shennong_samples#8 scene 1 [Vocabulary] `路上` → `山路` — **incorrect_correction, alternative** — The suggestion should be marked as 山路上 because it uses a different structure and cannot directly replace 路上.
- shennong_samples#8 scene 1 [Coherence] `了 / 着 / 在` → `` — **miscategorized** — This item should be categorized as Temporality rather than Coherence.
- shennong_samples#8 scene 1 [Coherence] `神农想帮别人` → `神农想帮助别人` — **miscategorized, missed_error** — This belongs in Vocabulary, and the feedback missed that 别人 should be 他们 to refer clearly to 一些人.
- shennong_samples#8 scene 2 [Vocabulary] `一些植物毒得很` → `一些植物有毒得很` — **duplicate** — The two suggestions for this phrase are repetitive.
- shennong_samples#8 scene 2 [Vocabulary] `尝` → `品尝` — **bad_suggestion** — “品尝” is inappropriate here because it means tasting food with enjoyment or appreciation.
- shennong_samples#8 scene 3 [Grammar] `一些植物不能吃` → `一些不能吃` — **miscategorized** — This suggestion belongs in Coherence (reference), not Grammar.
- shennong_samples#8 scene 3 [Vocabulary] `告诉` → `说明` — **missed_error** — The feedback missed that 别人 is inappropriate here; it should be 大家 or 人们.
- shennong_samples#8 scene 3 [Vocabulary] `这就要看你想不想生病…` → `这就要看你想不想生病…` — **false_positive, explanation_needed** — The original and correction are identical, and the explanation should identify “这就要看……了” as a fixed structure rather than contrast 看 and 看到.
- shennong_samples#8 scene 3 [Vocabulary] `一个人` → `男人` — **miscategorized** — This suggestion belongs in Coherence (reference), because a newly appearing character should be briefly introduced.
- shennong_samples#8 scene 3 [Vocabulary] `告诉` → `说明: This means to explain something clea` — **incorrect_correction, bad_suggestion** — Both vocabulary suggestions change the meaning, and 说明 cannot directly take an indirect object without 向.
- shennong_samples#8 scene 3 [Other] `麻烦我们可以吃什…` → `请问我们可以吃什…` — **partial_sentence, miscategorized** — The item is truncated and should be placed in Grammar rather than Other.
- shennong_samples#12 scene 1 [Grammar] `也什么植物不能…` → `也不知道什么植物不能…` — **explanation_needed** — Add an explanation that 也 should be followed by a verb phrase, such as 也不知道.
- shennong_samples#12 scene 1 [Grammar] `也什么植物不能吃` → `也什麼植物不能吃` — **bad_suggestion** — The traditional-character suggestion is irrelevant and should be deleted.
- shennong_samples#12 scene 1 [Grammar] `吃不安全的植物对你的…` → `吃有毒的植物对你的…` — **partial_sentence, miscategorized** — The correction is shown as a confusing partial sentence and belongs in Vocabulary, not Grammar.
- shennong_samples#12 scene 1 [Grammar] `吃不安全的植物对你的身体有…` → `吃不安全的食品对你的身体有…` — **partial_sentence, bad_suggestion** — The suggestion is a confusing partial sentence, and 食品 is inappropriate because the context is about plants rather than processed food.
- shennong_samples#12 scene 1 [Grammar] `…安全的植物对你的身体有坏处` → `…安全的植物对人的身体有坏处` — **partial_sentence** — The feedback displays a partial sentence, which may cause confusion.
- shennong_samples#12 scene 1 [Vocabulary] `古代的人很不知道什么植…` → `古代的人不知道什么植…` — **partial_sentence, explanation_needed** — The displayed sentence is truncated, and the feedback should explain that 知道 is not modified by 很 because it is an all-or-none state.
- shennong_samples#12 scene 1 [Vocabulary] `常吃不安全的植物` → `…常吃不安全的食物` — **bad_suggestion** — “食物” is inappropriate because the context specifically concerns plants, not food in general.
- shennong_samples#12 scene 1 [Vocabulary] `很麻烦的情况` → `这是一个很麻烦的情况` — **miscategorized** — This item should be in the Grammar section, not Vocabulary.
- shennong_samples#12 scene 1 [Vocabulary] `找出` → `` — **bad_suggestion** — “找出” is inappropriate because it changes Shennong’s goal from solving the problem to finding the problem.
- shennong_samples#12 scene 1 [Coherence] `古代的人` → `` — **missed_error** — The feedback missed that 古代的人 is redundant because 很久以前 already establishes the time period.
- shennong_samples#12 scene 2 [Vocabulary] `神农写他的主意` → `神农写下了他的主意` — **miscategorized, missed_error** — The 写下 correction belongs in Grammar, and 主意 should be corrected to 发现.
- shennong_samples#12 scene 2 [Vocabulary] `神农遇到了一个黄色的花` → `神农遇到了一朵黄色的花` — **missed_error** — The feedback missed that 遇到 is unsuitable for a static flower and should be 看到.
- shennong_samples#12 scene 2 [Vocabulary] `聪明` → `了不起: means very admirable, and is good f` — **bad_suggestion** — The suggested replacement words change the original meaning of 聪明.
- shennong_samples#12 scene 2 [Vocabulary] `不舒服` → `痛苦` — **bad_suggestion** — “痛苦” is too strong for this context.
- shennong_samples#12 scene 2 [Coherence] `No corrections.` → `` — **missed_error** — The feedback missed adding a time phrase before the new event.
- shennong_samples#12 scene 3 [Grammar] `写` → `写下` — **missed_error** — The feedback missed correcting 写 to 写下.
- shennong_samples#12 scene 3 [Grammar] `…友哪一个植物能不能吃` → `…友哪一个植物能吃，哪一种不能吃` — **partial_sentence, incorrect_correction, explanation_needed, alternative** — The item is truncated, needs a clearer explanation of Wh- versus yes/no questions, and should consistently use 哪一种 in both clauses.
- shennong_samples#12 scene 3 [Vocabulary] `别人` → `一个穿蓝色衣服的人` — **missed_error** — “别人” refers to all other people, so it should be replaced with a specific person.
- shennong_samples#12 scene 3 [Vocabulary] `信息` → `资料; 内容` — **bad_suggestion** — The suggested replacements 资料 and 内容 do not fit the context.
- shennong_samples#12 scene 3 [Coherence] `了 / 着 / 在` → `` — **miscategorized** — This feedback belongs under temporality rather than coherence.
- shennong_samples#12 scene 3 [Coherence] `了 / 着 / 在` → `` — **miscategorized** — The teacher says this item should be categorized as temporality rather than coherence.
- shennong_samples#12 scene 3 [Coherence] `…就觉得比较好` → `…就觉得比较好吃` — **other** — The teacher says this item should be labeled “temporality.”
- shennong_samples#12 scene 3 [Coherence] `…就觉得比较好` → `…就觉得比较好吃` — **incorrect_correction, alternative** — The correction is misaligned and contextually wrong; it should mean that Shennong felt much better, not that something tasted delicious.
- shennong_samples#12 scene 3 [Coherence] `…他的朋友哪一个植物能不能吃` → `…他的朋友哪一种植物能不能吃` — **partial_sentence, miscategorized** — The item is a confusing partial sentence and should be categorized as Vocabulary because it concerns the measure word choice.
