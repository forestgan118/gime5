# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-02 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('macdata', '0007_masterinfo2'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterinfo1',
            name='updatetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新时间'),
        ),
    ]
