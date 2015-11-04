
import urllib
import json
import requests
import os
import math
import pandas as pd
import re
from geographiclib.geodesic import Geodesic


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
                distance = re.findall(r'^[,0-9]*', parsed_json["routes"][0]["legs"][0]["steps"][counter]["distance"]["text"])
                distance = int(distance[0].replace(',',''))
                if distance > 50:
                    start = tuple((parsed_json["routes"][0]["legs"][0]["steps"][counter]["start_location"]["lat"], parsed_json["routes"][0]["legs"][0]["steps"][counter]["start_location"]["lng"]))
                    end = tuple((parsed_json["routes"][0]["legs"][0]["steps"][counter]["end_location"]["lat"], parsed_json["routes"][0]["legs"][0]["steps"][counter]["end_location"]["lng"]))
                    new_waypoints = points_between(start[0], start[1], end[0], end[1], round(distance/50))
                    for point in new_waypoints:
                        waypoints.append(point)
                counter+=1
            except:
                break
        directions["start_coord"]=start_coord
        directions["end_coord"]=end_coord
        directions["waypoints"]=waypoints
        #parsed_json
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
        return r.json()


def make_df():
    #makes a Pandas dataframe from the cities csv file that contains cities and their
    #coordinates
    df = pd.read_csv("road_trip/trip/new_largest_cities.csv", encoding="latin-1")
    #df["city-state"] = df["City"].map(str) + ", " + df["State"]
    newdf = df[['City', 'State', 'Location']]
    newdf = newdf.dropna()
    newdf['latitude']=newdf['Location'].str.extract('(\d\d.\d\d\d\d)')
    newdf['longitude']=newdf['Location'].str.extract('N ([\d.]+)')
    newdf.latitude = newdf.latitude.astype(float)
    newdf.longitude = newdf.longitude.astype(float)
    newdf['longitude']= -newdf['longitude']
    return newdf


def get_points_between(lat1,lon1,lat2,lon2):
    number_points = 20

    gd = Geodesic.WGS84.Inverse(35, 0, 35, 90)
    line = Geodesic.WGS84.Line(gd['lat1'], gd['lon1'], gd['azi1'])

    for i in range(number_points + 1):
        point = line.Position(gd['s12'] / number_points * i)
        print((point['lat2'], point['lon2']))



def points_between(lat1,lon1,lat2,lon2, num=30):
    fractionalincrement = (1.0/(num-1))

    lon1 = math.radians(lon1)
    lat1 = math.radians(lat1)
    lon2 = math.radians(lon2)
    lat2 = math.radians(lat2)

    distance_radians=2*math.asin(math.sqrt(math.pow((math.sin((lat1-lat2)/2)),2) + math.cos(lat1)*math.cos(lat2)*math.pow((math.sin((lon1-lon2)/2)),2)))
    # 3959.999 represents the mean radius of the earth
    # shortest path distance
    distance = 3959.999 * distance_radians

    mylats = []
    mylons = []

    # write the starting coordinates
    mylats.append([])
    mylons.append([])

    f = fractionalincrement
    counter = 1
    while (counter <  (num-1)):
            countmin1 = counter - 1
            mylats.append([])
            mylons.append([])
            # f is expressed as a fraction along the route from point 1 to point 2
            A=math.sin((1-f)*distance_radians)/math.sin(distance_radians)
            B=math.sin(f*distance_radians)/math.sin(distance_radians)
            x = A*math.cos(lat1)*math.cos(lon1) + B*math.cos(lat2)*math.cos(lon2)
            y = A*math.cos(lat1)*math.sin(lon1) +  B*math.cos(lat2)*math.sin(lon2)
            z = A*math.sin(lat1) + B*math.sin(lat2)
            newlat=math.atan2(z,math.sqrt(math.pow(x,2)+math.pow(y,2)))
            newlon=math.atan2(y,x)
            newlat_degrees = math.degrees(newlat)
            newlon_degrees = math.degrees(newlon)
            mylats[counter] = newlat_degrees
            mylons[counter] = newlon_degrees
            counter += 1
            f = f + fractionalincrement

    mycoords = list(zip(mylats,mylons))
    mycoords = mycoords[1:]
    return mycoords


#points_between(36.1589505, -86.82229009999999, 35.2655141, -89.6591249)

def find_dist(lat1,lon1,lat2,lon2):
    # approximate radius of earth in miles
    R = 3959.999

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def find_cities(origin, dest, radius=50):
    route = GoogleMapsDirections(origin, dest)
    waypoints = route.format_waypoints()
    df = make_df()
    cities = []
    for point in waypoints:
        for index, row in df.iterrows():
            dist = find_dist(lat1=point[0],lon1=point[1],lat2=row['latitude'],lon2=row['longitude'])
            if dist <= radius:
                if (row['City'], row['State']) not in cities:
                    if (row['City'], row['State']) != origin:
                        cities.append((row['City'], row['State']))

    print(cities)

find_cities("Raleigh, NC", "Los Angeles, CA")
