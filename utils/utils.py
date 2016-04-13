# -*- coding: utf-8 -*-

# 反转User-Item，提高计算jaccard,cosine 相似度公式中的分子。
def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      result[item][person]=prefs[person][item]
  return result