__author__ = 'admin'
# *_*coding:utf-8 *_*
import numpy as np
import os
from goods.util import distance_util

def  get_feature(img_feature_path):
    img_features = {}
    with open(img_feature_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            feature = line.split(",")
            filename = feature[0]
            feature = feature[1:]
            feat = []
            for fea in feature:
                feat.append(float(fea))
            img_features[filename] = feat
    return img_features


#计算多个商品之间的类间距
def outside_distance(img_feature_path1,img_feature_path2,out_side_path):
    img_features1 = get_feature(img_feature_path1)
    img_features2 = get_feature(img_feature_path2)
    img_dis = {}
    for img_feature1 in img_features1:
        for img_feature2 in img_features2:
            print(len(img_features1[img_feature1]))
            print(len(img_features2[img_feature2]))
            dis = distance_util.pdos(img_features1[img_feature1], img_features2[img_feature2])
            img_dis[img_feature1 + "---" + img_feature2] = dis
            print(img_feature1 + "---" + img_feature2, str(dis))
    a = sorted(img_dis.items(), key=lambda x: x[1], reverse=True)
    print(a)
    with open(out_side_path, 'w') as f:
        for key in a:
            f.write(key[0] + "," + str(float(key[1])))
            f.write("\n")

if  __name__=='__main__':
    img_feature_path1 = "E:\\opt\\data\\feature_top\\69024894.txt"
    img_feature_path2 = "E:\\opt\\data\\feature_top\\69029097.txt"
    img_dis_path = "E:\\opt\\data\\feature_top\\step2_outside_dos\\69024894-69029097.txt"
    outside_distance(img_feature_path1,img_feature_path2,img_dis_path)

