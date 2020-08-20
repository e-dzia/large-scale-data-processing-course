"""Sample pySpark app2."""

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors, VectorUDT

from ml_models import linear_regression, binary_classification, \
    multiclass_classification

debug = True

conf = SparkConf().setAppName('appName').setMaster('local')\
    .set("spark.jars.packages",
         "org.mongodb.spark:mongo-spark-connector_2.11:2.3.2")
sc = SparkContext(conf=conf)

sc.setLogLevel("ERROR")

mongo_uri = "mongodb://root:toor@mongodb:27017"
database_name = "reddit"
collection_name = "posts"

spark = SparkSession.builder\
    .appName('appName')\
    .config("spark.mongodb.input.uri", mongo_uri) \
    .config("spark.mongodb.input.database", database_name)\
    .config("spark.mongodb.input.collection", collection_name)\
    .getOrCreate()

data = spark.read \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .option('sampleSize', '50000') \
    .load()

spark.udf.register("vectorize_udf", lambda vs: Vectors.dense(vs), VectorUDT())

train_set, test_set = data.randomSplit([0.8, 0.2], seed=12)

print("##### Linear Regression #####")
lr_results = linear_regression(train_set, test_set, debug)
print("Linear Regression | RMSE (test, train): {}".format(lr_results))

print("##### Binary Classification #####")
lr_results = binary_classification(train_set, test_set, debug)
print("Binary Classification | F1: {}".format(lr_results))

print("##### Multiclass Classification #####")
lr_results = multiclass_classification(train_set, test_set, debug)
print("Multiclass Classification | F1: {}".format(lr_results))
print("Classification ended")
