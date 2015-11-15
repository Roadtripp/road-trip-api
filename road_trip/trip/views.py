from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import TripPermissions, CityPermissions, ActivityPermissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Trip, City, Interest, Activity
from .city_selector import *
from .serializers import TripSerializer, CitySerializer, ActivitySerializer
from django.views.decorators.csrf import csrf_exempt
import json
from .event_searches import search_events
from django.contrib.auth.models import User


# Create your views here.
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = (TripPermissions,)
    authentication_classes = (TokenAuthentication,)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (CityPermissions,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        trip_pk = self.kwargs["trip_pk"]
        tr = get_object_or_404(Trip, pk=trip_pk)
        return self.queryset.filter(trip=tr).order_by('id')

    def get_serializer_context(self):
        context = super().get_serializer_context().copy()
        context["trip_pk"] = self.kwargs["trip_pk"]
        return context


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = (ActivityPermissions,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        city_pk = self.kwargs["city_pk"]
        ct = get_object_or_404(City, pk=city_pk)
        return self.queryset.filter(city=ct)

    def get_serializer_context(self):
        context = super().get_serializer_context().copy()
        context["city_pk"] = self.kwargs["city_pk"]
        return context


def owned_and_not_owner(request, obj):
    if not obj.user:
        return False
    return obj.user != request.user


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
            "lowest_price": item["lowest_price"],
            "average_price": item["average_price"],
            "highest_price": item["highest_price"],
            "img_url": item["img_url"],
        }
        for item in x[category]
    ]


def suggestion_json(request, trip_pk):
    trip = get_object_or_404(Trip, pk=trip_pk)
    if owned_and_not_owner(request, trip):
        return HttpResponseForbidden()
    data = search_events(trip_pk)
    data = [{"all_activities": city} for city in data]

    c = ["activities", "food", "sport", "artist", "hotels"]
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
                    "sport": list_gen(x, "sport"),
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
        if owned_and_not_owner(request, trip):
            return HttpResponseForbidden()
        for wp in selections['waypoints']:
            if wp['stopover']:
                if len(City.objects.filter(trip=trip, city_name=wp['location']).all()) == 0:
                    city = City.objects.create(
                        city_name=wp['location'],
                        trip=trip,
                        visited=wp['stopover']
                    )
                acts = ["activities", "food", "sport", "artist", "hotels"]
                for act in acts:
                    try:
                        for a in wp[act]:
                            if a['activity_stopover']:
                                city = City.objects.get(trip=trip, city_name=wp['location'])
                                if len(Activity.objects.filter(city=city, title=a['title'])) == 0:
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
                    except KeyError:
                        continue
    return HttpResponse('', status=200)


@csrf_exempt
def interests_json(request, trip_pk):  # TODO: refactor
    if request.method == 'POST':
        interests = json.loads(request.body.decode('utf-8'))
        get_trip = get_object_or_404(Trip, pk=trip_pk)
        if owned_and_not_owner(request, get_trip):
            return HttpResponseForbidden()
        yelp_cats = ['activities', 'food', 'hotels']
        sg_cats = [('sport', 'sport1'), ('artist', 'artist1')]
        for cat in yelp_cats:
            try:
                for sub_cat in interests[cat].keys():
                    if len(Interest.objects.filter(trip=get_trip,
                                                   sub_category=sub_cat
                                                   ).all()) == 0:
                        Interest.objects.create(
                            category=cat,
                            sub_category=sub_cat,
                            trip=get_trip
                        )
            except KeyError:
                continue
        for cat in sg_cats:
            try:
                for sub_cat in interests[cat[0]][cat[1]]:
                    if len(Interest.objects
                            .filter(trip=get_trip,
                                    sub_category=interests[cat[0]][cat[1]][sub_cat]).all()) == 0:
                        Interest.objects.create(
                            category=cat[0],
                            sub_category=interests[cat[0]][cat[1]][sub_cat],
                            trip=get_trip
                        )
            except KeyError:
                continue
    return HttpResponse('', status=200)


@csrf_exempt
def user_create(request):
    if request.method == 'POST':
        user_info = json.loads(request.body.decode('utf-8'))
        user = User.objects.create_user(user_info['username'],
                                        user_info['email'],
                                        user_info['password'])
        user.save()
        return HttpResponse('', status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
    Token.objects.get(user=request.user).delete()
    return Response({'username': None})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def trip_save(request, trip_pk):
    get_trip = get_object_or_404(Trip, pk=trip_pk)
    get_trip.user = request.user
    req = json.loads(request.body.decode('utf-8'))
    dest_city = get_trip.destination.split(',')[0]
    if req['title'] == None:
        get_trip.title = "{} Trip".format(dest_city)
    else:
        get_trip.title = req['title']
    get_trip.save()
    return JsonResponse({"username": request.user.username}, status=200)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_trips(request):
    return JsonResponse({"username": request.user.username,
                         "trips": [{
                                    "id": x.pk,
                                    "title": x.title,
                                    "origin": x.origin,
                                    "destination": x.destination,
                                    "origin_date": x.origin_date,
                                    "destination_date": x.destination_date,
                                    }
                                   for x in Trip.objects
                                   .filter(user=request.user)
                                   .all()]})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def who_am_i(request):
    return JsonResponse({"username": request.user.username}, status=200)
