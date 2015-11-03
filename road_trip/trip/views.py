from django.shortcuts import render
from rest_framework import viewsets
from .models import Trip, City
from .serializers import TripSerializer, CitySerializer

# Create your views here.


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
