__author__ = 'admin'
# *_*coding:utf-8 *_*
import numpy as np
import json
np.set_printoptions(suppress=True)#不用科学计数法输出 numpy
from goods.test.net.nettop import Feature
import os
import cv2
feature = Feature()
def predict (net_name,step2_path,feature_path):
    for goods_path in os.listdir(step2_path):
        good_path = os.path.join(step2_path,goods_path)
        with open(goods_path + ".txt", "w") as f:
            for img_file in os.listdir(good_path):
                img_file_path = os.path.join(good_path,img_file)
                feat = feature.get_feature_by_net(net_name,img_file_path)
                # print (feat)
                featArr = feat[0]
                ft = ''
                ft = ft +img_file
                for fe in featArr:
                     ft  = ft + "," + str(float(fe))
                f.write(ft)
                f.write("\n")


def linux_main():
    net_name = 'vgg19'
    step2_path = '/home/ai/ai_data/step2/'
    feature_path = "/home/ai/ai_data/step2_feature/"
    predict(net_name, step2_path, feature_path)

def windows_main():
    net_name = 'vgg19'
    step2_path = 'E:\\opt\\data\\step_2_1\\'
    feature_path = "E:\\opt\\data\\step2_feature\\"
    predict(net_name, step2_path, feature_path)

if __name__=='__main__':
    windows_main()

