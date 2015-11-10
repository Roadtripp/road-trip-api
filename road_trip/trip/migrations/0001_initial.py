# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField(null=True, blank=True)),
                ('time', models.TimeField(null=True, blank=True)),
                ('address', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('sub_category', models.CharField(max_length=255)),
                ('activity_stopover', models.BooleanField(default=False)),
                ('url', models.URLField(null=True, blank=True, max_length=255)),
                ('phone', models.CharField(null=True, blank=True, max_length=20)),
                ('img_url', models.URLField(null=True, max_length=255)),
                ('small_rate_img_url', models.URLField(null=True, blank=True, max_length=255)),
                ('large_rate_img_url', models.URLField(null=True, blank=True, max_length=255)),
                ('average_rating', models.FloatField(null=True, blank=True)),
                ('num_ratings', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('city_name', models.CharField(max_length=255)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lon', models.FloatField(null=True, blank=True)),
                ('visited', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
                ('sub_category', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(null=True, blank=True, max_length=255)),
                ('origin', models.CharField(max_length=255)),
                ('origin_date', models.DateField(null=True, blank=True)),
                ('origin_time', models.TimeField(null=True, blank=True)),
                ('origin_lat', models.FloatField(null=True, blank=True)),
                ('origin_lon', models.FloatField(null=True, blank=True)),
                ('destination', models.CharField(max_length=255)),
                ('destination_date', models.DateField(null=True, blank=True)),
                ('destination_time', models.TimeField(null=True, blank=True)),
                ('destination_lat', models.FloatField(null=True, blank=True)),
                ('destination_lon', models.FloatField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='interest',
            name='trip',
            field=models.ForeignKey(to='trip.Trip'),
        ),
        migrations.AddField(
            model_name='city',
            name='trip',
            field=models.ForeignKey(to='trip.Trip'),
        ),
        migrations.AddField(
            model_name='activity',
            name='city',
            field=models.ForeignKey(to='trip.City'),
        ),
    ]
