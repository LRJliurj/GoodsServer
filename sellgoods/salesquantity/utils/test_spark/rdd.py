from sellgoods.salesquantity.utils.test_spark import test1
from pyspark.ml.feature import VectorAssembler
from pyspark.mllib.regression import LabeledPoint,Vectors
def filter():
    df,sc = test1.exe()
    df = df.select(df.ai_shop_id.cast("double"),df.ai_create_date.cast("double"),df.ai_nums.cast("double"))
    assembler = VectorAssembler(inputCols=["ai_nums"],outputCol="features")
    output = assembler.transform(df)
    train_feature,test_features = output.select("features", "ai_nums").toDF('features','label').randomSplit([7.0, 3.0],100)
    print (train_feature.show(10))
    # print (label_features.label)
    labelpointRDD = train_feature.rdd.map(lambda row: LabeledPoint(row['label']/1000000,  Vectors.dense([row['features'][0]/1000000])))
    print (labelpointRDD.collect())
    return labelpointRDD,sc