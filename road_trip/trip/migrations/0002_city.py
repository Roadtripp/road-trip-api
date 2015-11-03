# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('city_name', models.CharField(max_length=255)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('trip', models.ForeignKey(to='trip.Trip')),
            ],
        ),
    ]
