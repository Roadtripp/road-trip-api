import urllib
import json
import requests
import os
from math import sin, cos, sqrt, atan2, radians
import pandas as pd


gm_key = os.environ["GOOGLE_MAPS"]


class GoogleMapsDirections:
    def __init__(self, origin, dest):
        self.origin = origin
        self.dest = dest
        self.r = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}'.format(self.origin, self.dest, gm_key))

    def get_waypoints(self):
        parsed_json = self.r.json()
        directions = {}
        start_coord = tuple((parsed_json["routes"][0]["legs"][0]["start_location"]["lat"], parsed_json["routes"][0]["legs"][0]["start_location"]["lng"]))
        end_coord = tuple((parsed_json["routes"][0]["legs"][0]["end_location"]["lat"], parsed_json["routes"][0]["legs"][0]["end_location"]["lng"]))
        waypoints = []
        counter=0
        for x in range(100):
            try:
                waypoints.append(tuple((parsed_json["routes"][0]["legs"][0]["steps"][counter]["end_location"]["lat"], parsed_json["routes"][0]["legs"][0]["steps"][counter]["end_location"]["lng"])))
                counter += 1
            except:
                break
        directions["start_coord"]=start_coord
        directions["end_coord"]=end_coord
        directions["waypoints"]=waypoints
        return directions

    def format_waypoints_snap(self):
        dictionary = self.get_waypoints()
        waypoints = []
        for x in dictionary["waypoints"]:
            waypoints.append(str(x[0])+","+str(x[1]))
        waypoints = "|".join(waypoints)
        start = str(dictionary["start_coord"][0])+","+ str(dictionary["start_coord"][1])
        end = str(dictionary["end_coord"][0])+","+ str(dictionary["end_coord"][1])
        formatted_waypoints = start +"|"+ waypoints + "|" + end
        return formatted_waypoints

    def format_waypoints(self):
        dictionary = self.get_waypoints()
        waypoints = [dictionary["start_coord"]]
        for x in dictionary["waypoints"]:
            waypoints.append(x)
        waypoints.append(dictionary["end_coord"])
        return waypoints

    def get_incremental_points(self):
        waypoints = self.format_waypoints
        r = requests.get('https://roads.googleapis.com/v1/snapToRoads?path={}&interpolate=True&key={}'.format(waypoints, gm_key))
        print(r.json())


something = GoogleMapsDirections("Seattle", "San Diego")
something.format_waypoints()



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