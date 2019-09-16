

import numpy as np
from goods.net.kmean import Kmeans
from goods.util.kmean_util import online_util
online = online_util()
kmean = Kmeans()
clf = kmean.load_model()



def gettopn(file):
    f1ss = []
    upcs = []
    sum_i = 0
    sum_j = 0
    file_features = []
    with open(file,'r') as f:
        file_features = f.readlines()

    for img_feature in file_features:
        upc = None
        img_feature = img_feature.split(",")
        if "_" in img_feature[0]:
            upc = img_feature[0].split("_")[0]
        else:
            upc =  img_feature[0].strip(".jpg")
        upcs.append(upc)
        feature = img_feature[1:]
        feat = []
        for fea in feature:
            feat.append(float(fea))
        featArr = np.array(feat)
        featArr.resize(512, 7)
        f1s = []
        for f1 in featArr:
            f1s.append(float(np.sum(f1)))
        f1ss.append(f1s)
    cluter_labels = clf.predict(f1ss)
    for cluter_label, upc,feature in zip(cluter_labels, upcs,f1ss):
        print (feature)
        print (upc)
        upcs = online.get_topn_upc(cluter_label, feature)
        print (upcs)
        sum_i += 1
        if upc in upcs:
            sum_j += 1
        print (sum_j)
    print (sum_j/sum_i)

if __name__=='__main__':
    gettopn("D:\\opt\\data\\goods\\step2_all_feature\\vgg_features.txt")