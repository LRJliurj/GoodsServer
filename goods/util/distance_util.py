__author__ = 'admin'
# *_*coding:utf-8 *_*
#https://www.cnblogs.com/denny402/p/7028832.html
from scipy.spatial.distance import pdist
import numpy as np
#布雷柯蒂斯距离
def pdistance(x,y):
    x = np.asarray(x)
    y = np.asarray(y)
    X=np.vstack([x,y])
    d2=pdist(X,'braycurtis')
    return d2

#余弦距
def pcos(x,y):
    x = np.asarray(x)
    y = np.asarray(y)
    X=np.vstack([x,y])
    d2=1-pdist(X,'cosine')

#欧式距离
def pdist(x,y):
    x = np.asarray(x)
    y = np.asarray(y)
    X = np.vstack([x, y])
    d2 = pdist(X)