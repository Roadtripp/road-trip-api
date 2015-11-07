from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
# from rest_framework.response import Response
from .models import Trip, City, Interest
from .city_selector import *
from .serializers import TripSerializer, CitySerializer
from django.views.decorators.csrf import csrf_exempt
import json
from .event_searches import search_events



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
    data = search_events(trip_pk)
    suggestions = '{'+'"id": "{}", "origin": "{}", "destination": "{}",
    "waypoints": ['.format(str(trip.id), str(trip.origin), str(trip.destination)) + ', '.join(['{'+'"location": "{}", "stopover": false, "activities": ['.format(city[0]['city'][0]+', '.join(['{'+'"address": "{}", "small_rate_img_url": "{}", "large_rate_img_url": "{}", "average_rating": "{}", "num_ratings": "{}", "title": "{}", "category": "{}", "sub_category": "{}", "activity_stopover": false, "url": "{}", "phone": "{}"'.format(' '.join(poi['address']), poi['rating_img_url_small'], poi['rating_img_url'], poi['rating'], poi['num_reviews'], poi['name'], poi['category'], poi['subcategory'], poi['url'], poi['phone']) for poi in city])+']'+', '+city[0]['city'][1])+'}' for city in data]) + ']' + '}'
    json.dump(data, io)
    return JsonResponse(io)


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


@csrf_exempt
def interests_json(request, trip_pk):
    if request.method == 'POST':
        interests = json.loads(request.body.decode('utf-8'))
        get_trip = get_object_or_404(Trip, pk=trip_pk)
        for interest in interests:
            Interest.objects.create(
                category=interest['category'],
                sub_category=interest['sub_category'],
                trip=get_trip
            )
    return HttpResponse('', status=200)
