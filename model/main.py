from utils.metadata_extraction import *
from utils.nosql_crud import *
import pandas as pd
import concurrent.futures
from utils.postgresql_crud import *

#TODO while

raw_tweets = query_cosmosdb("SELECT * FROM r WHERE r.ml_processed = false")  #Where label is False

for raw_tweet in raw_tweets:
    # translated_tweet = translate_tweet_f(raw_tweet)
    insert_metadata_in_db_from_csv(raw_tweet)
    update_tweet(raw_tweet)