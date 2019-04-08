# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-13 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0014_auto_20180910_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='satisfactiondata_day',
            name='city',
            field=models.CharField(default='', max_length=20, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='satisfactiondata_day',
            name='region',
            field=models.CharField(default='', max_length=20, verbose_name='区域'),
        ),
        migrations.AddField(
            model_name='satisfactiondata_month',
            name='city',
            field=models.CharField(default='', max_length=20, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='satisfactiondata_month',
            name='region',
            field=models.CharField(default='', max_length=20, verbose_name='区域'),
        ),
        migrations.AddField(
            model_name='satisfactiondata_quarter',
            name='city',
            field=models.CharField(default='', max_length=20, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='satisfactiondata_quarter',
            name='region',
            field=models.CharField(default='', max_length=20, verbose_name='区域'),
        ),
        migrations.AddField(
            model_name='satisfactiondata_week',
            name='city',
            field=models.CharField(default='', max_length=20, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='satisfactiondata_week',
            name='region',
            field=models.CharField(default='', max_length=20, verbose_name='区域'),
        ),
        migrations.AddField(
            model_name='satisfactiondata_year',
            name='city',
            field=models.CharField(default='', max_length=20, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='satisfactiondata_year',
            name='region',
            field=models.CharField(default='', max_length=20, verbose_name='区域'),
        ),
        migrations.AddField(
            model_name='wifiprobedata_day',
            name='city',
            field=models.CharField(default='', max_length=20, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='wifiprobedata_day',
            name='region',
            field=models.CharField(default='', max_length=20, verbose_name='区域'),
        ),
        migrations.AddField(
            model_name='wifiprobedata_month',
            name='city',
            field=models.CharField(default='', max_length=20, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='wifiprobedata_month',
            name='region',
            field=models.CharField(default='', max_length=20, verbose_name='区域'),
        ),
        migrations.AddField(
            model_name='wifiprobedata_quarter',
            name='city',
            field=models.CharField(default='', max_length=20, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='wifiprobedata_quarter',
            name='region',
            field=models.CharField(default='', max_length=20, verbose_name='区域'),
        ),
        migrations.AddField(
            model_name='wifiprobedata_week',
            name='city',
            field=models.CharField(default='', max_length=20, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='wifiprobedata_week',
            name='region',
            field=models.CharField(default='', max_length=20, verbose_name='区域'),
        ),
        migrations.AddField(
            model_name='wifiprobedata_year',
            name='city',
            field=models.CharField(default='', max_length=20, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='wifiprobedata_year',
            name='region',
            field=models.CharField(default='', max_length=20, verbose_name='区域'),
        ),
    ]
