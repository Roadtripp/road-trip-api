import json
import os
import requests
from requests_oauthlib import OAuth1, OAuth1Session
from .city_selector import *
from .models import Trip
from .models import Interest
import re

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

"asianfusion":"asianfusion",
"barbeque":"bbq",
"burgers":"burgers",
"cafes":"cafes",
"chinese":"chinese",
"comfortfood":"comfortfood",
"filipino":"filipino",
"fishandchips":"fishnchips",
"foodstands":"foodstands",
"gastropubs":"gastropubs",
"glutenfree":"gluten_free",
"italian":"italian",
"mexican":"mexican",
"americannew":"newamerican",
"pizza":"pizza",
"salad":"salad",
"sandwiches":"sandwiches",
"seafood":"seafood",
"restaurants":"restaurants",
"steakhouses":"steak",
"thai":"thai",
"americantraditional":"tradamerican",
"vegan":"vegan"
}


yelp_activity_alias  = {

"amusementparks":"amusementparks",
"aquariums":"aquariums",
"beaches":"beaches",
"bikerentals":"bikerentals",
"boating":"boating",
"bowling":"bowling",
"challengecourses":"challengecourses",
"climbing":"climbing",
"discgolf":"discgolf",
"jetskis":"jetskis",
"kidsactivities":"kids_activities",
"parks":"parks",
"publicplazas":"publicplazas",
"waterparks":"waterparks",
"zoos":"zoos",
"nightlife":"nightlife",
"bars":"bars",
"museums":"museums",
"sportsteams":"sportsteams",
"wineries":"wineries",
"shopping":"shoppingcenters,outlet_stores,souvenirs,deptstores",
"tours":"tours"

}

yelp_hotels_alias = {

"bedandbreakfast":"bedbreakfast",
"campgrounds":"campgrounds",
"healthretreats":"healthretreats",
"hostels":"hostels",
"hotels":"hotels",
"resorts":"resorts",
"rvparks":"rvparks",
"skiresorts":"skiresorts"

}

def search_events(trip_id):

    trip = Trip.objects.get(pk=trip_id)
    city_list = find_cities(trip.origin, trip.destination)
    interest_food_list = Interest.objects.filter(trip=trip, category="food").all()
    interest_food_list = [x.sub_category for x in interest_food_list]
    yelp_food_list = []
    for item in interest_food_list:
        ret = yelp_food_alias[item]
        yelp_food_list.append(ret)

    interest_activity_list = Interest.objects.filter(trip=trip, category="activities").all()
    interest_activity_list = [x.sub_category for x in interest_activity_list]
    yelp_activity_list = []
    for item in interest_activity_list:
        ret = yelp_activity_alias[item]
        yelp_activity_list.append(ret)


    interest_hotels_list = Interest.objects.filter(trip=trip, category="hotels").all()
    interest_hotels_list = [x.sub_category for x in interest_hotels_list]
    yelp_hotels_list = []
    for item in interest_hotels_list:
        ret = yelp_hotels_alias[item]
        yelp_hotels_list.append(ret)


    interest_sports_list = []
    if Interest.objects.filter(trip=trip, category="sport").count() != 0:
        sports = Interest.objects.filter(trip=trip, category="sport").all()
        for x in sports:
            x_id = get_id(x.sub_category, x.category)
            if x_id is not None:
                interest_sports_list.append((x, x_id))


    interest_artist_list = []
    if Interest.objects.filter(trip=trip, category="artist").count() != 0:
        artist = Interest.objects.filter(trip=trip, category="artist").all()
        for x in artist:
            x_id = get_id(x.sub_category, x.category)
            if x_id is not None:
                interest_artist_list.append((x, x_id))


    yelp_activity_list = ','.join(yelp_activity_list)
    yelp_food_list = ','.join(yelp_food_list)
    yelp_hotels_list = ','.join(yelp_hotels_list)
    print(len(yelp_activity_list))
    print(yelp_activity_list)
    print(len(yelp_food_list))
    print(len(yelp_hotels_list))
    cities_events = []
    for city in city_list:
         if len(yelp_activity_list) != 0:
            url_activity = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], yelp_activity_list)
         else:
            url_activity = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], "active")
         if len(yelp_food_list) != 0:
            url_food = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], yelp_food_list)
         else:
            url_food = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], "restaurants")
         if len(yelp_hotels_list) != 0:
            url_hotel = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], yelp_hotels_list)
         else:
            url_hotel = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], "hotels")
         urls = [(url_activity, "activities"), (url_food, "food"), (url_hotel, "hotels")]


         city_businesses = []
         if len(interest_sports_list) != 0:
             for x in interest_sports_list:
                 ret = search_seatgeek(trip_id, x[0].sub_category, "sport", city, x[1][0], city_businesses, x[1][1])
                 try:
                     for r in ret:
                         if type(r) is not None:
                             city_businesses.append(r)
                 except:
                     continue


         if len(interest_artist_list) != 0:
             for x in interest_artist_list:
                 ret = search_seatgeek(trip_id, x[0].sub_category, "artist", city, x[1][0], city_businesses, x[1][1])
                 try:
                     for r in ret:
                         if type(r) is not None:
                             city_businesses.append(r)
                 except:
                     continue


         for url in urls:
            r = yelp.get(url[0])
            r = r.json()
            counter = 0
            for x in range(3):
                 try:
                    bus = {
                    "date": "null",
                    "time": "null"
                    }
                    bus["name"] = r['businesses'][counter]['name']
                    bus["category"] = url[1]
                    bus["subcategory"] = r["businesses"][counter]["categories"]
                    bus["rating"] = r['businesses'][counter]['rating']
                    bus["url"] = r['businesses'][counter]['url']
                    bus["num_reviews"] = r['businesses'][counter]['review_count']
                    bus["rating_img_url_small"] = r['businesses'][counter]['rating_img_url_small']
                    bus["rating_img_url"] = r['businesses'][counter]['rating_img_url']
                    try:
                        bus["phone"] = r['businesses'][counter]['display_phone']
                    except KeyError:
                        bus["phone"] = "null"
                    bus["address"] = r['businesses'][counter]['location']["display_address"]
                    bus["city"]=city
                    bus["lowest_price"]="null"
                    bus["average_price"]="null"
                    bus["highest_price"]="null"
                    bus["img_url"]="null"
                    city_businesses.append(bus)
                    counter += 1
                 except:
                     continue
         cities_events.append(city_businesses)
    return cities_events


