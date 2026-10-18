# Step 10 report: content check (required scenes) -- test

- model gpt-5.6-terra (medium), prompt ef48428c82, 3 run(s) per story; tokens {'prompt_tokens': 100500, 'completion_tokens': 116827, 'total_tokens': 217327}
- 20 test stories, 120 required scenes in total; the teacher flagged 46 as missing (1 of them only partly)
- evidence quotes not found in the story: 2

## How her flags map onto her scene list

| Her flag | Mapped to scene | Part only? | Word overlap |
|---|---|---|---|
| 孟母 decided to move away from the neighborhood near the graveyard because 孟子 imitated how to offer sacrifices every day | 2. 孟母 decided to move away from the neighborhood near the grave |  | 0.8 |
| 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day | 3. 孟母moved to the neighborhood near the market, 孟子imitated how  |  | 1.0 |
| 孟母 moved from the market to the neighborhood near a school, 孟子started to study every day | 4. 孟母 moved from the market to the neighborhood near a school,  |  | 1.0 |
| 神农found茶and took a record | 3. 神农found茶and took a record |  | 1.0 |
| 神农fainted | 4. 神农tried 夹竹桃 and fainted | yes | 1.0 |
| another person in brown came by and had a conversation with 神农 | 6. another person in brown came by and had a conversation with  |  | 1.0 |
| 神农takes record of灵芝and夹竹桃 | 7. 神农takes record of灵芝and夹竹桃 |  | 1.0 |
| 神农tried 夹竹桃 and fainted | 4. 神农tried 夹竹桃 and fainted |  | 1.0 |
| a person in blue stopped by and gave灵芝to 神农，神农felt better after eating灵芝 | 5. a person in blue stopped by and gave灵芝to 神农，神农felt better af |  | 1.0 |

## Agreement with her flags

Per required scene: does the check call it a gap where she flagged it, and not where she did not?

| Verdicts used | Counting as a gap | Her gaps found | Check's gaps she also flagged | Scenes where both agree |
|---|---|---|---|---|
| majority of 3 runs | missing only | 27/46 (59%) | 27/30 (90%) | 98/120 (82%) |
| majority of 3 runs | missing + partly | 36/46 (78%) | 36/55 (65%) | 91/120 (76%) |
| run 1 | missing only | 27/46 (59%) | 27/31 (87%) | 97/120 (81%) |
| run 1 | missing + partly | 32/46 (70%) | 32/49 (65%) | 89/120 (74%) |
| run 2 | missing only | 29/46 (63%) | 29/32 (91%) | 100/120 (83%) |
| run 2 | missing + partly | 37/46 (80%) | 37/57 (65%) | 91/120 (76%) |
| run 3 | missing only | 26/46 (57%) | 26/31 (84%) | 95/120 (79%) |
| run 3 | missing + partly | 34/46 (74%) | 34/55 (62%) | 87/120 (72%) |

Stability: the 3 run(s) gave the same verdict for 88/120 (73%) required scenes.

## Per scene of the story

| Story | Scene | Her flags | Check: missing | Check: partly |
|---|---|---|---|---|
| mengmu_san_qian | 1. 孟子and孟母lived near a graveyard, and 孟子 imitated how | 0 | 1 | 2 |
| mengmu_san_qian | 2. 孟母 decided to move away from the neighborhood near | 4 | 1 | 0 |
| mengmu_san_qian | 3. 孟母moved to the neighborhood near the market, 孟子imi | 8 | 6 | 4 |
| mengmu_san_qian | 4. 孟母 moved from the market to the neighborhood near  | 6 | 1 | 4 |
| mengmu_san_qian | 5. 孟子becomes a famous philosopher | 0 | 0 | 1 |
| shennong_chang_baicao | 1. in ancient times, people did not know which plants | 0 | 1 | 1 |
| shennong_chang_baicao | 2. 神农decided to find out which plants are safe to eat | 0 | 0 | 0 |
| shennong_chang_baicao | 3. 神农found茶and took a record | 7 | 5 | 2 |
| shennong_chang_baicao | 4. 神农tried 夹竹桃 and fainted | 3 | 1 | 7 |
| shennong_chang_baicao | 5. a person in blue stopped by and gave灵芝to 神农，神农felt | 4 | 2 | 2 |
| shennong_chang_baicao | 6. another person in brown came by and had a conversa | 9 | 7 | 1 |
| shennong_chang_baicao | 7. 神农takes record of灵芝and夹竹桃 | 5 | 5 | 1 |

