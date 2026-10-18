# Step 10 report: content check (required scenes) -- train

- model gpt-5.6-terra (medium), prompt b2931ef374, 1 run(s) per story; tokens {'prompt_tokens': 89970, 'completion_tokens': 178881, 'total_tokens': 268851}
- 83 train stories, 499 required scenes in total; the teacher flagged 194 as missing (0 of them only partly)
- evidence quotes not found in the story: 6

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
| majority of 3 runs | missing only | 106/194 (55%) | 106/128 (83%) | 389/499 (78%) |
| majority of 3 runs | missing + partly | 191/194 (98%) | 191/380 (50%) | 307/499 (62%) |

Stability: the 1 run(s) gave the same verdict for 499/499 (100%) required scenes.

## Per scene of the story

| Story | Scene | Her flags | Check: missing | Check: partly |
|---|---|---|---|---|
| mengmu_san_qian | 1. 孟子and孟母lived near a graveyard, and 孟子 imitated how | 0 | 6 | 27 |
| mengmu_san_qian | 2. 孟母 decided to move away from the neighborhood near | 19 | 14 | 18 |
| mengmu_san_qian | 3. 孟母moved to the neighborhood near the market, 孟子imi | 33 | 23 | 17 |
| mengmu_san_qian | 4. 孟母 moved from the market to the neighborhood near  | 24 | 4 | 34 |
| mengmu_san_qian | 5. 孟子becomes a famous philosopher | 4 | 2 | 20 |
| shennong_chang_baicao | 1. in ancient times, people did not know which plants | 0 | 6 | 16 |
| shennong_chang_baicao | 2. 神农decided to find out which plants are safe to eat | 0 | 2 | 23 |
| shennong_chang_baicao | 3. 神农found茶and took a record | 27 | 14 | 21 |
| shennong_chang_baicao | 4. 神农tried 夹竹桃 and fainted | 12 | 3 | 36 |
| shennong_chang_baicao | 5. a person in blue stopped by and gave灵芝to 神农，神农felt | 19 | 5 | 24 |
| shennong_chang_baicao | 6. another person in brown came by and had a conversa | 32 | 25 | 7 |
| shennong_chang_baicao | 7. 神农takes record of灵芝and夹竹桃 | 24 | 24 | 9 |

## Wrong information found (majority of runs not required; all runs listed)

