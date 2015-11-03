from django.shortcuts import render, get_object_or_404
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

    def get_queryset(self):
        trip_pk = self.kwargs['trip_pk']
        tr = get_object_or_404(Trip, pk=trip_pk)
        return self.queryset.filter(trip=tr)

    def get_serializer_context(self):
        context = super().get_serializer_context().copy()
        context['trip_pk'] = self.kwargs['trip_pk']
        return context
