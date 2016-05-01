import googlemaps
import json
import requests

api_key = 'AIzaSyBUOjTwQ5IqOWmZ2R0YvfDDiEcmja7au3Y'
gmaps = googlemaps.Client(key=api_key)

APPID='adc66a4a607358e4e7be3cab0bfb0abd'


def get_weather(geo_pair):
    # input : location tuple (lat, lng)
    # output: weather dict
    api_url = 'http://api.openweathermap.org/data/2.5/weather?units=metric&lat='\
              + str(geo_pair[0]) + '&lon=' + str(geo_pair[1]) + '&APPID=' + APPID
    r = requests.get(api_url)
    return json.loads(r.text)


def get_geocode(input_text):
    # Geocoding an address
    geocode_result = gmaps.geocode(input_text)
    return geocode_result


def geocode_to_geopair(geocode_result):
    if len(geocode_result) > 0:
        loc = geocode_result[0].get('geometry').get('location')
        return loc.get('lat'), loc.get('lng')
    return 0, 0


def get_nearby(location, radius=1000, s_type=None):
    places = gmaps.places_nearby(location=location, radius=radius, type=s_type)
    if places:
        return places.get('results')
    return {}


def get_photo(photo_ref, maxwidth=400):
    url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=' + str(maxwidth) + '&photoreference=' \
          + photo_ref + '&key=' + api_key
    return url


def get_photo_from_place(place, maxwidth=400, debug=False):
    name = place.get('name')
    photos = place.get('photos')
    url = ''
    if photos is not None:
        ref = photos[0].get('photo_reference')
        url = get_photo(ref)
    if debug:
        print(name, url)
    return url


def api_test():
    input_query = 'Tokyo Tower'
    geocode = get_geocode(input_query)
    if len(geocode) > 0:
        loc = geocode[0].get('geometry').get('location')
        print(loc)
        nearby_places = get_nearby(loc, radius=1000)
        print(json.dumps(nearby_places))
        for place in nearby_places:
            img_url = get_photo_from_place(place)
            print(place.get('name'), place.get('types'), place.get('price_level'), img_url)

    weather_info = get_weather(geocode_to_geopair(get_geocode(input_query)))
    print(weather_info)

if __name__ == '__main__':
    api_test()




