import googlemaps
import json

api_key = 'AIzaSyBUOjTwQ5IqOWmZ2R0YvfDDiEcmja7au3Y'
gmaps = googlemaps.Client(key=api_key)


def get_geocode(input_text):
    # Geocoding an address
    geocode_result = gmaps.geocode(input_text)
    return geocode_result


def get_nearby(location, radius=1000, s_type=None):
    places = gmaps.places_nearby(location=location, radius=radius, type=s_type)
    return places


def get_photo(photo_ref, maxwidth=400):
    url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=' + str(maxwidth) + '&photoreference=' \
          + photo_ref + '&key=' + api_key
    return url


def get_photos_from_places(places, maxwidth=400, debug=False):
    urls = list()
    results = places.get('results')
    for r in results:
        name = r.get('name')
        photos = r.get('photos')
        url = ''
        if photos is not None:
            ref = photos[0].get('photo_reference')
            url = get_photo(ref)
        urls.append(url)
        if debug:
            print(name, url)
    return urls


def test_api():
    input_query = '東京 淺草'
    geocode = get_geocode(input_query)
    if len(geocode) > 0:
        loc = geocode[0].get('geometry').get('location')
        print(loc)
        nearby_dict = get_nearby(loc, radius=1000, s_type='food')
        print(json.dumps(nearby_dict))
        img_urls = get_photos_from_places(nearby_dict, debug=True)
        '''for img_url in img_urls:
            print(img_url)'''


if __name__ == '__main__':
    test_api()



