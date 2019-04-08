# coding:utf-8
import json
import csv
import ast
import os
import time
import datetime
from io import StringIO
from django.http import StreamingHttpResponse 
from io import BytesIO
import xlwt
from django.http import FileResponse
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from json import dumps
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import View
from django.db.models import Q
from django.db.models import Count,Sum
#from datetime import datetime
from .models import RegionDict,ProvinceDict, CityDict, Store, SaleProduct, RegionDict,Store , SaleProduct_day,SaleProduct_day_city,SaleProduct_day_region,SaleProduct_day_province
from device.models import wifiprobeData,wifiprobeData_day,wifiprobeData_day_city,wifiprobeData_day_region,wifiprobeData_week,wifiprobeData_month,wifiprobeData_quarter,wifiprobeData_year,SatisfactionData_day,SatisfactionData_day_city,SatisfactionData_day_region,SatisfactionData_week,SatisfactionData_month,SatisfactionData_quarter,SatisfactionData_year
from users.forms import DataProductForm
#from datetime import date
from django.http import HttpResponse
#import simplejson
# Create your views here.

try:
    import cStringIO as stringIOModule
except ImportError:
    try:
        import StringIO as stringIOModule
    except ImportError:
        import io as stringIOModule


class OrgView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    
    
    
    def get(self, request):
        all_region = RegionDict.objects.all()
        return render(request, "data_input.html",{"all_region":all_region})
    #store = forms.CharField()
    def post(self, request):
        # 查找到所有的区域
        all_region = RegionDict.objects.all()
        # 取出所有的城市
        all_province= ProvinceDict.objects.all()
        all_city = CityDict.objects.all()
        # 查找所有门店
        all_store = Store.objects.all()
        #Sale_Product = SaleProduct()
        
        if request.is_ajax():
            if request.method == 'POST':
                array = request.POST.getlist('table')  #django接收数组
                region=request.POST.get('region',"")
                province=request.POST.get('province',"")
                city=request.POST.get('city',"")
                store=request.POST.get('store',"")
                date_select=request.POST.get('date',"")
                print("province=",province)
                if region=="":
                    return HttpResponse("请重新选择区域")
                if city=="":
                    return HttpResponse("请重新选择城市")
                store_select = all_store.filter(name=str(store)).values('id')
                #print (store_select)
                if not store_select:
                    return HttpResponse('{"status":"error"}', content_type='application/json')
            #print (region,city,store,date_select)
            #print ("table2=",array) 
            device_id=all_store.filter(name=str(store)).values('device_id')
            for device_data in device_id:
                device=device_data['device_id']
            data=eval(array[0])#将字符串转换位列表
            #print ("len=",array[0].split())
            #data2=array[1]
            #print (device)
            #print (data[0]['SumMoney'])
            #Sale_Product.store=store
            #Sale_Product.time=date_select
            for x in range(len(data)):
                #Sale_Product.quantity=int(data[x]['Amount'])
                #Sale_Product.classification=data[x]['ProductName']
                #Sale_Product.item=data[x]['Item']
                #Sale_Product.price=float(data[x]['Price'])
                #Sale_Product.sum=float(data[x]['SumMoney'])
                #SaleProduct.objects.create(quantity=int(data[x]['Amount']),classification=data[x]['ProductName'],item=data[x]['Item'],price=float(data[x]['Price'].strip()),sum=float(data[x]['SumMoney'].strip()),store=store,city=city,province=province,region=region,time=date_select,device_id=device_id)
                SaleProduct.objects.create(quantity=int(data[x]['Amount']),classification=data[x]['ProductName'],sum=float(data[x]['SumMoney'].strip()),store=store,city=city,province=province,region=region,time=date_select,device_id=device)
            
            
            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse("数据提交成功！")
        '''
        region=request.POST.get('region',"")
        city=request.POST.get('city',"")
        store=request.POST.get('store',"")
        date_select=request.POST.get('date',"")
        table=request.POST.getlist('Submit3')
        table1=request.POST.getlist('table')
        if date_select=="":
            return HttpResponse("请重新选择时间") 
        #print (region,city,store,date_select)
        #print ("table2=",array)
        '''
        #dataproduct_form = DataProductForm(request.POST)
        #if dataproduct_form.is_valid():
        #store = request.POST.get("store")
        #product = request.POST.get("product", "")
        #time = request.POST.get("date")
        #quantity = request.POST.get("quantity","")
        #price = request.POST.get("price","")
        #quantity_a = request.POST.get("quantity_a","")
        #price_a = request.POST.get("price_a","")
        #sum = request.POST.get("sum", "")
            #pass_word = request.POST.get("password", "")
        #print (quantity,price,quantity_a,price_a)
            #return HttpResponse('{"status": "success", "msg":"修改成功"}',content_type="application/json")
        #Sale_Product=SaleProduct.objects.get()
        '''
        Sale_Product = SaleProduct()
        Sale_Accessory = SaleAccessory()
        #Sale_Product.product=product
        #if store=="":
        #    store="黄埔华莱士"
        Sale_Product.store=store
        Sale_Accessory.store=store
        #if time=="":
        #    time=datetime.now()
        Sale_Product.time=date_select
        Sale_Accessory.time=date_select
        #if quantity=="":
        #    quantity=0
        #Sale_Product.quantity=int(quantity)
        #Sale_Accessory.quantity=int(quantity_a)
        #if price=="":
        #    price=0
        #Sale_Product.price=float(price)
        #Sale_Accessory.price=float(price_a)
        #sum=int(quantity)*float(price)
        #sum_a=int(quantity_a)*float(price_a)
        #Sale_Product.sum=float(sum)
        #Sale_Accessory.sum=float(sum_a)
        #Sale_Product.save()
        #Sale_Accessory.save()
        return HttpResponse("数据提交成功！")
        #return render(request, "data_input.html",{})
        '''
class Return_Province_DataView(View):
    def get(self,request):
        all_province=ProvinceDict.objects.all()
        all_region = RegionDict.objects.all()
        region_id = request.GET['region']
        all_province = all_province.filter(region_id=int(region_id))
        #print (region_id)
        Province_list = []
        for province in all_province:
            Province_list.append(province.name)
        return HttpResponse(json.dumps(Province_list))    


class Return_City_DataView(View):
    def get(self,request):
        all_province=ProvinceDict.objects.all()
        all_city=CityDict.objects.all()
        all_region = RegionDict.objects.all()
        #region_id,province_name = request.GET['region'],request.GET['province']
        #region_id = request.GET['region']
        province_name = request.GET['province']
        #all_city = all_city.filter(region_id=int(region_id))
        #print ('province_name=',province_name)
        #select_region=all_region.filter(id=int(region_id))
        select_province=all_province.filter(name=str(province_name))
        #print(select_province)
        for province in select_province:
            select_city=all_city.filter(province__id=int(province.id))
        City_list = []
        for city in select_city:
            City_list.append(city.name)
        return HttpResponse(json.dumps(City_list))    

class Return_Store_DataView(View):
    def get(self,request):
        all_city=CityDict.objects.all()
        all_province=ProvinceDict.objects.all()
        all_store=Store.objects.all()
        all_region = RegionDict.objects.all()
        #region_id,province_name,city_name = request.GET['region'],request.GET['province'],request.GET['City']
        city_name = request.GET['City']
        #print (region_id,city_name)
        #select_region=all_region.filter(id=int(region_id))
        select_city=all_city.filter(name=str(city_name))
        Store_list=[]
        for city in select_city:
            select_store=all_store.filter(city__id=int(city.id))
        for store in select_store:
            Store_list.append(store.name)
        return HttpResponse(json.dumps(Store_list))

