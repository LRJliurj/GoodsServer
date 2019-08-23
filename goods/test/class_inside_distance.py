__author__ = 'admin'
# *_*coding:utf-8 *_*
import numpy as np
import os
from goods.util import distance_util
#计算单个商品类内差异值
def inside_distance(img_feature_path,img_dis_path):
   img_features = {}
   with open(img_feature_path,'r') as f:
       lines = f.readlines()
       for line in lines:
           feature = line.split(",")
           filename = feature[0]
           feature = feature[1:]
           feat = []
           for fea in feature:
            feat.append(float(fea))
           img_features[filename] = feat

   img_dis={}
   for img_feature1 in img_features:
        for img_feature2 in img_features:
            print (len(img_features[img_feature1]))
            print(len(img_features[img_feature2]))
            dis = distance_util.pcos(img_features[img_feature1],img_features[img_feature2])
            img_dis[img_feature1+"---"+img_feature2] = dis
            print (img_feature1+"---"+img_feature2,str(dis))
   a = sorted(img_dis.items(), key=lambda x: x[1], reverse=True)
   print (a)
   with open(img_dis_path,'w') as f:
    for key in a:
        f.write(key[0]+","+str(float(key[1])))
        f.write("\n")


if  __name__=='__main__':
    # 布雷柯蒂斯距离
    img_feature_path = "E:\\opt\\data\\feature_top\\69024894.txt"
    img_dis_path = "E:\\opt\\data\\feature_top\\step2_inside_cos\\69024894.txt"
    inside_distance(img_feature_path,img_dis_path)


