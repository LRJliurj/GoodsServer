from goods.net.sift import SIFT
import os
import cv2
from goods.net.svm import SVM
def load_data(path):
    upc_paths = os.listdir(path)
    upc_features = {}
    for upc_path in upc_paths:
        upc_local_path = os.path.join(path,upc_path)
        features = []
        for file in os.listdir(upc_local_path):
            if "train_augment0" not in file:
                continue
            sift_ins = SIFT()
            img = cv2.imread(os.path.join(upc_local_path,file),0)
            feature = sift_ins.get_features(img)
            features.append(feature)
        upc_features[str(upc_path)] = features
    data = []
    labels = []
    for upc_feature1 in upc_features:
        features1 = upc_features[upc_feature1]
        for upc_feature2 in upc_features:
            features2 = upc_features[upc_feature2]
            for feat1 in features1:
                for feat2 in features2:
                    feature = []
                    print (feat2)
                    if type(feat1)==type(None) or type(feat2)==type(None):
                        continue
                    feature.extend(feat1)
                    feature.extend(feat2)
                    if upc_feature1 == upc_feature2:
                        labels.append(1)
                    else:
                        labels.append(0)
                    data.append(feature)
    return data,labels
#
def train(path,model_file):
    data,labels = load_data(path)
    svm_ins = SVM()
    svm_model = svm_ins.train(data,labels)
    svm_ins.save_model(svm_model,model_file)

def test(path,model_file):
    data,labels = load_data(path)
    svm_ins = SVM()
    model=svm_ins.load_model(model_file)
    label_ts = model.predict(data)
    j=0
    for label,pre in zip(labels,label_ts):
        if label == pre:
            j+=1

    print (float(j/len(label_ts)))
    socre = float(j/len(label_ts))
    with open("1.txt","w") as f:
        f.write(str(socre))


if __name__=="__main__":
    data_path = "D:\\opt\\data\\goods\\step2\\train_small\\"
    test_data_path = "D:\\opt\\data\\goods\\step2\\test_small\\"
    model_file = "D:\\opt\\code\\model\\svm_goods\\svm_good.ml"
    # train(data_path,model_file)

    test(test_data_path,model_file)

