# Generated by Django 2.0.5 on 2018-05-26 10:58

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('pram1_status', models.IntegerField(default=0, verbose_name='引导程序状态')),
                ('pram2_status', models.IntegerField(default=0, verbose_name='互动程序状态')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '设备运行状态',
                'verbose_name_plural': '设备运行状态',
            },
        ),
        migrations.CreateModel(
            name='InteractInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='互动装置名')),
                ('login_name', models.CharField(default='', max_length=30, verbose_name='登录名')),
                ('mac', models.CharField(default='', max_length=30, verbose_name='mac地址')),
                ('ip', models.CharField(default='', max_length=30, verbose_name='外网ip地址')),
                ('software_name', models.CharField(default='', max_length=50, verbose_name='软件名')),
                ('ver', models.CharField(default='', max_length=20, verbose_name='版本号')),
                ('utime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '互动装置信息',
                'verbose_name_plural': '互动装置信息',
            },
        ),
        migrations.CreateModel(
            name='SatisfactionData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('excellent_num', models.IntegerField(default=0, verbose_name='满意数')),
                ('good_num', models.IntegerField(default=0, verbose_name='一般数')),
                ('unsatisfy_num', models.IntegerField(default=0, verbose_name='不满意数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '满意度实时数据',
                'verbose_name_plural': '满意度实时数据',
            },
        ),
        migrations.CreateModel(
            name='SatisfactionData_day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('excellent_num', models.IntegerField(default=0, verbose_name='满意数')),
                ('good_num', models.IntegerField(default=0, verbose_name='一般数')),
                ('unsatisfy_num', models.IntegerField(default=0, verbose_name='不满意数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '满意度数据(24小时)',
                'verbose_name_plural': '满意度数据(24小时)',
            },
        ),
        migrations.CreateModel(
            name='SatisfactionData_month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('excellent_num', models.IntegerField(default=0, verbose_name='满意数')),
                ('good_num', models.IntegerField(default=0, verbose_name='一般数')),
                ('unsatisfy_num', models.IntegerField(default=0, verbose_name='不满意数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '满意度数据(月度)',
                'verbose_name_plural': '满意度数据(月度)',
            },
        ),
        migrations.CreateModel(
            name='SatisfactionData_quarter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('excellent_num', models.IntegerField(default=0, verbose_name='满意数')),
                ('good_num', models.IntegerField(default=0, verbose_name='一般数')),
                ('unsatisfy_num', models.IntegerField(default=0, verbose_name='不满意数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '满意度数据(季度)',
                'verbose_name_plural': '满意度数据(季度)',
            },
        ),
        migrations.CreateModel(
            name='SatisfactionData_week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('excellent_num', models.IntegerField(default=0, verbose_name='满意数')),
                ('good_num', models.IntegerField(default=0, verbose_name='一般数')),
                ('unsatisfy_num', models.IntegerField(default=0, verbose_name='不满意数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '满意度数据(周)',
                'verbose_name_plural': '满意度数据(周)',
            },
        ),
        migrations.CreateModel(
            name='SatisfactionData_year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('excellent_num', models.IntegerField(default=0, verbose_name='满意数')),
                ('good_num', models.IntegerField(default=0, verbose_name='一般数')),
                ('unsatisfy_num', models.IntegerField(default=0, verbose_name='不满意数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '满意度数据(年度)',
                'verbose_name_plural': '满意度数据(年度)',
            },
        ),
        migrations.CreateModel(
            name='wifiprobeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('wifi_3m_num', models.IntegerField(default=0, verbose_name='人流量数据(3米)')),
                ('wifi_1m_num', models.IntegerField(default=0, verbose_name='有效客户数(1米)')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '人流量实时数据',
                'verbose_name_plural': '人流量实时数据',
            },
        ),
        migrations.CreateModel(
            name='wifiprobeData_day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('wifi_3m_num', models.IntegerField(default=0, verbose_name='人流量数据(3米)')),
                ('wifi_1m_num', models.IntegerField(default=0, verbose_name='有效客户数(1米)')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '人流量数据(24小时)',
                'verbose_name_plural': '人流量数据(24小时)',
            },
        ),
        migrations.CreateModel(
            name='wifiprobeData_month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('wifi_3m_num', models.IntegerField(default=0, verbose_name='人流量数据(3米)')),
                ('wifi_1m_num', models.IntegerField(default=0, verbose_name='有效客户数(1米)')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '人流量数据(月度)',
                'verbose_name_plural': '人流量数据(月度)',
            },
        ),
        migrations.CreateModel(
            name='wifiprobeData_quarter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('wifi_3m_num', models.IntegerField(default=0, verbose_name='人流量数据(3米)')),
                ('wifi_1m_num', models.IntegerField(default=0, verbose_name='有效客户数(1米)')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '人流量数据(季度)',
                'verbose_name_plural': '人流量数据(季度)',
            },
        ),
        migrations.CreateModel(
            name='wifiprobeData_week',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('wifi_3m_num', models.IntegerField(default=0, verbose_name='人流量数据(3米)')),
                ('wifi_1m_num', models.IntegerField(default=0, verbose_name='有效客户数(1米)')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '人流量数据(周)',
                'verbose_name_plural': '人流量数据(周)',
            },
        ),
        migrations.CreateModel(
            name='wifiprobeData_year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, verbose_name='互动装置名')),
                ('wifi_3m_num', models.IntegerField(default=0, verbose_name='人流量数据(3米)')),
                ('wifi_1m_num', models.IntegerField(default=0, verbose_name='有效客户数(1米)')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': '人流量数据(年度)',
                'verbose_name_plural': '人流量数据(年度)',
            },
        ),
    ]
