from sklearn.cluster.k_means_ import KMeans
from sklearn.externals import joblib
from goods.util.distance_util import pdis
from set_config import config

class Kmeans:
    model_file = config.goods_params['kmean_params']['model_file']
    n_cluters = config.goods_params['kmean_params']['n_cluters']
    batch_size = config.goods_params['kmean_params']['batch_size']
    def train(self,X):
        clf = KMeans(self.n_cluters)
        s = clf.fit(X)
        return clf,s
    def save_model(self,clf):
        joblib.dump(clf, self.model_file)

    def load_model(self):
        clf = joblib.load(self.model_file)
        return clf





