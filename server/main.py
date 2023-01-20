import os
import json
import socket
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
from utils.query_for_twitter import query_for_twitter

load_dotenv()

bearer_token = os.environ["BEARER_TOKEN"]
endpoint_get = "https://api.twitter.com/2/tweets/search/stream"
endpoint_rules = "https://api.twitter.com/2/tweets/search/stream/rules"

# Set localhost socket parameters
HOST = os.environ.get("HOST", "127.0.0.1")
# HOST = "127.0.0.1"
PORT = 9095

print("="*100)
print(f"HOST = {HOST}")
print("="*100)

# TODO Create a function for the server (useful if it crashes so we call it again)

print(f"Listening to port {PORT}...")
# Create local socket
local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_socket.bind((HOST, PORT))
local_socket.listen(1)
conn, addr = local_socket.accept()
print("Connected by", addr)

#Body to add into Post request (so this is not "parameter" but "json" part in your Post request)
query_parameters = query_for_twitter

def request_headers(bearer_token: str) -> dict:
    """
    Sets up the request headers. 
    Returns a dictionary summarising the bearer token authentication details.
    """
    return {"Authorization": "Bearer {}".format(bearer_token)}

def connect_to_endpoint(endpoint_url: str, headers: dict, parameters: dict) -> json:
    """
    Connects to the endpoint and post customized filter for tweet search.
    Returns a json with data to show if your custom filter rule is created.
    
    """
    response = requests.post(url=endpoint_url, headers=headers, json=parameters)
    
    return response.json()

def get_tweets(url,headers):
    """
    Fetch real-time tweets based on your custom filter rule.
    Returns a Json format data where you can find Tweet id, text and some metadata.
    Sends the data to your defined local port where Spark reads streaming data.
    """
    params = {
    'tweet.fields':'geo,lang',
    'expansions':'author_id,geo.place_id',
    'user.fields':'username'
    }

    get_response = requests.get(url=url,headers=headers,stream=True, params=params)

    if get_response.status_code!=200:
        print(f"TWITTER API CODE: {get_response.status_code}")
    
    else:
        for line in get_response.iter_lines():
            if line==b'':
                pass
            else:
                try:
                    json_response = json.loads(line)
                    
                    tweet_id = json_response["data"]["id"]
                    tweet_text = json_response["data"]["text"]
                    tweet_lang = json_response["data"]["lang"]
                    tweet_username = json_response["includes"]["users"][0]["username"]
                    tweet_geo = json_response["data"]["geo"]

                    data_to_send = {
                        "id":tweet_id, 
                        "text":tweet_text, 
                        "lang":tweet_lang, 
                        "username":tweet_username, 
                        "geo":tweet_geo
                    }
                    
                    data_to_send_str = str(data_to_send) + "\n"
                    print(data_to_send_str)
                    
                    conn.send(bytes(data_to_send_str,'utf-8'))
                except Exception as e:
                    # TODO Call the server function and get_tweets here.
                    print(e)

headers = request_headers(bearer_token)
json_response = connect_to_endpoint(endpoint_rules, headers, query_for_twitter)
get_tweets(endpoint_get,headers)