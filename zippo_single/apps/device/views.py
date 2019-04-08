# coding:utf-8
import json
import os
import time
import datetime
import xlwt
from dateutil import parser
from django.http import FileResponse
from io import StringIO
from django.http import StreamingHttpResponse 
from io import BytesIO
from datetime import date
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from json import dumps
from django.shortcuts import render,redirect
from django.views.generic import View
from django.db.models import Q
from django.db.models import Count
from organization.models import RegionDict,CityDict,ProvinceDict, Store, SaleProduct_day, SaleProduct,SaleProduct_day_city,SaleProduct_day_province,SaleProduct_day_region,Sum_day_city,Sum_day_region,Sum_day_store,Sum_day_province
from .models import Mqtt,wifiprobeData,wifiprobeData_day_region,wifiprobeData_day_city,wifiprobeData_day_province,SatisfactionData_day_city,SatisfactionData_day_province,SatisfactionData_day_region,wifiprobeData_day,wifiprobeData_week,wifiprobeData_month,wifiprobeData_quarter,wifiprobeData_year,SatisfactionData,SatisfactionData_day,SatisfactionData_week,SatisfactionData_month,SatisfactionData_quarter,SatisfactionData_year,DeviceStatus
from macdata.models import DetailInfo, MasterInfo,MasterInfo1,MasterInfo2
from django.utils.timezone import now, timedelta
import collections
from django.http import HttpResponse
from .forms import UploadFileForm
# Create your views here.
#@sched.interval_schedule(seconds=3)  #装饰器，seconds=60意思为该函数为1分钟运行一次
class WebsocketView(View):
	def get(self,request):
		return render(request,'time.html')
        
class Return_City_DataView(View):
    def get(self,request):
        all_city=CityDict.objects.all()
        all_region = RegionDict.objects.all()
        region_id = request.GET['region']
        all_city = all_city.filter(region_id=int(region_id))
        #print (region_id)
        City_list = []
        for city in all_city:
            City_list.append(city.name)
        return HttpResponse(json.dumps(City_list))    

class Return_Store_DataView(View):
    def get(self,request):
        all_city=CityDict.objects.all()
        all_store=Store.objects.all()
        all_region = RegionDict.objects.all()
        region_id,city_name = request.GET['region'],request.GET['City']
        #print (region_id,city_name)
        select_region=all_region.filter(id=int(region_id))
        select_city=all_city.filter(name=str(city_name))
        Store_list=[]
        for city in select_city:
            select_store=all_store.filter(city__id=int(city.id))
        for store in select_store:
            Store_list.append(store.name)
        return HttpResponse(json.dumps(Store_list))

class StatusView(View):
    def get(self,request):
        all_region = RegionDict.objects.all()
        status=[]
        return render(request, "devicestatusstart.html",{"all_region":all_region,"status":status})
    def post(self, request):
        # 查找到所有的机构
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        all_province= ProvinceDict.objects.all()
        # 取出所有的城市
        all_city = CityDict.objects.all()

        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        device=DeviceStatus.objects.all()
        date_from=request.POST.get('date',"")
        #print (date_from)
        date_to=request.POST.get('date2',"")
        #print (date_to)
        region_id=request.POST.get('region',"")
        province_id=request.POST.get('province',"")
        city_id=request.POST.get('city',"")
        store_id=request.POST.get('store',"")
        if region_id=="":
            return HttpResponse("请重新选择区域")
        if province_id=="":
            return HttpResponse("请重新选择省份")
        if city_id=="":
            return HttpResponse("请重新选择城市")
        if store_id=="":
            return HttpResponse("请重新选择门店")
        if date_from=="":
            return HttpResponse("请重新选择时间")
        if date_to=="":
            return HttpResponse("请重新选择时间")
        if date_from > date_to:
                return HttpResponse("请重新选择时间")
        elif date_from <= date_to:
            if "全部" not in province_id:
                region_select = all_region.filter(name=str(region_id)).values('id')
                if len(region_select)==0:
                        return HttpResponse("请重新选择区域")
                province_select=all_province.filter(name=str(province_id)).values('id')
                if len(province_select)==0:
                    return HttpResponse("请重新选择省份")
                if "全部" not in city_id:
                    city_select = all_city.filter(name=str(city_id)).values('id')
                    
                    if len(city_select)==0:
                        return HttpResponse("请重新选择城市")
                    
                    for data in region_select:
                        region=data['id']
                    for data in province_select:
                        province=data['id']
                    for data in city_select:
                        city=data['id']
                    if "全部" not in store_id:
                        store_select = all_store.filter(name=str(store_id)).values('id')
                        if len(store_select)==0:
                            return HttpResponse("请重新选择门店")
                        for data in store_select:
                            store=data['id']
                    elif "全部" in store_id:
                        store=0
                elif "全部" in city_id:
                    region_select = all_region.filter(name=str(region_id)).values('id')
                    if len(region_select)==0:
                        return HttpResponse("请重新选择区域")
                    province_select=all_province.filter(name=str(province_id)).values('id')
                    if len(province_select)==0:
                        return HttpResponse("请重新选择省份")
                    for data in region_select:
                        region=data['id']
                    for data in province_select:
                        province=data['id']
                    city=0
                    store=0
            elif "全部" in province_id:
                region_select = all_region.filter(name=str(region_id)).values('id')
                if len(region_select)==0:
                        return HttpResponse("请重新选择区域")
                for data in region_select:
                        region=data['id']
                province=0
                city=0
                store=0
        
            '''
            if "全部" not in city_id:
                if "全部" not in store_id:
                    status = device.filter(store=str(store_id),time__range=(date_from, date_to)).values('online_status','add_time','store','city','region')
                elif "全部" in store_id:
                    status = device.filter(city=str(city_id),time__range=(date_from, date_to)).values('online_status','add_time','store','city','region')
            elif "全部" in city_id:
                status = device.filter(region=str(region_id),time__range=(date_from, date_to)).values('online_status','add_time','store','city','region')
            '''
        #print (store)
        #url_request="/device/status/"+str(region)+"/"+str(province)+"/"+str(city)+"/"+str(store)+"/"
        url_request="/device/statushome/"+str(region)+"/"+str(province)+"/"+str(city)+"/"+str(store)+"/"
        #print (url_request)
        return redirect(url_request+"?from="+str(date_from)+"&to="+str(date_to))

        #return render(request, "devicestatus.html",{"status":status,"all_region":all_region})

class StatusdetailView(View):
    def get(self,request):
        all_region = RegionDict.objects.all()
        status=[]
        return render(request, "devicestatus.html",{"all_region":all_region,"status":status})
    def post(self, request):
        # 查找到所有的机构
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        all_province= ProvinceDict.objects.all()
        # 取出所有的城市
        all_city = CityDict.objects.all()

        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        device=DeviceStatus.objects.all()
        date_from=request.POST.get('date',"")
        
        date_to=request.POST.get('date2',"")
        
        region_id=request.POST.get('region',"")
        province_id=request.POST.get('province',"")
        city_id=request.POST.get('city',"")
        store_id=request.POST.get('store',"")
        if region_id=="":
            return HttpResponse("请重新选择区域")
        if province_id=="":
            return HttpResponse("请重新选择省份")
        if city_id=="":
            return HttpResponse("请重新选择城市")
        if store_id=="":
            return HttpResponse("请重新选择门店")
        if date_from=="":
            return HttpResponse("请重新选择时间")
        if date_to=="":
            return HttpResponse("请重新选择时间")
        if date_from > date_to:
                return HttpResponse("请重新选择时间")
        elif date_from <= date_to:
            if "全部" not in province_id:
                region_select = all_region.filter(name=str(region_id)).values('id')
                if len(region_select)==0:
                        return HttpResponse("请重新选择区域")
                province_select=all_province.filter(name=str(province_id)).values('id')
                if len(province_select)==0:
                    return HttpResponse("请重新选择省份")
                if "全部" not in city_id:
                    city_select = all_city.filter(name=str(city_id)).values('id')
                    
                    if len(city_select)==0:
                        return HttpResponse("请重新选择城市")
                    
                    for data in region_select:
                        region=data['id']
                    for data in province_select:
                        province=data['id']
                    for data in city_select:
                        city=data['id']
                    if "全部" not in store_id:
                        store_select = all_store.filter(name=str(store_id)).values('id')
                        if len(store_select)==0:
                            return HttpResponse("请重新选择门店")
                        for data in store_select:
                            store=data['id']
                    elif "全部" in store_id:
                        store=0
                elif "全部" in city_id:
                    region_select = all_region.filter(name=str(region_id)).values('id')
                    if len(region_select)==0:
                        return HttpResponse("请重新选择区域")
                    province_select=all_province.filter(name=str(province_id)).values('id')
                    if len(province_select)==0:
                        return HttpResponse("请重新选择省份")
                    for data in region_select:
                        region=data['id']
                    for data in province_select:
                        province=data['id']
                    city=0
                    store=0
            elif "全部" in province_id:
                region_select = all_region.filter(name=str(region_id)).values('id')
                if len(region_select)==0:
                        return HttpResponse("请重新选择区域")
                for data in region_select:
                        region=data['id']
                province=0
                city=0
                store=0
        
            '''
            if "全部" not in city_id:
                if "全部" not in store_id:
                    status = device.filter(store=str(store_id),time__range=(date_from, date_to)).values('online_status','add_time','store','city','region')
                elif "全部" in store_id:
                    status = device.filter(city=str(city_id),time__range=(date_from, date_to)).values('online_status','add_time','store','city','region')
            elif "全部" in city_id:
                status = device.filter(region=str(region_id),time__range=(date_from, date_to)).values('online_status','add_time','store','city','region')
            '''
        #print (store)
        url_request="/device/status/"+str(region)+"/"+str(province)+"/"+str(city)+"/"+str(store)+"/"
        #url_request="/device/statushome/"+str(region)+"/"+str(province)+"/"+str(city)+"/"+str(store)+"/"
        #print (url_request)
        return redirect(url_request+"?from="+str(date_from)+"&to="+str(date_to))
        #return render(request, "devicestatus.html",{"status":status,"all_region":all_region})
        
class StatusAuthView(View):
    #login_url = '/login/'
    #redirect_field_name = 'next'
    def get(self, request,param1,param2,param3,param4):
        num1=param1
        num2=param2
        num3=param3
        num4=param4
        #print (num1)
        #print (num2)
        #print (num3)
        #print (num4)
        date_from=request.GET.get('from',"")
        date_to=request.GET.get('to',"")
        offset=request.GET.get('offset')
        limit = request.GET.get('limit')
        #print (date_from)
        #print (date_to)
        if date_from=="":
            return HttpResponse("请重新选择时间")
        if date_to=="":
            return HttpResponse("请重新选择时间")
        update_list=""
        str=""
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        all_province= ProvinceDict.objects.all()
        # 取出所有的城市
        all_city = CityDict.objects.all()
        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        region_id = all_region.filter(id=num1).values("name")
        if num2!='0':
            province_id = all_province.filter(id=num2).values("name")
        elif num2=='0':
            province_id=0
        if num3!='0':
            city_id = all_city.filter(id=num3).values("name")
        elif num3=='0':
            city_id=0
        if num4!='0':
            store_id = all_store.filter(id=num4).values("name","city_id")
        elif num4=='0':
            store_id=0
        #print (region_id,city_id,store_id)
        #series1=json.dumps(list(check_box_list))
        
        data_list=[]
        store_data=[]
        city_data=[]
        region_data=[]
        if province_id!=0 and city_id!=0 and store_id!=0:
            #data_list=Store.objects.filter(name=store_id.values('name')).values('name','cityname','regionname')
            status = MasterInfo1.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('utime','store','city','region','province','device_id','updatetime')
            status1 = MasterInfo2.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('utime')
            for data in status1:
                status.update(updatetime=data['utime']) 
            #status = DeviceStatus.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('online_status','add_time','store','city','region','province','name','time')
            #print(status)
        elif province_id!=0 and city_id!=0 and store_id==0:
            #data_list=Store.objects.filter(cityname=city_id.values('name')).values('name','cityname','regionname')
            status = MasterInfo1.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('utime','store','city','region','province','device_id','updatetime')
            status1 = MasterInfo2.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('utime')
            for data in status1:
                status.update(updatetime=data['utime']) 
            #print (data_list)
        elif province_id!=0 and city_id==0 and store_id==0:
            #data_list=Store.objects.filter(cityname=city_id.values('name')).values('name','cityname','regionname')
            status = MasterInfo1.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('utime','store','city','region','province','device_id','updatetime')
            status1 = MasterInfo2.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('utime')
            for data in status1:
                status.update(updatetime=data['utime'])
            #print (data_list)
        elif province_id==0 and city_id==0 and store_id==0:
            
            status = MasterInfo1.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('utime','store','city','region','province','device_id','updatetime')
            status1 = MasterInfo2.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('utime')
            for data in status1:
                status.update(updatetime=data['utime'])
        #print(status)
        '''
        data_list_count=status.count()
        if not offset:
            offset = 0
        if not limit:
            limit = 20    # 默认是每页20行的内容，与前端默认行数一致
        pageinator = Paginator(status, limit)   # 开始做分页

        page = int(int(offset) / int(limit) + 1)    
        response_data = {'total':data_list_count,'rows':[]}   # 必须带有rows和total这2个key，total表示总页数，rows表示每行的内容
            
        for asset in pageinator.page(page):    
            # 下面这些asset_开头的key，都是我们在前端定义好了的，前后端必须一致，前端才能接受到数据并且请求.
            #print ('asset=',asset)
            response_data['rows'].append({
                #"asset_id": '<a href="/asset/asset_list/%d" target="_blank">%d</a>' %(asset.id,asset.id),   
                "time" : asset['time'].strftime("%y-%m-%d ") if asset['time'] else "",
                "region": asset['region'] if asset['region'] else "",
                "province": asset['province'] if asset['province'] else "",
                "city": asset['city'] if asset['city'] else "",
                "store": asset['store'] if asset['store'] else "",
                "device_id": asset['name'] if asset['name'] else "",
                "add_time": asset['add_time'].strftime("%y-%m-%d %h:%m:%s") if asset['add_time'] else "",
                "online_status": asset['online_status'] if asset['online_status'] else "",
                })
        return  HttpResponse(json.dumps(response_data))
        '''
        
        if status:
            return render(request, "devicestatus.html",
                        {"status":status,
                        "all_region":all_region,
                        "region1":json.dumps(num1),
                         "province1":json.dumps(num2),
                         "city1":json.dumps(num3),
                         "store1":json.dumps(num4),
                         "date_from1":json.dumps(date_from),
                         "date_to1":json.dumps(date_to),
                        })
        else:
            return HttpResponse("没有数据")
    def toDicts(objs):
            obj_arr=[]
            for o in objs:
                    obj_arr.append(o.toDict())
            return obj_arr
        

