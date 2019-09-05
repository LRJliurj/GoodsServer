from sellgoods.salesquantity.utils import sparkdb
from sellgoods.sql import sales_quantity
sqldemo = sales_quantity.sql_params['linear_regression']

def exe():
    sc_name = "app222"
    db = sparkdb.SparkDb(sc_name)
    sc = db.get_spark_context()
    # sc = db.get_spark_context()
    # df = db.get_data_frame("(select sum(number) as nums,shop_id,shop_goods_id from payment_detail "
    #                     "where shop_id is not null and shop_goods_id is not null and number > 0 and "
    #                     "payment_id in ( "
    #                      "select payment.id from payment where payment.type != 50)  tmp")
    df = db.get_data_frame(sqldemo,sc)
    print (df.collect())
    return df,sc

if __name__=="__main__":
    exe()