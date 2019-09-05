# -*-coding=utf-8 -*-
from pyspark import SparkConf, SparkContext
sc = SparkContext()
import os
#os.environ["PYSPARK_PYTHON"]='/usr/bin/python3'
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD, LinearRegressionModel
# Load and parse the data 加载和解析数据，将每一个数转化为浮点数。每一行第一个数作为标记，后面的作为特征
def parsePoint(line):
    values = [float(x) for x in line.replace(',', ' ').split(' ')]
    return LabeledPoint(values[0], [values[0]])

data = sc.textFile(os.path.join("D:\\opt\\data\\linear\\lpsa.data"))
print (data.collect()[0]) #-0.4307829,-1.63735562648104 -2.00621178480549 -1.86242597251066 -1.024....-0.864466507337306
parsedData = data.map(parsePoint)
print (parsedData.collect()[0]) #(-0.4307829,[-1.63735562648,-2.00621178481,-1.86242597251,-1.024....,-0.864466507337])

# Build the model 建立模型
model = LinearRegressionWithSGD.train(parsedData, iterations=1000, step=0.1)
print (model.weights)