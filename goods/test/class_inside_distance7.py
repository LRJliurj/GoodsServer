__author__ = 'admin'
# *_*coding:utf-8 *_*
import numpy as np
import os
from goods.util import distance_util

import sys
np.set_printoptions(suppress=True)
np.set_printoptions(threshold=sys.maxsize)
vgg19=(7,512)
#计算单个商品类内差异值
def inside_distance(img_feature_path,img_dis_path):
   img_features = {}
   with open(img_feature_path,'r') as f:
       lines = f.readlines()
       for line in lines:
           feature = line.split(",")
           filename = feature[0]
           if "train_augment0" not in filename:
               continue
           feature = feature[1:]
           feat = []
           for fea in feature:
            feat.append(float(fea))
           # print (len(feat))
           featArr = np.array(feat)
           featArr.resize(512,7)
           f1s = []
           for f1 in featArr:
               f1s.append(np.sum(f1))

           img_features[filename] = f1s



   img_dis={}
   for img_feature1 in img_features:
        for img_feature2 in img_features:
            dis = distance_util.pdis(img_features[img_feature1],img_features[img_feature2])
            img_dis[img_feature1+"---"+img_feature2] = dis
            print (img_feature1+"---"+img_feature2,str(dis))
   a = sorted(img_dis.items(), key=lambda x: x[1], reverse=True)

   with open(img_dis_path,'w') as f:
    for key in a:
        f.write(key[0]+","+str(float(key[1])))
        f.write("\n")


if  __name__=='__main__':
    # 布雷柯蒂斯距离
    img_feature_path = "E:\\opt\\data\\step2_all_feature\\69024894.txt"
    img_dis_path = "E:\\opt\\data\\feature_no_top\\step2_inside_dis7\\69024894.txt"
    inside_distance(img_feature_path,img_dis_path)

    #欧式距离
    # img_feature_path = "E:\\opt\\data\\step2_all_feature\\69024894.txt"
    # img_dis_path = "E:\\opt\\data\\step2_inside_dos7\\69024894.txt"
    # inside_distance(img_feature_path,img_dis_path)

    #余弦距离
    # img_feature_path = "E:\\opt\\data\\step2_all_feature\\69024894.txt"
    # img_dis_path = "E:\\opt\\data\\step2_inside_cos7\\69024894.txt"
    # inside_distance(img_feature_path,img_dis_path)
