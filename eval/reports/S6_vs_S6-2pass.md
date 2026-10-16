# S6-S6-2pass: Two-pass retrieval with structured output

- **Before (S6)**: Teacher's extra rules and definitions. The teacher's 8 additional rules (extra rules.docx + general rules from her S5 comments) shown with the places they may apply; her 25 revised rule definitions on the rule cards; end-of-story feedback without scene numbers; vocabulary suggestions aimed at precision rather than formality.
- **After (S6-2pass)**: Two-pass retrieval with structured output. S6, but each scene runs in two passes: pass 1 lists candidate errors as JSON (span, category, rule); the teacher's rule card and labelled corrections are retrieved for each candidate; pass 2 writes the feedback as JSON. Every quoted span is checked against the student's text.


## mengmu_samples#10 (mengmu_san_qian)

### Scene 1

> 孟子小的时候，从早到晚都跟朋友玩。孟子和他的朋友喜欢玩在墓地里，装祭拜。孟子五岁的时候，跟妈妈搬家。他们搬家不是因为孟子玩得太多，而是因为妈妈认为他们的家离墓地太近。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 喜欢玩在墓地里：喜欢在墓地里玩，Place phrases normally come before the main verb they modify.
> - 装祭拜：假装祭拜，假装 can be followed directly by an action to mean pretending to do it; 装 does not fit naturally before this verb phrase.
> - 跟妈妈：妈妈带着他，When a mother moves home together with her child, use 带着 to show that the mother takes the child with her; 跟孟子搬家 is an incorrect word choice for this meaning.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 孟子小的时候，从早到晚都跟朋友玩。：有一个小男孩叫孟子，他从早到晚都跟朋友玩。，On first mention, introduce the character with a full noun phrase that says who he is before using his name or a pronoun.
> - Coherence (Reference): 孟子和他的朋友：他和朋友，Use a pronoun for a close re-occurrence when the referent has just been named and no other singular character competes with it.
> - Coherence (Temporality): 搬家：搬了家，Use 了 for this completed moving event in the past.
> - Expressiveness: When describing the cemetery games, add one concrete action to show what the children copied, such as “他们学着大人低头祭拜。”
> - Expressiveness: Add Mengzi’s feeling about the game to make his motivation clearer, such as “孟子觉得这样很好玩。”
> - Expressiveness: At the end, add the mother’s worried thought, such as “妈妈心想：这儿不适合孩子长大。”
> 
> **Encouragement**
> - You clearly show Mengzi’s daily habit with “从早到晚,” which makes the scene easy to imagine. The contrast structure “不是……而是……” also explains the mother’s reason for moving very clearly.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 装祭拜：假装祭拜，“装” does not naturally take “祭拜” as its object here. “假装” can introduce an action that someone pretends to perform.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 孟子和他的朋友：他和朋友，Use a pronoun for a close re-occurrence when the referent was named in the immediately preceding sentence and no competing character makes it unclear.
> - Coherence (Reference): 孟子五岁的时候：他五岁的时候，Use a pronoun for a close re-occurrence: the preceding sentence is still about Mengzi, so “他” is unambiguous.
> - Coherence (Temporality): 跟妈妈搬家：跟妈妈搬了家，Use completed-action “了” because this sentence recounts one finished move at the age of five.
> - Expressiveness: After “从早到晚都跟朋友玩”, add a concrete activity to show what the children did, for example: “他们常常在墓地里跑来跑去。”.
> - Expressiveness: At “假装祭拜”, add Mengzi’s feeling to make his reason clearer, for example: “孟子觉得这样很好玩。”.
> - Expressiveness: After the final reason for moving, show the mother’s worry with a short thought or quotation, for example: “妈妈很着急，心想：‘这儿不适合孩子。’”.
> 
> **Encouragement**
> You clearly establish Mengzi’s childhood setting and give a logical reason for the family’s move. The contrast pattern “不是……，而是……” is used effectively to explain the reason.

### Scene 2

> 妈妈认为，住离墓地太近，害得孟子的心气。孟子和孟母搬到子思老师的家，跟子思老师住。孟母帮子思打扫房间和做饭。子思帮孟母教她的儿子。因为孟子现在没有朋友，他老是读书。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 住离墓地太近，害得孟子的心气：住在离墓地太近的地方，会影响孟子的心情，住 needs 在 before a location, and the original use of 害得 does not contain a complete result clause; 影响 can directly take the noun 心情.
> - 他老是读书：他一直读书，老是 usually expresses annoyance or criticism about a repeated action; 一直 is neutral and fits regular studying.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 跟子思老师住：跟他住，Use a pronoun for a close re-occurrence: 子思老师 has just been named in the same sentence and no other male person competes as the referent.
> - Coherence (Reference): 教她的儿子：教儿子，Use zero form for a re-occurring person within the same clause: 孟母 has already been named, so the possessive pronoun is unnecessary.
> - Coherence (Temporality): 孟子和孟母搬到子思老师的家：孟子和孟母搬到了子思老师的家，Use 了 for the completed moving action in this past narrative.
> - Coherence (Conjunction): 因为孟子现在没有朋友，：因为孟子现在没有朋友，所以，Use 因为……所以…… to mark the cause-and-effect relation between having no friends and reading regularly.
> - Expressiveness: After the move, add one quiet detail about the new study environment, such as: “新家很安静，桌上放着几本书。”
> - Expressiveness: Show Meng母’s reaction when she sees her son study: “孟母看见孟子认真读书，心里很高兴。”
> - Expressiveness: Add a short line of speech from the mother after the tutoring begins: “这儿很适合学习。”
> 
> **Encouragement**
> - You clearly show how the move changes Meng子’s daily life, and you include helpful actions from both 孟母 and 子思老师. The final sentence also gives a clear reason for why 孟子 begins to read more.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 住离墓地太近：住的地方离墓地太近，A distance phrase with 离 needs a place noun as its subject. 住 cannot directly take 离墓地太近 as its complement.
> - 害得孟子的心气：害得孟子心情不好，害得 must be followed by the affected person and a clearly harmful result. The original ends with a noun phrase and does not state the harmful result.
> - 打扫房间和做饭：打扫房间、做饭，和 links nouns or noun phrases, not two verb phrases. Use a pause mark or 也 to link two actions.
> - 老是：一直，老是 usually carries a negative, complaining tone. Reading is neutral here, so 一直 expresses continued reading without that negative connotation.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 妈妈：她，Use a pronoun for a close re-occurrence when the character was mentioned in the immediately preceding context and no competing female referent makes it unclear.
> - Coherence (Temporality): 搬到：搬到了，Use 了 for this completed moving action: the following sentence shows that the move has already happened and they are now living with the teacher.
> - Coherence (Conjunction): 因为孟子现在没有朋友，他老是读书：因为孟子现在没有朋友，所以他老是读书，Because this sentence presents a cause and its result, use the paired connector 因为……所以…… to make the cause-and-effect relation explicit.
> - Expressiveness: After the first sentence, add a concrete detail about the cemetery atmosphere to show why it affects Mengzi: “墓地旁边常常有人哭，声音让孟子觉得害怕。”
> - Expressiveness: After the teacher begins teaching Mengzi, add a short line of dialogue to show his guidance: “子思说：‘读书的时候，要认真想一想。’”
> - Expressiveness: At the end, describe Mengzi’s quiet action or feeling while reading: “孟子一个人坐在桌前，安静地读书。”
> 
> **Encouragement**
> You clearly connect the move to a new learning environment, and you include both Mengzi’s mother and his teacher in the scene. Your sentences also show a logical reason for Mengzi’s reading.

### Scene 3

