# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0003_activity_interest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='destination_date',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='origin_date',
        ),
        migrations.AddField(
            model_name='trip',
            name='destination_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='origin_datetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
