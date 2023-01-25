from psycopg2 import connect
import os
from dotenv import load_dotenv

load_dotenv()

#establishing the connection
conn = psycopg2.connect(
    database= os.environ["dbname"]
    user= os.environ["user"]
    password=os.environ["password"]
    host=os.environ["host"]
    port=os.environ["port"]
)

cursor = conn.cursor()

def read_database(cursor):
    psotgreSQL_select_query = "select * from processed_tweets"