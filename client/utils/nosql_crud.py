import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, ContainerProxy, PartitionKey
import json
import re
import pandas as pd

load_dotenv()

endpoint = os.environ["NOSQL_ENDPOINT"]
key = os.environ["NOSQL_KEY"]

# Connect to the "raw_tweets" database and "tweets" container
def connect(endpoint:str, key:str) -> ContainerProxy:
    client = CosmosClient(endpoint, key)
    database_name = "raw_tweets"
    container_name = "tweets_db"
    partition_key = PartitionKey(path="/id")
    database = client.create_database_if_not_exists(id=database_name)
    container:ContainerProxy = database.create_container_if_not_exists(id=container_name, partition_key=partition_key)
    return container

# Inserts tweet to DB
def insert_tweet(tweet_dict:dict, tweet_id:int):
    container = connect(endpoint=endpoint, key=key)
    print('firsthere------------------')
    if (tweet_id != 0):
        print("tweet dict collect ",tweet_dict.collect()[0][0])
        json_object = tweet_dict.collect()[0][0]
        print("type: ",type(json_object))
        tweet_dumps = json.dumps(eval(json_object))
        tweet_json = json.loads(tweet_dumps)
        print("tweet json: ",tweet_json)
        print("type: ",type(tweet_json))
        container.create_item(tweet_json)

#search for tweets
def query_items(query_type,query):
    container = connect(endpoint=endpoint, key=key)
    items = list(container.query_items(
        query="SELECT * FROM r WHERE r." + query_type + "=@query OR r." + query_type + " LIKE '%" + query + "%'",
        parameters=[
            {"name":"@query", "value": query},
            
        ],
        enable_cross_partition_query=True
    ))
    return items

#query the whole database
def query_database():
    container = connect(endpoint=endpoint, key=key)
    items = list(container.query_items(
        query="SELECT * FROM r",
        enable_cross_partition_query=True
    ))
    df = pd.DataFrame(items)
    df.to_csv("dataframe.csv")
    return print('Database copied')

#ONLY FOR WRONGLY STRUCTURED TWEETS
def delete_wrongly_structured_tweets():
    container = connect(endpoint=endpoint, key=key)
    items = list(container.query_items(
        query="SELECT c.id from c where IS_DEFINED(c.tweet_raw) = false",
        enable_cross_partition_query=True
    ))
    id_list = [d['id'] for d in items]
    for item_id in id_list:
        response = container.delete_item(item=item_id, partition_key=item_id)
    return print(f"{id_list} has been deleted")



