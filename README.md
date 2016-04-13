# DIY-RecommedationSystem
 
##Goal
These best way to learn a recommedation is DIY

##Algorithms
###Item-basedCF:
Item-basedCF主要由两步组成：1）计算物品之间的相似性。2）根据物品的相似度和用户的历史行为产生推荐列表。
###存在的问题
* 推荐列表热门商品过多，覆盖度指标不高，长尾发掘能力差。细致的覆盖度指标通过信息熵来定义。解决的办法是计算相似度的时候，加大对热闹物品的惩罚。
* 不同邻域的热闹物品之间往往有很高的相似性。比如父母每天都会看新闻联播和中央八套的电视剧。



###User-basedCF
User-baseCF主要由两步组成：1）找到跟用户兴趣相同的用户。2）找到这个群体中用户喜欢的且没有听说的物品产生推荐列表。

###User-basedCF vs. Item-basedCF
以新浪的新闻推荐使用User-basedCF和当当的图书推荐使用的Item-basedCF为例
* ItemCF反映的是用户的历史兴趣，因此更加个性化；UserCF反映的是社群中物品的热门程度，因此更加热点化。

##Evaluation
###TopN推荐列表的评价指标
* Precision
* Recall

##Usage:
python command line


# Slope-one
## 感受
* 手动的计算过程到编码过程还是有差别的。
* 弄清楚数据结构非常重要
* 花了半天时间去实现，还是挺有成就感的，给自己实现算法增加了点信心。
