# -*- coding: utf-8 -*-
from utils.utils import transformPrefs

def euclidean(prefs,person1,person2):
    return None

'''
person_sim = (EXY-EXEY)/(EX^2-(EX)^2)*(EY^2-(EY)^2)
'''
def person_sim(prefs,person1,person2):
    # 共同评分数
    common_items = []
    for item in prefs[person1]:
        if item in prefs[person2]:
            common_items.append(item)
    
    # 如果共同评分数为0，则相似度为0，返回
    n = len(common_items)
    if n==0:
        return 
    
    # 根据变形的person similarity计算
    X = [prefs[person1][item] for item in common_items]
    Y = [prefs[person2][item] for item in common_items]
    EXsq = sum(pow(X,2))/n
    EYsq = sum(pow(Y,2))/n
    EX = sum(X)/n
    EY = sum(Y)/n

    XY = [X[i]*Y[i] for i in range(n)]
    EXY = sum(XY)/n
    num = EXY - EX*EY
    den = (EXsq-EX*EX)*(EYsq-EY*EY)
    return  num/den


'''
基于物品相似度，返回中k_neighs最近邻物品
'''
def calculate_sim_item(item_prefs,item,k_neighs):
    ratings = [(person_sim(item_prefs,item,other),other)
                        for other in item_prefs if item!=other]
    ratings.sort()
    ratings.reverse()
    return ratings[0:k_neighs]

'''
基于用户相似度，返回k_neighs最近邻用户
'''
def calculate_sim_user(user_prefs,user,k_neighs):
    # ratings = {}
    # for other in user_prefs:
    #     sim = person_sim(user_prefs,user,other)
    #     ratings.setdefault(other,0)
    #     ratings[other] = sim
    # ret = [(sim,other) for other,sim in ratings.items()]
    #ret = [(other,person_sim(user_prefs,user,other) for other in user_prefs if user!=other)]
    ret = [(person_sim(user_prefs,user,other),other)
                    for other in user_prefs if user!=other]
    ret.sort()
    ret.reverse()
    return ret[0:k_neighs]

'''
用item_cf生成topN推荐列表
'''
def rec_by_item_cf(user_prefs,user,topN=10):
    user_ratings = user_prefs[user].items()
    rec={}
    # 遍历user已评分的电影
    for (item,rating) in user_ratings:
        # 返回item的10个最近邻
        neighs = calculate_sim_item(transformPrefs(user_prefs),item,10)
        # 遍历相似电影并计算其评分
        for sim,neigh_item in neighs:
            #排除已购物品
            if neigh_item in user_ratings:continue
            rec.setdefault(neigh_item,0.0)
            rec[neigh_item] += sim*rating
    scores = [(score,item) for item,score in rec.items()]
    scores.sort()
    return scores[-topN:]

'''
用user_cf生成topN推荐列表
'''
def rec_by_user_cf(user_prefs,user,topN=10):
    rec={}
    # 返回10个最近邻
    neighs = calculate_sim_user(user_prefs,user,10)
    # 遍历neighs
    for (sim,neigh) in neighs:
        # 遍历user评分过的电影
        for item in user_prefs[neigh]:
            # 排除已评分电影
            if item in user_prefs[user]:continue
            rec.setdefault(item,.0)
            rec[item]+=sim*user_prefs[neigh][item]
    scores = [(score,item) for item,score in rec.items()]
    scores.sort()
    scores.reverse()
    # simple way
    # from operator import itemgetter
    # scores = sorted(rec.items(),key=itemgetter(1))
    return scores[-topN:]

'''
为用户推荐哪些书？
'''
def user_cf(user_prefs,user,topN=10):
    rec={}
    return rec[0:topN]

'''
根据Item-based-cf用户对新书的评分是多少？
'''
def rating_item_based_cf(user_prefs,user,item):
    rating = 0.0
    return rating

'''
根据User-based-cf用户对新书的评分是多少？
'''
def rating_user_based_cf(user_prefs,user,item):
    rating = 0.0
    return rating