> 子思认为，对孩子来说，读书最重要，特别是学哲学。孟子不是练习写文章，就是看哲学书。孟子从五岁一直学哲学。他才五岁就学哲学，难怪他成为很有名的哲学家。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - Nothing to flag.
> 
> **Vocabulary Suggestions**
> - 看 -- “就是看哲学书”：研读，emphasizes careful, in-depth reading that suits philosophy books.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 孟子从五岁一直学哲学：他从五岁一直学哲学，Use a pronoun for a close re-occurrence when the same character was named in the immediately preceding sentence and no competing character intervenes.
> - Coherence (Temporality): 他成为很有名的哲学家：他成为了很有名的哲学家，Use 了 with a completed change of state: becoming a philosopher is presented as an accomplished event in the narrative.
> - Expressiveness: After the first sentence, add a short line of quoted speech to show 子思’s teaching style: “子思对孟子说：‘学哲学要先认真读书。’”
> - Expressiveness: In the second sentence, add an action detail showing how hard 孟子 works: “他每天认真地练习写文章，还常常思考书里的问题。”
> - Expressiveness: Before the final sentence, add 孟子’s feeling about philosophy: “孟子觉得哲学很有意思，越学越喜欢。”
> 
> **Encouragement**
> - You used the pattern “不是……就是……” correctly to show Mengzi’s focused study routine.
> - The sentence with “才五岁就” effectively emphasizes that he began learning philosophy at a very young age.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 成为很有名的哲学家：成为了很有名的哲学家，This describes a completed achievement in Mengzi’s life, so the verb of change of state needs 了.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 孟子从五岁一直学哲学：他从五岁一直学哲学，Use a pronoun for a close re-occurrence: Mengzi was named in the immediately preceding sentence, and no competing male character appears there.
> - Expressiveness: After “看哲学书,” add a small reading detail to make his study visible, such as “认真地一页一页地看”.
> - Expressiveness: After “他才五岁就学哲学,” add an evaluative description of his unusual ability, such as “比同龄孩子懂得更多”.
> - Expressiveness: Near the ending, add Zisi’s reaction to show why Mengzi became well known, such as “子思很欣慰”.
> - Expressiveness: 
> 
> **Encouragement**
> You use the paired pattern “不是……就是……” correctly to show Mengzi’s daily study habits. The final use of “难怪” also creates a clear link between his early learning and his later success.

### End-of-story content feedback

#### S6 (before)

> **Content & Completeness**
> - After 孟母 decides that living near the graveyard is harmful, the story needs to show that 孟子 copied offering sacrifices every day, not only that he and his friends played there.
> - Between leaving the graveyard and moving near a school, the story needs the event where 孟母 and 孟子 live near a market and 孟子 imitates buying and selling every day.
> - After 孟子 imitates buying and selling near the market, the story needs to explain that 孟母 moves again because she is unhappy with this influence, before they move near the school.
> 
> **Overall Encouragement**
> - You clearly show how 孟子’s environment changes his behavior and how he eventually becomes a famous philosopher. The ending connects his studying to his future very well.

#### S6-2pass (after)

> **Content & Completeness**
> - After 孟母 moves away from the graveyard, the story needs the part where they live near a market and 孟子 copies people buying and selling every day.
> - The move from the market to a neighborhood near a school is missing. Before 孟子 begins studying every day, explain that 孟母 moves again because the market behavior is not a good influence.
> 
> **Overall Encouragement**
> - You clearly included the graveyard beginning, 孟母’s concern, and the ending where 孟子 becomes a famous philosopher. The story also gives a clear reason why he starts studying seriously.

## mengmu_samples#32 (mengmu_san_qian)

### Scene 1

> 有一天孟子去了墓地玩儿，但是他妈妈觉得这是不合适的地方让孩子玩，所以她决定了他们会搬家找更好的地方。她恐怕儿子的童年不会幸福，而且住在这儿教育不太好。因为她望子成龙，所以她会一直搬家才能找到质量好的教育。然后他们搬到了离城市更近的地方。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 这是不合适的地方让孩子玩：这不是适合孩子玩的地方，Use “适合 + person + action” to say that a place is suitable for someone to do something; the original word order does not naturally express this meaning.
> - 她恐怕儿子的童年不会幸福：她担心儿子的童年不会幸福，“恐怕” cannot follow another subject to mean that person is worried; use “担心” for a character’s fear or concern.
> - 找到质量好的教育：找到能提供优质教育的地方，“找到” should take something discoverable, such as a place or school; education is something a child receives rather than an object one finds.
> 
> **Vocabulary Suggestions**
> - 更好的 -- “找更好的地方”：更适合孩子成长的，specifies exactly why the new place would be better for the child.
> - 不太好 -- “住在这儿教育不太好”：教育质量不太理想，makes clear that the concern is the quality of education rather than the place in general.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 有一天孟子去了墓地玩儿：有一天，一个叫孟子的小男孩去了墓地玩儿，On first mention, introduce a character with a full noun phrase rather than only a name, so the reader knows who he is.
> - Coherence (Temporality): 决定了：决定，“决定” is a mental-state verb, so it normally takes the zero particle rather than completed-action “了”.
> - Expressiveness: At the cemetery, add a small action to show why the mother worries, such as “孟子看见有人来祭拜，就觉得很好玩。”
> - Expressiveness: Show the mother’s feeling with an action or thought after she judges the place, such as “孟母皱着眉头，心里很着急。”
> - Expressiveness: Add one detail about the new neighbourhood after the final sentence, such as “新家附近从早到晚都很热闹。”
> 
> **Encouragement**
> - You used the cause-and-effect pattern with “因为……所以……” clearly, and the completed action in “搬到了” is used well.
> - The scene also makes the mother’s goal easy to understand: she wants to find a better environment for her son.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 不合适的地方让孩子玩：不适合孩子玩儿的地方，The verb phrase modifying the noun must come before the noun and take 的. This revision makes the whole phrase modify 地方.
> - 住在这儿教育不太好：这儿的教育条件也不太好，The location needs to be linked to 教育 with an attributive phrase. 教育条件 clearly names what is not good in this place.
> - 会一直搬家才能：得一直搬家，才能，A necessary-condition pattern uses the action before 才能 to lead to the result. 得 expresses necessity here, while 会 only marks a future possibility and does not form this conditional relationship naturally.
> - 找到质量好的教育：获得高质量的教育，找到 is used for locating a person, object, or place; education is something a child receives or obtains. 获得 is the appropriate verb, and 高质量的 is the usual modifier for education.
> 
> **Vocabulary Suggestions**
> - 地方 -- “找更好的地方”：环境，This identifies the “place” more precisely as the surroundings in which the child will grow up.；更适合孩子成长的环境，This states exactly why the new place is better while keeping the intended meaning.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 孟子：一个叫孟子的小男孩，On first mention, introduce a character with a name plus a brief noun phrase explaining who the person is, rather than giving only the name.
> - Coherence (Temporality): 决定了：决定，决定 is a mental-state verb, so it normally takes the zero particle rather than 了.
> - Expressiveness: At the cemetery scene, add one visual detail about the mourners to make the setting easier to imagine, such as “墓地里有人低着头哭”.
> - Expressiveness: After the mother worries about her son, add her inner thought or quoted speech to show her feelings, such as “如果一直住在这儿，麻烦会越来越多。”.
> - Expressiveness: When they reach the new area, describe one lively sound or sight, such as “街上从早到晚都很热闹”. This can make the contrast with the cemetery more vivid.
> 
> **Encouragement**
> The scene has a clear sequence from the cemetery to the family’s move. You also clearly show the mother’s concern for her child and give a reason for her decision.

### Scene 2

