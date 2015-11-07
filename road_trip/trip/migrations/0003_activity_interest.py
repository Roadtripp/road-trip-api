# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0002_auto_20151104_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField(null=True, blank=True)),
                ('time', models.TimeField(null=True, blank=True)),
                ('address', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('sub_category', models.CharField(max_length=255)),
                ('activity_stopover', models.BooleanField(default=False)),
                ('url', models.URLField(null=True, max_length=255, blank=True)),
                ('phone', models.CharField(null=True, max_length=20, blank=True)),
                ('img_url', models.URLField(null=True, max_length=255)),
                ('small_rate_img_url', models.URLField(null=True, max_length=255, blank=True)),
                ('large_rate_img_url', models.URLField(null=True, max_length=255, blank=True)),
                ('average_rating', models.FloatField(null=True, blank=True)),
                ('num_ratings', models.IntegerField(null=True, blank=True)),
                ('city', models.ForeignKey(to='trip.City')),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('category', models.CharField(max_length=255)),
                ('sub_category', models.CharField(max_length=255)),
                ('trip', models.ForeignKey(to='trip.Trip')),
            ],
        ),
    ]
