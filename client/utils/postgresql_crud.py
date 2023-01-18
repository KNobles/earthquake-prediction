import os
import time
import random
import psycopg2

from dotenv import load_dotenv
from faker import Faker
from faker.providers.geo import Provider

fake = Provider(Faker())

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

# Create a table

# cursor.execute("CREATE TABLE tweet_info(id VARCHAR PRIMARY KEY, latitude DECIMAL(7,5), longitude DECIMAL(8,5));")
# print("Finished creating table")
def delete_content():
    cursor.execute("TRUNCATE tweet_info;")
    conn.commit()

# delete_content()
count = 0
while True:
    try:
        count += 1
        id_rand = str(random.randint(1000000, 1999999))
        rand_coord = fake.location_on_land()
        print(f"id: {id_rand}, lat: {float(rand_coord[0])}, lon: {float(rand_coord[1])}")
        
        cursor.execute(f"INSERT INTO tweet_info (id, latitude, longitude) VALUES ({id_rand},{float(rand_coord[0])}, {float(rand_coord[1])});")
        conn.commit()
        time.sleep(3)

        if (count == 20):
            delete_content()

    except KeyboardInterrupt as kb:
        cursor.close()
        conn.close()