> 他们住才一月就又搬家。古代的时候，一般人不喜欢卖东西的人。但是孟子老是跟这些卖东西的人常常玩儿，害得妈妈着急得很，因为她恐怕儿子会成为跟他们很像。她告诉了孟子：他们不是朋友，而是不好的人。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 他们住才一月：他们才住了一个月，The time adverbial with 才 comes before the verb, and a completed period of living needs 了; use the measure word 个 with 月.
> - 古代的时候：在古代，Use 在古代 for this broad historical time setting; 古代的时候 is not the natural form here.
> - 老是跟这些卖东西的人常常玩儿：老是跟这些卖东西的人玩儿，老是 and 常常 both mark a repeated habit, so using both together is redundant.
> - 害得妈妈着急得很：让妈妈很着急，害得 requires a clearly harmful consequence, while being worried is better expressed with 让.
> - 她恐怕：她担心，恐怕 means “I am afraid that” when used with 我, or it introduces a whole clause without another subject; use 担心 when the mother is the subject who is worried.
> - 成为跟他们很像：变得跟他们很像，成为 needs a noun phrase describing an identity or role after it, while 变得 can be followed by an adjective phrase such as 跟他们很像.
> 
> **Vocabulary Suggestions**
> - 不好 -- “而是不好的人”：品行不好，specifies that the people’s character or behaviour is bad, rather than leaving 不好 vague.
> 
> **Coherence & Expressiveness**
> - Coherence (Temporality): 她告诉了孟子：她告诉孟子：A saying verb that introduces quoted speech takes the zero particle, not 了.
> - Coherence (Conjunction): 他们才住了一个月又搬家：他们才住了一个月，就又搬家了，Use 就 after 才住了一个月 to show the sequence and unexpected quick change.
> - Expressiveness: After describing the sellers, add a lively market detail to show why it attracts孟子, such as “街上有人大声叫卖，还有很多好吃的东西。”
> - Expressiveness: Show孟子 copying the sellers’ actions more specifically, such as “孟子学着他们的样子，大声喊：‘快来买东西！’”
> - Expressiveness: Add the mother’s internal reaction before her speech, such as “妈妈看见以后，心里更着急了。”
> 
> **Encouragement**
> - You clearly show that the mother is worried about how the new neighbourhood may influence孟子, and the direct speech at the end gives the scene a strong ending.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 住才一月：才住了一个月，The adverb 才 comes before the verb, and a duration normally uses a measure word: 一个 + 月.
> - 古代的时候：在古代，For the broad historical period, use 在古代 rather than 古代的时候.
> - 老是跟这些卖东西的人常常玩儿：老是跟这些卖东西的人玩儿，老是 and 常常 both mark habitual frequency, so using both together is redundant.
> - 她恐怕：她担心，恐怕 usually introduces a clause without a third-person subject, or follows 我. Use 担心 when describing what she is afraid may happen.
> - 成为跟他们很像：变得跟他们很像，成为 takes a noun phrase to express becoming an identity or role. Use 变得 before an adjective phrase describing a change of state.
> 
> **Vocabulary Suggestions**
> - 卖东西的人 -- “跟这些卖东西的人常常玩儿”：商人，This names the people more precisely as people who sell goods in the market.
> 
> **Coherence & Expressiveness**
> - Coherence (Temporality): 又搬家：又搬家了，Use 了 for the completed moving event in this past narrative.
> - Coherence (Temporality): 告诉了：告诉，A saying verb that introduces quoted speech normally uses the zero particle rather than 了.
> - Expressiveness: At the mother's worry, add an inner thought that makes her fear more vivid: “如果儿子每天都跟他们玩儿，他会学坏的。”
> - Expressiveness: Before describing Mengzi's actions, add one market detail to create a setting: “街上从早到晚都很热闹，商人不停地叫卖。”
> - Expressiveness: Make the mother's warning more personal with a short line of speech after the colon: “你应该好好学习，不要老是跟他们玩儿。”
> 
> **Encouragement**
> You clearly show a cause-and-effect relationship between Mengzi's behaviour and his mother's worry. The direct speech at the end also gives the scene a clear, understandable ending.

### Scene 3

> 你不是当数学家，而是当哲学家，不能当卖东西的人。所以他们又搬家。在他们第三个家，孟子学了怎么祭拜。妈妈感觉这个地方适合他们，告诉了孟子：我们找到了最后的家。在这儿妈妈让儿子从早到晚学习，他难怪成为有名的哲学家。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 所以他们又搬家：所以他们又搬了家，The move is a completed event in the narrative, so the separable verb needs the completion marker 了 after 搬.
> - 在他们第三个家：在他们的第三个家里，An ordinal noun phrase after a possessive needs 的, and 家里 clearly marks the location.
> - 告诉了孟子：告诉孟子，A speaking verb that introduces quoted speech takes the zero aspect form; do not add 了 here.
> - 成为有名的哲学家：成为了有名的哲学家，Becoming a philosopher is presented as a completed change of state, so it needs 了.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Conjunction): 在这儿妈妈让儿子从早到晚学习，他难怪成为了有名的哲学家：在这儿，妈妈让儿子从早到晚学习，所以他后来成为了有名的哲学家，Use 所以 to show the cause-and-effect relationship between studying every day and his later success; 后来 also clearly orders the later event.
> - Expressiveness: After “妈妈感觉这个地方适合他们,” add the mother’s happiness or relief, such as “妈妈很高兴，觉得这次终于搬对了。”
> - Expressiveness: Make the learning scene more visual by adding what Mengzi does, such as “孟子每天认真看书，还常常问老师问题。”
> - Expressiveness: Add a short line of dialogue after the final move to show the mother’s thoughts, such as “妈妈说：‘这儿的环境很适合你。’”
> 
> **Encouragement**
> - You clearly show the family’s final move and connect it to Mengzi’s later achievement. You also used a direct statement from the mother, which helps the scene feel like part of a story.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 搬家：搬了家，This is a completed move in the past, so the verb needs the perfective marker 了. With an object, the natural order is 搬了家.
> - 在他们第三个家：在他们的第三个家里，A possessive pronoun before an ordinal and measure word normally takes 的. Adding 里 also makes the location phrase explicit.
> - 从早到晚学习：从早到晚都学习，The total-time expression 从早到晚 requires 都 before the verb to show that the action continues throughout the whole period.
> - 成为：成为了，Becoming a philosopher is a completed change of state in this past narrative, so 成为 takes the perfective marker 了.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 你：孟子，This narrative has been told in the third person, and the bare second-person reference has no identified speaker or addressee here. Repeat the character’s name so the referent is unambiguous.
> - Coherence (Temporality): 告诉了：告诉，A saying verb that introduces quoted speech normally uses the zero particle rather than 了. The quotation itself supplies the speech content.
> - Expressiveness: At the third-home sentence, add one concrete detail about the learning environment: “他们的新家在学校旁边，窗外常常传来读书声。”
> - Expressiveness: At “妈妈感觉这个地方适合他们,” show the mother’s happiness through an action and a line of speech: “妈妈高兴地说：‘这儿的环境很适合你学习。’”
> - Expressiveness: After the study routine, add Mengzi’s feeling to make his change more vivid: “孟子觉得读书很有意思，每天都认真看书。”
> 
> **Encouragement**
> You clearly connect Mengzi’s daily study with his later success as a philosopher. You also use a direct quotation to show the mother’s idea, which gives the scene a narrative voice.

### End-of-story content feedback

#### S6 (before)

> **Content & Completeness**
> - At the beginning, the story needs to say that 孟子 and 孟母 lived near a graveyard and that 孟子 copied the sacrifice rituals every day. He only goes there to play in this retelling.
> - After leaving the graveyard, the family should move near a market, where 孟子 copies how people buy and sell. The story mentions sellers, but it does not clearly explain that the new home is near the market.
> - After the market, they should move near a school, where 孟子 begins studying every day. In this retelling, the third home is connected to learning how to worship, so this part is in the wrong order and needs to be changed to studying near a school.
> 
> **Overall Encouragement**
> - You included Meng Mu’s care for her son and showed that she wanted him to receive a good education. You also gave the story an ending where 孟子 becomes a famous philosopher.

#### S6-2pass (after)

> **Content & Completeness**
> - At the beginning, the story needs to say that 孟子 and 孟母 lived near a graveyard and that 孟子 copied people offering sacrifices every day, before 孟母 decides to move away.
> - After they move away from the graveyard, the next home should be near a market, where 孟子 copies buying and selling every day; the story currently says they move closer to the city without clearly giving this setting.
> - After the market, they should move to a neighborhood near a school, where 孟子 begins studying every day. In the final home, the story says he learns how to worship instead, so this important event is mixed up.
> 
> **Overall Encouragement**
> - You included the important idea that 孟母 moves because she cares about 孟子’s education. You also gave the story an ending where 孟子 becomes a famous philosopher.

## mengmu_samples#45 (mengmu_san_qian)

### Scene 1

> 古代的时候，一个男孩子跟他的妈妈住在中国。他叫孟子。他们住在墓地的旁边，所以孟子老是祭拜。孟子不是祭拜，就是跟朋友聊天。他很喜欢他的城市，但是城市有才两个学校，都很小。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 古代的时候：在古代，this is the idiomatic time expression for a historical setting; the listed form is not natural here.
> - 城市有才两个学校：城市才有两所学校，restrictive 才 must come before the verb 有, and 所 is the usual measure word for schools.
> 
> **Vocabulary Suggestions**
> - 小 -- “都很小”：规模不大，specifies that the schools are small in scale rather than merely physically small.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 一个男孩子跟他的妈妈住在中国。他叫孟子：一个叫孟子的男孩子跟他的妈妈住在中国，under the first-mention rule, introduce the character’s name together with who he is, rather than naming him only in the following sentence.
> - Coherence (Reference): 孟子不是祭拜：他不是祭拜，under the pronoun rule, use a pronoun for a recently mentioned character when no other male character competes as the referent.
> - Expressiveness: After the cemetery setting, add one concrete detail about what he sees, such as “每天都有不同的人来墓地祭拜”.
> - Expressiveness: At “孟子不是祭拜”, show that he is copying others rather than doing a serious ritual: “他学着大人的样子祭拜，还一边笑一边跟朋友聊天”.
> - Expressiveness: After the last sentence, add Mengzi’s feeling about the small schools, such as “他觉得学校太小了，没有什么好玩的”.
> 
> **Encouragement**
> - You used the “不是……就是……” pattern effectively to show Mengzi’s repeated activities.
> - The scene clearly establishes the cemetery and then shifts to the city, giving the reader a sense of where Mengzi lives.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 古代的时候：在古代，Use the established narrative time expression “在古代”; “古代的时候” is not the appropriate form here.
> - 老是：常常，“老是” usually carries a negative or complaining tone. A neutral description of a repeated action should use “常常”.
> - 有才两个学校：才有两个学校，The restrictive adverb “才” comes before the verb it modifies, so it must be placed before “有”.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 孟子不是祭拜：他不是祭拜，Use a pronoun for a close re-occurrence: “孟子” was the subject in the immediately preceding sentence, and no competing singular character has intervened.
> - Coherence (Reference): 城市：它，Use a pronoun for a close re-occurrence: the city was just mentioned as “他的城市”, so repeating the noun is unnecessary.
> - Expressiveness: At the cemetery sentence, add one sensory or visual detail to show what Mengzi sees there. Example: “孟子看到有人哭着祭拜。”
> - Expressiveness: After describing Mengzi’s repeated worship, add his feeling or thought to make his action more vivid. Example: “他觉得这样很好玩。”
> - Expressiveness: At the city sentence, add a detail that explains why he likes the city. Example: “街上有很多商人，叫卖声不断。”
> 
> **Encouragement**
> You introduce Mengzi and his mother clearly at the start, and you use both a cause connector and a contrast connector to organize the scene. The final detail about the small number of schools gives the city a specific feature.

