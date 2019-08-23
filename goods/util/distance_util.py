__author__ = 'admin'
# *_*coding:utf-8 *_*
#https://www.cnblogs.com/denny402/p/7028832.html
from scipy.spatial.distance import pdist
import numpy as np
#布雷柯蒂斯距离  first  37
def pdis(x,y):
    x = np.asarray(x)
    y = np.asarray(y)
    X=np.vstack([x,y])
    d2=pdist(X,'braycurtis')
    return d2

def pdis2(x,y):
    up = 0
    down = 0
    for x1,y1 in zip(x,y):
        # print (abs(x1-y1))
        down+=x1+y1
        if abs(x1-y1) < 0.4:
            up+= abs(x1 - y1)
        else:
            up += abs(x1 + y1)
    return up/down
#余弦距
def pcos(x,y):
    x = np.asarray(x)
    y = np.asarray(y)
    X=np.vstack([x,y])
    d2=1-pdist(X,'cosine')
    return d2

#欧式距离
def pdos(x,y):
    x = np.asarray(x)
    y = np.asarray(y)
    X = np.vstack([x, y])
    d2 = pdist(X)
    return d2

#皮尔逊相关系数
def ppcs(x,y):
    x = np.asarray(x)
    y = np.asarray(y)
    X = np.vstack([x, y])
    d2 = np.corrcoef(X)[0][1]
    return d2
# 汉明距离
def pphs(x,y):
    x = np.asarray(x)
    y = np.asarray(y)
    X = np.vstack([x, y])
    d2 = pdist(X, 'hamming')
    return d2

# 杰卡德相似系数
def  pjkd(x,y):
    x = np.asarray(x)
    y = np.asarray(y)
    up = np.double(np.bitwise_and((abs(x - y)<0.5),np.bitwise_or(x != 0, y != 0)).sum())
    down = np.double(np.bitwise_or(x != 0.0, y != 0.0).sum())
    d1 = (up / down)
    return d1
