from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from utils.nosql_crud import *
import os
from dotenv import load_dotenv
import json

load_dotenv()

endpoint = os.environ["NOSQL_ENDPOINT"]
key = os.environ["NOSQL_KEY"]

# Set localhost socket parameters from ther server
HOST = "127.0.0.1"
PORT = 9090

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

# streamQuery = stream.writeStream.format("cosmos.oltp")\
#     .option("spark.cosmos.container", "tweets")\
#     .option("checkpointLocation", "/tmp/myRunId/")\
#     .outputMode("append")\
#     .start()
# def func(batch_df, batch_id):
#   batch_df


# tweet = json.load(test.json)

# insert_tweet()