# Step 11 report: the teacher's error categories

- 62 categories, built from the train edits only; train edits 1187, test edits 287
- sorted with low confidence: train 126, test 35; with a second category: train 90
- unknown ids returned (sorted to other): 0

## grammar (285 train / 79 test edits)

| Category | Found by | Train | Test | Definition |
|---|---|---|---|---|
| **在+Place / 在Place + V.** (`location_with_zai`) | parser | 47 | 11 | Use 在 + Place for a location, and place the location correctly before the action when needed: 在Place + V. or 住在+Place. |
| **的 in modifier phrases** (`modifier_de_structure`) | parser | 45 | 15 | Use 的 only where a modifier needs it, and omit it in structures that do not take 的. A descriptive modifier before a noun normally needs the appropriate 的 structure. |
| **V. + Obj. structure** (`verb_object_valency`) | parser | 37 | 6 | Use each verb with the object and complement structure it allows; do not give a verb an extra object or omit a required one. |
| **V. + directional complement + Place + 来/去** (`directional_complements`) | parser | 31 | 4 | Use directional complements in the correct order, for example 走到place来/去 and V. + directional complement + Place + 来/去. Do not use forms such as 走去 or 走来Place. |
| **是……吗 / repeated Wh-Q** (`question_patterns`) | parser | 27 | 9 | Form questions with the appropriate Chinese question pattern, such as 能不能吃, 知不知道, or the repeated Wh-Q pattern for “wh-ever…”. |
| **resultative complement** (`resultative_complements`) | parser | 15 | 10 | Use a resultative complement when the action has reached its result, for example 吃到, 找到, 撞到, 把Obj. V. Resultative complement. |
| **Num. + MW. + N., no 的** (`numeral_measure_word_order`) | parser | 14 | 5 | With a number and measure word, use Num. + MW. + noun directly; normally do not add 的. Use V. + Num. + MW. + Obj. in the normal object order. |
| **想 + V.; 叫/让 + V.** (`modal_and_control_verb_complements`) | parser | 13 | 7 | 想 must be followed by a verb phrase, not a noun. Control and modal-like verbs such as 叫/让 take a following action and do not take 了 in this use. |
| **Adj. can be predicate; usually Adj. takes 很** (`adjective_predicate_degree`) | parser | 12 | 4 | An adjective can be the predicate without 是. Usually use 很 before an adjective when giving a plain description, unless another degree pattern is intended. |
| **量词选择** (`measure_word_choice`) | judgement | 9 | 2 | Use the appropriate measure word for the noun, including polite 位 and noun-specific classifiers such as 棵. |
| **miss a Subj.** (`missing_or_unclear_subject`) | parser | 9 | 4 | State the subject when it is required for grammatical clarity, especially after an inserted narrator comment or when the previous subject cannot continue. |
| **V.V. for requests or plans** (`verb_reduplication_requests`) | parser | 8 | 1 | Use V.V. to make a request or express a tentative plan, not simply for any completed narrative action. |
| **把 / 被** (`ba_bei_constructions`) | parser | 8 | 0 | Use 把 for an initiated disposal action, usually with a result or completion; use 被 for passive voice. Do not use 把 when the subject did not cause the event. |
| **病 is not a normal Adj.** (`non_adjective_degree_patterns`) | parser | 6 | 1 | Do not treat verbs or nouns such as 病 / 生病 as ordinary adjectives with 很 or 不. Use patterns such as 病得很厉害 when describing the degree. |
| **不 for habit; 没 for non-occurrence** (`negation_bu_mei`) | parser | 4 | 0 | Use 不 for habit, routine, willingness, or general negation; use 没 for an event that did not occur. Use 没 + V. for a negated action event. |

## word_choice (329 train / 75 test edits)

