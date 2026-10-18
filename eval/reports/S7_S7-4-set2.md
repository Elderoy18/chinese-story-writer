# S7 measurement: S7-4-set2

Runs: S7-4-r4, S7-4-r5, S7-4-r6 -- snapshot `base-v6`, test set `eval/test_set_h20.json` (20 stories, 60 scenes). Judge gpt-5.6-terra (medium), prompts as `eval/v1_vs_v2/score.py`.

Scenes left out because the judge prompt was refused by OpenAI's content filter (all runs alike): none; scored scenes: 60. Other refusals: none.

## Accuracy (her order of priority), mean (lowest–highest) over the runs

| | |
|---|---|
| False positives / scene | 0.59 (0.50–0.75) |
| Incorrect corrections / scene | 0.44 (0.37–0.48) |
| Items fully right | 70% (69%–71%) |
| Corrected text not fully correct | 16% (13%–18%) |
| Partial sentences | 8% (7%–9%) |
| Items in Other / Content | 0% (0%–0%) |
| Wrong category (Grammar & Vocabulary as one) | 5% (4%–7%) |
| Her flagged scenes caught (content) | 99% (98%–100%) |
| Content notes worded 'miss…' / 'need…' | 100% (100%–100%) |
| Good expressiveness ideas: 孟母 | 71% (70%–73%) |
| Good expressiveness ideas: 神农 | 80% (71%–87%) |
| Recall of her corrections | 75% (74%–76%) |
| Items per run | 301 / 277 / 296 |

## Consistency across the runs (same input, same retrieval)

| | |
|---|---|
| Places flagged in every run | 184/297 (62%) |
| Places flagged in only one run | 56/297 (19%) |
| &nbsp;&nbsp;of which wrong (false positive or incorrect) | 28/56 (50%) |
| Places in every run: **lexical** (identical corrected text) | 61/184 (33%) |
| Places in every run: **information** (same error, equivalent fix) | 127/184 (69%) |
| Places in every run: same error identified | 149/184 (81%) |

## Retrieval

- Jaccard of retrieved chunks between runs, per scene: min 1.00, mean 1.00 (180 pairs) -- 1.0 = every run saw the same chunks, so any run-to-run difference is the model's.
- **Card reach**: her corrections whose rule card was in the prompt: 71/167 (43%).

Rule cards by how many of their places they reached (run 1; rules with 2+ places):

| Rule card | Reached / places |
|---|---|
| verb_object_collocation | 0/14 |
| adverbial_word_order | 0/9 |
| measure_word | 0/7 |
| reference_form | 0/6 |
| example_marker_tebie_bifang | 0/4 |
| adjective_predicate | 0/3 |
| you_zai_distinction | 0/2 |
| aspect_zhe_durative | 0/2 |
| dou_totality | 0/2 |
| word_choice | 6/48 |
| attributive_modifier_de | 1/6 |
| redundancy_delete | 4/21 |
| haide_harmful_result | 1/5 |
| resultative_complement | 4/15 |
| location_zai_place | 2/6 |
| bushi_ershi_construction | 1/3 |
| word_class_misuse | 3/7 |
| coherence_connectives | 4/9 |
| a_not_a_question | 3/5 |
| time_expression | 9/13 |
| cai_jiu_construction | 3/4 |
| zhe_jiu_yao_kan | 3/4 |
| aspect_le_completed | 29/29 |
| character_introduction_first_mention | 5/5 |
| ambiguous_reference | 3/3 |

## Citations (each error item names the rule it applies)

| | S7-4-r4 | S7-4-r5 | S7-4-r6 |
|---|---|---|---|
| Items with a citation | 301/301 (100%) | 276/277 (100%) | 296/296 (100%) |
| ... citing a rule card / teacher rule that was in the prompt | 185/301 (61%) | 175/277 (63%) | 185/296 (62%) |
| ... citing a card or rule that was NOT in the prompt | 0/301 (0%) | 0/277 (0%) | 0/296 (0%) |
| ... citing the vocabulary list | 29/301 (10%) | 24/277 (9%) | 25/296 (8%) |
| ... citing [rule: none] | 87/301 (29%) | 77/277 (28%) | 86/296 (29%) |
| Wrong (false positive or incorrect) among items citing rule | 26/136 (19%) | 26/125 (21%) | 27/137 (20%) |
| Wrong (false positive or incorrect) among items citing teacher rule | 11/49 (22%) | 6/50 (12%) | 10/48 (21%) |
| Wrong (false positive or incorrect) among items citing vocab list | 6/29 (21%) | 6/24 (25%) | 5/25 (20%) |
| Wrong (false positive or incorrect) among items citing rule: none | 24/87 (28%) | 20/77 (26%) | 19/86 (22%) |
| Wrong (false positive or incorrect) among items citing no citation | – | 0/1 (0%) | – |

Places flagged in every run that cite the same rule in every run: 126/184 (68%).

## Scene check (end of story, one verdict per required scene)

- Required scenes given the same verdict in every run: 84/120 (70%)
- Verdicts over all runs: {'partly told': 140, 'wrong': 72, 'missing': 101, 'told': 47}
- Stories where the runs listed different numbers of scenes: 0/20

## Accuracy split: retrieval and generation

Items at a place she corrected (generation accuracy on real errors):

| | S7-4-r4 | S7-4-r5 | S7-4-r6 |
|---|---|---|---|
| Items at her corrections (with a corrected text) | 196 | 195 | 186 |
| **Lexical accuracy**: corrected text is hers (any of her alternatives) | 62/196 (32%) | 60/195 (31%) | 62/186 (33%) |
| **Information accuracy**: right fix, clean corrected text (judge) | 161/196 (82%) | 150/195 (77%) | 137/186 (74%) |

Her corrections (with a rule card), split by whether retrieval brought the card:

| | S7-4-r4 | S7-4-r5 | S7-4-r6 |
|---|---|---|---|
| **Retrieval accuracy** (card reach) | 71/167 (43%) | 71/167 (43%) | 71/167 (43%) |
| **Generation accuracy given the card**: caught and rightly fixed | 53/71 (75%) | 52/71 (73%) | 50/71 (70%) |
| Generation accuracy without the card | 65/96 (68%) | 64/96 (67%) | 56/96 (58%) |

## Attribution: why her corrections were missed or got a wrong fix

| | S7-4-r4 | S7-4-r5 | S7-4-r6 |
|---|---|---|---|
| generation: card there, error missed | 11 | 11 | 10 |
| generation: card there, fix wrong | 7 | 8 | 11 |
| no card for this rule | 1 | 1 | 1 |
| retrieval: card not there, error missed | 23 | 22 | 25 |
| retrieval: card not there, fix wrong | 8 | 10 | 15 |
| right | 53 | 52 | 50 |
| right (without its card) | 65 | 64 | 56 |