def Caltime(date1,date2):  
        #%Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。  
        #date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")   
        #date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")  
        date1=time.strptime(date1,"%Y-%m-%d")  
        date2=time.strptime(date2,"%Y-%m-%d")  
        #根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...  
        #date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])  
        #date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])  
        date1=datetime.datetime(date1[0],date1[1],date1[2])  
        date2=datetime.datetime(date2[0],date2[1],date2[2])  
        #返回两个变量相差的值，就是相差天数  
        return date2-date1               
            
class StatushomeAuthView(View):
    #login_url = '/login/'
    #redirect_field_name = 'next'
    
    
    def get(self, request,param1,param2,param3,param4):
        num1=param1
        num2=param2
        num3=param3
        num4=param4
        date_from=request.GET.get('from',"")
        date_to=request.GET.get('to',"")
        
        if date_from=="":
            return HttpResponse("请重新选择时间")
        if date_to=="":
            return HttpResponse("请重新选择时间")
        update_list=""
        str=""
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        all_province= ProvinceDict.objects.all()
        # 取出所有的城市
        all_city = CityDict.objects.all()
        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        region_id = all_region.filter(id=num1).values("name")
        if num2!='0':
            province_id = all_province.filter(id=num2).values("name")
        elif num2=='0':
            province_id=0
        if num3!='0':
            city_id = all_city.filter(id=num3).values("name")
        elif num3=='0':
            city_id=0
        if num4!='0':
            #store_id = all_store.filter(id=num4).values("name","city_id")
            store_id = all_store.filter(id=num4).values("name","wifi_id","city_id")
        elif num4=='0':
            store_id=0
        #print (region_id,city_id,store_id)
        #series1=json.dumps(list(check_box_list))
        #duration=Caltime(date_from,date_to)
        #print ("duration=",duration)
        data_list=[]
        store_data=[]
        city_data=[]
        region_data=[]
        province_data=[]
        duration=[]
        time1=datetime.datetime.strptime(date_from,'%Y-%m-%d')
        time2=datetime.datetime.strptime(date_to,'%Y-%m-%d')
        d=(time2-time1).days+1
        #print (d)
        if province_id!=0 and city_id!=0 and store_id!=0:
            #data_list=Store.objects.filter(name=store_id.values('name')).values('name','cityname','regionname')
            #status = DeviceStatus.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to),online_status="on").values('store','city','province','region','device_id').order_by('store').distinct()
            status = MasterInfo1.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('store','city','province','region','device_id','utime').order_by('mid').distinct()
            #first_day= DeviceStatus.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('time').first()
            #last_day= DeviceStatus.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('time').last()
            for data in status:
                store_data.append(data)
            #print (store_data)
            for x in range(len(store_data)):
                #storex=store_data[x]
                day= MasterInfo1.objects.filter(store=store_data[x]['store'],time__range=(date_from, date_to)).values('time').order_by('time').distinct().count()
                duration.append(day)
            #print ("duration=",duration)
            #for x in range(len(duration)):
            #    d={'day':duration[x]}
            for x in range(len(store_data)):
                store_data[x].update(day=duration[x])                #添加字典元素
                store_data[x].update(dayoff=d-duration[x])

        elif province_id!=0 and city_id!=0 and store_id==0:
            #data_list=Store.objects.filter(cityname=city_id.values('name')).values('name','cityname','regionname')
            #status = DeviceStatus.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('store','city','region','province','name','time').order_by('store').distinct()
            status = MasterInfo1.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('store','city','province','region','device_id','utime').order_by('mid').distinct()
            #print ("status=",status)
            for data in status:
                store_data.append(data)
            #print ("store_data=",store_data)
            for x in range(len(store_data)):
                #storex=store_data[x]
                day= MasterInfo1.objects.filter(store=store_data[x]['store'],time__range=(date_from, date_to)).values('time').order_by('time').distinct().count()
                duration.append(day)
            #print ("duration=",duration)
            
            #for x in range(len(duration)):
            #    d1={'day':duration[x]}
            #print ("d1=",d1) 
            for x in range(len(store_data)):
                store_data[x].update(day=duration[x])                #添加字典元素
                store_data[x].update(dayoff=d-duration[x])
                
            for x in range(len(store_data)):
                if store_data[x]['store'] not in data_list:
                    data_list.append(store_data[x])
            print ('data_list=',data_list)

        elif province_id!=0 and city_id==0 and store_id==0:
            #data_list=Store.objects.filter(cityname=city_id.values('name')).values('name','cityname','regionname')
            status = MasterInfo1.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('store','city','province','region','device_id','utime').order_by('mid').distinct()
            #print (data_list)
            for data in status:
                store_data.append(data)
            print (store_data)
            for x in range(len(store_data)):
                #storex=store_data[x]
                day= MasterInfo1.objects.filter(store=store_data[x]['store'],time__range=(date_from, date_to)).values('time').order_by('time').distinct().count()
                duration.append(day)
            print ("duration=",duration)
            #for x in range(len(duration)):
            #    d={'day':duration[x]}
            for x in range(len(store_data)):
                store_data[x].update(day=duration[x])                #添加字典元素
                store_data[x].update(dayoff=d-duration[x])
                
            for x in range(len(store_data)):
                if store_data[x] not in data_list:
                    data_list.append(store_data[x])
            #print ('data_list=',data_list)
        elif province_id==0 and city_id==0 and store_id==0:
            status = MasterInfo1.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('store','city','province','region','device_id','utime').order_by('mid').distinct()
            for data in status:
                store_data.append(data)
            #print (store_data)
            for x in range(len(store_data)):
                #storex=store_data[x]
                day= MasterInfo1.objects.filter(store=store_data[x]['store'],time__range=(date_from, date_to)).values('time').order_by('time').distinct().count()
                duration.append(day)
            #print ("duration=",duration)
            #for x in range(len(duration)):
            #    d={'day':duration[x]}
            for x in range(len(store_data)):
                store_data[x].update(day=duration[x])                #添加字典元素
                store_data[x].update(dayoff=d-duration[x])
        if status:
            return render(request, "devicestatushome.html",
                        {"status":store_data,
                         "duration":duration,
                         "all_region":all_region,
                         "region1":json.dumps(num1),
                         "province1":json.dumps(num2),
                         "city1":json.dumps(num3),
                         "store1":json.dumps(num4),
                         "date_from1":json.dumps(date_from),
                         "date_to1":json.dumps(date_to),
                         "date_from":date_from,
                         "date_to":date_to,
                        })
        else:
            return HttpResponse("没有数据")
    def toDicts(objs):
            obj_arr=[]
            for o in objs:
                    obj_arr.append(o.toDict())
            return obj_arr
         
         
class StatustableView(View):
    
                    
    def post(self, request,param1,param2,param3,param4):
        num1=param1
        num2=param2
        num3=param3
        num4=param4
        deviceid=0
        
        if request.is_ajax():
            if request.method == 'POST':
                date_from=request.POST.get('from',"")
                date_to=request.POST.get('to',"")
      
        if date_from=="":
            return HttpResponse("请重新选择时间")
        if date_to=="":
            return HttpResponse("请重新选择时间")
        #print ("param=",num1,num2,num3,num4)
        #print(date_from,date_to)
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        #all_province= ProvinceDict.objects.all()
        # 取出所有的城市
        all_province= ProvinceDict.objects.all()
        all_city = CityDict.objects.all()
        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        region_id = all_region.filter(id=num1).values("name")
        if num2!='0':
            province_id = all_province.filter(id=num2).values("name")
        elif num2=='0':
            province_id=0
        if num3!='0':
            city_id = all_city.filter(id=num3).values("name")
        elif num3=='0':
            city_id=0
        if num4!='0':
            store_id = all_store.filter(id=num4).values("name","city_id")
        elif num4=='0':
            store_id=0
        print (region_id,city_id,store_id,date_from,date_to)

        data_list=[]
        store_data=[]
        city_data=[]
        region_data=[]
        duration=[]
        sum1=0
        quantity1=0
        sum=[]
        quantity=[]
        time1=datetime.datetime.strptime(date_from,'%Y-%m-%d')
        time2=datetime.datetime.strptime(date_to,'%Y-%m-%d')
        d=(time2-time1).days+1
        if province_id!=0 and city_id!=0 and store_id!=0:
            #data_list=Store.objects.filter(name=store_id.values('name')).values('name','cityname','regionname')
            #status = DeviceStatus.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to),online_status="on").values('store','city','province','region','device_id').order_by('store').distinct()
            status = MasterInfo1.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('store','city','province','region','device_id','utime').order_by('mid').distinct()
			#first_day= DeviceStatus.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('time').first()
            #last_day= DeviceStatus.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('time').last()
            for data in status:
                store_data.append(data)
            #print (store_data)
            for x in range(len(store_data)):
                #storex=store_data[x]
                day= MasterInfo1.objects.filter(store=store_data[x]['store'],time__range=(date_from, date_to)).values('time').order_by('time').distinct().count()
                duration.append(day)
            print ("duration=",duration)
            #for x in range(len(duration)):
            #    d={'day':duration[x]}
            for x in range(len(store_data)):
                store_data[x].update(day=duration[x])                #添加字典元素
                store_data[x].update(dayoff=d-duration[x])
            status_desc=Store.objects.filter(name=store_id.values('name')).values('name','desc')
        elif province_id!=0 and city_id!=0 and store_id==0:
            #data_list=Store.objects.filter(cityname=city_id.values('name')).values('name','cityname','regionname')
            #status = DeviceStatus.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('store','city','region','province','name','time').order_by('store').distinct()
            status = MasterInfo1.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('store','city','province','region','device_id','utime').order_by('store').distinct()
            #print ("status=",status)
            for data in status:
                store_data.append(data)
            #print (store_data)
            for x in range(len(store_data)):
                #storex=store_data[x]
                day= MasterInfo1.objects.filter(store=store_data[x]['store'],time__range=(date_from, date_to)).values('time').order_by('time').distinct().count()
                duration.append(day)
            #print ("duration=",duration)
            #for x in range(len(duration)):
            #    d={'day':duration[x]}
            for x in range(len(store_data)):
                store_data[x].update(day=duration[x])                #添加字典元素
                store_data[x].update(dayoff=d-duration[x])
            status_desc=CityDict.objects.filter(name=city_id.values('name')).values('name','desc')
        elif province_id!=0 and city_id==0 and store_id==0:
            #data_list=Store.objects.filter(cityname=city_id.values('name')).values('name','cityname','regionname')
            status = MasterInfo1.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('store','city','province','region','device_id','utime').order_by('store').distinct()
            #print (data_list)
            for data in status:
                store_data.append(data)
            #print (store_data)
            for x in range(len(store_data)):
                #storex=store_data[x]
                day= MasterInfo1.objects.filter(store=store_data[x]['store'],time__range=(date_from, date_to)).values('time').order_by('time').distinct().count()
                duration.append(day)
            #print ("duration=",duration)
            #for x in range(len(duration)):
            #    d={'day':duration[x]}
            for x in range(len(store_data)):
                store_data[x].update(day=duration[x])                #添加字典元素
                store_data[x].update(dayoff=d-duration[x])
            status_desc=ProvinceDict.objects.filter(name=province_id.values('name')).values('name','desc')
        elif province_id==0 and city_id==0 and store_id==0:
            status = MasterInfo1.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('store','city','province','region','device_id','utime').order_by('store').distinct()
            for data in status:
                store_data.append(data)
            #print (store_data)
            for x in range(len(store_data)):
                #storex=store_data[x]
                day= MasterInfo1.objects.filter(store=store_data[x]['store'],time__range=(date_from, date_to)).values('time').order_by('time').distinct().count()
                duration.append(day)
            #print ("duration=",duration)
            #for x in range(len(duration)):
            #    d={'day':duration[x]}
            for x in range(len(store_data)):
                store_data[x].update(day=duration[x])                #添加字典元素
                store_data[x].update(dayoff=d-duration[x])
            status_desc=RegionDict.objects.filter(name=region_id.values('name')).values('name','desc')
        ws =xlwt.Workbook(encoding='utf-8')
        w = ws.add_sheet(u"数据报表第一页")
        #w.write(0, 0, u"时间")
        w.write(0, 0, u"区域")
        w.write(0, 1, u"省份")
        w.write(0, 2, u"城市")
        w.write(0, 3, u"区域经销商")
        w.write(0, 4, u"门店")
        w.write(0, 5, u"设备ID")
        w.write(0, 6, u"开机时间(天)")
        w.write(0, 7, u"关机时间(天)")
        excel_row = 1
            


            
        for data in store_data:
            #data_time=data['time'].strftime("%Y-%m-%d ")
            region=data['region']
            province=data['province']
            city=data['city']
            store=data['store']
            for sale_data in status_desc:
                desc=sale_data['desc']
            deviceid=data['device_id']
            day=data['day']
            dayoff=data['dayoff']
            #w.write(excel_row, 0, data_time)
            w.write(excel_row, 0, region)
            w.write(excel_row, 1, province)
            w.write(excel_row, 2, city)
            w.write(excel_row, 3, desc)
            w.write(excel_row, 4, store)
            w.write(excel_row, 5, deviceid)
            w.write(excel_row, 6, day)
            w.write(excel_row, 7, dayoff)
            excel_row += 1
            '''
            def file_iterator(file_name, chunk_size=512):
                with open(file_name,encoding='utf-8') as f:
                    while True:
                        c = f.read(chunk_size).decode("utf8")
                        if c:
                            yield c
                        else:
                            break
            
            '''
        path=os.path
        #print(path)
        exist_file = path.exists("data.xls")
        if exist_file:
            os.remove(r"data.xls")
        ws.save("data.xls")
        return HttpResponse("下载成功")
            
