import os
from pyspark.sql import SparkSession
from utils.nosql_crud import insert_tweet

# Set localhost socket parameters from ther server
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = 9095

# Create Spark session
spark = SparkSession.builder.appName("Twitter Stream Reader").getOrCreate()

# Create streaming DataFrame from local socket
# delimiter added on server side
stream = spark.readStream.format("socket") \
    .option("host", HOST) \
    .option("port", PORT) \
    .option("delimiter", "\n") \
    .load()

query = stream.writeStream.format("console") \
  .option("truncate", False) \
  .outputMode("append") \
  .foreachBatch(insert_tweet)\
  .start() \
  .awaitTermination()