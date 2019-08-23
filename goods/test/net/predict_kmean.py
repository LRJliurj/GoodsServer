from goods.util.kmean_util import offline_util
from goods.net.kmean import Kmeans
offline=offline_util()
k_means = Kmeans()
def predict_offline():
    img_features, X = offline.get_goods_features()
    print("样本特征数："+str(len(X)))
    clf, s = k_means.train(X)
    print ("####################################")
    print ("质心")
    print (len(clf.cluster_centers_))
    # print (clf.cluster_centers_)
    print ("每个样本所属的簇")
    print (clf.labels_)
    offline.write_sort_feature(img_features,clf.labels_,clf.cluster_centers_)
    # print ("用来评估簇的个数的距离")
    # print (clf.inertia_)
    k_means.save_model(clf)

if __name__=="__main__":
    predict_offline()





