# 销量预测模型   特征处理
from sellgoods.salesquantity.utils import sparkdb
from sellgoods.sql import sales_quantity
from pyspark.ml.feature import VectorAssembler
from pyspark.mllib.regression import LabeledPoint,Vectors
sdb = sparkdb.SparkDb()
class Salves:
    sc = None
    sqlsc = None
    def __init__(self):
        self.sc = sdb.get_spark_context()
        self.sqlsc = sdb.get_sparksql_context(self.sc)
    def get_data_from_mysql(self,sql):
        sql_dataf =  sdb.get_data_frame(sql,self.sqlsc)
        return sql_dataf

    def generate_features(self):
        sql = sales_quantity.sql_params['train_data_sql']
        sql_dataf = self.get_data_from_mysql(sql)
        df = sql_dataf.select(sql_dataf.ai_shop_id.cast("double"), sql_dataf.ai_create_date.cast("double"), sql_dataf.ai_nums.cast("double"))
        assembler = VectorAssembler(inputCols=["ai_nums","ai_shop_id"], outputCol="features")
        output = assembler.transform(df)
        train_feature, test_features = output.select("features", "ai_nums").toDF('features', 'label').randomSplit(
            [7.0, 3.0], 100)
        print(train_feature.show(10))
        labelpointRDD_train = train_feature.rdd.map(
            lambda row: LabeledPoint(row['label'] / 1000000, Vectors.dense([row['features'][0] / 1000000])))
        labelpointRDD_test = test_features.rdd.map(
            lambda row: LabeledPoint(row['label'] / 1000000, Vectors.dense([row['features'][0] / 1000000])))
        print(labelpointRDD_train.show(10))
        return labelpointRDD_train,labelpointRDD_test
    # 用于门店的特征训练
    def generate_features2(self):
        sql = sales_quantity.sql_params['train_data_sql']
        sql_dataf = self.get_data_from_mysql(sql)
        sql_dataf.show(1000)
        sql_dataf.registerTempTable('salves_volume_day')
        sql_dataf = self.sqlsc.sql("select * from (select T4.ai_nums as ai_day_nums,T5.ai_nums as ai_next_nums,T4.ai_shop_id as shop_id,T4.ai_create_date as ai_day,T5.ai_create_date as ai_nextday from salves_volume_day T4 left join salves_volume_day T5 on T4.ai_shop_id  = T5.ai_shop_id  and T4.ai_next_date = T5.ai_create_date ) T6 where T6.ai_day_nums is not null and T6.ai_next_nums is not null and T6.shop_id is not null and T6.ai_day is not null and T6.ai_nextday is not null")
        # sql_dataf = self.sqlsc.sql("select T4.ai_nums as ai_day_nums,T5.ai_nums as ai_next_nums,T4.ai_shop_id as shop_id,T4.ai_create_date as ai_day,T5.ai_create_date as ai_nextday from salves_volume_day T4 left join salves_volume_day T5 on T4.ai_shop_id  = T5.ai_shop_id  and T4.ai_next_date = T5.ai_create_date")

        sql_dataf.show(1000)
        df = sql_dataf.select(sql_dataf.shop_id.cast("double"),
                              sql_dataf.ai_day_nums.cast("double"),sql_dataf.ai_next_nums.cast("double"))
        assembler = VectorAssembler(inputCols=["ai_day_nums","shop_id"], outputCol="features")
        output = assembler.transform(df)
        train_feature, test_features = output.select("features", "ai_next_nums").toDF('features', 'label').randomSplit(
            [7.0, 3.0], 100)
        print(train_feature.show(10))
        return train_feature,test_features

    #用于门店的线上特征获取
    def get_online_features(self):
        sql = sales_quantity.sql_params['predict_data_sql']
        sql_dataf = self.get_data_from_mysql(sql)
        sql_dataf.show(1000)
        sql_dataf.registerTempTable('salves_volume_day')
        sql_dataf.show(30)
        df = sql_dataf.select(sql_dataf.ai_shop_id.cast("int"),
                              sql_dataf.ai_nums.cast("int"),sql_dataf.ai_create_date.cast("string"),sql_dataf.ai_next_date.cast("string"))
        sql_dataf.show(30)
        assembler = VectorAssembler(inputCols=["ai_nums", "ai_shop_id"], outputCol="features")
        output = assembler.transform(df)
        feature = output.select("features").toDF('features')

        print(feature.show(10))
        return feature,df

    # 用于upc的特征训练
    def generate_features3(self):
        sql = sales_quantity.sql_params['upc_data_sql']
        sql_dataf = self.get_data_from_mysql(sql)
        sql_dataf.show(100)
        sql_dataf.registerTempTable('salves_volume_day')
        sql_dataf = self.sqlsc.sql(
            "select * from (select T4.ai_nums as ai_day_nums,T5.ai_nums as ai_next_nums,T4.ai_shop_id as shop_id,T4.ai_upc as upc ,T4.ai_create_date as ai_day,T5.ai_create_date as ai_nextday from salves_volume_day T4 left join salves_volume_day T5 on T4.ai_shop_id  = T5.ai_shop_id  and T4.ai_upc = T5.ai_upc and T4.ai_next_date = T5.ai_create_date ) T6 where T6.ai_day_nums is not null and T6.ai_next_nums is not null and T6.shop_id is not null and T6.ai_day is not null and T6.ai_nextday is not null and T6.upc != ''")
        # sql_dataf = self.sqlsc.sql("select T4.ai_nums as ai_day_nums,T5.ai_nums as ai_next_nums,T4.ai_shop_id as shop_id,T4.ai_create_date as ai_day,T5.ai_create_date as ai_nextday from salves_volume_day T4 left join salves_volume_day T5 on T4.ai_shop_id  = T5.ai_shop_id  and T4.ai_next_date = T5.ai_create_date")


        df = sql_dataf.select(sql_dataf.shop_id.cast("double"),
                              sql_dataf.ai_day_nums.cast("double"), sql_dataf.ai_next_nums.cast("double"),sql_dataf.upc.cast("double"))
        df.show(1000)
        assembler = VectorAssembler(inputCols=["ai_day_nums", "shop_id","upc"], outputCol="features")
        output = assembler.transform(df)
        train_feature, test_features = output.select("features", "ai_next_nums").toDF('features', 'label').randomSplit(
            [7.0, 3.0], 100)
        print(train_feature.show(10))
        return train_feature, test_features

    # 用于upc的线上特征获取
    def get_online_features3(self):
        sql = sales_quantity.sql_params['upc_predict_sql']
        sql_dataf = self.get_data_from_mysql(sql)
        sql_dataf.show(1000)
        sql_dataf.registerTempTable('salves_volume_day')
        sql_dataf.show(30)
        df = sql_dataf.select(sql_dataf.ai_shop_id.cast("double"),
                              sql_dataf.ai_nums.cast("double"),sql_dataf.ai_upc.cast("double"), sql_dataf.ai_create_date.cast("string"),
                              sql_dataf.ai_next_date.cast("string"))
        sql_dataf.show(30)
        assembler = VectorAssembler(inputCols=["ai_nums", "ai_shop_id","ai_upc"], outputCol="features",handleInvalid="skip")
        output = assembler.transform(df)
        feature = output.select("features").toDF('features')
        print(feature.show(10))
        return feature, df




