# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-01 00:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0011_auto_20180731_2329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicestatus',
            name='online_duration',
        ),
        migrations.AlterField(
            model_name='devicestatus',
            name='online_status',
            field=models.CharField(default='', max_length=10, verbose_name='设备状态'),
        ),
    ]
