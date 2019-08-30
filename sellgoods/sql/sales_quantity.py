sql_params={
    "linear_regression":"select sum(T1.nums) as ai_thrid_nums ,T1.shop_id as ai_shop_id  from "
                            "(select sum(number) as nums,shop_id,shop_goods_id from payment_detail "
                                "where shop_id is not null and shop_goods_id is not null and number > 0 and "
                                "payment_id in ( "
                                    "select payment.id from payment where payment.type != 50  and create_time > '2019-07-01 00:00:00') "
                            "group by shop_id,shop_goods_id  ) T1 "
                        "left join  shop_goods T2 on T1.shop_id = T2.shop_id "
                        "and T1.shop_goods_id  = T2.goods_id "
                        "where T2.upc is not null  and T2.third_cate_id is not null group by T1.shop_id ,T2.third_cate_id"

}