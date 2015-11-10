from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
# from rest_framework.response import Response
from .models import Trip, City, Interest, Activity
from .city_selector import *
from .serializers import TripSerializer, CitySerializer, ActivitySerializer
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


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        city_pk = self.kwargs["city_pk"]
        ct = get_object_or_404(City, pk=city_pk)
        return self.queryset.filter(city=ct)

    def get_serializer_context(self):
        context = super().get_serializer_context().copy()
        context["city_pk"] = self.kwargs["city_pk"]
        return context


def list_gen(x, category):
    return [
        {
            "title": item["name"],
            "address": " ".join(item["address"]),
            "category": item["category"],
            "sub_categories": item["subcategory"],
            "activity_stopover": False,
            "url": item["url"],
            "small_rate_img_url": item["rating_img_url_small"],
            "large_rate_img_url": item["rating_img_url"],
            "average_rating": item["rating"],
            "num_ratings": item["num_reviews"],
            "date": item["date"],
            "time": item["time"],
            "phone": item["phone"],
        }
        for item in x[category]
    ]


def suggestion_json(request, trip_pk):
    trip = get_object_or_404(Trip, pk=trip_pk)
    data = search_events(trip_pk)
    data = [{"all_activities": city} for city in data]

    c = ["activities", "food", "sports", "artist", "hotels"]
    for city in data:
        for category in c:
            city[category] = []
        for activity in city["all_activities"]:
            city[activity["category"]].append(activity)

    j = {
            "origin": trip.origin,
            "title": trip.title,
            "destination": trip.destination,
            "waypoints": [
                {
                    "location": ", ".join(x["all_activities"][0]["city"]),
                    "location_plus": ",+".join(x["all_activities"][0]["city"]),
                    "stopover": False,
                    "activities": list_gen(x, "activities"),
                    "hotels": list_gen(x, "hotels"),
                    "sports": list_gen(x, "sports"),
                    "food": list_gen(x, "food"),
                    "artist": list_gen(x, "artist")
                }
                for x in data
            ]
        }

    return JsonResponse(j)


def check_null(value):
    if value == "null":
        return None
    return value


@csrf_exempt
def selection_json(request, trip_pk):
    if request.method == 'POST':
        selections = json.loads(request.body.decode('utf-8'))
        trip = get_object_or_404(Trip, pk=trip_pk)
        for wp in selections['waypoints']:
            if wp['stopover']:
                city = City.objects.create(
                    city_name=wp['location'],
                    trip=trip,
                    visited=wp['stopover']
                )
                acts = ["activities", "food", "sports", "artist", "hotels"]
                for act in acts:
                    for a in wp[act]:
                        if a['activity_stopover']:
                            Activity.objects.create(
                                title=a['title'],
                                date=check_null(a['date']),
                                time=check_null(a['time']),
                                address=a['address'],
                                category=a['category'],
                                sub_category=a['sub_categories'][0][0],
                                url=a['url'],
                                phone=check_null(a['phone']),
                                # img_url=a['img_url'],
                                small_rate_img_url=a['small_rate_img_url'],
                                average_rating=check_null(a['average_rating']),
                                num_ratings=check_null(a['num_ratings']),
                                city=city
                            )

    return HttpResponse('', status=200)


@csrf_exempt
def interests_json(request, trip_pk):
    if request.method == 'POST':
        interests = json.loads(request.body.decode('utf-8'))
        get_trip = get_object_or_404(Trip, pk=trip_pk)
        yelp_cats = ['activities', 'food', 'hotels']
        sg_cats = ['artist1', 'artist2', 'artist3',
                   'sports1', 'sports2', 'sports3']
        for cat in yelp_cats:
            for sub_cat in interests[cat].keys():
                Interest.objects.create(
                    category=cat,
                    sub_category=sub_cat,
                    trip=get_trip
                )
        for cat in sg_cats:
            Interest.objects.create(
                category=cat,
                sub_category=interests[cat],
                trip=get_trip
            )

    return HttpResponse('', status=200)
