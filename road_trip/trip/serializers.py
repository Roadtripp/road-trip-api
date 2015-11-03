from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    origin_date = serializers.DateField(format="%m/%d/%Y",
                                        input_formats=['%m/%d/%Y', 'iso-8601'])
    destination_date = serializers.DateField(format="%m/%d/%Y",
                                             input_formats=['%m/%d/%Y',
                                                            'iso-8601'])

    class Meta:
        model = Trip
        fields = ('id', 'title', 'origin', 'origin_date', 'origin_time',
                  'origin_lat', 'origin_lon', 'destination',
                  'destination_date', 'destination_time', 'destination_lat',
                  'destination_lon',)
