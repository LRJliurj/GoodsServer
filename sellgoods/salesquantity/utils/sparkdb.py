from pyspark import SparkContext
from pyspark.sql import SQLContext
from set_config import config
from pyspark.sql import SparkSession
from sellgoods.sql import sales_quantity
spark_context = config.shellgoods_params['spark_context']
db_context = config.db_context
# db_context = config.db_context
class sparkdb_util:
    sc_name = ""
    def __init__(self,sc_name):
        self.sc_name = sc_name
    def get_spark_context(self):
        # sc = SparkContext(spark_context, sc_name)
        sc = SparkSession.builder.master(spark_context).appName(self.sc_name).config('spark.executor.memory','2g').getOrCreate()
        return sc

    def  get_data_frame(self,sql):
        sqlContext = SQLContext(self.get_spark_context())
        df = sqlContext.read.format("jdbc").options(url=db_context["url"],
                                                        driver=db_context["driver"],
                                                        # dbtable="(SELECT code,title,description FROM project) tmp",
                                                        dbtable=sql,
                                                        user=db_context["user"], password=db_context["password"]).load()
        # df.filter()
        print (df.select().show(2))
        return df

    def sql_context(self,sc):
        jdbcdf = sc.read.format('jdbc').option(url=db_context["url"], user=db_context["user"], password=db_context["password"]).option('dbtable', 'class').load()
        return jdbcdf
