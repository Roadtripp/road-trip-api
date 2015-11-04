# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0003_city_visited'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='end',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='start',
        ),
        migrations.AddField(
            model_name='trip',
            name='destination_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='destination_lat',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='trip',
            name='destination_lon',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='trip',
            name='destination_time',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='origin_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='origin_lat',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='trip',
            name='origin_lon',
            field=models.FloatField(default=None),
        ),
        migrations.AddField(
            model_name='trip',
            name='origin_time',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
