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


    # 用于upc的特征训练  经过平均编码
    def generate_features4(self):
        sql = sales_quantity.sql_params['upc_data_sql']
        sql_dataf = self.get_data_from_mysql(sql)
        print (sql_dataf.count())
        sql_dataf.registerTempTable('salves_volume_day')
        sql_dataf = self.sqlsc.sql(
            "select * from (select T4.ai_nums as ai_day_nums,T5.ai_nums as ai_next_nums,T4.ai_shop_id as shop_id,T4.ai_upc as upc ,T4.ai_create_date as ai_day,T5.ai_create_date as ai_nextday,T5.ai_week_date as ai_weekday from salves_volume_day T4 left join salves_volume_day T5 on T4.ai_shop_id  = T5.ai_shop_id  and T4.ai_upc = T5.ai_upc and T4.ai_next_date = T5.ai_create_date ) T6 where T6.ai_day_nums is not null and T6.ai_next_nums is not null and T6.shop_id is not null and T6.ai_day is not null and T6.ai_nextday is not null and T6.upc != '' and T6.ai_weekday is not null ")
        # enc = OneHotEncoder(categorical_features="ai_weekday")
        MeanEncoder = mean_enchder.MeanEncoder(["shop_id","upc"],n_splits=5,target_type='regression',prior_weight_func=None)
        sql_dataf = sql_dataf.select(sql_dataf.shop_id.cast("double"),
                              sql_dataf.ai_day_nums.cast("double"), sql_dataf.ai_next_nums.cast("double"),
                              sql_dataf.upc.cast("double"),sql_dataf.ai_weekday.cast("int"),sql_dataf.ai_day.cast("string"),sql_dataf.ai_nextday.cast("string"))

        # y_dataf = sql_dataf.select("ai_next_nums")
        sql_dataf = sql_dataf.toPandas()
        # y_dataf = y_dataf.toPandas()
        # sql_dataf = enc.fit(pd.Series(sql_dataf['ai_weekday']).values.reshape(-1,1))
        sql_dataf = MeanEncoder.fit_transform(sql_dataf,sql_dataf['ai_next_nums'])
        value = sql_dataf.values.tolist()
        column = list(sql_dataf.columns)
        sql_dataf = self.sqlsc.createDataFrame(value, column)
        train_f, test_f = sql_dataf.select("shop_id","upc","shop_id_pred", "upc_pred","ai_day_nums","ai_weekday","ai_day","ai_nextday","ai_next_nums").randomSplit(
            [7.0, 3.0], 100)
        assembler = VectorAssembler(inputCols=["ai_day_nums", "shop_id_pred", "upc_pred","ai_weekday"], outputCol="features")
        output_train = assembler.transform(train_f)
        out_test = assembler.transform(test_f)
        train_feature  = output_train.select("features", "ai_next_nums").toDF('features', 'label')
        test_features =  out_test.select("features", "ai_next_nums").toDF('features', 'label')
        print(train_feature.show(10))
        return train_feature, test_features,test_f

        # 用于upc的线上特征获取，经过平均编码

    def get_online_features4(self,MeanEncoder=None):
        sql = sales_quantity.sql_params['upc_data_sql_test']
        sql_dataf = self.get_data_from_mysql(sql)
        sql_dataf.show(10)
        sql_dataf.registerTempTable('salves_volume_day')
        sql_dataf.show(30)
        df = sql_dataf.select(sql_dataf.ai_shop_id.cast("double"),
                              sql_dataf.ai_nums.cast("double"), sql_dataf.ai_upc.cast("double"),
                              sql_dataf.ai_create_date.cast("string"),
                              sql_dataf.ai_next_date.cast("string"),sql_dataf.ai_week_date.cast("string"))
        df_feature = df.select("ai_shop_id", "ai_upc").toDF('features', 'label')
        sql_dataf.show(30)
        # assembler = VectorAssembler(inputCols=["ai_nums", "ai_shop_id", "ai_upc"], outputCol="features",
        #                             handleInvalid="skip")
        output = MeanEncoder.transform(df)
        feature = output.select("features").toDF('features')
        print(feature.show(10))
        return feature, df

    # 用于upc的特征训练  经过平均编码
    def generate_features5(self):
        MeanEncoder = mean_enchder.MeanEncoder(["shop_id", "upc"], n_splits=5, target_type='regression',
                                               prior_weight_func=None)
        train_feature, MeanEncoder = self.get_train_feature(MeanEncoder)
        feature, df = self.get_test_feature(MeanEncoder)
        return train_feature,feature,df
    def get_test_feature(self,MeanEncoder):
        print ("get_test_feature")
        sql = sales_quantity.sql_params['upc_data_sql_test']
        sql_dataf = self.get_data_from_mysql(sql)
        sql_dataf.show(10)
        sql_dataf.registerTempTable('salves_volume_day_test')
        sql_dataf = self.sqlsc.sql(
            "select * from (select T4.ai_nums as ai_day_nums,T5.ai_nums as ai_next_nums,T4.ai_shop_id as shop_id,T4.ai_upc as upc ,T4.ai_create_date as ai_day,T5.ai_create_date as ai_nextday,T5.ai_week_date as ai_weekday from salves_volume_day_test T4 left join salves_volume_day_test T5 on T4.ai_shop_id  = T5.ai_shop_id  and T4.ai_upc = T5.ai_upc and T4.ai_next_date = T5.ai_create_date ) T6 where T6.ai_day_nums is not null and T6.ai_next_nums is not null and T6.shop_id is not null and T6.ai_day is not null and T6.ai_nextday is not null and T6.upc != '' and T6.ai_weekday is not null")
        sql_dataf.show(10)
        df = sql_dataf.select(sql_dataf.shop_id.cast("double"),
                                     sql_dataf.ai_day_nums.cast("double"), sql_dataf.ai_next_nums.cast("double"),
                                     sql_dataf.upc.cast("double"), sql_dataf.ai_weekday.cast("int"),sql_dataf.ai_day.cast("string"),sql_dataf.ai_nextday.cast("string"))
        sql_dataf = df.select('shop_id', 'upc','ai_day_nums','ai_weekday','ai_next_nums')
        sql_dataf.show(10)
        sql_dataf = sql_dataf.toPandas()
        sql_dataf = MeanEncoder.transform(sql_dataf)
        value = sql_dataf.values.tolist()
        column = list(sql_dataf.columns)
        sql_dataf = self.sqlsc.createDataFrame(value, column)
        assembler = VectorAssembler(inputCols=["ai_day_nums", "shop_id_pred", "upc_pred", "ai_weekday"],
                                    outputCol="features")
        output = assembler.transform(sql_dataf)
        test_feature = output.select("features", "ai_next_nums").toDF('features', 'label')
        feature = output.select("features")
        print(feature.show(10))
        return test_feature, df


    def get_train_feature(self,MeanEncoder):
        print("get_train_feature")
        sql = sales_quantity.sql_params['upc_data_sql']
        sql_dataf = self.get_data_from_mysql(sql)
        sql_dataf.show(10)
        print(sql_dataf.count())
        sql_dataf.registerTempTable('salves_volume_day')
        sql_dataf = self.sqlsc.sql(
            "select * from (select T4.ai_nums as ai_day_nums,T5.ai_nums as ai_next_nums,T4.ai_shop_id as shop_id,T4.ai_upc as upc ,T4.ai_create_date as ai_day,T5.ai_create_date as ai_nextday,T5.ai_week_date as ai_weekday from salves_volume_day T4 left join salves_volume_day T5 on T4.ai_shop_id  = T5.ai_shop_id  and T4.ai_upc = T5.ai_upc and T4.ai_next_date = T5.ai_create_date ) T6 where T6.ai_day_nums is not null and T6.ai_next_nums is not null and T6.shop_id is not null and T6.ai_day is not null and T6.ai_nextday is not null and T6.upc != '' and T6.ai_weekday is not null")
        sql_dataf.show(10)
        # enc = OneHotEncoder(categorical_features="ai_weekday")
        # MeanEncoder = mean_enchder.MeanEncoder(["shop_id", "upc"], n_splits=5, target_type='regression',
        #                                        prior_weight_func=None)
        sql_dataf = sql_dataf.select(sql_dataf.shop_id.cast("double"),
                                     sql_dataf.ai_day_nums.cast("double"), sql_dataf.ai_next_nums.cast("double"),
                                     sql_dataf.upc.cast("double"), sql_dataf.ai_weekday.cast("int"))
        # y_dataf = sql_dataf.select("ai_next_nums")
        sql_dataf = sql_dataf.toPandas()
        # y_dataf = y_dataf.toPandas()
        # sql_dataf = enc.fit(pd.Series(sql_dataf['ai_weekday']).values.reshape(-1,1))
        sql_dataf = MeanEncoder.fit_transform(sql_dataf, sql_dataf['ai_next_nums'])
        value = sql_dataf.values.tolist()
        column = list(sql_dataf.columns)
        sql_dataf = self.sqlsc.createDataFrame(value, column)
        sql_dataf.show(10)
        assembler = VectorAssembler(inputCols=["ai_day_nums", "shop_id_pred", "upc_pred", "ai_weekday"],
                                    outputCol="features")
        output = assembler.transform(sql_dataf)
        train_feature = output.select("features", "ai_next_nums").toDF('features', 'label')
        print(train_feature.show(10))
        return train_feature, MeanEncoder


