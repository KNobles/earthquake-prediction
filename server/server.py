import os
import json
import socket
import requests
from dotenv import load_dotenv
from utils.query import query_earthquake_translations

load_dotenv()

bearer_token = os.environ["BEARER_TOKEN"]
endpoint_get = "https://api.twitter.com/2/tweets/search/stream"
tweet_lookup_endpoint = "https://api.twitter.com/2/tweets/"
#URL to add rules for tweet search
endpoint_rules = "https://api.twitter.com/2/tweets/search/stream/rules"

# Set localhost socket parameters
HOST = "127.0.0.1"
PORT = 9090

# Create local socket
local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_socket.bind((HOST, PORT))
local_socket.listen(1)

conn, addr = local_socket.accept()
print("Connected by", addr)

#Body to add into Post request (so this is not "parameter" but "json" part in your Post request)

query_earthquake_translations()


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
    get_response = requests.get(url=url,headers=headers,stream=True)

    if get_response.status_code!=200:
        print(get_response.status_code)
    
    else:
        for line in get_response.iter_lines():
            if line==b'':
                pass
            else:
                json_response = json.loads(line)  #json.loads----->Deserialize fp (a .read()-supporting text file or binary file containing a JSON document) to a Python object using this conversion table.ie json to python object 
                tweet_id = json_response["data"]["id"]
                params = {'tweet.fields':'geo,lang,withheld', 'expansions':'geo.place_id'}
                tweet_lookup = requests.get(url=tweet_lookup_endpoint + tweet_id, headers=headers, params=params)
                tweet_lookup_str = str(tweet_lookup.json()["data"]) + "\n"
                conn.send(bytes(tweet_lookup_str,'utf-8'))

headers = request_headers(bearer_token)

json_response = connect_to_endpoint(endpoint_rules, headers, query_parameters)

headers = request_headers(bearer_token)

get_tweets(endpoint_get,headers)