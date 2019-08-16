__author__ = 'admin'
# *_*coding:utf-8 *_*
import numpy as np
import os
from goods.util import distance_util

#计算多个商品之间的类间距
def outside_distance(img_feature_path,class_distance_path):
    goods_feature_distance = {}
    goods_feature = {}
    for img_feature_file in os.listdir(img_feature_path):
        img_feature = np.loadtxt(os.path.join(img_feature_path,img_feature_file))
        for feature in img_feature:
            goods_feature[img_feature_file+"##"+feature] = img_feature[feature]
    for key1 in goods_feature:
        x = goods_feature[key1]
        for key2 in goods_feature:
            y = goods_feature[key2]
            key_tag1 = key1+"##"+key2
            key_tag2 = key2+"##"+key1
            if key_tag1 not in goods_feature_distance and key_tag2 not in goods_feature_distance:
                distance = distance_util.pdistance(x,y)
                goods_feature_distance[key1+"##"+key2] = distance
        sorted(goods_feature_distance.items(), key=lambda d: d[1])
        dis_file = os.path.join(class_distance_path)
        if os.path.isfile(dis_file):
            os.remove(dis_file)
        with open(dis_file,'w') as f:
            for feature_key in goods_feature_distance:
                f.write(feature_key+","+goods_feature_distance[feature_key]+"\n")