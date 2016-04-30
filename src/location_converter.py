import json
from search_api import *


def translate_location(input_query):
    # input  : text query
    # output : (lat, lng)
    geocode = get_geocode(input_query)
    geopair = geocode_to_geopair(geocode)
    return geopair


if __name__ == '__main__':
    with open('place.txt', encoding='utf-8') as f:
        place_names = f.readlines()
        for name in place_names:
            name = name.strip()
            print(name, translate_location(name))