### Scene 2

> 他的妈妈不是不喜欢他们的城市，而是想孟子有很好的教育。他们搬家到有很多学校的城市。他们从早到晚走路，孟子一直抱怨。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 想孟子有很好的教育：想让孟子接受很好的教育，When the desired action has a different subject, use 想让 + person + verb; 想 directly before a clause can mean “think that,” rather than express a wish.
> 
> **Vocabulary Suggestions**
> - 好的 -- “孟子有很好的教育”：优质的，specifies that the education is high in quality rather than simply “good.”
> 
> **Coherence & Expressiveness**
> - Coherence (Temporality): 他们搬家到有很多学校的城市：他们搬家到了有很多学校的城市，Use 了 for the completed move in this past narrative.
> - Expressiveness: After the long walk, add Mengzi’s physical feeling and a short complaint, such as “孟子又累又饿，说：‘什么时候才能到啊？’”
> - Expressiveness: Show the mother’s purpose more vividly through her thoughts, such as “妈妈心想：‘学校多，孟子就能好好学习。’”
> 
> **Encouragement**
> - You clearly show the mother’s motivation for moving and connect Mengzi’s complaint naturally to the long journey. The phrase “一直抱怨” effectively shows that his unhappiness continued for some time.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 想孟子有很好的教育：想让孟子接受很好的教育，The verb 想 cannot directly introduce a new subject-predicate clause in this meaning. Use 想让 + person + verb; for receiving education, 接受教育 is the appropriate verb-object collocation.
> - 从早到晚走路：从早到晚都走路，A totality expression such as 从早到晚 requires 都 before the predicate to show that the action continues throughout the whole period.
> 
> **Vocabulary Suggestions**
> - 很多 -- “有很多学校的城市”：多所，This makes it explicit that the city has a number of separate schools, using the suitable measure word for schools.
> 
> **Coherence & Expressiveness**
> - Coherence (Temporality): 搬家到：搬到了，Use 了 with the movement verb 搬到 because this scene presents the move as a completed action.
> - Coherence (Conjunction): 他们搬家到有很多学校的城市。：所以，他们搬到了有很多学校的城市。，Add 所以 to mark the cause-effect link: the mother wants Mengzi to receive a good education, so they move to a city with many schools.
> - Coherence (Conjunction): 他们从早到晚走路，孟子一直抱怨。：因为他们从早到晚都走路，所以孟子一直抱怨。，Use 因为……所以…… to show that walking all day is the reason for Mengzi’s complaints.
> - Expressiveness: After the walking detail, add a physical sensation to make the journey more vivid, such as “脚又酸又疼”.
> - Expressiveness: Show Mengzi’s frustration with a short line of dialogue after “孟子一直抱怨”, such as “我不想再走了！”.
> - Expressiveness: Add the mother’s reaction to his complaints to show her feelings, such as “妈妈叹了口气”. 
> 
> **Encouragement**
> You used the contrast pattern “不是……而是……” well to show the mother’s real reason for moving. The scene also clearly keeps Mengzi and his mother as the focus.

### Scene 3

> 他难怪抱怨，他想他的朋友，因为他不要离开他的城市。他的妈妈找到孟子一个老师。跟老师孟子学最重要的文学，所以他成为哲学家。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 他难怪抱怨：难怪他抱怨，the sentence adverb 难怪 normally comes before the subject to introduce an understandable conclusion.
> - 想他的朋友：想念朋友，想 followed directly by a person usually means “think about”; 想念 expresses missing someone.
> - 不要离开：不想离开，use 不想 to express that a character does not want to do something; 不要 is usually a prohibition or refusal.
> - 找到孟子一个老师：给孟子找一个老师，when someone finds or seeks something for a recipient, place 给 + recipient before the verb.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Temporality): 找到：找到了，this is a completed past event, so add 了 after the result complement 到.
> - Coherence (Temporality): 成为哲学家：成为了哲学家，use 了 to mark the completed change of state in this past narrative outcome.
> - Expressiveness: After the complaint, add a short thought to show why leaving feels difficult: “他心想：‘我真舍不得我的朋友。’”
> - Expressiveness: Make the mother’s action warmer by showing her purpose: “妈妈希望孟子能受到更好的教育。”
> - Expressiveness: Add a brief line from the teacher to make the school scene more vivid: “老师对孟子说：‘我们一起认真读书吧。’”
> 
> **Encouragement**
> You clearly linked Mengzi’s complaint to a reason with 因为, and you kept the focus on his feelings, his mother, and his education.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 他难怪抱怨：难怪他抱怨，“难怪” is a discourse adverb meaning “no wonder,” and it normally comes before the subject and predicate it comments on.
> - 不要：不想，Use “不想” to describe a character’s personal wish not to do something. “不要” is more commonly used for an instruction, refusal, or request.
> - 找到孟子一个老师：给孟子找到了一个老师，The beneficiary must be introduced with “给,” so someone finds a teacher for Mengzi. “了” is also needed because the mother’s finding a teacher is a completed action.
> - 跟老师孟子学：孟子跟老师学，The subject should come before the “跟 + person” phrase: subject + 跟 + person + verb.
> 
> **Vocabulary Suggestions**
> - 想 -- “他想他的朋友”：想念，This specifically expresses missing friends who are not nearby, making the feeling clearer in this context.
> 
> **Coherence & Expressiveness**
> - Coherence (Temporality): 成为：成为了，Use “了” for a completed change of state: becoming a philosopher is presented as an achieved result.
> - Expressiveness: After “难怪他抱怨,” add a short inner feeling to show why he is upset, such as: “他心里很难过，也很想念朋友。”
> - Expressiveness: When the mother finds the teacher, add a brief line of dialogue to show her hope for him, such as: “妈妈说：‘你要认真跟老师学习。’”
> - Expressiveness: Make the learning moment more concrete by naming an activity, such as: “孟子每天跟老师读书、写字。”
> 
> **Encouragement**
> You clearly connect Mengzi’s unhappiness with leaving his city and then show how his mother tries to help him. The final result also gives the scene a clear direction.

### End-of-story content feedback

#### S6 (before)

> **Content & Completeness**
> - After 孟子 begins imitating sacrifices near the graveyard, the story needs his mother’s reason for moving: she worries that this daily behavior will have a bad influence on him.
> - Before moving to the area with a school, the story needs the part where they live near a market and 孟子 imitates buying and selling every day.
> - The move near a school should come after leaving the market, and then 孟子 should begin studying every day there.
> - At the end, make clear that 孟子 grows up and becomes a famous philosopher, not only that he becomes a philosopher after studying with one teacher.
> 
> **Overall Encouragement**
> - You clearly introduced 孟子, his mother, and their first home near the graveyard. You also gave the story an ending about 孟子 studying and becoming a philosopher.

#### S6-2pass (after)

> **Content & Completeness**
> - After Mengzi imitates offering sacrifices near the graveyard, the story needs his mother to decide to move because she worries this behavior will have a bad influence on him.
> - The story needs the move to the neighborhood near the market, where Mengzi imitates buying and selling every day.
> - After the market, the story needs Mengzi’s mother to move again to live near a school, and then Mengzi begins studying every day.
> - The ending should show that Mengzi grows up to become a famous philosopher, not only that he becomes a philosopher after studying with one teacher.
> 
> **Overall Encouragement**
> - You clearly introduced Mengzi, his mother, and their first home near the graveyard. You also included his later studying and becoming a philosopher, which gives your retelling a strong direction.

