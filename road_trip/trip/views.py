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


def list_gen(x, category):
    return [
        {
            "title": item["name"],
            "address": " ".join(item["address"]),
            "sub_categories": item["subcategory"],
            "activity_stopover": False,
            "url": item["url"],
            "small_rate_img_url": item["rating_img_url_small"],
            "large_rate_img_url": item["rating_img_url"],
            "average_rating": item["rating"],
            "num_ratings": item["num_reviews"]
        }
        for item in x[category]
    ]


def suggestion_json(request, trip_pk):
    trip = get_object_or_404(Trip, pk=trip_pk)
    data = search_events(trip_pk)
    data = [{"all_activities": city} for city in data]

    c = ["activity", "food", "sports", "artist", "hotel"]
    for city in data:
        for category in c:
            city[category] = []
        for activity in city["all_activities"]:
            city[activity["category"]].append(activity)

    j = [
            {
                "location": ", ".join(x["all_activities"][1]["city"]),
                "location_plus": ",+".join(x["all_activities"][1]["city"]),
                "stopover": False,
                "activities": list_gen(x, "activity"),
                "hotels": list_gen(x, "hotel"),
                "sports": list_gen(x, "sports"),
                "food": list_gen(x, "food"),
                "artist": list_gen(x, "artist")
            }
            for x in data
        ]
    with open('data.json', 'w') as f:
        f.write(json.dumps(j))
    return JsonResponse(json.dumps(j), safe=False)


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