## Wrong information found (majority of runs not required; all runs listed)

- mengmu_samples#4: “他们搬了到别一个城市找工作。” — The move away from the graveyard is prompted by 孟母's concern about 孟子 copying sacrifices, not by looking for work.
- mengmu_samples#4: “孟子在那个商店也找了到工作，可是不是做衣服的工作，而是喜欢的工作。” — At the market, 孟子 copies the buying and selling he sees; he does not get a job there.
- mengmu_samples#4: “孟子在那个商店也找了到工作，可是不是做衣服的工作，而是喜欢的工作。” — In the market episode, 孟子 imitates people buying and selling; he does not get a job in the shop.
- mengmu_samples#4: “难怪她跟孩子搬家，原来买不了房。” — This gives not being able to buy a house as the reason for the first move. In the story, 孟母 moves because she worries that copying sacrifices will affect 孟子 badly.
- mengmu_samples#4: “难怪她跟孩子搬家，原来买不了房。” — This gives not being able to buy a house as 孟母's reason for moving, but in the story she moves because she thinks copying sacrifices is bad for 孟子.
- mengmu_samples#4: “难怪她跟孩子搬家，原来买不了房。” — 孟母 moves because she worries that copying sacrifices will negatively affect 孟子, not because she cannot afford a house.
- mengmu_samples#10: “孟子和孟母搬到子思老师的家，跟子思老师住。” — The story requires them to move first near a market and later near a school, not directly to 子思老师's home.
- mengmu_samples#10: “孟子和孟母搬到子思老师的家，跟子思老师住。” — The story requires them to move first to a neighborhood near the market, and later from the market to a neighborhood near a school; it does not say they move to 子思老师's home.
- mengmu_samples#10: “孟子和孟母搬到子思老师的家，跟子思老师住。” — This replaces the required move to the neighborhood near the market, and later the move to the neighborhood near the school.
- mengmu_samples#18: “孟子的妈妈带孟子不是搬到城市，而是搬到了孟子老师的家。” — The story has them move first to a neighborhood near the market, and later to a neighborhood near a school; it does not say they move directly to the teacher's home.
- mengmu_samples#18: “孟子的妈妈带孟子不是搬到城市，而是搬到了孟子老师的家。” — This replaces the move to the neighborhood near the market with a move to 孟子's teacher's home.
- mengmu_samples#18: “孟子的妈妈带孟子不是搬到城市，而是搬到了孟子老师的家。” — This replaces the required move to the neighborhood near the market; later the story also requires a move to a neighborhood near a school.
- mengmu_samples#25: “从他的家到墓地很近，所以他每天老是从早到晚去墓地跟朋友们玩玩儿。” — At the graveyard, 孟子 imitates offering sacrifices, rather than going there to play with friends.
- mengmu_samples#25: “从他的家到墓地很近，所以他每天老是从早到晚去墓地跟朋友们玩玩儿。” — At the graveyard, 孟子 should imitate sacrifice offerings, rather than go there to play with friends.
- mengmu_samples#25: “从他的家到墓地很近，所以他每天老是从早到晚去墓地跟朋友们玩玩儿。” — In the story, 孟子 imitates offering sacrifices near the graveyard, rather than going there to play with friends.
- mengmu_samples#32: “在他们第三个家，孟子学了怎么祭拜。” — Learning to imitate sacrifices belongs when the family lives near the graveyard, not in their third home.
- mengmu_samples#32: “在他们第三个家，孟子学了怎么祭拜。” — This puts 孟子 learning sacrifices in the third home, after the market part. In the story, the sacrifice imitation belongs to the opening graveyard setting; the third home is where he begins studying.
- mengmu_samples#32: “在他们第三个家，孟子学了怎么祭拜。” — 孟子's sacrifice imitation belongs at the beginning, when the family is by the graveyard, before the later moves; it does not first happen in the third home.
- mengmu_samples#32: “孟子老是跟这些卖东西的人常常玩儿” — At the market, 孟子 imitates buying and selling; he is not described as merely playing with the sellers.
- mengmu_samples#33: “孟子妈妈的工作是祭拜，” — The story does not say that 孟母's job was performing sacrifices.
- mengmu_samples#33: “孟子想帮助妈妈祭拜，可是他六岁，所以不能祭拜。” — This says Mengzi could not perform sacrifices at this time, but the opening story has him imitating sacrifice rituals every day.
- mengmu_samples#33: “孟子成为很著名的古代画家。” — Mengzi becomes a famous philosopher in this story, not a famous painter.
- mengmu_samples#33: “孟子成为很著名的古代画家。” — 孟子 becomes a famous philosopher, not a famous ancient painter.
- mengmu_samples#33: “孟子成为很著名的古代画家。” — 孟子 becomes a famous philosopher, not an ancient painter.
- mengmu_samples#33: “很多墓地得我祭拜。所以我们得去很多不同的地方。” — This gives Mengmu's sacrifice work as the reason for moving, instead of her worry that Mengzi's imitation of sacrifices will affect him badly.
- mengmu_samples#33: “所以我们得去很多不同的地方。” — The family moves because 孟母 worries that copying sacrifice offerings will affect 孟子 badly, not because her job requires visits to many places.
- mengmu_samples#33: “所以我们得去很多不同的地方。” — This gives 孟母's work as the reason for moving, rather than her decision to leave the graveyard because she worries about the bad influence on 孟子.
- mengmu_samples#39: “孟子妈妈看了他的同学们对孟子不好的影响，所以孟子和孟子妈妈搬家了。” — In the story, 孟母 moves because she thinks 孟子 copying sacrifice rituals will have a bad effect on him, not because of his classmates' influence.
- mengmu_samples#39: “孟子妈妈看了他的同学们对孟子不好的影响，所以孟子和孟子妈妈搬家了。” — In the story, 孟母 moves because she thinks 孟子 copying sacrifices is harmful, not because of his classmates.
- mengmu_samples#39: “孟子妈妈看了他的同学们对孟子不好的影响，所以孟子和孟子妈妈搬家了。” — In the story, 孟母 moves because she thinks 孟子's imitation of sacrifices near the graveyard is a bad influence, not because of his classmates.
- mengmu_samples#39: “孟子才十一岁，成为一个哲学家。” — He becomes a famous philosopher later, after the moves and his daily study near the school.
- mengmu_samples#39: “孟子才十一岁，成为一个哲学家。” — He becomes a philosopher after the later moves and his period of studying near the school, not immediately after the first move.
- mengmu_samples#39: “孟子才十一岁，成为一个哲学家。” — In the story, 孟子 becomes a philosopher after the moves and after he begins studying near the school, not before that part of the story.
- mengmu_samples#45: “他们搬家到有很多学校的城市。” — The first move should be to a neighborhood near the market; the move near a school happens later, after the market scene.
- mengmu_samples#45: “他的妈妈不是不喜欢他们的城市，而是想孟子有很好的教育。” — This gives good education as the reason for moving, rather than 孟母 being worried that 孟子's sacrifice imitation near the graveyard would affect him badly.
- mengmu_samples#47: “先她让孟子跟朋友玩儿，然后教他怎么买又便宜又好质量的东西。” — In the story, 孟子 first copies sacrifice rituals near the graveyard, and later copies buying and selling from the market; these are not skills his mother teaches him.
- shennong_samples#4: “我一吃夹竹桃，就觉得这种植物对我的脑有坏处。” — After eating 夹竹桃, 神农 faints in the story; the retelling gives a different result.
- shennong_samples#4: “我一吃夹竹桃，就觉得这种植物对我的脑有坏处。” — In the story, eating 夹竹桃 makes 神农 faint; this says only that it harms his brain.
- shennong_samples#8: “神农说，这就要看你想不想生病了。” — This wrongly says that whether plants can be eaten depends on whether a person wants to get sick; 神农 is finding out which plants are actually safe or poisonous.
- shennong_samples#18: “哥哥给神农灵芝。” — In the story, a person who stops by gives 神农 灵芝; his brother is not part of the story.
- shennong_samples#18: “哥哥给神农灵芝。” — In the story, the person who gives 神农 灵芝 is a passer-by in blue, not 神农’s brother.
- shennong_samples#18: “因为他的家人常常生病了，所以神农和他的哥哥一起去旅行找可以吃的植物。” — The story has 神农 travel to investigate plants; it does not include a brother travelling with him.
- shennong_samples#19: “他一喝茶就很不舒服。” — In the story, 神农 becomes ill after trying 夹竹桃, not after drinking 茶.
- shennong_samples#19: “他一喝茶就很不舒服。” — This says that 茶 made 神农 ill. In the story, he becomes ill after trying 夹竹桃; 茶 and 夹竹桃 are different plants.
- shennong_samples#19: “他听说你跟黄色的花做茶很有用。” — The yellow flower is 夹竹桃, which is poisonous; it is not the useful 茶 in the story.
- shennong_samples#19: “他听说你跟黄色的花做茶很有用。” — This treats the yellow flower later identified as 夹竹桃 as useful for making tea, but 夹竹桃 is the poisonous plant in the story.
- shennong_samples#26: “比方说，他一吃灵芝就开始生病。” — In the story, 灵芝 is the medicine that makes 神农 feel better after he is harmed by 夹竹桃; it does not make him sick.
- shennong_samples#26: “比方说，他一吃灵芝就开始生病。” — In the story, 神农 becomes ill after trying 夹竹桃; 灵芝 is the medicine that makes him feel better.
- shennong_samples#26: “比方说，他一吃灵芝就开始生病。” — In the story, 神农 becomes ill and faints after trying 夹竹桃; 灵芝 is the plant that helps him feel better.
- shennong_samples#33: “一吃就开始死。” — After trying 夹竹桃, 神农 faints in the story; he does not begin to die.
- shennong_samples#33: “一吃就开始死。” — After trying 夹竹桃, 神农 faints in the story; he does not start to die.
- shennong_samples#33: “他最喜欢吃花，除了夹竹桃以外，什么都花想吃。” — This says that 神农 did not want to eat 夹竹桃, but in the story he tries 夹竹桃.
- shennong_samples#33: “他最喜欢吃花，除了夹竹桃以外，什么都花想吃。” — This says 神农 did not eat 夹竹桃, but in the story he tries 夹竹桃 and faints.
- shennong_samples#33: “他最喜欢吃花，除了夹竹桃以外，什么都花想吃。” — This says 神农 did not want to eat 夹竹桃, but in the story he tries 夹竹桃.
- shennong_samples#33: “古代时候，人不知道他们能吃什么植物，常常一吃就死。” — In the story, people often became sick after eating some plants, not died.
- shennong_samples#33: “古代时候，人不知道他们能吃什么植物，常常一吃就死。” — In the story, people often became sick after eating some plants; they did not usually die immediately.
- shennong_samples#33: “古代时候，人不知道他们能吃什么植物，常常一吃就死。” — In the story, people often became sick after eating unknown plants, not died.
- shennong_samples#35: “神农不知道他吃不吃灵芝或者夹竹桃。” — In the story, 神农 definitely tries 夹竹桃 before receiving 灵芝; he is not unsure whether he ate it.
- shennong_samples#35: “神农不知道他吃不吃灵芝或者夹竹桃。” — In the story, 神农 has tried 夹竹桃 and then is given 灵芝; he is not unsure whether he ate either plant.
- shennong_samples#35: “神农不知道他吃不吃灵芝或者夹竹桃。” — In the story, 神农 tries 夹竹桃 before another person gives him 灵芝; he is not unsure whether he ate 夹竹桃 or 灵芝.
- shennong_samples#42: “吃了以后，神农快生病。” — In the story, after eating 夹竹桃, 神农 faints; he does not merely almost become ill.
- shennong_samples#42: “吃了以后，神农快生病。” — In the story, after eating 夹竹桃, 神农 faints; he does not merely almost become sick.
- shennong_samples#42: “吃了以后，神农快生病。” — In the story, after trying 夹竹桃, 神农 faints; he does not merely almost become sick.

## Example learner feedback (run 1, first 6 stories)

**mengmu_samples#4**

**mengmu_samples#10**
- After they leave the graveyard, add that 孟母 moves them near the market and 孟子 copies buying and selling.
- After the market events, add that 孟母 moves them near a school before 孟子 studies every day.

**mengmu_samples#12**

**mengmu_samples#18**
- Near the graveyard, add that 孟子 copied the way people offered sacrifices.
- After they leave the graveyard and before 孟子 studies with his teacher, add that they move near a market and 孟子 copies buying and selling.

**mengmu_samples#25**
- Before 孟母 moves the family away, add that 孟子 copied how people offered sacrifices near the graveyard.
- After the family leaves the graveyard, add that they move near a market and 孟子 copies buying and selling there.
- After the market part, add that they move near a school, where 孟子 starts to study every day.

**mengmu_samples#32**

