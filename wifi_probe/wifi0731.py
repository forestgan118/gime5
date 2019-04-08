#!/usr/bin/python
# -*- coding: utf-8 -*-
# File Name:mqtt_chat_client.py
# Python Version:3.5.1


import sys, os, time, signal, importlib

importlib.reload(sys)

import datetime
import string
import paho.mqtt.client as mqtt
#import MySQLdb
import pymysql
import time,threading
from time import sleep,ctime
import schedule
#import logging
#import time
#from logging.handlers import RotatingFileHandler

global unit,mqtt_looping,num_1,mac_list1,mac_time1,duration1,n1,m1,num_3,mac_list3,mac_time3,duration3,n3,m3,mac_wait_5,satisfy_num,good_num,unsatisfy_num,name_wifi,name_satisfy
mac_list1=[]
mac_time1=[]
duration1=[]
mac_list3=[]
mac_time3=[]
duration3=[]
mac_wait_5=[]
num_3=0
num_1=0
n1=0
m1=0
n3=0
m3=0
satisfy_num=[]
good_num=[]
unsatisfy_num=[]
name_wifi=""
name_satisfy=""

i = 1
name=[]
device_id_wifi = []
device_id_info = []
device_id_satify = []
device_id_status=[]
login_name = []
mac = []
ip = []
software_name = []
ver = []
wifi_data_1 = []
wifi_data_3 = []
mac_wifi_list1=[]
satisfy = []
satisfy_data=[]
status=[]
#u = []
d = []
x=0
x2=0
x3=0
x4=0
#actd_num = []
unit = 1000
# time_stamp1 = []
for x in range( 0, unit ):
	device_id_wifi.append( " " )
	device_id_satify.append( " " )
	device_id_info.append(" ")
	device_id_status.append(" ")
	login_name.append( " " )
	mac.append( " " )
	ip.append( " " )
	software_name.append( " " )
	ver.append( " " )
	wifi_data_1.append( 0 )
	wifi_data_3.append(0)
	mac_wifi_list1.append("")
	satisfy.append( "" )
	satisfy_data.append("")
	satisfy_num.append(0)
	good_num.append(0)
	unsatisfy_num.append(0)
	status.append("")
	name.append("")
	#time_stamp1.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))#datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
for x in range(0,unit):    #初始化
	if x<10 :

#		u.append("u0000"+'%d'%x)
		d.append("Z0000"+'%d'%x)
		d.append("z0000"+'%d'%x)

	elif x>=10 and x<100 :

#		u.append("u000"+'%d'%x)
		d.append("Z000"+'%d'%x)
		d.append("z000"+'%d'%x)

	elif x>=100 and x<1000 :

#		u.append("u00"+'%d'%x)
		d.append("Z00"+'%d'%x)
		d.append("z00"+'%d'%x)

	elif x>=1000 and x<10000 :

#		u.append("u0"+'%d'%x)
		d.append("Z0"+'%d'%x)
		d.append("z0"+'%d'%x)

	elif x>=10000 and x<100000 :

#		u.append("u"+'%d'%x)
		d.append("Z"+'%d'%x)
		d.append("z"+'%d'%x)

###########################################


class MyThread(threading.Thread):
	def __init__(self,func,args,name=''):
		threading.Thread.__init__(self)
		self.name=name
		self.func=func
		self.args=args

	def run(self):
		self.func(*self.args)


