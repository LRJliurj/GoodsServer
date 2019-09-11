sql_params={
    #基于upc的训练sql
    "upc_data_sql":"(select sum(T2.t1_nums) as ai_nums,T2.t1_shop_id as ai_shop_id ,T3.upc as ai_upc,T2.t1_create_date as  ai_create_date,DATE_FORMAT( from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))+24*3600),'%Y-%m-%d') as ai_next_date,DAYOFWEEK(DATE_FORMAT(from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))-24*3600),'%Y-%m-%d')) as ai_week_date from ( "
                    "select sum(T1.nums) as t1_nums,T1.shop_id as t1_shop_id,T1.shop_goods_id,T1.create_date as t1_create_date  from "
		                "(select number nums,shop_id,shop_goods_id,DATE_FORMAT(create_time,'%Y-%m-%d') 	create_date from payment_detail "
                                "where shop_id is not null and goods_id is not null and number > 0 and create_time > '2019-07-31 00:00:00' and create_time < '2019-08-31 00:00:00' and "
				                "payment_id in ( "
                                    "select distinct(payment.id) from payment where payment.type != 50  and create_time > '2019-07-31 00:00:00' and create_time < '2019-08-31 00:00:00' "
											") "
                        ")  T1 "
		                "group by T1.shop_id,T1.shop_goods_id,T1.create_date) T2 "
                    "left join  shop_goods T3 on T2.t1_shop_id= T3.shop_id and T2.shop_goods_id = T3.id "
                    "where T3.upc != '' and  T3.upc != '0' "
                    "group by T2.t1_create_date,T2.t1_shop_id,T3.upc) tmp",


    "upc_data_sql_test":"(select sum(T2.t1_nums) as ai_nums,T2.t1_shop_id as ai_shop_id ,T3.upc as ai_upc,T2.t1_create_date as  ai_create_date,DATE_FORMAT( from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))+24*3600),'%Y-%m-%d') as ai_next_date,DAYOFWEEK(DATE_FORMAT(from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))-24*3600),'%Y-%m-%d')) as ai_week_date from ( "
                    "select sum(T1.nums) as t1_nums,T1.shop_id as t1_shop_id,T1.shop_goods_id,T1.create_date as t1_create_date  from "
		                "(select number nums,shop_id,shop_goods_id,DATE_FORMAT(create_time,'%Y-%m-%d') 	create_date from payment_detail "
                                "where shop_id is not null and goods_id is not null and number > 0 and create_time >= '2019-08-31 00:00:00' and create_time < '2019-09-02 00:00:00' and "
				                "payment_id in ( "
                                    "select distinct(payment.id) from payment where payment.type != 50  and create_time >= '2019-08-31 00:00:00' and create_time < '2019-09-02 00:00:00' "
											") "
                        ")  T1 "
		                "group by T1.shop_id,T1.shop_goods_id,T1.create_date) T2 "
                    "left join  shop_goods T3 on T2.t1_shop_id= T3.shop_id and T2.shop_goods_id = T3.id "
                    "where T3.upc != '' and  T3.upc != '0' "
                    "group by T2.t1_create_date,T2.t1_shop_id,T3.upc) tmp",

    #基于upc的预测sql
    "upc_predict_sql":"(select sum(T2.t1_nums) as ai_nums,T2.t1_shop_id as ai_shop_id ,T3.upc as ai_upc,T2.t1_create_date as  ai_create_date,DATE_FORMAT( from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))+24*3600),'%Y-%m-%d') as ai_next_date,DAYOFWEEK(DATE_FORMAT(from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))-24*3600),'%Y-%m-%d')) as ai_week_date from ( "
                            "select sum(T1.nums) as t1_nums,T1.shop_id as t1_shop_id,T1.goods_id,T1.create_date as t1_create_date  from "
		                        "(select number nums,shop_id,goods_id,DATE_FORMAT(create_time,'%Y-%m-%d') 	create_date from payment_detail "
                                    "where shop_id is not null and shop_goods_id is not null and number > 0  and "
				                    "payment_id in ( "
                                        "select payment.id from payment where payment.type != 50  and TO_DAYS( NOW( ) ) - TO_DAYS( create_time ) <= 3 "
											") "
                            ")  T1 "
		                    "group by T1.shop_id,T1.goods_id,T1.create_date) T2 "
                        "left join  shop_goods T3 on T2.t1_shop_id= T3.shop_id and T2.goods_id = T3.goods_id "
                        "where T3.upc != '' "
                        "group by T2.t1_create_date,T2.t1_shop_id,T3.upc ) tmp1",



    #基于upc的shopid 测试sql
    "upc_data_sql_shopid":"(select sum(T2.t1_nums) as ai_nums,T2.t1_shop_id as ai_shop_id ,T3.upc as ai_upc,T2.t1_create_date as  ai_create_date,DATE_FORMAT( from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))+24*3600),'%Y-%m-%d') as ai_next_date,DAYOFWEEK(DATE_FORMAT(from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))-24*3600),'%Y-%m-%d')) as ai_week_date from ( "
                    "select sum(T1.nums) as t1_nums,T1.shop_id as t1_shop_id,T1.shop_goods_id,T1.create_date as t1_create_date  from "
		                "(select number nums,shop_id,shop_goods_id,DATE_FORMAT(create_time,'%Y-%m-%d') 	create_date from payment_detail "
                                "where shop_id = 3607 and goods_id is not null and number > 0 and create_time > '2019-08-01 00:00:00' and create_time < '2019-09-01 00:00:00' and "
				                "payment_id in ( "
                                    "select distinct(payment.id) from payment where payment.type != 50  and create_time > '2019-08-01 00:00:00' and create_time < '2019-09-01 00:00:00' "
											") "
                        ")  T1 "
		                "group by T1.shop_id,T1.shop_goods_id,T1.create_date) T2 "
                    "left join  shop_goods T3 on T2.t1_shop_id= T3.shop_id and T2.shop_goods_id = T3.id "
                    "where T3.upc != '' and  T3.upc != '0' "
                    "group by T2.t1_create_date,T2.t1_shop_id,T3.upc) tmp",
}