| Category | Found by | Train | Test | Definition |
|---|---|---|---|---|
| **near-synonyms: choose the intended word** (`near_synonym_precision`) | judgement | 71 | 19 | Choose the near-synonym whose meaning fits the intended event, duration, possibility, or degree; similar-looking words are not interchangeable. |
| **word collocation** (`collocation_selection`) | judgement | 66 | 11 | Use words with their normal collocations; a grammatically possible combination may still not be a natural Chinese phrase. |
| **fixed expression** (`fixed_expressions`) | judgement | 38 | 7 | Use conventional fixed expressions and established compounds rather than creating a literal or nonstandard combination. |
| **word class** (`word_class_choice`) | parser | 32 | 8 | Choose the word class required by the structure, for example noun, adjective, adverb, or verb, rather than using a related word of the wrong class. |
| **be specific** (`specific_noun_choice`) | judgement | 27 | 6 | Use a specific noun when the story requires one; avoid overly general words such as 人, 东西, 事情, 水果, or vague 有麻烦. |
| **看 look vs. 看到 see** (`perception_look_see`) | judgement | 26 | 4 | 看 is “look”; 看到 is “see/catch sight of” and includes the result of seeing. Choose according to whether the narrative means the attempt or the achieved perception. |
| **害得 + N/sb. + harmful result** (`haide_harmful_result`) | judgement | 16 | 6 | 害得 is followed by a person or noun and a genuinely harmful result. Do not use it for a neutral event such as 搬家 or 玩儿, or for a merely mild feeling. |
| **成为 + N. / 成才** (`become_and_profession`) | parser | 16 | 3 | 成为 is followed by an appropriate noun, especially a profession or public identity; use 成才 rather than a literal phrase for becoming successful or capable. |
| **别的 vs. 另外** (`other_vs_additional`) | judgement | 9 | 6 | 别的 means a different type or all others except the one mentioned. 另外 means an additional quantity or another/the other. |
| **老是 for something negative** (`laoshi_negative_repetition`) | judgement | 8 | 1 | 老是 means “always” with a negative or complaining tone; do not use it for a neutral or positive repeated action. |
| **找 look for vs. 找到 find** (`search_find`) | judgement | 7 | 2 | 找 means “look for”; 找到 means “find” and includes the successful result. |
| **use the wrong character** (`wrong_character`) | pattern | 6 | 0 | Use the correct written Chinese character for the intended word or adverbial form. |
| **formal words and register** (`formal_register`) | judgement | 3 | 1 | Choose words that fit the register of the sentence; some words are formal, conversational, or used only in a particular context. |
| **问 vs. ask for help / ask sb. to do** (`ask_request_verbs`) | judgement | 3 | 1 | 问 is for asking a question. Use the appropriate verb for “ask for help” or “ask somebody to do something.” |
| **听 listen vs. 听到 hear** (`listen_hear`) | judgement | 1 | 0 | 听 is “listen”; 听到 is “hear” and expresses the result of perceiving a sound. |

## coherence_reference (136 train / 28 test edits)

| Category | Found by | Train | Test | Definition |
|---|---|---|---|---|
| **1st time, briefly introduce N.** (`first_mention_introduction`) | judgement | 46 | 12 | The first time a story character appears, introduce the person with a brief identifying noun phrase rather than using only the name or pronoun. |
| **zero form: delete redundant pronoun** (`zero_redundant_pronoun`) | parser | 46 | 7 | Within the same clause or a close continuation, omit a repeated subject or possessive when Chinese naturally uses zero form. |
| **“他/她/它” is ambiguous** (`ambiguous_pronoun`) | judgement | 17 | 1 | Use a pronoun only when its referent is close and unambiguous. Repeat the name or use a clear noun phrase when more than one possible referent intervenes. |
| **这个/这种 + N. must be clear** (`demonstrative_reference`) | judgement | 10 | 2 | Use 这个, 这种, 这些, and 有的 only when the preceding context identifies exactly which entity or set they refer to. |
| **re-occur: pronoun, zero, or N.** (`pronoun_name_zero_reference`) | judgement | 9 | 2 | For a re-occurring referent, use a pronoun when it is close, zero form within the same clause, and repeat the noun/name when it is far away or something intervenes. Avoid too many repeated names or too many pronouns. |
| **他的/她的 implies ownership** (`possessive_reference`) | judgement | 8 | 4 | Do not use a possessive pronoun when it wrongly implies ownership or leaves the owner unclear; use a more precise relationship expression instead. |

## coherence_temporality (125 train / 37 test edits)

| Category | Found by | Train | Test | Definition |
|---|---|---|---|---|
| **了 completed** (`le_completed`) | parser | 69 | 16 | Use 了 for a completed action or a change of state in the narrative. Do not add it merely because an action verb appears. |
| **Time + 以后 / 后来** (`time_sequence_markers`) | pattern | 16 | 7 | Use Time + 以后 and 后来 to show a clear temporal sequence, and avoid redundant time expressions. |
| **着 durative** (`zhe_durative`) | parser | 8 | 3 | Use 着 for a durative, accompanying, or static state, including an accompanying action such as V.着 + V2. |
| **mental state V.: no 了** (`no_le_mental_state`) | parser | 7 | 0 | Mental-state verbs such as 决定 and 发现 normally take zero particle when expressing the state, decision, or discovery in this narrative use. |
| **no 了 for routine/habit** (`no_le_routine_state`) | parser | 7 | 6 | Use zero particle for routines, habits, repeated conditions, and states, especially with 常常, 每天, 有的时候, and similar expressions. |
| **在/正在 ongoing** (`zai_progressive`) | parser | 5 | 1 | Use 在/正在 for a dynamic action that is ongoing. Do not use it when the sentence is only stating a location or does not emphasize an ongoing action. |
| **过 for experience** (`guo_experience`) | parser | 5 | 0 | Use 过 to mean “have done/have experienced.” Do not use it when the stated experience has not happened yet. |
| **没 + V., no 了** (`no_le_with_mei`) | parser | 4 | 1 | After 没/没有 for a non-occurring action, do not add 了 to the action verb. |
| **no 了 for speaking word** (`no_le_speaking_word`) | parser | 3 | 2 | A saying word that introduces quoted speech normally uses zero particle, not 了. |
| **a series of actions: last one with 了** (`action_series_last_le`) | parser | 1 | 1 | When narrating a series of actions, use the aspect marking to organize the sequence; normally the final completed action takes 了. |