- mengmu_samples#1: “为了找工作，孟母和孟子搬了很多次家。” — The moves in the story happen because 孟母 wants a better environment for 孟子, first away from the graveyard and then from the market, not in order to find work.
- mengmu_samples#1: “他每天在文学家的房子上学，从早到晚一直学习” — In the story, after leaving the market, they live near a school and 孟子 begins studying there; the story does not replace the school with a literary writer's house.
- mengmu_samples#1: “孟子才九岁，已经搬了五次家。” — The required story has two moves: from the graveyard neighbourhood to the market, and then from the market to the school neighbourhood.
- mengmu_samples#2: “一天孟子病了很重，难怪他病了，原来他昨天吃一张纸，因为他不喜欢学习写名字。” — This serious illness and eating paper are not events in the required story.
- mengmu_samples#2: “他成为了一个人写文章老是好。” — The story's ending is that 孟子 becomes a famous philosopher, not merely someone who is often good at writing.
- mengmu_samples#2: “他爸爸说，你不是在祭拜，就是在学习，所以孟子从早到晚没有空，老是很累，害得他的身体不好。” — The required story describes 孟母 guiding the moves and does not include a father directing 孟子's learning or causing his poor health.
- mengmu_samples#3: “他们搬家不是为了孟母要住在更好的房子，而是为了给孟子找一个好老师。” — The first move is because 孟母 thinks imitating sacrifices near the graveyard will harm 孟子, not because she is looking for a teacher.
- mengmu_samples#3: “所以孟子才八岁，跟孟母一起搬家三次。” — The required story has two moves: from the graveyard to the market, then from the market to the school.
- mengmu_samples#5: “他们去了墓地玩，孟子的妈妈不高兴。” — In the story, 孟子 imitates offering sacrifices at the graveyard; he is not described as going there to play.
- mengmu_samples#5: “大人的时候，他成为很有名的老师。” — 孟子 becomes a famous philosopher, not a famous teacher.
- mengmu_samples#6: “他们才搬了三次家。” — The story has two moves: from the graveyard neighborhood to the market neighborhood, then from the market neighborhood to the school neighborhood.
- mengmu_samples#7: “他今年才九岁，可是搬了十次家。” — This contradicts the story's sequence of the two moves described: first away from the graveyard and then away from the market.
- mengmu_samples#7: “孟子从小到大一直搬家。” — The story has the specific moves from the graveyard to the market and then to the school neighbourhood, not continual moving throughout his life.
- mengmu_samples#7: “孟子学习的时候，他的妈妈祭拜。” — In the story, 孟子 imitates sacrificial offerings while living near the graveyard; it is not 孟母 worshipping while he studies.
- mengmu_samples#8: “他们搬到城市。” — They move to the neighborhood near the market, not simply to a city.
- mengmu_samples#8: “他长大了以后，成为很有名的作家。” — 孟子 becomes a famous philosopher, not a famous writer.
- mengmu_samples#8: “孟母望子成龙，她让孟子才两岁就开始学习。” — In the story, 孟子 starts studying after the move to the neighborhood near a school, not at age two.
- mengmu_samples#8: “孟母看出来孟子老是难过，害得他不能好好学习。” — The bad influence near the graveyard is that 孟子 imitates offering sacrifices, not that he is sad and cannot study.
- mengmu_samples#11: “所以他们住在学校的旁边，一天三次搬家了。” — This says they moved three times, but the story has two moves: from the graveyard to the market, then from the market to the school.
- mengmu_samples#13: “她想搬家不是因为不喜欢孟子的朋友，而是因为住在那里以后孟子一直在没读书。” — 孟母 moves because she thinks 孟子's imitation of sacrifice rituals will harm him, not because he has not been studying.
- mengmu_samples#13: “孟子跟他的朋友老是去墓地祭拜，害得他的妈妈很生气紧张。” — The required story has 孟子 imitate sacrifice rituals; it does not include friends going with him to the graveyard.
- mengmu_samples#13: “所以孟子的妈妈搬家很安全很安静的公寓。” — The first new neighborhood in the required story is near the market, not a safe and quiet apartment.
- mengmu_samples#14: “孟子的妈妈有她的道理，不是房租太贵了，就是地方太吵了。” — 孟母 moves away from the graveyard because she is worried that 孟子 copying sacrifices will affect him badly, not because of rent or noise.
- mengmu_samples#14: “孟母老是搬家，她搬家搬了三次了。” — The required story describes two moves: from the graveyard neighborhood to the market neighborhood, then from the market to near a school.
- mengmu_samples#15: “妈妈以为他老是在墓地玩，觉得害得孟子的身体，所以妈妈跟孟子一起搬家。” — This says 孟母 thought 孟子 was playing in the graveyard and harming his body. In the story, she worried that his imitation of sacrifices would negatively affect him.
- mengmu_samples#16: “他妈妈就让他搬去城市。” — 孟母 moves to the neighbourhood near the market, not simply to a city.
- mengmu_samples#17: “孟子的妈妈搬了三次家。” — The required story describes two moves: from the graveyard area to the market area, then from the market area to the school area.
- mengmu_samples#19: “在城市里的时候，孟子老是乱跑，在马路上马虎地玩，害得他的妈妈很紧张。” — After the first move, 孟子 should imitate buying and selling near a market, rather than mainly run and play in the street.
- mengmu_samples#19: “孟子的妈妈怕孟子会受到别的小孩子的影响，所以她带孟子到一个城市搬家了。” — 孟母 moved because she thought 孟子's imitation of sacrifices would harm him, not because of other children.
- mengmu_samples#19: “所以他们到城市的外边搬家了。” — The next move should be from the market neighborhood to the neighborhood near a school, not to the outskirts of a city.
- mengmu_samples#20: “不是因为他们很喜欢旅行，而是因为他们每次搬家都找不到好工作，害得他们需要再搬家。” — The moves were not all caused by difficulty finding work. The first move was because 孟母 worried that copying sacrifice rituals would negatively affect 孟子.
- mengmu_samples#20: “在这儿，他们卖日用品” — The story says 孟子 imitated buying and selling near the market, rather than saying that they sold household goods as their work.
- mengmu_samples#20: “害得孟子才九岁的时候，他的妈妈选择搬家来找到比较好的工作。” — 孟母's first decision to move was not to find a better job; it was because she thought the sacrifice imitation would harm 孟子.
- mengmu_samples#20: “这儿，孟子和孟母从早到晚都在墓地帮别人祭拜他们的死家人” — In the story, 孟子 imitates the sacrifice rituals; he and 孟母 do not work at the cemetery helping people worship their dead relatives.
- mengmu_samples#22: “孟母一看孟子祭拜，就觉得孟子学哲学最重要。” — 孟母 should think that imitating sacrifices may have a bad impact on 孟子, not that it is most important for him to study philosophy.
- mengmu_samples#22: “孟母老是搬家，所以孟子会跟别的教授学哲学。” — The story has two specific moves, ending near a school, and does not include 孟子 studying with other professors.
- mengmu_samples#23: “在新家，一直去墓地吃祭品。” — After the move, they live near the market and 孟子 imitates buying and selling, rather than continuing to go to the graveyard to eat offerings.
- mengmu_samples#23: “孟子妈妈说，哎呀，你从早到晚去墓地吃祭品，所以他们要搬家。” — 孟母 moves because 孟子 is copying sacrifice rituals and she worries about its effect on him, not because he is eating offerings.
- mengmu_samples#23: “孟子是淘气的孩子，因为老是去墓地吃祭品。” — In the story, 孟子 imitates how people offer sacrifices; he does not go to eat the offerings.
- mengmu_samples#26: “孟子很聪明，不是学习害得，而是常常搬家，难怪他不喜欢常常学习。” — The story has two specific moves, not constant moving that makes 孟子 dislike studying.
- mengmu_samples#26: “孟母觉得孟子不喜欢他的小的城，所以她和孟子搬家。” — 孟母 moves because she is worried that copying sacrifices will negatively affect 孟子, not because he dislikes the small city.
- mengmu_samples#26: “孟母觉得学习害得孟子，所以孟子常常玩玩。” — 孟母 moves 孟子 near a school so that he begins studying; she does not think studying harms him.
- mengmu_samples#27: “他们老是搬家，不是因为他们喜欢搬家，而是因为他们没有很多钱，害得孟子的妈妈一直需要找工作。” — The moves were not caused by poverty or 孟母 needing work; she moved because she was concerned about the influences on 孟子.
- mengmu_samples#27: “孟子才三岁开始搬家，以后每年搬家。” — The story has the family move from the graveyard area to the market area, then from the market area to the school area, not move every year.
- mengmu_samples#27: “比方说，村民教他写书法，在墓地祭拜，等等。” — In the story, 孟子 imitates the sacrifice rituals he sees near the graveyard; the villagers do not teach him this as a lesson.
- mengmu_samples#29: “孟子的妈妈一共搬了三次家。” — In the required story, 孟母 moves twice: first from the graveyard area to the market area, then from the market area to the school area.
- mengmu_samples#30: “孟子不是跟朋友玩，就是在家学习。” — This says his activities were only playing with friends or studying at home, but the story says he imitated sacrifices near the graveyard.
- mengmu_samples#30: “孟子的妈妈说每天跟朋友见面害得他学习不怎么样。” — In the story, 孟母 is worried that imitating sacrifices will have a bad impact on 孟子, not that meeting friends harms his studies.
- mengmu_samples#31: “可是搬才三次就找到好的地方。” — The required story has two moves: from the graveyard area to the market area, then from the market area to the school area, not three moves.
- mengmu_samples#34: “孟子在那儿很忙，不是画画儿，而是祭拜。” — 孟子 imitates sacrifices while living near the graveyard, not after moving to a temple.
- mengmu_samples#34: “孟子才一岁的时候，他们先搬到了村庄，在那里生活五年后，他们搬到了街上，孟母才找到工作了，所以他们最后搬到了寺庙。” — The story has them first living near a graveyard, then moving near a market, and finally moving near a school. The moves are caused by 孟母 noticing what 孟子 imitates, not by finding a job.
- mengmu_samples#34: “孟子长大了以后成为一名画家，因为他画画儿很厉害。” — 孟子 grows up to become a famous philosopher, not a painter.
- mengmu_samples#35: “最后，他们在农村上住。” — The final move in the story is to a neighborhood near a school, not to the countryside.
- mengmu_samples#36: “他的妈妈老是告诉他，他不能跟别的孩子玩儿。” — The required story does not say that 孟母 forbade 孟子 from playing with other children.
- mengmu_samples#36: “古代的时候有一个男人叫孟子。” — 孟子 is introduced as a man, but the story begins when he is a child living with 孟母.
- mengmu_samples#36: “孟子一直不开心，可是他很聪明。” — The required story does not say that 孟子 was always unhappy.
- mengmu_samples#37: “但是什么时候都太吵了。” — The reason for leaving the market neighborhood is that 孟子 imitated buying and selling there, not that it was always too noisy.
- mengmu_samples#37: “但是孟子一直哭了。” — The story says 孟子 imitated offering sacrifices near the graveyard, not that he kept crying.
- mengmu_samples#37: “孟子学习很难” — The story says 孟子 began to study after moving near the school; it does not say that studying was difficult.
- mengmu_samples#38: “他们一直在搬家，因为孟母的工资很低。” — The moves in the story are not because of 孟母's low wages; the first move happens because she worries that copying sacrifices will harm 孟子.
- mengmu_samples#38: “他们早上六点半去老板的墓地打工。” — They do not go to an employer's graveyard to work in the story; they live near a graveyard at the beginning.
- mengmu_samples#38: “有一天，孟母找到一个打工，在墓地做祭拜。” — In the story, 孟母 does not get a job performing sacrifices at the graveyard; 孟子 copies people offering sacrifices there.
- mengmu_samples#38: “现在孟子和孟母不是打算搬家，而是打算待在这个小镇。” — 孟母 does move the family away from the graveyard and later away from the market in the story.
- mengmu_samples#40: “孟子说我不是不想学哲学，而是住在墓地的旁边太吵了。” — The reason for leaving the graveyard is 孟母's worry that 孟子 copying sacrificial offerings will harm him, not noise from the graveyard.
- mengmu_samples#40: “很多孩子去孟子妈妈的家，所以他们祭拜，结果孟子常常玩游戏跟孩子。” — In the story, 孟子 copies the sacrificial offerings near the graveyard; he is not described as responding by playing games with the children.
- mengmu_samples#43: “她跟孟子搬家去墓地做祭拜” — 孟子 and 孟母 already lived near the graveyard at the start; 孟母 later moved away from it. Also, the story says 孟子 copied sacrificial offerings, rather than both of them going there to perform them.
- mengmu_samples#50: “他现在是当医生，他能帮很多人。” — 孟子 becomes a famous philosopher, not a doctor.
- mengmu_samples#50: “她的妈妈已经搬家很多次，差不多十次。” — In the story, 孟母 makes the two moves described: first from the graveyard area to the market area, then from the market area to the school area.
- mengmu_samples#50: “孟子的妈妈觉得她得搬家，因为现在在他们的省，在中国不太安全。” — 孟母 moves because she is worried that copying sacrifice offerings will harm 孟子, not because the area is unsafe.
- mengmu_samples#50: “难怪她想搬家，因为如果她搬家，她会工作少，和她也会做她最喜欢的兴趣爱好。” — This gives work and hobbies as her reason for moving, rather than concern about the effect of 孟子 copying sacrifice offerings.
- mengmu_samples#51: “他们搬家三次以后，孟母找到了一位老师。” — The required story has a move from the graveyard to the market and then from the market to the school neighbourhood, not three moves; the key result is the school neighbourhood, not 孟母 finding a teacher.
- shennong_samples#1: “一吃夹竹桃就死，这就要看你也吃不吃灵芝了。” — In the story, 神农 faints after eating 夹竹桃; he does not die from it.
- shennong_samples#3: “神农一看他们就知道他们吃的植物里面有毒，” — This conflicts with the story situation that people did not know which plants were safe to eat, which is why 神农 needed to investigate them.
- shennong_samples#5: “他每次生病，因为别的人正好在他的旁边，所以他没死。” — The story says that a person gives 神农 灵芝 and he feels better after eating it; people being nearby is not what saves him.
- shennong_samples#5: “毒他吃很多次，比方说，他吃了灵芝和夹竹桃。” — This presents 灵芝 as one of the poisonous plants 神农 tried. In the story, he tries 夹竹桃, then later receives 灵芝 as the remedy.
- shennong_samples#6: “夹竹桃的解毒剂是灵芝。” — This reverses the story's event: 神农 eats 夹竹桃 and faints, while 灵芝 is what makes him feel better; 夹竹桃 is not an antidote.
- shennong_samples#9: “男人问他，神农，什么植物可以吃？” — This appears to make the conversation happen with the first man who helped 神农, but the required story has another person come by for the conversation.
- shennong_samples#10: “可是他不知道灵芝是药。所以他一吃，肚子就疼死了。” — After eating 灵芝, the story says 神农 feels better, not that he gets stomach pain.
- shennong_samples#10: “夹竹桃有毒，但是他们不知道这个花有毒，所以肚子疼死了。” — After trying 夹竹桃, the story says 神农 faints, not that he has stomach pain.
- shennong_samples#11: “所以神农吃了，一吃就生病。” — In the story, 神农 eats 灵芝 after a visitor gives it to him, and he feels better rather than becoming sick.
- shennong_samples#11: “正好看到了毒植物，特别是灵芝和夹竹桃。” — This says that 灵芝 is poisonous, but 灵芝 makes 神农 feel better in the story.
- shennong_samples#14: “所以他爬山找解药。” — This gives a different purpose for his mountain journey: in the required story, he climbs mountains to test plants and learn which ones are safe to eat.
- shennong_samples#15: “他一吃就病了” — In the story, 神农 faints after eating 夹竹桃; he is not only described as becoming sick.
- shennong_samples#16: “他一吃就生病了。” — After eating 夹竹桃, 神农 faints in the story, rather than merely becoming sick.
- shennong_samples#16: “正好他的旁边有灵芝” — 灵芝 is given to 神农 by a person in blue; it is not simply already beside him.
- shennong_samples#17: “夹竹桃找到了灵芝，他给神农。” — 夹竹桃 is a plant, not a person who can find 灵芝 and give it to 神农.
- shennong_samples#17: “神农的肚子疼死了，所以他的朋友夹竹桃帮他。” — The story says 神农 faints after trying the plant 夹竹桃; 夹竹桃 is not his friend who helps him.
- shennong_samples#20: “别的人看到神农疼死了。” — 神农 faints after trying 夹竹桃; he does not die from pain.
- shennong_samples#20: “蓝色衬衫的男人问：”你吃了夹竹桃吗？“” — The later conversation is with another person in brown, not the person in blue.
- shennong_samples#21: “夹竹桃很好吃，也对你的健康有好处。” — This says 夹竹桃 is good for health, but in the required story 神农 faints after trying 夹竹桃.
- shennong_samples#22: “但如果灵芝和夹竹桃一起吃，那就是药了。” — The story says 灵芝 makes 神农 better, while 夹竹桃 makes him faint; it does not say that eating them together makes medicine.
- shennong_samples#22: “只吃灵芝对身体不好，特别是夹竹桃对身体更不好。” — 灵芝 helps 神农 feel better in the story; it is not harmful when eaten alone.
- shennong_samples#22: “这个镇没有药，所以神农的朋友都生病了。” — The story says people often became sick after eating plants whose safety they did not know, not because the town had no medicine.
- shennong_samples#23: “他一喝那杯茶，就疼死了。” — The story says that 神农 faints after trying 夹竹桃; it does not say that he dies from pain.
- shennong_samples#24: “夹竹桃是毒，所以神农的肚子疼死了。” — After trying 夹竹桃, the story says 神农 faints, not that he has severe stomach pain.
- shennong_samples#25: “比方说，他一吃夹竹桃，就生病了。” — The required story says 神农 faints after trying 夹竹桃, not only that he becomes sick.
- shennong_samples#27: “他们给神农灵芝。” — The required story says that one person in blue gives 灵芝 to 神农; it does not say that both people give it.
- shennong_samples#28: “他一吃就毒死了。” — After trying 夹竹桃, 神农 faints; he does not die.
- shennong_samples#34: “但是他也知道毒的植物，特别是夹竹桃比较麻烦。” — This says 神农 already knows that 夹竹桃 is poisonous before he tries it; in the required story, he learns its danger by trying it and fainting.
- shennong_samples#37: “他穿灰色衣服以后，神农发现他朋友的耳朵突然变小了。” — The story says 神农 feels better after eating 灵芝. It does not say the helper's ears become smaller or that the helper changes to gray.
- shennong_samples#37: “他穿蓝色衣服的朋友吃了灵芝。” — The blue person gives 灵芝 to 神农; 神农 is the one who eats it.
- shennong_samples#37: “有一天，他的耳朵变得太重了，神农摔倒在地上。” — In the story, 神农 faints after trying 夹竹桃, not because his ears become too heavy.
- shennong_samples#38: “在中国古代很多人生病了，因为谁都没有药，所以，人山人海死了。” — The story says people became sick after eating plants whose safety they did not know, not because nobody had medicine.
- shennong_samples#38: “所以他去了又空又高的山，可是他没有吃了，因为他怕毒。” — 神农 goes to test different plants, so saying that he does not eat any because he is afraid of poison contradicts this event.
- shennong_samples#39: “他一尝肚子就疼。” — After trying 夹竹桃, the required outcome is that 神农 faints, not just that his stomach hurts.
- shennong_samples#40: “这时，一个穿着蓝色衣服的男人和一个穿着咖啡色的衣服的男人正好一起走过来。” — The brown-clothed person arrives together with the blue-clothed person, but in the required story the blue-clothed person gives 灵芝 first, and then the brown-clothed person comes by.
- shennong_samples#41: “吃了这个花儿以后，神农的肚子疼得受不了。” — After trying 夹竹桃, the story says that 神农 faints; severe stomach pain replaces that outcome.
- shennong_samples#41: “过几个分钟，一个穿紫色的男孩儿看到了神农” — The later person is described as wearing brown in the required story, not purple.
- shennong_samples#45: “可是一吃就肚子疼，难受得不得了。” — After eating 夹竹桃, 神农 faints in the story.
- shennong_samples#45: “所以他决定去山上找什么植物很好吃。” — 神农's purpose in the story is to find which plants are safe to eat and which are not, not to find plants that taste good.
- shennong_samples#45: “神农说：我吃坏肚子了。” — By the time the brown-clothed person arrives, 神农 has eaten 灵芝 and feels better in the story.
- shennong_samples#46: “可是花瓣有毒，所以他的头疼死了。” — This replaces the story outcome: after trying 夹竹桃, 神农 faints rather than having a severe headache or dying.
- shennong_samples#47: “后面这就是老板最好的菜，叫香毒菇蘑。” — The story does not say that 夹竹桃 and 灵芝 become a dish; 夹竹桃 is poisonous, while 灵芝 is recorded as a helpful plant.
- shennong_samples#47: “如果跟蘑菇一样的植物，做饭可以，没再有毒了。” — 灵芝 makes 神农 feel better; it does not make 夹竹桃 no longer poisonous.
- shennong_samples#47: “有一位餐馆的老板决定世界旅行找新植物做饭。” — The person in the story is 神农, not a restaurant owner.
- shennong_samples#48: “爬山前，他们吃了很多植物，神农的儿子王朋吃了夹竹桃，就开始肚子疼。” — 王朋 is not part of the required story. This also changes the event: 神农, not his son, tries 夹竹桃, and 神农 faints rather than getting a stomach ache.
- shennong_samples#52: “紫色人告诉他：你吃了灵芝，一吃就你的身体最好的。” — The second visitor is described as purple, but in the required story this visitor wears brown.

