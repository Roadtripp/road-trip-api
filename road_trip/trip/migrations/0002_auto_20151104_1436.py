# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='lon',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