## coherence_connectors (137 train / 30 test edits)

| Category | Found by | Train | Test | Definition |
|---|---|---|---|---|
| **又 / 也 / 还 / 并** (`addition_repetition_connectors`) | judgement | 19 | 3 | Use additive and repetition connectors according to their meanings: 又 for repetition, 也 for similarity, 还 for an added or surprising point, and 并 to strengthen a coherent addition. |
| **只要……就 / Subj. + 就** (`conditional_jiu`) | parser | 19 | 3 | Use 只要……就 for an “as long as” condition, and place the subject and 就 so that the conditional or natural continuation relationship is clear. |
| **所以: cause-result relationship** (`cause_result_soyi`) | judgement | 16 | 2 | Use 所以 only when the preceding clause is genuinely the cause or reason for the following result. Otherwise delete it or use a connector that matches the relationship. |
| **不是……而是……** (`not_but_refutation`) | judgement | 16 | 6 | 不是……而是…… refutes something conventional or mistaken and affirms an unexpected correction. Use it only when the two alternatives have that correction relationship. |
| **loose connection / no logic relationship** (`loose_clause_connection`) | judgement | 14 | 4 | Make the relationship between clauses and sentences explicit. Add an appropriate connector, purpose, condition, place, or sequence marker when the narrative is fractured or loosely connected. |
| **和 cannot connect clauses/verb phrases** (`he_scope_coordination`) | parser | 12 | 1 | 和/跟 + noun connects multiple nouns that share the same action. Do not use it to connect whole clauses, unrelated verb phrases, adjectives, or an accompanying object that does not perform the action. |
| **比方说 / 特别是** (`example_emphasis_connectors`) | judgement | 10 | 4 | 比方说 introduces an example; delete it when no example follows. 特别是 + N, + clause singles out a typical example and must match the category being exemplified. |
| **不是……就是……** (`either_or_choice`) | judgement | 9 | 1 | 不是……就是…… means “either…or…” and requires two genuinely alternative possibilities, not two compatible purposes, states, or actions. |
| **condition is not definite** (`condition_not_definite`) | judgement | 9 | 4 | Before expressions such as 这就要看……了, state an uncertain condition or alternative, for example 会不会生病 or 要不要吃. |
| **可是/却/而: semantic turn** (`adversative_connector`) | judgement | 8 | 2 | Use 可是, 却, 而, and 但 only when there is a real contrast, unexpected semantic turn, or concession. Do not add an adversative connector without that relationship. |
| **为了 + VP.** (`purpose_weile`) | parser | 5 | 0 | Use 为了 + verb phrase to state a purpose, in the appropriate clause position; do not use it as a result connector. |

## content (51 train / 10 test edits)

| Category | Found by | Train | Test | Definition |
|---|---|---|---|---|
| **wrong information** (`incorrect_story_information`) | judgement | 43 | 8 | Retell the traditional story accurately: do not add people, places, actions, objects, or character identities that are not in the story, and do not change established facts. |
| **miss information / result** (`missing_story_information`) | judgement | 8 | 2 | Include the important scene, action, motivation, or result needed for a complete retelling, rather than leaving a key event unexplained. |

## other (124 train / 28 test edits)

| Category | Found by | Train | Test | Definition |
|---|---|---|---|---|
| **redundant** (`redundant_words`) | judgement | 79 | 19 | Delete words, names, time phrases, or repeated structures that add no meaning or repeat information already expressed. |
| **other** (`other`) | judgement | 42 | 9 | Fits no other category. |
| **add descriptive detail** (`expressive_detail_and_description`) | judgement | 3 | 0 | Use clear descriptive detail and internal-state language where needed so the retelling has sufficient scenes and is more expressive, not only a bare sequence of events. |

## How the train edits could be found

- judgement: 650 edits (54%)
- parser: 515 edits (43%)
- pattern: 22 edits (1%)

## Examples per category (train, first 4)

