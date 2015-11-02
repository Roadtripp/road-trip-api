import urllib
import json
import requests
import os
from math import sin, cos, sqrt, atan2, radians
import pandas as pd


gm_key = os.environ["GOOGLE_MAPS"]


# class GoogleMapsDirections:
#     def __init__(self, origin, dest):
#         self.origin = origin
#         self.dest = dest
#         self.r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}'.format(self.origin, self.dest, gm_key))
#
#     def get(self):
#         parsed_json = self.r.json()
#         #start_coord = tuple(parsed_json["routes"]["legs"]["start_location"]["lat"], parsed_json["routes"]["legs"]["start_location"]["lng"])
#         #end_coord = tuple(parsed_json["routes"]["legs"]["end_location"]["lat"], parsed_json["routes"]["legs"]["end_location"]["lng"])
#         print(parsed_json)
#         #print(end_coord)


# something = GoogleMapsDirections(origin="Seattle", dest="San Diego")
# something.get()"


# class GoogleMapsDirections:
#     def __init__(self, origin, dest):
#         self.origin = origin
#         self.dest = dest
#         self.r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}'.format(self.origin, self.dest, gm_key))
#
#     def get(self):
#         parsed_json = self.r.json()
#         #start_coord = tuple(parsed_json["routes"]["legs"]["start_location"]["lat"], parsed_json["routes"]["legs"]["start_location"]["lng"])
#         #end_coord = tuple(parsed_json["routes"]["legs"]["end_location"]["lat"], parsed_json["routes"]["legs"]["end_location"]["lng"])
#         print(parsed_json)
#         #print(end_coord)


# something = GoogleMapsDirections(origin="Seattle", dest="San Diego")
# something.get()

def make_df():
    df = pd.read_csv("road_trip/trip/largest_cities.csv", encoding="latin-1")
    newdf = df[['City', 'Location']]
    newdf = newdf.dropna()
    newdf['latitude']=newdf['Location'].str.extract('(\d\d.\d\d\d\d)')
    newdf['longitude']=newdf['Location'].str.extract('N ([\d.]+)')
    newdf.latitude = newdf.latitude.astype(float)
    newdf.longitude = newdf.longitude.astype(float)
    newdf['longitude']= -newdf['longitude']
    return newdf


def find_dist(lat1,lon1,lat2,lon2):
    # approximate radius of earth in miles
    R = 3959.999

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
