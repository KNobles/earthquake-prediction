import os
import time
import random
import psycopg2
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

host = os.environ["PSQL_HOST"]
dbname = os.environ["PSQL_DB_NAME"]
user = os.environ["PSQL_USERNAME"]
password = os.environ["PSQL_PW"]
sslmode = "require"

# Construct connection string
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")


# TODO Create a Sample table which has the same columns but only ~500 items
# Create a table
def create_table():
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS tweet_processed_ml(
    ml_tweet_id VARCHAR PRIMARY KEY,
    ml_translated_text TEXT, 
    ml_geo_lat DECIMAL(7,5), 
    ml_geo_lng DECIMAL(8,5),
    ml_magnitude DECIMAL(3,1),
    ml_date DATE,
    ml_time TIME,
    ml_label SMALLINT);""")
    print("Finished creating table")
    conn.commit()
    cursor.close()

def delete_content():
    cursor = conn.cursor()
    cursor.execute("TRUNCATE tweet_info;")
    conn.commit()
    cursor.close()

def insert_data(data:dict):
    cursor = conn.cursor()
    id = data["id"]
    text = data["text"]
    lat = data["lat"]
    long = data["long"]
    date = data["date"] # yyyy-mm-dd
    time = data["time"] # hh:mm:ss
    label = data["label"]
    query = """INSERT INTO tweet_processed_ml
    (ml_tweet_id, ml_translated_text, ml_geo_lat, ml_geo_lng, ml_date, ml_time, ml_label) 
    VALUES (%s,%s, %s, %s, %s, %s, %s) ON CONFLICT(ml_tweet_id) DO NOTHING;"""
    cursor.execute(query, (id, text, lat, long, date, time, label))
    conn.commit()
    cursor.close()

# TODO to delete, just for testing purposes
def get_all_table():
    cursor = conn.cursor()
    cursor.execute("""SELECT COUNT(*) FROM tweet_info;""")
    result = cursor.fetchall()
    print(result)
    conn.commit()
    cursor.close()

#get_all_table()
#create_table()
# insert_data({"id":'hjkdchjkd', "text":"henloo", "lat":88.0003, "date":"2023-01-20", "time":"14:22:37"})