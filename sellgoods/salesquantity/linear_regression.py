# 多元线性回归
# 特征  下一天的销量，商店id,商品id,当天的销量
# from org.apache.spark.mlib.model import LinearRegressionModel,LinearRegressionWithSGD
from pyspark.mllib.regression import LinearRegressionModel,LinearRegressionWithSGD
from pyspark.ml.regression import LinearRegression
class Linear:
    def get_model(self,dataf,num_iter,step_size,mini_batch_frction):
        model = LinearRegressionWithSGD.train(dataf,iterations=num_iter,step=step_size,miniBatchFraction=mini_batch_frction)
        return model

    def get_model_weight(self,dataf,weights,num_iter,step_size,mini_batch_frction):
        model = LinearRegressionWithSGD.train(dataf,iterations=num_iter,step=step_size,miniBatchFraction=mini_batch_frction,initialWeights=weights)
        return model

    def load_model(self,sc,model_file):
        model = LinearRegressionModel.load(sc,model_file)
        return model