## shennong_samples#8 (shennong_chang_baicao)

### Scene 1

> 古代的时候，有一个人叫神农。一天，神农正在路上走，一看很多人正在吃一些植物。一些人一吃植物就生病了，神农想帮别人。所以想知道哪些植物能吃，哪些植物不能吃。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 古代的时候：在古代，Use this time expression for the historical period; the listed form is not natural here.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 有一个人叫神农：有一个叫神农的男人，For a first mention, introduce the character with a full noun phrase that gives both the name and a clear identity, rather than the vague noun “人”.
> - Coherence (Conjunction): 神农想帮别人。所以想知道哪些植物能吃，哪些植物不能吃：神农想帮别人，所以想知道哪些植物能吃，哪些植物不能吃，Use “所以” to join the cause and result in one sentence: wanting to help others leads to wanting this knowledge.
> - Coherence (Conjunction): 一看很多人正在吃一些植物：看到很多人正在吃一些植物，“一 + verb” must be followed by “就 ……”; here the sentence only reports what Shen Nong saw, so “看到” is the appropriate verb.
> - Expressiveness: After the people become ill, add a concrete physical detail to show their condition, such as “有人捂着肚子，疼得直冒汗。”
> - Expressiveness: Add Shen Nong’s inner thought after he sees the sick people, such as “神农心想：我一定要弄清楚哪些植物能吃。”
> - Expressiveness: Describe the plants briefly to make the setting more vivid, such as “路边长着绿绿的草和颜色鲜艳的花。”
> 
> **Encouragement**
> - You clearly establish the problem in this scene: people eat plants without knowing whether they are safe, and Shen Nong wants to help. You also used “正在” well to show an action in progress.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 古代的时候：在古代，Use 在古代 for a broad historical setting. 古代的时候 is not the appropriate time expression here.
> - 一看：看到，看 describes the act of looking, while 看到 includes the result of seeing. The sentence says that Shen Nong saw the people, so it needs the resultative complement 到.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Conjunction): 神农想帮别人。所以想知道：因为想帮别人，所以想知道，These ideas have a cause-and-effect relationship: wanting to help others is the reason for wanting to know which plants are edible. Use the paired connector 因为……所以…… to link them.
> - Expressiveness: After the people become ill, add one visible detail to make the danger clearer, for example: “有的人脸色发白，捂着肚子。”
> - Expressiveness: After Shen Nong sees the illness, add his feeling or inner thought, for example: “神农很着急，心想：‘我一定要弄清楚哪些植物能吃。’”
> 
> **Encouragement**
> You introduce Shen Nong clearly before continuing the action. You also use 正在 to show an ongoing action and 一……就…… effectively to show that the illness happens quickly after eating.

### Scene 2

> 然后，神农开始尝很多植物，比方说他吃过生姜、芥兰和菠菜。一些植物吃真好，特别是黄瓜。但是，一些植物毒得很，特别是夹竹桃。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 一些植物吃真好：一些植物吃起来真好，Use the result-complement pattern “verb + 起来 + adjective” to describe how food tastes when eaten.
> 
> **Vocabulary Suggestions**
> - 很多 -- “神农开始尝很多植物”：各种各样的，emphasizes that he is trying plants of many different kinds.
> 
> **Coherence & Expressiveness**
> - Coherence (Temporality): 神农开始尝很多植物，比方说他吃过生姜、芥兰和菠菜：神农开始尝很多植物，比方说吃了生姜、芥兰和菠菜，Use 了 for the completed examples of tasting; 吃过 is experiential and can sound less directly connected to this particular sequence.
> - Expressiveness: When introducing the dangerous plant, add a visual detail to make it memorable: “夹竹桃开着黄色的花，像星星一样。”
> - Expressiveness: After the warning about the poisonous plant, add Shen Nong’s physical reaction or feeling: “神农一吃夹竹桃，肚子就疼了起来。”
> 
> **Encouragement**
> - You use a clear contrast between plants that are pleasant to eat and plants that are dangerous. The examples of vegetables also make Shen Nong’s experimenting easy for the reader to understand.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 一些植物吃真好：一些植物吃起来真好，Use the result/complement pattern with 起来 to describe how a food tastes. Without 起来, 吃真好 does not form a grammatical predicate for the taste of the plants.
> - 但是，一些植物毒得很：但是，一些植物有毒，毒性很强，毒 cannot take the degree complement 得很 in this use. Use 有毒 to describe a poisonous plant, and 毒性很强 to state that its poison is strong.
> 
> **Vocabulary Suggestions**
> - 吃过 -- “比方说他吃过生姜、芥兰和菠菜”：尝过，This emphasizes that he sampled these plants as part of his investigation, rather than simply eating them as ordinary food.
> 
> **Coherence & Expressiveness**
> - Expressiveness: After naming the edible plants, add a sensory detail to show why one was appealing. For example: “黄瓜吃起来又脆又清爽。”
> - Expressiveness: At the mention of the poisonous plant, add a visual detail that makes it memorable. For example: “夹竹桃开着像星星一样的黄花，又大又漂亮。”
> - Expressiveness: You could show Shen Nong’s careful attitude while he tries the plants. For example: “他一边尝，一边把每种植物的样子记下来。”
> 
> **Encouragement**
> You clearly organize the scene with a sequence connector and a contrast connector. The examples of edible and poisonous plants also make the comparison easy for the reader to follow.

### Scene 3

> 一个人对神农说，麻烦我们可以吃什么植物？神农说，这就要看你想不想生病了。以后，神农告诉别人一些植物能吃，一些植物不能吃。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 麻烦我们可以吃什么植物？：请问，我们可以吃什么植物？，麻烦 cannot introduce a polite question in this way; 请问 is the appropriate expression for politely asking a question.
> - 这就要看你想不想生病了：这就要看是哪种植物了，this pattern must state the uncertain condition that answers the question. Here, which plants are edible depends on the type of plant, not on whether the listener wants to become ill.
> - 以后：后来，when it starts a new sentence to mean “afterwards,” use 后来 rather than 以后.
> - 别人：人们，别人 distinguishes other people from a stated person or group; here Shennong is speaking generally to people, so 人们 is needed.
> 
> **Vocabulary Suggestions**
> - 说 -- “一个人对神农说”：问，more precisely shows that the person is asking a question rather than simply speaking.
> 
> **Coherence & Expressiveness**
> - Coherence (Temporality): 神农告诉人们一些植物能吃：神农告诉了人们一些植物能吃，告诉 is a completed narrative action here, so it needs 了 to mark completion.
> - Expressiveness: At the question, add the person’s feeling to make the need for an answer clearer: “一个人着急地问：‘请问，我们可以吃什么植物？’”
> - Expressiveness: Add a small detail about Shennong’s manner of speaking: “神农耐心地解释：‘这就要看是哪种植物了。’”
> 
> **Encouragement**
> - You used a clear question-and-answer structure, which makes this short scene easy to follow.
> - You also clearly contrasted plants that can be eaten with plants that cannot be eaten.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 麻烦我们可以吃什么植物：麻烦问一下，我们可以吃什么植物，The word 麻烦 cannot introduce a question by itself. 麻烦问一下 is a polite fixed expression meaning that the speaker is asking for information.
> - 以后：后来，At the beginning of a narrative sentence, 后来 means “afterwards.” 以后 normally needs a time expression before it or refers to a later/future time.
> - 别人：人们，别人 means “other people” and requires a contrast with a person or group already mentioned. Here 神农 is speaking generally to people, so 人们 fits.
> 
> **Vocabulary Suggestions**
> - 说 -- “一个人对神农说”：问，This states more precisely that the person is asking a question rather than making a general statement.
> 
> **Coherence & Expressiveness**
> - Coherence (Temporality): 生病了：生病，Use the zero particle with 想 in an “want to do” construction. The illness is a possible result, not a completed action, so 了 is not needed.
> - Coherence (Temporality): 告诉：告诉了，Use 了 for this completed narrative action: after this point, 神农 finished telling people which plants could and could not be eaten.
> - Expressiveness: Before the question, add the person's worried expression to show why the question matters; for example: “皱着眉头问”.
> - Expressiveness: When 神农 answers, add a calm or helpful manner to show his character; for example: “耐心地告诉大家”.
> - Expressiveness: Add a short reaction after learning the answer, such as relief or thanks; for example: “松了一口气”. 
> 
> **Encouragement**
> You use direct speech effectively, so the scene feels like a real conversation. The contrast between plants that can be eaten and plants that cannot is also stated clearly.

### End-of-story content feedback

