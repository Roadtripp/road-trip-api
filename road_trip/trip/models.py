from django.db import models

# Create your models here.


class Trip(models.Model):
    title = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()


class City(models.Model):
    city_name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    trip = models.ForeignKey(Trip)