'''
def func():
    init_log()
    while True:
        #print "output to the console"
        logging.debug("output the debug log")
        logging.info("output the info log")
        time.sleep(3);


def init_log():
    logging.getLogger().setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    # add log ratate
    Rthandler = RotatingFileHandler("backend_run.log", maxBytes=10 * 1024 * 1024, backupCount=100,
                                    encoding="gbk")
    Rthandler.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    logging.getLogger().addHandler(Rthandler)
'''
		
		
def mqtt_client():
	global client,mqtt_looping
	client_id = ("zippo_server")
	client = mqtt.Client(client_id=client_id)    # 可能需要设置ClientId
	client.username_pw_set("gime5", "forestgan")  # 必须设置，否则会返回「Connected with result code 4」
	client.on_connect = on_connect
	client.on_message = on_message
	try:
		#client.connect("47.99.151.116", 1883, 60)
		client.connect("120.78.188.123", 1883, 60)

	except:
		print ("MQTT Broker is not online. Connect later")

	mqtt_looping=True
	print ("Looping")
	while  mqtt_looping:
		client.loop()

		
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	print("connected emqtt")
	for x in range(0,unit):
		client.subscribe("/zippo/"+d[x]+"/wifi",0)
		client.subscribe("/zippo/"+d[x]+"/info",0)
		client.subscribe("/zippo/"+d[x]+"/satisfy",0)
		client.subscribe("/zippo/"+d[x]+"/status",0)

	
