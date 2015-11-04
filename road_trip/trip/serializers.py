from rest_framework import serializers
from .models import Trip, City


class TripSerializer(serializers.ModelSerializer):
    origin_date = serializers.DateField(format="%m/%d/%Y",
                                        input_formats=['iso-8601', "%m/%d/%Y"])
    destination_date = serializers.DateField(format="%m/%d/%Y",
                                             input_formats=['iso-8601', "%m/%d/%Y"])

    class Meta:
        model = Trip
        fields = ('id', 'title', 'origin', 'origin_date', 'origin_time',
                  'origin_lat', 'origin_lon', 'destination',
                  'destination_date', 'destination_time', 'destination_lat',
                  'destination_lon', 'cities')


class CitySerializer(serializers.ModelSerializer):
    trip_id = serializers.PrimaryKeyRelatedField(many=False,
                                                 read_only=True)

    class Meta:
        model = City
        fields = ('id', 'city_name', 'lat', 'lon', 'trip_id', 'visited')

    def create(self, validated_data):
        validated_data['trip_id'] = self.context['trip_pk']
        city = City.objects.create(**validated_data)
        return city
