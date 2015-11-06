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

yelp_food_alias = {

"Asian Fusion":"asianfusion"
"Barbeque":"bbq"
"Burgers":"burgers"
"Cafes":"cafes"
"Chinese":"chinese"
"Comfort Food":"comfortfood"
"Filipino":"filipino"
"Fish & Chips":"fishnchips"
"Food Stands":"foodstands"
"Gastropubs":"gastropubs"
"Gluten-Free":"gluten_free"
"Italian":"italian"
"Mexican":"mexican"
"American (New)":"newamerican"
"Pizza":"pizza"
"Salad":"salad"
"Sandwiches":"sandwhiches"
"Seafood":"seafood"
"Steakhouses":"steak"
"Thai":"thai"
"American (Traditional)":"tradamerican"
"Vegan":"vegan"

}


yelp_activity_alias  = {


}

yelp_hotel_alias = {


}

def search_events(trip_id):
    yelp = OAuth1Session(CONSUMER_KEY,
                                client_secret=CONSUMER_SECRET,
                                resource_owner_key=TOKEN,
                                resource_owner_secret=TOKEN_SECRET)


    trip = Trip.objects.get(pk=trip_id)
    city_list = find_cities(trip.origin, trip.destination)
    interest_food_list = Interest.objects.filter(trip=trip, category="food").all()
    interest_food_list = [x.sub_category for x in interest_food_list]
    for item in interest_food_list:
        item = yelp_food_alias["item"]

    interest_activity_list = Interest.objects.filter(trip=trip, category="hotels").all()
    interest_activity_list = [x.sub_category for x in interest_activity_list]


    interest_hotels_list = Interest.objects.filter(trip=trip, category="activities").all()
    interest_hotels_list = [x.sub_category for x in interest_hotels_list]


    interest_activity_list = ','.join(interest_activity_list)
    interest_food_list = ','.join(interest_food_list)
    interest_hotels_list = ','.join(interest_hotels_list)

    cities_events = []
    for city in city_list:
         url_activity = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], interest_activity_list)
         url_food = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], interest_food_list)
         url_hotel = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], interest_hotels_list)
         urls = [tuple(url_activity, "activity"), tuple(url_food, "food"), tuple(url_hotel, "hotel")]
         city_businesses = []
         for url in urls:
             r = yelp.get(url[0])
             r = r.json()
             counter = 0
             for business in r["businesses"]:
                bus = {}
                bus["name"] = r['businesses'][counter]['name']
                bus["category"] = url[1]
                bus["subcategory"] = r["businesses"][counter]["categories"]
                bus["rating"] = r['businesses'][counter]['rating']
                bus["url"] = r['businesses'][counter]['url']
                bus["num_reviews"] = r['businesses'][counter]['review_count']
                bus["rating_img_url_small"] = r['businesses'][counter]['rating_img_url_small']
                bus["rating_img_url"] = r['businesses'][counter]['rating_img_url']
                bus["phone"] = r['businesses'][counter]['display_phone']
                bus["address"] = r['businesses'][counter]['location']["display_address"]
                bus["city"]=city
                city_businesses.append(bus)
                counter += 1

         cities_events.append(city_businesses)
    #print(cities_events)
    return cities_events

# def search_events(trip_id, city):
#     yelp = OAuth1Session(CONSUMER_KEY,
#                                 client_secret=CONSUMER_SECRET,
#                                 resource_owner_key=TOKEN,
#                                 resource_owner_secret=TOKEN_SECRET)
#
#
#     trip = Trip.objects.get(pk=trip_id)
#     #city_list = find_cities(trip.origin, trip.destination)
#     interest_food_list = Interest.objects.filter(trip=trip, category="food").all()
#     interest_food_list = [x.sub_category for x in interest_food_list]
#     interest_activity_list = Interest.objects.filter(trip=trip, category="hotels").all()
#     interest_activity_list = [x.sub_category for x in interest_activity_list]
#     interest_hotels_list = Interest.objects.filter(trip=trip, category="activities").all()
#     interest_hotels_list = [x.sub_category for x in interest_hotels_list]
#     interest_activity_list = ','.join(interest_activity_list)
#     interest_food_list = ','.join(interest_food_list)
#     interest_hotels_list = ','.join(interest_hotels_list)
#
#     city_events = []
#     url_activity = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city, interest_activity_list)
#     url_food = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city, interest_food_list)
#     url_hotel = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city, interest_hotels_list)
#     urls = [url_activity, url_food, url_hotel]
#     for url in urls:
#         r = yelp.get(url)
#         r = r.json()
#         counter = 0
#         for business in r["businesses"]:
#             bus = {}
#             bus["name"] = r['businesses'][counter]['name']
#             bus["category"] = url.replace(r'url_', '')
#             bus["subcategory"] = r["businesses"][counter]["categories"]
#             bus["rating"] = r['businesses'][counter]['rating']
#             bus["url"] = r['businesses'][counter]['url']
#             bus["num_reviews"] = r['businesses'][counter]['review_count']
#             bus["rating_img_url_small"] = r['businesses'][counter]['rating_img_url_small']
#             bus["rating_img_url"] = r['businesses'][counter]['rating_img_url']
#             bus["phone"] = r['businesses'][counter]['display_phone']
#             bus["address"] = r['businesses'][counter]['location']["display_address"]
#             bus["city"]=city
#             city_events.append(bus)
#             counter += 1
#
#     return city_events[0]