def on_message(client, userdata, msg): 
	# 打开数据库连接
	conn = pymysql.connect(
	#host='172.18.41.186',
	host='127.0.0.1',
	port=3306,
	user='root',
	passwd='ghqlxy814118',
	db='zippo',
	charset = 'utf8',  #数据库编码
	)
	global device_id_satify,device_id_wifi,num_1,mac_list1,mac_time1,n1,m1,duration1,num_3,mac_list3,mac_time3,n3,m3,duration3,mac_wait_5,satisfy_num,good_num,unsatisfy_num,name_wifi
	pram1=9
	pram2=9
	duration_time=10
	print(msg.topic+" "+msg.payload.decode("utf-8"))
	topic_str=msg.topic
	txPower=45  #21 45
	str_topic=msg.topic
	x=int(str_topic[9:13])
	if str_topic=="/zippo/"+d[x]+"/info":
		#print(msg.topic+" "+msg.payload.decode("utf-8"))
		payload_str=msg.payload.decode("utf-8")
		#name_info=msg.topic
		str_info=payload_str.split(",")
		name[x]=str_info[0]
		login_name[x]=str_info[1]
		mac[x]=str_info[2]
		ip[x]=str_info[3]
		software_name[x]=str_info[4]
		ver[x]=str_info[5]
		device_id_info[x]=str_info[6]

		cur = conn.cursor()
		time_stamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")# = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  #获取系统当前时间戳，精确到秒
		sql = "insert ignore into "+"device_interactinfo"+"(name,login_name,mac,ip,software_name,ver,utime,device_id) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (name[x],login_name[x],mac[x],ip[x],software_name[x],ver[x],time_stamp,device_id_info[x])
		aa=cur.execute("select * from "+"device_interactinfo")
		try:
			cur.execute(sql)
			conn.commit() #提交到数据库执行，一定要记提交哦
			print("connected MySQLdb")
		except Exception as e:
			conn.rollback() #发生错误时回滚
			print (e)
		x=0

		cur.close()
	
	str2=msg.topic
	x2=int(str2[9:13])
	#print("str2=",str2)
	online_status="off"
	if str2=="/zippo/"+d[x2]+"/status" :
		#print(msg.topic+" "+msg.payload.decode("utf-8"))
		payload_str=msg.payload.decode("utf-8")
		status_str=payload_str.split(",")
		device_id_status[x2]=status_str[0]
		status[x2]=status_str[1]   # 1---zippo.py 下线  2 ----zippo.py 上线    3----zippo_demo.py 下线   4----zippo_demo.py上线
		#print ("device_id_status[x2]=",device_id_status[x2])
		conn = pymysql.connect(
		#host='172.18.41.186',
		host='127.0.0.1',
		port=3306,
		user='root',
		passwd='ghqlxy814118',
		db='zippo',
		charset = 'utf8',  #数据库编码
		)
		
		cur = conn.cursor()
		aa=cur.execute("select * from organization_store where device_id = '"+device_id_status[x2]+"'")
		#print (aa)
		time_stamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")# = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  #获取系统当前时间戳，精确到秒	
		for i in range(aa):
			row=cur.fetchone()#每次取出一行，放到row中，这是一个元组(id,name)
			#print (row)
			storename=row[1]
			cityname=row[9]
			regionname=row[10]
			provincename=row[12]
			#print (storename,cityname,regionname,provincename)
		day_time=datetime.datetime.now()
		if status[x2]=="1":
			pram1=0
			pram2=0
			online_status="off"
			#print(pram1) 
			#print(pram2)
			sql = "insert ignore into "+"device_devicestatus"+"(name,pram1_status,pram2_status,add_time,device_id,online_status,time,store,city,region,province) values('%s','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s')" % (device_id_status[x2],pram1,pram2,time_stamp,device_id_status[x2],online_status,day_time,storename,cityname,regionname,provincename)
			#aa=cur.execute("select * from "+"device_devicestatus")
			try:
				cur.execute(sql)
				conn.commit() #提交到数据库执行，一定要记提交哦
			#	print("connected MySQLdb1")
			except Exception as e:
				conn.rollback() #发生错误时回滚
				print (e)
			x2=0
			cur.close()
        #    software_status="off"
		#elif status[x2]=="1":
		#	pram1=1
		#	software_status="on"
		#elif status[x2]=="2":
		#	pram2=0
		#	software_status="off"
		if status[x2]=="4":
			pram2=1
			pram1=1
			online_status="on"
			#print(pram1) 
			#print(pram2)
			sql = "insert ignore into "+"device_devicestatus"+"(name,pram1_status,pram2_status,add_time,device_id,online_status,time,store,city,region,province) values('%s','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s')" % (device_id_status[x2],pram1,pram2,time_stamp,device_id_status[x2],online_status,day_time,storename,cityname,regionname,provincename)
			#aa=cur.execute("select * from "+"device_devicestatus")
			try:
				cur.execute(sql)
				conn.commit() #提交到数据库执行，一定要记提交哦
			#	print("connected MySQLdb1")
			except Exception as e:
				conn.rollback() #发生错误时回滚
				print (e)
			x2=0
			cur.close()

	str3=msg.topic
	x4=int(str3[9:13])
	if str3=="/zippo/"+d[x4]+"/satisfy":
		#print(msg.topic+" "+msg.payload.decode("utf-8"))
		payload_str=msg.payload.decode("utf-8")
		satisfy_str=payload_str.split(",")
		device_id_satify[x4]=satisfy_str[0]
		satisfy_data[x4]=satisfy_str[1]
		if satisfy_data[x4]=="s":
			satisfy_num[x4]=1
		elif satisfy_data[x4]=="g":
			good_num[x4]=1
		elif satisfy_data[x4]=="u":
			unsatisfy_num[x4]=1
		cur = conn.cursor()
		time_stamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")# = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  #获取系统当前时间戳，精确到秒
		sql = "insert ignore into "+"device_satisfactiondata "+"(name,excellent_num,good_num,unsatisfy_num,add_time,device_id) values('%s','%d','%d','%d','%s','%s')" % (device_id_satify[x4],satisfy_num[x4],good_num[x4],unsatisfy_num[x4],time_stamp,device_id_satify[x4])
		aa=cur.execute("select * from "+"device_satisfactiondata ")
		try:
			cur.execute(sql)
			conn.commit() #提交到数据库执行，一定要记提交哦
		#	print("connected MySQLdb")
		except Exception as e:
			conn.rollback() #发生错误时回滚
			print (e)
		satisfy_num[x4]=0
		good_num[x4]=0
		unsatisfy_num[x4]=0
		x4=0
		cur.close()
			

def main():
	print ('starting at:',ctime())
	threads=[]
	t=MyThread(mqtt_client,(),mqtt_client.__name__)
	threads.append(t)
	#t1=MyThread(func,(),func.__name__)
	#threads.append(t1)
	threads[0].start()
	#threads[1].start()
	print ('all DONE at:',ctime())

if __name__ == '__main__':

	main()



