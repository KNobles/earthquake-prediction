    
def query_earthquake_translations():
    query_parameters = {
        "add": [
            {"value": "地震"},
            {"value": "jishin"},
            {"value": "gempa bumi"},
            {"value": "terremoto"},
            {"value": "deprem"},
            {"value": "भूकम्प"},
            {"value": "bhukamp"},
            {"value": "earthquake"},
            {"value": "زلزله"},
            {"value": "zelzeleh"},
            {"value": "dìzhèn"},
            {"value": "भूकंप"},
            {"value": "bhūkampa"},
            {"value": "lindol"},
            {"value": "σεισμός"},
            {"value": "seismos"},
            {"value": "землетрясение"},
            {"value": "zemletryasenie"},
            {"value": "tërmet"},
            {"value": "земетресение"},
            {"value": "zemotresenie"},
            {"value": "երկրաշարժ"},
            {"value": "erkrasharzh"},
            {"value": "მიწისძვრა"},
            {"value": "mits'idzghvra"},
            ]
        }
    return query_parameters

# def query(value:str):
#     query_parameters = {
#     "add": [
#         {"value":"earthquake"},
#         ]
#     }

# def query_earthquake_translations():
#     for key, value in earthquake_translations.items():
#         query(value)

#     return 