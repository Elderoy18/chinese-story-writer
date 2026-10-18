# Consistency: v1 S5, v1 S6 and v2, each run 3 times

Same 6 stories / 18 scenes as `v1_vs_v2.md`. Repeat runs use identical inputs: v1 stages `S5-r2/-r3`, `S6-r2/-r3` (aliases in `eval/stages.json`); v2 runs 2-3 from `eval/v1_vs_v2/v2_repeat.py` (LLM finder run k, explanation and enrichment re-run, content-check run k; the GEC model and teacher patterns are deterministic). All judged with the same judge and prompts as `v1_vs_v2.md`.

## 1. Run to run

A **place** is a stretch of the student's text flagged in at least one run (overlapping items across runs count as one place).

| | v1-S5 | v1-S6 | v2-S0 |
|---|---|---|---|
| Items per run | 78 / 91 / 77 | 87 / 88 / 84 | 101 / 102 / 102 |
| Places flagged in all 3 runs | 53/88 (60%) | 57/85 (67%) | 73/81 (90%) |
| Places flagged in only 1 run | 20/88 (23%) | 11/85 (13%) | 6/81 (7%) |
| &nbsp;&nbsp;of which wrong (false positive or incorrect) | 9/20 (45%) | 5/11 (45%) | 3/6 (50%) |
| Places in all 3 runs that are wrong | 25/53 (47%) | 21/57 (37%) | 49/73 (67%) |
| Places in all 3 runs: **same corrected text** every time | 12/53 (23%) | 15/57 (26%) | 39/73 (53%) |
| Places in all 3 runs: same section every time | 41/53 (77%) | 40/57 (70%) | 50/73 (68%) |
| Her corrections caught in all 3 runs | 49/88 (56%) | 50/88 (57%) | 70/88 (80%) |
| Her corrections caught in some runs only | 32/88 (36%) | 25/88 (28%) | 7/88 (8%) |
| Content: required scenes with the same verdict in all 3 runs | 25/36 (69%) | 25/36 (69%) | 28/36 (78%) |

Quality numbers across the 3 runs, mean (lowest–highest):

| | v1-S5 | v1-S6 | v2-S0 |
|---|---|---|---|
| False positives / scene | 0.57 (0.44–0.67) | 0.50 (0.22–0.67) | 0.85 (0.78–0.94) |
| Incorrect corrections / scene | 0.59 (0.44–0.67) | 0.57 (0.44–0.67) | 1.89 (1.61–2.06) |
| Items fully right | 66% (63%–68%) | 72% (69%–74%) | 30% (29%–31%) |
| Corrected text not fully correct | 16% (13%–21%) | 14% (11%–18%) | 59% (57%–60%) |
| Partial sentences | 3% (3%–4%) | 4% (3%–5%) | 41% (39%–45%) |
| Wrong category | 3% (2%–4%) | 5% (4%–6%) | 34% (32%–37%) |
| Her flagged scenes caught (content) | 98% (93%–100%) | 93% (93%–93%) | 82% (73%–93%) |
| Recall of her corrections | 75% (74%–75%) | 73% (72%–75%) | 83% (82%–85%) |

## 2. Same kind of error, different places

