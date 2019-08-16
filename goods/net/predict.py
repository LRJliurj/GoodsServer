__author__ = 'admin'
# *_*coding:utf-8 *_*
import numpy as np
from goods.net.net import Feature
import os
import cv2
def predict (net_name,step2_path,feature_path):
    for goods_path in os.listdir(step2_path):
        good_path = os.path.join(step2_path,goods_path)
        img_features = {}
        for img_file in os.listdir(good_path):
            img_file_path = os.path.join(good_path,img_file)
            feature = Feature.get_feature_by_net(net_name,img_file_path)
            img_features[img_file] = feature
            np.savetxt(net_name+"_"+goods_path,img_features)


if __name__=='__main__':
    net_name = 'nasnet'
    step2_path = '/home/ai/data/step2/'
    feature_path = "/home/ai/data/step2/"
    predict(net_name,step2_path)