class StatustabledetailView(View):
    
                    
    def post(self, request,param1,param2,param3,param4):
        num1=param1
        num2=param2
        num3=param3
        num4=param4
        deviceid=0
        
        if request.is_ajax():
            if request.method == 'POST':
                date_from=request.POST.get('from',"")
                date_to=request.POST.get('to',"")
      
        if date_from=="":
            return HttpResponse("请重新选择时间")
        if date_to=="":
            return HttpResponse("请重新选择时间")
        print ("param=",num1,num2,num3,num4)
        print(date_from,date_to)
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        #all_province= ProvinceDict.objects.all()
        # 取出所有的城市
        all_province= ProvinceDict.objects.all()
        all_city = CityDict.objects.all()
        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        region_id = all_region.filter(id=num1).values("name")
        if num2!='0':
            province_id = all_province.filter(id=num2).values("name")
        elif num2=='0':
            province_id=0
        if num3!='0':
            city_id = all_city.filter(id=num3).values("name")
        elif num3=='0':
            city_id=0
        if num4!='0':
            store_id = all_store.filter(id=num4).values("name","city_id")
        elif num4=='0':
            store_id=0
        #print (region_id,city_id,store_id,date_from,date_to)

        data_list=[]
        store_data=[]
        city_data=[]
        region_data=[]
        if province_id!=0 and city_id!=0 and store_id!=0:
            #data_list=Store.objects.filter(name=store_id.values('name')).values('name','cityname','regionname')
            status = MasterInfo1.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('utime','store','city','region','province','device_id','time','updatetime')
            status1 = MasterInfo2.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('utime')
            for data in status1:
                status.update(updatetime=data['utime']) 
            #print(status)
            status_desc=Store.objects.filter(name=store_id.values('name')).values('name','desc')
        elif province_id!=0 and city_id!=0 and store_id==0:
            #data_list=Store.objects.filter(cityname=city_id.values('name')).values('name','cityname','regionname')
            status = MasterInfo1.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('utime','store','city','region','province','name','device_id','time','updatetime')
            status1 = MasterInfo2.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('utime')
            for data in status1:
                status.update(updatetime=data['utime']) 
            #print (data_list)
            status_desc=CityDict.objects.filter(name=city_id.values('name')).values('name','desc')
        elif province_id!=0 and city_id==0 and store_id==0:
            #data_list=Store.objects.filter(cityname=city_id.values('name')).values('name','cityname','regionname')
            status = MasterInfo1.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('utime','store','city','region','province','name','device_id','time','updatetime')
            status1 = MasterInfo2.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('utime')
            for data in status1:
                status.update(updatetime=data['utime']) 
            #print (data_list)
            status_desc=ProvinceDict.objects.filter(name=province_id.values('name')).values('name','desc')
        elif province_id==0 and city_id==0 and store_id==0:
            status = MasterInfo1.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('utime','store','city','region','province','name','device_id','time','updatetime')
            status1 = MasterInfo2.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('utime')
            for data in status1:
                status.update(updatetime=data['utime']) 
            status_desc=RegionDict.objects.filter(name=region_id.values('name')).values('name','desc')
        ws =xlwt.Workbook(encoding='utf-8')
        w = ws.add_sheet(u"数据报表第一页")
        w.write(0, 0, u"时间")
        w.write(0, 1, u"区域")
        w.write(0, 2, u"省份")
        w.write(0, 3, u"城市")
        w.write(0, 4, u"区域经销商")
        w.write(0, 5, u"门店")
        w.write(0, 6, u"设备ID")
        w.write(0, 7, u"设备状态")
        w.write(0, 8, u"开机时间")
        w.write(0, 9, u"在线最新时间")
        excel_row = 1
            


            
        for data in status:
            data_time=data['time'].strftime("%Y-%m-%d ")
            region=data['region']
            province=data['province']
            city=data['city']
            store=data['store']
            for sale_data in status_desc:
                desc=sale_data['desc']
            deviceid=data['device_id']
            device_status="上线" #data['online_status']
            add_time=data['utime'].strftime('%Y-%m-%d %H:%M:%S')
            updatetime=data['updatetime'].strftime('%Y-%m-%d %H:%M:%S')
            w.write(excel_row, 0, data_time)
            w.write(excel_row, 1, region)
            w.write(excel_row, 2, province)
            w.write(excel_row, 3, city)
            w.write(excel_row, 4, desc)
            w.write(excel_row, 5, store)
            w.write(excel_row, 6, deviceid)
            w.write(excel_row, 7, device_status)
            w.write(excel_row, 8, add_time)
            w.write(excel_row, 9, updatetime)
            excel_row += 1
            '''
            def file_iterator(file_name, chunk_size=512):
                with open(file_name,encoding='utf-8') as f:
                    while True:
                        c = f.read(chunk_size).decode("utf8")
                        if c:
                            yield c
                        else:
                            break
            
            '''
        path=os.path
        #print(path)
        exist_file = path.exists("data.xls")
        if exist_file:
            os.remove(r"data.xls")
        ws.save("data.xls")
        return HttpResponse("下载成功")
            
class SoftwareView(View):
    #login_url = '/login/'
    #redirect_field_name = 'next'
    def get(self, request):
        all_region = RegionDict.objects.all()
        data_list=[]
        mqtt=Mqtt.objects.values("name","login_name","port","password","keepAlive")
        for mqtt_data in mqtt:
            print (mqtt_data['name'])
            host_name=mqtt_data['name']
            username=mqtt_data['login_name']
            password=mqtt_data['password']
            port=mqtt_data['port']
            keepAlive=mqtt_data['keepAlive']
            #print (host_name,username,password,port,keepAlive)
        return render(request, "software.html",{"all_region":all_region,
                                                "data_list":data_list,
                                                "hostname":json.dumps(host_name),
                                                "username":json.dumps(username),
                                                "port":json.dumps(port),
                                                "password":json.dumps(password),
                                                "keepAlive":json.dumps(keepAlive),
                                                })
    #store = forms.CharField()
    def post(self, request):
        # 查找到所有的机构
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        all_province= ProvinceDict.objects.all()
        # 取出所有的城市
        all_city = CityDict.objects.all()
        select_region=""
        select_city=""
        select_store=""

        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        data_list=[]
        region_id=request.POST.get('region',"")
        province_id=request.POST.get('province',"")
        city_id=request.POST.get('city',"")
        store_id=request.POST.get('store',"")
        if region_id=="":
            return HttpResponse("请重新选择区域")
        if province_id=="":
            return HttpResponse("请重新选择省份")
        if city_id=="":
            return HttpResponse("请重新选择城市")
        if store_id=="":
            return HttpResponse("请重新选择门店")
        #update=[]
        update = request.POST.getlist('inlineRadio')
        #print (region_id,city_id,store_id)
        mqtt=Mqtt.objects.values("name","login_name","port","password","keepAlive")
        for mqtt_data in mqtt:
            #print (mqtt_data['name'])
            host_name=mqtt_data['name']
            username=mqtt_data['login_name']
            password=mqtt_data['password']
            port=mqtt_data['port']
            keepAlive=mqtt_data['keepAlive']
            #print (host_name,username,password,port,keepAlive)
        
        
        
        #update=check_box_list.split(',')
        print('update=',update)
        if "全部" not in province_id:
            if "全部" not in city_id:
                #region_select = all_region.filter(name=str(region_id)).values('id')
                #city_select = all_city.filter(name=str(city_id)).values('id')
                #for data in region_select:
                #    region=data['id']
                #for data in city_select:
                #    city=data['id']
                if "全部" not in store_id:
                    device_id = all_store.filter(name=str(store_id)).values('device_id')
                    #print (device_id)
                    if not device_id:
                        return HttpResponse("请重新选择门店")
                    #for data in store_select:
                    #    device_id=data['device_id']
                    
                elif "全部" in store_id:
                    #device_id = all_city.filter(name=str(city_id)).values('device_id')
                    #store=0
                    return HttpResponse("请重新选择门店")
            elif "全部" in city_id:
                #region_select = all_region.filter(name=str(region_id)).values('id')
                #device_id = all_region.filter(name=str(region_id)).values('device_id')
                return HttpResponse("请重新选择门店")
        elif "全部" in province_id:
            return HttpResponse("请重新选择门店")
        #print (region_select,city_select,store_select)
        #if region_id and city_id and store_id and date_from and date_to :
        #if region_id and city_id and store_id :
        #url_request="/device/resource/"+str(region)+"/"+str(city)+"/"+str(store)+"/"
        #print (url_request)
        #return redirect(url_request+"?inlineRadio="+str(check_box_list))
        for device in device_id:
            deviceid=device['device_id']
        #print (update)
        files=request.FILES.getlist('updata_software')
        try:
            for f in files:
                file_path=os.path.join('update/'+str.lower(deviceid),f.name)
                #update.append(f.name)
                file=open(file_path, mode='wb+')
                for chunk in f.chunks():
                    file.write(chunk)
                file.close()
            updatecmd="success"
            #print (updatecmd)
        except Exception as e:
            print (e)
            updatecmd="failure"
            
        return render(request, "software.html",
                    {"data_list":data_list,
                     "updata_list":update,
                     "all_region":all_region,
                     #"device_id":json.dumps(str.lower(deviceid)),
                     "device_id":json.dumps(deviceid),
                     "hostname":json.dumps(host_name),
                     "username":json.dumps(username),
                     "port":json.dumps(port),
                     "password":json.dumps(password),
                     "keepAlive":json.dumps(keepAlive),
                     #"update_data":json.dumps(list(update)),
                     #"store":store_id,
                     })
                     
    def toDicts(objs):
            obj_arr=[]
            for o in objs:
                    obj_arr.append(o.toDict())
            return obj_arr

