# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-10 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamreporter', '0005_report_summary_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='summary_submitted',
            field=models.DateTimeField(null=True),
        ),
    ]
