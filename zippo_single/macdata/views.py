from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict
#from apscheduler.schedulers.background import BackgroundScheduler
#from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job 
import json
import logging
import ast
import time
import datetime
from datetime import date
from django.utils.timezone import now, timedelta
import collections
#import schedule
from macdata import models
from macdata.models import DetailInfo, MasterInfo,MasterInfo1,MasterInfo2

from device.models import wifiprobeData_day
from organization.models import Store,RegionDict,CityDict,ProvinceDict

# Create your views here.
class DisableCSRF(object):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

'''
global mac_list3,mac_list1,mac_time1,duration1,num_1,num_3,mac_wait_5
mac_list3 = []
mac_list1 = []
duration1 = []
mac_time1 = []
mac_wait_5 =[]
num_3=0
num_1=0
'''
'''
try:    
    # 实例化调度器  
    scheduler = BackgroundScheduler()  
    # 调度器使用DjangoJobStore()  
    scheduler.add_jobstore(DjangoJobStore(), "default")  
    # 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记  
    # ('scheduler',"interval", seconds=1)  #用interval方式循环，每一秒执行一次  
    #@register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')  
    #@register_job('scheduler',"interval", seconds=1)
    # 调度器开始
    scheduler.start()
      
    scheduler.add_job(time_task, "cron", id=task.name, hour=hour, minute=minute, second=0,misfire_grace_time=30,kwargs={"task": task})
    # 监控任务  
    register_events(scheduler)  
  
 
except Exception as e:  
    print(e)  
    # 报错则调度器停止执行  
    scheduler.shutdown()

def time_task(task):  
        t_now = time.localtime()  
        print(t_now)
'''
'''
#@sched.interval_schedule(seconds=3)  #装饰器，seconds=60意思为该函数为1分钟运行一次
def mac_data():
    #now = datetime.datetime.now()
    now =time.strftime('%Y-%m-%d',time.localtime(time.time())).split('-')
    year=now[0]
    month=now[1]
    day=str(int(now[2]))
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
    #start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
    #print(now)
    master=models.MasterInfo.objects.values()
    for x in master:
        mid.append(x['mid'])
        #data_list.
    #print (mid)
    #num=models.DetailInfo.objects.filter(utime__year=year,utime__month=month,utime__day=day).values("mac","range","mid","utime").count()
    detail_data=models.DetailInfo.objects.filter(utime__year=year,utime__month=month,utime__day=day).values("mac","range","mid","utime").order_by('utime')
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
    

   # print (mac_list1,mid_index)
    #print (mac_list5,maclist5,duration5,wifi_id5,n5)

    for y in range(0,len(n)):
        if n[y] < 3 :
            wifi_id[y]="x"   
    dic = collections.Counter(wifi_id)  #判断3米停留时间小于规定时间的个数

    del dic["x"]   #去掉冗余

    for y in range(0,len(n5)):
        if n5[y] < 3 :
            wifi_id5[y]="x"
    dic5 = collections.Counter(wifi_id5)  #判断3米停留时间小于规定时间的个数

    del dic5["x"]   #去掉冗余

    for key in dic5:
        if key in dic.keys():
            num1=dic[key]
        else:
            num1=0
        wifiprobeData_day.objects.create(device_id=key,wifi_3m_num=dic5[key],wifi_1m_num=num1)  #存入当天数据
        
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
'''

