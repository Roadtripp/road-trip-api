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
