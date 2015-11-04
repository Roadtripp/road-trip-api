# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0002_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='visited',
            field=models.BooleanField(default=False),
        ),
    ]
