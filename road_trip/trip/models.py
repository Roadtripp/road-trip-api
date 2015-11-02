from django.db import models

# Create your models here.


class Trip(models.Model):
    title = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    origin_date = models.DateField(null=True, blank=True)
    origin_time = models.TimeField(null=True, blank=True)
    origin_lat = models.FloatField(default=None)
    origin_lon = models.FloatField(default=None)
    destination = models.CharField(max_length=255)
    destination_date = models.DateField(null=True, blank=True)
    destination_time = models.TimeField(null=True, blank=True)
    destination_lat = models.FloatField(default=None)
    destination_lon = models.FloatField(default=None)


class City(models.Model):
    city_name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    trip = models.ForeignKey(Trip)
    visited = models.BooleanField(default=False)
