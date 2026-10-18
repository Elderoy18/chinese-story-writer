# Step 10 report: content check (required scenes) -- train

- model gpt-5.6-terra (medium), prompt b2931ef374, 1 run(s) per story; tokens {'prompt_tokens': 89970, 'completion_tokens': 185559, 'total_tokens': 275529}
- 83 train stories, 499 required scenes in total; the teacher flagged 194 as missing (0 of them only partly)
- evidence quotes not found in the story: 8

## How her flags map onto her scene list

| Her flag | Mapped to scene | Part only? | Word overlap |
|---|---|---|---|
| 孟母moved to the neighborhood near the market, 孟子imitated how to buy and sell every day | 3. 孟母moved to the neighborhood near the market, 孟子imitated how  |  | 1.0 |
| 孟母 decided to move away from the neighborhood near the graveyard because 孟子 imitated how to offer sacrifices every day | 2. 孟母 decided to move away from the neighborhood near the grave |  | 0.8 |
| 孟母 moved from the market to the neighborhood near a school, 孟子started to study every day | 4. 孟母 moved from the market to the neighborhood near a school,  |  | 1.0 |
| 孟子becomes a famous philosopher | 5. 孟子becomes a famous philosopher |  | 1.0 |
| 神农became better after eating灵芝 | 5. a person in blue stopped by and gave灵芝to 神农，神农felt better af |  | 0.88 |
| another person came by and had a conversation with 神农 | 6. another person in brown came by and had a conversation with  |  | 1.0 |
| 神农takes record of灵芝and夹竹桃 | 7. 神农takes record of灵芝and夹竹桃 |  | 1.0 |
| 神农tried 夹竹桃 and fainted | 4. 神农tried 夹竹桃 and fainted |  | 1.0 |
| a person in blue stopped by and gave灵芝to 神农，神农felt better after eating灵芝 | 5. a person in blue stopped by and gave灵芝to 神农，神农felt better af |  | 1.0 |
| another person in brown came by and had a conversation with 神农 | 6. another person in brown came by and had a conversation with  |  | 1.0 |
| 神农found茶and took a record | 3. 神农found茶and took a record |  | 1.0 |
| a person in blue stopped by and gave灵芝to 神农 | 5. a person in blue stopped by and gave灵芝to 神农，神农felt better af |  | 1.0 |
| 神农felt better after eating灵芝 | 5. a person in blue stopped by and gave灵芝to 神农，神农felt better af |  | 1.0 |

## Agreement with her flags

Per required scene: does the check call it a gap where she flagged it, and not where she did not?

| Verdicts used | Counting as a gap | Her gaps found | Check's gaps she also flagged | Scenes where both agree |
|---|---|---|---|---|
| majority of 3 runs | missing only | 108/194 (56%) | 108/137 (79%) | 384/499 (77%) |
| majority of 3 runs | missing + partly | 190/194 (98%) | 190/373 (51%) | 312/499 (63%) |

Stability: the 1 run(s) gave the same verdict for 499/499 (100%) required scenes.

## Per scene of the story

| Story | Scene | Her flags | Check: missing | Check: partly |
|---|---|---|---|---|
| mengmu_san_qian | 1. 孟子and孟母lived near a graveyard, and 孟子 imitated how | 0 | 8 | 23 |
| mengmu_san_qian | 2. 孟母 decided to move away from the neighborhood near | 19 | 13 | 19 |
| mengmu_san_qian | 3. 孟母moved to the neighborhood near the market, 孟子imi | 33 | 24 | 16 |
| mengmu_san_qian | 4. 孟母 moved from the market to the neighborhood near  | 24 | 5 | 34 |
| mengmu_san_qian | 5. 孟子becomes a famous philosopher | 4 | 4 | 18 |
| shennong_chang_baicao | 1. in ancient times, people did not know which plants | 0 | 8 | 14 |
| shennong_chang_baicao | 2. 神农decided to find out which plants are safe to eat | 0 | 2 | 17 |
| shennong_chang_baicao | 3. 神农found茶and took a record | 27 | 14 | 20 |
| shennong_chang_baicao | 4. 神农tried 夹竹桃 and fainted | 12 | 3 | 36 |
| shennong_chang_baicao | 5. a person in blue stopped by and gave灵芝to 神农，神农felt | 19 | 5 | 25 |
| shennong_chang_baicao | 6. another person in brown came by and had a conversa | 32 | 25 | 7 |
| shennong_chang_baicao | 7. 神农takes record of灵芝and夹竹桃 | 24 | 26 | 7 |

