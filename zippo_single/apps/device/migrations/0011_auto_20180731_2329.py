# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-31 23:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0010_auto_20180731_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicestatus',
            name='offline_time',
        ),
        migrations.RemoveField(
            model_name='devicestatus',
            name='online_time',
        ),
    ]
