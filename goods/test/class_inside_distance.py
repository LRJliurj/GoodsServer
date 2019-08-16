__author__ = 'admin'
# *_*coding:utf-8 *_*
import numpy as np
import os
from goods.util import distance_util
#计算单个商品类内差异值
def inside_distance(img_feature_path,class_distance_path):
    for img_feature_file in os.listdir(img_feature_path):
        img_feature = np.loadtxt(os.path.join(img_feature_path,img_feature_file))
        good_feature_distance = {}
        for key1 in img_feature:
            x = img_feature[key1]
            for key2 in img_feature:
                y = img_feature[key2]
                key_tag1 = key1+"##"+key2
                key_tag2 = key2+"##"+key1
                if key_tag1 not in good_feature_distance and key_tag2 not in good_feature_distance:
                    distance = distance_util.pdistance(x,y)
                    good_feature_distance[key1+"##"+key2] = distance
        sorted(good_feature_distance.items(), key=lambda d: d[1])
        dis_file = os.path.join(class_distance_path,img_feature_file)
        if os.path.isfile(dis_file):
            os.remove(dis_file)
        with open(dis_file,'w') as f:
            for feature_key in good_feature_distance:
                f.write(feature_key+","+good_feature_distance[feature_key]+"\n")
