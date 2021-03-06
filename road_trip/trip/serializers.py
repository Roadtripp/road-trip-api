from rest_framework import serializers
from .models import Trip, City, Activity


class ActivitySerializer(serializers.ModelSerializer):
    city_id = serializers.PrimaryKeyRelatedField(many=False,
                                                 read_only=True)

    class Meta:
        model = Activity
        fields = ('id', 'title', 'date', 'time', 'city_id',
                  'activity_stopover', 'address', 'category',
                  'sub_category', 'url', 'phone', 'img_url',
                  'small_rate_img_url', 'large_rate_img_url', 'average_rating',
                  'num_ratings')

    def create(self, validated_data):
        validated_data['activity_id'] = self.context['activity_pk']
        activity = Activity.objects.create(**validated_data)
        return activity


class CitySerializer(serializers.ModelSerializer):
    trip_id = serializers.PrimaryKeyRelatedField(many=False,
                                                 read_only=True)
    activity_set = ActivitySerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ('id', 'city_name', 'lat', 'lon', 'trip_id', 'visited',
                  'activity_set')

    def create(self, validated_data):
        validated_data['trip_id'] = self.context['trip_pk']
        city = City.objects.create(**validated_data)
        return city


class TripSerializer(serializers.ModelSerializer):
    origin_date = serializers.DateField(required=False,
                                        allow_null=True,
                                        format="%m/%d/%Y",
                                        input_formats=['iso-8601', "%m/%d/%Y",
                                                       '%Y-%m-%dT%H:%M:%S.%fZ'])
                                                    #    2015-11-19T05:00:00.000Z
    destination_date = serializers.DateField(required=False,
                                             allow_null=True,
                                             format="%m/%d/%Y",
                                             input_formats=['iso-8601', "%m/%d/%Y",
                                                            '%Y-%m-%dT%H:%M:%S.%fZ'])
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = ('id', 'title', 'origin', 'origin_date', 'origin_time',
                  'origin_lat', 'origin_lon', 'destination',
                  'destination_date', 'destination_time', 'destination_lat',
                  'destination_lon', 'cities')
        depth = 2
