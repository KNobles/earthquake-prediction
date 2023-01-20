import os
import time
import random
import psycopg2

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

cursor = conn.cursor()

# TODO Create a Sample table which has the same columns but only ~500 items
# TODO Create tweet_info table which will have the data processed by the ML sent live
# Create a table
def create_table():
    cursor.execute("""
CREATE TABLE IF NOT EXISTS tweet_info(
    tweet_id VARCHAR PRIMARY KEY,
    translated_text TEXT, 
    geo_lat DECIMAL(7,5), 
    get_lng DECIMAL(8,5),
    magnitude DECIMAL(3,1),
    date DATE,
    time TIME);""")
    print("Finished creating table")
    conn.commit()

def delete_content():
    cursor.execute("TRUNCATE tweet_info;")
    conn.commit()

def insert_data(data:dict):
    id = data["id"]
    text = data["text"]
    lat = data["lat"]
    date = data["date"] # yyyy-mm-dd
    time = data["time"] # hh:mm:ss
    query = """INSERT INTO tweet_info (tweet_id, translated_text, geo_lat, date, time) 
    VALUES (%s,%s, %s, %s, %s);"""
    cursor.execute(query, (id, text, lat, date, time))
    conn.commit()
    cursor.close()
    conn.close()



# insert_data({"id":'hjkdchjkd', "text":"henloo", "lat":88.0003, "date":"2023-01-20", "time":"14:22:37"})