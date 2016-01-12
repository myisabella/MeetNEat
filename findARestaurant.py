import httplib2
import json

import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# TODO: need to store them in another file
google_api_key = "AIzaSyB46S6ZFdQ1rrS7G3lHAZjthT3fmh_VC_Q"
foursquare_client_id = "V1VILC24KJ4RUO250BDNFS5VNYM4J2GUCTXNQN3WC3MXGFWT"
foursquare_client_secret = "KE31BCE0B5JH1SLKGTSMNTT3X4M4YWQZZUZILMJFSOXFDOGT"

def getGeocodeLocation(inputString):
    locationString = inputString(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))

    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude,longitude)

def findARestaurant(mealType, location):
    # Step 1: Use getGeocodeLocation to get the latitude and longitude coordinates of the location inputString
    latitude, longitude = getGeocodeLocation(location)

    # Step 2: Use Foursquare API to find a nearby restaurant with the latitude, longitude and mealType strings
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20151229&ll=%s,%s&query=%s' % (foursquare_client_id, foursquare_client_secret, latitude, longitude, mealType))
    h = httplib2.Http()

    # Step 3: Grab the first restaurant
    result = json.loads(h.request(url, 'GET')[1])
    if result['response']['venues']:
        restaurant = result['response']['venues'][0]
        venue_id = restaurant['id']
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']
        address = ""
        for item in restaurant_address:
            address += item + " "
        restaurant_address = address

    # Step 4: Get a 300x300 picture of the restaurant using venue_id
        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20151229&client_secret=%s' % (venue_id, foursquare_client_id, foursquare_client_secret))
        result = json.loads(h.request(url, 'GET')[1])

    # Step 5: Grab the first image
        if result['response']['photos']['items']:
            pic = result['response']['photos']['items'][0]
            pic_prefix = pic['prefix']
            pic_suffix = pic['suffix']
            pic_url = pic_prefix + "300x300" + pic_suffix

    # Step 6: If no image is available, insert default image URL
        else:
            pic_url = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

    # Stpe 7: Return a dict containing the restaurant information
        restaurant_info = {'name': restaurant_name, 'address': restaurant_address, 'image': pic_url}
        return restaurant_info

    else:
        print "No restaurant found near this location %s with this type %s" % (location, mealType)

