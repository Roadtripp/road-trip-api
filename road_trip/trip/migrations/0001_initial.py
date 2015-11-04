# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('city_name', models.CharField(max_length=255)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('visited', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255)),
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
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='trip',
            field=models.ForeignKey(to='trip.Trip'),
        ),
    ]
