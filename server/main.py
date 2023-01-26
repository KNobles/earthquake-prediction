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
    logger.info("Connected by", {str(addr)})
    return conn

#Body to add into Post request (so this is not "parameter" but "json" part in your Post request)
tweet_rules = {
    "add": [
        {"value": "earthquake -is:retweet "},
        {"value": "jishin -is:retweet"},
        {"value": "gempa bumi -is:retweet"},
        {"value": "terremoto -is:retweet"},
        {"value": "temblor -is:retweet"},
        {"value": "sismo -is:retweet"},
        #Earthquake in several languages with hashtags:
        {"value": "(#earthquake OR #jishin OR #gempabumi OR #terremoto OR #temblor OR #sismo) -is:retweet"},
        #Entities:
        {"value":"(entity:EmergencyEvents OR entity:Weather OR entity:Events OR entity:LocalNews)"},
        #Twitter accounts that tweet about earthquakes:
        # {"value":"(from:SismologicoMX OR from:sismos_chile OR from:Sismos_Peru_IGP) -is:retweet"},
        {"value":"""(
            from:USGSted OR from:LastQuake OR from:EmsC OR from:QuakesToday OR from:earthquakeBot OR 
            from:SismoDetector OR from:InfoEarthquakes OR from:SeismosApp OR fromeveryEarthquake OR from:eqgr
            ) -is:retweet"""}
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
    "tweet.fields":"geo,lang,attachments,context_annotations,conversation_id,created_at,entities,organic_metrics,promoted_metrics,possibly_sensitive,referenced_tweets,public_metrics,source,withheld",
    "user.fields":"created_at,description,entities,location,pinned_tweet_id,profile_image_url,protected,url,username,verified,withheld",
    "place.fields":"contained_within,country,country_code,full_name,geo,id,name,place_type",
    "expansions":"author_id,geo.place_id"
    }

    get_response = requests.get(url=url,headers=headers,stream=True, params=params)

    if get_response.status_code!=200:
        logger.info(f"TWITTER API CODE: {get_response.status_code}")
    
    else:
        for line in get_response.iter_lines():
            if line==b'':
                pass
            else:
                json_response = json.loads(line)
                # logger.info(json_response)
                tweet_field = json_response["data"]
                user_field = json_response.get("includes", {}).get("users", [])[0]
                place_field = json_response.get("includes", {}).get("places", [{}])[0]
                logger.info(place_field)

                if place_field:
                    place_country = place_field["country"]
                    place_city = place_field["name"]
                    place_type = place_field["place_type"]
                    if place_field.get("geo", {}):
                        if place_field.get("geo").get("type") == "Point":
                            place_geo = place_field["geo"]["coordinates"]
                        elif place_field.get("geo").get("type") == "Feature":
                            place_geo = place_field["geo"]["bbox"]
                else:
                    place_country = None
                    place_city = None
                    place_type = None
                    place_geo = None

                tweet_id = tweet_field["id"]
                tweet_text = tweet_field["text"]
                tweet_author_id = tweet_field["author_id"]
                tweet_created_at = tweet_field["created_at"]
                tweet_lang = tweet_field["lang"]
                
                if len(user_field) != 0:
                    user_id = user_field["id"]
                    user_username = user_field["username"]

                data_to_send = {
                    "id":tweet_id,
                    #  "tweet_content":json_response
                    "tweet_text":tweet_text,
                    "tweet_author_id":tweet_author_id,
                    "tweet_created_at":tweet_created_at, 
                    "tweet_lang":tweet_lang,
                    "user_id":user_id, 
                    "user_username":user_username,
                    "place_country":place_country,
                    "place_city":place_city,
                    "place_geo":place_geo,
                    "place_place_type":place_type,
                    "ml_processed": False
                }

                data_to_send_str = str(data_to_send) + "\n"
                logger.info(data_to_send_str)
            try:
                conn.send(bytes(data_to_send_str,'utf-8'))

            except BrokenPipeError as e:
                print(e + ", Reconnecting...")
                server_connect(HOST, PORT)
                get_tweets(url, headers)

conn = server_connect(HOST, PORT)
headers = request_headers(bearer_token)
json_response = connect_to_endpoint(endpoint_rules, headers, tweet_rules)
get_tweets(endpoint_get,headers)