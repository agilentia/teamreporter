# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-10 13:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamreporter', '0004_auto_20160409_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='summary_time',
            field=models.TimeField(default=datetime.time(18, 0)),
        ),
    ]