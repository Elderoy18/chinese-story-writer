# Step 1 report: Word files -> paragraphs

Each Word file in `raw/basic_data/` becomes `data/01_extracted/<name>.json`: its non-empty
paragraphs in document order, each with the character ranges that are bold.

| File | Paragraphs | Bold ranges | Characters normalized |
|---|---|---|---|
| 4 model stories.docx | 8 | 0 | 0 |
| Pear Story with Teacher feedback.docx | 102 | 26 | 205 |
| 孟母 samples with Teacher feedback.docx | 651 | 0 | 0 |
| 神农 samples with Teacher feedback.docx | 678 | 0 | 0 |

## Look-alike characters replaced

- ⼈ (U+2F08) -> 人: 32x
- ⼦ (U+2F26) -> 子: 21x
- ⼀ (U+2F00) -> 一: 21x
- ⾃ (U+2F83) -> 自: 9x
- ⾛ (U+2F9B) -> 走: 8x
- ⼩ (U+2F29) -> 小: 8x
- ⼏ (U+2F0F) -> 几: 6x
- ⼠ (U+2F20) -> 士: 6x
- ⾏ (U+2F8F) -> 行: 6x
- ⼉ (U+2F09) -> 儿: 6x
- ⼰ (U+2F30) -> 己: 5x
- ⽣ (U+2F63) -> 生: 5x
- ⽊ (U+2F4A) -> 木: 4x
- ⽤ (U+2F64) -> 用: 4x
- ⽽ (U+2F7D) -> 而: 4x
- ⼯ (U+2F2F) -> 工: 4x
- ⽂ (U+2F42) -> 文: 4x
- ⻋ (U+2ECB) -> 车: 4x
- ⽔ (U+2F54) -> 水: 3x
- ⽬ (U+2F6C) -> 目: 3x
- ⼤ (U+2F24) -> 大: 3x
- ⽋ (U+2F4B) -> 欠: 3x
- ⼒ (U+2F12) -> 力: 3x
- ⾰ (U+2FB0) -> 革: 3x
- ⾄ (U+2F84) -> 至: 2x
- ⽕ (U+2F55) -> 火: 2x
- ⻢ (U+2EE2) -> 马: 2x
- ⽓ (U+2F53) -> 气: 2x
- ⻓ (U+2ED3) -> 长: 2x
- ⾝ (U+2F9D) -> 身: 2x
- ⾼ (U+2FBC) -> 高: 2x
- ⽴ (U+2F74) -> 立: 2x
- ⾥ (U+2FA5) -> 里: 2x
- ⼥ (U+2F25) -> 女: 2x
- ⼼ (U+2F3C) -> 心: 2x
- ⾳ (U+2FB3) -> 音: 1x
- ⾹ (U+2FB9) -> 香: 1x
- ⽜ (U+2F5C) -> 牛: 1x
- ⼜ (U+2F1C) -> 又: 1x
- ⼝ (U+2F1D) -> 口: 1x
- ⽠ (U+2F60) -> 瓜: 1x
- ⽆ (U+2F46) -> 无: 1x
- ⽯ (U+2F6F) -> 石: 1x

## Bold text, for checking

Every bold range found, shown as **bold** inside its paragraph (first 40 per file).

### Pear Story with Teacher feedback.docx
- (paragraph 3) 张先生在梨子树口摆着一张梯子：张先生在梨子树口摆**了**一张梯子，Subj. V. 了 (completed) Obj., or 梨子树口摆着一张梯子，Place + V. 着 + Obj.
- (paragraph 9) 小王骑自行车到张先生的梨子树：到张先生的梨子树**下**，到 + place
- (paragraph 10) 就拿一筐水果：就拿**了**一筐梨子，了completed, “水果” is more generic and here it should be “梨子”，otherwise it will cause ambiguity, what “fruits” other than “pears”?
- (paragraph 11) 小王在马路骑自行车一看到别个人：在马路**上**，在+ place；骑**着**自行车，“着” is for “durative”；另外一个人/一个女孩子，there is no “别个人”.
- (paragraph 13) 小王和那筐梨子倒：小王和那筐梨子倒**了**，了completed/change
- (paragraph 15) 一个孩子在马路看到小王的帽子，拿上去：在马路**上**，在+ place；拿起来pick up，拿上去means “bring it up”
- (paragraph 16) 给孩子三个梨子：给**了**孩子三个梨子，了completed
- (paragraph 17) 孩子一直走去张先生的树，吃梨子：走**到**张先生的树**下**，走到place来/去，cannot say “走去/来Place”；吃着梨子，着 durative
- (paragraph 59) “从香甜的睡梦” incorrect: 从香甜的睡梦**中**；从 + Place
- (paragraph 63) 我兄弟姐妹：我**的**兄弟姐妹
- (paragraph 64) 所有全：所有**权**；use the wrong character
- (paragraph 70) 先打了大哈欠：先打了**个**大哈欠
- (paragraph 72) 拼几个小时之后：拼**了**几个小时之后；completed
- (paragraph 73) 我家长：我**的**爸爸妈妈；“家长“ is used in the context related to “education”, usually referring to parents who deal with children’s education.
- (paragraph 82) 但政府实行的改革经济一系列政策就让他失业，被迫转行：实行的改革经济**的**一系列政策，**却使**他失业**并**被迫转行；“却” indicates unexpected semantic turn, “使” is more formal and better fit other formal words like “失业，被迫，转行”，adding “并” will increase the coherence.
- (paragraph 84) 没办法回去以前的工作：回去**做**以前的工作
- (paragraph 85) 但只能思考几分钟，就被他拿起来了：但**我**只思考**了**几分钟； the Subj. here cannot be omitted, because the preceding “我怎么能…” is an inserted “narrator comment”, which is temporarily detached from the main storyline. When it goes back to the main story, the Subj. should be restated.
- (paragraph 93) 人类创造文明到底从哪里由此而来啊：人类创造**的**文明，the Subj. should be a noun “文明”, not a verb phrase “人类创造文明”；到底从何而来：由此而来 means “come from this”, but here should be a question “come from where”.
- (paragraph 94) 看起一点文明都没有：看起**来**一点儿都不文明，“文明” can be an Adj., meaning “civilized”.
- (paragraph 99) 看到我们糟糕的状态，用心得来帮忙整理梨子，拿起骑车：**他们过来**用心**地**帮忙整理梨子，扶起自行车，since the preceding phrase has “我们”, the Subj. 他们 should be stated, adv.地V，“骑车” is a verb phrase, cannot be the Obj. of “扶起”，“拿起” is usually used for smaller items.

