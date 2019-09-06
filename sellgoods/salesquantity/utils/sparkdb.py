from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from set_config import config
#
# from sellgoods.sql import sales_quantity
# spark_context = config.shellgoods_params['spark_context']
db_context = config.db_context
# db_context = config.db_context
class SparkDb:
    def get_spark_context(self):
        # sc = SparkContext(spark_context, sc_name)
        # sc = SparkSession.builder.master(spark_context).appName(self.sc_name).config('spark.executor.memory','2g').getOrCreate()
        # sc = ss.sparkContext()
        sc = SparkContext()
        sc.setSystemProperty('spark.executor.memory', '6g')
        sc.setSystemProperty('spark.driver.memory', '4g')
        sc.setSystemProperty('spark.worker.memory', '8g')
        sc.setSystemProperty('spark.driver.maxResultsSize', '0')
        sc.setSystemProperty('spark.executor.cores', '6')
        sc.setSystemProperty('spark.shuffle.memoryFraction', '0')
        return sc
    def get_sparksql_context(self,sc):
        sqlContext = SQLContext(sc)
        return sqlContext
    def  get_data_frame(self,sql,sqlContext):
        df = sqlContext.read.format("jdbc").options(url=db_context["url"],
                                                        driver=db_context["driver"],
                                                        # dbtable="(SELECT code,title,description FROM project) tmp",
                                                        dbtable=sql,
                                                        user=db_context["user"], password=db_context["password"]).load()
        return df
