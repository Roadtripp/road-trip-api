from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trip
        fields = ('id', 'title', 'origin', 'origin_date', 'origin_time',
                  'origin_lat', 'origin_lon', 'destination', 'destination_date',
                  'destination_time', 'destination_lat', 'destination_lon',)
