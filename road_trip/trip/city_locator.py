import urllib
import json
import requests
import os

gm_key = "AIzaSyBXAFA_oJnBAk8ZZqFLe4MPyJEG8TLDG88"


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
