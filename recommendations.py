#用户-电影评分数据
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


from math import sqrt

'''
欧拉相似性度量
'''
def sim_distance(prefs,person1,person2):
  # 共同评分电影
  si={}
  for item in prefs[person1]: 
    if item in prefs[person2]: si[item]=1

  # 没有共同评分的电影
  if len(si)==0: return 0

  # 计算欧拉距离
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                      for item in prefs[person1] if item in prefs[person2]])
  # 计算Euclidean
  sum_of_squares2 = sum([pow(prefs[person1][item]-prefs[person2][item],2)
                          for item in si])
  return 1/(1+sum_of_squares)

'''
计算Pearson correlation 用到的是变形后的公式公式非定义公式，见wiki
https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
'''
def sim_pearson(prefs,p1,p2):
  # 共同评分的电影
  si={}
  for item in prefs[p1]: 
    if item in prefs[p2]: si[item]=1

  # 没有共同的评分，返回
  if len(si)==0: return 0

  # 共同评分的数量
  n=len(si)
  
  # 所有的评分和，EX,EY
  sumX=sum([prefs[p1][it] for it in si])
  sumY=sum([prefs[p2][it] for it in si])

  # EX^2,EY^2
  sumXsq=sum([pow(prefs[p1][it],2) for it in si])
  sumYsq=sum([pow(prefs[p2][it],2) for it in si])
  
  # EXY
  sumXY=sum([prefs[p1][it]*prefs[p2][it] for it in si])
  
  # 分子是EXY-EX*EY,分母是sqrt(E(X^2)-(EX)^2) * sqrt(E(Y^2)-(EY)^2)
  num=sumXY-(sumX*sumY/n)
  den=sqrt((sumXsq-pow(sumX,2)/n)*(sumYsq-pow(sumY,2)/n))
  if den==0: return 0

  r=num/den

  return r


'''
返回最相似的N个邻居
'''
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]
  scores.sort()
  #scores.reverse()
  return scores[-n:]


'''
生成TOP-N推荐，每个邻居所推荐的物品*邻居的权重，推荐score最大的前N个物品。
'''
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    # 排除计算自己跟自己的相关性
    if other==person: continue
    sim=similarity(prefs,person,other)

    # 忽略负相关分数
    if sim<=0: continue
    for item in prefs[other]:
	    
      # 推荐没有看过的电影
      if item not in prefs[person] or prefs[person][item]==0:
        totals.setdefault(item,0)
        # 邻居推荐的Item*邻居的权重
        totals[item]+=prefs[other][item]*sim
        # 相似度和，用于归一化
        simSums.setdefault(item,0)
        simSums[item]+=sim
  # 把dict->tuple list进行排序
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  rankings.sort()
  rankings.reverse()
  return rankings

'''
为person推荐item，根据userCF
'''
def userCFRecommendation(prefs,person,recNum=5,simMeasure=sim_pearson):
  rec = {}
  sumsim = 0.0
  # 用户person的K个最近邻用户,neighs is tuple list
  neighs = topMatches(prefs,person,n=5,similarity=sim_pearson)

  # 遍历neighs
  for tuples in neighs:
    sim = tuples[0]
    user = tuples[1]
    for item in prefs[user]:
      rec.setdefault(item,0)
      rec[item] += sim*prefs[user][item]
      sumsim += sim
  ratings = [(rating/sumsim,item) for (rating,item) in rec.items()]
  ratings.sort()
  return ratings[-recNum:]

# 反转User-Item，提高计算jaccard,cosine 相似度公式中的分子。
def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      result[item][person]=prefs[person][item]
  return result

'''
计算Item相似性，用的特征是Item是否被相同的用户购买
'''
def calculateSimilarItems(prefs,n=10):
  # 找到item的n最近邻
  result={}
  # 反转字典
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores
  return result

'''
基于Item的推荐.根据用户已买物品的N最近邻物品*相应权重
为用户推荐什么书？
'''
def getRecommendedItems(prefs,itemMatch,user):
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # 遍历用户已评分的物品
  for (item,rating) in userRatings.items():

    # 遍历已评分物品的N个最近邻
    for (similarity,item2) in itemMatch[item]:

      # 排除已购物品
      if item2 in userRatings: continue
      # 物品评分*权重
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating
      # 用于归一化
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  rankings=[(score/totalSim[item],item) for item,score in scores.items()]

  rankings.sort( )
  rankings.reverse( )
  return rankings
'''
Item-basedCF
'''
def itemCFRecommendation(prefs,user,nrec=5,similarity=sim_pearson):
  # 返回包含nrec的推荐列表
  rec={}
  # 计算user的k个最近邻
  neighs = topMatches(prefs,user,n=5,similarity=sim_pearson)

  # 遍历neighs
  for tuple in neighs:
    person = tuple[1]
    sim = tuple[0]
    #遍历perfs[person]
    for item in prefs[person]:
      # if item not in rec:
      #   rec[item] = .0
      # else:
      #   rec[item]+=sim*prefs[person][item]
      rec.setdefault(item,.0)
      rec[item]+=sim*prefs[person][item]

  # 把rec转换为tuple list 并排序
  ratings = [(score,item) for item,score in rec.items()]
  ratings.sort()
  return ratings[-nrec:]



'''
用moviedLens data 做测试
'''
def loadMovieLens(path='/data/movielens'):
  movies={}
  for line in open(path+'/u.item'):
    (id,title)=line.split('|')[0:2]
    movies[id]=title
  
  # Load data
  prefs={}
  for line in open(path+'/u.data'):
    (user,movieid,rating,ts)=line.split('\t')
    prefs.setdefault(user,{})
    prefs[user][movies[movieid]]=float(rating)
  return prefs