def home(request):
    #global mac_list3,mac_list1,mac_time1,duration1,num_1,num_3
    if request.method == 'POST':
        concat = request.POST
        postBody = request.body
        #indata=json.dumps(postBody.decode())
        #data_dict_str = json.loads(indata)
        #data_dict_str1=data_dict_str[5:]
        #data = ast.literal_eval(data_dict_str1)
        #print(postBody.decode())
        
        try:
            indata=json.dumps(postBody.decode("utf8","ignore"))
            data_dict_str = json.loads(indata)
            data_dict_str1=data_dict_str[5:]
            data = ast.literal_eval(data_dict_str1)
            #print(data.keys())
            start=time.time()
            detail_info_list= []
            
            rate = 0 
            wssid = "" 
            wmac = "" 
            lat	= ""
            lon	= ""
            addr = ""
            utime = ""			
            detailkeys = ""
            masterinfo=""			
            datakeys=data.keys() 
            if 'rate' in datakeys:
                rate = data['rate'] 
            if 'wssid' in datakeys:
                wssid = data['wssid']
            if 'wmac' in datakeys:
                wmac = data['wmac']
            if 'lat' in datakeys: 
                lat  = data['lat']
            if 'lon' in datakeys: 
                lon  = data['lon']
            if 'addr' in datakeys: 
                addr = data['addr']
            if 'time' in datakeys: 
                utime = data['time']
            #print (data.keys()) 
            #print ('wssid value is') 
            #print (wssid)
            master_info = Master_Info(data["id"],data['mmac'],rate,wssid,wmac,lat,lon,addr)
            masterinfo=master_info.split(",")
            
            for e in data["data"]: 
                ts = ""
                tmc	= ""
                tc	= ""
                ds	= "" 
                essid0 = ""
                essid1 = "" 
                essid2 = "" 
                essid3 = ""
                essid4 = ""
                essid5 = "" 
                essid6 = "" 
                range = ""
                detailkeys = e.keys()
                #print (e.keys())				
                if 'ts' in detailkeys:
                    ts = "" #e['ts']
                if 'tmc' in detailkeys: 
                    tmc = "" #e['tmc']
                if 'tc' in detailkeys: 
                    tc = "" #e['tc']
                if 'ds' in detailkeys: 
                    ds = "" #e['ds']
                if 'essid0' in detailkeys: 
                    essid0 = ""#e['essid0']
                if 'essid1' in detailkeys: 
                    essid1 = ""#e['essid1']
                if 'essid2' in detailkeys: 
                    essid2 = "" #e['essid2']
                if 'essid3' in detailkeys: 
                    essid3 = ""#e['essid3']
                if 'essid4' in detailkeys: 
                    essid4 = ""#e['essid4']
                if 'essid5' in detailkeys: 
                    essid5 = ""#e['essid5']
                if 'essid6' in detailkeys: 
                    essid6 = ""#e['essid6']
                if 'range' in detailkeys: 
                    range = e['range']
                #print (e["mac"],e["rssi"],range,ts,tmc,tc,ds)
                detail_info = Detail_Info(e["mac"],e["rssi"],range,ts,tmc,tc,ds,essid0,essid1,essid2,essid3,essid4,essid5,essid6) 
                if detail_info!="":
                    detail_info_list.append(detail_info)
            #print (detail_info_list)
            #save_master(master_info)
            save_detail(detail_info_list,master_info)			
            #mslove_data =slove_data() 
            #mslove_data.save_data(master_info, detail_info_list) 
            end = time.time()
            #logging.info(u'end request totol time: %d',int(end-start)) 
        except:
            import sys
            ExecInfo = sys.exc_info() 
            logging.error(ExecInfo[1]) 
            raise Exception(ExecInfo[1])
        
        resp='ok'
        resperr='error'
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps(resperr), content_type="application/json")

def Master_Info(id,mmac,rate,wssid,wmac,lat,lon,addr):
    data_master=""
    data_master=id+","+mmac #+","+rate+","+wssid+","+wmac+","+lat+","+lon+","+addr
    utime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    day_time=now().date() + timedelta(days=0)
    all_master = MasterInfo.objects.all()
    all_master1 = MasterInfo1.objects.all()
    all_master2 = MasterInfo2.objects.all()
    #print ("all_master=",all_master)
    storedata=Store.objects.filter(wifi_id=id).values("name","cityname","provincename","regionname","device_id")
    #print(storedata)
    for data in storedata:
        storewifi=data['name']
        city=data['cityname']
        province=data['provincename']
        region=data['regionname']
        device_id=data['device_id']
    mac=all_master.filter(mmac=mmac).values("mmac")
    mac1=all_master1.filter(mmac=mmac,time=day_time).values("mmac")
    mac2=all_master2.filter(mid=id,time=day_time).values("mid")
    print (storewifi)
    if len(mac2) == 0 :
        models.MasterInfo2.objects.create(mmac=mmac,mid=id,utime=utime,store=storewifi,city=city,province=province,region=region,time=day_time,device_id=device_id)
        print("get3")
    elif len(mac2) > 0 :
        #models.MasterInfo2.objects.update(mmac=mmac,mid=id,utime=utime,store=storewifi,city=city,province=province,region=region,time=day_time,device_id=device_id))
        print ("get2")
    if len(mac) == 0 :
        models.MasterInfo.objects.create(mmac=mmac,mid=id,rate=rate,wssid=wssid,wmac=wmac,lat=lat,lon=lon,addr=addr,utime=utime,store=storewifi,city=city,province=province,region=region,time=day_time,device_id=device_id)
        print ("get")
    if len(mac1)== 0:
        models.MasterInfo1.objects.create(mmac=mmac,mid=id,rate=rate,wssid=wssid,wmac=wmac,lat=lat,lon=lon,addr=addr,utime=utime,store=storewifi,city=city,province=province,region=region,time=day_time,device_id=device_id)
        print ("get1")
    return data_master

