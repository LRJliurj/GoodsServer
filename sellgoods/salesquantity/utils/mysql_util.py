import pymysql
from set_config import config
dbcontext = config.db_context
class MysqlUtil:
    cursor = None
    conn = None
    def __init__(self):
        conn = pymysql.connect(
            host=dbcontext['host'],
            port=int(dbcontext['port']),
            user=dbcontext['user'],
            passwd=dbcontext['password'],
            db=dbcontext['database'],
            charset='utf8'
        )
        self.conn = conn
        self.cursor = conn.cursor()
    #cursor
    def insert_many(self,conn,data):
        cursor = self.cursor
        cursor.executemany('insert into ai_sales_goods (shop_id,class_three_id,predict_sales,create_date,upc) value(%s,%s,%s,%s,%s)',data)
        cursor.connection.commit()
        cursor.close()
        conn.close()
if __name__=='__main__':
    mysql_ins = MysqlUtil()
    data =  [(3220, 0, 155936, '2019-09-03')]
    mysql_ins.insert_many(mysql_ins.conn,data)
