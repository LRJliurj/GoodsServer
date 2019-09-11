import matplotlib.pyplot as plt
import os
import math
import random


def random_samples(samples,test_trues,test_predicts,random_size=None):
    test_trues_ = []
    test_predicts_ = []
    if random_size != None:
        random.seed(10)
        slice = random.sample(samples, random_size)
        for i in slice:
            test_trues_.append(test_trues[i])
            test_predicts_.append(test_predicts[i])
        samples_ = list(range(len(slice)))
        return samples_,test_trues_,test_predicts_
    else:
        return samples,test_trues,test_predicts
#散点图
def regressor_test_plot_s(test_trues,test_predicts,random_size=None):
    samples = list(range(len(test_trues)))
    print (len(samples))
    samples,test_trues,test_predicts = random_samples(samples,test_trues,test_predicts,random_size)

    plt.scatter(samples, test_trues,
                c='steelblue', marker='.', edgecolor='green',
                label='true')
    plt.scatter(samples, test_predicts,
                c='steelblue', marker='.', edgecolor='red',
                label='predict')
    plt.xlabel('samples')
    plt.ylabel('predict/true values')
    plt.tight_layout()
    plt.show()

# 折线图
def regressor_test_plot_z(test_trues,test_predicts,random_size=None):
    samples = list(range(len(test_trues)))
    print(len(samples))
    samples, test_trues, test_predicts = random_samples(samples, test_trues, test_predicts, random_size)
    plt.plot(samples, test_trues, label='True')
    plt.plot(samples, test_predicts, label='Predict')
    plt.legend()
    plt.show()
# 误差波动
def regressor_test_plot_z1(test_trues,test_predicts,random_size=None):
    samples = list(range(len(test_trues)))
    print(len(samples))
    samples, test_trues, test_predicts = random_samples(samples, test_trues, test_predicts, random_size)
    pes = []
    for i,j in zip(test_trues,test_predicts):
        pes.append(int(i-j))

    plt.plot(samples, pes, label='se')
    plt.legend()
    plt.show()


# 选择门店 和 upc 的 误差


if __name__=='__main__':
    test_path = "D:\\opt\\data\\linear\\predict_test\\"
    files = os.listdir(test_path)
    test_trues=[]
    test_predicts = []
    for file in files:
        file_path = os.path.join(test_path, file)
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                true_l = int(float(str(line).split(",")[0]))
                predict_l = int(math.floor(float(str(line).split(",")[1])))
                test_trues.append(true_l)
                test_predicts.append(predict_l)
    # regressor_test_plot_s(test_trues,test_predicts,200)
    regressor_test_plot_z1(test_trues, test_predicts,2000)