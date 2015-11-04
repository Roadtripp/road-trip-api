from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from .models import Trip, City
from .city_selector import *
from .serializers import TripSerializer, CitySerializer

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
    suggestions = '{'+'"origin": "{}", "destination": "{}", "waypoints": ['.format(str(trip.origin), str(trip.destination)) + ', '.join(['{'+'"location": "{}", "stopover": false, "activities": []'.format(x[0]+', '+x[1])+'}' for x in find_cities(trip.origin, trip.destination)]) + ']' + '}'
    return JsonResponse(json.loads(suggestions))


def selection_json(request, trip_pk):
    if request.method == 'POST'
