    
def query_earthquake_translations():
    query_parameters = {
    "add": [
        # {"value": "地震"},
        # {"value": "jishin"},
        # # {"value": "gempa bumi"},
        # {"value": "terremoto"},
        # {"value": "temblor"},
        # {"value": "sismo"},
        # # {"value": "tsunami"},
        # {"value": "deprem"},
        # {"value": "भूकम्प"},
        # {"value": "bhukamp"},
        # {"value": "earthquake"},
        # {"value": "زلزله"},
        # {"value": "zelzeleh"},
        # {"value": "dìzhèn"},
        # {"value": "भूकंप"},
        # {"value": "bhūkampa"},
        # {"value": "lindol"},
        # {"value": "σεισμός"},
        # {"value": "seismos"},
        # {"value": "землетрясение"},
        # {"value": "zemletryasenie"},
        # {"value": "tërmet"},
        # {"value": "земетресение"},
        # {"value": "zemotresenie"},
        # {"value": "երկրաշարժ"},
        # {"value": "erkrasharzh"},
        # {"value": "მიწისძვრა"},
        # {"value": "mits'idzghvra"},
        {"value":"from:SismologicoMX"},
        {"value":"from:sismos_chile"},
        {"value":"from:Sismos_Peru_IGP"},
        {"value":"(from:USGSted OR from:LastQuake OR from:EmsC OR from:QuakesToday OR\
        from:earthquakeBot OR from:SismoDetector OR from:InfoEarthquakes OR from:SeismosApp\
        OR fromeveryEarthquake OR from:eqgr)"},

        ]
    }
    return query_parameters