'''
class SoftwareAuthView(View):
    #login_url = '/login/'
    #redirect_field_name = 'next'
    def get(self, request,param1,param2,param3):
        num1=param1
        num2=param2
        num3=param3
        update_list=""
        update_data=[]
        update=[]
        str=""
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        #all_province= ProvinceDict.objects.all()
        # 取出所有的城市
        all_city = CityDict.objects.all()
        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        region_id = all_region.filter(id=num1).values("name")
        if num2!='0':
            city_id = all_city.filter(id=num2).values("name")
        elif num2=='0':
            city_id=0
        if num3!='0':
            store_id = all_store.filter(id=num3).values("name","city_id")
        elif num3=='0':
            store_id=0
        print (region_id,city_id,store_id)
        #series1=json.dumps(list(check_box_list))
        
        data_list=[]
        store_data=[]
        city_data=[]
        region_data=[]
        if city_id!=0 and store_id!=0:
            data_list=Store.objects.filter(name=store_id.values('name')).values('name','cityname','regionname')
            device_id=Store.objects.filter(name=store_id.values('name')).values('device_id')
            
        elif city_id!=0 and store_id==0:
            data_list=Store.objects.filter(cityname=city_id.values('name')).values('name','cityname','regionname')
            device_id=Store.objects.filter(name=store_id.values('name')).values('device_id')
            print (data_list)
        elif city_id==0 and store_id==0:
            data_list=Store.objects.filter(regionname=region_id.values('name')).values('name','cityname','regionname')
            device_id=Store.objects.filter(name=store_id.values('name')).values('device_id')
        return render(request, "software.html",
                    {"data_list":data_list,
                     "device_id":json.dumps(list(device_id)),
                     })
    def toDicts(objs):
            obj_arr=[]
            for o in objs:
                    obj_arr.append(o.toDict())
            return obj_arr
    
    
class SoftwareUpdateView(View):
    def post(self, request):
        deviceid=[]
        device_id=''
        update=[]
        data_list=[]
        store=request.POST.get('update_store','')
        #print ("updata_store=",store)
        files=request.FILES.getlist('updata_resource')
        try:
            for f in files:
                file_path=os.path.join('files',f.name)
                #update.append(f.name)
                file=open(file_path, mode='wb+')
                for chunk in f.chunks():
                    file.write(chunk)
                file.close()
            updatecmd="success"
            print (updatecmd)
            device=Store.objects.filter(name=store).values('device_id')
            for device_id in device:
                deviceid=device_id['device_id']
            device_id=json.dumps(deviceid)
            print ('device_id=',device_id)
            #updata_list=json.dumps(updata)
        except Exception as e:
            print (e)
            updatecmd="failure"
        return render(request, "software.html",
                    {'updatecmd':json.dumps(updatecmd),"device_id":device_id,"data_list":data_list})
        
'''
class ResourceView(View):
    #login_url = '/login/'
    #redirect_field_name = 'next'
    def get(self, request):
        all_region = RegionDict.objects.all()
        data_list=[]
        mqtt=Mqtt.objects.values("name","login_name","port","password","keepAlive")
        for mqtt_data in mqtt:
            #print (mqtt_data['name'])
            host_name=mqtt_data['name']
            username=mqtt_data['login_name']
            password=mqtt_data['password']
            port=mqtt_data['port']
            keepAlive=mqtt_data['keepAlive']
            #print (host_name,username,password,port,keepAlive)
        return render(request, "resource.html",{"all_region":all_region,
                                                "data_list":data_list,
                                                "hostname":json.dumps(host_name),
                                                "username":json.dumps(username),
                                                "port":json.dumps(port),
                                                "password":json.dumps(password),
                                                "keepAlive":json.dumps(keepAlive),
                                                })
    #store = forms.CharField()
    def post(self, request):
        # 查找到所有的机构
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        all_province= ProvinceDict.objects.all()
        # 取出所有的城市
        all_city = CityDict.objects.all()
        select_region=""
        select_province=""
        select_city=""
        select_store=""

        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        data_list=[]
        region_id=request.POST.get('region',"")
        province_id=request.POST.get('province',"")
        city_id=request.POST.get('city',"")
        store_id=request.POST.get('store',"")
        if region_id=="":
            return HttpResponse("请重新选择区域")
        if province_id=="":
            return HttpResponse("请重新选择省份")
        if city_id=="":
            return HttpResponse("请重新选择城市")
        if store_id=="":
            return HttpResponse("请重新选择门店")

        update = request.POST.getlist('inlineRadio')

        print (region_id,province_id,city_id,store_id,update)
       
        mqtt=Mqtt.objects.values("name","login_name","port","password","keepAlive")
        for mqtt_data in mqtt:
            #print (mqtt_data['name'])
            host_name=mqtt_data['name']
            username=mqtt_data['login_name']
            password=mqtt_data['password']
            port=mqtt_data['port']
            keepAlive=mqtt_data['keepAlive']
            #print (host_name,username,password,port,keepAlive)
        
        
        #update=check_box_list.split(',')
        #print('update=',update)
        if "全部" not in province_id:
            if "全部" not in city_id:
                #region_select = all_region.filter(name=str(region_id)).values('id')
                #city_select = all_city.filter(name=str(city_id)).values('id')
                #for data in region_select:
                #    region=data['id']
                #for data in city_select:
                #    city=data['id']
                if "全部" not in store_id:
                    device_id = all_store.filter(name=str(store_id)).values('device_id')
                    #print (device_id)
                    if not device_id:
                        return HttpResponse("请重新选择门店")
                    #for data in store_select:
                    #    device_id=data['device_id']
                    
                elif "全部" in store_id:
                    #device_id = all_city.filter(name=str(city_id)).values('device_id')
                    #store=0
                    return HttpResponse("请重新选择门店")
            elif "全部" in city_id:
                #region_select = all_region.filter(name=str(region_id)).values('id')
                #device_id = all_region.filter(name=str(region_id)).values('device_id')
                return HttpResponse("请重新选择门店")
        elif "全部" in province_id:
            return HttpResponse("请重新选择门店")
            #for data in region_select:
            #    region=data['id']
            #city=0
            #store=0
        #print (region_select,city_select,store_select)
        #if region_id and city_id and store_id and date_from and date_to :
        #if region_id and city_id and store_id :
        #url_request="/device/resource/"+str(region)+"/"+str(city)+"/"+str(store)+"/"
        #print (url_request)
        #return redirect(url_request+"?inlineRadio="+str(check_box_list))
        for device in device_id:
            deviceid=device['device_id']
        #print (deviceid)
        files=request.FILES.getlist('updata_resource')
        try:
            for f in files:
                file_path=os.path.join('update/'+str.lower(deviceid),f.name)  #将文件存放到update/deviceid 目录
                #update.append(f.name)
                #print (file_path)
                file=open(file_path, mode='wb+')
                for chunk in f.chunks():
                    file.write(chunk)
                file.close()
            updatecmd="success1"
            
            #print (updatecmd)
        except Exception as e:
            print (e)
            updatecmd="failure"
        return render(request, "resource.html",
                    {"data_list":data_list,
                     "updata_list":update,
                     "all_region":all_region,
                     #"device_id":json.dumps(str.lower(deviceid)),
                     "device_id":json.dumps(deviceid),
                     "hostname":json.dumps(host_name),
                     "username":json.dumps(username),
                     "port":json.dumps(port),
                     "password":json.dumps(password),
                     "keepAlive":json.dumps(keepAlive),
                     #"update_data":json.dumps(list(update)),
                     #"store":store_id,
                     })
                     
    def toDicts(objs):
            obj_arr=[]
            for o in objs:
                    obj_arr.append(o.toDict())
            return obj_arr
'''
class ResourceAuthView(View):
    #login_url = '/login/'
    #redirect_field_name = 'next'
    def get(self, request,param1,param2,param3):
        num1=param1
        num2=param2
        num3=param3
        update_list=""
        update_data=[]
        update=[]
        str=""
        check_box_list=request.GET.get('inlineRadio',"")
        print ("check_box_list=",check_box_list)
        #for update in check_box_list:
        update_list=check_box_list.strip(']')
        update_list=update_list.strip('[')
        update_list=update_list.strip(' ')
        print (update_list)
        update_data=update_list.split(',')
        print ('update_list=',update_data)
        for x in range(len(update_data)):
            str=update_data[x]
            str=str.strip(' ')
            data=int(str[1])
            update.append(data)
        print ("update_data=",update)
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        #all_province= ProvinceDict.objects.all()
        # 取出所有的城市
        all_city = CityDict.objects.all()
        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        region_id = all_region.filter(id=num1).values("name")
        if num2!='0':
            city_id = all_city.filter(id=num2).values("name")
        elif num2=='0':
            city_id=0
        if num3!='0':
            store_id = all_store.filter(id=num3).values("name","city_id")
        elif num3=='0':
            store_id=0
        print (region_id,city_id,store_id)
        #series1=json.dumps(list(check_box_list))
        
        data_list=[]
        store_data=[]
        city_data=[]
        region_data=[]
        if city_id!=0 and store_id!=0:
            data_list=Store.objects.filter(name=store_id.values('name')).values('name','cityname','regionname')
            device_id=Store.objects.filter(name=store_id.values('name')).values('device_id')
            
        elif city_id!=0 and store_id==0:  #城市全部门店
            data_list=Store.objects.filter(cityname=city_id.values('name')).values('name','cityname','regionname')
            device_id=CityDict.objects.filter(name=city_id.values('name')).values('device_id')
            print (data_list,device_id)
        elif city_id==0 and store_id==0:
            data_list=Store.objects.filter(regionname=region_id.values('name')).values('name','cityname','regionname')
            device_id=RegionDict.objects.filter(name=region_id.values('name')).values('device_id')
        print (device_id)
        return render(request, "resource.html",
                    {"data_list":data_list,
                     "update_list":list(update),
                     #'num':len(update),
                     #"device_id":json.dumps(list(device_id)),
                     "update_data":json.dumps(list(update)),
                     #"store":store_id,
                     })
                     
    def toDicts(objs):
            obj_arr=[]
            for o in objs:
                    obj_arr.append(o.toDict())
            return obj_arr
        


class ResourceUpdateView(View):
    #login_url = '/login/'
    #redirect_field_name = 'next'
    #def get(self, request):
    #    all_region = RegionDict.objects.all()
    #    data_list=[]
    #    return render(request, "resource.html",{"all_region":all_region,"data_list":data_list})
    
    def post(self, request):
        deviceid=[]
        device_id=''
        update=[]
        data_list=[]
        update_data = request.POST.get('update_list','')
        print (update_data)
        region=request.POST.get('update_region','')
        city=request.POST.get('update_city','')
        store=request.POST.get('update_store','')
        print ("updata_region=",region)
        print ("updata_city=",city)
        print ("updata_store=",store)
        files=request.FILES.getlist('updata_resource')
        try:
            for f in files:
                file_path=os.path.join('files',f.name)
                #update.append(f.name)
                file=open(file_path, mode='wb+')
                for chunk in f.chunks():
                    file.write(chunk)
                file.close()
            updatecmd="success"
            print (updatecmd)
            device=Store.objects.filter(name=store).values('device_id')
            for device_id in device:
                deviceid=device_id['device_id']
            device_id=json.dumps(deviceid)
            print ('device_id=',device_id)
            #updata_list=json.dumps(updata)
        except Exception as e:
            print (e)
            updatecmd="failure"
        return render(request, "resource.html",
                    {'updatecmd':json.dumps(updatecmd),"device_id":device_id,'updata_list':update_data,"data_list":data_list})
    
    
                
    def toDicts(objs):
            obj_arr=[]
            for o in objs:
                    obj_arr.append(o.toDict())
            return obj_arr
'''
class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, field)
        
