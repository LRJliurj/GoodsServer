from pyspark.ml.regression import LinearRegression,LinearRegressionModel
from pyspark.ml.regression import DecisionTreeRegressor,DecisionTreeRegressionModel
from pyspark.ml.regression import GBTRegressor,GBTRegressionModel
from pyspark.ml.regression import RandomForestRegressor,RandomForestRegressionModel
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline, PipelineModel
class Regressor:
    model_load_factory = {
        "linear":LinearRegressionModel,
        "decision_tree":DecisionTreeRegressionModel,
        "gb_tree":GBTRegressionModel,
        "random_forest":RandomForestRegressionModel
    }


    # 线性回归
    def linear_train(self,train_data):
        lr = LinearRegression(maxIter=1000, elasticNetParam=0.8, regParam=0.3)
        # lr_model = lr.fit(train_data)
        pipeline = Pipeline(stages=[lr])
        lr_model = pipeline.fit(train_data)

        return lr_model
    # 模型评估指标
    def evaluate(self,test_data,model):
        result = model.transform(test_data)
        print ("预测结果：")
        print (str(result.show(100)))
        evaluator_r2 = RegressionEvaluator(labelCol='label', metricName="r2", predictionCol='prediction')
        evaluator_rmse = RegressionEvaluator(labelCol='label', metricName="rmse", predictionCol='prediction')
        rmse = evaluator_rmse.evaluate(result)
        r2 = evaluator_r2.evaluate(result)
        return rmse,r2,result

    #决策树回归
    def decision_tree_train(self,train_data):
        dt = DecisionTreeRegressor(maxDepth=10)
        pipeline = Pipeline(stages=[dt])
        dt_model = pipeline.fit(train_data)
        # dt_model = dt.fit(train_data)
        return dt_model
    # 梯度提升树回归
    def gb_tree_train(self,train_data):
        gbt = GBTRegressor(maxIter=100, maxDepth=3)
        pipeline = Pipeline(stages=[gbt])
        gbt_model = pipeline.fit(train_data)
        # gbt_model = gbt.fit(train_data)
        return gbt_model

    #随机森林回归
    def random_forest_train(self,train_data):
        rf = RandomForestRegressor(numTrees=100, maxDepth=5, seed=101)
        pipeline = Pipeline(stages=[rf])
        rf_model = pipeline.fit(train_data)
        # rf_model = rf.fit(train_data)
        return rf_model



    def save_model(self,model_path,model):
        # model.write().format("pmml").save(model_path)
        model.write().overwrite().save(model_path)
        # model.save(model_path)

    def load_model(self,model_path):
        model = PipelineModel.load(model_path)
        # model = self.model_load_factory[regressor_name].load(model_path)
        return model