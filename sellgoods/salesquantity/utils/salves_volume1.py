# 销量预测模型   特征处理
from sellgoods.salesquantity.utils import sparkdb
from sellgoods.sql import sales_quantity
from pyspark.ml.feature import VectorAssembler
from pyspark.mllib.regression import LabeledPoint,Vectors
from sellgoods.salesquantity.utils import mean_enchder
from sklearn.preprocessing import OneHotEncoder
from pyspark.sql import SparkSession
import pandas as pd
sdb = sparkdb.SparkDb()
class Salves:
    sc = None
    sqlsc = None
    ss = None
    def __init__(self):
        self.sc = sdb.get_spark_context()
        self.sqlsc = sdb.get_sparksql_context(self.sc)
        self.ss =SparkSession(self.sqlsc)

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
        sql_dataf = self.sqlsc.sql("select * from (select T4.ai_nums as ai_day_nums,T5.ai_nums as ai_next_nums,T4.ai_shop_id as shop_id,T4.ai_create_date as ai_day,T5.ai_create_date as ai_nextday from salves_volume_day T4 left join salves_volume_day T5 on T4.ai_shop_id  = T5.ai_shop_id  and T4.ai_next_date = T5.ai_create_date ) T6 where T6.ai_day_nums is not null and T6.ai_next_nums is not null and T6.shop_id is not null and T6.ai_day is not null and T6.ai_nextday is not null and T6.ai_nums < 500 ")
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
        sql_dataf.show(10)
        sql_dataf.registerTempTable('salves_volume_day')
        sql_dataf = self.sqlsc.sql(
            "select * from (select T4.ai_nums as ai_day_nums,T5.ai_nums as ai_next_nums,T4.ai_shop_id as shop_id,T4.ai_upc as upc ,T4.ai_create_date as ai_day,T5.ai_create_date as ai_nextday from salves_volume_day T4 left join salves_volume_day T5 on T4.ai_shop_id  = T5.ai_shop_id  and T4.ai_upc = T5.ai_upc and T4.ai_next_date = T5.ai_create_date ) T6 where T6.ai_day_nums is not null and T6.ai_next_nums is not null and T6.shop_id is not null and T6.ai_day is not null and T6.ai_nextday is not null and T6.upc != ''")
        # sql_dataf = self.sqlsc.sql("select T4.ai_nums as ai_day_nums,T5.ai_nums as ai_next_nums,T4.ai_shop_id as shop_id,T4.ai_create_date as ai_day,T5.ai_create_date as ai_nextday from salves_volume_day T4 left join salves_volume_day T5 on T4.ai_shop_id  = T5.ai_shop_id  and T4.ai_next_date = T5.ai_create_date")
        df = sql_dataf.select(sql_dataf.shop_id.cast("double"),
                              sql_dataf.ai_day_nums.cast("double"), sql_dataf.ai_next_nums.cast("double"),sql_dataf.upc.cast("double"))
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
        sql_dataf.show(10)
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

        # 用于upc的特征训练  经过平均编码

    def generate_features4(self):
        sql = sales_quantity.sql_params['upc_data_sql']
        # sql1 = sales_quantity.sql_params['upc_data_sql1']  # payment_detail
        # sql2 = sales_quantity.sql_params['upc_data_sql2']  # payment
        # sql3 = sales_quantity.sql_params['upc_data_sql3']  # shop_goods
        # sql_dataf1 = self.get_data_from_mysql(sql1)
        # sql_dataf2 = self.get_data_from_mysql(sql2)
        # sql_dataf3 = self.get_data_from_mysql(sql3)
        # sql_dataf1.registerTempTable('payment_detail')
        # sql_dataf2.registerTempTable('payment')
        # sql_dataf3.registerTempTable('shop_goods')
        sql_dataf = self.get_data_from_mysql(sql)
        # sql_dataf = self.sqlsc.sql(sql)
        sql_dataf.show(10)
        print (sql_dataf.count())
        sql_dataf.registerTempTable('salves_volume_day')
        sql_dataf = self.sqlsc.sql(
            "select * from (select T4.ai_nums as ai_day_nums,T5.ai_nums as ai_next_nums,T4.ai_shop_id as shop_id,T4.ai_upc as upc ,T4.ai_create_date as ai_day,T5.ai_create_date as ai_nextday,T5.ai_week_date as ai_weekday from salves_volume_day T4 left join salves_volume_day T5 on T4.ai_shop_id  = T5.ai_shop_id  and T4.ai_upc = T5.ai_upc and T4.ai_next_date = T5.ai_create_date ) T6 where T6.ai_day_nums is not null and T6.ai_next_nums is not null and T6.shop_id is not null and T6.ai_day is not null and T6.ai_nextday is not null and T6.upc != '' and T6.ai_weekday is not null and T6.ai_next_nums < 1000 ")
        # sql_dataf = self.sqlsc.sql("select T4.ai_nums as ai_day_nums,T5.ai_nums as ai_next_nums,T4.ai_shop_id as shop_id,T4.ai_create_date as ai_day,T5.ai_create_date as ai_nextday from salves_volume_day T4 left join salves_volume_day T5 on T4.ai_shop_id  = T5.ai_shop_id  and T4.ai_next_date = T5.ai_create_date")
        sql_dataf.show(10)
        enc = OneHotEncoder(categorical_features="ai_weekday")

        MeanEncoder = mean_enchder.MeanEncoder(["shop_id","upc"],n_splits=5,target_type='regression',prior_weight_func=None)
        # sql_dataf=self.ss.createDataFrame(sql_dataf)
        sql_dataf = sql_dataf.select(sql_dataf.shop_id.cast("double"),
                              sql_dataf.ai_day_nums.cast("double"), sql_dataf.ai_next_nums.cast("double"),
                              sql_dataf.upc.cast("double"),sql_dataf.ai_weekday.cast("int"))

        # y_dataf = sql_dataf.select("ai_next_nums")
        sql_dataf = sql_dataf.toPandas()
        # y_dataf = y_dataf.toPandas()
        # sql_dataf = enc.fit(pd.Series(sql_dataf['ai_weekday']).values.reshape(-1,1))
        sql_dataf = MeanEncoder.fit_transform(sql_dataf,sql_dataf['ai_next_nums'])
        value = sql_dataf.values.tolist()
        column = list(sql_dataf.columns)
        sql_dataf = self.sqlsc.createDataFrame(value, column)
        sql_dataf.show(10)
        assembler = VectorAssembler(inputCols=["ai_day_nums", "shop_id_pred", "upc_pred","ai_weekday"], outputCol="features")
        output = assembler.transform(sql_dataf)
        train_feature, test_features = output.select("features", "ai_next_nums").toDF('features', 'label').randomSplit(
            [7.0, 3.0], 100)
        print(train_feature.show(10))
        return train_feature, test_features

        # 用于upc的线上特征获取，经过平均编码

    def get_online_features4(self):
        sql = sales_quantity.sql_params['upc_predict_sql']
        sql_dataf = self.get_data_from_mysql(sql)
        sql_dataf.show(10)
        sql_dataf.registerTempTable('salves_volume_day')
        sql_dataf.show(30)
        df = sql_dataf.select(sql_dataf.ai_shop_id.cast("double"),
                              sql_dataf.ai_nums.cast("double"), sql_dataf.ai_upc.cast("double"),
                              sql_dataf.ai_create_date.cast("string"),
                              sql_dataf.ai_next_date.cast("string"))
        sql_dataf.show(30)
        assembler = VectorAssembler(inputCols=["ai_nums", "ai_shop_id", "ai_upc"], outputCol="features",
                                    handleInvalid="skip")
        output = assembler.transform(df)
        feature = output.select("features").toDF('features')
        print(feature.show(10))
        return feature, df