**redundant** (`redundant_words`)
- 我现在有良好的[-教育和]生活
- 跟孟母[-一起]搬家三次
- 他们搬家不是为了[-孟母]要住在更好的房子 — delete孟母
- 在[古代时候→古代]

**near-synonyms: choose the intended word** (`near_synonym_precision`)
- 而是他的爸爸[喜欢他练习→想要他练习]
- 所以孟子[从早到晚→都]没有空
- 他们⟦才搬了三次家⟧ — 才 + Num. to express “small, few”, but here搬了三次家 is a large quantity
- 而是因为[学校→学业]很难

**了 completed** (`le_completed`)
- 原来他昨天吃[+了]一张纸 — 了completed
- 他们搬到[+了]城市 — 了completed
- 所以妈妈跟孟子一起搬家[+了] — 了completed
- 旅行的时候孟子经验[+了]很多的看法 — 了completed

**word collocation** (`collocation_selection`)
- 我现在有[良好→幸福]的教育和生活 — 良好 is usually not with生活
- 在第一个[房子→地方]
- 在[第三个房子→第三个地方]
- 孟母希望这个地方[对孟子长大很合适→适合孟子成长]

**在+Place / 在Place + V.** (`location_with_zai`)
- 孟母终于在[一位很有名的文学家→作家的家里]找工作了
- 他每天在文学家的[房子上→房子里]学 — 在+Place
- 他们搬家不是为了孟母要住在更好的房子[+里] — 在+Place
- 他[离墓地住很近→住在离墓地很近的地方]

**1st time, briefly introduce N.** (`first_mention_introduction`)
- ⟦孟子⟧一直祭拜 — better to briefly introduce “孟子” when this character first appears
- ⟦孟子⟧和孟母住在一起 — better to briefly introduce “孟子” when this character first appears
- ⟦孟子⟧跟他妈妈常常搬家 — better to briefly introduce “孟子” when this character first appears
- ⟦孟子⟧从小到大一直搬家 — better to briefly introduce “孟子” when this character first appears

**zero form: delete redundant pronoun** (`zero_redundant_pronoun`)
- 就[-自己]觉得我不想我的儿子在这个地方长大
- 就自己觉得[-我]不想我的儿子在这个地方长大
- [-他]跟他的妈妈住在一个小房子
- [-孟子跟他的妈妈]已经搬家了

**的 in modifier phrases** (`modifier_de_structure`)
- 他们去了[一个房子，在购物中心的旁边→一个在购物中心旁边的房子]
- 有一个[男孩子叫孟子→叫孟子的男孩子]和他的妈妈
- [搬家十年→在搬家的十年里]
- 搬家[带给了孟子→带给孟子的]不是悲伤的童年

**wrong information** (`incorrect_story_information`)
- 而是⟦他的爸爸⟧喜欢他练习 — wrong information, his father did not appear in this story
- ⟦他爸爸说⟧ — wrong information, his father did not appear in this story
- ⟦难怪我们没有钱⟧ — wrong information, 搬家因为孟母觉得it is not good to imitate how to buy and sell
- [他成为很有名的老师→哲学家]

**other** (`other`)
- [别→不要]吃纸
- 孟子[+还是]从早到晚努力学习
- 孟子从早到晚[+都]努力学习
- [古代的时候→在古代]

**fixed expression** (`fixed_expressions`)
- 不是他喜欢[学习写文字→写字]
- [是大人的时候→长大以后]
- [古代的时候→在古代]
- [大人的时候→长大以后]

**V. + Obj. structure** (`verb_object_valency`)
- 而是她觉得墓地[不合适→不适合]孩子们玩
- 孟母看孟子老是[+学]做他们住很近的人做的事情
- 从早到晚孟子跟小朋友看[+别人]祭拜
- 他们听[饭馆和商店→在饭馆和商店人们说话的声音]

**word class** (`word_class_choice`)
- 孟母[恐怕→怕]孟子住在墓地的旁边对孟子有影响 — 恐怕usually does not take Subj. except 我
- 难怪他成为[名的→有名的]哲学家
- 旅行的时候孟子[经验→了解]很多的看法 — “经验” is a noun.
- 因为他这么[无→无聊] — 无聊？add所以

**V. + directional complement + Place + 来/去** (`directional_complements`)
- 这害得孟母[离学校很近搬家→搬家到离学校很近的地方]
- 他们[去了→搬到了]一个房子
- 所以孟子的妈妈[搬家→搬到]很安全很安静的公寓
- 所以她带孟子[-到一个]城市搬家了

**是……吗 / repeated Wh-Q** (`question_patterns`)
- 小孟[在→在哪儿？]
- 这个植物你[能吃吗→能不能吃]
- 这就要看蘑菇[看不看像→像不像]伞
- 让每个人都知道[什么植物能不能吃→什么植物能吃，什么植物不能吃]

