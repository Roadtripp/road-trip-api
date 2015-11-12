from django.contrib import admin

# Register your models here.
from .models import Activity, City, Interest, Trip


class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'origin', 'origin_date', 'origin_time',
                    'destination', 'destination_date', 'destination_time']


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date', 'time',
                    'activity_stopover', 'address', 'category',
                    'sub_category', 'url', 'phone', 'img_url',
                    'small_rate_img_url', 'large_rate_img_url',
                    'average_rating', 'num_ratings']


class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'city_name', 'lat', 'lon', 'trip_id', 'visited',
                    'activity_set']


class InterestAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'sub_category']


admin.site.register(Trip, TripAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Interest, InterestAdmin)
