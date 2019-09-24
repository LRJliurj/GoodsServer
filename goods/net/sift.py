"""
使用sift提取图像特征
"""
import cv2
from sklearn.decomposition import PCA
import numpy

class SIFT:
    detector=None
    extractor=None
    def __init__(self):
        self.detector = cv2.xfeatures2d.SIFT_create()
        self.extractor = cv2.xfeatures2d.SIFT_create()

    #返回一组数组 图像特征
    def extract_sift(self,im):
        return self.extractor.compute(im,self.detector.detect(im))[1]

    def get_sift_features(self,img):
        return self.extract_sift(img)

    def pca(self,x,n_components=1):
        pca = PCA(n_components=n_components)  # 加载PCA算法，设置降维后主成分数目为1
        return pca.fit_transform(x)  # 对样本进行降维

    def get_features(self,img,size=(15,500)):
        sift_feature = self.get_sift_features(img)
        if type(sift_feature) != type(None):
            features_rows = sift_feature.shape[0]
            if features_rows > 20:
                sift_feature = self.pca(sift_feature.T, 15) #降维 (128,15)
                sift_feature = numpy.resize(sift_feature, (1, size[1]))
                return sift_feature[0]
        else:
            return None

if __name__=="__main__":
    test_jpg = cv2.imread("D:\\opt\\data\\goods\\uc_merchant_goods\\img\\6922316110348_7446.jpg",0)
    sift_ins = SIFT()
    print (sift_ins.get_features(test_jpg))
