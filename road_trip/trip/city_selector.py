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
        #Sends a call to Google Maps Directions and return a dictionary with
        #start and end coordinates and a list of all waypoint coordinates
        parsed_json = self.r.json()
        #print(parsed_json)
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


    def format_waypoints(self):
        #formats dictionary response from above into a list of tuples of coordinates
        dictionary = self.get_waypoints()
        waypoints = [dictionary["start_coord"]]
        for x in dictionary["waypoints"]:
            waypoints.append(x)
        waypoints.append(dictionary["end_coord"])
        return waypoints


    def format_waypoints_snap(self):
        #To be used with Snap To Roads requests
        dictionary = self.get_waypoints()
        waypoints = []
        for x in dictionary["waypoints"]:
            waypoints.append(str(x[0])+","+str(x[1]))
        waypoints = "|".join(waypoints)
        start = str(dictionary["start_coord"][0])+","+ str(dictionary["start_coord"][1])
        end = str(dictionary["end_coord"][0])+","+ str(dictionary["end_coord"][1])
        formatted_waypoints = start +"|"+ waypoints + "|" + end
        return formatted_waypoints


    def get_incremental_points(self):
        #formatting Snap To Roads requests
        waypoints = self.format_waypoints
        r = requests.get('https://roads.googleapis.com/v1/snapToRoads?path={}&interpolate=True&key={}'.format(waypoints, gm_key))
        print(r.json())


def make_df():
    #makes a Pandas dataframe from the cities csv file that contains cities and their
    #coordinates
    df = pd.read_csv("new_largest_cities.csv", encoding="latin-1")
    #df["city-state"] = df["City"].map(str) + ", " + df["State"]
    newdf = df[['City', 'State', 'Location']]
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


def find_cities(origin, dest, radius=20):
    route = GoogleMapsDirections(origin, dest)
    waypoints = route.format_waypoints()
    df = make_df()
    cities = {}
    for point in waypoints:
        for index, row in df.iterrows():
            dist = find_dist(lat1=point[0],lon1=point[1],lat2=row['latitude'],lon2=row['longitude'])
            if dist <= radius:
                if (row['City'], row['State']) not in cities:
                    if row['City'] != origin:
                        cities[(row['City'], row['State'])] = [row['latitude'], row['longitude']]

    print(cities)

find_cities("Raleigh", "Dayton", radius=20)
