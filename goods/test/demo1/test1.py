import numpy as np
import os
files_features = {}
template_features = {}
def  get_feature (good_upc,file_feature):
    img_features = {}
    with open(file_feature, 'r') as f:
        lines = f.readlines()
        for line in lines:
            feature = line.split(",")
            filename = feature[0]
            feature = feature[1:]
            feat = []
            for fea in feature:
                feat.append(float(fea))
            # print (len(feat))
            featArr = np.array(feat)
            featArr.resize(512, 7)
            f1s = []
            for f1 in featArr:
                f1s.append(np.sum(f1))
            img_features[filename] = f1s
        files_features[good_upc] = img_features
#E:\opt\data\step2_all_feature
def  get_all_goods_feature(feature_path):
    for feature_file in os.listdir(feature_path):
        feature_file_path = os.path.join(feature_path,feature_file)
        good_upc = feature_file.strip(".txt")
        get_feature(good_upc,feature_file_path)

def get_template_feature(template_dir_path):
    for good_upc in os.listdir(template_dir_path):
        tempalte_feature_path = os.path.join(template_dir_path,good_upc)
        template_feature = {}
        for template_file in os.listdir(tempalte_feature_path):
            for key in files_features:
                if good_upc == key:
                    template_feature[template_file] = files_features[good_upc][template_file]
        template_features[good_upc] = template_feature

# def windows_main(dis_socre = 0.1250):
#
#     feature_path = "E:\\opt\\data\\step2_all_feature\\"
#     template_dir_path = "E:\\opt\\data\\step2_all\\step_small_template\\"
#     get_template_feature(template_dir_path)
#     get_all_goods_feature(feature_path)
#     tp = 0
#     sum = 0
#     for good_upc1 in files_features:
#         sum += 1
#         for good_upc2 in template_features:
#
