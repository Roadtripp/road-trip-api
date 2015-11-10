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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('address', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('sub_category', models.CharField(max_length=255)),
                ('activity_stopover', models.BooleanField(default=False)),
                ('url', models.URLField(blank=True, null=True, max_length=255)),
                ('phone', models.CharField(blank=True, null=True, max_length=20)),
                ('img_url', models.URLField(null=True, max_length=255)),
                ('small_rate_img_url', models.URLField(blank=True, null=True, max_length=255)),
                ('large_rate_img_url', models.URLField(blank=True, null=True, max_length=255)),
                ('average_rating', models.FloatField(blank=True, null=True)),
                ('num_ratings', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('city_name', models.CharField(max_length=255)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lon', models.FloatField(blank=True, null=True)),
                ('visited', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('category', models.CharField(max_length=255)),
                ('sub_category', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(blank=True, null=True, max_length=255)),
                ('origin', models.CharField(max_length=255)),
                ('origin_date', models.DateField(blank=True, null=True)),
                ('origin_time', models.TimeField(blank=True, null=True)),
                ('origin_lat', models.FloatField(blank=True, null=True)),
                ('origin_lon', models.FloatField(blank=True, null=True)),
                ('destination', models.CharField(max_length=255)),
                ('destination_date', models.DateField(blank=True, null=True)),
                ('destination_time', models.TimeField(blank=True, null=True)),
                ('destination_lat', models.FloatField(blank=True, null=True)),
                ('destination_lon', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
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
