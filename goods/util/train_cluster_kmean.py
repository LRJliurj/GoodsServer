from goods.util.kmean_util import online_util,offline_util
from goods.net.kmean import Kmeans
k_means = Kmeans()

def train_first():
    offline = offline_util()
    img_features,X = offline.get_goods_features()
    print ("样本已载入："+str(len(X)))
    clf, s = k_means.train(X)
    offline_util.write_sort_feature(img_features, clf.labels_, clf.cluster_centers_)
    k_means.save_model(clf)


def train_alter():
    online = online_util()
    goods_upcs, all_features, img_file_names = online.get_all_features()
    clf, s = k_means.train(all_features)
    online_util.write_sort_feature(all_features, clf.labels_, clf.cluster_centers_,goods_upcs,img_file_names)
    k_means.save_model(clf)