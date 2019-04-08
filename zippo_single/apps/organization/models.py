# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

# Create your models here.
class RegionDict(models.Model):

    name = models.CharField(default="", max_length=20, verbose_name=u"区域")
    desc = models.CharField(default="", max_length=200, verbose_name=u"区域经销商")
    device_id=models.CharField(default="", max_length=50, verbose_name=u"rasp设备id")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"区域"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class ProvinceDict(models.Model):
    region = models.ForeignKey(RegionDict, verbose_name=u"所属区域")
    name = models.CharField(default="",max_length=20, verbose_name=u"省")
    desc = models.CharField(default="",max_length=200, verbose_name=u"区域经销商")
    device_id=models.CharField(default="", max_length=50, verbose_name=u"rasp设备id")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"省份"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CityDict(models.Model):
    region = models.ForeignKey(RegionDict, verbose_name=u"所属区域")
    province = models.ForeignKey(ProvinceDict, verbose_name=u"所属省份",default="")
    name = models.CharField(default="", max_length=20, verbose_name=u"城市")
    desc = models.CharField(default="", max_length=200, verbose_name=u"区域经销商")
    device_id=models.CharField(default="", max_length=50, verbose_name=u"rasp设备id")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

'''
class DistrictDict(models.Model):
    city = models.ForeignKey(CityDict, verbose_name=u"所属城市")
    name = models.CharField(max_length=20, verbose_name=u"区域")
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"区域"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
'''

'''
class Org(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    tag = models.CharField(max_length=10, verbose_name=u"机构标签", default="全国知名")
    image = models.ImageField(
        max_length=100, upload_to="org/%Y%m", verbose_name=u"logo")
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    org_id = models.CharField(max_length=10, verbose_name=u"机构id")
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市")
    equipment_nums = models.IntegerField(default=0, verbose_name=u"互动装置数")
    device_nums = models.IntegerField(default=0, verbose_name=u"互动器件数")
    point_nums = models.IntegerField(default=0, verbose_name=u"互动点数")
    act_nums = models.IntegerField(default=0, verbose_name=u"互动数")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
'''

class Store(models.Model):
    region = models.ForeignKey(RegionDict, verbose_name=u"所属区域")
    province = models.ForeignKey(ProvinceDict, verbose_name=u"所属省份",default="")
    city = models.ForeignKey(CityDict, verbose_name=u"所属城市")
    name = models.CharField(default="", max_length=50, verbose_name=u"门店名")
    desc = models.CharField(default="", max_length=200, verbose_name=u"区域经销商")
#    city = models.ForeignKey(CityDict, verbose_name=u"所在城市")
    
    device_id=models.CharField(default="", max_length=50, verbose_name=u"rasp设备id")
    address = models.CharField(default="", max_length=150, verbose_name=u"机构地址")
    store_id = models.CharField(default="", max_length=10, verbose_name=u"门店id")
    wifi_id = models.CharField(default="", max_length=50, verbose_name=u"wifi设备id")
    add_time = models.DateTimeField(default=datetime.now)
    cityname = models.CharField(default="", max_length=30, verbose_name=u"城市")
    provincename = models.CharField(default="", max_length=30, verbose_name=u"省份")
    regionname = models.CharField(default="", max_length=30, verbose_name=u"区域")
    class Meta:
        verbose_name = u"门店"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_store_nums(self):
        """
        获取课程数
        :return:
        """
        return self.store_set.all().count()


class SaleProduct(models.Model):
    store = models.CharField(default="", max_length=50, verbose_name=u"门店")
    city= models.CharField(default="", max_length=50, verbose_name=u"城市")
    province= models.CharField(default="", max_length=50, verbose_name=u"省份")
    region= models.CharField(default="", max_length=50, verbose_name=u"区域")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    classification = models.CharField(default="", max_length=20, verbose_name=u"分类")
    item = models.CharField(default="", max_length=50, verbose_name=u"商品型号")
    quantity = models.IntegerField(default=0, verbose_name=u"数量")
    price = models.FloatField(default=0.0, verbose_name=u"单价")
    sum = models.FloatField(default=0,verbose_name=u"总价")
    device_id=models.CharField(default="", max_length=50, verbose_name=u"rasp设备id")

    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"录入时间")

    class Meta:
        verbose_name = u"机具销售"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class SaleProduct_day(models.Model):
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province = models.CharField(default="", max_length=20, verbose_name=u"省份")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    store = models.CharField(default="", max_length=50, verbose_name=u"门店名")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    classification = models.CharField(default="", max_length=20, verbose_name=u"分类")
    item = models.CharField(default="", max_length=50, verbose_name=u"商品型号")
    quantity_pro = models.CharField(default="", max_length=50, verbose_name=u"数量")
    price_pro = models.CharField(default="", max_length=50, verbose_name=u"单价")
    sum_pro = models.CharField(default="", max_length=50,verbose_name=u"销售额")
    quantity_total_pro=models.CharField(default="", max_length=50, verbose_name=u"累计数量")
    sum_total_pro=models.CharField(default="", max_length=50,verbose_name=u"累计销售额")
    quantity_total_proj=models.CharField(default="", max_length=50, verbose_name=u"火机累计数量")
    sum_total_proj=models.CharField(default="", max_length=50,verbose_name=u"火机累计销售额")
    quantity_total_prop=models.CharField(default="", max_length=50, verbose_name=u"配件累计数量")
    sum_total_prop=models.CharField(default="", max_length=50,verbose_name=u"配件累计销售额")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"录入时间")
    device_id=models.CharField(default="", max_length=50, verbose_name=u"rasp设备id")
    class Meta:
        verbose_name = u"门店数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.store

