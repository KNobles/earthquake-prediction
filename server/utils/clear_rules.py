import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.environ["BEARER_TOKEN"]
header = {"Authorization": "Bearer {}".format(bearer_token)}
current_rules = requests.get(url="https://api.twitter.com/2/tweets/search/stream/rules", headers=header)
current_rules_json = current_rules.json()

try:
    list_ids=list(map(lambda rule: rule["id"], current_rules_json["data"]))
    to_delete={"delete":{'ids':list_ids}}
    response=requests.post(url="https://api.twitter.com/2/tweets/search/stream/rules", headers=header, json=to_delete)
    print("All rules deleted")
except Exception as e:
    print("No rules to delete")