## Wrong information found (majority of runs not required; all runs listed)

- mengmu_samples#1: “为了找工作，孟母和孟子搬了很多次家。” — In the required story, 孟母 moves because of 孟子’s behaviour, not to look for work, and the story has the two moves from the graveyard area to the market area and then to the school area.
- mengmu_samples#1: “他每天在文学家的房子上学，从早到晚一直学习，他不是看书就是写文章，难怪他长大以后就成为了很有名的哲学家。” — The required story places the family near a school; it does not say that 孟子 studies in a famous writer’s house.
- mengmu_samples#1: “孟子才九岁，已经搬了五次家。” — The required story describes two moves, not five.
- mengmu_samples#2: “不是他喜欢学习写文字，而是他的爸爸喜欢他练习。” — The required story has no father who makes 孟子 practise writing.
- mengmu_samples#2: “他爸爸说，你不是在祭拜，就是在学习，所以孟子从早到晚没有空，老是很累，害得他的身体不好。” — The required story has no father giving this instruction or causing 孟子 to become exhausted and unhealthy.
- mengmu_samples#3: “孟子和孟母住在一起。孟母望子成龙，可是孟子想当小商贩，老是在路上跟朋友们一起卖东西。” — The story says 孟子 imitates buying and selling after moving near the market; it does not say that he actually sells things with friends as a street vendor.
- mengmu_samples#3: “所以孟子才八岁，跟孟母一起搬家三次。” — The required story has two moves: first from the graveyard area to the market area, then from the market area to the school area; it does not have three moves.
- mengmu_samples#5: “不是她觉得孩子们最好不玩，而是她觉得墓地不合适孩子们玩。” — 孟母's reason for moving was concern about the bad effect of 孟子 copying sacrifice offerings, not that a graveyard was unsuitable for children to play in.
- mengmu_samples#5: “大人的时候，他成为很有名的老师。” — The story says that 孟子 becomes a famous philosopher, not a famous teacher.
- mengmu_samples#5: “孟子老是买东西。” — In the story, 孟子 imitates the buying and selling he sees at the market; he is not simply described as buying things.
- mengmu_samples#6: “他们才搬了三次家。” — The required story describes a move from the graveyard area to the market area, then a move from the market area to the school area: two moves, not three.
- mengmu_samples#7: “可是搬了十次家。” — The required story has the family move away from the graveyard, then to the market, and then from the market to near a school; it does not say they moved ten times.
- mengmu_samples#8: “他长大了以后，成为很有名的作家。” — 孟子 becomes a famous philosopher in the story, not a famous writer.
- mengmu_samples#8: “孟母望子成龙，她让孟子才两岁就开始学习。” — In the story, 孟子 begins studying after 孟母 moves with him to the neighbourhood near a school, not when he is two.
- mengmu_samples#11: “一天三次搬家了。” — The story has two moves: from the graveyard area to the market area, then to the school area; it does not say they moved three times in one day.
- mengmu_samples#11: “孟子一直跟他的朋友去了墓地祭拜。” — This changes 孟子 copying sacrificial rituals into actually worshipping at the graveyard with friends.
- mengmu_samples#14: “孟子的妈妈有她的道理，不是房租太贵了，就是地方太吵了。” — For the move away from the graveyard, 孟母's reason is that 孟子 copying sacrifices would have a bad influence on him, not rent or noise.
- mengmu_samples#14: “孟母老是搬家，她搬家搬了三次了。” — The story has two moves: from the graveyard neighborhood to the market neighborhood, and then to the school neighborhood.
- mengmu_samples#15: “妈妈以为他老是在墓地玩，觉得害得孟子的身体，” — In the story, 孟母 moves because she worries that 孟子 copying sacrifice rituals will negatively influence him, not because playing in the graveyard harms his physical body.
- mengmu_samples#16: “古代的时候，孟子跟妈妈一起住在西安。” — The story says they lived near a graveyard at the beginning, not in 西安.
- mengmu_samples#16: “她以为孟子每天出去跟别的小孩子在马路上老是玩游戏，” — 孟母 sees 孟子 imitating sacrifice offerings; she does not think that he is playing games in the road.
- mengmu_samples#19: “孟子的妈妈怕孟子会受到别的小孩子的影响，所以她带孟子到一个城市搬家了。” — 孟母 moves away because she thinks 孟子 copying sacrifices is harmful, not because of the influence of other children.
- mengmu_samples#19: “孟子的妈妈觉得住在城市里很危险，所以他们到城市的外边搬家了。” — The next move is from the market neighbourhood to a neighbourhood near a school, not because the city is dangerous.
- mengmu_samples#20: “不是因为他们很喜欢旅行，而是因为他们每次搬家都找不到好工作，害得他们需要再搬家。” — The moves were not because the family could not find good work. The first move was because 孟母 worried that the graveyard rituals would negatively affect 孟子.
- mengmu_samples#20: “别人不是给他们很少钱，就是一点儿钱都没付，害得孟子才九岁的时候，他的妈妈选择搬家来找到比较好的工作。” — 孟母 moved because she was concerned about the effect of 孟子 copying sacrifice rituals, not to find a better job.
- mengmu_samples#20: “在这儿，他们卖日用品，可是他们的收入也很低，害得孟子才十一岁他们又搬家。” — In the story, 孟子 copies the buying and selling he sees near the market; the family is not described as selling household goods for income.
- mengmu_samples#20: “这儿，孟子和孟母从早到晚都在墓地帮别人祭拜他们的死家人，可是他们老是有问题。” — The story says 孟子 imitated sacrifice rituals near the graveyard; it does not say that he and 孟母 worked there helping others perform sacrifices.
- mengmu_samples#21: “他们新的家在商店的旁边” — The required story says their new home is near a market, not near a single shop.
- mengmu_samples#22: “孟母一看孟子祭拜，就觉得孟子学哲学最重要。” — This gives 孟母 the opposite reaction: in the story, she worries that copying sacrifices will have a bad impact on 孟子 and decides to move.
- mengmu_samples#23: “在新家，一直去墓地吃祭品。” — After the first move, they live near a market and 孟子 imitates buying and selling; he does not continue going to the graveyard to eat offerings.
- mengmu_samples#23: “孟子妈妈说，哎呀，你从早到晚去墓地吃祭品，所以他们要搬家。” — The move is prompted by 孟子 copying sacrifice rituals and 孟母's concern about their influence, not by him eating offerings.
- mengmu_samples#23: “孩子叫孟子，孟子是淘气的孩子，因为老是去墓地吃祭品。” — In the story, 孟子 imitates the way people offer sacrifices; he does not go to the graveyard to eat offerings.
- mengmu_samples#26: “孟母觉得孟子不喜欢他的小的城，所以她和孟子搬家。” — 孟母 moves because she worries that copying sacrifices near the graveyard will harm 孟子, not because she thinks he dislikes the small city.
- mengmu_samples#26: “孟母觉得学习害得孟子，所以孟子常常玩玩。” — This conflicts with the story: after moving near the school, 孟子 begins studying.
- mengmu_samples#27: “他们老是搬家，不是因为他们喜欢搬家，而是因为他们没有很多钱，害得孟子的妈妈一直需要找工作。” — This gives poverty and work as the reason for moving, but 孟母 moves because she worries that Meng子's imitation will negatively affect him.
- mengmu_samples#27: “孟子才三岁开始搬家，以后每年搬家。” — The story has two specific moves: first from the graveyard area to the market area, then from the market area to the school area; it does not say they moved every year.
- mengmu_samples#29: “孟子的妈妈一共搬了三次家。” — In the required story, 孟母 moves twice: from the graveyard area to the market area, and then from the market area to the school area.
- mengmu_samples#30: “孟子的妈妈说每天跟朋友见面害得他学习不怎么样。” — 孟母's concern in the story is that imitating sacrifices near the graveyard will harm 孟子, not that meeting friends harms his studies.
- mengmu_samples#31: “可是搬才三次就找到好的地方。” — The required story has two moves: from the graveyard area to the market area, then from the market area to the school area.
- mengmu_samples#34: “孟子长大了以后成为一名画家，因为他画画儿很厉害。” — 孟子 becomes a famous philosopher, not a painter.
- mengmu_samples#35: “最后，他们在农村上住。” — The final move is to a neighborhood near a school, not to the countryside.
- mengmu_samples#35: “第一次他们搬家，他们在墓地住。” — In the story, they already live near the graveyard at the beginning; their later move is away from the graveyard.
- mengmu_samples#35: “难怪她的男孩子成为孟子。” — The boy is already 孟子; the ending is that he becomes a famous philosopher.
- mengmu_samples#37: “但是孟子一直哭了。” — In the graveyard neighborhood, the story says 孟子 imitated how to offer sacrifices, not that he kept crying.
- mengmu_samples#38: “他们一直在搬家，因为孟母的工资很低。” — The move away from the graveyard is supposed to happen because 孟母 is worried about 孟子 copying sacrifices, not because of low wages.
- mengmu_samples#38: “有一天，孟母找到一个打工，在墓地做祭拜。” — The graveyard scene is about the family living near a graveyard and 孟子 copying sacrifices, not 孟母 getting a job there.
- mengmu_samples#38: “现在孟子和孟母不是打算搬家，而是打算待在这个小镇。” — They need to move on from the graveyard area to the market area and then to the school area.
- mengmu_samples#40: “孟子说我不是不想学哲学，而是住在墓地的旁边太吵了。” — This gives noise at the graveyard as the reason for moving, but 孟母 moves because she thinks copying sacrifices will negatively affect 孟子.
- mengmu_samples#43: “她跟孟子搬家去墓地做祭拜” — In the story, they already live near the graveyard, and 孟子 imitates sacrificial rituals. They do not move to the graveyard together to perform the rituals.
- mengmu_samples#44: “一天，孟子决定了祭拜。” — 孟子 does not decide to perform sacrifices on one day; he imitates people offering sacrifices every day while living near the graveyard.
- mengmu_samples#44: “她常常搬家” — In the story, 孟母 moves twice: first from the graveyard neighborhood and then from the market neighborhood.
- mengmu_samples#49: “所以每天从早到晚，孟子跟他的妈妈一直待在墓地里。” — The story says 孟子 and 孟母 lived near a graveyard, not that they stayed inside the graveyard all day.
- mengmu_samples#50: “他现在是当医生，他能帮很多人。” — 孟子 becomes a famous philosopher in the story, not a doctor.
- mengmu_samples#50: “他的妈妈已经搬家很多次，差不多十次。” — The story has two moves: from the graveyard area to the market area, then from the market area to the school area.
- mengmu_samples#50: “孟子的妈妈觉得她得搬家，因为现在在他们的省，在中国不太安全。” — In the story, 孟母 decides to move because 孟子 is copying sacrifices, not because the area is unsafe.
- mengmu_samples#50: “难怪她想搬家，因为如果她搬家，她会工作少，和她也会做她最喜欢的兴趣爱好。” — This gives work and hobbies as the reason for moving, but the story says the reason is 孟子 copying sacrifices.
- mengmu_samples#51: “他们搬家三次以后，孟母找到了一位老师。” — The required story has the family move from the graveyard area to the market area and then to the school area; it does not describe three moves or 孟母 finding a teacher after them.
- shennong_samples#1: “一吃夹竹桃就死，这就要看你也吃不吃灵芝了。” — The story says 神农 faints after eating 夹竹桃; it does not say that eating it causes death.
- shennong_samples#5: “毒他吃很多次，比方说，他吃了灵芝和夹竹桃。” — This presents 灵芝 as a poison. In the story, 灵芝 is what helps 神农 feel better after he faints from 夹竹桃.
- shennong_samples#7: “他一吃夹竹桃就生病了。” — In the story, 神农 faints after trying 夹竹桃, rather than only becoming sick.
- shennong_samples#9: “男人问他，神农，什么植物可以吃？” — This makes the man who helped 神农 the person who talks with him. In the required story, a different second visitor comes by for this conversation.
- shennong_samples#10: “他的朋友太糟糕了，他们常常饿死了，所以他看什么就吃什么。” — The story says people often became sick after eating plants they did not understand; it does not say that 神农's friends often starved to death.
- shennong_samples#10: “夹竹桃有毒，但是他们不知道这个花有毒，所以肚子疼死了。” — In the story, 神农 tries 夹竹桃 and faints; he does not die from stomach pain.
- shennong_samples#10: “所以他一吃，肚子就疼死了。” — After eating 灵芝 in the story, 神农 feels better, not stomach pain or death.
- shennong_samples#10: “神农的朋友告诉神农，麻烦你去找药。” — In the story, 神农 himself decides to discover which plants are safe to eat; a friend does not tell him to look for medicine.
- shennong_samples#11: “再找到了灵芝，灵芝真像伞。所以神农吃了，一吃就生病。” — In the story, 神农 feels better after eating 灵芝; he does not become sick from it.
- shennong_samples#11: “神农回他的家，他看到了药，正好看到了毒植物，特别是灵芝和夹竹桃。” — This says that 灵芝 is a poisonous plant, but in the story 灵芝 is the medicine that helps 神农 feel better.
- shennong_samples#15: “他一吃就病了。” — In the required story, 神农 faints after eating 夹竹桃, rather than only becoming ill.
- shennong_samples#16: “正好他的旁边有灵芝” — In the story, a person gives 灵芝 to 神农; it is not simply beside him.
- shennong_samples#17: “夹竹桃找到了灵芝，他给神农。” — 夹竹桃 does not find or give 灵芝. A person in blue gives 灵芝 to 神农.
- shennong_samples#17: “所以他的朋友夹竹桃帮他。” — 夹竹桃 is the plant that 神农 tries and that makes him faint; it is not his friend or helper.
- shennong_samples#20: “别的人看到神农疼死了。” — This says that 神农 died from pain, but in the story he faints after eating 夹竹桃.
- shennong_samples#21: “夹竹桃很好吃，也对你的健康有好处。” — This contradicts the story: after 神农 tries 夹竹桃, he faints.
- shennong_samples#21: “比方说，一个人一吃灵芝就死了。” — This contradicts the story: 灵芝 helps 神农 feel better after he eats it.
- shennong_samples#22: “只吃灵芝对身体不好，特别是夹竹桃对身体更不好。” — In the story, 神农 feels better after eating 灵芝.
- shennong_samples#22: “这个镇没有药，所以神农的朋友都生病了。” — In the story, people became sick because they ate plants they did not know were unsafe, not because the town had no medicine.
- shennong_samples#23: “他一喝那杯茶，就疼死了。” — In the story, 神农 faints after trying 夹竹桃; he does not die from drinking tea.
- shennong_samples#24: “夹竹桃是毒，所以神农的肚子疼死了。” — The story says 神农 fainted after trying 夹竹桃, not that he died from stomach pain.
- shennong_samples#25: “比方说，他一吃夹竹桃，就生病了。” — In the required story, 神农 faints after trying 夹竹桃, rather than only becoming ill.
- shennong_samples#28: “他一吃就毒死了。” — After eating 夹竹桃, 神农 faints; he does not die.
- shennong_samples#28: “正好很多人离神农很近，些的男人看神农，要帮他。” — The story has one person who stops and helps 神农, not many people.
- shennong_samples#31: “正好两个人在他吃毒的地方，他们帮助老人。” — The story has two separate arrivals: first a person in blue gives 神农 灵芝, and later another person in brown talks with him. They are not both presented as being there together when he eats the poisonous plant.
- shennong_samples#36: “他朋友帮他，他们给神农灵芝。” — In the story, a person in blue who stops by gives 灵芝 to 神农, not his friends.
- shennong_samples#36: “哎呀，神农就病了。” — After eating 夹竹桃, 神农 faints in the story, rather than only becoming sick.
- shennong_samples#36: “正好在山上看到很多植物，但是不多植物可能吃，特别是夹竹桃。” — The story says people did not know which plants were edible; it does not say that only a small number of plants could be eaten.
- shennong_samples#37: “他想吃植物可能可以解决他的问题，他走到离家很远的地方。” — 神农 tries plants to learn which are safe to eat, not to cure his growing ears.
- shennong_samples#37: “他穿灰色衣服以后，神农发现他朋友的耳朵突然变小了。” — After eating 灵芝, 神农 feels better; the story does not say that his friend's ears become smaller.
- shennong_samples#37: “他穿蓝色衣服的朋友吃了灵芝。” — The person in blue gives 灵芝 to 神农; the blue person does not eat it instead.
- shennong_samples#37: “有一天，他的耳朵变得太重了，神农摔倒在地上。” — 神农 faints after trying 夹竹桃, not because his ears become too heavy.
- shennong_samples#37: “灵芝是小耳朵的药，我非常开心。” — 灵芝 makes 神农 feel better after he faints from 夹竹桃; it is not medicine for making ears smaller.
- shennong_samples#38: “在中国古代很多人生病了，因为谁都没有药，所以，人山人海死了。” — The story explains that people got sick because they did not know which plants were edible, not because nobody had medicine.
- shennong_samples#38: “神农吃了那个花以后头越来越好。” — In the story, eating 夹竹桃 makes 神农 faint; he feels better after eating 灵芝.
- shennong_samples#40: “这时，一个穿着蓝色衣服的男人和一个穿着咖啡色的衣服的男人正好一起走过来。” — The brown-clothed person is supposed to come by later, after the blue-clothed person gives 神农 灵芝 and he feels better, not arrive together with him.
- shennong_samples#41: “吃了这个花儿以后，神农的肚子疼得受不了。” — After trying 夹竹桃, the story says that 神农 faints, not that he has unbearable stomach pain.
- shennong_samples#41: “过几个分钟，一个穿紫色的男孩儿看到了神农” — The other person in the story wears brown, not purple.
- shennong_samples#44: “一个穿蓝衣服的人和他的朋友路过，碰巧看到神农受苦，就给了他一个附近的蘑菇吃。” — The person in blue should give 神农 灵芝, not an unnamed nearby mushroom.
- shennong_samples#44: “他们的父亲神农担心儿子们的病，决定出发寻找药物来治病。” — 神农's reason for trying plants is changed: he should set out to discover which plants are safe to eat and which are not.
- shennong_samples#44: “当他继续徘徊时，他偶然看到了一朵美丽的黄花。” — The plant in this event should be 夹竹桃, not an unspecified yellow flower.
- shennong_samples#45: “可是一吃就肚子疼，难受得不得了。” — This replaces the required outcome after eating 夹竹桃: 神农 should faint.
- shennong_samples#45: “所以他决定去山上找什么植物很好吃。” — This gives 神农 a different goal: he should decide to find out which plants are safe to eat and which are unsafe, rather than only which plants taste good.
- shennong_samples#46: “一个农民帮神农吃灵芝” — In the story, a passer-by gives 灵芝 to 神农; the person does not merely help him eat it.
- shennong_samples#46: “所以他的头疼死了。” — The story says 神农 fainted after trying 夹竹桃, not that he had a severe headache.
- shennong_samples#47: “如果跟蘑菇一样的植物，做饭可以，没再有毒了。” — 灵芝 helps 神农 feel better after he eats it; the story does not say it makes 夹竹桃 safe or removes its poison for cooking.
- shennong_samples#47: “有一位餐馆的老板决定世界旅行找新植物做饭。” — The story says 神农 decides to find out which plants are safe to eat and which are not; he is not a restaurant owner travelling to find cooking ingredients.
- shennong_samples#47: “有一天，老板第一次看到一黄色新的花，赶快想吃下去。” — The plant 神农 tries in the story is 夹竹桃, not an unnamed yellow flower.
- shennong_samples#47: “老板不可动，得问男人给他地方上像蘑菇一样的植物吃了。” — The healing plant in the story is 灵芝, not an unnamed mushroom-like plant.
- shennong_samples#48: “在家，王朋吃了蘑菇吃了以后，王朋不再哭了。” — In the story, 神农 feels better after eating 灵芝; 王朋 does not recover after eating a mushroom.
- shennong_samples#48: “爬山前，他们吃了很多植物，神农的儿子王朋吃了夹竹桃，就开始肚子疼。” — In the story, 神农 tries 夹竹桃 and faints; there is no son named 王朋 who eats it and gets a stomachache.
- shennong_samples#48: “神农决定跟家人回家，他要回家，所以王朋也可以吃一个蘑菇，那个蘑菇是药。” — The cure in the story is 灵芝 given to 神农 by a person in blue, not a medicinal mushroom for 王朋.
- shennong_samples#51: “有一天，他看到夹竹桃，他吃了以后，马上感觉不舒服。” — After eating 夹竹桃, the story says that 神农 faints, not only that he feels uncomfortable.
- shennong_samples#52: “穿着紫色衣服的男人怎么了？” — The second person should be wearing brown, not purple.
- shennong_samples#52: “紫色人告诉他：你吃了灵芝，一吃就你的身体最好的。” — The second person should be wearing brown, not purple.

