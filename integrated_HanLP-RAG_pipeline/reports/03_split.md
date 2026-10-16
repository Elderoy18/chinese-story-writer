# Step 3 report: test / train split

10 test samples per story (mengmu_san_qian, shennong_chang_baicao), including the first pipeline's 6.
Everything else -- including all Pear Story samples -- is train.

## Are test and train alike?

| Story | Set | Samples | Avg characters | Avg feedback lines | Characters per feedback line | With a missing-scene flag |
|---|---|---|---|---|---|---|
| mengmu_san_qian | test | 10 | 234 | 8.5 | 27.6 | 9 |
| mengmu_san_qian | train | 41 | 214 | 7.7 | 27.9 | 34 |
| shennong_chang_baicao | test | 10 | 270 | 9.9 | 27.2 | 10 |
| shennong_chang_baicao | train | 42 | 246 | 7.8 | 31.7 | 36 |

(Characters per feedback line is a rough measure of how error-dense a story is: lower = more errors.)

## Test samples

| Sample | In first pipeline's test | Feedback lines | Scenes (characters) |
|---|---|---|---|
| mengmu_samples#4 |  | 12 | 96, 79, 84 |
| mengmu_samples#10 | yes | 5 | 83, 82, 74 |
| mengmu_samples#12 |  | 9 | 82, 65, 66 |
| mengmu_samples#18 |  | 5 | 110, 82, 73 |
| mengmu_samples#25 |  | 7 | 58, 55, 17 |
| mengmu_samples#32 | yes | 15 | 118, 94, 105 |
| mengmu_samples#33 |  | 7 | 92, 104, 79 |
| mengmu_samples#39 |  | 11 | 109, 63, 83 |
| mengmu_samples#45 | yes | 7 | 84, 57, 60 |
| mengmu_samples#47 |  | 7 | 65, 84, 40 |
| shennong_samples#4 |  | 10 | 162, 134, 136 |
| shennong_samples#8 | yes | 6 | 77, 60, 60 |
| shennong_samples#12 |  | 7 | 84, 98, 67 |
| shennong_samples#18 |  | 9 | 82, 78, 79 |
| shennong_samples#19 | yes | 8 | 59, 66, 51 |
| shennong_samples#26 |  | 13 | 92, 91, 76 |
| shennong_samples#33 | yes | 9 | 74, 92, 53 |
| shennong_samples#35 |  | 14 | 127, 94, 101 |
| shennong_samples#42 |  | 12 | 120, 92, 62 |
| shennong_samples#49 |  | 11 | 126, 102, 101 |

## Scene split example: mengmu_samples#4

- Scene 1: 古代的时候，孟子和孟母住了在靠墓地的家。孩子才五岁就每天在墓地祭拜了。在那个城市，孟母从早到晚都找工作，可是找不到，害得孟母没有钱。难怪她跟孩子搬家，原来买不了房。他们搬了到别一个城市找工作。
- Scene 2: 这个城市老是很吵，不是人吵架，就是都叫，害得孟子一直不能睡觉。在那儿，孟母也找不到工作。孟子和妈妈要又一个次搬了家。在第三个城市，孟母找到工作，在商店做衣服。
- Scene 3: 孟子在那个商店也找了到工作，可是不是做衣服的工作，而是喜欢的工作。孟子学习馆学了十五年，他的学习和他的旅行经验很重要，对他很多好处。他是大人的时候，他成为很有名的哲人。