if __name__=='__main__':
    sql = "(SELECT  count(1) FROM   ( SELECT sum(T2.t1_nums) AS ai_nums,  T2.t1_shop_id AS ai_shop_id,T3.upc AS ai_upc, T2.t1_create_date AS ai_create_date, DATE_FORMAT(  from_unixtime(  unix_timestamp(   DATE_FORMAT(  T2.t1_create_date,'%Y-%m-%d' )  ) + 24 * 3600 ), '%Y-%m-%d'          ) AS ai_next_date       FROM            (               SELECT                  sum(T1.nums) AS t1_nums,                    T1.shop_id AS t1_shop_id,                   T1.goods_id,                    T1.create_date AS t1_create_date                FROM                    (                       SELECT                          number nums,                            shop_id,                            goods_id,                           DATE_FORMAT(create_time, '%Y-%m-%d') create_date                        FROM                            payment_detail                      WHERE                           shop_id IS NOT NULL                         AND goods_id IS NOT NULL                        AND number > 0                      AND create_time > '2019-06-01 00:00:00'                         AND create_time < '2019-09-01 00:00:00'                         AND payment_id IN (                             SELECT DISTINCT                                 (payment.id)                            FROM                                payment                             WHERE                               payment.type != 50                          AND create_time > '2019-06-01 00:00:00'                             AND create_time < '2019-09-01 00:00:00'                         )                   ) T1                GROUP BY                    T1.shop_id,                     T1.goods_id,                    T1.create_date          ) T2        LEFT JOIN shop_goods T3 ON T2.t1_shop_id = T3.shop_id       AND T2.goods_id = T3.goods_id       WHERE           T3.upc != ''        GROUP BY            T2.t1_create_date,          T2.t1_shop_id,          T3.upc  ) T8) tmp "
    salves_ins = Salves()
    sql_dataf = salves_ins.get_data_from_mysql(sql)
    sql_dataf.show(10)