**be specific** (`specific_noun_choice`)
- 练习写[文字→字] — 文字 is a general term, not for specific individual characters
- [人→来祭拜的人]一直在墓地大声哭 — “人“ is too general and too vague, and does not stand alone
- 原来他妈妈选择[特别好的地方孟子长大→对孟子成长特别好的环境]
- [一个家人→孟子一家人]住在中国

**看 look vs. 看到 see** (`perception_look_see`)
- 他妈妈[看→看到]他跟别的孩子在墓地里祭拜 — 看look vs.看到see
- 她[一看这→一看到这样] — 看look vs.看到see
- 孟母[一看→看到]孟子祭拜 — 看look vs.看到see
- 孟子跟朋友[看→看到]很多的大人在墓地祭拜 — 看look vs.看到see

**又 / 也 / 还 / 并** (`addition_repetition_connectors`)
- 孟母[也觉得→又觉得]在市场的旁边对孟子不合适的地方长大 — “又“ emphasizes repeating vs. ”也“ emphasizes similarity
- 孟子跟他的妈妈[已经→就又]搬家了
- 妈妈觉得他们[应该又搬家了→又应该搬家了] — 又+ modal V.
- 害得他的妈妈[很生气紧张→又生气又紧张]

**只要……就 / Subj. + 就** (`conditional_jiu`)
- [+就]开始祭拜 — 才 Num.就V.
- [+就]跟孟母一起搬家三次 — 才 Num.就V.
- [+就]开始学哲学 — 才 Num.就V.
- 孟子才三岁[+就]开始搬家 — 才Num.就V.

**“他/她/它” is ambiguous** (`ambiguous_pronoun`)
- [他然后没有朋友→然后孟子失去了这个朋友] — “他“ is ambiguous
- [他的→孟子的]妈妈告诉他：你不能祭拜 — “他的” is ambiguous
- [她→他的妈妈]认为搬家对孟子有好处 — “她” is ambiguous
- 孟母发现[孩子们→孟子]老是用功工作 — “孩子们” is ambiguous

**害得 + N/sb. + harmful result** (`haide_harmful_result`)
- 害得[-对]孟子有不好的影响 — 害得+Sb.+V.
- 害得对孟子[有→受到了]不好的影响 — 害得+Sb.+V.
- ⟦这害得孟母决定搬家⟧ — “害得“ is followed by something harmful, 搬家is not harmful
- 这⟦害得孟母离学校很近搬家⟧ — “害得“ is followed by something harmful, 搬家is not harmful

**成为 + N. / 成才** (`become_and_profession`)
- 他成为了一个[人写文章老是好→写文章非常好的作家]
- 他成为[有名的→有名的哲学家] — 成为+N
- 难怪他成为很聪明[+的人]
- 很多人想孟子[做→成为]哲学家是本质的

**Time + 以后 / 后来** (`time_sequence_markers`)
- [常常祭拜以后，→常常在祭拜以后]孟子和他的妈妈一起去买东西
- 他难怪[+后来]成为了一个很聪明的哲学家
- [+原来]他成长在学校的旁边
- [以后→后来]每年搬家 — 后来每年都搬家

**所以: cause-result relationship** (`cause_result_soyi`)
- [-所以]妈妈跟孟子一起搬家
- ⟦所以⟧孟子会跟别的教授学哲学 — 这样in this way
- [结果他→所以，]取得生活经验 — “结果” for unexpected result
- ⟦所以⟧孟子常常玩玩 — “所以” is not appropriate, since here is not a cause-effect relationship

**不是……而是……** (`not_but_refutation`)
- 孟子的家人[-不是富有的，而是他们]很穷
- 孟子的家人⟦不是富有的，而是他们很穷⟧ — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- 他们[不是住在购物中心的旁边，而是住在学校的旁边→搬到了学校旁边] — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong
- 可是他不[-是]在家读书 — “不是……而是……” is used to refute something conventional and affirm something unexpected, and to correct something wrong

**resultative complement** (`resultative_complements`)
- 他还[想起来→想得起来]
- 害得孟子[不可以睡觉好→睡不好觉]
- 孟子说：我为什么老是学习？不能跟别人玩？他的妈妈说：跟别人玩害得你[不学习好→学习不好]
- 他⟦一吃新的植物就写了植物有没有毒⟧ — 吃到result, 写下

**Num. + MW. + N., no 的** (`numeral_measure_word_order`)
- 跟孟母一起[搬家三次→搬了三次家] — 了completed，V. + Num. + MW. + Obj.
- 我们要[搬家再一次→再搬一次家] — 再V. + Num. + MW. + N.
- 我心里不让我们[搬家再一次→再搬一次家]
- [一天三次搬家了→一年搬了三次家] — V. + Num. + MW. + Obj.

