from goods.util import train_svm

if __name__=="__main__":
    data_path = "/home/ai/data/step2/train/"
    test_data_path = "/home/ai/data/step2/test/"
    model_file = "/home/ai/model/svm_good.ml"
    train_svm.train(data_path,model_file)
    train_svm.test(test_data_path,model_file)