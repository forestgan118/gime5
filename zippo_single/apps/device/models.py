# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
import django.utils.timezone as timezone
# Create your models here.

class Mqtt(models.Model):
    name = models.CharField(default="", max_length=30, verbose_name=u"mqtt server ip")
    login_name = models.CharField(max_length=30, verbose_name=u"登录名", default="")
    password = models.CharField(max_length=30, verbose_name=u"密码", default="")
    port = models.CharField(max_length=10,verbose_name=u"端口", default="")
    keepAlive = models.CharField(max_length=10,verbose_name=u"keepAlive", default="")
    class Meta:
        verbose_name = u"mqtt server"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class InteractInfo(models.Model):
    name = models.CharField(default="", max_length=30, verbose_name=u"互动装置名")
    login_name = models.CharField(max_length=30, verbose_name=u"登录名", default="")
    mac = models.CharField(max_length=30, verbose_name=u"mac地址", default="")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    ip = models.CharField(max_length=30, verbose_name=u"外网ip地址", default="")
    software_name = models.CharField(max_length=50, verbose_name=u"软件名", default="")
    # address_id = models.CharField(max_length=20, verbose_name=u"门店地址id", default="")
    ver = models.CharField(max_length=20, verbose_name=u"版本号", default="")
    #mendian_id = models.CharField(max_length=20, verbose_name=u"门店id", default="")
    #address = models.CharField(max_length=50, verbose_name=u"设备地址", default="")
    utime = models.DateTimeField(default=timezone.now, verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"互动装置信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class DeviceStatus(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    pram1_status = models.IntegerField(default=0, verbose_name=u"引导程序状态")
    pram2_status = models.IntegerField(default=0, verbose_name=u"互动程序状态")
    online_status= models.CharField(max_length=10,default="", verbose_name=u"设备状态")
    #software_status= models.CharField(max_length=10,default="", verbose_name=u"软件状态")
    time=models.DateField(default=datetime.now, verbose_name=u"时间")
    add_time = models.DateTimeField(default=datetime.now)
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    city=models.CharField(max_length=30, verbose_name=u"城市", default="")
    province=models.CharField(max_length=30, verbose_name=u"省份", default="")
    region=models.CharField(max_length=30, verbose_name=u"区域", default="")

    class Meta:
        verbose_name = u"设备运行状态"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class SatisfactionData(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    excellent_num = models.IntegerField(default=0, verbose_name=u"满意数")
    good_num = models.IntegerField(default=0, verbose_name=u"一般数")
    unsatisfy_num = models.IntegerField(default=0, verbose_name=u"不满意数")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"满意度实时数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class wifiprobeData(models.Model):
#    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    wifi_3m_num = models.IntegerField(default=0, verbose_name=u"人流量数据(3米)")
    wifi_1m_num = models.IntegerField(default=0, verbose_name=u"有效客户数(1米)")
    #mac_list = models.TextField(max_length=2000, verbose_name=u"有效")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"人流量实时数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
'''
class DeviceStatus(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    device_on = models.BooleanField(default=False, verbose_name=u"设备在线状态")
    device_on_time = models.DateTimeField(default=datetime.now)
    device_off = models.BooleanField(default=True, verbose_name=u"设备下线状态")
    device_off_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"设备状态"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
'''
class SatisfactionData_day(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    excellent_num = models.CharField(default="", max_length=30, verbose_name=u"满意数")
    good_num = models.CharField(default="", max_length=30, verbose_name=u"一般数")
    unsatisfy_num = models.CharField(default="", max_length=30, verbose_name=u"不满意数")
    excellent_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计满意数")
    good_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计一般数")
    unsatisfy_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计不满意数")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    province=models.CharField(max_length=30, verbose_name=u"省份", default="")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"满意度数据(24小时)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class SatisfactionData_day_city(models.Model):
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    excellent_num = models.CharField(default="", max_length=30, verbose_name=u"满意数")
    good_num = models.CharField(default="", max_length=30, verbose_name=u"一般数")
    unsatisfy_num = models.CharField(default="", max_length=30, verbose_name=u"不满意数")
    excellent_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计满意数")
    good_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计一般数")
    unsatisfy_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计不满意数")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province=models.CharField(max_length=30, verbose_name=u"省份", default="")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"满意度数据(24小时)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name        

class SatisfactionData_day_province(models.Model):
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    excellent_num = models.CharField(default="", max_length=30, verbose_name=u"满意数")
    good_num = models.CharField(default="", max_length=30, verbose_name=u"一般数")
    unsatisfy_num = models.CharField(default="", max_length=30, verbose_name=u"不满意数")
    excellent_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计满意数")
    good_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计一般数")
    unsatisfy_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计不满意数")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province=models.CharField(max_length=30, verbose_name=u"省份", default="")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"满意度数据(24小时)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name        

class SatisfactionData_day_region(models.Model):
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    excellent_num = models.CharField(default="", max_length=30, verbose_name=u"满意数")
    good_num = models.CharField(default="", max_length=30, verbose_name=u"一般数")
    unsatisfy_num = models.CharField(default="", max_length=30, verbose_name=u"不满意数")
    excellent_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计满意数")
    good_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计一般数")
    unsatisfy_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计不满意数")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province=models.CharField(max_length=30, verbose_name=u"省份", default="")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"满意度数据(24小时)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name        


class SatisfactionData_week(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    excellent_num = models.IntegerField(default=0, verbose_name=u"满意数")
    good_num = models.IntegerField(default=0, verbose_name=u"一般数")
    unsatisfy_num = models.IntegerField(default=0, verbose_name=u"不满意数")
    excellent_num_total = models.IntegerField(default=0, verbose_name=u"累计满意数")
    good_num_total = models.IntegerField(default=0, verbose_name=u"累计一般数")
    unsatisfy_num_total = models.IntegerField(default=0, verbose_name=u"累计不满意数")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"满意度数据(周)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class SatisfactionData_month(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    excellent_num = models.IntegerField(default=0, verbose_name=u"满意数")
    good_num = models.IntegerField(default=0, verbose_name=u"一般数")
    unsatisfy_num = models.IntegerField(default=0, verbose_name=u"不满意数")
    excellent_num_total = models.IntegerField(default=0, verbose_name=u"累计满意数")
    good_num_total = models.IntegerField(default=0, verbose_name=u"累计一般数")
    unsatisfy_num_total = models.IntegerField(default=0, verbose_name=u"累计不满意数")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"满意度数据(月度)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class SatisfactionData_quarter(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    excellent_num = models.IntegerField(default=0, verbose_name=u"满意数")
    good_num = models.IntegerField(default=0, verbose_name=u"一般数")
    unsatisfy_num = models.IntegerField(default=0, verbose_name=u"不满意数")
    excellent_num_total = models.IntegerField(default=0, verbose_name=u"累计满意数")
    good_num_total = models.IntegerField(default=0, verbose_name=u"累计一般数")
    unsatisfy_num_total = models.IntegerField(default=0, verbose_name=u"累计不满意数")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"满意度数据(季度)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class SatisfactionData_year(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    excellent_num = models.IntegerField(default=0, verbose_name=u"满意数")
    good_num = models.IntegerField(default=0, verbose_name=u"一般数")
    unsatisfy_num = models.IntegerField(default=0, verbose_name=u"不满意数")
    excellent_num_total = models.IntegerField(default=0, verbose_name=u"累计满意数")
    good_num_total = models.IntegerField(default=0, verbose_name=u"累计一般数")
    unsatisfy_num_total = models.IntegerField(default=0, verbose_name=u"累计不满意数")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"满意度数据(年度)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class wifiprobeData_day(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    wifi_3m_num = models.CharField(default="", max_length=30, verbose_name=u"人流量数据(3米)")
    wifi_1m_num = models.CharField(default="", max_length=30, verbose_name=u"有效客户数(1米)")
    wifi_3m_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计人流量数据(3米)")
    wifi_1m_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计有效客户数(1米)")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province=models.CharField(max_length=30, verbose_name=u"省份", default="")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    timer_fenqu=models.DateTimeField(default=datetime.now)
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"人流量数据(24小时)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class wifiprobeData_day_city(models.Model):
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    wifi_3m_num = models.CharField(default="", max_length=30, verbose_name=u"人流量数据(3米)")
    wifi_1m_num = models.CharField(default="", max_length=30, verbose_name=u"有效客户数(1米)")
    wifi_3m_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计人流量数据(3米)")
    wifi_1m_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计有效客户数(1米)")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province=models.CharField(max_length=30, verbose_name=u"省份", default="")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"人流量数据(24小时)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class wifiprobeData_day_province(models.Model):
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    wifi_3m_num = models.CharField(default="", max_length=30, verbose_name=u"人流量数据(3米)")
    wifi_1m_num = models.CharField(default="", max_length=30, verbose_name=u"有效客户数(1米)")
    wifi_3m_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计人流量数据(3米)")
    wifi_1m_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计有效客户数(1米)")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province=models.CharField(max_length=30, verbose_name=u"省份", default="")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"人流量数据(24小时)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class wifiprobeData_day_region(models.Model):
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    wifi_3m_num = models.CharField(default="", max_length=30, verbose_name=u"人流量数据(3米)")
    wifi_1m_num = models.CharField(default="", max_length=30, verbose_name=u"有效客户数(1米)")
    wifi_3m_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计人流量数据(3米)")
    wifi_1m_num_total = models.CharField(default="", max_length=30, verbose_name=u"累计有效客户数(1米)")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    province=models.CharField(max_length=30, verbose_name=u"省份", default="")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"人流量数据(24小时)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class wifiprobeData_week(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    wifi_3m_num = models.IntegerField(default=0, verbose_name=u"人流量数据(3米)")
    wifi_1m_num = models.IntegerField(default=0, verbose_name=u"有效客户数(1米)")
    wifi_3m_num_total = models.IntegerField(default=0, verbose_name=u"累计人流量数据(3米)")
    wifi_1m_num_total = models.IntegerField(default=0, verbose_name=u"累计有效客户数(1米)")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"人流量数据(周)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class wifiprobeData_month(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    wifi_3m_num = models.IntegerField(default=0, verbose_name=u"人流量数据(3米)")
    wifi_1m_num = models.IntegerField(default=0, verbose_name=u"有效客户数(1米)")
    wifi_3m_num_total = models.IntegerField(default=0, verbose_name=u"累计人流量数据(3米)")
    wifi_1m_num_total = models.IntegerField(default=0, verbose_name=u"累计有效客户数(1米)")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"人流量数据(月度)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class wifiprobeData_quarter(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    wifi_3m_num = models.IntegerField(default=0, verbose_name=u"人流量数据(3米)")
    wifi_1m_num = models.IntegerField(default=0, verbose_name=u"有效客户数(1米)")
    wifi_3m_num_total = models.IntegerField(default=0, verbose_name=u"累计人流量数据(3米)")
    wifi_1m_num_total = models.IntegerField(default=0, verbose_name=u"累计有效客户数(1米)")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"人流量数据(季度)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class wifiprobeData_year(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"互动装置名", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    device_id=models.CharField(max_length=30, verbose_name=u"设备id", default="")
    wifi_3m_num = models.IntegerField(default=0, verbose_name=u"人流量数据(3米)")
    wifi_1m_num = models.IntegerField(default=0, verbose_name=u"有效客户数(1米)")
    wifi_3m_num_total = models.IntegerField(default=0, verbose_name=u"累计人流量数据(3米)")
    wifi_1m_num_total = models.IntegerField(default=0, verbose_name=u"累计有效客户数(1米)")
    store=models.CharField(max_length=30, verbose_name=u"门店", default="")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"人流量数据(年度)"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name