import os
import json
import socket
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
        level=logging.INFO,
        handlers=[
            # Write logs to file
            logging.FileHandler(f"logs/{datetime.now().strftime('%d-%m-%Y%H:%M')}.log"),
            logging.StreamHandler(),
        ])

logger = logging.getLogger("TWITTER SERVER")
bearer_token = os.environ["BEARER_TOKEN"]
endpoint_get = "https://api.twitter.com/2/tweets/search/stream"
endpoint_rules = "https://api.twitter.com/2/tweets/search/stream/rules"

# Set localhost socket parameters
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = 9095

def server_connect(HOST:str, PORT:int) -> socket:
    logger.info(f"Listening to port {PORT}...")
    # Create local socket
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_socket.bind((HOST, PORT))
    local_socket.listen(1)
    conn, addr = local_socket.accept()
    logger.info("Connected by", addr)
    return conn

#Body to add into Post request (so this is not "parameter" but "json" part in your Post request)
tweet_rules = {
    "add": [
        {"value": "earthquake"},
        {"value": "jishin"},
        {"value": "gempa bumi"},
        {"value": "terremoto"},
        {"value": "temblor"},
        {"value": "sismo"},
        #Twitter accounts that tweet about earthquakes:,
        {"value":"(from:SismologicoMX OR from:sismos_chile OR from:Sismos_Peru_IGP)"},
        {"value":"""(
            from:USGSted OR from:LastQuake OR from:EmsC OR from:QuakesToday OR 
            from:earthquakeBot OR from:SismoDetector OR from:InfoEarthquakes OR 
            from:SeismosApp OR fromeveryEarthquake OR from:eqgr
            )"""}
        ]
    }

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

def get_tweets(url:str, headers:dict) -> None:
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
        logger.info(f"TWITTER API CODE: {get_response.status_code}")
    
    else:
        for line in get_response.iter_lines():
            if line==b'':
                pass
            else:
                try:
                    json_response = json.loads(line)
                    
                    tweet_field = json_response["data"] 
                    user_field = json_response.get("includes", {}).get("users", [])[0]
                    place_field = json_response.get("includes", {}).get("places", [])[0]

                    tweet_id = tweet_field["id"]
                    tweet_text = tweet_field["text"]
                    tweet_author_id = tweet_field["author_id"]
                    tweet_created_at = tweet_field["created_at"]
                    tweet_lang = tweet_field["lang"]
                    
                    if len(user_field != 0):
                        user_id = user_field["id"]
                        user_username = user_field["username"]

                    if len(place_field != 0):
                        place_country = place_field["country"]
                        place_city = place_field["name"]
                        place_type = place_field["place_type"]
                    
                        if place_field["geo"]["type"] == "Point":
                            place_geo = place_field["geo"]["coordinates"]
                        elif place_field["geo"]["type"] == "Feature":
                            place_geo = place_field["geo"]["bbox"]
                    # Check if geo.type = Feature then "bbox" else if POINT its the coordinates-3.88

                    data_to_send = {
                        "tweet_id":tweet_id, 
                        "tweet_text":tweet_text,
                        "tweet_author_id":tweet_author_id,
                        "tweet_created_at":tweet_created_at, 
                        "tweet_lang":tweet_lang,
                        "user_id":user_id, 
                        "user_username":user_username,
                        "place_country":place_country,
                        "place_city":place_city,
                        "place_geo":place_geo,
                        "place_place_type":place_type
                    }
                    
                    data_to_send_str = str(data_to_send) + "\n"
                    logger.info(data_to_send_str)
                    
                    conn.send(bytes(data_to_send_str,'utf-8'))

                except BrokenPipeError as e:
                    print(e + ", Reconnecting...")
                    server_connect(HOST, PORT)
                    get_tweets(url, headers)

conn = server_connect(HOST, PORT)
headers = request_headers(bearer_token)
json_response = connect_to_endpoint(endpoint_rules, headers, tweet_rules)
get_tweets(endpoint_get,headers)