def mac_data():
    #计算当天wifi探针数据
    #now = datetime.datetime.now()
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]#2019#now_time[0]
    month=now_time[1]#2#now_time[1]
    day=str(int(now_time[2]))#1#str(int(now_time[2]))
    '''
    yesterday = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d").split('-')
    year=2019#int(yesterday[0])
    month=4#int(yesterday[1])
    day=4#int(yesterday[2])
    
    
    mid=[]
    maclist1=[]
    u_time=[]
    wifi_id=[]
    wifi_id5=[]
    n1=[]
    n=0
    n0=0
    n5=0
    store_name=[]
    device_id_add=[]
    wifi_id_add=[]
    store_add=[]
    city_id=[]
    city=[]
    city_name=[]
    province_id=[]
    province=[]
    provinceid=[]
    province_name=[]
    region_id=[]
    region=[]
    region_dict_name=[]
    region_name=[]
    store_city_id=[]

    province_device=ProvinceDict.objects.values("id","name","region_id")
    for province_data in province_device:
        provinceid.append(province_data['id'])
        province.append(province_data['name'])
    #print("province=",province)
    city_device=CityDict.objects.values("id","name","region_id","province_id")
    
    for city_data in city_device:
        city_id.append(city_data['id'])
        city.append(city_data['name'])
        region_id.append(city_data['region_id'])
        province_id.append(city_data['province_id'])
    #print ("province_id=",province_id)
    region_device=RegionDict.objects.values("id","name")
    for region_data in region_device:
        region.append(region_data['id'])
        region_dict_name.append(region_data['name'])
    store_device=Store.objects.values("name","device_id","wifi_id","city_id")
    #print ("store_device=",store_device)
    for store_add in store_device:
        if store_add['wifi_id'] != "":
            store_name.append(store_add['name'])
            device_id_add.append(store_add['device_id'])
            
            wifi_id_add.append(store_add['wifi_id'])
            store_city_id.append(store_add['city_id'])
            city_index=city_id.index(store_add['city_id'])   #获取city 的index
            city_name.append(city[city_index])   #将city name加入list
            province_id_select=province_id[city_index]
            #print ("province_id_select=",province_id_select)
            province_index=provinceid.index(province_id_select)
            province_name.append(province[province_index])
            region_id_select=region_id[city_index]  #根据所选的city确定citydcit的region_id
            region_index=region.index(region_id_select)  #根据所选的citydict中的region_id
            region_name.append(region_dict_name[region_index])   #确定regiondcit中的name
    #start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
    #print ("STORE=",store_name,"CITY=",city_name,"PROVINCE=",province_name,"REGION=",region_name)
    
    master=MasterInfo.objects.values("mid")
    for x in master:
        
        m=0
        s=0
        detail_data1=DetailInfo.objects.filter(utime__year=year,utime__month=month,utime__day=day,mid=x['mid']).values("mac").first()
 
        if detail_data1!=None:
            for h in range(8,21,1):
                date_from = datetime.datetime(int(year), int(month), int(day), h, m,s) 
                date_to = datetime.datetime(int(year), int(month), int(day), (h+1), m,s) 
                print("mid=",x['mid'])
                print("date_from=",date_from)
                print("date_to=",date_to)
                #detail_data=DetailInfo.objects.filter(utime__year=year,utime__month=month,utime__day=day,utime__hour=h,utime__minute=m,utime__second=s,mid=x['mid']).values("mac","range","utime").order_by('utime')
                detail_data=DetailInfo.objects.filter(utime__range=(date_from,date_to),mid=x['mid']).values("mac","range","utime").order_by('utime')
                print("detail_data=",detail_data)
                for data in detail_data:
                    if data['mac'][:-3] not in maclist1:
                        maclist1.append(data['mac'][:-3])
                        u_time.append(data['utime'])
                        n1.append(0)
                        if float(data['range'])<=3:
                            n5=n5+1
                    
                    else:
                        index=maclist1.index(data['mac'][:-3])
                        if float(data['range'])<=1.5:
                            if (data['utime']-u_time[index]).total_seconds()<=10 and (data['utime']-u_time[index]).total_seconds()>=8:
                                n1[index]=1 #如果同一个MAC时间大于8，小于10秒则判断为有效客户
                                #if n1[index]>10:
                                #    n2=n2+1
                                u_time[index]=data['utime']
                            else:
                                #n1=0
                                u_time[index]=data['utime']
                
                dict = {}
                
                for key in n1:
                    dict[key] = dict.get(key, 0) + 1  #记录无效客户
                #print("dict=",dict)
                day_time=now().date() + timedelta(days=0)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
                fenqu=str(year)+"-"+str(month)+"-"+str(day)+" "+str(h+1)+":00:00"
                #time_string = fenqu.ctime() # 'Thu Dec 22 10:35:25 2016'，这里可以是任意的时间格式
                datetime_struct = parser.parse(fenqu)
                print (type(datetime_struct)) # <type 'datetime.datetime'>
                print (datetime_struct.strftime('%Y-%m-%d %H:%M:%S')) 
                print (fenqu)
                if dict:
                    n0=dict[0] #记录无效客户数量
                    n=len(n1)-n0  #总数-无效客户=有效客户数
                    index_wifi=wifi_id_add.index(x['mid'])
                    store_select=store_name[index_wifi]  #判断wifi设备id对应的门店
                    wifiid_select=wifi_id_add[index_wifi]
                    city_select=city_name[index_wifi]
                    device_select=device_id_add[index_wifi]
                    province_select=province_name[index_wifi]
                    region_select=region_name[index_wifi]
                    wifi3_total=wifiprobeData_day.objects.filter(device_id=device_select).aggregate(nums=Sum('wifi_3m_num'))  #聚合方法计算累计3m
                    wifi1_total=wifiprobeData_day.objects.filter(device_id=device_select).aggregate(nums1=Sum('wifi_1m_num'))  #聚合方法计算累计1m
                    if wifi3_total['nums']==None:
                        wifi3_total['nums']=0
                    if wifi1_total['nums1']==None:
                        wifi1_total['nums1']=0
                    wifiprobeData_day.objects.create(device_id=device_select,wifi_3m_num=n5,wifi_1m_num=n,store=store_select,city=city_select,region=region_select,province=province_select,wifi_3m_num_total=wifi3_total['nums'],wifi_1m_num_total=wifi1_total['nums1'],time=day_time,timer_fenqu=fenqu)
                #print ("n=",n)
                #print ("n5=",n5)
                maclist1=[]
                u_time=[]
                n5=0
                n=0
                dict.clear()
                n1=[]
    print("end")

    wifi3=[]
    wifi1=[]
    city=[]
    wifi1_total=[]
    wifi3_total=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    wifi_data=wifiprobeData_day.objects.filter(time__year=year,time__month=month,time__day=day).values("city","region","province","wifi_3m_num","wifi_1m_num","wifi_3m_num_total","wifi_1m_num_total")
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳

    for wifi_city in wifi_data:
        if wifi_city['city'] not in city:
            wifi1.append(float(wifi_city['wifi_1m_num']))
            wifi3.append(float(wifi_city['wifi_3m_num']))
            wifi1_total.append(float(wifi_city['wifi_1m_num_total']))
            wifi3_total.append(float(wifi_city['wifi_3m_num_total']))
            city.append(wifi_city['city'])
        elif wifi_city['city'] in city:
            index_wifi=city.index(wifi_city['city'])
            wifi1[index_wifi]=wifi1[index_wifi]+float(wifi_city['wifi_1m_num'])
            wifi3[index_wifi]=wifi3[index_wifi]+float(wifi_city['wifi_3m_num'])
            wifi1_total[index_wifi]=wifi1_total[index_wifi]+float(wifi_city['wifi_1m_num_total'])
            wifi3_total[index_wifi]=wifi3_total[index_wifi]+float(wifi_city['wifi_3m_num_total'])

    for x in range(len(city)):
        city_index=city_name.index(city[x])
        wifiprobeData_day_city.objects.create(wifi_1m_num=wifi1[x],wifi_3m_num=wifi3[x],wifi_1m_num_total=wifi1_total[x],wifi_3m_num_total=wifi3_total[x],add_time= time_stamp,time=day_time,city=city[x],region=region_name[city_index],province=province_name[city_index])  #存入当天数据
    
    wifi3=[]
    wifi1=[]
    city=[]
    wifi1_total=[]
    wifi3_total=[]    
    print("end1")
    province=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    wifi_data=wifiprobeData_day_city.objects.filter(time__year=year,time__month=month,time__day=day).values("city","region","province","wifi_3m_num","wifi_1m_num","wifi_3m_num_total","wifi_1m_num_total")
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳

    for wifi_province in wifi_data:
        if wifi_province['province'] not in province:
            wifi1.append(float(wifi_province['wifi_1m_num']))
            wifi3.append(float(wifi_province['wifi_3m_num']))
            wifi1_total.append(float(wifi_province['wifi_1m_num_total']))
            wifi3_total.append(float(wifi_province['wifi_3m_num_total']))
            province.append(wifi_province['province'])
        elif wifi_province['province'] in province:
            index_wifi=province.index(wifi_province['province'])
            wifi1[index_wifi]=wifi1[index_wifi]+float(wifi_province['wifi_1m_num'])
            wifi3[index_wifi]=wifi3[index_wifi]+float(wifi_province['wifi_3m_num'])
            wifi1_total[index_wifi]=wifi1_total[index_wifi]+float(wifi_province['wifi_1m_num_total'])
            wifi3_total[index_wifi]=wifi3_total[index_wifi]+float(wifi_province['wifi_3m_num_total'])
    for x in range(len(province)):
        if province[x]!="":
            province_index=province_name.index(province[x])
            wifiprobeData_day_province.objects.create(wifi_1m_num=wifi1[x],wifi_3m_num=wifi3[x],wifi_1m_num_total=wifi1_total[x],wifi_3m_num_total=wifi3_total[x],add_time= time_stamp,time=day_time,region=region_name[province_index],province=province[x])  #存入当天数据
    
    
    wifi3=[]
    wifi1=[]
    wifi1_total=[]
    wifi3_total=[]    
    print("end2")
    province=[]
    region=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    wifi_data=wifiprobeData_day_city.objects.filter(time__year=year,time__month=month,time__day=day).values("city","region","province","wifi_3m_num","wifi_1m_num","wifi_3m_num_total","wifi_1m_num_total")
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳

    for wifi_region in wifi_data:
        if wifi_region['region'] not in region:
            wifi1.append(float(wifi_region['wifi_1m_num']))
            wifi3.append(float(wifi_region['wifi_3m_num']))
            wifi1_total.append(float(wifi_region['wifi_1m_num_total']))
            wifi3_total.append(float(wifi_region['wifi_3m_num_total']))
            region.append(wifi_region['region'])
        elif wifi_region['region'] in region:
            index_wifi=region.index(wifi_region['region'])
            wifi1[index_wifi]=wifi1[index_wifi]+float(wifi_region['wifi_1m_num'])
            wifi3[index_wifi]=wifi3[index_wifi]+float(wifi_region['wifi_3m_num'])
            wifi1_total[index_wifi]=wifi1_total[index_wifi]+float(wifi_region['wifi_1m_num_total'])
            wifi3_total[index_wifi]=wifi3_total[index_wifi]+float(wifi_region['wifi_3m_num_total'])
    for x in range(len(region)):
        wifiprobeData_day_region.objects.create(wifi_1m_num=wifi1[x],wifi_3m_num=wifi3[x],wifi_1m_num_total=wifi1_total[x],wifi_3m_num_total=wifi3_total[x],add_time= time_stamp,time=day_time,region=region[x])  #存入当天数据
    
    wifi3=[]
    wifi1=[]
    wifi1_total=[]
    wifi3_total=[]    
    print("end3")
    region=[]
    
   
    

    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=2019#now_time[0]
    month=2#now_time[1]
    day=1#str(int(now_time[2]))
    '''
    satisfy_data=[]
    satisfy_day=[]
    satis_data=[]
    good_day=[]
    unsatisfy_day=[]
    sy_device_id=[]
    device_id_satisfy_day=[]
    device_id_id=device_id_add[:]
    device_sa=[]
    execllect=[]
    good=[]
    unsatisfy=[]

    #计算当天满意度数据
    #从实时数据库SatisfactionData获取实时数据
    satisfy_data=SatisfactionData.objects.filter(add_time__year=year,add_time__month=month,add_time__day=day).values("excellent_num","good_num","unsatisfy_num","device_id").order_by('add_time')
    #print ("satisfy_data=",satisfy_data)
    if satisfy_data :
        for satis_data in satisfy_data:   #字典遍历
            execllect.append(float(satis_data['excellent_num']))
            good.append(float(satis_data['good_num']))
            unsatisfy.append(float(satis_data['unsatisfy_num']))
            sy_device_id.append(satis_data['device_id'])
            #print ("sy_device_id=",sy_device_id)
        for x in range(len(sy_device_id)):
            if sy_device_id[x] not in device_id_satisfy_day:
                device_id_satisfy_day.append(sy_device_id[x])
                satisfy_day.append(execllect[x])
                good_day.append(good[x])
                unsatisfy_day.append(unsatisfy[x])
            elif sy_device_id[x] in device_id_satisfy_day:
                satisfy_index=device_id_satisfy_day.index(sy_device_id[x])
                satisfy_day[satisfy_index]=satisfy_day[satisfy_index]+execllect[x]
                good_day[satisfy_index]=good_day[satisfy_index]+good[x]
                unsatisfy_day[satisfy_index]=unsatisfy_day[satisfy_index]+unsatisfy[x]
        day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
        time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
        #print ("device_id_satisfy_day=",device_id_satisfy_day)
        #print ("device_id_id=",device_id_id)
        for i in range(len(device_id_satisfy_day)):
            device_id_index=device_id_id.index(device_id_satisfy_day[i])
            store_select=store_name[device_id_index]
            city_select=city_name[device_id_index]
            region_select=region_name[device_id_index]
            province_select=province_name[device_id_index]
            device_select=device_id_id[device_id_index]
            #device_sa.append(device_select)
            #print ("device_select=",device_select)
            excellent_num_total=SatisfactionData_day.objects.filter(device_id=device_select).aggregate(nums1=Sum('excellent_num'))  #聚合方法计算累计excellent_num
            good_num_total=SatisfactionData_day.objects.filter(device_id=device_select).aggregate(nums2=Sum('good_num'))  #聚合方法计算累计good_num 
            unsatisfy_num_total=SatisfactionData_day.objects.filter(device_id=device_select).aggregate(nums3=Sum('unsatisfy_num'))  #聚合方法计算累计unsatisfy_num
            if excellent_num_total['nums1']==None:
                excellent_num_total['nums1']=0
            good_num_total=SatisfactionData_day.objects.filter(device_id=device_select).aggregate(nums2=Sum('good_num'))  #聚合方法计算累计good_num 
            if good_num_total['nums2'] ==None:
                good_num_total['nums2']=0 
            unsatisfy_num_total=SatisfactionData_day.objects.filter(device_id=device_select).aggregate(nums3=Sum('unsatisfy_num'))  #聚合方法计算累计unsatisfy_num
            if  unsatisfy_num_total['nums3']==None:
                unsatisfy_num_total['nums3']=0
            SatisfactionData_day.objects.create(device_id=device_select,name=device_id_satisfy_day[i],excellent_num=satisfy_day[i],good_num=good_day[i],unsatisfy_num=unsatisfy_day[i],excellent_num_total=excellent_num_total['nums1'],good_num_total=good_num_total['nums2'],unsatisfy_num_total=unsatisfy_num_total['nums3'],add_time= time_stamp,time=day_time,store=store_select,city=city_select,region=region_select,province=province_select)  #存入当天数据
    execllect=[]
    good=[]
    unsatisfy=[]
    sy_device_id=[]
    device_id_satisfy_day=[] 
    satisfy_day=[]
    satis_data=[]
    good_day=[]
    unsatisfy_day=[]
    
    excellent_add=[]
    good_add=[]
    unsatisfy_add=[]
    device_satisfy=[]
    store_name_add=[]
    city=[]
    ex1=[]
    go1=[]
    un1=[]
    ex_total=[]
    go_total=[]
    un_total=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    sati=SatisfactionData_day.objects.filter(time__year=year,time__month=month,time__day=day).values("excellent_num","good_num","unsatisfy_num","store","city","province","region","excellent_num_total","good_num_total","unsatisfy_num_total")
    #print(sati)
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for sati_data in sati:
        if sati_data['city'] not in city:
            ex1.append(float(sati_data['excellent_num']))
            go1.append(float(sati_data['good_num']))
            un1.append(float(sati_data['unsatisfy_num']))
            ex_total.append(float(sati_data['excellent_num_total']))
            go_total.append(float(sati_data['good_num_total']))
            un_total.append(float(sati_data['unsatisfy_num_total']))
            city.append(sati_data['city'])
        elif sati_data['city'] in city:
            sa_index=city.index(sati_data['city'])
            ex1[sa_index]=ex1[sa_index]+float(sati_data['excellent_num'])
            go1[sa_index]=go1[sa_index]+float(sati_data['good_num'])
            un1[sa_index]=un1[sa_index]+float(sati_data['unsatisfy_num'])
            ex_total[sa_index]=ex_total[sa_index]+float(sati_data['excellent_num_total'])
            go_total[sa_index]=go_total[sa_index]+float(sati_data['good_num_total'])
            un_total[sa_index]=un_total[sa_index]+float(sati_data['unsatisfy_num_total'])
    for x in range(len(city)):
        city_index=city_name.index(city[x])
        SatisfactionData_day_city.objects.create(excellent_num=ex1[x],good_num=go1[x],unsatisfy_num=un1[x],excellent_num_total=ex_total[x],good_num_total=go_total[x],unsatisfy_num_total=un_total[x],add_time= time_stamp,time=day_time,city=city[x],region=region_name[city_index],province=province_name[city_index])
      
    excellent_add=[]
    good_add=[]
    unsatisfy_add=[]
    device_satisfy=[]
    store_name_add=[]
    city=[]
    ex1=[]
    go1=[]
    un1=[]
    ex_total=[]
    go_total=[]
    un_total=[]
    province=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    sati=SatisfactionData_day_city.objects.filter(time__year=year,time__month=month,time__day=day).values("excellent_num","good_num","unsatisfy_num","city","province","region","excellent_num_total","good_num_total","unsatisfy_num_total")
    #print(sati)
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for sati_data in sati:
        if sati_data['province'] not in province:
            ex1.append(float(sati_data['excellent_num']))
            go1.append(float(sati_data['good_num']))
            un1.append(float(sati_data['unsatisfy_num']))
            ex_total.append(float(sati_data['excellent_num_total']))
            go_total.append(float(sati_data['good_num_total']))
            un_total.append(float(sati_data['unsatisfy_num_total']))
            province.append(sati_data['province'])
        elif sati_data['province'] in province:
            sa_index=province.index(sati_data['province'])
            ex1[sa_index]=ex1[sa_index]+float(sati_data['excellent_num'])
            go1[sa_index]=go1[sa_index]+float(sati_data['good_num'])
            un1[sa_index]=un1[sa_index]+float(sati_data['unsatisfy_num'])
            ex_total[sa_index]=ex_total[sa_index]+float(sati_data['excellent_num_total'])
            go_total[sa_index]=go_total[sa_index]+float(sati_data['good_num_total'])
            un_total[sa_index]=un_total[sa_index]+float(sati_data['unsatisfy_num_total'])
    for x in range(len(province)):
        province_index=province_name.index(province[x])
        SatisfactionData_day_province.objects.create(excellent_num=ex1[x],good_num=go1[x],unsatisfy_num=un1[x],excellent_num_total=ex_total[x],good_num_total=go_total[x],unsatisfy_num_total=un_total[x],add_time= time_stamp,time=day_time,region=region_name[province_index],province=province_name[province_index])
        
    excellent_add=[]
    good_add=[]
    unsatisfy_add=[]
    device_satisfy=[]
    store_name_add=[]
    ex1=[]
    go1=[]
    un1=[]
    ex_total=[]
    go_total=[]
    un_total=[]
    province=[]
    region=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    sati=SatisfactionData_day_province.objects.filter(time__year=year,time__month=month,time__day=day).values("excellent_num","good_num","unsatisfy_num","city","province","region","excellent_num_total","good_num_total","unsatisfy_num_total")
    #print(sati)
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for sati_data in sati:
        if sati_data['region'] not in region:
            ex1.append(float(sati_data['excellent_num']))
            go1.append(float(sati_data['good_num']))
            un1.append(float(sati_data['unsatisfy_num']))
            ex_total.append(float(sati_data['excellent_num_total']))
            go_total.append(float(sati_data['good_num_total']))
            un_total.append(float(sati_data['unsatisfy_num_total']))
            region.append(sati_data['region'])
        elif sati_data['region'] in region:
            sa_index=region.index(sati_data['region'])
            ex1[sa_index]=ex1[sa_index]+float(sati_data['excellent_num'])
            go1[sa_index]=go1[sa_index]+float(sati_data['good_num'])
            un1[sa_index]=un1[sa_index]+float(sati_data['unsatisfy_num'])
            ex_total[sa_index]=ex_total[sa_index]+float(sati_data['excellent_num_total'])
            go_total[sa_index]=go_total[sa_index]+float(sati_data['good_num_total'])
            un_total[sa_index]=un_total[sa_index]+float(sati_data['unsatisfy_num_total'])
    for x in range(len(region)):
        region_index=region_name.index(region[x])
        SatisfactionData_day_region.objects.create(excellent_num=ex1[x],good_num=go1[x],unsatisfy_num=un1[x],excellent_num_total=ex_total[x],good_num_total=go_total[x],unsatisfy_num_total=un_total[x],add_time= time_stamp,time=day_time,region=region_name[region_index])
        
    excellent_add=[]
    good_add=[]
    unsatisfy_add=[]
    device_satisfy=[]
    store_name_add=[]
    ex1=[]
    go1=[]
    un1=[]
    ex_total=[]
    go_total=[]
    un_total=[]
    region=[]
    
    
     #统计当天产品销售数据
    salepro_data=[]
    store_now=[]
    quantity_now=[]
    sum_now=[]
    classification=[]
    time_sale=[]
    store_day=[]
    quantity_day=[]
    sum_day=[]
    time_sale_day=[]
    total_num=[]
    total_sum=[]
    total_sum_pro=[]
    total_num_pro=[]
    total_num_di=[]
    total_sum_di=[]
    device=[]
    store_j=[]
    store_p=[]
    item_j=[]
    item_p=[]
    time_j=[]
    time_p=[]
    device_j=[]
    device_p=[]
    class_j="火机"
    class_p="配件"
    sum_p=[]
    sum_j=[]
    quantity_j=[]
    quantity_p=[]
    for x in range(len(store_name)):
        quantity_day.append(0)
        #price_day.append(0)
        sum_day.append(0)
        total_num.append(0)
        total_sum.append(0)
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=2019#now_time[0]
    month=2#now_time[1]
    day=1#str(int(now_time[2]))  
    '''
    #day_time=now().date() + timedelta(days=-1)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    salepro_data=SaleProduct.objects.filter(time__year=year,time__month=month,time__day=day).values("store","time","quantity","sum","classification","device_id").order_by("store") #按销售时间查询，不是按录入时间查询，排除延时录入被漏掉的可能性
    #print(salepro_data)
    for sale_data in salepro_data:   #字典遍历
        store_now.append(sale_data['store'])
        classification.append(sale_data['classification'])
        quantity_now.append(float(sale_data['quantity']))
        #price_now.append(float(sale_data['price']))
        sum_now.append(float(sale_data['sum']))
        device.append(sale_data['device_id'])
        #item.append(sale_data['item'])
        time_sale.append(sale_data['time'])

    

    
    for x in range(len(store_now)): 
        if classification[x] ==class_j:
            if store_now[x] not in store_j :
                store_j.append(store_now[x])
                quantity_j.append(float(quantity_now[x]))
                #price_j.append(price_now[x])
                sum_j.append(float(sum_now[x]))
                device_j.append(device[x])
                #item_j.append(item[x])
                time_j.append(time_sale[x])
            elif store_now[x] in store_j :
                index_storej=store_j.index(store_now[x])
                quantity_j[index_storej]=quantity_j[index_storej]+float(quantity_now[x])
                #price_j[index_storej]=price_j[index_storej]+float(price_now[x])
                sum_j[index_storej]=sum_j[index_storej]+float(sum_now[x])
                
        if classification[x] ==class_p:        
            if store_now[x] not in store_p :
                store_p.append(store_now[x])
                quantity_p.append(float(quantity_now[x]))
                #price_p.append(price_now[x])
                sum_p.append(float(sum_now[x]))
                device_p.append(device[x])
                #item_p.append(item[x])
                time_p.append(time_sale[x])
            elif store_now[x] in store_p :
                index_storep=store_p.index(store_now[x])
                quantity_p[index_storep]=quantity_p[index_storep]+float(quantity_now[x])
                #price_p[index_storep]=price_p[index_storep]+float(price_now[x])
                sum_p[index_storep]=sum_p[index_storep]+float(sum_now[x])
   
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    for x in range(len(store_j)):
        total_num_di_j=SaleProduct.objects.filter(store=store_j[x],classification=class_j).aggregate(nums1=Sum('quantity')) #截至当天的累计数据
        if total_num_di_j['nums1']==None:
            total_num_di_j['nums1']=0
        total_sum_di_j=SaleProduct.objects.filter(store=store_j[x],classification=class_j).aggregate(nums2=Sum('sum'))
        if total_sum_di_j['nums2']==None:
            total_sum_di_j['nums2']=0
        store_index=store_name.index(store_j[x])
        print("write1")
        SaleProduct_day.objects.create(store=str(store_j[x]),time=day_time,quantity_pro=quantity_j[x],price_pro=0,sum_pro=sum_j[x],item=0,classification=class_j,add_time= time_stamp,quantity_total_pro=total_num_di_j['nums1'],sum_total_pro=total_sum_di_j['nums2'],city=city_name[store_index],region=region_name[store_index],province=province_name[store_index],device_id=device[x])  #存入当天数据

    for x in range(len(store_p)):
        total_num_di_p=SaleProduct.objects.filter(store=store_p[x],classification=class_p).aggregate(nums1=Sum('quantity')) #截至当天的累计数据
        if total_num_di_p['nums1']==None:
            total_num_di_p['nums1']=0
        total_sum_di_p=SaleProduct.objects.filter(store=store_p[x],classification=class_p).aggregate(nums2=Sum('sum'))
        if total_sum_di_p['nums2']==None:
            total_sum_di_p['nums2']=0
        store_index=store_name.index(store_p[x])
        #print("write2")
        SaleProduct_day.objects.create(store=str(store_p[x]),time=day_time,quantity_pro=quantity_p[x],price_pro=0,sum_pro=sum_p[x],item=0,classification=class_p,add_time= time_stamp,quantity_total_pro=total_num_di_p['nums1'],sum_total_pro=total_sum_di_p['nums2'],city=city_name[store_index],region=region_name[store_index],province=province_name[store_index],device_id=device[x])  #存入当天数据
    
   
    
    
    salepro_data=[]
    store_now=[]
    quantity_now=[]
    sum_now=[]
    classification=[]
    time_sale=[]
    store_day=[]
    quantity_day=[]
    sum_day=[]
    time_sale_day=[]
    total_num=[]
    total_sum=[]
    total_sum_pro=[]
    total_num_pro=[]
    total_num_di=[]
    total_sum_di=[]
    device=[]
    store_j=[]
    store_p=[]
    item_j=[]
    item_p=[]
    time_j=[]
    time_p=[]
    device_j=[]
    device_p=[]
    class_j="火机"
    class_p="配件"
    sum_p=[]
    sum_j=[]
    city=[]
    quantity_j=[]
    quantity_p=[]
    city_day=[]
    region=[]
    province_day=[]
    quantity_pro=[]
    sum_pro=[]
    cityname=[]
    quantity_pro=[]
    price_pro=[]
    sum_pro=[]
    quantity_total_pro=[]
    sum_total_pro=[]
    quantity_total_proj=[]
    sum_total_proj=[]
    quantity_total_prop=[]
    sum_total_prop=[]
    classification_city=[]
    item_city=[]
    cityj=[]
    cityp=[]
    province=[]
    region=[]
    classificationj=[]
    classificationp=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    salestore_data=SaleProduct_day.objects.filter(time__year=year,time__month=month,time__day=day).values("store","time","quantity_pro","price_pro","sum_pro","quantity_total_pro","sum_total_pro","city","region","province","classification") 

    
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    
    for sale_data_day in salestore_data:
        
        if sale_data_day['classification']==class_j:
            if sale_data_day['city'] not in cityj:
                cityj.append(sale_data_day['city'])
                classificationj.append(sale_data_day['classification'])
                quantity_j.append(float(sale_data_day['quantity_pro']))
                sum_j.append(float(sale_data_day['sum_pro']))
                sum_total_proj.append(float(sale_data_day['sum_total_pro']))
                quantity_total_proj.append(float(sale_data_day['quantity_total_pro']))
            elif sale_data_day['city'] in cityj:
                index=cityj.index(sale_data_day['city'])
                quantity_j[index]=quantity_j[index]+float(sale_data_day['quantity_pro'])
                sum_j[index]=sum_j[index]+float(sale_data_day['sum_pro'])
                sum_total_proj[index]=sum_total_proj[index]+float(sale_data_day['sum_total_pro'])
                quantity_total_proj[index]=quantity_total_proj[index]+float(sale_data_day['quantity_total_pro'])
            
        elif sale_data_day['classification']==class_p:    
            if sale_data_day['city'] not in cityp:
                cityp.append(sale_data_day['city'])
                classificationp.append(sale_data_day['classification'])
                quantity_p.append(float(sale_data_day['quantity_pro']))
                sum_p.append(float(sale_data_day['sum_pro']))
                sum_total_prop.append(float(sale_data_day['sum_total_pro']))
                quantity_total_prop.append(float(sale_data_day['quantity_total_pro']))
        
            elif sale_data_day['city'] in cityp:
                index=cityp.index(sale_data_day['city'])
                quantity_p[index]=quantity_p[index]+float(sale_data_day['quantity_pro'])
                sum_p[index]=sum_p[index]+float(sale_data_day['sum_pro'])
                sum_total_prop[index]=sum_total_prop[index]+float(sale_data_day['sum_total_pro'])
                quantity_total_prop[index]=quantity_total_prop[index]+float(sale_data_day['quantity_total_pro'])    
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for x in range(len(cityj)):
        index=city_name.index(cityj[x])
        province=province_name[index]
        region=region_name[index]
        SaleProduct_day_city.objects.create(time=day_time,quantity_pro=str(quantity_j[x]),price_pro=0,sum_pro=str(sum_j[x]),add_time= time_stamp,quantity_total_pro=str(quantity_total_proj[x]),sum_total_pro=str(sum_total_proj[x]) ,city=cityj[x],region=region,province=province,item=0,classification=class_j)  #存入当天数据
        
        
    for x in range(len(cityp)):
        index=city_name.index(cityp[x])
        province=province_name[index]
        region=region_name[index]    
        SaleProduct_day_city.objects.create(time=day_time,quantity_pro=str(quantity_p[x]),price_pro=0,sum_pro=str(sum_p[x]),add_time= time_stamp,quantity_total_pro=str(quantity_total_prop[x]),sum_total_pro=str(sum_total_prop[x]) ,city=cityp[x],region=region,province=province,item=0,classification=class_p)  #存入当天数据
    print("end5")
    
    
    salepro_data=[]
    store_now=[]
    quantity_now=[]
    sum_now=[]
    classification=[]
    time_sale=[]
    store_day=[]
    quantity_day=[]
    sum_day=[]
    time_sale_day=[]
    total_num=[]
    total_sum=[]
    total_sum_pro=[]
    total_num_pro=[]
    total_num_di=[]
    total_sum_di=[]
    device=[]
    store_j=[]
    store_p=[]
    item_j=[]
    item_p=[]
    time_j=[]
    time_p=[]
    device_j=[]
    device_p=[]
    class_j="火机"
    class_p="配件"
    sum_p=[]
    sum_j=[]
    quantity_j=[]
    quantity_p=[]
    city_day=[]
    region=[]
    province_day=[]
    quantity_pro=[]
    sum_pro=[]
    cityname=[]
    quantity_pro=[]
    price_pro=[]
    sum_pro=[]
    quantity_total_pro=[]
    sum_total_pro=[]
    quantity_total_proj=[]
    sum_total_proj=[]
    quantity_total_prop=[]
    sum_total_prop=[]
    classification_city=[]
    item_city=[]
    cityj=[]
    cityp=[]
    province=[]
    region=[]
    classificationj=[]
    classificationp=[]
    provincej=[]
    provincep=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    salestore_data=SaleProduct_day_city.objects.filter(time__year=year,time__month=month,time__day=day).values("time","quantity_pro","price_pro","sum_pro","quantity_total_pro","sum_total_pro","city","region","province","classification") 

    
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    
    for sale_data_day in salestore_data:
        
        if sale_data_day['classification']==class_j:
            if sale_data_day['province'] not in provincej:
                provincej.append(sale_data_day['province'])
                classificationj.append(sale_data_day['classification'])
                quantity_j.append(float(sale_data_day['quantity_pro']))
                sum_j.append(float(sale_data_day['sum_pro']))
                sum_total_proj.append(float(sale_data_day['sum_total_pro']))
                quantity_total_proj.append(float(sale_data_day['quantity_total_pro']))
            elif sale_data_day['province'] in provincej:
                index=provincej.index(sale_data_day['province'])
                quantity_j[index]=quantity_j[index]+float(sale_data_day['quantity_pro'])
                sum_j[index]=sum_j[index]+float(sale_data_day['sum_pro'])
                sum_total_proj[index]=sum_total_proj[index]+float(sale_data_day['sum_total_pro'])
                quantity_total_proj[index]=quantity_total_proj[index]+float(sale_data_day['quantity_total_pro'])
            
        elif sale_data_day['classification']==class_p:    
            if sale_data_day['province'] not in provincep:
                provincep.append(sale_data_day['province'])
                classificationp.append(sale_data_day['classification'])
                quantity_p.append(float(sale_data_day['quantity_pro']))
                sum_p.append(float(sale_data_day['sum_pro']))
                sum_total_prop.append(float(sale_data_day['sum_total_pro']))
                quantity_total_prop.append(float(sale_data_day['quantity_total_pro']))
        
            elif sale_data_day['province'] in provincep:
                index=provincep.index(sale_data_day['province'])
                quantity_p[index]=quantity_p[index]+float(sale_data_day['quantity_pro'])
                sum_p[index]=sum_p[index]+float(sale_data_day['sum_pro'])
                sum_total_prop[index]=sum_total_prop[index]+float(sale_data_day['sum_total_pro'])
                quantity_total_prop[index]=quantity_total_prop[index]+float(sale_data_day['quantity_total_pro'])    
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for x in range(len(provincej)):
        index=province_name.index(provincej[x])
        region=region_name[index]
        SaleProduct_day_province.objects.create(time=day_time,quantity_pro=str(quantity_j[x]),price_pro=0,sum_pro=str(sum_j[x]),add_time= time_stamp,quantity_total_pro=str(quantity_total_proj[x]),sum_total_pro=str(sum_total_proj[x]) ,region=region,province=provincej[x],item=0,classification=class_j)  #存入当天数据
        
        
    for x in range(len(provincep)):
        index=province_name.index(provincep[x])
        region=region_name[index]    
        SaleProduct_day_province.objects.create(time=day_time,quantity_pro=str(quantity_p[x]),price_pro=0,sum_pro=str(sum_p[x]),add_time= time_stamp,quantity_total_pro=str(quantity_total_prop[x]),sum_total_pro=str(sum_total_prop[x]) ,region=region,province=provincep[x],item=0,classification=class_p)  #存入当天数据
    #print("end5")
    salepro_data=[]
    store_now=[]
    quantity_now=[]
    sum_now=[]
    classification=[]
    time_sale=[]
    store_day=[]
    quantity_day=[]
    sum_day=[]
    time_sale_day=[]
    total_num=[]
    total_sum=[]
    total_sum_pro=[]
    total_num_pro=[]
    total_num_di=[]
    total_sum_di=[]
    device=[]
    store_j=[]
    store_p=[]
    item_j=[]
    item_p=[]
    time_j=[]
    time_p=[]
    device_j=[]
    device_p=[]
    class_j="火机"
    class_p="配件"
    sum_p=[]
    sum_j=[]
    quantity_j=[]
    quantity_p=[]
    city_day=[]
    region=[]
    province_day=[]
    quantity_pro=[]
    sum_pro=[]
    cityname=[]
    quantity_pro=[]
    price_pro=[]
    sum_pro=[]
    quantity_total_pro=[]
    sum_total_pro=[]
    quantity_total_proj=[]
    sum_total_proj=[]
    quantity_total_prop=[]
    sum_total_prop=[]
    classification_city=[]
    item_city=[]
    cityj=[]
    cityp=[]
    province=[]
    region=[]
    classificationj=[]
    classificationp=[]
    provincej=[]
    provincep=[]
    regionj=[]
    regionp=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    salestore_data=SaleProduct_day_province.objects.filter(time__year=year,time__month=month,time__day=day).values("time","quantity_pro","price_pro","sum_pro","quantity_total_pro","sum_total_pro","region","province","classification") 

    
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    
    for sale_data_day in salestore_data:
        
        if sale_data_day['classification']==class_j:
            if sale_data_day['region'] not in regionj:
                regionj.append(sale_data_day['region'])
                classificationj.append(sale_data_day['classification'])
                quantity_j.append(float(sale_data_day['quantity_pro']))
                sum_j.append(float(sale_data_day['sum_pro']))
                sum_total_proj.append(float(sale_data_day['sum_total_pro']))
                quantity_total_proj.append(float(sale_data_day['quantity_total_pro']))
            elif sale_data_day['region'] in regionj:
                index=regionj.index(sale_data_day['region'])
                quantity_j[index]=quantity_j[index]+float(sale_data_day['quantity_pro'])
                sum_j[index]=sum_j[index]+float(sale_data_day['sum_pro'])
                sum_total_proj[index]=sum_total_proj[index]+float(sale_data_day['sum_total_pro'])
                quantity_total_proj[index]=quantity_total_proj[index]+float(sale_data_day['quantity_total_pro'])
            
        elif sale_data_day['classification']==class_p:    
            if sale_data_day['region'] not in regionp:
                regionp.append(sale_data_day['region'])
                classificationp.append(sale_data_day['classification'])
                quantity_p.append(float(sale_data_day['quantity_pro']))
                sum_p.append(float(sale_data_day['sum_pro']))
                sum_total_prop.append(float(sale_data_day['sum_total_pro']))
                quantity_total_prop.append(float(sale_data_day['quantity_total_pro']))
        
            elif sale_data_day['region'] in regionp:
                index=regionp.index(sale_data_day['region'])
                quantity_p[index]=quantity_p[index]+float(sale_data_day['quantity_pro'])
                sum_p[index]=sum_p[index]+float(sale_data_day['sum_pro'])
                sum_total_prop[index]=sum_total_prop[index]+float(sale_data_day['sum_total_pro'])
                quantity_total_prop[index]=quantity_total_prop[index]+float(sale_data_day['quantity_total_pro'])    
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for x in range(len(regionj)):
        SaleProduct_day_region.objects.create(time=day_time,quantity_pro=str(quantity_j[x]),price_pro=0,sum_pro=str(sum_j[x]),add_time= time_stamp,quantity_total_pro=str(quantity_total_proj[x]),sum_total_pro=str(sum_total_proj[x]) ,region=regionj[x],item=0,classification=class_j)  #存入当天数据
        
        
    for x in range(len(regionp)):
        SaleProduct_day_region.objects.create(time=day_time,quantity_pro=str(quantity_p[x]),price_pro=0,sum_pro=str(sum_p[x]),add_time= time_stamp,quantity_total_pro=str(quantity_total_prop[x]),sum_total_pro=str(sum_total_prop[x]) ,region=regionp[x],item=0,classification=class_p)  #存入当天数据
    #print("end5")
    salepro_data=[]
    store_now=[]
    quantity_now=[]
    sum_now=[]
    classification=[]
    time_sale=[]
    store_day=[]
    quantity_day=[]
    sum_day=[]
    time_sale_day=[]
    total_num=[]
    total_sum=[]
    total_sum_pro=[]
    total_num_pro=[]
    total_num_di=[]
    total_sum_di=[]
    device=[]
    store_j=[]
    store_p=[]
    item_j=[]
    item_p=[]
    time_j=[]
    time_p=[]
    device_j=[]
    device_p=[]
    class_j="火机"
    class_p="配件"
    sum_p=[]
    sum_j=[]
    quantity_j=[]
    quantity_p=[]
    city_day=[]
    region=[]
    province_day=[]
    quantity_pro=[]
    sum_pro=[]
    cityname=[]
    quantity_pro=[]
    price_pro=[]
    sum_pro=[]
    quantity_total_pro=[]
    sum_total_pro=[]
    quantity_total_proj=[]
    sum_total_proj=[]
    quantity_total_prop=[]
    sum_total_prop=[]
    classification_city=[]
    item_city=[]
    cityj=[]
    cityp=[]
    province=[]
    region=[]
    classificationj=[]
    classificationp=[]
    provincej=[]
    provincep=[]
    regionj=[]
    regionp=[]
    
    salepro_data=[]
    store_now=[]
    quantity_now=[]
    sum_now=[]
    classification=[]
    time_sale=[]
    store_day=[]
    quantity_day=[]
    sum_day=[]
    time_sale_day=[]
    total_num=[]
    total_sum=[]
    total_sum_pro=[]
    total_num_pro=[]
    total_num_di=[]
    total_sum_di=[]
    device=[]
    store_j=[]
    store_p=[]
    item_j=[]
    item_p=[]
    time_j=[]
    time_p=[]
    device_j=[]
    device_p=[]
    class_j="火机"
    class_p="配件"
    sum_p=[]
    sum_j=[]
    quantity_j=[]
    quantity_p=[]
    city_day=[]
    region=[]
    province_day=[]
    quantity_pro=[]
    sum_pro=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    salestore_data_store=SaleProduct_day.objects.filter(time__year=year,time__month=month,time__day=day).values("quantity_pro","price_pro","sum_pro","quantity_total_pro","sum_total_pro","store","city","region","province","item","device_id") 
    #print(salestore_data_store)
    
    for sale_data_sum in salestore_data_store:

        if sale_data_sum['store'] not in store_day:
            store_day.append(sale_data_sum['store'])
            city_day.append(sale_data_sum['city'])
            province_day.append(sale_data_sum['province'])
            region.append(sale_data_sum['region'])
            quantity_pro.append(float(sale_data_sum['quantity_pro']))
            sum_pro.append(float(sale_data_sum['sum_pro']))
            total_num_di.append(float(sale_data_sum['quantity_total_pro']))
            total_sum_di.append(float(sale_data_sum['sum_total_pro']))
            device.append(sale_data_sum['device_id'])
        elif sale_data_sum['store'] in store_day:
            index_store=store_day.index(sale_data_sum['store'])
            quantity_pro[index_store]=quantity_pro[index_store]+float(sale_data_sum['quantity_pro'])
            sum_pro[index_store]=sum_pro[index_store]+float(sale_data_sum['sum_pro'])
            total_num_di[index_store]=total_num_di[index_store]+float(sale_data_sum['quantity_total_pro'])
            total_sum_di[index_store]=total_sum_di[index_store]+float(sale_data_sum['sum_total_pro'])
    #print(store_day)
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for x in range(len(store_day)):
        Sum_day_store.objects.create(time=day_time,quantity_pro=quantity_pro[x],price_pro=0,sum_pro=sum_pro[x],add_time= time_stamp,quantity_total_pro=total_num_di[x],sum_total_pro= round(total_sum_di[x],2),store=store_day[x],city=city_day[x],region=region[x],province=province_day[x],device_id=device[x])  #存入当天数据
    #print("end4")
    salepro_data=[]
    store_now=[]
    quantity_now=[]
    sum_now=[]
    classification=[]
    time_sale=[]
    store_day=[]
    quantity_day=[]
    sum_day=[]
    time_sale_day=[]
    total_num=[]
    total_sum=[]
    total_sum_pro=[]
    total_num_pro=[]
    total_num_di=[]
    total_sum_di=[]
    device=[]
    store_j=[]
    store_p=[]
    item_j=[]
    item_p=[]
    time_j=[]
    time_p=[]
    device_j=[]
    device_p=[]
    class_j="火机"
    class_p="配件"
    sum_p=[]
    sum_j=[]
    quantity_j=[]
    quantity_p=[]
    city_day=[]
    region=[]
    province_day=[]
    quantity_pro=[]
    sum_pro=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    salestore_data_city=SaleProduct_day_city.objects.filter(time__year=year,time__month=month,time__day=day).values("quantity_pro","price_pro","sum_pro","quantity_total_pro","sum_total_pro","store","city","region","province","item","device_id") 
    #print(salestore_data_city)
    
    for sale_data_sum in salestore_data_city:

        if sale_data_sum['city'] not in city_day:
            city_day.append(sale_data_sum['city'])
            province_day.append(sale_data_sum['province'])
            region.append(sale_data_sum['region'])
            quantity_pro.append(float(sale_data_sum['quantity_pro']))
            sum_pro.append(float(sale_data_sum['sum_pro']))
            total_num_di.append(float(sale_data_sum['quantity_total_pro']))
            total_sum_di.append(float(sale_data_sum['sum_total_pro']))

        elif sale_data_sum['city'] in city_day:
            index_city=city_day.index(sale_data_sum['city'])
            quantity_pro[index_city]=quantity_pro[index_city]+float(sale_data_sum['quantity_pro'])
            sum_pro[index_city]=sum_pro[index_city]+float(sale_data_sum['sum_pro'])
            total_num_di[index_city]=total_num_di[index_city]+float(sale_data_sum['quantity_total_pro'])
            total_sum_di[index_city]=total_sum_di[index_city]+float(sale_data_sum['sum_total_pro'])
    #print(city_day)
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for x in range(len(city_day)):
        Sum_day_city.objects.create(time=day_time,quantity_pro=quantity_pro[x],price_pro=0,sum_pro=sum_pro[x],add_time= time_stamp,quantity_total_pro=total_num_di[x],sum_total_pro= round(total_sum_di[x],2),city=city_day[x],region=region[x],province=province_day[x])  #存入当天数据
    #print("end4")
    salepro_data=[]
    store_now=[]
    quantity_now=[]
    sum_now=[]
    classification=[]
    time_sale=[]
    store_day=[]
    quantity_day=[]
    sum_day=[]
    time_sale_day=[]
    total_num=[]
    total_sum=[]
    total_sum_pro=[]
    total_num_pro=[]
    total_num_di=[]
    total_sum_di=[]
    device=[]
    store_j=[]
    store_p=[]
    item_j=[]
    item_p=[]
    time_j=[]
    time_p=[]
    device_j=[]
    device_p=[]
    class_j="火机"
    class_p="配件"
    sum_p=[]
    sum_j=[]
    quantity_j=[]
    quantity_p=[]
    city_day=[]
    region=[]
    province_day=[]
    quantity_pro=[]
    sum_pro=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    salestore_data_province=SaleProduct_day_province.objects.filter(time__year=year,time__month=month,time__day=day).values("quantity_pro","price_pro","sum_pro","quantity_total_pro","sum_total_pro","store","city","region","province","item","device_id") 
    #print(salestore_data_province)
    
    for sale_data_sum in salestore_data_province:

        if sale_data_sum['province'] not in province_day:
            province_day.append(sale_data_sum['province'])
            region.append(sale_data_sum['region'])
            quantity_pro.append(float(sale_data_sum['quantity_pro']))
            sum_pro.append(float(sale_data_sum['sum_pro']))
            total_num_di.append(float(sale_data_sum['quantity_total_pro']))
            total_sum_di.append(float(sale_data_sum['sum_total_pro']))

        elif sale_data_sum['province'] in province_day:
            index_province=province_day.index(sale_data_sum['province'])
            quantity_pro[index_province]=quantity_pro[index_province]+float(sale_data_sum['quantity_pro'])
            sum_pro[index_province]=sum_pro[index_province]+float(sale_data_sum['sum_pro'])
            total_num_di[index_province]=total_num_di[index_province]+float(sale_data_sum['quantity_total_pro'])
            total_sum_di[index_province]=total_sum_di[index_province]+float(sale_data_sum['sum_total_pro'])
    #print(province_day)
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for x in range(len(province_day)):
        Sum_day_province.objects.create(time=day_time,quantity_pro=quantity_pro[x],price_pro=0,sum_pro=sum_pro[x],add_time= time_stamp,quantity_total_pro=total_num_di[x],sum_total_pro= round(total_sum_di[x],2),region=region[x],province=province_day[x])  #存入当天数据
    #print("end4")
    salepro_data=[]
    store_now=[]
    quantity_now=[]
    sum_now=[]
    classification=[]
    time_sale=[]
    store_day=[]
    quantity_day=[]
    sum_day=[]
    time_sale_day=[]
    total_num=[]
    total_sum=[]
    total_sum_pro=[]
    total_num_pro=[]
    total_num_di=[]
    total_sum_di=[]
    device=[]
    store_j=[]
    store_p=[]
    item_j=[]
    item_p=[]
    time_j=[]
    time_p=[]
    device_j=[]
    device_p=[]
    class_j="火机"
    class_p="配件"
    sum_p=[]
    sum_j=[]
    quantity_j=[]
    quantity_p=[]
    city_day=[]
    region=[]
    province_day=[]
    quantity_pro=[]
    sum_pro=[]
    '''
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    '''
    salestore_data_region=SaleProduct_day_region.objects.filter(time__year=year,time__month=month,time__day=day).values("quantity_pro","price_pro","sum_pro","quantity_total_pro","sum_total_pro","store","city","region","province","item","device_id") 
    #print(salestore_data_region)
    
    for sale_data_sum in salestore_data_region:

        if sale_data_sum['region'] not in region:
            region.append(sale_data_sum['region'])
            quantity_pro.append(float(sale_data_sum['quantity_pro']))
            sum_pro.append(float(sale_data_sum['sum_pro']))
            total_num_di.append(float(sale_data_sum['quantity_total_pro']))
            total_sum_di.append(float(sale_data_sum['sum_total_pro']))

        elif sale_data_sum['region'] in region:
            index_region=region.index(sale_data_sum['region'])
            quantity_pro[index_region]=quantity_pro[index_region]+float(sale_data_sum['quantity_pro'])
            sum_pro[index_region]=sum_pro[index_region]+float(sale_data_sum['sum_pro'])
            total_num_di[index_region]=total_num_di[index_region]+float(sale_data_sum['quantity_total_pro'])
            total_sum_di[index_region]=total_sum_di[index_region]+float(sale_data_sum['sum_total_pro'])
    #print(region)
    day_time=now().date() + timedelta(days=-1)#-4)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for x in range(len(region)):
        Sum_day_region.objects.create(time=day_time,quantity_pro=quantity_pro[x],price_pro=0,sum_pro=sum_pro[x],add_time= time_stamp,quantity_total_pro=total_num_di[x],sum_total_pro= round(total_sum_di[x],2),region=region[x])  #存入当天数据
    print("end4")
    #DetailInfo.objects.all().delete()
    #MasterInfo1.objects.all().delete() 	
    salepro_data=[]
    store_now=[]
    quantity_now=[]
    sum_now=[]
    classification=[]
    time_sale=[]
    store_day=[]
    quantity_day=[]
    sum_day=[]
    time_sale_day=[]
    total_num=[]
    total_sum=[]
    total_sum_pro=[]
    total_num_pro=[]
    total_num_di=[]
    total_sum_di=[]
    device=[]
    store_j=[]
    store_p=[]
    item_j=[]
    item_p=[]
    time_j=[]
    time_p=[]
    device_j=[]
    device_p=[]
    class_j="火机"
    class_p="配件"
    sum_p=[]
    sum_j=[]
    quantity_j=[]
    quantity_p=[]
    city_day=[]
    region=[]
    province_day=[]
    quantity_pro=[]
    sum_pro=[]