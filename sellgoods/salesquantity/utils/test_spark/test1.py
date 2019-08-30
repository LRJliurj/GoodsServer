from sellgoods.salesquantity.utils import sparkdb

def exe():
    sc_name = "app222"
    db = sparkdb.sparkdb_util(sc_name)
    sc = db.get_spark_context()
    # df = db.get_data_frame("(select sum(number) as nums,shop_id,shop_goods_id from payment_detail "
    #                     "where shop_id is not null and shop_goods_id is not null and number > 0 and "
    #                     "payment_id in ( "
    #                      "select payment.id from payment where payment.type != 50)  tmp")
    df = db.get_data_frame("(SELECT shop_id from payment) tmp")
    print (df.select.show(2))