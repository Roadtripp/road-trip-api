# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('origin', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
    ]
