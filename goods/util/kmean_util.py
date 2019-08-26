from set_config import config
import os
import numpy as np
from goods.util.distance_util import pdis
# 线上保存kmean模型获取特征的util,保存后，重新排序
class online_util:
    save_sort_feature_path = config.goods_params['kmean_params']['online']["kmean_predict_features_path"]
    top_n = config.goods_params['kmean_params']['top_n']
    # 获取指定聚类的商品特征
    def get_goods_feature(self,cluter):
        cluter_feature_file = os.path.join(self.save_sort_feature_path,str(cluter)+".txt")
        features = []
        goods_upcs = []
        dises = []
        with open(cluter_feature_file,'r') as f:
            features = f.readlines()
            for feature in features:
                good_upc = feature.split(",")[0]
                dis = feature.split(",")[-1]
                goods_upcs.append(good_upc)
                dises.append(float(dis))
        return features,goods_upcs,dises
    # 获取top_n 商品
    def get_topn_upc(self,cluter,to_cluter_dis,top_n=top_n):
        upcs = []
        features, goods_upcs, dises = self.get_good_feature(cluter)
        cluter_dict = {}
        for i,good_upc,distance in zip(range(len(goods_upcs)),goods_upcs,dises):
            cluter_dict[str(i)+"##"+str(good_upc)] = abs(distance-to_cluter_dis)
        a = sorted(cluter_dict.items(), key=lambda x: x[1], reverse=True)
        for key in a:
            upc = key[0].split("##")[1]
            if (len(upcs) <= top_n) and (good_upc not in upcs):
                upcs.append(upc)
            elif (len(upcs) >= top_n):
                break
        return upcs
    # 保存新建商品的聚类特征
    def save_new_goods_feature(self,cluter,to_cluter_dis,good_upc,good_feature,img_file_name):
        features, goods_upcs, dises = self.get_good_feature(cluter)
        save_features = []
        for i in range(len(dises)):
            save_features.append(features[i])
            if to_cluter_dis > dises[i+1] and to_cluter_dis <= dises[i]:
                fts = good_upc+","+img_file_name
                for gf in good_feature:
                    fts = fts+","+str(float(gf))
                fts=fts+","+str(to_cluter_dis)
                save_features.append(fts)
        cluter_feature_file = os.path.join(self.save_sort_feature_path, str(cluter) + ".txt")
        with open(cluter_feature_file,'w') as f:
            for feats in save_features:
                f.write(feats)
                f.write("\n")
    #获取重新训练时刻的所有已知特征
    def get_all_features(self):
        goods_upcs = []
        all_features = []
        img_file_names=[]
        for cluter_feature_file in os.listdir(self.save_sort_feature_path):
            with open(cluter_feature_file, 'r') as f:
                features = f.readlines()
                for feature in features:
                    ft = feature.split(",")
                    good_upc = ft[0]
                    img_file = ft[1]
                    feats = ft[2:(len(ft)-1)]
                    feats = list(map(float, feats))
                    goods_upcs.append(good_upc)
                    all_features.append(feats)
                    img_file_names.append(img_file)
        return goods_upcs,all_features,img_file_names

    #保存在线重新训练完成后的排序聚类特征
    def write_sort_feature(self, all_features, label_centers, centers,goods_upcs,img_file_names):
        for j, center in zip(range(len(centers)), centers):
            center_dict = {}
            for i, img_feature,good_upc,img_file_name in zip(label_centers, all_features,goods_upcs,img_file_names):
                if j == i:
                    dis = pdis(center, img_feature)
                    file_feature = str(good_upc)+","+str(img_file_name)+","
                    for feat in img_feature:
                        file_feature = file_feature+","+str(float(feat))
                    center_dict[file_feature] = dis
            a = sorted(center_dict.items(), key=lambda x: x[1], reverse=True)
            save_file = os.path.join(self.save_sort_feature_path, str(j) + ".txt")
            with open(save_file, 'w') as f:
                for key in a:
                    f.write(key[0] + "," + str(float(key[1])))
                    f.write("\n")



# 离线保存kmean模型,获取特征的util，保存排序后的聚类特征
class offline_util:
    feature_path = config.goods_params['kmean_params']['offline']["vgg_predict_features_path"]
    save_sort_feature_path = config.goods_params['kmean_params']['online']["kmean_predict_features_path"]
    img_features = []
    X = []
    def get_goods_features(self):
        for good_feature_file in os.listdir(self.feature_path):
            img_feature_path = os.path.join(self.feature_path, good_feature_file)
            good_upc = str(good_feature_file).strip(".txt")
            self.get_feature(good_upc, img_feature_path)
        return self.img_features,self.X
    def get_feature(self,goods_upc, file_feature):
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
                f2s = goods_upc + ',' + filename
                for f1 in featArr:
                    f1s.append(float(np.sum(f1)))
                    f2s = f2s + "," + str(float(np.sum(f1)))
                self.X.append(f1s)
                self.img_features.append(f2s)

    def write_sort_feature(self,img_features, label_center, centers):
        for j, center in zip(range(len(centers)), centers):
            center_dict = {}
            for i, img_feature in zip(label_center, img_features):
                if j == i:
                    feature = str(img_feature).split(",")
                    feature_img = feature[2:]
                    print (feature_img)
                    feature_img = list(map(float,feature_img))
                    dis = pdis(center, feature_img)
                    center_dict[img_feature] = dis
            a = sorted(center_dict.items(), key=lambda x: x[1], reverse=True)
            save_file = os.path.join(self.save_sort_feature_path,str(j)+".txt")
            with open(save_file, 'w') as f:
                for key in a:
                    f.write(key[0] + "," + str(float(key[1])))
                    f.write("\n")