#### S6 (before)

> **Content & Completeness**
> - After 神农 decides to help people, the story needs to show him climbing mountains to try different plants.
> - While trying plants, the story needs the part where 神农 finds “茶” and writes it in his record.
> - When 神农 tries “夹竹桃,” the story needs to say that he faints from it, not only that it is poisonous.
> - After he faints, the story needs the person in blue to arrive and give him “灵芝,” so that 神农 feels better.
> - After 神农 feels better, the story needs the conversation with the person in brown.
> - Before 神农 tells everyone what he learned, the story needs to show him recording both “灵芝” and “夹竹桃.”
> 
> **Overall Encouragement**
> - You clearly introduced 神农’s goal and explained why he wanted to learn about safe plants. Your ending also shows that he uses what he learns to help other people.

#### S6-2pass (after)

> **Content & Completeness**
> - After Shennong decides to help people, the story needs him to climb mountains to look for and try different plants.
> - While trying plants, the story needs Shennong to find “茶” and write it down in his record.
> - After he tries “夹竹桃,” the story needs to show that he faints from it, not only say that it is poisonous.
> - After Shennong faints, a person in blue needs to arrive and give him “灵芝,” and Shennong needs to feel better after eating it.
> - After Shennong feels better, the story needs another person in brown to come and talk with him.
> - At the end, Shennong needs to record both “灵芝” and “夹竹桃” so people know which plant helps and which plant is dangerous.
> 
> **Overall Encouragement**
> - You clearly introduced Shennong, the problem of people getting sick from plants, and his wish to help them. You also included several examples of plants and showed that some are safe while others are dangerous.

## shennong_samples#19 (shennong_chang_baicao)

### Scene 1

> 古代的时候，一个男人觉得植物很有意思。他叫神农。有的植物吃了以后他的肚子疼死了，可是有的吃了以后很舒服。他找很多植物。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 古代的时候：在古代，this time expression is not used naturally for a broad historical setting; use 在古代 or 古代.
> - 他找很多植物：他找到了很多植物，找 means “to look for,” while 找到 means “to find”; 到 also marks that the search reached a result, and 了 marks the completed event.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 一个男人觉得植物很有意思。他叫神农。：一个叫神农的男人觉得植物很有意思。，On first mention, introduce the character with both the name and a full noun phrase, rather than giving an unnamed noun first and naming him only in the next sentence.
> - Expressiveness: After the stomach pain, add a physical reaction to show how severe it is: 神农在地上躺着，难受得不得了。
> - Expressiveness: Add a short inner thought after the painful experience: 神农想：“这种植物有毒吗？”
> - Expressiveness: Describe one kind of plant more specifically before he eats it: 有的植物开着黄色的、像星星一样的花。
> 
> **Encouragement**
> - You clearly contrast the two kinds of plants with 有的……可是有的……, which helps the reader understand the difference.
> - Your use of 吃了以后 correctly shows that eating happens before the stomach pain or comfort.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 古代的时候：在古代，This time expression is not idiomatic for a general historical setting. Use 在古代 to mean “in ancient times.”
> - 他找很多植物。：他找到了很多植物。，找 means “to look for,” while 找到 means “to find.” Since the sentence states that he successfully found the plants, it needs the resultative complement 到; 了 marks the completed finding.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 一个男人觉得植物很有意思。他叫神农。：一个叫神农的男人觉得植物很有意思。，At first mention, introduce a character with both a name and a noun phrase. Naming 神农 immediately makes the reference clear and avoids introducing him first as an unnamed man.
> - Expressiveness: After “植物很有意思,” add a brief reason showing what interests him, such as: “他觉得每一种植物都不一样。”
> - Expressiveness: After “他的肚子疼死了,” add a physical detail to make the pain more vivid, such as: “他疼得躺在地上。”
> - Expressiveness: You could add a short thought after he finds a plant, such as: “这种植物能吃吗？”
> 
> **Encouragement**
> You use the contrast between harmful and helpful plants clearly with 可是. The phrase 疼死了 is also vivid and effectively shows how badly Shennong feels.

### Scene 2

> 凉山很大的山，这也找植物。一天，他找到黄色的花。他听说你跟黄色的花做茶很有用。比方说，你的头发疼死，这冰茶是药。他一喝茶就很不舒服。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 凉山很大的山：凉山是一座很大的山，A noun predicate needs 是, and a single mountain is counted with the measure word 座.
> - 你跟黄色的花做茶：用黄色的花做茶，Use 用 to introduce the material used to make something. 你 has no referent here, and 跟 does not mean “using” in this structure.
> - 头发疼死：头疼得要死，头发 means “hair,” which cannot ache; use 头疼 for a headache. A degree complement also requires 得 before 要死.
> - 这冰茶：这杯冰茶，A demonstrative before a countable noun follows the pattern 这/那 + measure word + noun.
> 
> **Vocabulary Suggestions**
> - 大 -- “凉山很大的山”：高大，specifies that the mountain is both tall and large in scale.
> - 不舒服 -- “他一喝茶就很不舒服”：难受，more directly describes physical discomfort in this situation.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 这也找植物：他也在这儿找植物，Use a pronoun for the previously introduced character 神农; 这 refers to a place, so 在这儿 is needed to show where the searching happens.
> - Coherence (Reference): 黄色的花：一些黄色的花，This is the first mention of these flowers, so introduce them as an indefinite group rather than as an already known, specific object.
> - Coherence (Temporality): 找到黄色的花：找到了一些黄色的花，Use 了 after 找到 because this is a completed discovery in the story.
> - Coherence (Conjunction): 头疼得要死，这杯冰茶是药：头疼得要死的时候，这杯冰茶是药，Use 的时候 to connect the headache condition with the tea’s use.
> - Expressiveness: When the yellow flowers appear, add one visual detail to make the place easier to imagine, such as “黄色的花像星星一样，又大又漂亮。”
> - Expressiveness: After the tea makes him ill, describe a physical reaction more specifically, such as “他的肚子疼了起来，难受得不得了。”
> - Expressiveness: Add a short thought to show his fear, such as “他想：‘我会不会生病了？’”
> 
> **Encouragement**
> - You clearly move the scene forward with a mountain, yellow flowers, tea, and 神农’s reaction. Using “一天” and “一……就……” also helps the reader follow the event sequence.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 凉山很大的山：凉山是一座很大的山，A noun predicate normally needs 是; 座 is the usual measure word for a mountain.
> - 找到：找到了，The discovery is a completed action, so it needs the completion marker 了.
> - 头发疼死：头疼死了，Hair does not feel pain; the body part that aches is the head. The result/intensity expression also needs 了 here.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 这：他，Use a pronoun for the previously introduced character; this demonstrative cannot refer to a person in this position.
> - Coherence (Reference): 黄色的花：一朵黄色的花，This is the flower’s first mention, so introduce it as an indefinite noun phrase with an appropriate measure word.
> - Coherence (Reference): 你：，Second person is not appropriate in narration without quoted speech addressing a listener. Remove it so the sentence can describe the general action instead.
> - Coherence (Reference): 你：一个人，This second-person reference has no introduced listener. Use an indefinite person for a general example.
> - Coherence (Conjunction): 跟黄色的花做茶：用黄色的花做茶，Use 用 to mark the ingredient or material used to make something. 跟 introduces participants performing the same action, not a material.
> - Coherence (Conjunction): 这冰茶：这种冰茶，A demonstrative before a noun requires a measure word; 种 classifies a type of drink.
> - Expressiveness: After the flower is found, add a visual detail to make the setting clearer: 黄色的花像星星一样，又大又漂亮。
> - Expressiveness: At the point where he feels ill, describe a physical reaction and feeling: 他肚子疼了起来，难受得不得了。
> - Expressiveness: You could add a short thought after he becomes ill: 他想：“我会不会生病了？”
> 
> **Encouragement**
> You used a clear time shift to begin a new event, and the pattern with one action immediately leading to another is a good way to show a quick result. The scene also has a strong contrast between hearing that the tea is useful and then feeling unwell after drinking it.

### Scene 3

