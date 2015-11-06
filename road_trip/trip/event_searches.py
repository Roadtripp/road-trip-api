import json
import os
import requests
from requests_oauthlib import OAuth1, OAuth1Session
from .city_selector import *
from .models import Trip
from .models import Interest

#OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = os.environ["YELP_CONSUMER"]
CONSUMER_SECRET = os.environ["YELP_CONSUMER_SECRET"]
TOKEN = os.environ["YELP_TOKEN"]
TOKEN_SECRET = os.environ["YELP_TOKEN_SECRET"]


#print(json.dumps(r, indent=2))


def search_events(trip_id):
    yelp = OAuth1Session(CONSUMER_KEY,
                                client_secret=CONSUMER_SECRET,
                                resource_owner_key=TOKEN,
                                resource_owner_secret=TOKEN_SECRET)


    trip = Trip.objects.get(pk=trip_id)
    city_list = find_cities(trip.origin, trip.destination)
    interest_list = Interest.objects.filter(trip=trip)
    interest_list = [x.sub_category+',' for x in interest_list]
    interest_list = ''.join(interest_list)
    cities_events = []
    for city in city_list:
         url = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], "chinese")
         r = yelp.get(url)
         r = r.json()
         city_dict = {}
         city_dict["city_name"] = city[0]+', '+ city[1]
         cities_events.append(city_dict)
         counter = 0
         for business in r["businesses"]:
            bus = {}
            bus["name"] = r['businesses'][counter]['name']
            bus["rating"] = r['businesses'][counter]['rating']
            bus["url"] = r['businesses'][counter]['url']
            bus["num_reviews"] = r['businesses'][counter]['review_count']
            bus["rating_img_url_small"] = r['businesses'][counter]['rating_img_url_small']
            bus["rating_img_url"] = r['businesses'][counter]['rating_img_url']
            bus["phone"] = r['businesses'][counter]['display_phone']
            bus["address"] = r['businesses'][counter]['location']["display_address"]
            city_dict["business: "+str(counter)]=bus
            counter += 1
    return cities_events
