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
SEAT_GEEK = os.environ["SEAT_GEEK_KEY"]


yelp = OAuth1Session(CONSUMER_KEY,
                            client_secret=CONSUMER_SECRET,
                            resource_owner_key=TOKEN,
                            resource_owner_secret=TOKEN_SECRET)


yelp_food_alias = {

"Asian Fusion":"asianfusion",
"Barbeque":"bbq",
"Burgers":"burgers",
"Cafes":"cafes",
"Chinese":"chinese",
"Comfort Food":"comfortfood",
"Filipino":"filipino",
"Fish & Chips":"fishnchips",
"Food Stands":"foodstands",
"Gastropubs":"gastropubs",
"Gluten-Free":"gluten_free",
"Italian":"italian",
"Mexican":"mexican",
"American (New)":"newamerican",
"Pizza":"pizza",
"Salad":"salad",
"Sandwiches":"sandwiches",
"Seafood":"seafood",
"Steakhouses":"steak",
"Thai":"thai",
"American (Traditional)":"tradamerican",
"Vegan":"vegan"

}


yelp_activity_alias  = {

"Amusement Parks":"amusementparks",
"Aquariums":"aquariums",
"Beaches":"beaches",
"Bike Rentals":"bikerentals",
"Boating":"boating",
"Bowling":"bowling",
"Challenge Courses":"challengecourses",
"Climbing":"climbing",
"Disc Golf":"discgolf",
"Jet Skis":"jetskis",
"Kids Activities":"kids_activities",
"Parks":"parks",
"Public Plazas":"publicplazas",
"Water Parks":"waterparks",
"Zoos":"zoos",
"Nightlife":"nightlife",
"Bars":"bars",
"Museums":"museums",
"Sports Teams":"sportsteams",
"Wineries":"wineries",
"Shopping":"shoppingcenters,outlet_stores,souvenirs,deptstores",
"Tours":"tours"

}

yelp_hotels_alias = {

"Bed & Breakfast":"bedbreakfast",
"Campgrounds":"campgrounds",
"Health Retreats":"healthretreats",
"Hostels":"hostels",
"Hotels":"hotels",
"Resorts":"resorts",
"RV Parks":"rvparks",
"Ski Resorts":"skiresorts"

}

def search_events(trip_id):

    trip = Trip.objects.get(pk=trip_id)
    city_list = find_cities(trip.origin, trip.destination)
    interest_food_list = Interest.objects.filter(trip=trip, category="Food").all()
    interest_food_list = [x.sub_category for x in interest_food_list]
    yelp_food_list = []
    for item in interest_food_list:
        ret = yelp_food_alias[item]
        yelp_food_list.append(ret)

    interest_activity_list = Interest.objects.filter(trip=trip, category="Activity").all()
    interest_activity_list = [x.sub_category for x in interest_activity_list]
    yelp_activity_list = []
    for item in interest_activity_list:
        ret = yelp_activity_alias[item]
        yelp_activity_list.append(ret)


    interest_hotels_list = Interest.objects.filter(trip=trip, category="Hotels").all()
    interest_hotels_list = [x.sub_category for x in interest_hotels_list]
    yelp_hotels_list = []
    for item in interest_hotels_list:
        ret = yelp_hotels_alias[item]
        yelp_hotels_list.append(ret)


    interest_teams_list = Interest.objects.filter(trip=trip, category="Teams").all()
    interest_teams_list = [x.sub_category for x in interest_teams_list]

    interest_performers_list = Interest.objects.filter(trip=trip, category="Performers").all()
    interest_performers_list = [x.sub_category for x in interest_performers_list]


    yelp_activity_list = ','.join(interest_activity_list)
    yelp_food_list = ','.join(yelp_food_list)
    yelp_hotels_list = ','.join(interest_hotels_list)
    cities_events = []
    for city in city_list:
         url_activity = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], yelp_activity_list)
         url_food = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], yelp_food_list)
         url_hotel = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], yelp_hotels_list)
         urls = [(url_activity, "Activity"), (url_food, "Food"), (url_hotel, "Hotels")]
         city_businesses = []
         for x in interest_teams_list:
             ret = search_seatgeek(trip_id, x, "Teams", city)
             try:
                 for r in ret:
                     city_businesses.append(r)
             except:
                 continue
         for x in interest_performers_list:
             ret = search_seatgeek(trip_id, x, "Performers", city)
             try:
                 for r in ret:
                     city_businesses.append(r)
             except:
                 continue
         for url in urls:
             r = yelp.get(url[0])
             r = r.json()
             counter = 0
             print(yelp_activity_list)
             print(url[0])
             print(r)
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

def search_seatgeek(trip_id, performer, category, city):
    trip = Trip.objects.get(pk=trip_id)
    if type(city) is tuple:
        city = city[0].title()
    else:
        city = city.title()
    df = make_df()
    df = df.set_index("City")
    lat = df.get_value(city, "latitude")
    lon = df.get_value(city, "longitude")
    slug = performer.lower().replace(' ', '-')
    performer_data = requests.get("http://api.seatgeek.com/2/performers?slug={}".format(slug))
    performer_json = performer_data.json()
    if category == "Performers":
        performer_id = performer_json["performers"][0]["id"]
        r = requests.get('http://api.seatgeek.com/2/recommendations?performers.id={id}&datetime_local.gte={start}&datetime_local.lt={end}&range=50mi&lat={lat}&lon={lon}&client_id={key}'.format(id=performer_id, start=str(trip.origin_date), end = str(trip.destination_date),lat = lat, lon = lon, key=SEAT_GEEK))

        parsed_json = r.json()
        recs = []
        counter = 0
    #print(parsed_json)
        try:
            for rec in parsed_json["recommendations"]:
                rec_dict = {}
                rec["category"]=category
                rec["subcategory"] = performer
                rec["title"] = parsed_json["recommendations"][counter]["event"]["title"]
                rec["datetime"] = parsed_json["recommendations"][counter]["event"]["datetime_local"]
                rec["url"] = parsed_json["recommendations"][counter]["event"]["url"]
                rec["address"] = parsed_json["recommendations"][counter]["event"]["address"]+", " +parsed_json["recommendations"][counter]["event"]["extended_address"]
                rec["lowest_price"] =parsed_json["recommendations"][counter]["event"]["stats"]["lowest_price"]
                recs.append(rec_dict)
            print(recs)
            return recs
        except:
            pass







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
#     yelp_food_list = []
#      for item in interest_food_list:
#          item = yelp_food_alias[item]
#          yelp_food_list.append(item)

#     interest_activity_list = Interest.objects.filter(trip=trip, category="hotels").all()
#     interest_activity_list = [x.sub_category for x in interest_activity_list]
#     yelp_activity_list = []
    # for item in interest_activity_list:
    #     item = yelp_activity_alias[item]
    #     yelp_activity_list.append(item)

#     interest_hotels_list = Interest.objects.filter(trip=trip, category="activities").all()
#     interest_hotels_list = [x.sub_category for x in interest_hotels_list]
#     yelp_hotels_list = []
    #   for item in interest_hotels_list:
    #       item = yelp_hotels_alias[item]
    #       yelp_hotels_list.append(item)

#     yelp_activity_list = ','.join(yelp_activity_list)
#     yelp_food_list = ','.join(yelp_food_list)
#     yelp_hotels_list = ','.join(yelp_hotels_list)
#
#     city_events = []
#     url_activity = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city, yelp_activity_list)
#     url_food = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city, yelp_food_list)
#     url_hotel = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city, yelp_hotels_list)
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
#     return city_events[0]
