# 销量预测模型   特征处理
from pyspark import SparkContext,SQLContext
class salves:
    def is_check(self,dataf):
        dataf = dataf.filter(dataf[0] > 0)

        return dataf
