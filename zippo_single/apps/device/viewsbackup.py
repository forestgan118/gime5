# coding:utf-8
import json
import os
import time
from datetime import date,datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from json import dumps
from django.shortcuts import render,redirect
from django.views.generic import View
from django.db.models import Q
from organization.models import RegionDict,CityDict, Store, SaleProduct_day, SaleAccessory_day,SaleProduct,SaleAccessory,SaleProduct_day_city,SaleProduct_day_region
from .models import wifiprobeData,wifiprobeData_day,wifiprobeData_week,wifiprobeData_month,wifiprobeData_quarter,wifiprobeData_year,SatisfactionData,SatisfactionData_day,SatisfactionData_week,SatisfactionData_month,SatisfactionData_quarter,SatisfactionData_year,DeviceStatus
from macdata.models import DetailInfo, MasterInfo
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
        return render(request, "devicestatus.html",{"all_region":all_region,"status":status})
    def post(self, request):
        # 查找到所有的机构
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        #all_province= ProvinceDict.objects.all()
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
        city_id=request.POST.get('city',"")
        store_id=request.POST.get('store',"")
        if region_id=="":
            return HttpResponse("请重新选择区域")
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
            if "全部" not in city_id:
                if "全部" not in store_id:
                    status = device.filter(store=str(store_id),time__range=(date_from, date_to)).values('online_status','add_time','store','city','region')
                elif "全部" in store_id:
                    status = device.filter(city=str(city_id),time__range=(date_from, date_to)).values('online_status','add_time','store','city','region')
            elif "全部" in city_id:
                status = device.filter(region=str(region_id),time__range=(date_from, date_to)).values('online_status','add_time','store','city','region')
        print (status)
        return render(request, "devicestatus.html",{"status":status,"all_region":all_region})
