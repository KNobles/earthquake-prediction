import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, ContainerProxy, DatabaseProxy, PartitionKey

load_dotenv()

endpoint = os.environ["NOSQL_ENDPOINT"]
key = os.environ["NOSQL_KEY"]
database_name = "raw_tweets"
container_name = "tweets"

# Connect to the "raw_tweets" database and "tweets" container
def connect(endpoint:str, key:str, database_name:str, container_name:str) -> ContainerProxy:
    client = CosmosClient(endpoint, key)
    partition_key = PartitionKey(path="/id")
    database:DatabaseProxy = client.get_database_client(database=database_name)
    container:ContainerProxy = database.get_container_client(id=container_name, partition_key=partition_key)
    return container

# Inserts tweet to DB
def insert_tweet(tweet_dict:dict):
    container = connect(endpoint=endpoint, key=key, database_name=database_name, container_name=container_name)
    container.create_item(tweet_dict)
