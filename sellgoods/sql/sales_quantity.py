sql_params={

    #基于商店的训练sql
    "train_data_sql":"(select sum(T2.t1_nums) as ai_nums,T2.t1_shop_id as ai_shop_id ,T2.t1_create_date as  ai_create_date,DATE_FORMAT( from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))+24*3600),'%Y-%m-%d') as ai_next_date from ( "
                            "select sum(T1.nums) as t1_nums,T1.shop_id as t1_shop_id,T1.shop_goods_id,T1.create_date as t1_create_date  from "
		                        "(select number nums,shop_id,shop_goods_id,DATE_FORMAT(create_time,'%Y-%m-%d') 	create_date from payment_detail "
                                "where shop_id is not null and shop_goods_id is not null and number > 0 and  "					     					       
				                "payment_id in ( "	
                                "select payment.id from payment where payment.type != 50  and create_time > '2019-07-01 00:00:00' "
											")"
                            " )  T1 "
		                    "group by T1.shop_id,T1.shop_goods_id,T1.create_date) T2 "
                        "left join  shop_goods T3 on T2.t1_shop_id= T3.shop_id "
                        "group by T2.t1_create_date,T2.t1_shop_id) tmp",
    #基于商店的预测sql
    "predict_data_sql":"(select sum(T2.t1_nums) as ai_nums,T2.t1_shop_id as ai_shop_id ,T2.t1_create_date as  ai_create_date,DATE_FORMAT( from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))+24*3600),'%Y-%m-%d') as ai_next_date from ( "
                            "select sum(T1.nums) as t1_nums,T1.shop_id as t1_shop_id,T1.shop_goods_id,T1.create_date as t1_create_date  from "
		                        "(select number nums,shop_id,shop_goods_id,DATE_FORMAT(create_time,'%Y-%m-%d') 	create_date from payment_detail "
                                "where shop_id is not null and shop_goods_id is not null and number > 0 and  "					     					       
				                "payment_id in ( "	
                                "select payment.id from payment where payment.type != 50  and TO_DAYS( NOW( ) ) - TO_DAYS( create_time ) <= 2   "
											")"
                            " )  T1 "
		                    "group by T1.shop_id,T1.shop_goods_id,T1.create_date) T2 "
                        "left join  shop_goods T3 on T2.t1_shop_id= T3.shop_id "
                        "group by T2.t1_create_date,T2.t1_shop_id) tmp1",


    #基于upc的训练sql
    "upc_data_sql":"select sum(T2.t1_nums) as ai_nums,T2.t1_shop_id as ai_shop_id ,T3.upc as ai_upc,T2.t1_create_date as  ai_create_date,DATE_FORMAT( from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))+24*3600),'%Y-%m-%d') as ai_next_date from ( "
                    "select sum(T1.nums) as t1_nums,T1.shop_id as t1_shop_id,T1.goods_id,T1.create_date as t1_create_date  from "
		                "(select number nums,shop_id,goods_id,DATE_FORMAT(create_time,'%Y-%m-%d') 	create_date from payment_detail "
                                "where shop_id is not null and goods_id is not null and number > 0 and "
				                "payment_id in ( "
                                    "select distinct(payment.id) from payment where payment.type != 50  and create_time > '2019-08-01 00:00:00' and create_time < '2019-09-01 00:00:00' "
											") "
                        ")  T1 "
		                "group by T1.shop_id,T1.goods_id,T1.create_date) T2 "
                    "left join  shop_goods T3 on T2.t1_shop_id= T3.shop_id and T2.goods_id = T3.goods_id "
                    "where T3.upc != '' "
                    "group by T2.t1_create_date,T2.t1_shop_id,T3.upc",

    # "upc_data_sql":"select sum(T2.t1_nums) as ai_nums,T2.t1_shop_id as ai_shop_id ,T3.upc as ai_upc,FROM_UNIXTIME(T2.t1_create_date,'yyyy-MM-dd') as  ai_create_date,FROM_UNIXTIME((T2.t1_create_date+24*3600),'yyyy-MM-dd') as ai_next_date from ( "
    #                 "select sum(T1.nums) as t1_nums,T1.shop_id as t1_shop_id,T1.goods_id,T1.create_date as t1_create_date  from "
		#                 "(select number nums,shop_id,goods_id,create_date from payment_detail "
    #                             "where shop_id is not null and goods_id is not null and number > 0 and "
		# 		                "payment_id in ( "
    #                                 "select distinct(payment.id) from payment "
		# 									") "
    #                     ")  T1 "
		#                 "group by T1.shop_id,T1.goods_id,T1.create_date) T2 "
    #                 "left join  shop_goods T3 on T2.t1_shop_id= T3.shop_id and T2.goods_id = T3.goods_id "
    #                 "where T3.upc != '' "
    #                 "group by T2.t1_create_date,T2.t1_shop_id,T3.upc",


    # "upc_data_sql":"select sum(T2.t1_nums) as ai_nums,T2.t1_shop_id as ai_shop_id ,T3.upc as ai_upc,T2.t1_create_date as ai_create_date,DATE_FORMAT(from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))+24*3600),'%Y-%m-%d') as ai_next_date from (select sum(T1.nums) as t1_nums,T1.shop_id as t1_shop_id,T1.goods_id,T1.create_date as t1_create_date  from (select number nums,shop_id,goods_id,DATE_FORMAT(create_time,'%Y-%m-%d') create_date from payment_detail  where shop_id is not null and goods_id is not null and number > 0 and create_time > '2019-08-01 00:00:00' and create_time < '2019-09-01 00:00:00'  and payment_id in ( select distinct(payment.id) from payment where payment.type != 50  and create_time > '2019-08-01 00:00:00' and create_time < '2019-09-01 00:00:00') )  T1  group by T1.shop_id,T1.goods_id,T1.create_date) T2 left join  shop_goods T3 on T2.t1_shop_id= T3.shop_id and T2.goods_id = T3.goods_id where T3.upc != '' group by T2.t1_create_date,T2.t1_shop_id,T3.upc",
    #基于upc的训练sql
    "upc_data_sql1":"(select number,shop_id,goods_id,payment_id,unix_timestamp(DATE_FORMAT(create_time,'%Y-%m-%d')) as create_date,unix_timestamp(date_sub(DATE_FORMAT(create_time,'%Y-%m-%d'),interval -1 day)) as next_day from payment_detail where create_time > '2019-08-01 00:00:00' and create_time < '2019-09-01 00:00:00') payment_detail",
    "upc_data_sql2":"(select payment.id,payment.type from payment where payment.type != 50  and create_time > '2019-08-01 00:00:00' and create_time < '2019-09-01 00:00:00') payment",
    "upc_data_sql3":"(select shop_id,upc,goods_id from shop_goods ) shop_goods",
    #基于upc的预测sql
    "upc_predict_sql":"(select sum(T2.t1_nums) as ai_nums,T2.t1_shop_id as ai_shop_id ,T3.upc as ai_upc,T2.t1_create_date as  ai_create_date,DATE_FORMAT( from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))+24*3600),'%Y-%m-%d') as ai_next_date from ( "
                            "select sum(T1.nums) as t1_nums,T1.shop_id as t1_shop_id,T1.goods_id,T1.create_date as t1_create_date  from "
		                        "(select number nums,shop_id,goods_id,DATE_FORMAT(create_time,'%Y-%m-%d') 	create_date from payment_detail "
                                    "where shop_id is not null and shop_goods_id is not null and number > 0 and "
				                    "payment_id in ( "
                                        "select payment.id from payment where payment.type != 50  and TO_DAYS( NOW( ) ) - TO_DAYS( create_time ) <= 3 "
											") "
                            ")  T1 "
		                    "group by T1.shop_id,T1.goods_id,T1.create_date) T2 "
                        "left join  shop_goods T3 on T2.t1_shop_id= T3.shop_id and T2.goods_id = T3.goods_id "
                        "where T3.upc != '' "
                        "group by T2.t1_create_date,T2.t1_shop_id,T3.upc ) tmp1",
}