# Step 4 report: HanLP parse

- model: CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH; tasks: tok/fine, pos/ctb, ner/msra, dep; custom dictionary: 15 words
- load 1132s, parse 117s
- units: model_sentence 84, student_sentence 1254, teacher_fix 1002; tokens: 23210
- units whose tokens do not reproduce the text (positions unusable): 0


## Dictionary words HanLP still split

- 匈奴: 1 units

## Student sentences: parts of speech (top 20)

VV 3221, NN 2950, PU 2810, AD 2061, PN 1374, NR 790, DEG 613, VA 507, P 506, CD 505, AS 382, DT 316, DEC 295, M 293, CC 221, JJ 209, VC 183, SP 179, VE 174, LC 117

Aspect markers (AS) found in student sentences: 了 345, 着 27, 过 7, 的 3

## Names tagged PERSON in student and model sentences (top 25)

孟子 376, 神农 300, 孟母 85, 张骞 11, 灵芝 10, 后羿 9, 孟 9, 王 9, 嫦娥 7, 张 6, 王朋 5, 王母 4, 汉武帝 4, 子思 4, 孟轲 4, 甘父 2, 大月氏 2, 大山 2, 马 2, 梨子 2, 小孟 1, 树 1

Anything here that is not a character (or a character missing) shows where the name tagger needs help.

## Story words labelled from our own list (`story_entity`)

('孟子', 'character') 422, ('神农', 'character') 311, ('灵芝', 'object') 117, ('夹竹桃', 'object') 95, ('孟母', 'character') 93, ('张骞', 'character') 11, ('匈奴', 'group') 10, ('后羿', 'character') 9, ('大月氏', 'group') 8, ('嫦娥', 'character') 7, ('王母', 'character') 5, ('汉朝', 'place') 4, ('汉武帝', 'character') 4, ('甘父', 'character') 2

## Example parses, for checking

Each word as word/POS, then its grammatical link (relation → head word).

**mengmu_samples#1/s0** (student_sentence): 在古代中国，有一位小孩子叫孟子，他妈妈在墓地工作，所以孟子老是在墓地跟朋友祭拜。
- words: 在/P  古代/NN  中国/NR  ，/PU  有/VE  一/CD  位/M  小孩子/NN  叫/VV  孟子/NR  ，/PU  他/PN  妈妈/NN  在/P  墓地/NN  工作/VV  ，/PU  所以/AD  孟子/NR  老是/AD  在/P  墓地/NN  跟/P  朋友/NN  祭拜/VV  。/PU
- links: 在 prep→有  古代 nn→中国  中国 pobj→在  ， punct→有  有 root→ROOT  一 nummod→位  位 clf→小孩子  小孩子 nsubj→叫  叫 dep→有  孟子 dobj→叫  ， punct→有  他 nn→妈妈  妈妈 nsubj→工作  在 prep→工作  墓地 pobj→在  工作 conj→有  ， punct→有  所以 advmod→祭拜  孟子 nsubj→祭拜  老是 advmod→祭拜  在 prep→祭拜  墓地 pobj→在  跟 prep→祭拜  朋友 pobj→跟  祭拜 conj→有  。 punct→有
- names: 中国 (LOCATION), 孟子 (PERSON), 孟子 (PERSON)

**mengmu_samples#1/s1** (student_sentence): 孟母觉得这样住对孟子将来没有好处，所以她想找新的工作。
- words: 孟母/NN  觉得/VV  这样/AD  住/VV  对/P  孟子/NR  将来/NT  没有/VE  好处/NN  ，/PU  所以/AD  她/PN  想/VV  找/VV  新/VA  的/DEC  工作/NN  。/PU
- links: 孟母 nsubj→觉得  觉得 root→ROOT  这样 advmod→住  住 dep→没有  对 prep→没有  孟子 pobj→对  将来 advmod→没有  没有 ccomp→觉得  好处 dobj→没有  ， punct→觉得  所以 advmod→想  她 nsubj→想  想 conj→觉得  找 ccomp→想  新 rcmod→工作  的 cpm→新  工作 dobj→找  。 punct→觉得
- names: 孟母 (PERSON), 孟子 (PERSON)

**mengmu_samples#1/s2** (student_sentence): 为了找工作，孟母和孟子搬了很多次家。
- words: 为了/P  找/VV  工作/NN  ，/PU  孟母/NR  和/CC  孟子/NR  搬/VV  了/AS  很多/CD  次/M  家/NN  。/PU
- links: 为了 prep→搬  找 pccomp→为了  工作 dobj→找  ， punct→搬  孟母 conj→孟子  和 cc→孟子  孟子 nsubj→搬  搬 root→ROOT  了 asp→搬  很多 nummod→次  次 dep→搬  家 dobj→搬  。 punct→搬
- names: 孟母 (PERSON), 孟子 (PERSON), 次 (FREQUENCY)

