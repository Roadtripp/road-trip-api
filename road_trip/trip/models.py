from django.db import models

# Create your models here.


class Trip(models.Model):
    title = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    origin_date = models.DateField(null=True, blank=True)
    origin_time = models.TimeField(null=True, blank=True)
    origin_lat = models.FloatField(null=True, blank=True)
    origin_lon = models.FloatField(null=True, blank=True)
    destination = models.CharField(max_length=255)
    destination_date = models.DateField(null=True, blank=True)
    destination_time = models.TimeField(null=True, blank=True)
    destination_lat = models.FloatField(null=True, blank=True)
    destination_lon = models.FloatField(null=True, blank=True)


class City(models.Model):
    city_name = models.CharField(max_length=255)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    trip = models.ForeignKey(Trip)
    visited = models.BooleanField(default=False)


class Activity(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    address = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    activity_stopover = models.BooleanField(default=False)
    url = models.URLField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    img_url = models.URLField(max_length=255, null=True)
    small_rate_img_url = models.URLField(max_length=255, null=True, blank=True)
    large_rate_img_url = models.URLField(max_length=255, null=True, blank=True)
    average_rating = models.FloatField(null=True, blank=True)
    num_ratings = models.IntegerField(null=True, blank=True)
    city = models.ForeignKey(City)


class Interest(models.Model):
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    trip = models.ForeignKey(Trip)

    def __str__(self):
         return 'Category: {} Subcategory: {}'.format(self.category, self.sub_category)




# import json
# import os
# import requests
# from requests_oauthlib import OAuth1, OAuth1Session
# from city_selector import *
#
# #OAuth credential placeholders that must be filled in by users.
# CONSUMER_KEY = os.environ["YELP_CONSUMER"]
# CONSUMER_SECRET = os.environ["YELP_CONSUMER_SECRET"]
# TOKEN = os.environ["YELP_TOKEN"]
# TOKEN_SECRET = os.environ["YELP_TOKEN_SECRET"]
#
#
#
#
# yelp = OAuth1Session(CONSUMER_KEY,
#                             client_secret=CONSUMER_SECRET,
#                             resource_owner_key=TOKEN,
#                             resource_owner_secret=TOKEN_SECRET)
#
# #print(json.dumps(r, indent=2))
#
#
# def search_events(trip_id):
#     trip = Trip.objects.get(pk=trip_id)
#     city_list = find_cities(trip.origin, trip.destination)
#     interest_list = Interest.objects.filter(trip=trip)
#     interest_list = [x+',' for x in interest_list]
#     #print(interest_list)
#     for city in city_list:
#          url = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], )
#          r = yelp.get(url)
#          r = r.json()
# search_events(1)