if __name__=='__main__':
    sql = "(SELECT  count(1) FROM   ( SELECT sum(T2.t1_nums) AS ai_nums,  T2.t1_shop_id AS ai_shop_id,T3.upc AS ai_upc, T2.t1_create_date AS ai_create_date, DATE_FORMAT(  from_unixtime(  unix_timestamp(   DATE_FORMAT(  T2.t1_create_date,'%Y-%m-%d' )  ) + 24 * 3600 ), '%Y-%m-%d'          ) AS ai_next_date       FROM            (               SELECT                  sum(T1.nums) AS t1_nums,                    T1.shop_id AS t1_shop_id,                   T1.goods_id,                    T1.create_date AS t1_create_date                FROM                    (                       SELECT                          number nums,                            shop_id,                            goods_id,                           DATE_FORMAT(create_time, '%Y-%m-%d') create_date                        FROM                            payment_detail                      WHERE                           shop_id IS NOT NULL                         AND goods_id IS NOT NULL                        AND number > 0                      AND create_time > '2019-06-01 00:00:00'                         AND create_time < '2019-09-01 00:00:00'                         AND payment_id IN (                             SELECT DISTINCT                                 (payment.id)                            FROM                                payment                             WHERE                               payment.type != 50                          AND create_time > '2019-06-01 00:00:00'                             AND create_time < '2019-09-01 00:00:00'                         )                   ) T1                GROUP BY                    T1.shop_id,                     T1.goods_id,                    T1.create_date          ) T2        LEFT JOIN shop_goods T3 ON T2.t1_shop_id = T3.shop_id       AND T2.goods_id = T3.goods_id       WHERE           T3.upc != ''        GROUP BY            T2.t1_create_date,          T2.t1_shop_id,          T3.upc  ) T8) tmp "
    salves_ins = Salves()
    sql_dataf = salves_ins.get_data_from_mysql(sql)
    sql_dataf.show(10)