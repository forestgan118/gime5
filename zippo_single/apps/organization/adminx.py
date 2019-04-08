# /usr/bin/python
# coding:utf-8


import xadmin
from .models import RegionDict, CityDict, ProvinceDict,Store,SaleProduct,SaleProduct_day

class RegionDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']

class ProvinceDictAdmin(object):
    list_display = ['region','name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['region__name','name', 'desc', 'add_time']


class CityDictAdmin(object):
    list_display = ['province', 'name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['province__name', 'name', 'desc',
                   'add_time']  # xadmin 外键的filter要夹两个下划线__

'''
class DistrictDictAdmin(object):
    list_display = ['city', 'name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['city_name', 'name', 'desc',
                   'add_time']  # xadmin 外键的filter要夹两个下划线__


class OrgAdmin(object):
    list_display = ['name', 'desc', 'org_id', 'act_nums',
                    'device_nums', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'act_nums',
                     'device_nums', 'address', 'city']
    list_filter = ['name', 'desc', 'org_id', 'act_nums',
                   'device_nums', 'address', 'city', 'add_time']
'''

class StoreAdmin(object):
    list_display = ['name','store_id', 'city', 'address', 'device_id','wifi_id','cityname','provincename','regionname','add_time']
    search_fields = ['name', 'city', 'address', 'store_id','device_id','wifi_id','cityname','provincename','regionname']
    list_filter = ['city__name', 'name', 'address', 'store_id','device_id','wifi_id','cityname','provincename','regionname', 'add_time']

class SaleProductAdmin(object):
    list_display = ['store', 'time', 'quantity', 'price', 'sum','add_time']
    search_fields = ['store', 'time', 'quantity', 'price', 'sum','add_time']
    list_filter = ['store', 'time', 'quantity', 'price', 'sum','add_time']

class SaleProduct_dayAdmin(object):
    list_display = ['city','store','time','quantity_pro', 'price_pro','sum_pro','quantity_total_pro','sum_total_pro','add_time']
    search_fields =['city','store','time','quantity_pro', 'price_pro','sum_pro','quantity_total_pro','sum_total_pro','add_time']
    list_filter = ['city','store','time','quantity_pro', 'price_pro','sum_pro','quantity_total_pro','sum_total_pro','add_time']

#xadmin.site.register(Org, OrgAdmin)
xadmin.site.register(RegionDict, RegionDictAdmin)
xadmin.site.register(ProvinceDict, ProvinceDictAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(Store, StoreAdmin)
xadmin.site.register(SaleProduct, SaleProductAdmin)
xadmin.site.register(SaleProduct_day, SaleProduct_dayAdmin)




