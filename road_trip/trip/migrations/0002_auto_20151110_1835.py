# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='destination_datetime',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='origin_datetime',
        ),
        migrations.AddField(
            model_name='trip',
            name='destination_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='origin_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
