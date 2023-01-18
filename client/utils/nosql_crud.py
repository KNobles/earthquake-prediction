import os
import json
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, ContainerProxy, DatabaseProxy, PartitionKey

load_dotenv()

endpoint = os.environ["NOSQL_ENDPOINT"]
key = os.environ["NOSQL_KEY"]

# Connect to the "raw_tweets" database and "tweets" container
def connect(endpoint:str, key:str) -> ContainerProxy:
    client = CosmosClient(endpoint, key)
    database_name = "raw_tweets"
    container_name = "tweets_db"
    partition_key = PartitionKey(path="/id")
    database:DatabaseProxy = client.create_database_if_not_exists(id=database_name)
    container:ContainerProxy = database.create_container_if_not_exists(id=container_name, partition_key=partition_key)
    return container

# Inserts tweet to DB
def insert_tweet(tweet_dict:dict, tweet_id:int):
    container = connect(endpoint=endpoint, key=key)
    if (tweet_id != 0):
        json_object = tweet_dict.collect()[0][0]
        tweet_dumps = json.dumps(eval(json_object))
        tweet_json = json.loads(tweet_dumps)
        container.create_item(tweet_json)