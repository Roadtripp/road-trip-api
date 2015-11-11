# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='average_price',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='highest_price',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='lowest_price',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