**mengmu_samples#1/s3** (student_sentence): 孟子才九岁，已经搬了五次家。
- words: 孟子/NR  才/AD  九/CD  岁/M  ，/PU  已经/AD  搬/VV  了/AS  五/CD  次/M  家/NN  。/PU
- links: 孟子 nsubj→岁  才 advmod→岁  九 nummod→岁  岁 root→ROOT  ， punct→岁  已经 advmod→搬  搬 conj→岁  了 asp→搬  五 nummod→次  次 dep→搬  家 dobj→搬  。 punct→岁
- names: 孟子 (PERSON), 九 (AGE), 五 (INTEGER)

**mengmu_samples#1/s4** (student_sentence): 孟母找工作很难，不是因为她的工作经验不够，而是因为她想在老师的家工作，让孟子多学习。
- words: 孟母/NN  找/VV  工作/NN  很/AD  难/VA  ，/PU  不是/AD  因为/P  她/PN  的/DEG  工作/NN  经验/NN  不够/VA  ，/PU  而是/CC  因为/P  她/PN  想/VV  在/P  老师/NN  的/DEG  家/NN  工作/VV  ，/PU  让/VV  孟子/NR  多/AD  学习/VV  。/PU
- links: 孟母 nsubj→找  找 dep→难  工作 dobj→找  很 advmod→难  难 root→ROOT  ， punct→难  不是 dep→难  因为 prep→难  她 assmod→经验  的 assm→她  工作 nn→经验  经验 nsubj→不够  不够 pccomp→因为  ， punct→难  而是 cc→难  因为 prep→而是  她 nsubj→想  想 pccomp→因为  在 prep→工作  老师 assmod→家  的 assm→老师  家 pobj→在  工作 ccomp→想  ， punct→工作  让 ccomp→想  孟子 dobj→让  多 advmod→学习  学习 dep→让  。 punct→难
- names: 孟母 (PERSON), 孟子 (PERSON)

**mengmu_samples#1/s5** (student_sentence): 孟母终于在一位很有名的文学家找工作了。
- words: 孟母/NN  终于/AD  在/P  一/CD  位/M  很/AD  有名/VA  的/DEC  文学家/NN  找工作/VV  了/SP  。/PU
- links: 孟母 nsubj→找工作  终于 advmod→找工作  在 prep→找工作  一 nummod→位  位 clf→文学家  很 advmod→有名  有名 rcmod→文学家  的 cpm→有名  文学家 pobj→在  找工作 root→ROOT  了 dep→找工作  。 punct→找工作
- names: 孟母 (PERSON)

**model:shennong_chang_baicao/s0** (model_sentence): 在古代，人们不知道什么植物能吃，什么植物不能吃。
- words: 在/P  古代/NN  ，/PU  人们/NN  不/AD  知道/VV  什么/DT  植物/NN  能/VV  吃/VV  ，/PU  什么/DT  植物/NN  不能/VV  吃/VV  。/PU
- links: 在 prep→知道  古代 pobj→在  ， punct→知道  人们 nsubj→知道  不 neg→知道  知道 root→ROOT  什么 det→植物  植物 nsubj→吃  能 mmod→吃  吃 ccomp→知道  ， punct→吃  什么 det→植物  植物 nsubj→吃  不能 advmod→吃  吃 conj→吃  。 punct→知道

**model:shennong_chang_baicao/s1** (model_sentence): 很多人因为吃了有毒的植物，常常生病。
- words: 很多/CD  人/NN  因为/P  吃/VV  了/AS  有毒/VA  的/DEC  植物/NN  ，/PU  常常/AD  生病/VV  。/PU
- links: 很多 nummod→人  人 nsubj→生病  因为 prep→生病  吃 pccomp→因为  了 asp→吃  有毒 rcmod→植物  的 cpm→有毒  植物 dobj→吃  ， punct→生病  常常 advmod→生病  生病 root→ROOT  。 punct→生病

**mengmu_samples#1/f0/p0/k0/a0** (teacher_fix): 有一个叫孟子的小孩子
- words: 有/VE  一个/CD  叫/VV  孟子/NR  的/DEC  小孩子/NN
- links: 有 root→ROOT  一个 nummod→小孩子  叫 rcmod→小孩子  孟子 dobj→叫  的 cpm→叫  小孩子 dobj→有
- names: 孟子 (PERSON)

**mengmu_samples#1/f1/p0/k0/a0** (teacher_fix): 作家的家里找到工作了
- words: 作家/NN  的/DEG  家里/NN  找到/VV  工作/NN  了/SP
- links: 作家 assmod→家里  的 assm→作家  家里 dep→找到  找到 root→ROOT  工作 dobj→找到  了 dep→找到

**mengmu_samples#1/f2/p0/k0/a0** (teacher_fix): 房子里
- words: 房子/NN  里/LC
- links: 房子 lobj→里  里 root→ROOT

**mengmu_samples#1/f3/p0/k0/a0** (teacher_fix): 在被问到对童年应该做什么的看法时
- words: 在/P  被/SB  问到/VV  对/P  童年/NN  应该/VV  做/VV  什么/PN  的/DEC  看法/NN  时/LC
- links: 在 root→ROOT  被 pass→问到  问到 lccomp→时  对 prep→做  童年 pobj→对  应该 mmod→做  做 ccomp→问到  什么 dobj→做  的 cpm→做  看法 dobj→问到  时 plmod→在