**loose connection / no logic relationship** (`loose_clause_connection`)
- [他对孩子的童年的看法是，说→在被问到对童年应该做什么的看法时，他说：]孩子童年多玩或者多学习重要
- ⟦妈妈让孟子每天上课，孟子长得很乖，很聪明⟧ — loosely connected, unclear between-sentence relationship
- ⟦孟子从早到晚想玩玩儿，所以他和朋友坐墓地在祭拜⟧ — loosely connected with the preceding sentence
- ⟦孟子很聪明，不是学习害得，而是常常搬家⟧ — no logic relationship, fractured

**想 + V.; 叫/让 + V.** (`modal_and_control_verb_complements`)
- 孟子的妈妈叫[-了]孟子搬家 — 叫/让 is a modal verb, no了
- 孟子的妈妈一直[想她的儿子在很好的地方长大→想让她的儿子在很好的地方长大] — 想 + V., cannot be followed by N.
- 就自己觉得我不想[我的儿子→儿子不应该]在这个地方长大
- 他的妈妈[不想跟他的朋友去墓地→不想让他跟朋友去墓地] — otherwise it means his mother didn’t want to go with his friend to the graveyard.

**Adj. can be predicate; usually Adj. takes 很** (`adjective_predicate_degree`)
- 第二个房子离购物中心[+很]近 — usually Adj. takes 很
- 孟母看出来孟子老是[+很]难过 — usually Adj. takes 很
- 孟子[是淘气的孩子→很淘气]
- 而是学多[+很]文章

**和 cannot connect clauses/verb phrases** (`he_scope_coordination`)
- 孟子才四岁就开始学文学[-和]写汉字 — 和cannot connect verb phrases
- 孟子决定[他可以学习和高兴→这样又能学习又能每天都很高兴]
- 哲学人很聪明[和→也很]重要 — 和cannot connect Adj.
- 从早到晚[看和写文章→看书、写文章] — 和cannot connect verb phrases

**这个/这种 + N. must be clear** (`demonstrative_reference`)
- [小房子→这个小房子]离一个墓地不太远 — otherwise unclear which house
- [这个小孩子→儿子]叫孟子 — “这个小孩子” is unclear and ambiguous
- 因为我们不知道[+这个]植物是什么
- 神农的朋友给他[这植物→灵芝]

**比方说 / 特别是** (`example_emphasis_connectors`)
- 这个大山⟦特别是⟧的 — 特别是+N, + clause
- ⟦特别是夹竹桃⟧对身体更不好 — 特别是is used to single out a typical example, but夹竹桃is not an example of灵芝
- [-比方说，]他又不能思考清楚又不能问帮忙 — 比方说is used to express “for example”, delete it
- 灵芝[特别是帮忙→特别有用] — ”特别是+N, + Clause” is used to single out a typical example

**量词选择** (`measure_word_choice`)
- 有[一位小孩子叫孟子→一个叫孟子的小孩子] — “位” is a polite MW.
- 他正好吃[一毒→一种有毒]的花
- 有[一位人→一个人]来了
- 老板第一次看到[一黄色新的花→一种新的黄色的花]

**miss a Subj.** (`missing_or_unclear_subject`)
- [+孟子]练习写文字 — miss a Subj.
- 因为[+他]老是去墓地吃祭品
- [+他]就生病了 — otherwise it is ambiguous who gets sick
- [+这朵花]漂亮是漂亮 — here needs a subject

**别的 vs. 另外** (`other_vs_additional`)
- 他测试[别的→各种]植物 — “别的” is for “a different type”, and “all else except the spoken one”
- 因为[别的人→有人]正好在他的旁边 — “别的” is for “a different type”, and “all else except the spoken one”
- 然后他又找到了[别的→另外一种]白花 — “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”
- [一个别的人→另外一个人]跟神农说 — “别的” is for “a different type”, and “all else except the spoken one”, whereas “另外“ is for “addition in quantity”, and “another, the other”

**re-occur: pronoun, zero, or N.** (`pronoun_name_zero_reference`)
- [妈妈→孟母]老是工作了 — “妈妈” here is ambiguous
- [孟子→他]每个地方才住了一年 — replace the second孟子with他
- ⟦孟子⟧从早到晚想玩玩儿 — replace孟子with他
- [-孟子]和孟子的妈妈一直住在墓地的旁边