(Blame needs her correction's rule card: 'retrieval' = the card was not in the prompt; 'generation' = it was, and the model missed or misapplied it.)

## Places flagged in only some runs, or with different fixes

- mengmu_samples#10 scene 1 (3/3 runs) -- Runs 1 and 3 address the placement of 在墓地里, while Run 2 addresses repetition of 孟子 rather than the same grammar error.
  - run 1: 喜欢玩在墓地里：喜欢在墓地里玩，The place phrase should come before the verb it modifies. [rule: none]
  - run 2: Coherence (Reference): 孟子和他的朋友：他和朋友，Use a pronoun when the character was named in the immediately preceding sentence and no competing refere
  - run 3: 喜欢玩在墓地里，装祭拜：喜欢在墓地里玩，装作祭拜，Place phrases normally come before the action verb, and 装作 must be followed by the action someone is pretending to 
- mengmu_samples#10 scene 1 (2/3 runs) -- The runs do not identify the same issue, and Run 1 incorrectly changes the already correct phrase “五岁的时候” while Run 2 flags nothing.
  - run 1: 五岁的时候：五岁的时候，The structure ……的时候 requires 的 after a multi-syllable phrase. [teacher rule: de_shihou]
  - run 2: —
  - run 3: Coherence (Reference): 孟子五岁的时候：他五岁的时候，Use a pronoun for Mengzi because he remains the clear referent from the previous sentence. [rule: char
- mengmu_samples#10 scene 1 (3/3 runs) -- Run 1 changes aspect with 了, whereas Runs 2 and 3 recast the moving event to make Mengzi’s mother the agent.
  - run 1: Coherence (Temporality): 跟妈妈搬家：跟妈妈搬了家，This is a completed move at a specific age, so the completed action needs 了. [rule: aspect_le_complete
  - run 2: 跟妈妈搬家：孟母带着他搬家，The subject who moves together with someone uses 跟; when the mother takes her child to move, use 带着. [vocab list]
  - run 3: 跟妈妈：孟母带着他，The original wording presents Mengzi as simply accompanying his mother. To describe the mother moving Mengzi, make the mother the 
- mengmu_samples#10 scene 1 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 妈妈认为：她认为，The mother was mentioned in the preceding sentence, so a pronoun is natural for this close re-occurrence. [r
- mengmu_samples#10 scene 2 (3/3 runs) -- All runs flag the same use of 老是, but the teacher retains 老是 and instead corrects the sentence’s causal relationship.
  - run 1: 老是读书：一直读书，老是 often expresses complaint or an unwanted repeated action, while the intended meaning here is a regular study habit. [vocab list
  - run 2: 老是读书：一直读书，This is a neutral result of having no friends, while this word carries a complaining or negative connotation. [rule: laoshi_negati
  - run 3: 老是：一直，老是 carries a complaining or negative tone, while 一直 neutrally describes the continuing habit of reading. [vocab list]
- mengmu_samples#10 scene 2 (3/3 runs) -- Runs 1 and 2 add 了 to 搬到, while Run 3 instead changes 子思 to 他, so they address different issues.
  - run 1: Coherence (Temporality): 搬到子思老师的家：搬到了子思老师的家，The move is a completed narrative action, so 搬到 takes 了. [rule: aspect_le_completed]
  - run 2: 搬到：搬到了，The move is a completed past action, so the verb needs the completion marker. [rule: aspect_le_completed]
  - run 3: Coherence (Reference): 子思：他，子思老师 was named very recently and no other male character is competing in this sentence, so a pronoun is more nat
- mengmu_samples#10 scene 2 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 孟子和孟母：他们，Both characters were mentioned in the immediately preceding sentence, so a pronoun naturally refers back to 
- mengmu_samples#10 scene 3 (3/3 runs) -- All runs target the same verb, but the teacher marked no error here, so adding 了 is not a required correction.
  - run 1: Coherence (Temporality): 他成为很有名的哲学家：他成为了很有名的哲学家，Becoming a philosopher is a completed change of state in the narrative, so the verb needs 了.
  - run 2: Coherence (Temporality): 成为：成为了，Becoming a well-known philosopher is a completed change of state, so it needs 了. [rule: aspect_le_completed]
  - run 3: Coherence (Temporality): 成为很有名的哲学家：成为了很有名的哲学家，This is a completed change of state in the narrative, so the verb takes 了. [rule: aspect_le_co
- mengmu_samples#12 scene 1 (1/3 runs)
  - run 1: Coherence (Conjunction): 可是：—，可是 introduces contrast, but the previous sentence does not set up an expectation that the next sentence oppose
  - run 2: —
  - run 3: —
- mengmu_samples#12 scene 1 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: 古代：在古代，Use the preposition with this historical time expression when it introduces the sentence. [rule: time_expression]
- mengmu_samples#12 scene 2 (3/3 runs) -- Run 1 only corrects “不是适合” to “不适合,” while Runs 2 and 3 also address the inappropriate 不是……而是…… contrast structure.
  - run 1: 不是适合孟子：不适合孟子，For a negative evaluation with “适合,” use “不适合”; “不是适合” would need a following noun phrase such as a place or situation. [rule: 
  - run 2: Coherence (Conjunction): 住在商店的旁边不是适合孟子，而是让他觉得很伤心：住在商店的旁边不适合孟子，因为这让他觉得很伤心，sadness is a reason that the place is unsuitable, not an alternativ
  - run 3: 不是适合孟子，而是让他觉得很伤心：不适合孟子，只会让他觉得很伤心，Use the negative predicate 不适合 for a situation that is unsuitable. 不是……而是…… should correct or replace one c
- mengmu_samples#12 scene 2 (2/3 runs) -- Run 1 flags the additive “也”, while Run 3 flags the causal order of “难怪…原来…”, and Run 2 flags nothing.
  - run 1: Coherence (Conjunction): 孟子也没有朋友：孟子没有朋友，“也” is additive and needs an earlier comparable statement; no one else has been stated to have no fr
  - run 2: —
  - run 3: Coherence (Conjunction): 孟子也没有朋友，难怪他老是看起来不高兴：难怪孟子老是看起来不高兴，原来他没有朋友，Use 难怪 for the conclusion first and 原来 for the explanation that reveals it
- mengmu_samples#12 scene 3 (3/3 runs) -- Runs 1 and 3 address aspect marking, while Run 2 only changes the noun phrase to a pronoun.
  - run 1: Coherence (Temporality): 搬到学校的旁边住：搬到学校的旁边住了，The move and beginning to live there are completed narrative actions; in a series of actions, on
  - run 2: Coherence (Reference): 孟母和孟子搬到学校的旁边住：他们搬到学校的旁边住，Both characters were established in the earlier scenes, so the collective pronoun is natural
  - run 3: Coherence (Temporality): 孟母和孟子搬到学校的旁边住：孟母和孟子搬到了学校的旁边住，The move is a completed narrative event, so `了` is needed after the verb-result sequen
- mengmu_samples#18 scene 1 (2/3 runs) -- Runs 1 and 3 flag the same repetition issue, but Run 2 provides no item or correction.
  - run 1: Coherence (Reference): 孟子和孟子的妈妈住在这里：孟子和他的妈妈住在这里，use a pronoun for the already established possessor instead of repeating the name in the sam
  - run 2: —
  - run 3: Coherence (Reference): 孟子和孟子的妈妈住在这里：孟子和他的妈妈住在这里，use a pronoun for the mother after the first mention rather than repeating the name in the s
- mengmu_samples#18 scene 1 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: 有一个男孩名字叫孟子：有一个男孩叫孟子，use the verb phrase for naming a person; the original structure incorrectly treats the name as the subject of the naming
- mengmu_samples#18 scene 1 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Conjunction): 因为人们在祭拜，他们一直在哭：因为人们在祭拜，所以他们一直在哭，add 所以 to complete the cause-and-effect connector pair. [rule: none]
- mengmu_samples#18 scene 2 (3/3 runs) -- All runs target “跟孟子搬家,” but this wording is acceptable here and the teacher did not identify it as an error, so replacing it with “带着孟子搬家” is unnecessary.
  - run 1: 跟：带着，跟孟子搬家 suggests that the mother moves together with Mengzi as equals; 带着孟子搬家 shows that she takes her child with her. [vocab list]
  - run 2: 跟孟子搬家：带着孟子搬家，this phrase should show that the mother takes her child with her when moving. [vocab list]
  - run 3: 跟孟子搬家：带着孟子搬家，This action means that the mother takes her son with her when moving; the original wording incorrectly suggests that they move 
- mengmu_samples#18 scene 2 (3/3 runs) -- Run 1 addresses repeated noun references, while Runs 2 and 3 address the unnecessary 不是……而是…… contrast structure.
  - run 1: Coherence (Reference): 孟子的妈妈带孟子：她带他，both characters were named in the immediately previous sentence, so pronouns make the repeated reference
  - run 2: 不是搬到城市，而是搬到了：搬到了，this situation does not correct a previously stated or conventional assumption, so the contrast construction is unnecessary
  - run 3: 不是搬到城市，而是搬到了孟子老师的家：搬到了孟子老师的家，This paired structure is for correcting or refuting an established, usually expected claim. No earlier claim sa
- mengmu_samples#18 scene 3 (2/3 runs) -- Run 3 flags no error, while Runs 1 and 2 both address the repeated reference to 孟子/孟子的妈妈 rather than the teacher-corrected temporal expression.
  - run 1: Coherence (Reference): 孟子的妈妈：他的妈妈，After “孟子” has just been named in the time clause, use a pronoun for this close re-occurrence; it makes th
  - run 2: Coherence (Reference): 孟子学习的时候，孟子的妈妈不是待在家里就是编织衣服赚钱：孟子学习的时候，他妈妈不是待在家里就是编织衣服赚钱，The second mention is close to “孟子” and no other male character
  - run 3: —
- mengmu_samples#25 scene 1 (2/3 runs) -- Runs 1 and 2 identify and correctly fix the distance-expression error, but Run 3 flags nothing.
  - run 1: 从他的家到墓地很近：他的家离墓地很近，use 离 to express that one place is close to another; 从 marks a starting point for movement, not distance. [vocab list]
  - run 2: 从他的家到墓地很近：他的家离墓地很近，Use 离 to express that one place is close to another; 从 marks a starting point for movement rather than a distance relatio
  - run 3: —
- mengmu_samples#25 scene 1 (2/3 runs) -- The runs do not target the same issue, and Run 2 provides no correction while Runs 1 and 3 make different rewrites.
  - run 1: 每天老是从早到晚去墓地跟朋友们玩玩儿：每天从早到晚都在墓地跟朋友们玩儿，老是 describes repeated habitual actions, while 从早到晚 describes a continuous duration; the revised wording 
  - run 2: —
  - run 3: 从早到晚去墓地跟朋友们玩玩儿：从早到晚都在墓地跟朋友们玩儿，A trip expressed by 去墓地 is a bounded action, so it does not naturally last from morning to evening; use 在墓地 fo
- mengmu_samples#25 scene 1 (2/3 runs) -- Runs 1 and 2 address the same first-mention introduction issue, but Run 3 provides no item or correction.
  - run 1: Coherence (Reference): 孟子小的时候：有一个小男孩叫孟子。他小的时候，at a character’s first mention, introduce the character with a full noun phrase; after that, u
  - run 2: Coherence (Reference): 孟子小的时候，他的爸爸很早就去世了：有一个小男孩叫孟子。孟子小的时候，他的爸爸很早就去世了，On a character’s first mention, introduce the character with a full nou
  - run 3: —
- mengmu_samples#25 scene 2 (3/3 runs) -- Runs 1 and 3 address the incomplete 害得 structure, while Run 2 addresses the missing subject of the embedded action.
  - run 1: 在墓地玩儿，害得：孟子在墓地玩儿会带来麻烦，The original use of 害得 is incomplete: this structure must be followed by the person affected and a harmful result. [te
  - run 2: 觉得在墓地玩儿：觉得孟子在墓地玩儿，The embedded action needs its own subject; without it, the sentence incorrectly suggests that the mother is playing at the
  - run 3: 在墓地玩儿，害得：孟子在墓地玩儿会带来不好的影响，The structure 害得 must be followed by the affected person and a harmful result; the original leaves both parts unfin
- mengmu_samples#25 scene 3 (3/3 runs) -- All runs target the same verb phrase, but adding 了 addresses an error not indicated by the teacher and is not required here.
  - run 1: 成为有名的人：成为了有名的人，The becoming is presented as a completed result, so add 了 after the verb. [rule: aspect_le_completed]
  - run 2: Coherence (Temporality): 成为有名的人：成为了有名的人，This is a completed achievement in the story, so the verb needs 了 to mark completion. [rule: aspect_
  - run 3: 成为：成为了，This describes a completed outcome in the narrative, so add 了 after the verb. [rule: aspect_le_completed]
- mengmu_samples#32 scene 1 (2/3 runs) -- Both flagged runs identify the same modifier error and correctly revise it to “这儿的教育不太好.”
  - run 1: —
  - run 2: 住在这儿教育不太好：这儿的教育不太好，Use a location phrase with “的” to show that the education belongs to or is available in that place. [rule: none]
  - run 3: 住在这儿教育不太好：这儿的教育不太好，Use a location-based noun phrase to say that the education in a place is not good; “住在这儿” cannot directly modify “教育” her
- mengmu_samples#32 scene 1 (1/3 runs)
  - run 1: —
  - run 2: Coherence (Conjunction): 因为她望子成龙，所以她会一直搬家才能找到质量好的教育：因为她望子成龙，所以她会一直搬家才能找到质量好的教育，Use “因为……所以……” to mark the cause-and-effect relationship betw
  - run 3: —
- mengmu_samples#32 scene 1 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: 这是不合适的地方让孩子玩：这不是一个适合孩子玩的地方，Use the structure “适合 + person + verb” to describe what a place is suitable for; “让孩子玩” cannot be attached after 
- mengmu_samples#32 scene 2 (3/3 runs) -- Run 1 corrects both 才 placement and completed-event 了, while Runs 2–3 only correct the 才/duration phrasing and leave the required 了 unaddressed.
  - run 1: Coherence (Temporality): 他们住才一月就又搬家。：他们才住了一个月，就又搬家了。Put 才 before the verb, and use 了 to show that the one-month stay and the later move were
  - run 2: 住才一月：才住一个月，In the pattern with a short duration followed by an early result, put 才 before the verb; use 一个月 for a duration of one month. [ru
  - run 3: 住才一月：才住一个月，In a pattern with a short duration followed by an early next action, place 才 before the verb; 一个月 is the usual duration phrase he
- mengmu_samples#32 scene 2 (1/3 runs)
  - run 1: Coherence (Conjunction): 他们不是朋友，而是不好的人。：他们不是好人，你不能老跟他们玩儿。Use 不是……而是…… when correcting a conventional or mistaken idea; here a direct warning
  - run 2: —
  - run 3: —
- mengmu_samples#32 scene 2 (1/3 runs)
  - run 1: —
  - run 2: Coherence (Reference): 妈妈：她，Use a pronoun for a close re-occurrence when the mother was mentioned in the earlier scene and no other female c
  - run 3: —
- mengmu_samples#32 scene 3 (1/3 runs)
  - run 1: 在他们第三个家：在他们的第三个家里，A pronoun used as a possessive modifier normally takes 的 here, and 里 clearly marks the home as the location. [rule: none]
  - run 2: —
  - run 3: —
- mengmu_samples#32 scene 3 (1/3 runs)
  - run 1: Coherence (Temporality): 又搬家：又搬家了，This move is completed before the following sentence introduces the third home, so the completed action ne
  - run 2: —
  - run 3: —
- mengmu_samples#32 scene 3 (3/3 runs) -- All runs flag the same alleged missing 了, but the teacher’s intended correction is to add 后来 rather than require 了.
  - run 1: Coherence (Temporality): 成为：成为了，Becoming a philosopher is presented as a completed result in the narrative, so use 了. [rule: aspect_le_compl
  - run 2: Coherence (Temporality): 成为有名的哲学家：成为了有名的哲学家，Use 了 because becoming a philosopher is presented as a completed outcome in the past. [rule: asp
  - run 3: Coherence (Temporality): 成为有名的哲学家：成为了有名的哲学家，The becoming is presented as a completed result in the past, so it needs 了. [rule: aspect_le_com
- mengmu_samples#32 scene 3 (2/3 runs) -- Run 3 flags nothing and therefore leaves the misplaced 难怪 construction uncorrected.
  - run 1: Coherence (Conjunction): ，他难怪：，所以他后来，Use 所以 to connect the mother’s requirement that her son study with the resulting achievement. 难怪 introd
  - run 2: 他难怪：难怪他，The conclusion marker should introduce the clause that follows it, so it comes before the subject. [teacher rule: nanguai_yuanlai]
  - run 3: —
- mengmu_samples#32 scene 3 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 妈妈让儿子从早到晚学习：她让他从早到晚学习，Both people were named in the immediately preceding sentence, so close re-occurrence normally u
- mengmu_samples#33 scene 1 (2/3 runs) -- Runs 1 and 2 address the modal-verb word order, but Run 2 also changes direct-speech punctuation and Run 3 provides no correction.
  - run 1: 很多墓地得我祭拜：我得去很多墓地祭拜，The modal verb requires the person who must act as its subject; the place phrase belongs with the action of going there. 
  - run 2: 他妈妈说，从早到晚，我一直祭拜，很多墓地得我祭拜。：他妈妈说：“从早到晚，我得去很多墓地祭拜。”，Direct speech needs a colon and quotation marks. Also, the person who has an obligation mus
  - run 3: —
- mengmu_samples#33 scene 1 (3/3 runs) -- Runs 1 and 3 address the missing character introduction, while Run 2 corrects the time-expression word order.
  - run 1: Coherence (Reference): 孟子和他妈妈住在中国：有一个小男孩叫孟子，他和妈妈住在中国，The first mention should introduce the character with both a name and a brief identity;
  - run 2: 一天，很久很久以前：很久很久以前的一天，The time phrase needs to modify “一天” with “的”; this order clearly means one day in the distant past. [rule: time_express
  - run 3: Coherence (Reference): 一天，很久很久以前，孟子和他妈妈住在中国。：很久很久以前的一天，有一个小男孩叫孟子，他和妈妈住在中国。，On first mention, introduce the character with both a name and a 
- mengmu_samples#33 scene 1 (1/3 runs)
  - run 1: —
  - run 2: Coherence (Reference): 孟子妈妈的工作：她的工作，For a close re-occurrence, use a pronoun when the referent is clear; “她” clearly refers to Mengzi’s moth
  - run 3: —
- mengmu_samples#33 scene 1 (2/3 runs) -- Run 1 flags nothing, while Runs 2 and 3 both address the unnecessary 因为 and recast the complaint as direct speech.
  - run 1: —
  - run 2: Coherence (Conjunction): 因为他说我们老是搬家，为什么？：说：“我们老是搬家，为什么？”，“因为” should introduce a cause, but this question expresses Mengzi’s complaint rathe
  - run 3: 孟子不高兴，因为他说我们老是搬家，为什么？：孟子不高兴，问：“我们为什么老是搬家？”，Use a quoted question after a speaking verb; the question word belongs inside the question rather
- mengmu_samples#33 scene 2 (2/3 runs) -- Run 1 flags nothing, while Runs 2 and 3 both make the same optional pronoun-style change rather than a teacher-corrected error.
  - run 1: —
  - run 2: Coherence (Reference): 每次搬家孟子也觉得：每次搬家，他也觉得，use a pronoun when the same character was named in the immediately previous sentence and no compe
  - run 3: Coherence (Reference): 每次搬家孟子也觉得：每次搬家他也觉得，Use a pronoun for a close re-occurrence when the preceding sentence has already named the same cha
- mengmu_samples#33 scene 2 (2/3 runs) -- Run 1 flags no error, while Runs 2 and 3 flag an unnecessary repeated name rather than either teacher-corrected error.
  - run 1: —
  - run 2: Coherence (Reference): 孟子想帮助妈妈祭拜：他想帮助妈妈祭拜，use a pronoun for the close re-occurrence of the same character. [rule: character_introduction_fir
  - run 3: Coherence (Reference): 孟子想帮助妈妈祭拜：他想帮助妈妈祭拜，Use a pronoun for a close re-occurrence of the same character; the preceding sentence already make
- mengmu_samples#33 scene 3 (3/3 runs) -- Runs 1 and 3 only remove a redundant repeated subject, while Run 2 also rewrites the contrast into a purpose-versus-reason structure.
  - run 1: Coherence (Reference): 而是他很喜欢画画：而是很喜欢画画，The subject has not changed within the paired clause, so Chinese normally uses the zero form instead
  - run 2: 不是想帮妈妈工作，而是他很喜欢画画：不是为了帮妈妈工作，而是因为喜欢画画，The two halves of this contrast should give parallel reasons for the action; use “不是为了……，而是因为……” here, 
  - run 3: Coherence (Reference): 而是他很喜欢画画：而是很喜欢画画，The contrasting clause still has the same subject, so zero form is more natural than another pronoun
- mengmu_samples#33 scene 3 (3/3 runs) -- Runs 1 and 2 address missing 了, while Run 3 changes the reference, and all retain the incorrect claim that Mencius was a painter.
  - run 1: Coherence (Temporality): 孟子成为很著名的古代画家：孟子成为了很著名的古代画家，This is a completed change of state in the narrative, so the verb takes 了. [rule: aspect
  - run 2: Coherence (Temporality): 成为很著名的古代画家：成为了很著名的古代画家，This is a completed change of state in the narrative, so use 了 after the verb. [rule: aspect
  - run 3: Coherence (Reference): 孟子成为了很著名的古代画家：他成为了很著名的古代画家，The character was named recently and no other person competes as the referent, so use a pr
- mengmu_samples#33 scene 3 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 他越来越喜欢祭拜：越来越喜欢祭拜，The subject is the same as in the preceding clause, so use zero form rather than repeating the prono
- mengmu_samples#33 scene 3 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 所以他祭拜：所以祭拜，This continues the same subject within the sentence, so the repeated pronoun should be omitted. [rule: non
- mengmu_samples#33 scene 3 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 很多中国人很喜欢孟子：很多中国人很喜欢他，The character remains the clear, recently mentioned referent, so a pronoun avoids unnecessarily 
- mengmu_samples#39 scene 1 (1/3 runs)
  - run 1: Coherence (Reference): 孟子很小的时候：有一个叫孟子的小男孩，他很小的时候，This is the character’s first mention, so introduce him with a full noun phrase before usin
  - run 2: —
  - run 3: —
- mengmu_samples#39 scene 1 (3/3 runs) -- All runs address the repeated reference to 孟子’s mother, but their rewrites retain the redundant subject instead of making the teacher’s intended deletion.
  - run 1: Coherence (Reference): 孟子和孟子妈妈搬家了：孟子和妈妈搬家了，Within the same clause, the second repeated name should be omitted because “妈妈” clearly refers to
  - run 2: Coherence (Reference): 孟子和孟子妈妈搬家了：孟子和他的妈妈搬家了，his mother was mentioned in the immediately preceding sentence, so a pronoun is more natural fo
  - run 3: Coherence (Reference): 孟子和孟子妈妈搬家了：孟子和妈妈搬家了，The mother was just mentioned, so use the close re-occurrence form instead of repeating Mengzi’s 
- mengmu_samples#39 scene 1 (1/3 runs)
  - run 1: —
  - run 2: 孟子妈妈：孟子的妈妈，when a proper name modifies a kinship noun, add 的 to form the attributive phrase. [rule: attributive_modifier_de]
  - run 3: —
- mengmu_samples#39 scene 2 (3/3 runs) -- All runs identify the incorrect placement of 对他 with 害得, but Run 3 produces an incomplete and ungrammatical correction.
  - run 1: 对他害得，他有很多问题：害得他有很多问题，害得 must be followed directly by the person affected and then the harmful result; 对他 cannot be placed before 害得. [teache
  - run 2: 看过很多政治文章对他害得，他有很多问题：看过很多政治文章害得他有很多问题，害得 must be followed by the person affected and then the harmful result; 对他 cannot fill that position. [
  - run 3: 看过很多政治文章对他害得：他看了很多政治文章，害得他，害得 cannot be used after 对. The structure is a cause followed by 害得 + person + harmful result. [teacher rule: haid
- mengmu_samples#39 scene 3 (3/3 runs) -- Runs 1 and 2 address repeated naming/pronoun use, while Run 3 addresses the missing aspect marker 了.
  - run 1: Coherence (Reference): 孟子长大，他开始能解决问题：他长大了，开始能解决问题，孟子 was named in the immediately previous sentence with no competing character, so use the 
  - run 2: Coherence (Reference): 孟子长大：他长大，The character was named in the immediately preceding context and no competing character is present, so a pro
  - run 3: 孟子长大：孟子长大了，Growing up is a completed change of state in this past narrative, so it takes 了. [rule: aspect_le_completed]
- mengmu_samples#39 scene 3 (3/3 runs) -- Runs 2 and 3 only add aspect marker 了, while Run 1 also changes repeated subject reference and omits the second pronoun.
  - run 1: Coherence (Reference): 后来孟子成为教授，他教学生很厉害：后来他成为了教授，教学生很厉害，after the same character has remained the topic, use a pronoun for close re-occurren
  - run 2: Coherence (Temporality): 后来孟子成为教授：后来孟子成为了教授，Use 了 to mark the completed event of becoming a professor. [rule: aspect_le_completed]
  - run 3: 成为教授：成为了教授，Becoming a professor is a completed change in the narrative, so the verb takes 了. [rule: aspect_le_completed]
- mengmu_samples#39 scene 3 (2/3 runs) -- Run 1 flags nothing, while Runs 2 and 3 both correct the advice construction to “不要……而要……”.
  - run 1: —
  - run 2: 不是学金融，而是学政治：不要学金融，而要学政治，After 建议, use a directive form to recommend avoiding one action and choosing another; 不是……而是…… is for correcting or 
  - run 3: 不是学金融，而是学政治：不要学金融，而要学政治，After 建议, use a negative recommendation with 不要 rather than 不是……而是……, which refutes one statement and replaces it wi
- mengmu_samples#39 scene 3 (2/3 runs) -- Runs 2 and 3 flag the same ambiguous pronoun, but Run 1 flags nothing, so not every run identifies or fixes the error.
  - run 1: —
  - run 2: Coherence (Reference): 你：学生，This pronoun has no established referent in the narrative; introduce the group clearly with a full noun on first
  - run 3: Coherence (Reference): 你：学生，The second-person pronoun has no identifiable addressee in this third-person story; introduce the people receivi
- mengmu_samples#39 scene 3 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 他：∅，After naming 孟子 in the same sentence, omit the repeated subject in the following clause: 孟子长大了，开始能解决问题. [rule: ch
- mengmu_samples#4 scene 1 (3/3 runs) -- Runs 1 and 3 correct the placement of 了 and 在 after 住, while Run 2 instead targets the location wording and does not address the same grammatical error.
  - run 1: 住了在靠墓地的家：住在墓地旁边的家里，了 cannot be placed between the verb and its location phrase; this is a continuing living situation, so use 住在 + place wit
  - run 2: 靠墓地的家：靠近墓地的家里，The verb phrase needs a clear location: this wording specifies that the home is near the cemetery and that they live inside it
  - run 3: 住了在靠墓地的家：住在靠墓地的家里，A continuing living state uses no 了, and 住 takes 在 before its location phrase. [rule: location_zai_place]
- mengmu_samples#4 scene 1 (3/3 runs) -- Runs 1 and 2 correct 别一个城市 to 另一个城市, while Run 3 corrects the separate error 搬了到 to 搬到了.
  - run 1: 别一个城市：另一个城市，别 cannot be used directly before 一个 to mean “another”; use 另一个 for one different city. [rule: none]
  - run 2: 别一个城市：另一个城市，This refers to one additional or different city; this use requires the word meaning “another,” rather than the form used to dist
  - run 3: 搬了到：搬到了，Put 了 after the resultative/directional part of the verb phrase, not between 搬 and 到. [teacher rule: le_placement]
- mengmu_samples#4 scene 1 (2/3 runs) -- Runs 1 and 2 identify the same missing first-mention introduction, but Run 3 flags no error.
  - run 1: Coherence (Reference): 孟子和孟母：有一个小男孩叫孟子，他和孟母，孟子 is appearing for the first time, so introduce him as a child with his name before using the f
  - run 2: Coherence (Reference): 孟子和孟母：一个叫孟子的小男孩和他的妈妈，At first mention, introduce the child with a name and identity so the reader does not need prior
  - run 3: —
- mengmu_samples#4 scene 1 (2/3 runs) -- Run 2 flags no error, while Runs 1 and 3 both address the unclear reference in “那个城市” with equivalent fixes.
  - run 1: Coherence (Reference): 在那个城市：在一个城市里，那个 assumes that the city has already been identified, but this is its first mention; introduce it with a
  - run 2: —
  - run 3: Coherence (Reference): 在那个城市：在他们住的城市，The city has not previously been introduced, so 那个 does not have a clear antecedent; use a full noun ph
- mengmu_samples#4 scene 1 (2/3 runs) -- Run 2 flags nothing, while Runs 1 and 3 both address the vague reference “孩子”.
  - run 1: Coherence (Reference): 孩子：他，孟子 has just been referred to as 孩子, so a pronoun is more natural for this close re-occurrence. [rule: ambiguous_
  - run 2: —
  - run 3: Coherence (Reference): 孩子才五岁：他才五岁，孟子 was named in the immediately preceding sentence and no other child competes as the referent, so a prono
- mengmu_samples#4 scene 2 (3/3 runs) -- All runs target the repeated-action construction, but their future-plan rewrites retain 要 and conflict with the teacher’s completed-action correction 又搬了一次家。
  - run 1: 要又一个次搬：要再搬一次，A planned repeat uses the pattern modal verb + 再 + verb + number + measure word; 又 is for a repeat that has already happened, a
  - run 2: 要又一个次搬了家：要再搬一次家，With a modal verb for a future repeated action, use the pattern modal verb + 再 + verb + number + measure word + object; comp
  - run 3: 又一个次：再……一次，For a move that has not happened yet, use 再; after a modal verb, place 再 before the verb and place 一次 after it. [teacher rule: za
- mengmu_samples#4 scene 2 (3/3 runs) -- Run 1 rewrites the full parallel structure, while Runs 2 and 3 only change 人 to 人们 and leave the problematic 都叫 construction unfixed.
  - run 1: 不是人吵架，就是都叫：不是有人吵架，就是有人大叫，The two alternatives in this pattern need parallel clauses; 都 also needs a clear plural group to quantify, while 有人
  - run 2: 人：人们，This refers to the concrete group of people making noise in the city, so use the plural noun rather than the generic noun. [teacher rul
  - run 3: 人：人们，This refers to a concrete group making noise in the city, so use the plural noun rather than the generic noun. [teacher rule: ren_renme
- mengmu_samples#4 scene 3 (3/3 runs) -- All runs target the malformed location phrase, but Run 3 deletes the location instead of correcting it with 在 as in the teacher’s fix.
  - run 1: 孟子学习馆学了十五年：孟子在学习馆学习了十五年，A location noun needs 在 before it, and the action verb 学习 should follow the location phrase. [rule: none]
  - run 2: 孟子学习馆学了十五年：孟子在学习馆学习了十五年，A place where an action happens needs 在 before it, and 学习 is the action being described. [rule: none]
  - run 3: 学习馆学了十五年：学习了十五年，学习 is the verb here and can take the duration directly; 馆 is a noun and cannot be placed between the verb and its duration w
- mengmu_samples#4 scene 3 (3/3 runs) -- Runs 1 and 3 add 了 after 成为, while Run 2 deletes the repeated pronoun 他, so they address different errors.
  - run 1: Coherence (Temporality): 成为很有名的哲人：成为了很有名的哲人，This is a completed change of identity in the narrative, so use 了 after 成为. [rule: aspect_le_com
  - run 2: Coherence (Reference): 他成为很有名的哲人：成为很有名的哲人，After the same person has already been named in the time clause, use zero form rather than repeati
  - run 3: 成为：成为了，This is a completed change of state in the narrative, so 成为 takes 了. [rule: aspect_le_completed]
- mengmu_samples#4 scene 3 (2/3 runs) -- Both flagged runs identify the same unnatural time expression and correctly replace it with 长大以后, matching the teacher's correction.
  - run 1: —
  - run 2: 他是大人的时候：他长大以后，Use 长大以后 to introduce the later stage after someone has grown up. [rule: time_expression]
  - run 3: 他是大人的时候：他长大以后，Use 长大以后 to show that becoming an adult happened before the later event of becoming a philosopher. [rule: time_expression]
- mengmu_samples#4 scene 3 (2/3 runs) -- Run 1 flags nothing and therefore leaves the repeated possessive error uncorrected, unlike Runs 2 and 3.
  - run 1: —
  - run 2: Coherence (Reference): 他的学习和他的旅行经验：自己的学习和旅行经验，Use 自己的 to show clearly that the learning and travel experience belong to Mengzi, the person b
  - run 3: Coherence (Reference): 他的学习和他的旅行经验：他的学习和旅行经验，When the same possessor applies to two nouns in one phrase, use zero form for the second refere
- mengmu_samples#45 scene 1 (2/3 runs) -- Both flagged runs identify the same delayed character introduction and correctly combine the name with the initial noun phrase; the unflagged run does not conflict.
  - run 1: Coherence (Reference): 一个男孩子跟他的妈妈住在中国。他叫孟子：有一个叫孟子的男孩子和他的妈妈住在中国，at first mention, introduce the character with both the name and a full noun 
  - run 2: —
  - run 3: Coherence (Reference): 一个男孩子跟他的妈妈住在中国。他叫孟子。：一个叫孟子的男孩子跟他的妈妈住在中国。，Introduce the character by name when he first appears, rather than naming hi
- mengmu_samples#45 scene 1 (1/3 runs)
  - run 1: Coherence (Reference): 孟子不是祭拜，就是跟朋友聊天：他不是祭拜，就是跟朋友聊天，孟子 was named in the immediately preceding sentence and no other male character competes 
  - run 2: —
  - run 3: —
- mengmu_samples#45 scene 2 (1/3 runs)
  - run 1: Coherence (Conjunction): 他们：所以他们，The move happens because the mother wants better education for Meng子, so add 所以 to show the cause-and-effec
  - run 2: —
  - run 3: —
- mengmu_samples#45 scene 2 (2/3 runs) -- Run 1 flags nothing, while Runs 2–3 change aspect rather than the teacher’s issue of removing 他们 and expressing the causal relationship.
  - run 1: —
  - run 2: Coherence (Temporality): 他们从早到晚走路：他们从早到晚走了一天的路，This is one completed journey in the narrative, so the action needs 了; adding 一天的路 also makes
  - run 3: Coherence (Temporality): 他们从早到晚走路：他们从早到晚走了一天的路，This is a finished journey lasting from morning to evening, so the completed action needs 了. 
- mengmu_samples#45 scene 3 (3/3 runs) -- Runs 1 and 2 correct the 难怪／原来 construction, while Run 3 changes the possessive reference instead.
  - run 1: 他难怪抱怨，他想他的朋友：难怪他抱怨，原来他想他的朋友，The subject follows 难怪, and the explanation for the surprising result is introduced with 原来. [teacher rule: nang
  - run 2: Coherence (Conjunction): 他难怪抱怨，他想他的朋友：难怪他抱怨，原来他想朋友，Use 难怪……，原来…… to introduce an understandable result and then reveal its reason. [teacher 
  - run 3: Coherence (Reference): 他的朋友：自己的朋友，Because the subject is thinking about his own friends, 自己的 makes the possessor clear. [teacher rule: ziji_
- mengmu_samples#45 scene 3 (3/3 runs) -- All runs address the missing 给 for 孟子, but Run 2 additionally changes aspect and Run 3 removes 找到, so they do not make the same correction.
  - run 1: 孟子：给孟子，Use 给 before the person who receives the result of finding a teacher. [rule: none]
  - run 2: Coherence (Temporality): 找到孟子一个老师：给孟子找到了一个老师，孟子 is the beneficiary and needs 给; the finding has been completed, so add 了 after the resultati
  - run 3: 找到孟子一个老师：给孟子找一个老师，Use 给 to introduce the person who benefits from the action; the teacher is the object of 找. [rule: none]
- mengmu_samples#45 scene 3 (2/3 runs) -- Run 2 flags nothing, while Runs 1 and 3 identify the possessive wording 他的城市 and correct it to 自己的城市.
  - run 1: Coherence (Reference): 他的城市：自己的城市，Use 自己的 when the city belongs to the same person as the subject, making the possessor clear. [teacher rule
  - run 2: —
  - run 3: Coherence (Reference): 他的城市：自己的城市，Because the subject does not want to leave his own city, 自己的 clearly links the city to him. [teacher rule:
- mengmu_samples#47 scene 1 (1/3 runs)
  - run 1: 对童年很重要：对孩子的成长很重要，童年 is a time period, while the sentence means that the living place affects the child’s development. [rule: none]
  - run 2: —
  - run 3: —
- mengmu_samples#47 scene 2 (3/3 runs) -- judge prompt refused by the content filter
  - run 1: 又便宜又好质量的东西：又便宜、质量又好的东西，质量好 is the correct predicate for “good quality”; 好质量 cannot directly modify a noun in this structure. [rule: none]
  - run 2: 又便宜又好质量的东西：又便宜又质量好的东西，The phrase for “good quality” is 质量好; the full adjective phrase can then modify 东西. [rule: none]
  - run 3: 又便宜又好质量的东西：又便宜、质量又好的东西，质量 is a noun, so it needs the adjective 好 to describe it; the two coordinated descriptions are “cheap” and “of good q
- mengmu_samples#47 scene 2 (1/3 runs)
  - run 1: Coherence (Temporality): 然后教他：然后教了他，In a completed series of actions, only the final verb takes 了; here 教 is the final action after 让. [rule
  - run 2: —
  - run 3: —
- shennong_samples#12 scene 1 (2/3 runs) -- Run 1 flags nothing, while Runs 2 and 3 address the redundant/misused 也 in the second embedded question.
  - run 1: —
  - run 2: 也什么植物不能吃：也不知道什么植物不能吃，Also must modify a verb phrase, so repeat 不知道 before the second embedded question. [teacher rule: ye_vp]
  - run 3: Coherence (Conjunction): 也什么植物不能吃：什么植物不能吃，Also cannot directly be followed by a noun phrase or clause; here the two embedded questions can s
- shennong_samples#12 scene 2 (3/3 runs) -- Runs 1 and 2 address “写他的主意,” while Run 3 addresses the separate phrase “遇到了一个黄色的花.”
  - run 1: 写他的主意：写下了自己的想法，写下 means to record an idea in writing; 写 by itself is not natural for recording a thought in this context. [rule: none]
  - run 2: 写他的主意：记下自己的主意，“记下” means to record an idea so it is kept; “自己的” clearly shows that the ideas belong to the subject. [vocab list]
  - run 3: 遇到了一个黄色的花：看到了一朵黄色的花，Use the matching measure word “朵” for a flower. “看到” is also more suitable for noticing a flower than “遇到.” [rule: none]
- shennong_samples#12 scene 2 (1/3 runs)
  - run 1: Coherence (Temporality): 一吃就觉得不舒服：一吃这种花，就觉得不舒服了，The final 了 marks the change into an uncomfortable state; it does not attach to the mental-s
  - run 2: —
  - run 3: —
- shennong_samples#12 scene 3 (2/3 runs) -- Run 1 flags nothing, while Runs 2 and 3 address the 能不能吃 phrasing and give an acceptable parallel-clause correction.
  - run 1: —
  - run 2: 哪一个植物能不能吃：哪一种植物能吃，哪一种不能吃，哪一种 already asks which type of plant, so it should not be combined with the yes-or-no form 能不能. Use parallel clause
  - run 3: 哪一个植物能不能吃：哪一种植物能吃，哪一种不能吃，`哪一个` asks which item, while `能不能` forms an A-not-A question. Use parallel clauses to state which kinds are edible 
- shennong_samples#18 scene 1 (3/3 runs) -- All runs flag “住在古代,” but Run 3 changes the meaning by adding “住在一起,” so its correction is not an equivalent fix.
  - run 1: 住在古代：生活在古代，古代 is a historical time period rather than a physical place; use a verb such as 生活 to describe living in that period. [rule: time
  - run 2: 住在古代：生活在古代，古代 is a historical time period rather than a physical place of residence; use 生活在古代 to place the characters in that era. [rule: t
  - run 3: 住在古代：在古代住在一起，An era is a time expression, so it should be introduced with 在古代 rather than used as the location after 住在. [rule: time_express
- shennong_samples#18 scene 2 (3/3 runs) -- All runs flag “接近知道,” but Run 3 changes the intended meaning to “更接近答案” rather than expressing “想知道夹竹桃有没有毒.”
  - run 1: 接近知道：想知道，接近 means “approach” and cannot directly modify 知道 in this phrase; 想知道 expresses the intended wish to learn something. [rule: none]
  - run 2: 接近知道了：想知道答案，`接近` cannot take the verb `知道` as its object. To express wanting knowledge, use `想知道`; mental-state verbs such as `想` take no `了
  - run 3: “这就要看你想要安全还是接近知道了。“：“这就要看你是想要安全，还是想更接近答案了。”，The phrase “接近知道” is not grammatical because “接近” needs a noun such as “答案,” not the verb “知道.” 
- shennong_samples#18 scene 2 (1/3 runs)
  - run 1: 太麻烦了。：太麻烦了。”，Direct speech needs a closing quotation mark after the final punctuation. [rule: none]
  - run 2: —
  - run 3: —
- shennong_samples#18 scene 2 (2/3 runs) -- Run 1 flags nothing, while Runs 2 and 3 both correct the missing closing quotation mark.
  - run 1: —
  - run 2: 哥哥说：“太麻烦了。：哥哥说：“太麻烦了。”，Direct speech needs the closing quotation mark after the sentence-final punctuation. [rule: none]
  - run 3: 哥哥说：“太麻烦了。：哥哥说：“太麻烦了。”，Direct speech needs a closing quotation mark after the sentence-final punctuation. [rule: none]
- shennong_samples#18 scene 3 (2/3 runs) -- Runs 1 and 2 identify and correctly fix the same error, but Run 3 flags nothing and therefore does not provide the correction.
  - run 1: 夹竹桃是毒的：夹竹桃是有毒的，毒 is a noun here; use 有毒 to describe a plant’s poisonous property. [rule: word_class_misuse]
  - run 2: 夹竹桃是毒的：夹竹桃是有毒的，The word after the linking verb needs an adjectival description; 有毒的 describes a poisonous plant, while 毒 alone is a noun. [r
  - run 3: —
- shennong_samples#18 scene 3 (2/3 runs) -- Runs 1 and 3 flag the same phrase, but Run 2 flags nothing, so not every run identifies and fixes the same error.
  - run 1: 开始痊愈了：开始好起来了，痊愈 means recovering completely, so it cannot naturally follow 开始; 好起来 expresses that the recovery has begun. [rule: none]
  - run 2: —
  - run 3: 开始痊愈了：开始好转了，痊愈 describes a full recovery, so it does not fit well with 开始; 好转 describes the condition beginning to improve. [rule: none]
- shennong_samples#18 scene 3 (1/3 runs)
  - run 1: Coherence (Reference): 神农说：他说，after 神农 was named in the immediately preceding sentence and no new speaker intervened, use a pronoun for clos
  - run 2: —
  - run 3: —
- shennong_samples#18 scene 3 (2/3 runs) -- The runs address different issues (conditional phrasing versus a missing closing quotation mark), and one run flags nothing.
  - run 1: Coherence (Conjunction): 灵芝我们可以吃，特别是如果我们已经吃了夹竹桃：灵芝可以吃；如果我们已经吃了夹竹桃，就更应该吃灵芝，特别是 introduces a typical example, not a conditional situation; use
  - run 2: 夹竹桃。“：夹竹桃。”，The direct speech that begins earlier needs a closing quotation mark at its end. [rule: none]
  - run 3: —
- shennong_samples#19 scene 1 (2/3 runs) -- Run 2 flags no error, while Runs 1 and 3 correctly identify and fix 找 to 找到了.
  - run 1: 他找很多植物：他找到了很多植物，找 means “to look for,” while 找到 means “to find”; the completed discovery in this narrative needs 找到了. [vocab list]
  - run 2: —
  - run 3: 他找很多植物：他找到了很多植物，找 means “to look for,” while 找到 means “to find”; 到 shows that the search reached a result, and 了 marks the completed action.
- shennong_samples#19 scene 1 (2/3 runs) -- Run 2 flags nothing, while Runs 1 and 3 identify the same character-introduction coherence issue rather than the teacher-corrected 找/找到 error.
  - run 1: Coherence (Reference): 一个男人觉得植物很有意思。他叫神农：有一个叫神农的男人觉得植物很有意思，Introduce a character with the name and identity together at the first mention, r
  - run 2: —
  - run 3: Coherence (Reference): 一个男人觉得植物很有意思。他叫神农：一个叫神农的男人觉得植物很有意思，Introduce a character by name and description at the first mention, rather than na
- shennong_samples#19 scene 2 (3/3 runs) -- Runs 1 and 2 address only the missing 是/座 in the first clause, while Run 3 also changes the separate 「这也找植物」 error.
  - run 1: 凉山很大的山：凉山是一座很大的山，A noun description needs the linking verb and an appropriate measure word before the noun phrase. [rule: none]
  - run 2: 凉山很大的山：凉山是一座很大的山，A named mountain needs a predicate, and 座 is the appropriate measure word for a mountain. [rule: none]
  - run 3: 凉山很大的山，这也找植物：凉山是一座很大的山，他在这儿找植物，Use 是 and the measure word 座 to describe what 凉山 is; 这 cannot be the subject that performs 找, so use the esta
- shennong_samples#19 scene 3 (3/3 runs) -- All runs target the malformed noun chain, but their rewrites omit the intended antidote relationship and Run 3 is not a complete acceptable correction.
  - run 1: 灵芝药的夹竹桃他吃完了：他吃了灵芝这种药，The original modifier chain does not show a grammatical relationship between 灵芝 and 夹竹桃. Use 灵芝这种药 to identify what he 
  - run 2: 正好在这儿，灵芝药的夹竹桃他吃完了：正好在这儿有灵芝这种药，神农吃完了灵芝，药的 cannot connect 灵芝 and 夹竹桃 into one noun phrase. Use 有 to introduce the plant at this place, and use
  - run 3: 灵芝药的夹竹桃：灵芝是药，夹竹桃，The original incorrectly joins three nouns with 的. 灵芝 needs 是药 to state that it is medicine, while 夹竹桃 begins a separate ph
- shennong_samples#19 scene 3 (3/3 runs) -- All runs target the malformed phrase about writing plants, but they change the intended meaning to recording plants rather than writing an article about plants as corrected by the teacher.
  - run 1: 写一个课文的植物：记下这些植物，When recording information about plants, use 记下 or 写下 rather than 写 directly with the plants as its object. [vocab list]
  - run 2: 写一个课文的植物：记下了这两种植物，Use 记下 to mean recording plants or discoveries; 写 cannot directly take 植物 in this meaning, and 一个课文的植物 does not form a mea
  - run 3: 写一个课文的植物：记下这两种植物，写 directly with plants does not express recording information about them; 记下 means to record them, and the revised phrase c
- shennong_samples#26 scene 1 (2/3 runs) -- Runs 1 and 2 correct “老男人” to “老人,” but Run 3 flags no error there.
  - run 1: 老男人：老人，this is the usual respectful and natural noun for an elderly male character; the original word can sound informal or negative in a st
  - run 2: 老男人：老人，The original term can sound impolite or carry an unwanted negative tone; this word is the neutral term for an elderly man. [rule: non
  - run 3: —
- shennong_samples#26 scene 1 (3/3 runs) -- Runs 1–2 address the unnecessary 别的, while Run 3 addresses the 人/人们 construction and retains the incorrect 别.
  - run 1: 别的：删除，this word distinguishes other people or things from a specifically mentioned one, but no such comparison has been established here. [t
  - run 2: 别的小镇人：小镇上的人，The word distinguishes other ones from a stated one, but no contrasting town has been established; this location phrase clearly 
  - run 3: 别的小镇人：别的小镇的人们，A concrete group of people should use 人们, and 的 links the town phrase to the people. [teacher rule: ren_renmen]
- shennong_samples#26 scene 1 (3/3 runs) -- Run 1 changes the repeated subject to a pronoun, while Runs 2 and 3 address the verb and/or measure word for plants.
  - run 1: Coherence (Reference): 神农试一试：他试一试，use a pronoun because the same character was mentioned in the preceding sentence and there is no competing
  - run 2: 试一试每个植物：尝一尝每种植物，The verb precisely describes tasting plants to test them, and the measure word is used for kinds of plants rather than indiv
  - run 3: 每个植物：每种植物，种 is the appropriate measure word for types of plants; 个 is too generic here. [rule: none]
- shennong_samples#26 scene 1 (2/3 runs) -- Run 1 flags nothing and leaves “下一天” uncorrected, while Runs 2 and 3 correctly change it to “第二天.”
  - run 1: —
  - run 2: 下一天：第二天，Use this time expression to mean “the next day” in a narrative. [rule: time_expression]
  - run 3: 下一天：第二天，Use 第二天 to mean the day following the previously described day in a narrative. [rule: time_expression]
- shennong_samples#26 scene 2 (3/3 runs) -- All runs identify the misuse of 吃得 for describing the leaves’ qualities, but Run 1’s 觉得又新鲜又甜 is not the teacher’s accepted 吃起来 construction.
  - run 1: 吃得又新鲜又甜：觉得又新鲜又甜，the structure with 得 describes the degree or result of eating, but “fresh” and “sweet” describe the leaves; use a perception
  - run 2: 吃得又新鲜又甜：吃起来又新鲜又甜，Use 起来 when describing how food tastes; 新鲜 and 甜 describe the leaves’ taste, not the manner of eating. [rule: none]
  - run 3: 吃得又新鲜又甜：吃起来又新鲜又甜，吃起来 introduces an evaluation of how food tastes; 吃得 cannot be used to describe the leaves’ flavour in this structure. [rule
- shennong_samples#26 scene 2 (3/3 runs) -- Runs 1–2 address the unnatural “知道他发现” meaning, while Run 3 instead treats “发现” as a completed-action aspect error.
  - run 1: 知道他发现新的茶叶：发现这是一种茶，this needs one verb for the realization and a complete clause stating what he discovered; “知道他发现” does not naturally expre
  - run 2: 知道他发现：发现，知道 means “know a fact,” while 发现 means “make a discovery”; the intended meaning is that he discovered tea. [rule: none]
  - run 3: 发现新的茶叶：发现了新的茶叶，Finding the tea leaves is a completed action, so add 了 after the verb. [rule: aspect_le_completed]
- shennong_samples#26 scene 3 (1/3 runs)
  - run 1: 神农的麻烦：神农遇到了麻烦，Use the verb-object phrase to show that someone experiences trouble; “神农的麻烦” treats the trouble only as a possessed noun and i
  - run 2: —
  - run 3: —
- shennong_samples#26 scene 3 (3/3 runs) -- Run 2 additionally changes the aspect to 分享了, while Runs 1 and 3 address only 别的人/别人.
  - run 1: 跟别的人：跟别人，“别人” refers generally to other people; “别的人” is used when distinguishing them from a specifically mentioned person or group. [teach
  - run 2: 跟别的人分享他的发现：跟别人分享了他的发现，The noun 别人 is the usual form for “other people” here, and the final action in this completed sequence needs 了. [rule:
  - run 3: 跟别的人分享他的发现：跟别人分享他的发现，别的人 is used to distinguish people from someone already mentioned; here there is no such contrast, so 别人 is the natural 
- shennong_samples#26 scene 3 (2/3 runs) -- Runs 1 and 2 correct the missing “是,” but Run 3 flags no error at this location.
  - run 1: 你认为神农的故事真的吗？：你认为神农的故事是真的吗？，A noun phrase needs “是” before the adjective “真的” when asking whether the story is true. [rule: none]
  - run 2: 你认为神农的故事真的吗？：你认为神农的故事是真的吗？，A noun phrase followed by 真的 requires 是 to form a yes-or-no question about whether it is true. [rule: none]
  - run 3: —
- shennong_samples#26 scene 3 (3/3 runs) -- All runs address the final 看…了 structure, but Run 3 leaves out 相不相信 and therefore does not make the intended conditional question as clear as the teacher’s correction.
  - run 1: Coherence (Temporality): 这就要看你相信中药对身体有好处。：这就要看你相不相信中药对身体有好处了。，This fixed structure ends with “了”; “相不相信” also makes clear that the answer de
  - run 2: Coherence (Temporality): 这就要看你相信中药对身体有好处。：这就要看你相不相信中药对身体有好处了。，This fixed response structure ends with 了, and 看 naturally introduces whether 
  - run 3: 这就要看你相信中药对身体有好处：这就要看你相信中药对身体有好处了，This fixed structure ends with 了; this 了 belongs to the structure rather than marking a completed action. [
- shennong_samples#33 scene 1 (3/3 runs) -- Runs 1–2 treat 时候 as redundant, while Run 3 treats 的 as missing, though both corrections are acceptable rewrites of the phrase.
  - run 1: 古代时候：在古代，The original repeats the idea of time because 古代 already names a historical period. [teacher rule: gudai_de_shihou_why]
  - run 2: 古代时候：在古代，古代 already identifies a time period, so adding 时候 is redundant. [teacher rule: gudai_de_shihou_why]
  - run 3: 古代时候：古代的时候，A multi-syllable time noun needs 的 before 时候; only fixed expressions such as 古时候 omit it. [teacher rule: de_shihou]
- shennong_samples#33 scene 1 (2/3 runs) -- Runs 1 and 2 flag the same conjunction issue, but Run 3 flags nothing at this location.
  - run 1: Coherence (Conjunction): 但是不知道为什么：他们也不知道为什么，The earlier event and not knowing the reason do not form a contrast; 也 adds another related prob
  - run 2: Coherence (Conjunction): 但是不知道为什么，没有办法：不知道为什么，也没有办法，但是 marks contrast, but these two ideas are additional related problems rather than contr
  - run 3: —
- shennong_samples#33 scene 1 (1/3 runs)
  - run 1: Coherence (Conjunction): 所以有一天：于是，有一天，Use 于是 to show that Shennong’s action follows from the people’s problem; it links the cause to the res
  - run 2: —
  - run 3: —
- shennong_samples#33 scene 1 (2/3 runs) -- Run 1 flags nothing, while Runs 2–3 add 了 to 告诉, which does not address the teacher’s required 的 after 安全 and 危险.
  - run 1: —
  - run 2: Coherence (Temporality): 告诉：告诉了，telling people is presented as the completed final action in this series, so it takes 了. [rule: aspect_le_co
  - run 3: Coherence (Temporality): 告诉人们：告诉了人们，This is the final completed action in the sequence, so it takes 了; earlier actions in a series can remai
- shennong_samples#33 scene 1 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 他们能吃什么植物：能吃什么植物，Use zero form when the embedded clause has the same referent as the main-clause subject; repeating th
- shennong_samples#33 scene 2 (3/3 runs) -- Runs 1–2 also address the experiencer of 感觉, while Run 3 only changes 清楚, and Run 1 changes the intended bodily meaning to 清醒.
  - run 1: 让肚子感觉又暖和又清楚：让人觉得又暖和又清醒，In this causative structure, the affected experiencer should be a person who can “feel”; a stomach can be warm but ca
  - run 2: 让肚子感觉又暖和又清楚：让人觉得肚子又暖和又舒服，A person, rather than the stomach itself, has the feeling; also, 清楚 describes clear understanding or perception, wh
  - run 3: 又暖和又清楚：又暖和又舒服，清楚 describes mental understanding or clear information, not a bodily sensation; 舒服 describes physical comfort. [rule: none]
- shennong_samples#33 scene 2 (2/3 runs) -- Run 2 correctly adds 了 to the pattern, while Run 3 changes the construction and does not provide the teacher's accepted fix.
  - run 1: —
  - run 2: 你吃哪种植物，这就要看你的口味。：你吃哪种植物？这就要看你的口味了。The fixed response pattern 这就要看……了 needs the final 了; the first part is the uncertain question being answe
  - run 3: 这就要看你的口味：要看你的口味，the pattern 这就要看……了 requires a question form after 看, but 你的口味 is a noun phrase rather than a question. [rule: zhe_jiu_yao_k
- shennong_samples#33 scene 2 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 朋友：一个朋友，this character appears for the first time, so use a full noun phrase to introduce the friend clearly. [rule: 
- shennong_samples#33 scene 3 (3/3 runs) -- All runs address the incompatible phrase “开始死,” but Run 2 merely adds 了 and still treats death as something that can begin.
  - run 1: 一吃就开始死：一吃就快要死了，死 describes an endpoint, so it does not normally follow 开始; 快要……了 expresses that the change of state is about to happen. [rul
  - run 2: 开始死：开始死了，The particle 了 marks the completed change of state: he began to die after eating the flower. [rule: aspect_le_completed]
  - run 3: 开始死：快要死了，Death is normally treated as an endpoint rather than an action that can simply begin; this revision expresses that he was close to 
- shennong_samples#33 scene 3 (3/3 runs) -- All runs identify the unclear reference in “这个口味,” but the proposed replacements retain an unrelated phrase rather than the teacher-approved deletion.
  - run 1: Coherence (Reference): 这个口味：一种花的味道，This is the first mention of the taste, so 这个 does not have a clear earlier noun to refer to; introduce i
  - run 2: Coherence (Reference): 这个口味：自己的口味，The demonstrative 这个 needs a clear previously named referent, but no particular taste has been identified;
  - run 3: Coherence (Reference): 这个口味：自己喜欢的口味，The reader does not know which specific flavour 这个 refers to; name the preference more clearly. [rule: a
- shennong_samples#33 scene 3 (1/3 runs)
  - run 1: Coherence (Conjunction): 但是：删除，But does not express contrast here; the time phrase already connects the action of becoming ill with telling 
  - run 2: —
  - run 3: —
- shennong_samples#33 scene 3 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Temporality): 发现：发现了，This is a completed discovery before the later event, so it needs 了. [rule: aspect_le_completed]
- shennong_samples#35 scene 1 (3/3 runs) -- Run 1 corrects the earlier missing 了 and medication-description issue, while Runs 2 and 3 correct the extra 的 in a different phrase.
  - run 1: 吃很多植物对药：吃了很多可以做药的植物，“了” marks the completed eating action, and “可以做药的植物” correctly describes plants that can be made into medicine. [rule: a
  - run 2: 他们的吃的植物：他们吃的植物，The first “的” incorrectly makes the pronoun possessive. In a relative clause, the pronoun should directly be the subject of t
  - run 3: 他们的吃的植物：他们吃的植物，The possessor is unnecessary because the embedded verb already identifies who eats the plants. [rule: redundancy_delete]
- shennong_samples#35 scene 1 (3/3 runs) -- Run 2 also addresses the measure word and modifier order, while Run 1's “找一个植物做药” does not fully make the plant itself the described medicine-capable plant as in the teacher's correction.
  - run 1: 找一个植物对药：找一个植物做药，“做药” means to use something in making medicine; “对药” does not express this meaning. [rule: none]
  - run 2: 一个植物对药，他们可以吃对药：一种可以做药、他们可以吃的植物，“种” is the suitable measure word for a type of plant. Both descriptions must come before the noun, and “对药” i
  - run 3: 一个植物对药：一种能做药的植物，`对药` cannot modify `植物`; `能做药的` correctly describes a plant that can be used to make medicine. [rule: none]
- shennong_samples#35 scene 1 (2/3 runs) -- The two runs target different redundancies (repeated subject 他 versus repeated object 花), and the third run flags nothing.
  - run 1: Coherence (Reference): 他找到了一把花，他想：他找到了一把花，想，After the subject has already been named in the same sentence, use zero form rather than repeati
  - run 2: Coherence (Reference): 一把花，他想把花：一把花，他想把它，When an object was named very recently and no other object competes with it, use a pronoun rather t
  - run 3: —
- shennong_samples#35 scene 2 (3/3 runs) -- All runs target the misuse of 如果 after 不知道, but Run 3's 对不对身体好 has incorrect word order and is not an acceptable correction.
  - run 1: 不知道如果这把花对他的身体好不好：不知道这把花对他的身体好不好，An embedded yes/no question after “不知道” uses an A-not-A form, not “如果,” which introduces a condition. [rule:
  - run 2: 如果这把花对你的身体好：这把花对你的身体好不好，After 不知道, an embedded yes/no question needs the A-not-A form instead of 如果 plus a statement. [rule: a_not_a_questio
  - run 3: 不知道如果这把花对你的身体好：不知道这把花对不对身体好，An embedded yes/no question after 不知道 needs an A-not-A form; 对不对身体好 asks whether the flower is beneficial to the
- shennong_samples#35 scene 2 (3/3 runs) -- All runs identify the same 吃不吃……或者…… construction, but their 是……还是…… rewrites change the intended meaning rather than the teacher’s 要不要吃 correction.
  - run 1: 他吃不吃灵芝或者夹竹桃：自己吃的是灵芝还是夹竹桃，The uncertainty is about which plant he ate, not whether he eats. Two alternative possibilities use “是……还是……”. [rul
  - run 2: 他吃不吃灵芝或者夹竹桃：他吃的是灵芝还是夹竹桃，When choosing between two possibilities after 不知道, use 是……还是…… rather than 吃不吃……或者…… . [rule: a_not_a_question]
  - run 3: 不知道他吃不吃灵芝或者夹竹桃：不知道吃的是灵芝还是夹竹桃，When choosing between two specific possibilities, use 是……还是……; 吃不吃 does not express the choice between these tw
- shennong_samples#35 scene 2 (2/3 runs) -- Run 1 flags nothing, while Runs 2 and 3 both alter the 一……就…… phrasing.
  - run 1: —
  - run 2: Coherence (Conjunction): 很快：就很快，The pattern 一……就…… needs 就 to connect the first action with its immediate result. [teacher rule: yi_jiu]
  - run 3: Coherence (Conjunction): 一吃花，很快就：一吃花，就很快，The pattern 一……就…… needs 就 to connect the immediate action of eating with the result of becoming il
- shennong_samples#35 scene 2 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 神农：他，The character was mentioned in the immediately previous sentence and no other character competes as the referent
- shennong_samples#35 scene 3 (3/3 runs) -- All runs identify the misuse of 别的人, but they replace it with 一个/有人 rather than the teacher’s intended 另外一个人.
  - run 1: 别的人给了神农一个灵芝：一个男人给了神农一个灵芝，别的人 distinguishes other people from a person already under discussion, but no such person has been introduced here.
  - run 2: 别的人给了神农一个灵芝：一个人给了神农一个灵芝，别的人 means people other than a previously identified person or group; no such contrast has been established here, so 
  - run 3: 别的人：有人，别的人 distinguishes other people from a previously specified person or group; here the giver has not been introduced, so an indefinite 
- shennong_samples#35 scene 3 (2/3 runs) -- Runs 1 and 2 flag the same redundant repetition, but Run 3 flags no error.
  - run 1: Coherence (Reference): 神农想跟很多人分享他的新药：他想跟很多人分享他的新药，after a close mention of the same person and with no competing male character, use a prono
  - run 2: Coherence (Reference): 神农想跟很多人分享他的新药：他想跟很多人分享他的新药，continue with a pronoun when the same character remains the clear subject in the next sent
  - run 3: —
- shennong_samples#35 scene 3 (2/3 runs) -- Run 1 flags nothing, and Runs 2–3 change 这个植物 to 它 rather than fixing the intended issue of saying 身体更好.
  - run 1: —
  - run 2: Coherence (Reference): 这个植物：它，灵芝 was named in the immediately preceding sentence, so use a pronoun for this close re-occurrence rather than 
  - run 3: Coherence (Reference): 这个植物：它，after 灵芝 was named in the immediately previous sentence, use a pronoun for this close re-occurrence. [rule: no
- shennong_samples#35 scene 3 (1/3 runs)
  - run 1: —
  - run 2: Coherence (Reference): 这些植物让神农很高兴：这些植物让他很高兴，神农 was mentioned recently and there is no competing male character, so a pronoun is more natural
  - run 3: —
- shennong_samples#35 scene 3 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Temporality): 吃灵芝以后：吃了灵芝以后，this eating action is completed before Shennong can walk again, so it needs 了. [rule: aspect_le_comple
- shennong_samples#4 scene 1 (2/3 runs) -- Runs 1 and 2 flag the same unnecessary “你的,” but Run 3 provides no correction for this error.
  - run 1: Coherence (Reference): 你的身体：身体，The reader-facing pronoun has no specific referent in this general statement; use a general noun phrase inste
  - run 2: Coherence (Reference): 对你的身体有好处：对身体有好处，The pronoun shifts to an unintroduced listener; use a general expression because the sentence is abou
  - run 3: —
- shennong_samples#4 scene 1 (2/3 runs) -- Runs 1 and 2 flag the same pronoun-reference error, but Run 3 provides no item for it.
  - run 1: Coherence (Reference): 对你有没有好处：对身体有没有好处，The pronoun does not refer to a particular person in the narration, so a general expression makes th
  - run 2: Coherence (Reference): 对你有没有好处：对身体有没有好处，The pronoun has no clear addressee in this narration; a general expression keeps the reference consi
  - run 3: —
- shennong_samples#4 scene 1 (3/3 runs) -- Runs 1–2 replace a repeated name with a pronoun, while Run 3 changes the aspect marker 了, so they target different issues.
  - run 1: Coherence (Reference): 有的时候，神农：有的时候，他，The name was mentioned recently and no other character is competing, so a pronoun is more natural for 
  - run 2: Coherence (Reference): 有的时候，神农：有的时候，他，Shennong was mentioned in the preceding sentence, so a pronoun is the natural close re-occurrence form
  - run 3: Coherence (Temporality): 有的时候，神农吃了很好吃的植物：有的时候，神农吃很好吃的植物，\(有的时候\) introduces a routine, so use the zero particle rather than completed-action
- shennong_samples#4 scene 1 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: 哪个植物好吃：哪些植物能吃，\(好吃\) means “tasty,” while \(能吃\) means “edible” or safe to eat; \(哪些\) fits an unknown group of plants. [rule: none]
- shennong_samples#4 scene 2 (1/3 runs)
  - run 1: 哪个植物：哪种植物，Use 种 when asking which type of plant in a general category. [rule: none]
  - run 2: —
  - run 3: —
- shennong_samples#4 scene 2 (2/3 runs) -- Run 2 flags nothing, while Runs 1 and 3 both change a phrase the teacher did not identify as erroneous.
  - run 1: 这就要看你的口味了：这就要看你喜欢什么口味了，The structure 这就要看……了 needs a question form after 看, such as a wh-question. [rule: zhe_jiu_yao_kan]
  - run 2: —
  - run 3: 这就要看你的口味了：这就要看你喜欢什么口味的食物了，The expression requires a question form after 看; a wh-question makes the condition for the answer explicit. [rule:
- shennong_samples#4 scene 2 (1/3 runs)
  - run 1: Coherence (Reference): 对你的身体有好处：对身体有好处，This is a general fact about plants, so the addressee pronoun is unnecessary and can make the benefit
  - run 2: —
  - run 3: —
- shennong_samples#4 scene 2 (1/3 runs)
  - run 1: Coherence (Reference): 对你的身体有坏处：对身体有坏处，This is also a general statement, so removing the pronoun keeps the reference broad and clear. [rule:
  - run 2: —
  - run 3: —
- shennong_samples#4 scene 3 (3/3 runs) -- All runs flag “脑,” but Run 1 changes the meaning to “身体” rather than making the teacher’s intended correction to “大脑.”
  - run 1: 我的脑：我的身体，The noun “脑” refers specifically to the brain. For general physical harm from a poisonous plant, “身体” fits the intended meaning. [r
  - run 2: 对我的脑有坏处：对我的大脑有害，“脑” alone does not fit naturally in this health expression. “大脑” names the organ clearly, and “有害” expresses harm to it. [ru
  - run 3: 对我的脑有坏处：对我的大脑有坏处，脑 normally appears in compounds; 大脑 is the natural noun when referring to the body part in this structure. [rule: none]
- shennong_samples#4 scene 3 (2/3 runs) -- Runs 1 and 2 address the same ambiguous reference, but Run 3 provides no item or correction.
  - run 1: Coherence (Reference): 那个植物：灵芝，Two plants have already appeared, so “那个植物” could refer to either the oleander or the lingzhi. Repeat the nam
  - run 2: Coherence (Reference): 那个植物：那株灵芝，There are two plants in the nearby context, so “那个植物” could refer either to the earlier flower or to the ne
  - run 3: —
- shennong_samples#4 scene 3 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: 这个灵芝：这株灵芝，use the measure word 株 when referring back to that individual plant. [rule: none]
- shennong_samples#42 scene 1 (1/3 runs)
  - run 1: 什么病人：病人，什么病人 asks which type of patient, but this sentence makes a general claim about patients who eat the plant. [rule: word_choice]
  - run 2: —
  - run 3: —
- shennong_samples#42 scene 1 (3/3 runs) -- Run 1 targets an ambiguous plant reference, while Runs 2 and 3 target repeated use of 神农, and their edits do not address the needed 走了三个月 correction.
  - run 1: Coherence (Reference): 有植物的地方：有这种植物的地方，Use 这种植物 to refer back clearly to the plant mentioned in the previous sentence. [rule: ambiguous_refe
  - run 2: Coherence (Reference): 神农三个月走去：他三个月走去，Use a pronoun because 神农 was named in the immediately preceding sentence and no other character compet
  - run 3: Coherence (Reference): 神农三个月走去：他三个月走去，The same character was just mentioned, so use a pronoun rather than repeat the name. [rule: none]
- shennong_samples#42 scene 1 (2/3 runs) -- Runs 1 and 3 make the same pronoun-deletion suggestion, but Run 2 flags nothing and therefore leaves that issue uncorrected.
  - run 1: Coherence (Reference): 他看到：看到，After 神农 has remained the subject throughout the same sentence, Chinese normally uses zero form rather than re
  - run 2: —
  - run 3: Coherence (Reference): 他看到：看到，Within the same sentence, the subject is already clear, so use zero form for the later action. [rule: redundan
- shennong_samples#42 scene 1 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: 一个远远的地方：一个很远的地方，远远的 is not the usual modifier in this noun phrase; 很远的 directly describes a faraway place. [rule: word_choice]
- shennong_samples#42 scene 1 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 他有一个问题，他不知道：他有一个问题，不知道，After the subject has appeared in the same sentence and no other person competes as the subjec
- shennong_samples#42 scene 1 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 神农听说：他听说，The character was named in the preceding sentence and no competing character has appeared, so a pronoun is m
- shennong_samples#42 scene 2 (2/3 runs) -- Run 1 addresses pronoun repetition, Run 2 corrects the illness expression, and Run 3 flags nothing.
  - run 1: Coherence (Reference): 神农快生病：他快生病，Use a pronoun for a close re-occurrence when the same character was named or clearly referred to in the im
  - run 2: 快生病：很快就生病了，In this completed past event, “很快” describes how rapidly the illness began, and “了” marks that becoming ill as completed. [rule: 
  - run 3: —
- shennong_samples#42 scene 2 (2/3 runs) -- Run 1 flags nothing, while Runs 2 and 3 both address the omitted 有 and 过 in “以前一个人告诉他.”
  - run 1: —
  - run 2: 以前一个人告诉他：以前有一个人告诉过他，“有” is needed to introduce the existence of this person, and “过” marks the earlier experience that he now remembers. [ru
  - run 3: 以前一个人告诉他：以前有一个人告诉过他，An indefinite person in this earlier event needs 有 to introduce them, and 过 marks the earlier completed experience of be
- shennong_samples#42 scene 2 (2/3 runs) -- Run 2 corrects the recovery expression “没有病” to “病好了,” while Run 3 only deletes the redundant pronoun, and Run 1 flags nothing.
  - run 1: —
  - run 2: Coherence (Temporality): 他没有病：他的病好了，This is a change from being ill to recovering, so “好了” marks the completed change of state. [rule: aspec
  - run 3: Coherence (Reference): 神农吃了以后，他没有病：神农吃了以后，没有病，When the same subject continues within one sentence, use zero form rather than repeating a pro
- shennong_samples#42 scene 2 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 他：神农，Two male characters are present in this sentence, so the pronoun can be unclear; repeat the name of the recipien
- shennong_samples#42 scene 3 (3/3 runs) -- Runs 1 and 3 address the missing completion marker 了, while Run 2 changes 别人 to 大家, so they target different issues.
  - run 1: Coherence (Temporality): 告诉别人：告诉了人们，The telling happens as a completed action after returning home, so add 了; 人们 refers to the concrete grou
  - run 2: 别人：大家，This scene does not set up a particular person from whom these people are being distinguished; use a word that clearly names the group
  - run 3: Coherence (Temporality): 一回家就告诉别人：一回家就告诉了别人，The telling is a completed action after returning home, so the final verb takes 了. [rule: aspect
- shennong_samples#49 scene 1 (3/3 runs) -- Runs 1–2 correct “吃毒” to “吃到有毒的植物,” while Run 3 only adds “就” for the conditional structure.
  - run 1: 还怕吃毒：害怕吃到有毒的植物，吃毒 is not natural for accidentally eating a poisonous plant; 吃到 expresses encountering and eating it. [vocab list]
  - run 2: 怕吃毒：怕吃到有毒的植物，吃 describes the action, while 吃到 shows that someone ends up consuming the plant; 有毒的植物 clearly names the danger. [rule: resulta
  - run 3: Coherence (Conjunction): 如果他们还怕吃毒，不会吃他喜欢的植物：如果他们还怕吃毒，就不会吃他喜欢的植物，an if-condition normally uses 就 to introduce its result. [rule: none]
- shennong_samples#49 scene 1 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: 他什么植物都觉得好吃：他觉得什么植物都好吃，觉得 should introduce the whole evaluative clause; the speaker’s judgment comes after 觉得. [rule: none]
- shennong_samples#49 scene 1 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Temporality): 吃植物以后：吃了植物以后，the eating is completed before the later result of getting an upset stomach, so use 了 for the complete
- shennong_samples#49 scene 2 (2/3 runs) -- Runs 1 and 2 address the inappropriate 了 in 一直都吃了, but Run 3 flags no error at this location.
  - run 1: 一直都吃了：一直都在吃各种植物，了 marks a completed action, but 一直 describes an ongoing action; use 在 for the progressive action instead. [rule: aspect_le_c
  - run 2: Coherence (Temporality): 他一直都吃了：他一直都吃，The action is ongoing or habitual because of 一直, so it takes the zero particle rather than completed-a
  - run 3: —
- shennong_samples#49 scene 2 (2/3 runs) -- Run 1 changes “毒” to “有毒的植物,” while Run 3 targets the repeated subject “他,” and Run 2 flags nothing.
  - run 1: 毒：有毒的植物，毒 is a noun meaning poison; this sentence needs a noun phrase naming the plants that are poisonous. [rule: none]
  - run 2: —
  - run 3: Coherence (Reference): 他连毒都能吃：连毒都能吃，after 他 has already been used as the subject earlier in the same sentence, use zero form instead of repe
- shennong_samples#49 scene 2 (2/3 runs) -- Runs 1 and 2 address the inappropriate 了, but Run 3 flags nothing and their fixes omit the needed experiential 过.
  - run 1: 还没吃了：还没吃，没 already negates the completed action, so 了 is not used after the verb here. [rule: aspect_le_completed]
  - run 2: Coherence (Temporality): 还没吃了：还没吃，A negated completed action with 没 does not take 了. [rule: aspect_le_completed]
  - run 3: —
- shennong_samples#49 scene 2 (2/3 runs) -- Run 1 flags nothing, while Runs 2 and 3 identify and correctly fix “很多样子的植物” as “很多种植物.”
  - run 1: —
  - run 2: 很多样子的植物：很多种植物，Use 种 to count different varieties of plants; 样子 refers to an object’s appearance and does not naturally classify plants here.
  - run 3: 很多样子的植物：很多种植物，样子 describes an object’s appearance, while 种 is the measure word used for different types of plants. [rule: none]
- shennong_samples#49 scene 2 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: 吃了：在吃，an action continuing with 一直 needs the progressive form 在 + verb, not 了, which marks completion. [rule: aspect_le_completed]
- shennong_samples#49 scene 3 (2/3 runs) -- Runs 1 and 2 identify the misuse of 别人, but Run 3 flags nothing and therefore does not correct it.
  - run 1: 别人：一个男人，别人 distinguishes other people from a stated person or group, but no such contrast has been established here; use an indefinite noun 
  - run 2: 别人：一个人，别人 distinguishes other people from a speaker or a stated person; an unknown rescuer should be introduced as 一个人. [teacher rule: biere
  - run 3: —
- shennong_samples#49 scene 3 (1/3 runs)
  - run 1: 像伞的植物：像伞一样的植物，Use the comparison pattern 像……一样 to state that the plant has the shape of an umbrella. [rule: none]
  - run 2: —
  - run 3: —
- shennong_samples#49 scene 3 (1/3 runs)
  - run 1: 不再生病了：肚子不再痛了，生病 means “to become ill”; for the current recovery from the poison, refer to the symptom that has stopped. [rule: none]
  - run 2: —
  - run 3: —
- shennong_samples#49 scene 3 (2/3 runs) -- Run 1 addresses the incorrect verb, while Run 3 adds a sequence connector and leaves it unchanged, and Run 2 flags nothing.
  - run 1: 测量起来了：明白了，测量 means physically determining size or length, while this sentence describes realizing the different effects of the two plants. [
  - run 2: —
  - run 3: Coherence (Conjunction): 他测量起来了：后来，他测量起来了，Add 后来 to show that this is the next event after he recovers. [rule: coherence_connectives]
- shennong_samples#49 scene 3 (1/3 runs)
  - run 1: 像星星的植物：像星星一样的植物，Use the comparison pattern 像……一样 to describe the plant’s star-like shape. [rule: none]
  - run 2: —
  - run 3: —
- shennong_samples#49 scene 3 (1/3 runs)
  - run 1: —
  - run 2: Coherence (Temporality): 找到他了：找到了他，Finding him is a completed action, so 了 follows the verb before its object. [rule: aspect_le_completed]
  - run 3: —
- shennong_samples#49 scene 3 (1/3 runs)
  - run 1: —
  - run 2: —
  - run 3: Coherence (Reference): 他：自己，Because the person who is thinking and the person who may die are the same, use 自己 to make the self-reference cl
- shennong_samples#8 scene 1 (3/3 runs) -- Run 1 also corrects the missing 就 in the 一……就 structure, whereas Runs 2 and 3 address only 看→看到 and leave that issue unfixed.
  - run 1: 一看很多人正在吃一些植物：一看到很多人正在吃一些植物，就发现一些人一吃植物就生病了，看到 expresses the result of looking—actually seeing—and the pattern 一V requires 就 in the following 
  - run 2: 一看很多人正在吃一些植物：看到很多人正在吃一些植物，the intended meaning is that 神农 perceived the people; 看 means “look,” while 看到 marks the result of seeing. [rule: 
  - run 3: 一看：看到，Here the verb means that Shennong perceived the people, so it needs the resultative complement 到. [rule: resultative_complement]
- shennong_samples#8 scene 1 (1/3 runs)
  - run 1: —
  - run 2: Coherence (Reference): 一天，神农：一天，他，use a pronoun when the character was named in the immediately preceding sentence and no other character co
  - run 3: —
- shennong_samples#8 scene 2 (3/3 runs) -- All runs identify the same misuse of “毒得很,” but “有毒” is grammatical without preserving the teacher’s intended intensive meaning “毒性强得很.”
  - run 1: 一些植物毒得很：一些植物有毒，The word “毒” cannot be intensified with “得很”; use “有毒” to describe poisonous plants. [teacher rule: du_youdu]
  - run 2: 一些植物毒得很：一些植物有毒，“毒” cannot be intensified with “得很”; use “有毒” to state that a plant is poisonous. [teacher rule: du_youdu]
  - run 3: 毒得很：有毒，毒 cannot take a degree complement such as 得很; use 有毒 to describe a poisonous plant. [teacher rule: du_youdu]
- shennong_samples#8 scene 2 (1/3 runs)
  - run 1: —
  - run 2: Coherence (Reference): 神农：他，The character was named in the immediately preceding context and no other possible subject competes here, so a p
  - run 3: —
- shennong_samples#8 scene 3 (2/3 runs) -- Runs 1 and 3 flag a missing 了, while Run 2 flags nothing, and the teacher instead corrects the time word and object wording without requiring 了.
  - run 1: Coherence (Temporality): 告诉：告诉了，This is a completed narrative action that happens later, so it needs 了 to mark completion. [rule: aspect_le_
  - run 2: —
  - run 3: Coherence (Temporality): 告诉：告诉了，this is a completed event in the past narrative, so the verb needs 了 to mark completion. [rule: aspect_le_co
- shennong_samples#8 scene 3 (2/3 runs) -- Run 1 flagged no error, while Runs 2 and 3 both address the wording after “这就要看” with equivalent plant-type corrections.
  - run 1: —
  - run 2: 这就要看你想不想生病了：这就要看是什么植物了，this pattern should identify the uncertain factor that determines the answer; whether someone wants illness does not 
  - run 3: 这就要看你想不想生病了：这就要看是哪种植物了，this pattern should identify the uncertain condition that determines the answer; here, the type of plant determines w