## Example learner feedback (run 1, first 6 stories)

**mengmu_samples#1**
- At the beginning, add that 孟子 and 孟母 lived near the graveyard before 孟子 copied sacrifices.
- After 孟子 copies sacrifices, say that 孟母 decides to move away from the graveyard because this is bad for him.
- After they leave the graveyard area, add that they move near the market and 孟子 copies buying and selling.
- After the market events, say that 孟母 moves near a school, and then 孟子 begins studying.

**mengmu_samples#2**
- At the beginning, add that 孟子 and 孟母 lived near the graveyard and that 孟子 copied the sacrifice ritual.
- After the graveyard events, add that 孟母 decided to move away because she thought the sacrifice imitation would be bad for 孟子.
- After they leave the graveyard, add that 孟母 moved near the market and 孟子 copied buying and selling.
- After the market events, add that they moved near a school before 孟子 started studying.
- At the end, say that 孟子 became a famous philosopher.

**mengmu_samples#3**
- Before 孟母 decides to move, add that 孟子 imitates sacrifice offerings every day near the graveyard.
- When 孟母 leaves the graveyard area, say that she worries 孟子’s sacrifice imitation will affect him badly.
- After leaving the graveyard area and before the school move, add that they move near the market and 孟子 imitates buying and selling there.
- After the market events and before 孟子 studies hard, add that 孟母 moves to a neighbourhood near a school.