**不是……就是……** (`either_or_choice`)
- 说孩子童年多玩[或者→和]多学习重要
- [不是学习中文，他就是跟老师说中文→他不是学习中文，就是跟老师说中文] — Subj. at the beginning of 不是……就是……
- 从早到晚他[学习不是历史，就是哲学→不是学习历史，就是学习哲学]
- [不是孟子幸福的生活就是孟子的妈妈开心→虽然孟子的生活不快乐，可是妈妈很开心]

**condition is not definite** (`condition_not_definite`)
- [+如果吃了夹竹桃，]这就要看你也吃不吃灵芝了 — e.g., 如果吃了夹竹桃
- [+病能不能好？]这就要看你也吃不吃灵芝了
- ⟦他有时候病了⟧ — the component before “这就要看……了“ should be “not definite” condition, 他会不会生病
- [+蘑菇能不能吃，]这就要看蘑菇看不看像伞 — e.g., 蘑菇能不能吃

**V.V. for requests or plans** (`verb_reduplication_requests`)
- 孟子从早到晚想[玩玩儿→玩儿] — V.V. is used to make requests or plans
- 孟子老是想[玩玩→玩] — V.V. is used to make requests or plans
- 在家不是学习就是[玩玩→玩] — V.V. is used to make requests or plans
- 孟轲老是[看看→去看]别的人

**把 / 被** (`ba_bei_constructions`)
- 所以他[把灵芝→用灵芝]治好了他的朋友们
- 然后神农[给生病朋友灵芝→把灵芝拿给生病的朋友] — avoid “生病的朋友“ and “灵芝” close to each other
- [叫了这个对身体有好处的植物→把这个对身体有好处的植物叫做]灵芝
- 得问男人[给他地方上像蘑菇一样的植物吃了→把地上像蘑菇一样的植物给他吃了] — to avoid “他” and “地上像……的植物” too close to each other

**老是 for something negative** (`laoshi_negative_repetition`)
- 孟子[跟老师老是学习中文→一直学习中文] — “老是“ for something negative, used to complain
- 所以孟子[老是→一直]在学习 — “老是“ for something negative, used to complain
- 孟母⟦老是⟧搬家 — “老是“ for something negative, used to complain
- 他写汉字[老是→一直]写得很好 — “老是“ for something negative, used to complain

**他的/她的 implies ownership** (`possessive_reference`)
- 有一个妈妈和[他的→她的]儿子
- 孟母觉得孟子不喜欢[他的小的城→这个小城市] — “他的……” indicates that孟子owns this city
- [他的人民→他发现人们]又饿又病 — “他的人民”implies that神农is a king
- [在他的旅行，→旅行中，]神农发现很多植物

**着 durative** (`zhe_durative`)
- 她[穿→穿着]很漂亮的衣服 — 着durative
- 他[拿说→拿着花说] — 着durative
- 神农很常[走去→走着]找饭 — 走着durative
- 找到了开着[+的]黄色的像星星一样的花

**可是/却/而: semantic turn** (`adversative_connector`)
- [-可是]孟子的妈妈一直很控制他
- ⟦可是⟧他很聪明 — no “semantic turn” relationship, so可是is inappropriate
- ⟦而⟧追求知识是很重要的 — “而” is not appropriate, because here is no “semantic turn”
- 他才三岁[+，可是一直]的以后待在墓地里

**miss information / result** (`missing_story_information`)
- ⟦孟母看出来孟子老是难过，害得他不能好好学习。⟧孟母恐怕孟子住在墓地的旁边对孟子有影响 — miss information: 孟子 imitated how to offer sacrifices
- 有一个男孩子叫孟子和他的妈妈[+住在一起]
- 有一个妈妈和他的儿子[+住在一起]
- 有一个孩子和他的妈妈[+住在一起]

**找 look for vs. 找到 find** (`search_find`)
- 孟母终于在一位很有名的文学家[找→找到]工作了 — 找look for vs. 找到find
- 一个人正好[找了→找到了]神农 — 找look for vs.找到find
- 神农开始[-找]我们可以吃的植物
- 神农开始找[+找到]我们可以吃的植物

**mental state V.: no 了** (`no_le_mental_state`)
- 她决定[-了]以后搬出去学校的旁边 — 决定is a mental state verb, no了
- 孟子⟦决定了⟧祭拜 — 决定is a mental state verb, no了
- 决定[-了]吃外面的植物 — “决定“ is a mental state verb, no了
- 他发现[-了]黄色花有毒 — 发现is a mental state verb, no了

**no 了 for routine/habit** (`no_le_routine_state`)
- 妈妈老是工作[-了] — no了for routine/habit
- 孟子一直跟他的朋友⟦去了⟧墓地祭拜 — no了for routine/habit
- 孟子从早到晚[学了新的东西→学习新知识]
- 他们常常生病[-了] — no了for routine/habit

