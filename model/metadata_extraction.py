import pandas as pd
import spacy
from postgresql_crud import insert_data
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="MyApp")

"""
    This script will extract Named Entities from a tweet text.
    The entities will be processed and saved to the DB as latitude, longitude, magnitude, date and time.
"""

test_tweet = "USGS reports a M2.4 earthquake, 39 km W of Mentone, Texas on 1/17/23 @ 4:49:57 UTC https://t.co/HA6XJ8XzF6 #earthquake"
test_entities = [('ORG', 'USGS'), ('CARDINAL', 'M2.4'), ('QUANTITY', '39 km'), ('GPE', 'Mentone'), ('GPE', 'Texas'), ('DATE', '1/17/23'), ('TIME', '4:49:57 UTC')]

nlp = spacy.load("en_core_web_trf", disable=["tagger", "parser", "attribute_ruler", "lemmatizer"])

def extract_entities_from_tweet_text(text:str) -> list:
    entities = []
    doc = nlp(text)
    if doc.ents is not None:
        for ent in doc.ents:
            entities.append((str(ent.label_), str(ent.text)))
    return entities

# function that gets the location from the extracted entities as city, region, country
def get_location_from_entities(entities):
    location = ""
    if entities != []:
        for label, text in entities:
            if label.startswith('GPE'):
                location = text if location == "" else location + ", " + text
    return location

def get_date_and_time_from_entities(entities):
    date = ""
    time = ""
    if entities != []:
        for label, text in entities:
            if label.startswith('DATE'):
                date = text
            if label.startswith('TIME'):
                time = text
    return date, time

# function to get the geo coordinates as a list of tuples: latitude, longitude
def get_geo_coordinates(location):
    coordinates = []
    try :
        lat_and_long = geolocator.geocode(location)
        latitude = lat_and_long.latitude
        longitude = lat_and_long.longitude
        coordinates.append(("latitude", str(latitude)))
        coordinates.append(("longitude", str(longitude)))

    except :
        pass #TODO define exception to be thrown
    return coordinates

def insert_metadata_in_db(test_tweet):
    entities = extract_entities_from_tweet_text(test_tweet)
    location = get_location_from_entities(entities)
    coordinates = get_geo_coordinates(location)
    date, time = get_date_and_time_from_entities(entities)
    metadata = {
        "id" : 'bbb',
        "text" : test_tweet,
        "lat" : coordinates[0][1],
        "long" : coordinates[1][1],
        "date" : date, # yyyy-mm-dd
        "time" : time # hh:mm:ss
    }
    insert_data(metadata)
    print("metadata inserted!")

insert_metadata_in_db(test_tweet)