## Example learner feedback (run 1, first 6 stories)

**mengmu_samples#1**
- At the beginning, add that 孟子 and 孟母 lived near the graveyard, and that he copied sacrifice rituals there.
- After the sacrifices, say that 孟母 moves away from the graveyard because she worries this copying will harm 孟子.
- Between leaving the graveyard and moving near the school, add the move near the market and 孟子 copying buying and selling.
- After the market scene, add that they move near a school, where 孟子 begins studying every day.

**mengmu_samples#2**
- After 孟子 imitates sacrifices near the graveyard, add that 孟母 worries this will affect him badly and decides to move away.
- After leaving the graveyard, add that they move near the market and 孟子 imitates buying and selling there.
- After the market part, add that 孟母 moves them near a school before 孟子 begins to study.
- At the end, say that 孟子 becomes a famous philosopher.

**mengmu_samples#3**
- Near the first home by the graveyard, add that 孟子 copied how people offered sacrifices.
- After 孟子 copied sacrifices by the graveyard, explain that 孟母 moved because she feared this would harm him.
- After leaving the graveyard, add that they moved near the market, where 孟子 copied buying and selling.
- Before 孟子 studies hard, add that they moved from the market to live near a school.

**mengmu_samples#5**
- At the beginning, before 孟母 decides to leave the graveyard area, add that 孟子 copied people offering sacrifices there.
- After they leave the graveyard and before they move again, say that they live near a market and 孟子 copies buying and selling.
- When they arrive at the third home, add that it is near a school before 孟子 starts studying.
- At the end, say that 孟子 becomes a famous philosopher.

**mengmu_samples#6**
- At the beginning, add that 孟子 and 孟母 lived near a graveyard and 孟子 copied sacrifice offerings.
- After the graveyard scene, add that 孟母 chose to move because she thought the sacrifice imitation would harm 孟子.
- Before they find the learning environment, add that they moved near a market and 孟子 copied buying and selling.
- When they find the good learning environment, say it was near a school and that they had moved there from the market.
- At the end, say that 孟子 became a famous philosopher.

**mengmu_samples#7**
- At the beginning, add that 孟子 and 孟母 live near a graveyard and 孟子 copies sacrificial offerings.
- After 孟子 copies sacrifices near the graveyard, add that 孟母 decides to move away from there.
- After leaving the graveyard, add that they move near a market and 孟子 copies buying and selling.
- Before 孟子 studies with his teacher, say that they move from the market to a neighbourhood near a school.
- At the end, add that 孟子 becomes a famous philosopher.

