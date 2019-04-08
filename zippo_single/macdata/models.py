from django.db import models
from datetime import datetime
import django.utils.timezone as timezone
# Create your models here.
class MasterInfo2(models.Model):
    mid = models.CharField(default="", max_length=30, verbose_name=u"探测器id")
    mmac = models.CharField(max_length=30, verbose_name=u"探测器mac", default="")
    utime = models.DateTimeField(default=timezone.now, verbose_name=u"采集时间")
    store = models.CharField(max_length=20, verbose_name=u"门店", default="")
    city = models.CharField(max_length=20, verbose_name=u"城市", default="")
    province= models.CharField(max_length=20, verbose_name=u"省份", default="")
    region= models.CharField(max_length=20, verbose_name=u"区域", default="")
    device_id=models.CharField(max_length=20, verbose_name=u"设备编码", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")

    class Meta:
        verbose_name = u"探测器信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mid
class MasterInfo1(models.Model):
    mid = models.CharField(default="", max_length=30, verbose_name=u"探测器id")
    rate = models.CharField(max_length=10, verbose_name=u"发送频率", default="")
    mmac = models.CharField(max_length=30, verbose_name=u"探测器mac", default="")
    wssid=models.CharField(max_length=30, verbose_name=u"探测器连接Wifi", default="")
    wmac = models.CharField(max_length=30, verbose_name=u"探测器连接Wifi", default="")
    lat = models.CharField(max_length=20, verbose_name=u"纬度", default="")
    lon = models.CharField(max_length=20, verbose_name=u"经度", default="")
    addr = models.CharField(max_length=50, verbose_name=u"物理地址", default="")
    utime = models.DateTimeField(default=timezone.now, verbose_name=u"采集时间")
    store = models.CharField(max_length=20, verbose_name=u"门店", default="")
    city = models.CharField(max_length=20, verbose_name=u"城市", default="")
    province= models.CharField(max_length=20, verbose_name=u"省份", default="")
    region= models.CharField(max_length=20, verbose_name=u"区域", default="")
    device_id=models.CharField(max_length=20, verbose_name=u"设备编码", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    updatetime = models.DateTimeField(default=timezone.now, verbose_name=u"更新时间")

    class Meta:
        verbose_name = u"探测器信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mid

class MasterInfo(models.Model):
    mid = models.CharField(default="", max_length=30, verbose_name=u"探测器id")
    rate = models.CharField(max_length=10, verbose_name=u"发送频率", default="")
    mmac = models.CharField(max_length=30, verbose_name=u"探测器mac", default="")
    wssid=models.CharField(max_length=30, verbose_name=u"探测器连接Wifi", default="")
    wmac = models.CharField(max_length=30, verbose_name=u"探测器连接Wifi", default="")
    lat = models.CharField(max_length=20, verbose_name=u"纬度", default="")
    lon = models.CharField(max_length=20, verbose_name=u"经度", default="")
    addr = models.CharField(max_length=50, verbose_name=u"物理地址", default="")
    utime = models.DateTimeField(default=timezone.now, verbose_name=u"采集时间")
    store = models.CharField(max_length=20, verbose_name=u"门店", default="")
    city = models.CharField(max_length=20, verbose_name=u"城市", default="")
    province= models.CharField(max_length=20, verbose_name=u"省份", default="")
    region= models.CharField(max_length=20, verbose_name=u"区域", default="")
    device_id=models.CharField(max_length=20, verbose_name=u"设备编码", default="")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")

    class Meta:
        verbose_name = u"探测器信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mid

class DetailInfo(models.Model):
    mac = models.CharField(default="", max_length=30, verbose_name=u"mac地址")
    rssi = models.CharField(max_length=10, verbose_name=u"信号强度", default="")
    range = models.CharField(max_length=10, verbose_name=u"距离", default="")
    ts=models.CharField(max_length=30, verbose_name=u"手机连接的Wifi", default="")
    tmc = models.CharField(max_length=30, verbose_name=u"手机连接Wifi的mac", default="")
    tc = models.CharField(max_length=20, verbose_name=u"是否与路由器相连", default="")
    ds = models.CharField(max_length=20, verbose_name=u"手机是否睡眠", default="")
    essid0 = models.CharField(max_length=50, verbose_name=u"连接过wifi0", default="")
    essid1 = models.CharField(max_length=50, verbose_name=u"连接过wifi1", default="")
    essid2 = models.CharField(max_length=50, verbose_name=u"连接过wifi2", default="")
    essid3 = models.CharField(max_length=50, verbose_name=u"连接过wifi3", default="")
    essid4 = models.CharField(max_length=50, verbose_name=u"连接过wifi4", default="")
    essid5 = models.CharField(max_length=50, verbose_name=u"连接过wifi5", default="")
    essid6 = models.CharField(max_length=50, verbose_name=u"连接过wifi6", default="")
    mid = models.CharField(default="", max_length=30, verbose_name=u"探测器id")
    mmac = models.CharField(max_length=30, verbose_name=u"探测器mac", default="")    
    utime = models.DateTimeField(default=timezone.now, verbose_name=u"采集时间")

    class Meta:
        verbose_name = u"采集信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mac

class MacInfo_1(models.Model):
    wifi_3m_num = models.IntegerField(default=0, verbose_name=u"人流量数据(3米)")
    wifi_1m_num = models.IntegerField(default=0, verbose_name=u"有效客户数(1米)")
    #range_3 = models.CharField(max_length=10, verbose_name=u"距离_3米", default="")
    mid = models.CharField(default="", max_length=30, verbose_name=u"探测器id")
    mmac = models.CharField(max_length=30, verbose_name=u"探测器mac", default="")    
    utime = models.DateTimeField(default=timezone.now, verbose_name=u"采集时间")

    class Meta:
        verbose_name = u"人流量信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mid