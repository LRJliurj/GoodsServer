from sklearn.cluster import k_means_
from sklearn.externals import joblib
from goods.util.distance_util import pdis
from set_config import config

class Kmeans:
    model_file = config.goods_params['kmean_params']['model_file']
    n_cluters = config.goods_params['kmean_params']['n_cluters']
    batch_size = config.goods_params['kmean_params']['batch_size']
    def train(self,X):
        clf = self.create_cluster(self.n_cluters)
        s = clf.fit(X)
        return clf,s
    def create_cluster(self,nclust = 10):
    # Manually override euclidean
        def euc_dist(X, Y = None, Y_norm_squared = None, squared = False):
            return pdis(X, Y)
        k_means_.euclidean_distances = euc_dist
        # kmeans = k_means_.KMeans(max_iter = 10000,n_clusters = nclust, n_jobs = 1, random_state = 3425)
        kmeans = k_means_.MiniBatchKMeans(init='k-means++', n_clusters=nclust, batch_size=self.batch_size, max_no_improvement=10, verbose=0,reassignment_ratio=0.001)
        return kmeans

    def save_model(self,clf):
        joblib.dump(clf, self.model_file)

    def load_model(self):
        clf = joblib.load(self.model_file)
        return clf