**病 is not a normal Adj.** (`non_adjective_degree_patterns`)
- 一天孟子[病了很重→病得很重]
- 这朵花他一吃[就很生病→就病得很重] — “生病”cannot be with “很”
- [然后，不病→就好了] — “病” is not a normal Adj., so it cannot be with 很 or 不
- 神农看他的朋友[很生病→病得很重] — “生病” is not an Adj., so it cannot be with 很 or 不

**use the wrong character** (`wrong_character`)
- [-感]觉得身体健康
- 这个坏人好像以为自己有我们家的[所有全→所有权]！但并不是这样
- 这个坏人好像以为自己有我们家的所有⟦全⟧！但并不是这样 — use the wrong character
- 他怎么能随便⟦马虎得⟧掉我家庭呢？一点都不合理 — 马虎地V., use the wrong character

**在/正在 ongoing** (`zai_progressive`)
- 而是因为住在那里以后孟子[一直在没读书→一直没在读书]
- 孟子[一直学了→一直在学习]很多东西 — 一直在+V., emphasizing always ongoing
- 孟子不是[-在]看商店的员工 — here is not emphasizing “ongoing”
- 就是[-在]跟其他的孩子玩商店的游戏 — here is not emphasizing “ongoing”

**过 for experience** (`guo_experience`)
- 他跟很多人[打交道→打过交道] — “过” for “have done, experience”
- 原来他的父母都[没做过而祭拜→没祭拜过]
- 他认为没做过[祭拜的→祭拜过的]孩子的父母老是死了
- 他们[在到处的中国住→在中国各地都住过] — “过” experience, have done, Place到处都 + Clause

**为了 + VP.** (`purpose_weile`)
- 他们搬家不是为了孟母[-要]住在更好的房子 — 为了 + VP.
- [每次搬家她都辛苦地工作，为了给孟子提供更好的学习环境→为了给孟子提供更好的学习环境，每次搬家她都辛苦地工作] — “为了……” cannot be in the latter clause
- [+为了帮助人们找到能吃的植物，]神农旅行了 — it is loosely connected with the previous sentence, better add “为了帮助人们找到能吃的植物”, 神农决定去旅行尝试新的植物，“过” is to express “experience”, now the experience has not yet been experienced
- [+为了找到没有毒的植物，]所以他去了又空又高的山 — “所以” is inappropriate because here is not a result, delete it, add “为了找到没有毒的植物”

**不 for habit; 没 for non-occurrence** (`negation_bu_mei`)
- 孟母觉得这个环境[不对孩子的成长有→对孩子的成长没有]好处
- 这就要看你也吃[不→没]吃灵芝了 — 不for habit/routine/willingness, 没for non-occurrence of an event
- 现在他们懂什么植物[不毒→没有毒]
- [没→不]再有毒了

**没 + V., no 了** (`no_le_with_mei`)
- 神农没死[-了] — 没+ V.
- 所以他没死[-了] — no了in “没+V.”
- 和他[没病了→病好了] — 没 +V., no了, the verb is an action verb
- 可是他没有吃[-了] — no了in “没+V.”

**formal words and register** (`formal_register`)
- 墓地的人[真→很]影响孟子 — “真” is usually used in conversation
- 他这个没有礼貌的人每天爬上⟦本树⟧ — 本+N. is usually used in formal advertisement/news, also it indicates the author owns the tree, which is not the fact: the author is a pear, who does not own the whole pear tree. 爬上这棵树。
- 但政府实行的改革经济一系列政策⟦就让⟧他失业 — “使” is more formal and better fit other formal words like “失业

**问 vs. ask for help / ask sb. to do** (`ask_request_verbs`)
- 他又不能思考清楚又不能[问帮忙→找别人帮忙] — the “ask” in “ask for help” is not问
- 神农[问人帮他→请人]给他灵芝 — the “ask” in “ask for help” is not问
- 得[问→让]男人给他地方上像蘑菇一样的植物吃了 — the “ask” in “ask sb. to do” is not问

**no 了 for speaking word** (`no_le_speaking_word`)
- 所以她问[-了] — no 了for speaking word
- 他问[-了] — no了for speaking word introducing quoted speech
- 神农说：我死了吗？他一说[-了] — no了for speaking word

**add descriptive detail** (`expressive_detail_and_description`)
- 结果他取得[+很多]生活经验
- [植物→一种绿色的植物]他觉得好吃得很
- 古代的生活很多的人[+每天都]吃很多的植物

**听 listen vs. 听到 hear** (`listen_hear`)
- 他们[听→听到]饭馆和商店 — 听listen vs.听到hear

**a series of actions: last one with 了** (`action_series_last_le`)
- 他走了很远的路去[-了]学哪些植物可以入药

