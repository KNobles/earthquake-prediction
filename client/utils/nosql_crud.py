import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, ContainerProxy, PartitionKey

load_dotenv()

endpoint = os.environ["NOSQL_ENDPOINT"]
key = os.environ["NOSQL_KEY"]

# Connect to the "raw_tweets" database and "tweets" container
def connect(endpoint:str, key:str) -> ContainerProxy:
    client = CosmosClient(endpoint, key)
    database_name = "raw_tweets"
    container_name = "tweets"
    partition_key = PartitionKey(path="/id")
    database = client.create_database_if_not_exists(id=database_name)
    container:ContainerProxy = database.create_container_if_not_exists(id=container_name, partition_key=partition_key)
    return container

# Inserts tweet to DB
def insert_tweet(tweet_dict:dict):
    container = connect(endpoint=endpoint, key=key)
    container.create_item(tweet_dict)
