# -*- coding: utf-8 -*-
# Copyright 2016-robin-lai <robin_fj_cn@163.com>.

class SlopeOne(object):
    def __init__(self):
        self.diffs = {}
        #对两部电影做出评分的用户数
        self.freqs = {}

    def predict(self, userprefs):
        preds, freqs = {}, {}
        # 根据用户的现有评分及Item之间的分差来预测的，所以要遍历现有评分
        for item, rating in userprefs.iteritems():
            # diffs里记录的是item1与item1,item2,item3...的分差。预测需要的是计算已评的item跟缺失的item的分差。
            for diffitem, diffratings in self.diffs.iteritems():#此句非常重要，弄清楚是怎么遍历diffs的。
                #print(item,rating)
                try:
                    freq = self.freqs[diffitem][item]
                except KeyError:
                    continue
                preds.setdefault(diffitem, 0.0)
                freqs.setdefault(diffitem, 0)
                preds[diffitem] += freq * (diffratings[item] + rating)#
                freqs[diffitem] += freq#看评分公式，用权重和归一化
        return dict([(item, value / freqs[item])
                     for item, value in preds.iteritems()
                     if item not in userprefs and freqs[item] > 0])

    def update(self, userdata):
        for ratings in userdata.itervalues():
            for item1, rating1 in ratings.iteritems():
                self.freqs.setdefault(item1, {})
                self.diffs.setdefault(item1, {})
                for item2, rating2 in ratings.iteritems():
                    self.freqs[item1].setdefault(item2, 0)
                    self.diffs[item1].setdefault(item2, 0.0)
                    self.freqs[item1][item2] += 1
                    self.diffs[item1][item2] += rating1 - rating2
        # 平均差值，diffs为累计差值
        for item1, ratings in self.diffs.iteritems():
            for item2 in ratings:
                ratings[item2] /= self.freqs[item1][item2]

if __name__ == '__main__':
    #two level dict
    userdata = dict(
        alice=dict(squid=1.0,
                   cuttlefish=0.5,
                   octopus=0.2),
        bob=dict(squid=1.0,
                 octopus=0.5,
                 nautilus=0.2),
        carole=dict(squid=0.2,
                    octopus=1.0,
                    cuttlefish=0.4,
                    nautilus=0.4),
        dave=dict(cuttlefish=0.9,
                  octopus=0.4,
                  nautilus=0.5),
        )

    makedata = {
        'a':{'A':3,'B':2},
        'b':{'C':2,'B':1,'D':4},
        'c':{'A':3,'B':4,'E':3},
        'd':{'D':3,'E':2}
    }
    s = SlopeOne()
    s.update(userdata)
    print s.predict(dict(squid=0.4))

    s.update(makedata)
    print s.predict({'A':3,'B':3})