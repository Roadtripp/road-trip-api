from django.db import models

# Create your models here.


class Trip(models.Model):
    title = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    origin_date = models.DateField(null=True, blank=True)
    origin_time = models.TimeField(null=True, blank=True)
    origin_lat = models.FloatField(null=True, blank=True)
    origin_lon = models.FloatField(null=True, blank=True)
    destination = models.CharField(max_length=255)
    destination_date = models.DateField(null=True, blank=True)
    destination_time = models.TimeField(null=True, blank=True)
    destination_lat = models.FloatField(null=True, blank=True)
    destination_lon = models.FloatField(null=True, blank=True)


class City(models.Model):
    city_name = models.CharField(max_length=255)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    trip = models.ForeignKey(Trip)
    visited = models.BooleanField(default=False)


class Activity(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    address = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    activity_stopover = models.BooleanField(default=False)
    url = models.URLField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    img_url = models.URLField(max_length=255, null=True)
    small_rate_img_url = models.URLField(max_length=255, null=True, blank=True)
    large_rate_img_url = models.URLField(max_length=255, null=True, blank=True)
    average_rating = models.FloatField(null=True, blank=True)
    num_ratings = models.IntegerField(null=True, blank=True)
    city = models.ForeignKey(City)


class Interest(models.Model):
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    trip = models.ForeignKey(Trip)