> 糟糕，这黄色的花是夹竹桃，特别是毒。正好在这儿，灵芝药的夹竹桃他吃完了，也写一个课文的植物。谢谢神农。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 这黄色的花：这朵黄色的花，this/that + measure word + noun requires a measure word; “朵” is the appropriate measure word for a flower.
> - 特别是毒：特别有毒，“毒” is a noun here, so it cannot serve as the adjective predicate after “是”; use “有毒” to describe a poisonous plant.
> - 灵芝药的夹竹桃：灵芝和夹竹桃，“的” makes one noun modify another and cannot join two separate plants; use “和” to coordinate the two nouns.
> - 写一个课文的植物：把这些植物记下来，“写” cannot take plants themselves as its object when the meaning is to record information; “记下” means to write down and preserve a record of the plants.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Temporality): 吃完了，也写：吃，也写了，when a series of completed actions is connected, only the last verb takes “了”; here the recording is the final completed action.
> - Expressiveness: After “糟糕”, add a physical reaction to show the danger: “神农的肚子马上疼了起来。”
> - Expressiveness: Describe the flower more vividly at “这朵黄色的花”: “这朵黄色的花像星星一样，又大又漂亮。”
> - Expressiveness: Add a short thought or line of speech after learning it is poisonous: “神农想：‘以后不能随便吃不认识的植物。’”
> 
> **Encouragement**
> - You used the important story words “夹竹桃” and “灵芝” and clearly showed that the flower is dangerous. The opening “糟糕” also gives the scene an immediate feeling of alarm.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 这黄色的花：这种黄色的花，A demonstrative such as 这 needs a measure word before a noun; 种 is the appropriate measure word for a kind of flower.
> - 特别是毒：特别有毒，特别 is the degree adverb needed before the predicate. 特别是 introduces a singled-out example, while 有毒, not 毒 alone, is the normal adjectival predicate meaning “poisonous.”
> - 灵芝药的夹竹桃：夹竹桃，灵芝药的 cannot naturally modify 夹竹桃: 灵芝 medicine and oleander are different things, so this modifier creates an ungrammatical noun phrase.
> - 也写一个课文的植物：也写下了一篇关于植物的课文，Use 写下 to show that the writing was successfully recorded, and use 了 for this completed final action. A text takes the measure word 篇, and 关于植物的 should modify 课文 rather than placing 植物 after 的.
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Temporality): 吃完了：吃完，In a series of completed actions, 了 normally appears only on the last verb. Here the final writing action takes 了, so 吃完 does not need it.
> - Expressiveness: After the first sentence, add a visual detail about the flower: “那儿开着黄色的像星星一样的花，又大又漂亮。” This makes the dangerous plant easier to picture.
> - Expressiveness: After he eats the flower, show his physical reaction: “他肚子疼了起来，难受得不得了。” This gives the event a clear emotional and physical effect.
> - Expressiveness: You could add his worried thought at that moment: “他想：‘我会死吗？’” This lets the reader hear his fear directly.
> 
> **Encouragement**
> You clearly identify 夹竹桃 as the dangerous flower, and you try to connect eating a plant with recording knowledge about it. Those are strong story actions for this scene.

### End-of-story content feedback

#### S6 (before)

> **Content & Completeness**
> - The beginning needs to explain that, in ancient times, people did not know which plants were safe to eat, so many people became sick after eating the wrong plants. This should come before introducing 神农’s work.
> - After introducing 神农, the story needs to say that he decided to discover which plants were safe and which were poisonous, and that this was why he climbed mountains and tried plants.
> - When 神农 finds 茶, the story needs to show that he drinks it and feels better, not uncomfortable. He should also make a record about 茶.
> - After 神农 eats 夹竹桃, the story needs to show that he faints.
> - After he faints, a person in blue should arrive and give him 灵芝; 神农 should eat the 灵芝 and feel better.
> - After 神农 feels better, another person in brown should come and talk with him.
> - At the end, 神农 needs to record both 灵芝 and 夹竹桃, including that 灵芝 can help and 夹竹桃 is poisonous.
> 
> **Overall Encouragement**
> You included 神农, the mountain, 茶, 夹竹桃, and 灵芝, so you remembered many important parts of the story. You also showed that 神农 was trying different plants, which is a strong main idea.

#### S6-2pass (after)

> **Content & Completeness**
> - The story needs an opening explanation that, in ancient times, people did not know which plants were safe to eat, so people often became sick after eating plants.
> - Before 神农 starts finding plants, explain that he decided to discover which plants were safe and which were poisonous; then show him climbing mountains to try them.
> - After 神农 finds 茶, include that he drinks it, feels better, and writes it in his record. In this retelling, he feels sick after drinking tea, which changes the event.
> - After 神农 eats 夹竹桃, show that he faints from the poison.
> - After he faints, add the person in blue who gives him 灵芝, and show that 神农 feels better after eating the 灵芝.
> - After 神农 recovers, include the person in brown coming to talk with him.
> - At the end, show 神农 recording both 灵芝 and 夹竹桃 in his plant record.
> 
> **Overall Encouragement**
> - You included 神农, the mountain, 茶, 夹竹桃, and 灵芝, so you remembered several important parts of the story. Keep building the events in order so the ending shows how 神农 learns from each plant.

## shennong_samples#33 (shennong_chang_baicao)

### Scene 1

> 古代时候，人不知道他们能吃什么植物，常常一吃就死。但是不知道为什么，没有办法。所以有一天，神农出去试一试很多种植物，告诉人什么植物是安全什么是危险。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 古代时候：古代的时候，The time phrase uses ……的时候; the particle 的 is required here because 古代 has more than one syllable.
> - 人：人们，Use 人们 for a concrete group of people in this situation; 人 is a generic noun.
> - 什么植物是安全什么是危险：什么植物是安全的，什么植物是危险的，The two parallel clauses need clear separation, and adjectives used as the descriptive complement after 是 naturally take 的 here.
> - 告诉人：告诉人们，Use 人们 rather than the generic noun 人 when referring to the people whom 神农 tells.
> 
> **Vocabulary Suggestions**
> - 试一试 -- “神农出去试一试很多种植物”：尝一尝，specifies that he tests the plants by tasting them, which fits this plant-discovery scene.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 他们能吃什么植物：什么植物能吃，Use zero form for the same referent within one sentence: after 人们 has been named, 他们 is unnecessary.
> - Coherence (Reference): 神农：一个叫神农的男人，Follow the first-mention rule by introducing a new character with a full noun phrase.
> - Coherence (Temporality): 告诉：告诉了，This is the final action in a completed series of past events, so it takes 了; in a series of actions, the last verb carries the completion marker.
> - Expressiveness: After the deaths are mentioned, add the people’s fear to make the danger more immediate: “人们很害怕，不知道该吃什么。”
> - Expressiveness: At the moment 神农 decides to act, add his inner determination or a short thought: “神农想：‘我一定要找出能吃的植物。’”
> - Expressiveness: Add one detail about how he explores the plants: “他走到高山上，仔细观察各种植物。”
> 
> **Encouragement**
> - You used “一……就……” correctly to show that eating an unknown plant could lead to an immediate result.
> - The scene clearly presents the problem first and then introduces 神农’s action as a response.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 古代时候：在古代，Use the established time expression 在古代 for a general historical setting; 古代时候 is not a natural time phrase.
> - 是安全：安全，安全 is an adjective and can directly function as the predicate here; do not place 是 before it in this structure.
> - 是危险：危险，危险 is an adjective and can directly function as the predicate here; do not place 是 before it in this structure.
> 
> **Vocabulary Suggestions**
> - 很多种 -- “试一试很多种植物”：各种各样的，This emphasizes that the plants differ in many ways, making the range of plants more vivid and specific.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 人不知道他们能吃什么植物：人们不知道什么植物能吃，Use 人们 for the concrete group of people in this setting. After naming that group, the possessive pronoun 他们 is unnecessary; the plants' edibility is understood to be for people.
> - Coherence (Reference): 神农：一个叫神农的人，This is the character's first mention, so introduce him with a full noun phrase rather than using only his name.
> - Coherence (Reference): 告诉人什么植物是安全什么是危险：告诉人们什么植物安全，什么植物危险，Use 人们, not bare 人, when referring to the concrete group of people whom he will tell.
> - Coherence (Temporality): 出去试一试很多种植物：出去试了很多种植物，This is a completed narrative action, so the last verb in the action series takes 了. Also, V一V is for a brief or tentative try, not for carrying out tests on many kinds of plants.
> - Coherence (Conjunction): 但是不知道为什么，没有办法：因为不知道为什么，所以没有办法，The second idea is the result of not knowing the reason, so use the cause-and-effect connector 因为……所以…… rather than the contrast connector 但是.
> - Expressiveness: After the deaths are mentioned, add one physical detail to make the danger easier to imagine, for example: “很多人吃了有毒的植物以后，肚子疼得很厉害。”
> - Expressiveness: At the point where Shennong decides to test plants, add his determination in a short thought or line of speech, for example: “神农想：‘我一定要找出安全的植物。’”
> - Expressiveness: When describing his testing, add a small action detail, for example: “他仔细看了看植物的叶子和花。”
> 
> **Encouragement**
> You establish the problem clearly: people cannot tell which plants are edible, and Shennong acts to help them. Your final sentence also gives his goal in a clear, easy-to-follow way.