'''
class StatusAuthView(View):
    #login_url = '/login/'
    #redirect_field_name = 'next'
    def get(self, request,param1,param2,param3):
        num1=param1
        num2=param2
        num3=param3
        update_list=""
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
            store_id = all_store.filter(id=num3).values("name","device_id")
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
            status=DeviceStatus.objects.filter(device_id=store_id.values('device_id')).values('online_status','time')
        elif city_id!=0 and store_id==0:
            data_list=Store.objects.filter(cityname=city_id.values('name')).values('name','cityname','regionname')
            status=DeviceStatus.objects.filter(device_id=store_id.values('device_id')).values('online_status','time')
            print (data_list)
        elif city_id==0 and store_id==0:
            data_list=Store.objects.filter(regionname=region_id.values('name')).values('name','cityname','regionname')

        return render(request, "devicestatus.html",
                    {"data_list":data_list,
                    "all_region":all_region,
                    })
    def toDicts(objs):
            obj_arr=[]
            for o in objs:
                    obj_arr.append(o.toDict())
            return obj_arr
'''
class SoftwareView(View):
    #login_url = '/login/'
    #redirect_field_name = 'next'
    def get(self, request):
        all_region = RegionDict.objects.all()
        data_list=[]
        return render(request, "software.html",{"all_region":all_region,"data_list":data_list})
    #store = forms.CharField()
    def post(self, request):
        # 查找到所有的机构
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        #all_province= ProvinceDict.objects.all()
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
        city_id=request.POST.get('city',"")
        store_id=request.POST.get('store',"")
        if region_id=="":
            return HttpResponse("请重新选择区域")
        if city_id=="":
            return HttpResponse("请重新选择城市")
        if store_id=="":
            return HttpResponse("请重新选择门店")
        #update=[]
        #update = request.POST.getlist('inlineRadio')
        print (region_id,city_id,store_id)
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
        except Exception as e:
            print (e)
            updatecmd="failure"
        
        
        
        #update=check_box_list.split(',')
        #print('update=',update)
        if "全部" not in city_id:
            #region_select = all_region.filter(name=str(region_id)).values('id')
            #city_select = all_city.filter(name=str(city_id)).values('id')
            #for data in region_select:
            #    region=data['id']
            #for data in city_select:
            #    city=data['id']
            if "全部" not in store_id:
                device_id = all_store.filter(name=str(store_id)).values('device_id')
                #for data in store_select:
                #    device_id=data['device_id']
                    
            elif "全部" in store_id:
                device_id = all_city.filter(name=str(city_id)).values('device_id')
                #store=0
        elif "全部" in city_id:
            #region_select = all_region.filter(name=str(region_id)).values('id')
            device_id = all_region.filter(name=str(region_id)).values('device_id')
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
        #print (update)
        return render(request, "software.html",
                    {"data_list":data_list,
                     #"updata_list":update,
                     "all_region":all_region,
                     "device_id":json.dumps(deviceid),
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
        return render(request, "resource.html",{"all_region":all_region,"data_list":data_list})
    #store = forms.CharField()
    def post(self, request):
        # 查找到所有的机构
        all_region = RegionDict.objects.all()
        # 查找到所有的省
        #all_province= ProvinceDict.objects.all()
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
        city_id=request.POST.get('city',"")
        store_id=request.POST.get('store',"")
        if region_id=="":
            return HttpResponse("请重新选择区域")
        if city_id=="":
            return HttpResponse("请重新选择城市")
        if store_id=="":
            return HttpResponse("请重新选择门店")
        #update=[]
        update = request.POST.getlist('inlineRadio')
        print (region_id,city_id,store_id,update)
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
        except Exception as e:
            print (e)
            updatecmd="failure"
        
        
        
        #update=check_box_list.split(',')
        #print('update=',update)
        if "全部" not in city_id:
            #region_select = all_region.filter(name=str(region_id)).values('id')
            #city_select = all_city.filter(name=str(city_id)).values('id')
            #for data in region_select:
            #    region=data['id']
            #for data in city_select:
            #    city=data['id']
            if "全部" not in store_id:
                device_id = all_store.filter(name=str(store_id)).values('device_id')
                #for data in store_select:
                #    device_id=data['device_id']
                    
            elif "全部" in store_id:
                device_id = all_city.filter(name=str(city_id)).values('device_id')
                #store=0
        elif "全部" in city_id:
            #region_select = all_region.filter(name=str(region_id)).values('id')
            device_id = all_region.filter(name=str(region_id)).values('device_id')
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
        print (update)
        return render(request, "resource.html",
                    {"data_list":data_list,
                     "updata_list":update,
                     "all_region":all_region,
                     "device_id":json.dumps(deviceid),
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
    now_time =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now_time[0]
    month=now_time[1]
    day=str(int(now_time[2]))
    duration=[]
    duration5=[]
    data=[]
    mac=[]
    mid=[]
    u_dict=[]
    distance=[]
    u_list=[]
    maclist1=[]
    maclist5=[]
    mid_list=[]
    data_list=[]
    u_time=[]
    u_time5=[]
    u_distance=[]
    u_distance5=[]
    mac_list1=[]
    mac_list5=[]
    mac_index=0
    mac_str=""
    wifi_id=[]
    wifi_id5=[]
    id=[]
    n1=0
    n5=0
    n=[]
    n5=[]
    c_time=[]
    store_name=[]
    device_id_add=[]
    wifi_id_add=[]
    store_add=[]
    city_id=[]
    city=[]
    city_name=[]
    region_id=[]
    region=[]
    region_dict_name=[]
    region_name=[]
    store_city_id=[]
    city_device=CityDict.objects.values("id","name","region_id")
    
    for city_data in city_device:
        city_id.append(city_data['id'])
        city.append(city_data['name'])
        region_id.append(city_data['region_id'])
    region_device=RegionDict.objects.values("id","name")
    for region_data in region_device:
        region.append(region_data['id'])
        region_dict_name.append(region_data['name'])
    store_device=Store.objects.values("name","device_id","wifi_id","city_id")
    for store_add in store_device:
        if store_add['wifi_id'] != "":
            store_name.append(store_add['name'])
            device_id_add.append(store_add['device_id'])
            wifi_id_add.append(store_add['wifi_id'])
            store_city_id.append(store_add['city_id'])
            city_index=city_id.index(store_add['city_id'])   #获取city 的index
            city_name.append(city[city_index])   #将city name加入list
            region_id_select=region_id[city_index]  #根据所选的city确定citydcit的region_id
            region_index=region.index(region_id_select)  #根据所选的citydict中的region_id
            region_name.append(region_dict_name[region_index])   #确定regiondcit中的name
    #start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
    print (store_name,city_name,region_name)
    master=MasterInfo.objects.values()
    for x in master:
        mid.append(x['mid'])
    
    detail_data=DetailInfo.objects.filter(utime__year=year,utime__month=month,utime__day=day).values("mac","range","mid","utime").order_by('utime')
    #获取当天"mac","range","mid","utime"，按时间倒序排列，输出为字典格式
    #detail_data1=detail_data.values("mac","range","mid","utime").order_by("mid")
    #print (detail_data.values())
    #for data1 in detail_data:   #字典遍历
    #    u_dict=list(data1.values())    
        #if u_dict[3]==str("'"+mid[0]+"'"):
    #    print (u_dict)
    
    
    for data in detail_data:   #字典遍历
        mac.append(data['mac'])
        distance.append(data['range'])
        id.append(data['mid'])
        c_time.append(data['utime'])
    #print (id)
    for i in range(0,len(mid)):
        data_list.append([])
        
        for j in range(0,len(mac)):
            data_list[i].append(" ")
            #duration.append(0)
    #print (data_list)
    #print(c_time)
    #for y in range(num):
    #    print (mac[y])
    #    print(mac)
    for i in range(0,len(mac)):
        if float(distance[i]) <=3:
            mid_index=mid.index(id[i])
            mac_str=mac[i][:-3]
            if mac_str  not in maclist1:
                maclist1.append(mac_str)  #探测范围3m内的mac列表
                u_time.append(c_time[i])   #探测范围3m内MAC的采集时间
                u_distance.append(distance[i])  #探测范围3m内MAC的距离
                duration.append(0)   #探测范围3m内MAC的停留时间

            elif mac_str in maclist1:
                mac_index=maclist1.index(mac_str)
                duration[mac_index]=(c_time[i]-u_time[mac_index]).total_seconds()#3m内计算停留时间
                u_time[mac_index]=c_time[i]
                if float(duration[mac_index]) <70 :
                    if mac_str  not in mac_list1:
                        mac_list1.append(mac_str)  #3m内超过计时单位的mac
                        wifi_id.append(id[i])  #3m内超过计时单位的mid
                        n.append(0)  #3m内超过计时单位的列表
                        
                    elif mac_str  in mac_list1:
                        mac_index2=mac_list1.index(mac_str)
                        n[mac_index2]=n[mac_index2]+1  #3m内超过计时单位的列表累加
                 
                elif float(duration[mac_index]) >=70:
                    if mac_str  in mac_list1:
                        index_mac_str=mac_list1.index(mac_str)
                        del(mac_list1[index_mac_str])
                        del(wifi_id[index_mac_str])
                        del(n[index_mac_str])
                
        elif float(distance[i]) >3  : 
            mid_index=mid.index(id[i])
            mac_str=mac[i][:-3]
            if mac_str in maclist1:   
                mac_index1=maclist1.index(mac_str)
                del(maclist1[mac_index1])  #超出探测距离3m后删除该mac
                del(u_time[mac_index1])   #超出探测距离3m后删除该mac的采集时间
                del(duration[mac_index1])  #超出探测距离3m后删除该mac的停留时间 
                del(u_distance[mac_index1])  #超出探测距离3m后删除该mac的距离
            if mac_str in mac_list1:
                mac_index=mac_list1.index(mac_str)
                del(n[mac_index])   #超出探测距离3m后删除该mac的计时单位
                del(mac_list1[mac_index])  #超出探测距离3m后删除达到停留时间的mac 
                del(wifi_id[mac_index])   #超出探测距离3m后删除达到停留时间的mid
                
        if (float(distance[i]) <=5 and float(distance[i]) >3):   #如果距离大于3米 <5米
            mid_index5=mid.index(id[i])
            mac_str5=mac[i][:-3]
            if mac_str5  not in maclist5:
                maclist5.append(mac_str5)  #探测3~5米范围内的mac列表
                u_time5.append(c_time[i])   #探测3~5m范围内MAC的采集时间
                u_distance5.append(distance[i])  #探测3~5m范围内MAC的距离
                duration5.append(0)   #探测3~5m范围内MAC的停留时间
            elif mac_str5 in maclist5:
                mac_index5=maclist5.index(mac_str)
                duration5[mac_index5]=(c_time[i]-u_time5[mac_index5]).total_seconds()#计算3~5m停留时间
                u_time5[mac_index5]=c_time[i]
                if float(duration5[mac_index5]) <70 :
                    if mac_str5  not in mac_list5:
                        mac_list5.append(mac_str5)  #3~5m超过计时单位的mac
                        wifi_id5.append(id[i])  #3~5m超过计时单位的mid
                        n5.append(0)  #3~5m超过计时单位的列表
                    
                    elif mac_str5  in mac_list5:
                        mac_index5=mac_list5.index(mac_str5)
                        n5[mac_index5]=n5[mac_index5]+1  #3~5m内超过计时单位的列表累加
                        
        elif float(distance[i]) >5 : 
            mid_index5=mid.index(id[i])
            mac_str5=mac[i][:-3]
            if mac_str5 in maclist5:   
                mac_index5=maclist5.index(mac_str5)
                del(maclist5[mac_index5])  #超出探测距离5m后删除该mac
                del(u_time5[mac_index5])   #超出探测距离5m后删除该mac的采集时间
                del(duration5[mac_index5])  #超出探测距离5m后删除该mac的停留时间 
                del(u_distance5[mac_index5])  #超出探测距离5m后删除该mac的距离
            if mac_str5 in mac_list5:
                mac_index5=mac_list5.index(mac_str5)
                del(n5[mac_index5])   #超出探测距离5m后删除该mac的计时单位
                del(mac_list5[mac_index5])  #超出探测距离5m后删除达到停留时间的mac 
                del(wifi_id5[mac_index5])   #超出探测距离5m后删除达到停留时间的mid
                
                
    #存入数据库的mac_list5 wifi_id5 n5  mac_list1 wifi_id n
    

    #print (mac_list1,wifi_id,n)
    #print (mac_list5,maclist5,duration5,wifi_id5,n5)

    for y in range(0,len(n)):
        if n[y] < 3 :
            wifi_id[y]="x"   
    dic = collections.Counter(wifi_id)  #判断3米停留时间小于规定时间的个数

    del dic["x"]   #去掉冗余
    #print ("dic=",dic)
    for y in range(0,len(n5)):
        if n5[y] < 3 :
            wifi_id5[y]="x"
    dic5 = collections.Counter(wifi_id5)  #判断3米停留时间小于规定时间的个数

    del dic5["x"]   #去掉冗余
    #print (dic5)
    for key in dic5:
        if key in dic.keys():
            num1=dic[key]
            
        else:
            num1=0
        key_index=wifi_id_add.index(str(key))
        
        store_select=store_name[key_index]  #判断wifi设备id对应的门店
        wifiprobeData_day.objects.create(device_id=key,wifi_3m_num=dic5[key],wifi_1m_num=num1,store=store_select)  #存入当天数据
        
    duration.clear()
    duration5.clear()
    maclist1.clear()
    maclist5.clear()
    u_time.clear()
    u_time5.clear()
    u_distance.clear()
    u_distance5.clear()
    mac_list1.clear()
    mac_list5.clear()
    n.clear()
    n5.clear()
    wifi_id.clear()
    wifi_id5.clear()
    
    
    satisfy_data=[]
    satisfy_day=[]
    good_day=[]
    unsatisfy_day=[]
    sy_device_id=[]
    device_id_satisfy_day=[]
    execllect=[]
    good=[]
    unsatisfy=[]
    #计算当天满意度数据
    #从实时数据库SatisfactionData获取实时数据
    satisfy_data=SatisfactionData.objects.filter(add_time__year=year,add_time__month=month,add_time__day=day).values("excellent_num","good_num","unsatisfy_num","device_id").order_by('add_time')
    #print (satisfy_data)
    for satisfy_data in satisfy_data:   #字典遍历
        execllect.append(satisfy_data['excellent_num'])
        good.append(satisfy_data['good_num'])
        unsatisfy.append(satisfy_data['unsatisfy_num'])
        sy_device_id.append(satisfy_data['device_id'])
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
    day_time=now().date() + timedelta(days=0)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for i in range(len(device_id_satisfy_day)):
        device_id_index=device_id_add.index(device_id_satisfy_day[i])
        store_select=store_name[device_id_index]
        SatisfactionData_day.objects.create(device_id=device_id_satisfy_day[i],name=device_id_satisfy_day[i],excellent_num=satisfy_day[i],good_num=good_day[i],unsatisfy_num=unsatisfy_day[i],add_time= time_stamp,time=day_time,store=store_select)  #存入当天数据

    
    
    excellent_add=[]
    good_add=[]
    unsatisfy_add=[]
    device_satisfy=[]
    store_name_add=[]
    device_id_add=[]
    wifi3=[]
    wifi1=[]
    store_wifi=[]
    sati=SatisfactionData_day.objects.filter(time__year=year,time__month=month,time__day=day).values("excellent_num","good_num","unsatisfy_num","store")
    for sa_data in sati:
        store_name_add.append(sa_data['store'])
        excellent_add.append(sa_data['excellent_num'])
        good_add.append(sa_data['good_num'])
        unsatisfy_add.append(sa_data['unsatisfy_num'])
    wifi_data=wifiprobeData_day.objects.filter(time__year=year,time__month=month,time__day=day).values("store","wifi_3m_num","wifi_1m_num")
    for wifi_data_add in wifi_data:
        store_wifi.append(wifi_data_add['store'])
        wifi1.append(wifi_data_add['wifi_1m_num'])
        wifi3.append(wifi_data_add['wifi_3m_num'])
    
    
    
    #统计前一天产品销售数据
    store_last=[]
    num_saleproduct_last=[]
    sum_saleproduct_last=[]
    total_num_last=[]
    total_sum_last=[]
    date_last = str(now().date() + timedelta(days=-1)).split('-') #获取前一天时间
    year_last=date_last[0]
    month_last=date_last[1]
    day_last=str(int(date_last[2]))
    #print (year_last,month_last,day_last)
    salepro_day_last=SaleProduct_day.objects.filter(time__year=year_last,time__month=month_last,time__day=day_last).values("store","quantity_pro","sum_pro","quantity_total_pro","sum_total_pro")
    for sale_data_last in salepro_day_last:   #字典遍历
        store_last.append(sale_data_last['store'])
        num_saleproduct_last.append(sale_data_last['quantity_pro']) #产品销售数量
        sum_saleproduct_last.append(sale_data_last['sum_pro'])  # 产品销售额
        total_num_last.append(sale_data_last['quantity_total_pro']) # 累计产品销售数量
        total_sum_last.append(sale_data_last['sum_total_pro']) #累计产品销售额
    
    #统计前一天配件销售数据
    store_acc_last=[]
    num_saleacc_last=[]
    sum_saleacc_last=[]
    total_accnum_last=[]
    total_accsum_last=[]
    #print (year_last,month_last,day_last)
    saleacc_day_last=SaleAccessory_day.objects.filter(time__year=year_last,time__month=month_last,time__day=day_last).values("store","quantity_acc","sum_acc","quantity_total_acc","sum_total_acc")
    for sale_acc_last in saleacc_day_last:   #字典遍历
        store_acc_last.append(sale_acc_last['store'])
        num_saleacc_last.append(sale_acc_last['quantity_acc']) #产品销售数量
        sum_saleacc_last.append(sale_acc_last['sum_acc'])  # 产品销售额
        total_accnum_last.append(sale_acc_last['quantity_total_acc']) # 累计产品销售数量
        total_accsum_last.append(sale_acc_last['sum_total_acc']) #累计产品销售额
    
    #统计当天配件销售数据
    saleacc_data=[]
    store_acc_now=[]
    quantity_acc_now=[]
    price_acc_now=[]
    sum_acc_now=[]
    time_acc_sale=[]
    store_acc_day=[]
    quantity_acc_day=[]
    price_acc_day=[]
    sum_acc_day=[]
    time_saleacc_day=[]
    total_acc_num=[]
    total_acc_sum=[]
    saleacc_data=SaleAccessory.objects.filter(time__year=year,time__month=month,time__day=day).values("store","time","quantity","price","sum") #按销售时间查询，不是按录入时间查询，排除延时录入被漏掉的可能性
    for sale_accdata in saleacc_data:   #字典遍历
        store_acc_now.append(sale_accdata['store'])
        quantity_acc_now.append(sale_accdata['quantity'])
        price_acc_now.append(sale_accdata['price'])
        sum_acc_now.append(sale_accdata['sum'])
        time_acc_sale.append(sale_accdata['time'])
    for x in range(len(store_acc_now)):
        if store_acc_now[x] not in store_acc_day:
            store_acc_day.append(store_acc_now[x])
            quantity_acc_day.append(quantity_acc_now[x])
            price_acc_day.append(price_acc_now[x])
            sum_acc_day.append(sum_acc_now[x])
        
        elif store_acc_now[x] in store_acc_day:
            store_acc_index=store_acc_day.index(store_acc_now[x])
            quantity_acc_day[store_acc_index]=quantity_acc_day[store_acc_index]+quantity_acc_now[x]
            sum_acc_day[store_acc_index]=sum_acc_day[store_acc_index]+sum_acc_now[x]
            price_acc_day[store_acc_index]=price_acc_day[store_acc_index]+price_acc_now[x]
    for x in range (len(store_name)):    #如果门店没有销售，则将销售额/销售量/价格设置为0
        if store_name[x] not in store_acc_day:
            store_acc_day.append(store_name[x])
            quantity_acc_day.append(0)
            sum_acc_day.append(0)
            price_acc_day.append(0)
        #统计当天销售数据累计
    for i in range(len(store_acc_day)):
        total_acc_num.append(0)
        total_acc_sum.append(0)
    for k in range(len(store_acc_day)):
        if store_acc_day[k] in store_acc_last:  #如果今天销售数据中门店在前一天的销售数据中有
            store_acc_index_last=store_acc_last.index(store_acc_day[k])  #如果今天的销售数据中的门店在前一天有数据，定位index
            total_acc_num[k]=total_accnum_last[store_acc_index_last]+quantity_acc_day[k] #今天的数量+前一天的数量
            total_acc_sum[k]=total_accsum_last[store_acc_index_last]+sum_acc_day[k]
        else:                                 #如果今天销售数据中新增门店
            total_acc_num[k]=quantity_acc_day[k] 
            total_acc_sum[k]=sum_acc_day[k]
    
    
    
    
    #统计当天产品销售数据
    salepro_data=[]
    store_now=[]
    quantity_now=[]
    price_now=[]
    sum_now=[]
    time_sale=[]
    store_day=[]
    quantity_day=[]
    price_day=[]
    sum_day=[]
    time_sale_day=[]
    total_num=[]
    total_sum=[]
    
    for x in range(len(store_name)):
        quantity_day.append(0)
        price_day.append(0)
        sum_day.append(0)
        total_num.append(0)
        total_sum.append(0)
    
    
    salepro_data=SaleProduct.objects.filter(time__year=year,time__month=month,time__day=day).values("store","time","quantity","price","sum") #按销售时间查询，不是按录入时间查询，排除延时录入被漏掉的可能性
    for sale_data in salepro_data:   #字典遍历
        store_now.append(sale_data['store'])
        quantity_now.append(sale_data['quantity'])
        price_now.append(sale_data['price'])
        sum_now.append(sale_data['sum'])
        time_sale.append(sale_data['time'])
    for x in range(len(store_now)):
        store_index=store_name.index(store_now[x])
        quantity_day[store_index]=quantity_day[store_index]+quantity_now[x]
        price_day[store_index]=price_day[store_index]+price_now[x]
        sum_day[store_index]=sum_day[store_index]+sum_now[x]

    '''
    for x in range (len(store_name)):    #如果门店没有销售，则将销售额/销售量/价格设置为0
        if store_name[x] not in store_day:
            store_day.append(store_name[x])
            quantity_day.append(0)
            sum_day.append(0)
            price_day.append(0)
    
        #统计当天销售数据累计
    city_day=[]
    region_day=[]
    for i in range(len(store_name)):
        total_num.append(0)
        total_sum.append(0)
    '''
    print (store_name,city_name,region_name)
    for k in range(len(store_last)):
        if store_last[k] in store_name:  #如果今天销售数据中门店在前一天的销售数据中有
            store_index_last=store_name.index(store_last[k])  #如果今天的销售数据中的门店在前一天有数据，定位index
            total_num[store_index_last]=total_num_last[x]+quantity_day[store_index_last] #今天的数量+前一天的数量
            total_sum[store_index_last]=total_sum_last[x]+sum_day[store_index_last]
        else:
            pass
    
    if store_name:
        for i in range(len(store_name)):
            if store_name[i] in store_wifi:
                wifi_index=store_wifi.index(store_name[i])  #定位wifi设备门店
                wifi1_select=int(wifi1[wifi_index])
                wifi3_select=int(wifi3[wifi_index])
                sa_index=store_name_add.index(store_name[i])  #定位满意度门店
                execllect_select=int(excellent_add[sa_index])
                good_select=int(good_add[sa_index])
                unsatisfy_select=int(unsatisfy_add[sa_index])
                acc_index=store_acc_day.index(store_name[i])   #定位配件销售门店
                quantity_acc_select=int(quantity_acc_day[acc_index])
                sum_acc_select=sum_acc_day[acc_index]
                total_acc_num_select=int(total_acc_num[acc_index])
                total_acc_sum_select=float("%0.2f" % total_acc_sum[acc_index])
                if quantity_acc_day[acc_index]!=0:
                    price_acc_select=float("%0.2f" % (sum_acc_day[acc_index]/quantity_acc_day[acc_index]))
                else:
                    price_acc_select=price_acc_day[acc_index]
                if quantity_day[i]!=0:
                    price_day[i]=float("%0.2f" % (sum_day[i]/quantity_day[i]))
                total_sum[i]=float("%0.2f" % total_sum[i])
                day_time=now().date() + timedelta(days=0)  #获取今天时间       date = now().date() + timedelta(days=-1) #昨天
                time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
                
                SaleProduct_day.objects.create(store=str(store_name[i]),time=day_time,quantity_pro=int(quantity_day[i]),price_pro=price_day[i],sum_pro=float(sum_day[i]),add_time= time_stamp,quantity_total_pro=int(total_num[i]),sum_total_pro=total_sum[i],wifi_1m_num=wifi1_select,wifi_3m_num=wifi3_select,excellent_num=execllect_select,good_num=good_select,unsatisfy_num=unsatisfy_select,price_acc=price_acc_select,quantity_acc=quantity_acc_select,quantity_total_acc=total_acc_num_select,sum_acc=sum_acc_select,sum_total_acc=total_acc_sum_select,city=city_name[i],region=region_name[i])  #存入当天数据
                
                
    salestore_data=SaleProduct_day.objects.filter(time__year=year,time__month=month,time__day=day).values("store","time","quantity_pro","price_pro","sum_pro","quantity_total_pro","sum_total_pro","wifi_1m_num","wifi_3m_num","excellent_num","good_num","unsatisfy_num","price_acc","quantity_acc","quantity_total_acc","sum_acc","sum_total_acc","city","region") 
    cityname=[]
    quantity_pro=[]
    price_pro=[]
    sum_pro=[]
    quantity_total_pro=[]
    sum_total_pro=[]
    wifi_1m_num=[]
    wifi_3m_num=[]
    excellent_num=[]
    good_num=[]
    unsatisfy_num=[]
    price_acc=[]
    quantity_acc=[]
    quantity_total_acc=[]
    sum_acc=[]
    sum_total_acc=[]
    region=[]
    for sale_data_day in salestore_data:
        if sale_data_day['city'] not in cityname:
            cityname.append(sale_data_day['city'])
            quantity_pro.append(sale_data_day['quantity_pro'])
            price_pro.append(sale_data_day['price_pro'])
            sum_pro.append(sale_data_day['sum_pro'])
            quantity_total_pro.append(sale_data_day['quantity_total_pro'])
            sum_total_pro.append(sale_data_day['sum_total_pro'])
            wifi_1m_num.append(sale_data_day['wifi_1m_num'])
            wifi_3m_num.append(sale_data_day['wifi_3m_num'])
            excellent_num.append(sale_data_day['excellent_num'])
            good_num.append(sale_data_day['good_num'])
            unsatisfy_num.append(sale_data_day['unsatisfy_num'])
            price_acc.append(sale_data_day['price_acc'])
            quantity_acc.append(sale_data_day['quantity_acc'])
            quantity_total_acc.append(sale_data_day['quantity_total_acc'])
            sum_acc.append(sale_data_day['sum_acc'])
            sum_total_acc.append(sale_data_day['sum_total_acc'])
            region.append(sale_data_day['region'])
        elif sale_data_day['city'] in cityname:
            index=cityname.index(sale_data_day['city'])
            quantity_pro[index]=quantity_pro[index]+sale_data_day['quantity_pro']
            price_pro[index]=price_pro[index]+sale_data_day['price_pro']
            sum_pro[index]=sum_pro[index]+sale_data_day['sum_pro']
            quantity_total_pro[index]=quantity_total_pro[index]+sale_data_day['quantity_total_pro']
            sum_total_pro[index]=sum_total_pro[index]+sale_data_day['sum_total_pro']
            wifi_1m_num[index]=wifi_1m_num[index]+sale_data_day['wifi_1m_num']
            wifi_3m_num[index]=wifi_3m_num[index]+sale_data_day['wifi_3m_num']
            excellent_num[index]=excellent_num[index]+sale_data_day['excellent_num']
            good_num[index]=good_num[index]+sale_data_day['good_num']
            unsatisfy_num[index]=unsatisfy_num[index]+sale_data_day['unsatisfy_num']
            price_acc[index]=price_acc[index]+sale_data_day['price_acc']
            quantity_acc[index]=quantity_acc[index]+sale_data_day['quantity_acc']
            quantity_total_acc[index]=quantity_total_acc[index]+sale_data_day['quantity_total_acc']
            sum_acc[index]=sum_acc[index]+sale_data_day['sum_acc']
            sum_total_acc[index]=sum_total_acc[index]+sale_data_day['sum_total_acc']
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for i in range(len(cityname)):
        SaleProduct_day_city.objects.create(time=day_time,quantity_pro=int(quantity_pro[i]),price_pro=price_pro[i],sum_pro=float(sum_pro[i]),add_time= time_stamp,quantity_total_pro=int(quantity_total_pro[i]),sum_total_pro=sum_total_pro[i],wifi_1m_num=wifi_1m_num[i],wifi_3m_num=wifi_3m_num[i],excellent_num=excellent_num[i],good_num=good_num[i],unsatisfy_num=unsatisfy_num[i],price_acc=price_acc[i],quantity_acc=quantity_acc[i],quantity_total_acc=quantity_total_acc[i],sum_acc=sum_acc[i],sum_total_acc=sum_total_acc[i],city=cityname[i],region=region[i])  #存入当天数据
    cityname.clear()
    quantity_pro.clear()
    price_pro.clear()
    sum_pro.clear()
    quantity_total_pro.clear()
    sum_total_pro.clear()
    wifi_1m_num.clear()
    wifi_3m_num.clear()
    excellent_num.clear()
    good_num.clear()
    unsatisfy_num.clear()
    price_acc.clear()
    quantity_acc.clear()
    quantity_total_acc.clear()
    sum_acc.clear()
    sum_total_acc.clear()
    region.clear()
    regionname=[]
    quantity_pro=[]
    price_pro=[]
    sum_pro=[]
    quantity_total_pro=[]
    sum_total_pro=[]
    wifi_1m_num=[]
    wifi_3m_num=[]
    excellent_num=[]
    good_num=[]
    unsatisfy_num=[]
    price_acc=[]
    quantity_acc=[]
    quantity_total_acc=[]
    sum_acc=[]
    sum_total_acc=[]
    region=[]
    
    
    salecity_data=SaleProduct_day_city.objects.filter(time__year=year,time__month=month,time__day=day).values("time","quantity_pro","price_pro","sum_pro","quantity_total_pro","sum_total_pro","wifi_1m_num","wifi_3m_num","excellent_num","good_num","unsatisfy_num","price_acc","quantity_acc","quantity_total_acc","sum_acc","sum_total_acc","city","region") 
    for sale_data_city in salecity_data:
        if sale_data_city['region'] not in regionname:
            regionname.append(sale_data_city['region'])
            quantity_pro.append(sale_data_city['quantity_pro'])
            price_pro.append(sale_data_city['price_pro'])
            sum_pro.append(sale_data_city['sum_pro'])
            quantity_total_pro.append(sale_data_city['quantity_total_pro'])
            sum_total_pro.append(sale_data_city['sum_total_pro'])
            wifi_1m_num.append(sale_data_city['wifi_1m_num'])
            wifi_3m_num.append(sale_data_city['wifi_3m_num'])
            excellent_num.append(sale_data_city['excellent_num'])
            good_num.append(sale_data_city['good_num'])
            unsatisfy_num.append(sale_data_city['unsatisfy_num'])
            price_acc.append(sale_data_city['price_acc'])
            quantity_acc.append(sale_data_city['quantity_acc'])
            quantity_total_acc.append(sale_data_city['quantity_total_acc'])
            sum_acc.append(sale_data_city['sum_acc'])
            sum_total_acc.append(sale_data_city['sum_total_acc'])

        elif sale_data_city['city'] in regionname:
            index=regionname.index(sale_data_city['region'])
            quantity_pro[index]=quantity_pro[index]+sale_data_city['quantity_pro']
            price_pro[index]=price_pro[index]+sale_data_city['price_pro']
            sum_pro[index]=sum_pro[index]+sale_data_city['sum_pro']
            quantity_total_pro[index]=quantity_total_pro[index]+sale_data_city['quantity_total_pro']
            sum_total_pro[index]=sum_total_pro[index]+sale_data_city['sum_total_pro']
            wifi_1m_num[index]=wifi_1m_num[index]+sale_data_city['wifi_1m_num']
            wifi_3m_num[index]=wifi_3m_num[index]+sale_data_city['wifi_3m_num']
            excellent_num[index]=excellent_num[index]+sale_data_city['excellent_num']
            good_num[index]=good_num[index]+sale_data_city['good_num']
            unsatisfy_num[index]=unsatisfy_num[index]+sale_data_city['unsatisfy_num']
            price_acc[index]=price_acc[index]+sale_data_city['price_acc']
            quantity_acc[index]=quantity_acc[index]+sale_data_city['quantity_acc']
            quantity_total_acc[index]=quantity_total_acc[index]+sale_data_city['quantity_total_acc']
            sum_acc[index]=sum_acc[index]+sale_data_city['sum_acc']
            sum_total_acc[index]=sum_total_acc[index]+sale_data_city['sum_total_acc']
    time_stamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))#获取系统当前时间戳
    for i in range(len(regionname)):
        SaleProduct_day_region.objects.create(time=day_time,quantity_pro=int(quantity_pro[i]),price_pro=price_pro[i],sum_pro=float(sum_pro[i]),add_time= time_stamp,quantity_total_pro=int(quantity_total_pro[i]),sum_total_pro=sum_total_pro[i],wifi_1m_num=wifi_1m_num[i],wifi_3m_num=wifi_3m_num[i],excellent_num=excellent_num[i],good_num=good_num[i],unsatisfy_num=unsatisfy_num[i],price_acc=price_acc[i],quantity_acc=quantity_acc[i],quantity_total_acc=quantity_total_acc[i],sum_acc=sum_acc[i],sum_total_acc=sum_total_acc[i],region=regionname[i])  #存入当天数据
    
    store_now.clear()
    quantity_now.clear()
    price_now.clear()
    sum_now.clear()
    time_sale.clear()
    store_day.clear()
    quantity_day.clear()
    price_day.clear()
    sum_day.clear()
    time_sale_day.clear()
    total_num.clear()
    total_sum.clear()
    excellent_add.clear()
    good_add.clear()
    unsatisfy_add.clear()
    device_satisfy.clear()
    store_name_add.clear()
    device_id_add.clear()
    wifi3.clear()
    wifi1.clear()
    store_wifi.clear()
    device_id_satisfy_day.clear()
    satisfy_day.clear()
    good_day.clear()
    unsatisfy_day.clear()
    execllect.clear()
    good.clear()
    unsatisfy.clear()
    sy_device_id.clear()
    store_name.clear()
    device_id_add.clear()
    wifi_id_add.clear()
    store_add.clear()
    #city_day.clear()
    #region_day.clear()
    city_id.clear()
    city.clear()
    city_name.clear()
    region_id.clear()
    region.clear()
    region_dict_name.clear()
    region_name.clear()