class Sum_day_store(models.Model):
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province = models.CharField(default="", max_length=20, verbose_name=u"省份")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    store = models.CharField(default="", max_length=50, verbose_name=u"门店名")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    quantity_pro = models.CharField(default="", max_length=50, verbose_name=u"数量")
    price_pro = models.CharField(default="", max_length=50, verbose_name=u"单价")
    sum_pro = models.CharField(default="", max_length=50,verbose_name=u"总价")
    quantity_total_pro=models.CharField(default="", max_length=50, verbose_name=u"累计数量")
    sum_total_pro=models.CharField(default="", max_length=50,verbose_name=u"累计总价")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"录入时间")
    device_id=models.CharField(default="", max_length=50, verbose_name=u"rasp设备id")
    class Meta:
        verbose_name = u"门店数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.store

class SaleProduct_day_city(models.Model):
    store = models.CharField(default="", max_length=50, verbose_name=u"门店名")
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province = models.CharField(default="", max_length=20, verbose_name=u"省份")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    classification = models.CharField(default="", max_length=20, verbose_name=u"分类")
    item = models.CharField(default="", max_length=50, verbose_name=u"商品型号")
    quantity_pro = models.CharField(default="", max_length=50, verbose_name=u"数量")
    price_pro = models.CharField(default="", max_length=50, verbose_name=u"单价")
    sum_pro = models.CharField(default="", max_length=50,verbose_name=u"总价")
    quantity_total_pro=models.CharField(default="", max_length=50, verbose_name=u"累计数量")
    sum_total_pro=models.CharField(default="", max_length=50,verbose_name=u"累计总价")
    device_id=models.CharField(default="", max_length=50, verbose_name=u"rasp设备id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"录入时间")

    class Meta:
        verbose_name = u"城市数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.city

class Sum_day_city(models.Model):
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province = models.CharField(default="", max_length=20, verbose_name=u"省份")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    quantity_pro = models.CharField(default="", max_length=50, verbose_name=u"数量")
    price_pro = models.CharField(default="", max_length=50, verbose_name=u"单价")
    sum_pro = models.CharField(default="", max_length=50,verbose_name=u"总价")
    quantity_total_pro=models.CharField(default="", max_length=50, verbose_name=u"累计数量")
    sum_total_pro=models.CharField(default="", max_length=50,verbose_name=u"累计总价")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"录入时间")

    class Meta:
        verbose_name = u"城市数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.city

class SaleProduct_day_province(models.Model):
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province = models.CharField(default="", max_length=20, verbose_name=u"省份")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    classification = models.CharField(default="", max_length=20, verbose_name=u"分类")
    item = models.CharField(default="", max_length=50, verbose_name=u"商品型号")
    quantity_pro = models.CharField(default="", max_length=50, verbose_name=u"数量")
    price_pro = models.CharField(default="", max_length=50, verbose_name=u"单价")
    sum_pro = models.CharField(default="", max_length=50,verbose_name=u"总价")
    quantity_total_pro=models.CharField(default="", max_length=50, verbose_name=u"累计数量")
    sum_total_pro=models.CharField(default="", max_length=50,verbose_name=u"累计总价")
    store = models.CharField(default="", max_length=50, verbose_name=u"门店名")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    device_id=models.CharField(default="", max_length=50, verbose_name=u"rasp设备id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"录入时间")

    class Meta:
        verbose_name = u"区域数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.province

class Sum_day_province(models.Model):
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province = models.CharField(default="", max_length=20, verbose_name=u"省份")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    quantity_pro = models.CharField(default="", max_length=50, verbose_name=u"数量")
    price_pro = models.CharField(default="", max_length=50, verbose_name=u"单价")
    sum_pro = models.CharField(default="", max_length=50,verbose_name=u"总价")
    quantity_total_pro=models.CharField(default="", max_length=50, verbose_name=u"累计数量")
    sum_total_pro=models.CharField(default="", max_length=50,verbose_name=u"累计总价")
    
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"录入时间")

    class Meta:
        verbose_name = u"区域数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.province

        
class SaleProduct_day_region(models.Model):
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    province = models.CharField(default="", max_length=20, verbose_name=u"省份")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    classification = models.CharField(default="", max_length=20, verbose_name=u"分类")
    item = models.CharField(default="", max_length=50, verbose_name=u"商品型号")
    quantity_pro = models.CharField(default="", max_length=50, verbose_name=u"数量")
    price_pro = models.CharField(default="", max_length=50, verbose_name=u"单价")
    sum_pro = models.CharField(default="", max_length=50,verbose_name=u"总价")
    quantity_total_pro=models.CharField(default="", max_length=50, verbose_name=u"累计数量")
    sum_total_pro=models.CharField(default="", max_length=50,verbose_name=u"累计总价")
    store = models.CharField(default="", max_length=50, verbose_name=u"门店名")
    city = models.CharField(default="", max_length=20, verbose_name=u"城市")
    device_id=models.CharField(default="", max_length=50, verbose_name=u"rasp设备id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"录入时间")

    class Meta:
        verbose_name = u"区域数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.region

class Sum_day_region(models.Model):
    region = models.CharField(default="", max_length=20, verbose_name=u"区域")
    time = models.DateField(default=datetime.now, verbose_name=u"时间")
    quantity_pro = models.CharField(default="", max_length=50, verbose_name=u"数量")
    price_pro = models.CharField(default="", max_length=50, verbose_name=u"单价")
    sum_pro = models.CharField(default="", max_length=50,verbose_name=u"总价")
    quantity_total_pro=models.CharField(default="", max_length=50, verbose_name=u"累计数量")
    sum_total_pro=models.CharField(default="", max_length=50,verbose_name=u"累计总价")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"录入时间")

    class Meta:
        verbose_name = u"区域数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.region