class DetailView(View):
    #login_url = '/login/'
    #redirect_field_name = 'next'
    def get(self, request):
        all_region = RegionDict.objects.all()
        return render(request, "detail.html",{"all_region":all_region})
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
        data1=""
        data2=""
        data3=""
        data4=""
        data5=""
        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        all_province= ProvinceDict.objects.all()
        region_id=request.POST.get('region',"")
        province_id=request.POST.get('province',"")
        city_id=request.POST.get('city',"")
        store_id=request.POST.get('store',"")
        detail_select=request.POST.get('detail_select',"")
        #print('city=',city_id)
        #print('store=',store_id)
        date_from=request.POST.get('date',"")
        date_to=request.POST.get('date2',"")
        #print (region_id,city_id,store_id,date_from,date_to)
        if region_id=="":
            return HttpResponse("请重新选择区域")
        if province_id=="":
            return HttpResponse("请重新选择省份")
        if city_id=="":
            return HttpResponse("请重新选择城市")
        if store_id=="":
            return HttpResponse("请重新选择门店")
        if date_from =="" or date_to=="":
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
        #print (region_select,city_select,store_select)
        #if region_id and city_id and store_id and date_from and date_to :
        #if region_id and city_id and store_id :
        url_request="/org/detailselect/"+str(region)+"/"+str(province)+"/"+str(city)+"/"+str(store)+"/"
        #url_request="/org/detail/"+str(region)+"/"+str(province)+"/"+str(city)+"/"+str(store)+"/"
        #print (url_request)
        return redirect(url_request+"?from="+str(date_from)+"&to="+str(date_to)+"&detail="+str(detail_select))
        
