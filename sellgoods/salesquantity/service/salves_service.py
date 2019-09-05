from sellgoods.salesquantity.utils import sparkdb
from sellgoods.salesquantity.utils import salves_volume
from sellgoods.salesquantity.model import regressor
from set_config import config
from sellgoods.salesquantity.utils import mysql_util
import math
regressor_model_path = config.shellgoods_params['regressor_model_path']
online_model_name = config.shellgoods_params['online_model_name']
sdb = sparkdb.SparkDb()
salves_ins = salves_volume.Salves()
regressor_ins = regressor.Regressor()
class Salves:
    model=None
    def __init__(self):
        self.model = regressor_ins.load_model(regressor_model_path[online_model_name])
    def predict(self):
       feature,online_df = salves_ins.get_online_features3()
       result = self.model.transform(feature)
       result = result.select('prediction')
       sql_dfl = []
       for row1,row2 in zip(online_df.collect(),result.collect()):
           df1={}
           df1['shop_id'] = list(row1)[0]
           df1['class_three_id'] = 1
           df1['predict_sales'] = math.floor(list(row2)[0])
           df1['create_date'] = list(row1)[-1]
           df1['upc'] = list(row1)[-3]
           sql_dfl.append((
               int(df1['shop_id']),
               int(df1['class_three_id']),
               int( df1['predict_sales']),
               str(df1['create_date']),
               str(df1['upc'])
           ))
       print (sql_dfl)
       mysql_ins = mysql_util.MysqlUtil()
       cur = mysql_ins.cursor
       mysql_ins.insert_many(cur,sql_dfl)


if __name__=='__main__':
    salves = Salves()
    salves.predict()