**mengmu_samples#5**
- Near the beginning, before the first move, add that 孟子 and 孟母 live near a graveyard and 孟子 copies sacrifice offerings.
- When 孟母 moves after the graveyard episode, make clear that they are leaving a home near the graveyard.
- After this first move, say that they live near a market and 孟子 copies buying and selling.
- After they leave the market area, add that their new home is near a school before 孟子 begins to study.
- At the end, say that 孟子 becomes a famous philosopher.

**mengmu_samples#6**
- At the beginning, add that 孟子 and 孟母 lived near a graveyard and 孟子 copied sacrificial offerings.
- After the graveyard events, add that 孟母 decided to leave because copying sacrifices could affect 孟子 badly.
- After they leave the graveyard, add that they moved near a market and 孟子 copied buying and selling.
- Before 孟子 studies every day, say that they moved from the market to a neighborhood near a school.
- At the end, say that 孟子 became a famous philosopher, not only a famous scholar.

**mengmu_samples#7**
- At the beginning, add that 孟子 and 孟母 live near a graveyard and 孟子 copies sacrifice ceremonies.
- After the graveyard events, say that 孟母 moves away from the graveyard area.
- After they leave the graveyard area, add that they move near a market and 孟子 copies buying and selling.
- Before 孟子 studies, add that they move from the market to a neighborhood near a school.
- At the end, say that 孟子 becomes a famous philosopher.