def Detail_Info(mac,rssi,range,ts,tmc,tc,ds,essid0,essid1,essid2,essid3,essid4,essid5,essid6):
    #global mac_list3,mac_list1,mac_time1,duration1,num_1,num_3,mac_wait_5
    #duration_time=10	
    data_detail=""
    range=str(round(rssi_distance(int(rssi)),2))
    if float(range)<5:
        data_detail=mac+","+rssi+","+range+","+ts+","+tmc+","+tc+","+ds+","+essid0+","+essid1+","+essid2+","+essid3+","+essid4+","+essid5+","+essid6	
        '''
        if float(range) <= 3.5 and float(range) > 1.5:
            if mac not in mac_list3:
                mac_list3.append(mac)
                #print (mac_list3)
                num_3=num_3+1
        elif float(range) > 3.5:			#走出5米探测范围，将数据移除
            if mac in mac_list3:
                n3=mac_list3.index(mac)
                del(mac_list3[n3])  #mac 移动出5米，从列表中删除
                num_3=num_3-1
        elif float(range) <= 1.5:
            if mac not in mac_list1:
                mac_list1.append(mac)
                mac_time1.append(time.time())   #在探测范围内的最新时间
                duration1.append(0)   #停留时间
            elif mac in mac_list1:    #如果mac还在探测范围内，
                m1=mac_list1.index(mac)     #找出mac位置
                duration1[m1]=float('% 0.2f' % (time.time()-mac_time1[m1]))+duration1[m1]  #计算停留时间
                mac_time1[m1]=time.time()    #更新最新时间
                if duration1[m1]>=duration_time:
                    if mac not in mac_wait_5:
                        mac_wait_5.append(mac)
                        #print (mac_wait_5)
                        num_1=num_1+1
                        
        elif float(range) > 1.5:			#走出1米探测范围，将数据移除
            if mac in mac_list1:
                n1=mac_list1.index(mac)
                del(mac_list1[n1])  #mac 移动出1米，从列表中删除
                del(mac_time1[n1])    # 同时删除该mac的时间
                del(duration1[n1])
                del(mac_wait_5)
                num_1=num_1-1
        #print (mac_list1)
        #print (duration1)
        print (num_1)
        '''
    else:
        data_detail=""	
    #print (data_detail)
    return data_detail

#def save_master(master_info):


def save_detail(detail_info_list,master_info):
    datalist=detail_info_list
    master=master_info
    obj_master=master.split(",")
    for data in datalist:
        #print (data)
        obj_rev=data.split(",")
        models.DetailInfo.objects.create(mac=obj_rev[0],rssi=obj_rev[1],range=obj_rev[2],ts=obj_rev[3],tmc=obj_rev[4],tc=obj_rev[5],ds=obj_rev[6],essid0=obj_rev[7],essid1=obj_rev[8],essid2=obj_rev[9],essid3=obj_rev[10],essid4=obj_rev[11],essid5=obj_rev[12],essid6=obj_rev[13],mid=obj_master[0],mmac=obj_master[1])
        '''	
        detail_data.mac=obj_rev[0]
        detail_data.rssi=obj_rev[1]
        detail_data.range=obj_rev[2]
        detail_data.ts=obj_rev[3]
        detail_data.tmc=obj_rev[4]
        detail_data.tc=obj_rev[5]
        detail_data.ds=obj_rev[6]
        detail_data.essid0=obj_rev[7]
        detail_data.essid1=obj_rev[8]
        detail_data.essid2=obj_rev[9]
        detail_data.essid3=obj_rev[10]
        detail_data.essid4=obj_rev[11]
        detail_data.essid5=obj_rev[12]
        detail_data.essid6=obj_rev[13]		
        detail_data.save()
        '''

def rssi_distance(rssi):
    txPower=30
    refDistance = 1.0
    pathLoss = 4.0
    c1=txPower
    c2=pathLoss
    fm=(c1-rssi)/(10*c2)
    fp=pow(10,fm)
    distance=refDistance*fp/100

    return distance
'''
def task_day():
    detaildata=DetailInfo.objects.filter(mid="001ec387").values("mac","range","utime")
    for data in detaildata:
        print(detaildata)
    #mid=detaildata.mid()

def run_task():
	#schedule.every(5).seconds.do(task_3)
	#schedule.every(30).minutes.do(wifiprobe_30)   #30分钟统计一次实时人流量
	schedule.every(3).seconds.do(task_day)   #30分钟统计一次实时人流量
	#schedule.every(10).minutes.do(job)
	#schedule.every().hour.do(job)
	#schedule.every(1).day.at("1:44").do(task_day)
	#schedule.every().monday.do(job)
	#schedule.every().wednesday.at("13:15").do(job)
	while True:
		schedule.run_pending()
		time.sleep(1)
'''