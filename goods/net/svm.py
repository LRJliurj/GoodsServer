from sklearn import svm
from sklearn.svm import SVC
from sklearn.externals import joblib
class SVM:
    svm = None
    def __init__(self):
        self.svm = SVC(kernel='rbf', random_state=0, gamma=0.10, C=10.0)
    def train(self,X,labels):
        return self.svm.fit(X,labels)
    def predict(self,X):
        return self.svm.predict(X)

    def load_model(self,file):
        return joblib.load(file)

    def save_model(self,model,file):
        joblib.dump(model,file)

