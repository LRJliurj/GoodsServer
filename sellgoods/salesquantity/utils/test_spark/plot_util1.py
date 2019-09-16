import matplotlib.pyplot as plt
import matplotlib
import os
import math
import random
zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')

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

def regressor_test_plot_a(p_date,test_days,title):
    plt.plot(test_days, p_date, label='p')
    plt.title(title,fontproperties=zhfont1)
    plt.legend()
    plt.show()

def regressor_test_plot_b (day_upc_sum, upcs,title):
    upcs = list(set(upcs))
    # random.seed(100)
    upcs = random.sample(upcs, 1)
    print (upcs)
    days = []
    upc_yp = {}
    for upc in upcs:
        y_true = []
        y_predict = []
        for key1 in day_upc_sum:
            days.append(int(key1))
            if upc not in list(day_upc_sum[key1].keys()):
                y_true.append(0)
                y_predict.append(0)
            else :
                y_true.append(day_upc_sum[key1][upc][0])
                y_predict.append(day_upc_sum[key1][upc][1])
        upc_yp[upc] = (y_true,y_predict)


    print (upc_yp)
    print (days)
    days = list(set(days))
    for key in upc_yp:
        plt.plot(days, upc_yp[key][0], label=key+'_true')
        plt.plot(days, upc_yp[key][1], label=key+'_predict')
    plt.title(title, fontproperties=zhfont1)
    plt.legend()
    plt.show()


def  load_data(test_path,shop_id,upc):
    files = os.listdir(test_path)
    test_days = []
    i= 0
    j= 0
    p_date = []
    upcs =[]
    day_upc_sum = {}
    for file in files:
        i_date = 0
        j_date = 0
        file_path = os.path.join(test_path, file)
        day = str(file).strip("test.txt").split("-")[2]
        test_days.append(day)
        upc_sum= {}
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if shop_id != None and shop_id not in line.split(","):
                    continue
                if upc != None and upc not in line.split(","):
                    continue
                i+=1
                i_date += 1
                true_l = int(float(str(line).split(",")[-2]))
                predict_l = int(math.floor(float(str(line).split(",")[-1])))
                true_l_f = float(str(line).split(",")[-2])
                predict_l_f = float(str(line).split(",")[-1])
                upc_sum[str(line).split(",")[1]] = (true_l,predict_l)
                upcs.append(str(line).split(",")[1])
                if true_l_f < 10 and abs(true_l_f-predict_l_f) <= 1:
                    j += 1
                    j_date += 1
                elif  true_l_f >10 and abs(true_l_f-predict_l_f) <= int(true_l_f*0.05) :
                    j += 1
                    j_date += 1
        day_upc_sum[day] = upc_sum
        p_date.append(float(j_date) / i_date)
    p = float(j) / i
    return day_upc_sum,upcs,p,p_date,test_days



# 选择门店 和 upc 的 误差


if __name__=='__main__':
    test_path = "D:\\opt\\data\\linear\\predict_test\\"
    day_upc_sum, upcs, p, p_date, test_days = load_data(test_path,None,None)
    print (p)
    # title="所有商店，所有商品准确率" + str(p)
    # regressor_test_plot_a(p_date,test_days,p,title)
    title1 = "所有店 某个upc下的真实销量与预测销量 "
    regressor_test_plot_b(day_upc_sum, upcs, title1)

    # 广州 shop_id = 3607
    # day_upc_sum, upcs, p, p_date, test_days = load_data(test_path, '3607', None)
    # title = "广州 shop_id = 3607 ,准确率 p = "+str(p)
    # regressor_test_plot_a(p_date, test_days, title)
    # title1 = "广州 shop_id = 3607 upc下的真实销量与预测销量 "
    # regressor_test_plot_b(day_upc_sum, upcs, title1)

    # 普天 shop_id = 1284
    # day_upc_sum, upcs, p, p_date, test_days = load_data(test_path, '1284', None)
    # title = "普天 shop_id = 1284  ,准确率 p = " + str(p)
    # regressor_test_plot_a(p_date, test_days, title)
    # title1 = "普天 shop_id = 1284 upc下的真实销量与预测销量 "
    # regressor_test_plot_b(day_upc_sum, upcs, title1)

    #深圳 shop_id = 1629
    # day_upc_sum, upcs, p, p_date, test_days = load_data(test_path, '1629', None)
    # print (upcs)
    # # title = "深圳 shop_id = 1629  ,准确率 p = " + str(p)
    # # regressor_test_plot_a(p_date, test_days, title)
    # title1 = "深圳 shop_id = 1629 upc下的真实销量与预测销量 "
    # regressor_test_plot_b(day_upc_sum, upcs, title1)