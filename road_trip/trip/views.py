from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Trip, City
from .city_selector import *
from .serializers import TripSerializer, CitySerializer
from django.views.decorators.csrf import csrf_exempt
import json



# Create your views here.


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        trip_pk = self.kwargs["trip_pk"]
        tr = get_object_or_404(Trip, pk=trip_pk)
        return self.queryset.filter(trip=tr)

    def get_serializer_context(self):
        context = super().get_serializer_context().copy()
        context["trip_pk"] = self.kwargs["trip_pk"]
        return context


def suggestion_json(request, trip_pk):
    trip = get_object_or_404(Trip, pk=trip_pk)
    suggestions = '{'+'"id": "{}", "origin": "{}", "destination": "{}", "waypoints": ['.format(str(trip.id), str(trip.origin), str(trip.destination)) + ', '.join(['{'+'"location": "{}", "stopover": false, "activities": []'.format(x[0]+', '+x[1])+'}' for x in find_cities(trip.origin, trip.destination)]) + ']' + '}'
    return JsonResponse(json.loads(suggestions))


@csrf_exempt
def selection_json(request, trip_pk):
    if request.method == 'POST':
        selections = json.loads(request.body.decode('utf-8'))
        trip = get_object_or_404(Trip, pk=selections['id'])
        for wp in selections['waypoints']:
            if wp['stopover']:
                City.objects.create(
                    city_name=wp['location'],
                    trip=trip,
                    visited=wp['stopover']
                )
    return HttpResponse('', status=200)



import os
import requests
from requests_oauthlib import OAuth1, OAuth1Session

#OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = os.environ["YELP_CONSUMER"]
CONSUMER_SECRET = os.environ["YELP_CONSUMER_SECRET"]
TOKEN = os.environ["YELP_TOKEN"]
TOKEN_SECRET = os.environ["YELP_TOKEN_SECRET"]




yelp = OAuth1Session(CONSUMER_KEY,
                            client_secret=CONSUMER_SECRET,
                            resource_owner_key=TOKEN,
                            resource_owner_secret=TOKEN_SECRET)

#print(json.dumps(r, indent=2))


def search_events(trip_id):
    trip = Trip.objects.get(pk=trip_id)
    city_list = find_cities(trip.origin, trip.destination)
    interest_list = Interest.objects.filter(trip=trip)
    interest_list = [x+',' for x in interest_list]
    print(interest_list)
    cities_events = []
    for city in city_list:
         url = 'https://api.yelp.com/v2/search/?location={}&sort=2&category_filter={}'.format(city[0], interest_list)
         r = yelp.get(url)
         r = r.json()
         city = {}
         cities_events.append(city)
         #for business in r['businesses']



search_events(1)