### Scene 2

> 发现有的植物对身体非常好，特别是茶，让肚子感觉又暖和又清楚。他告诉朋友：“你吃哪种植物，这就要看你的口味。比方说，你爱吃甜的，可能喜欢糖。”他最喜欢吃花，除了夹竹桃以外，什么都花想吃。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 让肚子感觉又暖和又清楚：让肚子感觉又暖和又舒服，清楚 describes clear thoughts, vision, or explanation, not a physical feeling in the stomach; 舒服 describes bodily comfort.
> - 你吃哪种植物，这就要看你的口味：你吃哪种植物，要看你的口味，the pattern 这就要看……了 is used as a flexible response to an uncertain question; here, a simple dependency statement with 要看 is the natural structure.
> - 什么都花想吃：什么花都想吃，什么花都 is the correct universal object phrase meaning “every kind of flower”; 什么都花 cannot form this word order.
> 
> **Vocabulary Suggestions**
> - 好 -- “有的植物对身体非常好”：有益，states more precisely that the plants benefit health；有好处，clearly expresses a positive effect on the body.
> - 最喜欢 -- “他最喜欢吃花”：偏爱，emphasizes that flowers are his particular preference among foods or plants.
> 
> **Coherence & Expressiveness**
> - Expressiveness: After the tea discovery, add a sensory detail about its taste or warmth, such as “茶水香香的，喝下去以后，肚子暖暖的。”
> - Expressiveness: Add Shen Nong’s reaction when he realizes tea is useful, such as “神农高兴地想：这种植物不但好喝，还对身体有好处！”
> - Expressiveness: The friend could respond with a short line of dialogue to make the exchange more lively, such as “朋友说：‘可是有些花有毒，不能随便吃。’”
> 
> **Encouragement**
> You gave a concrete example, tea, rather than only saying that some plants are healthy. You also tried to include dialogue and an exception structure, which makes this scene more story-like.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 又暖和又清楚：又暖和又舒服，“清楚” describes clarity of information, speech, or thought; it does not describe a physical stomach sensation. “舒服” correctly describes feeling physically comfortable.
> - 你吃哪种植物，这就要看你的口味。：你吃哪种植物，这就要看你喜欢吃哪种植物了。，In the pattern “这就要看……了”, the part after “看” must be an indirect question, such as a wh-question or an A-not-A question, and the sentence ends with “了”.
> - 什么都花想吃：什么花都想吃，For the “whatever/whichever” pattern, the wh-object stays with its noun before “都”: “什么花都想吃” means that he wants to eat every kind of flower.
> 
> **Vocabulary Suggestions**
> - 好 -- “有的植物对身体非常好”：有益，This specifically means beneficial to health, so it states the plants’ effect on the body more precisely.
> 
> **Coherence & Expressiveness**
> - Expressiveness: At the description of tea, add a sensory detail about its taste and warmth: “茶水香香的，喝下去以后，肚子暖暖的。 ”
> - Expressiveness: Before the character wants to eat flowers, describe their appearance and hint at the danger: “那些黄色的花像星星一样，又大又漂亮。”
> 
> **Encouragement**
> You clearly connect tea with a positive effect on the body, and you use direct speech to make the scene more lively. The exception with the oleander also shows that you are thinking carefully about different kinds of plants.

### Scene 3

> 他发现这个口味，一百岁时候，不小心吃了毒的花。一吃就开始死。但是生病时候告诉人什么植物是药，什么植物是毒。

#### S6 (before)

> **Grammar & Vocabulary Corrections**
> - 开始死：快要死了，"开始" normally takes a durative action, while "死" is a change-of-state verb; use "快要……了" to express that someone is close to dying.
> - 生病时候：生病的时候，A multi-syllable verb phrase before "时候" needs the linking particle "的".
> - 人：人们，"人" is a generic noun and cannot refer by itself to the concrete group of people being told.
> - 是毒：有毒，Use "有毒" to describe that a plant contains poison; "是毒" does not fit this predicate meaning.
> 
> **Vocabulary Suggestions**
> - 吃 -- “不小心吃了有毒的花”：误食了，more precisely means accidentally ate something that should not have been eaten.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 这个口味：一种花，"这个" needs a clear earlier referent, but no specific taste has been introduced; introduce this first-mentioned object with an indefinite noun phrase.
> - Coherence (Temporality): 告诉人们什么植物是药：告诉了人们什么植物是药，This is one completed action in the past narrative, so the verb needs completed-action "了".
> - Expressiveness: After the poisonous flower is mentioned, add a visual detail to make it memorable: “那种花又黄又大，像星星一样漂亮。”
> - Expressiveness: After the illness begins, show his physical feeling: “他的肚子疼得不得了，只能躺在地上。”
> - Expressiveness: Add a short thought at the dangerous moment: “他想：我会不会死？”
> 
> **Encouragement**
> - You used the pattern “一……就……” correctly to show an immediate result. You also clearly tried to explain the important difference between plants that are medicine and plants that are poisonous.

#### S6-2pass (after)

> **Grammar & Vocabulary Corrections**
> - 一百岁时候：一百岁的时候，With a multi-syllable expression before 时候, the structural particle 的 is required.
> - 毒的花：有毒的花，毒 is a noun and cannot directly modify 花 in this way. 有毒的 means “poisonous” and correctly describes the flower.
> - 开始死：快要死了，死 describes an endpoint and is not natural after 开始 in this context. 快要死了 expresses that the character is close to dying.
> - 生病时候：生病的时候，生病 has two syllables, so it needs 的 before 时候.
> - 人：人们，人 is a generic noun and does not naturally refer to the concrete group receiving this information. 人们 refers to people as a group.
> - 是毒：有毒，毒 is a noun, so it cannot serve directly as the predicate meaning “poisonous.” 有毒 correctly means “is poisonous.”
> 
> **Vocabulary Suggestions**
> - No suggestions.
> 
> **Coherence & Expressiveness**
> - Coherence (Reference): 这个口味：一种花的味道，The demonstrative 这个 has no clear antecedent in the preceding context. For a first-mentioned object, use an unambiguous full noun phrase.
> - Coherence (Temporality): 告诉人：告诉了人，This is a completed telling event in the narrative, so the verb takes 了. After the vocabulary correction, the full phrase is 告诉了人们.
> - Expressiveness: After the poisonous flower is eaten, add a physical reaction to make the danger vivid: “他肚子疼得不得了，只能躺在地上。”
> - Expressiveness: At the moment he fears death, add an inner thought: “他想：‘我会死吗？’”
> - Expressiveness: When he explains the plants, add direct speech to show his knowledge clearly: “他说：‘灵芝可以做药，夹竹桃有毒，不能吃。’”
> 
> **Encouragement**
> You used the useful 一……就…… pattern to show an immediate result, and you clearly tried to contrast plants that are medicine with plants that are poisonous.

### End-of-story content feedback

#### S6 (before)

> **Content & Completeness**
> - After 神农 decides to test plants, the story needs to show him climbing mountains to try many different plants.
> - When 神农 finds 茶, he also needs to make a record of it.
> - The dangerous plant needs to be clearly identified as 夹竹桃, and 神农 should faint after trying it.
> - After 神农 faints, a person in blue needs to arrive and give him 灵芝, which makes him feel better.
> - After 神农 recovers, another person in brown needs to come and talk with him.
> - At the end, 神农 needs to record both 灵芝 and 夹竹桃 so people know that one is medicine and the other is poisonous.
> 
> **Overall Encouragement**
> - You included the ancient setting, the problem of people not knowing safe plants, and 神农’s wish to help them. You also remembered that 茶 is good for the body and that some plants can be dangerous.

#### S6-2pass (after)

> **Content & Completeness**
> - At the beginning, the people should become sick after eating unknown plants, rather than die right away.
> - After 神农 decides to test plants, include that he climbs mountains to find and try many different plants.
> - After he finds 茶, add that he writes it down in his record.
> - The story needs a clear event where 神农 eats 夹竹桃 and faints; the later “poisonous flower” is not clearly named as 夹竹桃.
> - After 神农 faints, add the person in blue who gives him 灵芝, and show that he feels better after eating it.
> - After he recovers, add the person in brown who comes and talks with 神农.
> - At the end, show 神农 recording both 灵芝 and 夹竹桃, so readers know what people can use as medicine and what they should avoid.
> 
> **Overall Encouragement**
> - You included the important beginning idea that people did not know which plants were safe, and you showed 神农 trying plants to help others. You also remembered 茶 and the idea of poisonous plants.
