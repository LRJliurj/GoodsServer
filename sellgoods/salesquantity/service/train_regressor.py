from sellgoods.salesquantity.model import regressor
from sellgoods.salesquantity.utils import salves_volume
import os
import shutil
from set_config import config
from sellgoods.salesquantity.utils import file_util
regressor_model_path = config.shellgoods_params['regressor_model_path']
test_data_save_path = config.shellgoods_params['test_data_save_path']
salves_ins = salves_volume.Salves()
regressor_ins = regressor.Regressor()
def train_regressor():
    # train_features,test_features,test_f =salves_ins.generate_features4()
    train_features,test_features,test_d = salves_ins.generate_features5()
    sc = salves_ins.sc
    # # 线性回归模型
    # lr_model = regressor_ins.linear_train(train_features)
    # # print ("lr:"+str(lr_model))
    # rmse,r2,result = regressor_ins.evaluate(test_features,lr_model)
    # print("lr test rootMeanSquaredError:" + str(rmse))
    # print("lr test r2::" + str(r2))
    # model_path = regressor_model_path['linear']
    # if os.path.isdir(model_path):
    #     shutil.rmtree(model_path)
    # regressor_ins.save_model(model_path, lr_model)
    # result = result.select("prediction")
    # test_d = test_f.select("shop_id", "upc", "ai_weekday", "ai_day", "ai_nextday", "ai_day_nums", "ai_next_nums")
    # file_util.save_test_dataRdd(test_d, result,test_data_save_path)
    print("###########################################################")
    #
    # # 决策树回归模型
    dt_model = regressor_ins.decision_tree_train(train_features)
    print("dt:" + str(dt_model))
    rmse,r2,result = regressor_ins.evaluate(train_features, dt_model)
    print("dt test rootMeanSquaredError:" + str(rmse))
    print("dt test r2::" + str(r2))
    model_time = '2019-08-30'
    test_time = '2019-08-31'
    test_path =  test_data_save_path+test_time
    model_path = regressor_model_path['decision_tree']+model_time
    if os.path.isdir(model_path):
        shutil.rmtree(model_path)
    regressor_ins.save_model(model_path, dt_model)
    result = dt_model.transform(test_features)
    result = result.select('prediction')
    result = result.select("prediction")
    test_d = test_d.select("shop_id","upc","ai_weekday","ai_day","ai_nextday","ai_day_nums","ai_next_nums")
    file_util.save_test_dataRdd(test_d,result,test_path)
    print("###########################################################")

    # # 梯度提升树回归
    # gbt_model = regressor_ins.gb_tree_train(train_features)
    # print("gbt:" + str(gbt_model))
    # rmse,r2,result = regressor_ins.evaluate(test_features, gbt_model)
    # print("gbt test rootMeanSquaredError:" + str(rmse))
    # print("gbt test r2::" + str(r2))
    # model_path = regressor_model_path['gb_tree']
    # if os.path.isdir(model_path):
    #     shutil.rmtree(model_path)
    # regressor_ins.save_model(model_path, gbt_model)
    # result = result.select("prediction")
    # test_d = test_f.select("shop_id", "upc", "ai_weekday", "ai_day", "ai_nextday", "ai_day_nums", "ai_next_nums")
    # file_util.save_test_dataRdd(test_d, result,test_data_save_path)
    # print("###########################################################")
    # # #
    # # # # 随机森林回归
    # rf_model = regressor_ins.random_forest_train(train_features)
    # print("rf:" + str(rf_model))
    # rmse,r2,result = regressor_ins.evaluate(test_features, rf_model)
    # print("rf test rootMeanSquaredError:" + str(rmse))
    # print("rf test r2::" + str(r2))
    # model_path = regressor_model_path['random_forest']
    # if os.path.isdir(model_path):
    #     shutil.rmtree(model_path)
    # regressor_ins.save_model(model_path, rf_model)
    # result = result.select("prediction")
    # test_d = test_f.select("shop_id", "upc", "ai_weekday", "ai_day", "ai_nextday", "ai_day_nums", "ai_next_nums")
    # file_util.save_test_dataRdd(test_d, result,test_data_save_path)
    # print("###########################################################")


if __name__=='__main__':
    train_regressor()