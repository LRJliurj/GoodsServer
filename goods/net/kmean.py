import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics


def kmean_train(X,n_cluters=50):
    model = KMeans(n_cluters=50).fit(X)
    return model

def get_data_from_features(feature_file):
    feature_dict = np.loadtxt(feature_file)
    X=[]
    for key in feature_dict:
        X.append(np.asarray(feature_dict[key]))
    return X,feature_dict

def write(X,feature_dict):
    model = kmean_train(X)