Her corrections grouped by error category (v2's draft category labels on her edits; 21 categories with 2+ corrections in these stories). A category is **mixed** in a run when the run catches some of its places but not others.

| | v1-S5 | v1-S6 | v2-S0 |
|---|---|---|---|
| Categories caught at every place (per run) | 11 / 10 / 10 | 11 / 8 / 13 | 10 / 11 / 9 |
| Mixed (per run) | 9 / 9 / 10 | 8 / 11 / 6 | 10 / 8 / 11 |
| None caught (per run) | 1 / 2 / 1 | 2 / 2 / 2 | 1 / 2 / 1 |

Places caught per category, runs 1 / 2 / 3:

| Category | Her corrections | v1-S5 | v1-S6 | v2-S0 |
|---|---|---|---|---|
| modifier_de_structure | 8 | 8 / 8 / 7 | 7 / 7 / 8 | 8 / 8 / 8 |
| near_synonym_precision | 7 | 5 / 6 / 7 | 7 / 6 / 7 | 6 / 6 / 6 |
| word_class_choice | 5 | 2 / 3 / 2 | 4 / 4 / 5 | 4 / 4 / 4 |
| not_but_refutation | 5 | 0 / 0 / 3 | 0 / 0 / 0 | 3 / 1 / 1 |
| location_with_zai | 4 | 4 / 4 / 4 | 4 / 4 / 4 | 4 / 4 / 4 |
| modal_and_control_verb_complements | 4 | 3 / 4 / 3 | 3 / 4 / 4 | 4 / 4 / 4 |
| redundant_words | 4 | 3 / 2 / 4 | 3 / 2 / 2 | 3 / 4 / 4 |
| collocation_selection | 3 | 3 / 3 / 2 | 3 / 2 / 2 | 2 / 2 / 2 |
| resultative_complements | 3 | 2 / 1 / 1 | 2 / 1 / 0 | 3 / 2 / 2 |
| missing_or_unclear_subject | 3 | 1 / 2 / 3 | 1 / 2 / 2 | 2 / 2 / 2 |
| loose_clause_connection | 2 | 2 / 1 / 1 | 2 / 2 / 2 | 1 / 2 / 1 |
| le_completed | 2 | 2 / 2 / 2 | 2 / 2 / 2 | 2 / 2 / 2 |
| no_le_speaking_word | 2 | 1 / 1 / 0 | 2 / 2 / 2 | 2 / 2 / 2 |
| time_sequence_markers | 2 | 2 / 2 / 2 | 2 / 1 / 2 | 1 / 0 / 1 |
| zero_redundant_pronoun | 2 | 2 / 1 / 1 | 1 / 1 / 2 | 1 / 1 / 1 |
| cause_result_soyi | 2 | 2 / 0 / 2 | 0 / 0 / 1 | 0 / 0 / 0 |
| fixed_expressions | 2 | 1 / 1 / 1 | 1 / 1 / 1 | 1 / 1 / 1 |
| verb_object_valency | 2 | 2 / 2 / 2 | 2 / 2 / 2 | 2 / 2 / 2 |
| question_patterns | 2 | 2 / 2 / 1 | 2 / 1 / 2 | 2 / 2 / 2 |
| search_find | 2 | 1 / 2 / 2 | 2 / 2 / 1 | 2 / 2 / 2 |
| adjective_predicate_degree | 2 | 2 / 2 / 2 | 2 / 2 / 2 | 2 / 2 / 1 |

## 3. Places flagged in only one run

### v1-S5

- mengmu_samples#10 scene 1 (v1-S5-S5-r2) [Coherence: reference] `Coherence (Reference): 孟子五岁的时候：他五岁的时候，Use a pronoun for a close re-occurrence because Mengzi remains` -- ok
- mengmu_samples#10 scene 2 (v1-S5-S5-r2) [Coherence: reference] `Coherence (Reference): 跟子思老师住：跟他住，after 子思老师 has been named earlier in the same sentence, use a pron` -- ok
- mengmu_samples#10 scene 2 (v1-S5-S5-r2) [Coherence: reference] `Coherence (Reference): 孟母帮子思：她帮他，both characters were named in the previous sentence, so close re-oc` -- ok
- mengmu_samples#10 scene 2 (v1-S5-S5-r2) [Coherence: reference] `Coherence (Reference): 子思帮孟母：他帮她，use pronouns when both referents were mentioned in the immediately ` -- ok
- mengmu_samples#32 scene 1 (v1-S5-S5-r2) [Grammar & Vocabulary] `他们会搬家找更好的地方：带着孟子搬家，找一个更好的地方，After a decision verb, use the action that is decided on rather than a f` -- ok
- mengmu_samples#32 scene 2 (v1-S5) [Coherence: temporality] `Coherence (Temporality): 她告诉了孟子：她告诉孟子：，a saying verb that introduces direct speech normally uses the` -- ok
- mengmu_samples#32 scene 3 (v1-S5-S5-r2) [Coherence: temporality] `Coherence (Temporality): 告诉了孟子：告诉孟子，A saying verb that introduces direct speech takes the zero parti` -- ok
- mengmu_samples#32 scene 3 (v1-S5-S5-r3) [Grammar & Vocabulary] `你不是当数学家，而是当哲学家：你不要当数学家，要当哲学家，The original uses the corrective pattern “不是……而是……”, but this line give` -- ok
- mengmu_samples#45 scene 1 (v1-S5-S5-r2) [Coherence: reference] `Coherence (Reference): 城市：∅，Within the same sentence, use zero form for the second mention of the sa` -- incorrect
- shennong_samples#19 scene 2 (v1-S5-S5-r2) [Grammar & Vocabulary] `这冰茶是药：这种茶是药，冰茶 means “iced tea,” but the context refers to the tea made from the yellow flowers. 种 i` -- ok
- shennong_samples#19 scene 2 (v1-S5-S5-r2) [Coherence: connectors] `Coherence (Conjunction): 他一喝茶就很不舒服：可是，他一喝茶就很不舒服，Use 可是 to mark contrast: the tea was said to be usef` -- false positive
- shennong_samples#19 scene 3 (v1-S5) [Coherence: temporality] `Coherence (Temporality): 吃完了：吃完，In a series of completed actions, only the last verb takes 了. Here, ` -- ok
- shennong_samples#19 scene 3 (v1-S5-S5-r3) [Coherence: reference] `Coherence (Reference): 他：神农，Use the name again after several sentences and after the focus has shift` -- false positive
- shennong_samples#33 scene 1 (v1-S5) [Coherence: connectors] `Coherence (Conjunction): 但是不知道为什么，没有办法：人们不知道为什么，也没有办法，but does not express contrast here; 也 links tw` -- false positive
- shennong_samples#33 scene 3 (v1-S5) [Coherence: reference] `Coherence (Reference): 这个口味：一种味道，This is a first mention in the current scene, so the demonstrative ` -- incorrect
- shennong_samples#33 scene 3 (v1-S5) [Coherence: temporality] `Coherence (Temporality): 他发现：他发现了，Use 了 for the completed action of discovering something.` -- incorrect
- shennong_samples#33 scene 3 (v1-S5) [Coherence: connectors] `Coherence (Conjunction): 但是：虽然他生病了，但是他，Contrast needs the paired pattern 虽然……但是…… when the character` -- incorrect
- shennong_samples#33 scene 3 (v1-S5-S5-r3) [Grammar & Vocabulary] `生病时候：生病的时候，A time phrase with 时候 needs 的 after the verb phrase.` -- ok
- shennong_samples#8 scene 1 (v1-S5-S5-r2) [Coherence: connectors] `Coherence (Conjunction): 神农想帮别人。所以想知道：因为神农想帮别人，所以想知道，Use the paired connector “因为……所以……” to show the` -- incorrect
- shennong_samples#8 scene 1 (v1-S5-S5-r3) [Coherence: reference] `Coherence (Reference): 有一个人叫神农：有一位叫神农的人，first mention should introduce a character with a clear noun` -- false positive

### v1-S6

- mengmu_samples#10 scene 1 (v1-S6-S6-r3) [Coherence: temporality] `Coherence (Temporality): 他们搬家不是因为：他们搬家了不是因为，Use “了” because this sentence explains the cause of a co` -- ok
- mengmu_samples#10 scene 2 (v1-S6-S6-r3) [Coherence: reference] `Coherence (Reference): 孟母帮子思打扫房间和做饭：孟母帮他打扫房间和做饭，Use a pronoun for a close re-occurrence of the recen` -- ok
- mengmu_samples#32 scene 1 (v1-S6) [Grammar & Vocabulary] `找到质量好的教育：找到能提供优质教育的地方，“找到” should take something discoverable, such as a place or school; education ` -- ok
- mengmu_samples#32 scene 1 (v1-S6-S6-r2) [Grammar & Vocabulary] `住在这儿教育不太好：这儿的教育不太好，use a possessive structure to show that the education in this place is not good.` -- ok
- mengmu_samples#32 scene 1 (v1-S6-S6-r2) [Coherence: reference] `Coherence (Reference): 他妈妈：孟子的妈妈，on first mention, use a full noun phrase rather than a pronoun-base` -- false positive
- mengmu_samples#45 scene 1 (v1-S6) [Coherence: reference] `Coherence (Reference): 孟子不是祭拜：他不是祭拜，under the pronoun rule, use a pronoun for a recently mentioned c` -- ok
- mengmu_samples#45 scene 3 (v1-S6-S6-r2) [Grammar & Vocabulary] `跟老师孟子学：孟子跟老师学，place the subject before the phrase that names the person he studies with.` -- ok
- shennong_samples#19 scene 2 (v1-S6) [Coherence: reference] `Coherence (Reference): 黄色的花：一些黄色的花，This is the first mention of these flowers, so introduce them as ` -- incorrect
- shennong_samples#33 scene 1 (v1-S6-S6-r2) [Coherence: temporality] `Coherence (Temporality): 试一试很多种植物：试了很多种植物，The reduplicated verb suggests a brief tentative action, b` -- false positive
- shennong_samples#33 scene 3 (v1-S6-S6-r2) [Coherence: connectors] `Coherence (Conjunction): 但是：delete，但是 introduces contrast, but being ill does not contrast with tell` -- false positive
- shennong_samples#8 scene 2 (v1-S6) [Coherence: temporality] `Coherence (Temporality): 神农开始尝很多植物，比方说他吃过生姜、芥兰和菠菜：神农开始尝很多植物，比方说吃了生姜、芥兰和菠菜，Use 了 for the completed ex` -- false positive

### v2-S0

- mengmu_samples#32 scene 3 (v2-S0) [Coherence: connectors] `你不是当数学家 → 你不要当数学家 -- For advice or prohibition, use 不要, not 不是. 不是……而是…… is used to correct a mistak` -- incorrect
- mengmu_samples#45 scene 1 (v2-S0) [Content] `孟子不是祭拜 → 孟子不是模仿别人办丧事 -- Here, 孟子 is copying funeral rituals, not actually worshipping. Use 模仿别人办丧事.` -- ok
- shennong_samples#19 scene 1 (v2-S0-r3) [Coherence: reference] `有的植物吃了以后他的… → 有的植物他吃了以后他的… -- The plants are not doing the eating. Add 他 to show that he eats the pl` -- ok
- shennong_samples#19 scene 3 (v2-S0-r2) [Vocabulary] `这黄色的花是夹… → 这朵黄色的花是夹… -- 朵 normally collocates with a single flower; use 这朵黄色的花.` -- ok
- shennong_samples#33 scene 1 (v2-S0) [Vocabulary] `所以有一天 → 于是有一天 -- Use 于是 to introduce the resulting action naturally here, not 所以.` -- false positive
- shennong_samples#33 scene 3 (v2-S0-r2) [Vocabulary] `他发现这个口味 → 他有这个口味 -- It would be more natural to say 有 because a preference is something a person has` -- incorrect