def search_seatgeek(trip_id, performer, category, city, performer_id, city_businesses, genre):
    trip = Trip.objects.get(pk=trip_id)
    if type(city) is tuple:
        city_pd = city[0].title()
    else:
        city_pd = city.title()
    df = make_df()
    df = df.set_index("City")
    lat = df.get_value(city_pd, "latitude")
    lon = df.get_value(city_pd, "longitude")

    r = requests.get('http://api.seatgeek.com/2/recommendations?performers.id={id}&datetime_local.gte={start}&datetime_local.lt={end}&range=50mi&lat={lat}&lon={lon}&client_id={key}'.format(id=performer_id, start=str(trip.origin_date), end = str(trip.destination_date),lat = lat, lon = lon, key=SEAT_GEEK))
    parsed_json = r.json()
    recs = []
    counter = 0
    try:
        if len(parsed_json["recommendations"]) != 0:

            for x in parsed_json["recommendations"]:
                if float(parsed_json["recommendations"][counter]["event"]["score"]) > .70:
                    time = re.findall(r'\T(.*)[:]', parsed_json["recommendations"][counter]["event"]["datetime_local"])
                    time = ''.join(time)
                    hours = time[0]+time[1]
                    if int(hours) > 12:
                         hours = int(hours) - 12
                         newtime = str(hours) + time[2] +time[3] +time[4] + "PM"
                    elif int(hours) == 12:
                        newtime = str(hours) + time[2] +time[3] +time[4] + "PM"
                    else:
                        newtime = time + "AM"

                    date = str((parsed_json["recommendations"][counter]["event"]["datetime_local"])).split("T")
                    date = date[0]
                    rec_dict = {
                        "name": parsed_json["recommendations"][counter]["event"]["title"],
                        "category": category,
                        "subcategory": performer,
                        "rating": "null",
                        "url":parsed_json["recommendations"][counter]["event"]["url"],
                        "num_reviews": "null",
                        "rating_img_url_small": "null",
                        "rating_img_url": "null",
                        "phone": "null",
                        "date":date,
                        "time": newtime,
                        "address" :[parsed_json["recommendations"][counter]["event"]["venue"]["address"], parsed_json["recommendations"][counter]["event"]["venue"]["extended_address"]],
                        "lowest_price": parsed_json["recommendations"][counter]["event"]["stats"]["lowest_price"],
                        "average_price": parsed_json["recommendations"][counter]["event"]["stats"]["average_price"],
                        "highest_price": parsed_json["recommendations"][counter]["event"]["stats"]["highest_price"],
                        "img_url":"null",
                        "city":city}
                    event_dates = []
                    counter += 1
                    for x in city_businesses:
                        event_dates.append((x["date"],x["time"],x["address"]))
                    if (rec_dict["date"], rec_dict["time"],rec_dict["address"]) not in event_dates:
                        recs.append(rec_dict)
                else:
                    counter += 1
            return recs
    except KeyError:
        pass

def get_id(performer, cat):
    slug = performer.lower().replace(' ', '-')
    performer_data = requests.get("http://api.seatgeek.com/2/performers?slug={}".format(slug))
    performer_json = performer_data.json()
    try:
        if cat == "artist":
            performer_id = performer_json["performers"][0]["id"]
            genre = performer_json["performers"][0]["genres"][0]["name"]
            return (performer_id, genre)
        elif cat == "sport":
            performer_id = performer_json["performers"][0]["id"]
            sport = performer_json["performers"][0]["taxonomies"][1]["name"]
            return (performer_id, sport)
    except:
        pass
