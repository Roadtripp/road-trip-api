# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0004_auto_20151102_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='destination_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='destination_lon',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='origin_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='origin_lon',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