class DetailSelectView(View):
    def get(self, request,param1,param2,param3,param4):
        num1=param1
        num2=param2
        num3=param3
        num4=param4
        deviceid=0
        date_from=request.GET.get('from',"")
        date_to=request.GET.get('to',"")
        num5=request.GET.get('detail',"")
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
        '''
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
        print(region_id ,province_id,city_id,store_id)
        '''
        #print (num1,num2,num3,num4,num5)
        if num5=="1":
            return render(request, "detail_auth.html",{"all_region":all_region,
                                                  "region":json.dumps(num1),
                                                  "province":json.dumps(num2),
                                                  "city":json.dumps(num3),
                                                  "store":json.dumps(num4),
                                                  "detail_select":json.dumps(num5),
                                                  "date_from":json.dumps(date_from),
                                                  "date_to":json.dumps(date_to)})
        
        
        if num5=="2":
            return render(request, "detail_auth_people.html",{"all_region":all_region,
                                                  "region":json.dumps(num1),
                                                  "province":json.dumps(num2),
                                                  "city":json.dumps(num3),
                                                  "store":json.dumps(num4),
                                                  "detail_select":json.dumps(num5),
                                                  "date_from":json.dumps(date_from),
                                                  "date_to":json.dumps(date_to)})
        
        if num5=="3":
            return render(request, "detail_auth_sa.html",{"all_region":all_region,
                                                  "region":json.dumps(num1),
                                                  "province":json.dumps(num2),
                                                  "city":json.dumps(num3),
                                                  "store":json.dumps(num4),
                                                  "detail_select":json.dumps(num5),
                                                  "date_from":json.dumps(date_from),
                                                  "date_to":json.dumps(date_to)})
        
        
        '''
        region_select = all_region.filter(name=str(region_id))
        city_select = all_city.filter(name=str(city_id))
        store_select = all_store.filter(name=str(store_id))
        print (region_select,city_select,store_select)
        if region_id and city_id and store_id and date_from and date_to :
            if date_from > date_to:
                return HttpResponse("请重新选择时间")
            elif date_from <= date_to:
                data_list=[]
                data_list=SaleProduct_day.objects.filter(store=store_select.values('name'),time__range=(date_from, date_to)).values('sum_pro','sum_acc','price_pro','sum_total_pro','quantity_total_pro','wifi_1m_num','wifi_3m_num','quantity_pro','quantity_acc','price_acc','sum_total_acc','quantity_total_acc','excellent_num','good_num','unsatisfy_num','time').order_by('time')
                return render(request, "detail.html",
                    {"data_list":data_list,
                     #"num":num,
                     "region":region_id,
                     "city":city_id,
                     "store":store_id,
                     })
        else:
            print ("无权限")
            all_region = RegionDict.objects.all()
            return render(request,"detail.html",{"all_region":all_region})
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

class DetailAuthView(View):
    #login_url = '/login/'
    #redirect_field_name = 'next'
    def get(self, request,param1,param2,param3,param4):
        num1=param1
        num2=param2
        num3=param3
        num4=param4
        deviceid=0
        date_from=request.GET.get('from',"")
        date_to=request.GET.get('to',"")
        num5=request.GET.get('detail',"")
        offset=request.GET.get('offset')
        limit = request.GET.get('limit')
        if date_from=="":
            return HttpResponse("请重新选择时间")
        if date_to=="":
            return HttpResponse("请重新选择时间")
        #print ("param=",num1,num2,num3,num4)
        #print(date_from,date_to,num5)
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
        datalist=[]
        data_list=[]
        store_data=[]
        city_data=[]
        region_data=[]
        sum1j=0
        quantity1j=0
        sum1p=0
        quantity1p=0
        sumj=[]
        sump=[]
        quantityj=[]
        quantityp=[]
        if num5=='1':
            if province_id!=0 and city_id!=0 and store_id!=0:
                data_list=SaleProduct_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('sum_pro','price_pro','sum_total_pro','quantity_total_pro','quantity_pro','time','store','city','region','province','item','classification','device_id','sum_total_proj','quantity_total_proj','sum_total_prop','quantity_total_prop').order_by('time')
                '''
                for data in data_list:
                    if data['classification']=='火机':
                        sumj.append(data['sum_pro'])
                    elif data['classification']=='配件':
                        sump.append(data['sum_pro'])
                for data1 in data_list:
                    if data1['classification']=='火机':
                        quantityj.append(data1['quantity_pro'])
                    elif data1['classification']=='配件':
                        quantityp.append(data1['quantity_pro'])
                for x in range(0,len(sumj)):
                    sum1j=sum1j+sumj[x]
                for x in range(0,len(sump)):
                    sum1p=sum1p+sump[x]
                for x in range(0,len(quantityj)):
                    quantity1j=quantity1j+quantityj[x]
                for x in range(0,len(quantityp)):
                    quantity1p=quantity1p+quantityp[x]
                '''
                '''
                sum_total_pro=SaleProduct_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('sum_pro','classification').order_by('time')
                quantity_total_pro=SaleProduct_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('quantity_pro','classification').order_by('time')
                print ("sum_total_pro=",sum_total_pro)
                for data in sum_total_pro:
                    if data['classification']=='火机':
                        sumj.append(data['sum_pro'])
                    elif data['classification']=='配件':
                        sump.append(data['sum_pro'])
                for data1 in quantity_total_pro:
                    if data1['classification']=='火机':
                        quantityj.append(data1['quantity_pro'])
                    elif data1['classification']=='配件':
                        quantityp.append(data1['quantity_pro'])
                for x in range(0,len(sumj)):
                    sum1j=sum1j+sumj[x]
                for x in range(0,len(sump)):
                    sum1p=sum1p+sump[x]
                for x in range(0,len(quantityj)):
                    quantity1j=quantity1j+quantityj[x]
                for x in range(0,len(quantityp)):
                    quantity1p=quantity1p+quantityp[x]
                '''
            elif province_id!=0 and city_id!=0 and store_id==0:
                #print('city_id.values("name")=',city_id.values('name'))
                data_list=SaleProduct_day.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('sum_pro','price_pro','sum_total_pro','quantity_total_pro','quantity_pro','time','store','city','region','province','item','classification','device_id','sum_total_proj','quantity_total_proj','sum_total_prop','quantity_total_prop').order_by('time')
                '''
                sum_total_pro=SaleProduct_day_city.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('sum_pro').order_by('time')
                quantity_total_pro=SaleProduct_day_city.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('quantity_pro').order_by('time')
                for data in sum_total_pro:
                    sum.append(data['sum_pro'])
                for data1 in quantity_total_pro:
                    quantity.append(data1['quantity_pro'])
                for x in range(0,len(sum)):
                    sum1=sum1+sum[x]
                for x in range(0,len(quantity)):
                    quantity1=quantity1+quantity[x]
                #print (data_list)
                '''
            elif province_id!=0 and city_id==0 and store_id==0:
                data_list=SaleProduct_day.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('sum_pro','price_pro','sum_total_pro','quantity_total_pro','quantity_pro','time','store','city','region','province','item','classification','device_id','sum_total_proj','quantity_total_proj','sum_total_prop','quantity_total_prop').order_by('time')
                '''
                sum_total_pro=SaleProduct_day_province.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('sum_pro').order_by('time')
                quantity_total_pro=SaleProduct_day_province.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('quantity_pro').order_by('time')
                for data in sum_total_pro:
                    sum.append(data['sum_pro'])
                for data1 in quantity_total_pro:
                    quantity.append(data1['quantity_pro'])
                for x in range(0,len(sum)):
                    sum1=sum1+sum[x]
                for x in range(0,len(quantity)):
                    quantity1=quantity1+quantity[x]
                #print ("data_list=",data_list)
                '''
            elif province_id==0 and city_id==0 and store_id==0:
                data_list=SaleProduct_day.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('sum_pro','price_pro','sum_total_pro','quantity_total_pro','quantity_pro','time','store','city','region','province','item','classification','device_id','sum_total_proj','quantity_total_proj','sum_total_prop','quantity_total_prop').order_by('time')
                '''
                sum_total_pro=SaleProduct_day_region.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('sum_pro').order_by('time')
                quantity_total_pro=SaleProduct_day_region.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('quantity_pro').order_by('time')
                for data in sum_total_pro:
                    sum.append(data['sum_pro'])
                for data1 in quantity_total_pro:
                    quantity.append(data1['quantity_pro'])
                for x in range(0,len(sum)):
                    sum1=sum1+sum[x]
                for x in range(0,len(quantity)):
                    quantity1=quantity1+quantity[x]
                '''
            for data in data_list:
                if data['classification']=='火机':
                    sumj.append(data['sum_pro'])
                    quantityj.append(data['quantity_pro'])
                elif data['classification']=='配件':
                    sump.append(data['sum_pro'])
                    quantityp.append(data['quantity_pro'])
            for x in range(0,len(sumj)):
                sum1j=sum1j+round(float(sumj[x]),2)
            for x in range(0,len(sump)):
                sum1p=sum1p+round(float(sump[x]),2)
            for x in range(0,len(quantityj)):
                quantity1j=quantity1j+round(float(quantityj[x]),2)
            for x in range(0,len(quantityp)):
                quantity1p=quantity1p+round(float(quantityp[x]),2)
            data_list.update(sum_total_proj=sum1j)
            data_list.update(quantity_total_proj=quantity1j)
            data_list.update(sum_total_prop=sum1p)
            data_list.update(quantity_total_prop=quantity1p)
            data_list_count=data_list.count()
            #print("data_list_count=",data_list_count)
            if data_list_count!=0:
                if not offset:
                    offset = 0
                if not limit:
                    limit = 20    # 默认是每页20行的内容，与前端默认行数一致
                pageinator = Paginator(data_list, limit)   # 开始做分页
                #print (pageinator)
                page = int(int(offset) / int(limit) + 1)    
                response_data = {'total':data_list_count,'rows':[]}   # 必须带有rows和total这2个key，total表示总页数，rows表示每行的内容
                
                for asset in pageinator.page(page):    
                    # 下面这些asset_开头的key，都是我们在前端定义好了的，前后端必须一致，前端才能接受到数据并且请求.
                    #print ('asset=',asset)
                    response_data['rows'].append({
                        #"asset_id": '<a href="/asset/asset_list/%d" target="_blank">%d</a>' %(asset.id,asset.id),   
                        "time" : asset['time'].strftime("%Y-%m-%d ") if asset['time'] else "",
                        "region": asset['region'] if asset['region'] else "",
                        "province": asset['province'] if asset['province'] else "",
                        "city": asset['city'] if asset['city'] else "",
                        "store": asset['store'] if asset['store'] else "",
                        "device_id": asset['device_id'] if asset['device_id'] else "",
                        "classification": asset['classification'] if asset['classification'] else "",
                        "sum_pro": asset['sum_pro'] if asset['sum_pro'] else "",
                        "quantity_pro": asset['quantity_pro'] if asset['quantity_pro'] else "",
                        "sum_total_pro1j": asset['sum_total_proj'] if asset['sum_total_proj'] else "",
                        "quantity_total_pro1j": asset['quantity_total_proj'] if asset['quantity_total_proj'] else "",
                        "sum_total_pro1p": asset['sum_total_prop'] if asset['sum_total_prop'] else "",
                        "quantity_total_pro1p":asset['quantity_total_prop'] if asset['quantity_total_prop'] else "",
                    })
                return  HttpResponse(json.dumps(response_data))
            elif data_list_count==0:
                return HttpResponse("该时间段无数据")
            '''
            if data_list:
                return render(request, "detail_auth.html",
                        {"data_list":data_list,
                         "device_id":deviceid,
                         "sum":sum1,
                         "quantity":quantity1,
                         "all_region":all_region,
                         #"num":num,
                         #"region":region_id,
                         #"city":city_id,
                         #"store":store_id,
                         })
            else:
                #data_list=
                return HttpResponse("该时间段无数据")
            '''
        duration_1=0
        duration_3=0
        
        pd1=[]
        pd3=[]
        if num5=='2':
            if province_id!=0 and city_id!=0 and store_id!=0:
                
                data_list=wifiprobeData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num','wifi_3m_num','wifi_1m_num_total','wifi_3m_num_total','time','device_id','store','city','region','province').order_by('time')
                '''
                people_1=wifiprobeData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num').order_by('time')
                people_3=wifiprobeData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('wifi_3m_num').order_by('time')
                for data in people_1:
                    pd1.append(float(data['wifi_1m_num']))
                #print (pd1)
                for data1 in people_3:
                    pd3.append(float(data1['wifi_3m_num']))
                #print (pd3)
                for x in range(0,len(pd1)):
                    duration_1=duration_1+pd1[x]
                for x in range(0,len(pd3)):
                    duration_3=duration_3+pd3[x]
                '''
            elif province_id!=0 and city_id!=0 and store_id==0:
                data_list=wifiprobeData_day.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num','wifi_3m_num','wifi_1m_num_total','wifi_3m_num_total','time','store','city','region','province','device_id','time').order_by('time')
                '''
                people_1=wifiprobeData_day_city.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num').order_by('time')
                people_3=wifiprobeData_day_city.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('wifi_3m_num').order_by('time')
                for data in people_1:
                    pd1.append(float(data['wifi_1m_num']))
                #print (pd1)
                for data1 in people_3:
                    pd3.append(float(data1['wifi_3m_num']))
                #print (pd3)
                for x in range(0,len(pd1)):
                    duration_1=duration_1+pd1[x]
                for x in range(0,len(pd3)):
                    duration_3=duration_3+pd3[x]
                #print (data_list)
                '''
            elif province_id!=0 and city_id==0 and store_id==0:
                data_list=wifiprobeData_day.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num','wifi_3m_num','wifi_1m_num_total','wifi_3m_num_total','time','store','city','region','province','device_id','time').order_by('time')
                '''
                people_1=wifiprobeData_day_province.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num').order_by('time')
                people_3=wifiprobeData_day_province.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('wifi_3m_num').order_by('time')
                for data in people_1:
                    pd1.append(float(data['wifi_1m_num']))
                #print (pd1)
                for data1 in people_3:
                    pd3.append(float(data1['wifi_3m_num']))
                #print (pd3)
                for x in range(0,len(pd1)):
                    duration_1=duration_1+pd1[x]
                for x in range(0,len(pd3)):
                    duration_3=duration_3+pd3[x]
                #print (data_list)
                '''
            elif province_id==0 and city_id==0 and store_id==0:
                data_list=wifiprobeData_day.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num','wifi_3m_num','wifi_1m_num_total','wifi_3m_num_total','time','store','city','province','region','device_id','time').order_by('time')
                '''
                people_1=wifiprobeData_day_region.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num').order_by('time')
                people_3=wifiprobeData_day_region.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('wifi_3m_num').order_by('time')
                for data in people_1:
                    pd1.append(float(data['wifi_1m_num']))
                #print (pd1)
                for data1 in people_3:
                    pd3.append(float(data1['wifi_3m_num']))
                #print (pd3)
                for x in range(0,len(pd1)):
                    duration_1=duration_1+pd1[x]
                for x in range(0,len(pd3)):
                    duration_3=duration_3+pd3[x]
                '''
            for data in data_list:
                pd1.append(float(data['wifi_1m_num']))
                pd3.append(float(data['wifi_3m_num']))
                #print (pd3)
            for x in range(0,len(pd1)):
                duration_1=duration_1+pd1[x]
            for x in range(0,len(pd3)):
                duration_3=duration_3+pd3[x]
            
            #print(duration_1)
            data_list.update(wifi_1m_num_total=duration_1)
            data_list.update(wifi_3m_num_total=duration_3)
            #print(data_list)
            
            
            data_list_count=data_list.count()
            if not offset:
                offset = 0
            if not limit:
                limit = 20    # 默认是每页20行的内容，与前端默认行数一致
            pageinator = Paginator(data_list, limit)   # 开始做分页

            page = int(int(offset) / int(limit) + 1)    
            response_data = {'total':data_list_count,'rows':[]}   # 必须带有rows和total这2个key，total表示总页数，rows表示每行的内容
            
            for asset in pageinator.page(page):    
                # 下面这些asset_开头的key，都是我们在前端定义好了的，前后端必须一致，前端才能接受到数据并且请求.
                #print ('asset=',asset)
                response_data['rows'].append({
                    #"asset_id": '<a href="/asset/asset_list/%d" target="_blank">%d</a>' %(asset.id,asset.id),   
                    "time" : asset['time'].strftime("%Y-%m-%d ") if asset['time'] else "",
                    "region": asset['region'] if asset['region'] else "",
                    "province": asset['province'] if asset['province'] else "",
                    "city": asset['city'] if asset['city'] else "",
                    "store": asset['store'] if asset['store'] else "",
                    "device_id": asset['device_id'] if asset['device_id'] else "",
                    "wifi_1m_num": asset['wifi_1m_num'] if asset['wifi_1m_num'] else "",
                    "wifi_3m_num": asset['wifi_3m_num'] if asset['wifi_3m_num'] else "",
                    "wifi_1m_num_total": asset['wifi_1m_num_total'] if asset['wifi_1m_num_total'] else "",
                    "wifi_3m_num_total": asset['wifi_3m_num_total'] if asset['wifi_3m_num_total'] else "",
                })
            return  HttpResponse(json.dumps(response_data))
            
            
            '''
            if data_list:
                return render(request, "detail_auth_people.html",
                        {"data_list":data_list,
                         "device_id":deviceid,
                         "all_region":all_region,
                         "duration_1":duration_1,
                         "duration_3":duration_3,
                         #"region":region_id,
                         #"city":city_id,
                         #"store":store_id,
                         })
            else:
                #data_list=
                return HttpResponse("该时间段无数据")
            '''
        ex1=[]
        go1=[]
        un1=[]
        ex2=0
        go2=0
        un2=0
        if num5=='3':
            if province_id!=0 and city_id!=0 and store_id!=0:
                data_list=SatisfactionData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('excellent_num','good_num','unsatisfy_num','excellent_num_total','good_num_total','unsatisfy_num_total','time','store','city','region','province','device_id').order_by('time')
                '''
                ex=SatisfactionData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('excellent_num').order_by('time')
                go=SatisfactionData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('good_num').order_by('time')
                un=SatisfactionData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('unsatisfy_num').order_by('time')
                for data in ex:
                    ex1.append(float(data['excellent_num']))
                for data1 in go:
                    go1.append(float(data1['good_num']))
                for data2 in un:
                    un1.append(float(data2['unsatisfy_num']))
                for x in range(0,len(ex1)):
                    ex2=ex2+ex1[x]
                for x in range(0,len(go1)):
                    go2=go2+go1[x]
                for x in range(0,len(un1)):
                    un2=un2+un1[x]
                '''
            elif province_id!=0 and city_id!=0 and store_id==0:
                data_list=SatisfactionData_day.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('excellent_num','good_num','unsatisfy_num','excellent_num_total','good_num_total','unsatisfy_num_total','time','store','city','region','province','device_id').order_by('time')
                '''
                ex=SatisfactionData_day.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('excellent_num').order_by('time')
                go=SatisfactionData_day.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('good_num').order_by('time')
                un=SatisfactionData_day.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('unsatisfy_num').order_by('time')
                for data in ex:
                    ex1.append(float(data['excellent_num']))
                for data1 in go:
                    go1.append(float(data1['good_num']))
                for data2 in un:
                    un1.append(float(data2['unsatisfy_num']))
                for x in range(0,len(ex1)):
                    ex2=ex2+ex1[x]
                for x in range(0,len(go1)):
                    go2=go2+go1[x]
                for x in range(0,len(un1)):
                    un2=un2+un1[x]
                '''
            elif province_id!=0 and city_id==0 and store_id==0:
                data_list=SatisfactionData_day.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('excellent_num','good_num','unsatisfy_num','excellent_num_total','good_num_total','unsatisfy_num_total','time','store','city','region','province','device_id').order_by('time')
                '''
                ex=SatisfactionData_day.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('excellent_num').order_by('time')
                go=SatisfactionData_day.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('good_num').order_by('time')
                un=SatisfactionData_day.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('unsatisfy_num').order_by('time')
                for data in ex:
                    ex1.append(float(data['excellent_num']))
                for data1 in go:
                    go1.append(float(data1['good_num']))
                for data2 in un:
                    un1.append(float(data2['unsatisfy_num']))
                for x in range(0,len(ex1)):
                    ex2=ex2+ex1[x]
                for x in range(0,len(go1)):
                    go2=go2+go1[x]
                for x in range(0,len(un1)):
                    un2=un2+un1[x]
                '''
            elif province_id==0 and city_id==0 and store_id==0:
                data_list=SatisfactionData_day.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('excellent_num','good_num','unsatisfy_num','excellent_num_total','good_num_total','unsatisfy_num_total','time','store','city','region','province','device_id').order_by('time')
                '''
                ex=SatisfactionData_day.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('excellent_num').order_by('time')
                go=SatisfactionData_day.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('good_num').order_by('time')
                un=SatisfactionData_day.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('unsatisfy_num').order_by('time')
                for data in ex:
                    ex1.append(float(data['excellent_num']))
                for data1 in go:
                    go1.append(float(data1['good_num']))
                for data2 in un:
                    un1.append(float(data2['unsatisfy_num']))
                for x in range(0,len(ex1)):
                    ex2=ex2+ex1[x]
                for x in range(0,len(go1)):
                    go2=go2+go1[x]
                for x in range(0,len(un1)):
                    un2=un2+un1[x]
                '''
            for data in data_list:
                ex1.append(float(data['excellent_num']))
                go1.append(float(data['good_num']))
                un1.append(float(data['unsatisfy_num']))
            for x in range(0,len(ex1)):
                ex2=ex2+ex1[x]
            for x in range(0,len(go1)):
                go2=go2+go1[x]
            for x in range(0,len(un1)):
                un2=un2+un1[x]
            data_list.update(excellent_num_total=ex2)
            data_list.update(good_num_total=go2)
            data_list.update(unsatisfy_num_total=un2)

            
            data_list_count=data_list.count()
            if not offset:
                offset = 0
            if not limit:
                limit = 20    # 默认是每页20行的内容，与前端默认行数一致
            pageinator = Paginator(data_list, limit)   # 开始做分页

            page = int(int(offset) / int(limit) + 1)    
            response_data = {'total':data_list_count,'rows':[]}   # 必须带有rows和total这2个key，total表示总页数，rows表示每行的内容
            
            for asset in pageinator.page(page):    
                # 下面这些asset_开头的key，都是我们在前端定义好了的，前后端必须一致，前端才能接受到数据并且请求.
                #print ('asset=',asset)
                response_data['rows'].append({
                    #"asset_id": '<a href="/asset/asset_list/%d" target="_blank">%d</a>' %(asset.id,asset.id),   
                    "time" : asset['time'].strftime("%Y-%m-%d ") if asset['time'] else "",
                    "region": asset['region'] if asset['region'] else "",
                    "province": asset['province'] if asset['province'] else "",
                    "city": asset['city'] if asset['city'] else "",
                    "store": asset['store'] if asset['store'] else "",
                    "device_id": asset['device_id'] if asset['device_id'] else "",
                    "excellent_num": asset['excellent_num'] if asset['excellent_num'] else "",
                    "good_num": asset['good_num'] if asset['good_num'] else "",
                    "unsatisfy_num": asset['unsatisfy_num'] if asset['unsatisfy_num'] else "",
                    "excellent_num_total": asset['excellent_num_total'] if asset['excellent_num_total'] else "",
                    "good_num_total": asset['good_num_total'] if asset['good_num_total'] else "",
                    "unsatisfy_num_total": asset['unsatisfy_num_total'] if asset['unsatisfy_num_total'] else "",
                })
            return  HttpResponse(json.dumps(response_data))
            
            
            '''
            if data_list:
                return render(request, "detail_auth_sa.html",
                        {"data_list":data_list,
                        
                         "device_id":deviceid,
                         "execllent":ex2,
                         "good":go2,
                         "unsatisfy":un2,
                         "all_region":all_region,
                         #"num":num,
                         #"region":region_id,
                         #"city":city_id,
                         #"store":store_id,
                         })
            else:
                #data_list=
                return HttpResponse("该时间段无数据")        
            '''
    '''
    def toDicts(objs):
            obj_arr=[]
            for o in objs:
                    obj_arr.append(o.toDict())
            return obj_arr
            
            
    '''

class DetailtableView(View):
    
                    
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
                num5=request.POST.get('detail',"")
      
        if date_from=="":
            return HttpResponse("请重新选择时间")
        if date_to=="":
            return HttpResponse("请重新选择时间")
        #print ("param=",num1,num2,num3,num4)
        #print(date_from,date_to,num5)
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
        sum1=0
        sum1j=0
        sum1p=0
        quantity1j=0
        quantity1p=0
        quantity1=0
        sum=[]
        quantity=[]
        sumj=[]
        quantityj=[]
        sump=[]
        quantityp=[]
        if num5=='1':
            if province_id!=0 and city_id!=0 and store_id!=0:
                data_list=SaleProduct_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('sum_pro','price_pro','sum_total_pro','quantity_total_pro','quantity_pro','time','store','city','region','province','item','classification','device_id','sum_total_proj','quantity_total_proj','sum_total_prop','quantity_total_prop').order_by('time')
                '''
                sum_total_pro=SaleProduct_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('sum_pro').order_by('time')
                quantity_total_pro=SaleProduct_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('quantity_pro').order_by('time')
                #print ("sum_total_pro=",sum_total_pro)
                for data in sum_total_pro:
                    sum.append(data['sum_pro'])
                for data1 in quantity_total_pro:
                    quantity.append(data1['quantity_pro'])
                for x in range(0,len(sum)):
                    sum1=sum1+sum[x]
                for x in range(0,len(quantity)):
                    quantity1=quantity1+quantity[x]
                '''
                sale_desc=Store.objects.filter(name=store_id.values('name')).values('name','desc')
                #print (sale_desc)
            elif province_id!=0 and city_id!=0 and store_id==0:
                data_list=SaleProduct_day.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('sum_pro','price_pro','sum_total_pro','quantity_total_pro','quantity_pro','time','city','region','province','item','classification','device_id','store','sum_total_proj','quantity_total_proj','sum_total_prop','quantity_total_prop').order_by('time')
                '''
                sum_total_pro=SaleProduct_day_city.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('sum_pro').order_by('time')
                quantity_total_pro=SaleProduct_day_city.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('quantity_pro').order_by('time')
                for data in sum_total_pro:
                    sum.append(data['sum_pro'])
                for data1 in quantity_total_pro:
                    quantity.append(data1['quantity_pro'])
                for x in range(0,len(sum)):
                    sum1=sum1+sum[x]
                for x in range(0,len(quantity)):
                    quantity1=quantity1+quantity[x]
                '''
                sale_desc=CityDict.objects.filter(name=city_id.values('name')).values('name','desc')
                #print (data_list)
            elif province_id!=0 and city_id==0 and store_id==0:
                data_list=SaleProduct_day.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('sum_pro','price_pro','sum_total_pro','quantity_total_pro','quantity_pro','time','store','city','region','province','item','device_id','classification','sum_total_proj','quantity_total_proj','sum_total_prop','quantity_total_prop').order_by('time')
                '''
                sum_total_pro=SaleProduct_day_province.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('sum_pro').order_by('time')
                quantity_total_pro=SaleProduct_day_province.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('quantity_pro').order_by('time')
                for data in sum_total_pro:
                    sum.append(data['sum_pro'])
                for data1 in quantity_total_pro:
                    quantity.append(data1['quantity_pro'])
                for x in range(0,len(sum)):
                    sum1=sum1+sum[x]
                for x in range(0,len(quantity)):
                    quantity1=quantity1+quantity[x]
                #print ("data_list=",data_list)
                '''
                sale_desc=ProvinceDict.objects.filter(name=province_id.values('name')).values('name','desc')
            elif province_id==0 and city_id==0 and store_id==0:
                data_list=SaleProduct_day.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('sum_pro','price_pro','sum_total_pro','quantity_total_pro','quantity_pro','time','store','city','region','province','item','classification','device_id','sum_total_proj','quantity_total_proj','sum_total_prop','quantity_total_prop').order_by('time')
                '''
                sum_total_pro=SaleProduct_day_region.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('sum_pro').order_by('time')
                quantity_total_pro=SaleProduct_day_region.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('quantity_pro').order_by('time')
                for data in sum_total_pro:
                    sum.append(data['sum_pro'])
                for data1 in quantity_total_pro:
                    quantity.append(data1['quantity_pro'])
                for x in range(0,len(sum)):
                    sum1=sum1+sum[x]
                for x in range(0,len(quantity)):
                    quantity1=quantity1+quantity[x]
                '''
                sale_desc=RegionDict.objects.filter(name=region_id.values('name')).values('name','desc')
                #print(sale_desc)
            ws =xlwt.Workbook(encoding='utf-8')
            w = ws.add_sheet(u"数据报表第一页")
            w.write(0, 0, u"时间")
            w.write(0, 1, u"区域")
            w.write(0, 2, u"省份")
            w.write(0, 3, u"城市")
            w.write(0, 4, u"区域经销商")
            w.write(0, 5, u"门店")
            w.write(0, 6, u"设备ID")
            w.write(0, 7, u"商品分类")
            w.write(0, 8, u"销售量")
            w.write(0, 9, u"销售额")
            w.write(0, 10, u"火机累计销售量")
            w.write(0, 11, u"火机累计销售额")
            w.write(0, 12, u"配件累计销售量")
            w.write(0, 13, u"配件累计销售额")
            excel_row = 1
            for data in data_list:
                if data['classification']=='火机':
                    sumj.append(data['sum_pro'])
                    quantityj.append(data['quantity_pro'])
                elif data['classification']=='配件':
                    sump.append(data['sum_pro'])
                    quantityp.append(data['quantity_pro'])
            for x in range(0,len(sumj)):
                sum1j=sum1j+round(float(sumj[x]),2)
            for x in range(0,len(sump)):
                sum1p=sum1p+round(float(sump[x]),2)
            for x in range(0,len(quantityj)):
                quantity1j=quantity1j+round(float(quantityj[x]),2)
            for x in range(0,len(quantityp)):
                quantity1p=quantity1p+round(float(quantityp[x]),2)
            data_list.update(sum_total_proj=sum1j)
            data_list.update(quantity_total_proj=quantity1j)
            data_list.update(sum_total_prop=sum1p)
            data_list.update(quantity_total_prop=quantity1p)
            
            
            for data in data_list:
                data_time=data['time'].strftime("%Y-%m-%d ")
                store=data['store']
                #if province_id!=0 and city_id!=0 and store_id!=0:
                #    for sale_data in sale_desc:
                #        desc=sale_data['desc']
                #        print (desc)
                city=data['city']

                province=data['province']
                region=data['region']
                for sale_data in sale_desc:
                    desc=sale_data['desc']
                    #print (desc)
                
                
                
                deviceid=data['device_id']
                classification=data['classification']
                quantity=data['quantity_pro']
                sum=data['sum_pro']
                
                quantity_totalj=data['quantity_total_proj']
                sum_totalj=data['sum_total_proj']
                quantity_totalp=data['quantity_total_prop']
                sum_totalp=data['sum_total_prop']

                w.write(excel_row, 0, data_time)
                w.write(excel_row, 1, region)
                w.write(excel_row, 2, province)
                w.write(excel_row, 3, city)
                w.write(excel_row, 4, desc)
                w.write(excel_row, 5, store)
                w.write(excel_row, 6, deviceid)
                w.write(excel_row, 7, classification)
                w.write(excel_row, 8, quantity)
                w.write(excel_row, 9, sum)
                w.write(excel_row, 10, quantity_totalj)
                w.write(excel_row, 11, sum_totalj)
                w.write(excel_row, 12, quantity_totalp)
                w.write(excel_row, 13, sum_totalp)
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
            data_list=[]
            store_data=[]
            city_data=[]
            region_data=[]
            sum1=0
            quantity1=0
            sum=[]
            quantity=[]
            sumj=[]
            quantityj=[]
            sump=[]
            quantityp=[]
            return HttpResponse("下载成功")
            
            
            
            '''
            if data_list:
                return render(request, "detail_auth.html",
                        {"data_list":data_list,
                         "device_id":deviceid,
                         "sum":sum1,
                         "quantity":quantity1,
                         "all_region":all_region,
                         #"num":num,
                         #"region":region_id,
                         #"city":city_id,
                         #"store":store_id,
                         })
            else:
                #data_list=
                return HttpResponse("该时间段无数据")
            '''
        duration_1=0
        duration_3=0
        
        pd1=[]
        pd3=[]
        if num5=='2':
            if province_id!=0 and city_id!=0 and store_id!=0:
                
                data_list=wifiprobeData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num','wifi_3m_num','wifi_1m_num_total','wifi_3m_num_total','time','device_id','store','city','region','province').order_by('time')
                '''
                people_1=wifiprobeData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num').order_by('time')
                people_3=wifiprobeData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('wifi_3m_num').order_by('time')
                for data in people_1:
                    pd1.append(float(data['wifi_1m_num']))
                #print (pd1)
                for data1 in people_3:
                    pd3.append(float(data1['wifi_3m_num']))
                #print (pd3)
                for x in range(0,len(pd1)):
                    duration_1=duration_1+pd1[x]
                for x in range(0,len(pd3)):
                    duration_3=duration_3+pd3[x]
                '''
                sale_desc=Store.objects.filter(name=store_id.values('name')).values('name','desc')
            elif province_id!=0 and city_id!=0 and store_id==0:
                data_list=wifiprobeData_day.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num','wifi_3m_num','wifi_1m_num_total','wifi_3m_num_total','time','store','city','region','province','device_id','time').order_by('time')
                '''
                people_1=wifiprobeData_day_city.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num').order_by('time')
                people_3=wifiprobeData_day_city.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('wifi_3m_num').order_by('time')
                for data in people_1:
                    pd1.append(float(data['wifi_1m_num']))
                #print (pd1)
                for data1 in people_3:
                    pd3.append(float(data1['wifi_3m_num']))
                #print (pd3)
                for x in range(0,len(pd1)):
                    duration_1=duration_1+pd1[x]
                for x in range(0,len(pd3)):
                    duration_3=duration_3+pd3[x]
                '''
                #print (data_list)
                sale_desc=CityDict.objects.filter(name=city_id.values('name')).values('name','desc')
            elif province_id!=0 and city_id==0 and store_id==0:
                data_list=wifiprobeData_day.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num','wifi_3m_num','wifi_1m_num_total','wifi_3m_num_total','time','store','city','region','province','device_id','time').order_by('time')
                '''
                people_1=wifiprobeData_day_province.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num').order_by('time')
                people_3=wifiprobeData_day_province.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('wifi_3m_num').order_by('time')
                for data in people_1:
                    pd1.append(float(data['wifi_1m_num']))
                #print (pd1)
                for data1 in people_3:
                    pd3.append(float(data1['wifi_3m_num']))
                #print (pd3)
                for x in range(0,len(pd1)):
                    duration_1=duration_1+pd1[x]
                for x in range(0,len(pd3)):
                    duration_3=duration_3+pd3[x]
                '''
                #print (data_list)
                sale_desc=ProvinceDict.objects.filter(name=province_id.values('name')).values('name','desc')
            elif province_id==0 and city_id==0 and store_id==0:
                data_list=wifiprobeData_day.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num','wifi_3m_num','wifi_1m_num_total','wifi_3m_num_total','time','store','city','province','region','device_id','time').order_by('time')
                '''
                people_1=wifiprobeData_day_region.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('wifi_1m_num').order_by('time')
                people_3=wifiprobeData_day_region.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('wifi_3m_num').order_by('time')
                for data in people_1:
                    pd1.append(float(data['wifi_1m_num']))
                #print (pd1)
                for data1 in people_3:
                    pd3.append(float(data1['wifi_3m_num']))
                #print (pd3)
                for x in range(0,len(pd1)):
                    duration_1=duration_1+pd1[x]
                for x in range(0,len(pd3)):
                    duration_3=duration_3+pd3[x]
                '''
                sale_desc=RegionDict.objects.filter(name=region_id.values('name')).values('name','desc')
            ws =xlwt.Workbook(encoding='utf-8')
            w = ws.add_sheet(u"数据报表第一页")
            w.write(0, 0, u"时间")
            w.write(0, 1, u"区域")
            w.write(0, 2, u"省份")
            w.write(0, 3, u"城市")
            w.write(0, 4, u"区域经销商")
            w.write(0, 5, u"门店")
            w.write(0, 6, u"设备ID")
            w.write(0, 7, u"有效客户数")
            w.write(0, 8, u"人流量")
            w.write(0, 9, u"累计有效客户数")
            w.write(0, 10, u"累计人流量")
            excel_row = 1
            
            for data in data_list:
                pd1.append(float(data['wifi_1m_num']))
                pd3.append(float(data['wifi_3m_num']))
                #print (pd3)
            for x in range(0,len(pd1)):
                duration_1=duration_1+pd1[x]
            for x in range(0,len(pd3)):
                duration_3=duration_3+pd3[x]
            
            #print(duration_1)
            data_list.update(wifi_1m_num_total=duration_1)
            data_list.update(wifi_3m_num_total=duration_3)

            
            for data in data_list:
                data_time=data['time'].strftime("%Y-%m-%d ")
                region=data['region']
                province=data['province']
                city=data['city']
                store=data['store']
                for sale_data in sale_desc:
                    desc=sale_data['desc']
                deviceid=data['device_id']
                wifi1=data['wifi_1m_num']
                wifi3=data['wifi_3m_num']
                wifi1_total=data['wifi_1m_num_total']
                wifi3_total=data['wifi_3m_num_total']
                w.write(excel_row, 0, data_time)
                w.write(excel_row, 1, region)
                w.write(excel_row, 2, province)
                w.write(excel_row, 3, city)
                w.write(excel_row, 4, desc)
                w.write(excel_row, 5, store)
                w.write(excel_row, 6, deviceid)
                w.write(excel_row, 7, wifi1)
                w.write(excel_row, 8, wifi3)
                w.write(excel_row, 9, wifi1_total)
                w.write(excel_row, 10, wifi3_total)
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
            #output = stringIOModule.BytesIO()
            
            #file=open('data.xls','rb')
            #output = BytesIO()
            #ws.save(output)
            #output.seek(0)
            #ws.save("data.xls")
            #the_file_name = "data.xls"
            #response = StreamingHttpResponse(file_iterator(the_file_name))
            '''
            response = HttpResponse(content_type='application/vnd.ms-excel')  # 指定返回为excel文件
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=data.xls'
            '''
            #response =FileResponse(file)
            #response = HttpResponse(content_type='application/vnd.ms-excel')  # 指定返回为excel文件
            #response['Content-Type']='application/octet-stream'
            #response['Content-Disposition'] = 'attachment;filename=data.xls'  # 指定返回文件名
            #response.write(output.getvalue())
            
            #return response
            '''
            ws.save(sio)
            sio.seek(0)
            response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=data.xls'
            response.write(sio.getvalue())
            return response
            '''
            
            '''
            if data_list:
                return render(request, "detail_auth_people.html",
                        {"data_list":data_list,
                         "device_id":deviceid,
                         "all_region":all_region,
                         "duration_1":duration_1,
                         "duration_3":duration_3,
                         #"region":region_id,
                         #"city":city_id,
                         #"store":store_id,
                         })
            else:
                #data_list=
                return HttpResponse("该时间段无数据")
            '''
        ex1=[]
        go1=[]
        un1=[]
        ex1_total=[]
        go1_total=[]
        un1_total=[]
        device_id=[]
        ex2=0
        go2=0
        un2=0
        if num5=='3':
            if province_id!=0 and city_id!=0 and store_id!=0:
                data_list=SatisfactionData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('excellent_num','good_num','unsatisfy_num','excellent_num_total','good_num_total','unsatisfy_num_total','time','store','city','region','province','device_id').order_by('time')
                '''
                ex=SatisfactionData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('excellent_num').order_by('time')
                go=SatisfactionData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('good_num').order_by('time')
                un=SatisfactionData_day.objects.filter(store=store_id.values('name'),time__range=(date_from, date_to)).values('unsatisfy_num').order_by('time')
                for data in ex:
                    ex1.append(data['excellent_num'])
                for data1 in go:
                    go1.append(data1['good_num'])
                for data2 in un:
                    un1.append(data2['unsatisfy_num'])
                for x in range(0,len(ex1)):
                    ex2=ex2+ex1[x]
                for x in range(0,len(go1)):
                    go2=go2+go1[x]
                for x in range(0,len(un1)):
                    un2=un2+un1[x]
                '''
                sale_desc=Store.objects.filter(name=store_id.values('name')).values('name','desc')
            elif province_id!=0 and city_id!=0 and store_id==0:
                data_list=SatisfactionData_day.objects.filter(city=city_id.values('name'),time__range=(date_from, date_to)).values('excellent_num','good_num','unsatisfy_num','excellent_num_total','good_num_total','unsatisfy_num_total','time','store','city','region','province','device_id').order_by('time')
                '''
                for device_id in data_list['device_id']:
                        
                    ex=SatisfactionData_day.objects.filter(device_id=device_id,time__range=(date_from, date_to)).values('excellent_num').order_by('time')
                    go=SatisfactionData_day.objects.filter(device_id=device_id,time__range=(date_from, date_to)).values('good_num').order_by('time')
                    un=SatisfactionData_day.objects.filter(device_id=device_id,time__range=(date_from, date_to)).values('unsatisfy_num').order_by('time')
                    for data in ex:
                        ex1.append(data['excellent_num'])
                    for data1 in go:
                        go1.append(data1['good_num'])
                    for data2 in un:
                        un1.append(data2['unsatisfy_num'])
                    for x in range(0,len(ex1)):
                        ex2=ex2+ex1[x]
                    for x in range(0,len(go1)):
                        go2=go2+go1[x]
                    for x in range(0,len(un1)):
                        un2=un2+un1[x]
                '''
                sale_desc=CityDict.objects.filter(name=city_id.values('name')).values('name','desc')
            elif province_id!=0 and city_id==0 and store_id==0:
                data_list=SatisfactionData_day.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('excellent_num','good_num','unsatisfy_num','excellent_num_total','good_num_total','unsatisfy_num_total','time','store','city','region','province','device_id').order_by('time')
                '''
                ex=SatisfactionData_day.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('excellent_num').order_by('time')
                go=SatisfactionData_day.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('good_num').order_by('time')
                un=SatisfactionData_day.objects.filter(province=province_id.values('name'),time__range=(date_from, date_to)).values('unsatisfy_num').order_by('time')
                for data in ex:
                    ex1.append(data['excellent_num'])
                for data1 in go:
                    go1.append(data1['good_num'])
                for data2 in un:
                    un1.append(data2['unsatisfy_num'])
                for x in range(0,len(ex1)):
                    ex2=ex2+ex1[x]
                for x in range(0,len(go1)):
                    go2=go2+go1[x]
                for x in range(0,len(un1)):
                    un2=un2+un1[x]
                '''    
                sale_desc=ProvinceDict.objects.filter(name=province_id.values('name')).values('name','desc')
            elif province_id==0 and city_id==0 and store_id==0:
                data_list=SatisfactionData_day.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('excellent_num','good_num','unsatisfy_num','excellent_num_total','good_num_total','unsatisfy_num_total','time','store','city','region','province','device_id').order_by('time')
                '''
                ex=SatisfactionData_day.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('excellent_num').order_by('time')
                go=SatisfactionData_day.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('good_num').order_by('time')
                un=SatisfactionData_day.objects.filter(region=region_id.values('name'),time__range=(date_from, date_to)).values('unsatisfy_num').order_by('time')
                for data in ex:
                    ex1.append(data['excellent_num'])
                for data1 in go:
                    go1.append(data1['good_num'])
                for data2 in un:
                    un1.append(data2['unsatisfy_num'])
                for x in range(0,len(ex1)):
                    ex2=ex2+ex1[x]
                for x in range(0,len(go1)):
                    go2=go2+go1[x]
                for x in range(0,len(un1)):
                    un2=un2+un1[x]
                '''
                sale_desc=RegionDict.objects.filter(name=region_id.values('name')).values('name','desc')
            ws =xlwt.Workbook(encoding='utf-8')
            w = ws.add_sheet(u"数据报表第一页")
            w.write(0, 0, u"时间")
            w.write(0, 1, u"区域")
            w.write(0, 2, u"省份")
            w.write(0, 3, u"城市")
            w.write(0, 4, u"区域经销商")
            w.write(0, 5, u"门店")
            w.write(0, 6, u"设备ID")
            w.write(0, 7, u"非常满意")
            w.write(0, 8, u"满意")
            w.write(0, 9, u"不满意")
            w.write(0, 10, u"累计非常满意")
            w.write(0, 11, u"累计满意")
            w.write(0, 12, u"累计不满意")
            excel_row = 1
            
            for data in data_list:
                ex1.append(float(data['excellent_num']))
                go1.append(float(data['good_num']))
                un1.append(float(data['unsatisfy_num']))
            for x in range(0,len(ex1)):
                ex2=ex2+ex1[x]
            for x in range(0,len(go1)):
                go2=go2+go1[x]
            for x in range(0,len(un1)):
                un2=un2+un1[x]
            data_list.update(excellent_num_total=ex2)
            data_list.update(good_num_total=go2)
            data_list.update(unsatisfy_num_total=un2)

            
            for data in data_list:
                data_time=data['time'].strftime("%Y-%m-%d ")
                region=data['region']
                province=data['province']
                city=data['city']
                store=data['store']
                for sale_data in sale_desc:
                    desc=sale_data['desc']
                deviceid=data['device_id']
                excellent_num=data['excellent_num']
                good_num=data['good_num']
                unsatisfy_num=data['unsatisfy_num']
                excellent_num_total=data['excellent_num_total']
                good_num_total=data['good_num_total']
                unsatisfy_num_total=data['unsatisfy_num_total']
                w.write(excel_row, 0, data_time)
                w.write(excel_row, 1, region)
                w.write(excel_row, 2, province)
                w.write(excel_row, 3, city)
                w.write(excel_row, 4, desc)
                w.write(excel_row, 5, store)
                w.write(excel_row, 6, deviceid)
                w.write(excel_row, 7, excellent_num)
                w.write(excel_row, 8, good_num)
                w.write(excel_row, 9, unsatisfy_num)
                w.write(excel_row, 10, excellent_num_total)
                w.write(excel_row, 11, good_num_total)
                w.write(excel_row, 12, unsatisfy_num_total)

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
            
            '''
            if data_list:
                return render(request, "detail_auth_sa.html",
                        {"data_list":data_list,
                        
                         "device_id":deviceid,
                         "execllent":ex2,
                         "good":go2,
                         "unsatisfy":un2,
                         "all_region":all_region,
                         #"num":num,
                         #"region":region_id,
                         #"city":city_id,
                         #"store":store_id,
                         })
            else:
                #data_list=
                return HttpResponse("该时间段无数据")        
            '''
    '''
    def toDicts(objs):
            obj_arr=[]
            for o in objs:
                    obj_arr.append(o.toDict())
            return obj_arr
        
        #return render(request, "detail.html",{"all_region":all_region})
        #store = forms.CharField()
    '''

def download(request):
    file=open('data.xls','rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=data.xls'  # 指定返回文件名
    return response
    
    
    
    
    '''
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
        data1=""
        data2=""
        data3=""
        data4=""
        data5=""
        # 热门机构,如果不加负号会是有小到大
        # hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 查找所有门店
        all_store = Store.objects.all()
        
        region_id=request.POST.get('region',"")
        city_id=request.POST.get('city',"")
        store_id=request.POST.get('store',"")
        date_from=request.POST.get('date',"")
        date_to=request.POST.get('date2',"")
        print (region_id,city_id,store_id,date_from,date_to)
        region_select = all_region.filter(name=str(region_id))
        city_select = all_city.filter(name=str(city_id))
        store_select = all_store.filter(name=str(store_id))
        print (region_select,city_select,store_select)
        if region_id and city_id and store_id and date_from and date_to :
            if date_from > date_to:
                return HttpResponse("请重新选择时间")
            elif date_from <= date_to:
                data_list=[]
                data_list=SaleProduct_day.objects.filter(store=store_select.values('name'),time__range=(date_from, date_to)).values('sum_pro','sum_acc','price_pro','sum_total_pro','quantity_total_pro','wifi_1m_num','wifi_3m_num','quantity_pro','quantity_acc','price_acc','sum_total_acc','quantity_total_acc','excellent_num','good_num','unsatisfy_num','time').order_by('time')
                return render(request, "detail.html",
                    {"data_list":data_list,
                     #"num":num,
                     "region":region_id,
                     "city":city_id,
                     "store":store_id,
                     })
        else:
            print ("无权限")
            all_region = RegionDict.objects.all()
            return render(request,"detail.html",{"all_region":all_region})
    def toDicts(objs):
            obj_arr=[]
            for o in objs:
                    obj_arr.append(o.toDict())
            return obj_arr
'''
