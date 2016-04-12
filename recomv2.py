
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
    ratings = {}
    return ratings[0:k_neighs]

'''
基于用户相似度，返回k_neighs最近邻用户
'''
def calculate_sim_user(user_prefs,user,k_neighs):
    ratings = {}
    return ratings[0:k_neighs]

'''
用item_cf生成topN推荐列表
'''
def rec_by_item_cf(user_prefs,user,topN=10):
    rec={}
    return rec[0:topN]

'''
用user_cf生成topN推荐列表
'''
def rec_by_user_cf(user_prefs,user,topN=10):
    rec={}
    return rec[0:topN]

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

