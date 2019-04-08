#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#AssertionError: group argument must be None for now

import os
import sys
import pygame
import uuid
from urllib2 import urlopen
from pygame.locals import *
import paho.mqtt.client as mqtt 
import time,threading
from json import load
import paramiko
from sys import exit
from time import sleep,ctime
#import subprocess32 as subprocess
from pygame.compat import unicode_
import RPi.GPIO as GPIO
from neopixel import *
#import argparse
#import serial
#import schedule
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
        
    def run(self):
        self.func(*self.args)
		 
def movie_play():
    global mos1_frame1,mos1_frame2,mos2_frame1,mos2_frame2,mos3_frame1,mos3_frame2,mos4_frame1,mos4_frame2,mos5_frame1,mos5_frame2,mos1_num,mos2_num,mos3_num,mos4_num,mos5_num,mos1,mos2,mos3,mos4,mos5,device_id,state,m_remote_path,m_local_path,config_led_path,c_local_path,movie1,movie2,movie3,movie4,movie5,all_frame1,all_frame2,all_frame3,all_frame4,all_frame5,led_state,led1_r,led1_g,led1_b,led2_r,led2_g,led2_b,led3_r,led3_g,led3_b,led4_r,led4_g,led4_b,led5_r,led5_g,led5_b

    #c_remote_path=config_led_path
    #c_local_path=os.path.join(current_path,'config_led.txt')
    mos1_on=1
    mos1_off=1
    mos2_on=1
    mos2_off=1
    mos3_on=1
    mos3_off=1
    mos4_on=1
    mos4_off=1
    mos5_on=1
    mos5_off=1
    while True:
        if ((movie1.get_frame()==all_frame1) and (state==1)):
            movie1.rewind()
            movie1.stop()
            state=2
        if ((movie2.get_frame()==all_frame2) and (state==2)):
            movie2.rewind()
            movie2.stop()
            state=3
        if ((movie3.get_frame()==all_frame3) and (state==3)):
            movie3.rewind()
            movie3.stop()
            state=4
        if ((movie4.get_frame()==all_frame4) and (state==4)):
            movie4.rewind()
            movie4.stop()
            state=5
        if ((movie5.get_frame()==all_frame5) and (state==5)):
            movie5.rewind()
            movie5.stop()
            state=1    
    		 
        if (state==1):
            movie1.play()  #重新播放
            
            if mos1==0:
                GPIO.output(4,GPIO.LOW)
            if mos1==1:
                if (mos1_num!=0):				
                    for x in range(mos1_num):				
                        time1[x]=movie1.get_frame()
                        #print (time1)
                        if (time1[x]==mos1_frame1[x]):
                            if (mos1_on==1):						
                                GPIO.output(4,GPIO.HIGH)
                                #print ("MOS1 ON")
                                mos1_on=0
                                mos1_off=1
                        if (time1[x]==mos1_frame2[x]):
                            if (mos1_off==1):
                                GPIO.output(4,GPIO.LOW)
                                #print ("MOS1 OFF")
                                mos1_off=0
                                mos1_on=1
            colorWipe(strip, Color(led1_r,led1_g, led1_b))  # Red wipe
            #colorWipe(strip1, Color(led1_r1,led1_g1, led1_b1))  # Green wipe        
        elif (state==2):
            movie2.play()  #重新播放
            if mos2==0:
                GPIO.output(4,GPIO.LOW)
            if mos2==1:
                if (mos2_num!=0):				
                    for x in range(mos2_num):				
                        time2[x]=movie2.get_frame()
                        #print (time1)
                        if (time2[x]==mos2_frame1[x]):
                            if (mos2_on==1):						
                                GPIO.output(4,GPIO.HIGH)
                                #print ("MOS2 ON")
                                mos2_on=0
                                mos2_off=1
                        if (time2[x]==mos2_frame2[x]):
                            if (mos2_off==1):
                                GPIO.output(4,GPIO.LOW)
                                #print ("MOS2 OFF")
                                mos2_off=0
                                mos2_on=1
            colorWipe(strip, Color(led2_r,led2_g, led2_b))  # Blue wipe
            #colorWipe(strip1, Color(led2_r1,led2_g1, led2_b1))  # Green wipe        
        elif (state==3):
            movie3.play()  #重新播放
            if mos3==0:
                GPIO.output(4,GPIO.LOW)
            if mos3==1:
                if (mos3_num!=0):				
                    for x in range(mos3_num):				
                        time3[x]=movie3.get_frame()
                        #print (time1)
                        if (time3[x]==mos3_frame1[x]):
                            if (mos3_on==1):						
                                GPIO.output(4,GPIO.HIGH)
                                #print ("MOS3 ON")
                                mos3_on=0
                                mos3_off=1
                        if (time3[x]==mos3_frame2[x]):
                            if (mos3_off==1):
                                GPIO.output(4,GPIO.LOW)
                                #print ("MOS3 OFF")
                                mos3_off=0
                                mos3_on=1
            colorWipe(strip, Color(led3_r,led3_g, led3_b))  # Green wipe
            #colorWipe(strip1, Color(led3_r1,led3_g1, led3_b1))  # Green wipe        
        elif (state==4):
            movie4.play()  #重新播放
            if mos4==0:
                GPIO.output(4,GPIO.LOW)
            if mos4==1:
                if (mos4_num!=0):				
                    for x in range(mos4_num):				
                        time4[x]=movie4.get_frame()
                        #print (time1)
                        if (time4[x]==mos4_frame1[x]):
                            if (mos4_on==1):						
                                GPIO.output(4,GPIO.HIGH)
                                #print ("MOS4 ON")
                                mos4_on=0
                                mos4_off=1
                        if (time4[x]==mos4_frame2[x]):
                            if (mos4_off==1):
                                GPIO.output(4,GPIO.LOW)
                                #print ("MOS4 OFF")
                                mos4_off=0
                                mos4_on=1
            colorWipe(strip, Color(led4_r,led4_g, led4_b))  # Green wipe
            #colorWipe(strip1, Color(led4_r1,led4_g1, led4_b1))  # Green wipe        
        elif (state==5):
            movie5.play()  #重新播放
            if mos5==0:
                GPIO.output(4,GPIO.LOW)
            if mos5==1:
                if (mos5_num!=0):				
                    for x in range(mos5_num):				
                        time5[x]=movie5.get_frame()
                        #print (time1)
                        if (time5[x]==mos5_frame1[x]):
                            if (mos5_on==1):						
                                GPIO.output(4,GPIO.HIGH)
                                #print ("MOS5 ON")
                                mos5_on=0
                                mos5_off=1
                        if (time5[x]==mos5_frame2[x]):
                            if (mos5_off==1):
                                GPIO.output(4,GPIO.LOW)
                                #print ("MOS5 OFF")
                                mos5_off=0
                                mos5_on=1
            colorWipe(strip, Color(led5_r,led5_g, led5_b))  # Green wipe        
            #colorWipe(strip1, Color(led5_r1,led5_g1, led5_b1))  # Green wipe        
        elif (state==100):
            colorWipe(strip, Color(0,0,0))
            #colorWipe(strip1, Color(0,0,0))
            GPIO.output(4,GPIO.LOW)
            pygame.quit()#退出  
            
            sys.exit()
        elif (state==99):
            movie1.stop() 
            movie1.rewind() 
            movie2.stop() 
            movie2.rewind() 
            movie3.stop()
            movie3.rewind()
            movie4.stop()
            movie4.rewind()
            movie5.stop()
            movie5.rewind()
            GPIO.output(4,GPIO.LOW)
            colorWipe(strip, Color(0,0,0))
            #colorWipe(strip1, Color(0,0,0))
            update_pic = pygame.image.load(os.path.join(current_path,'update_pic.jpg')).convert()
            screen.blit(update_pic, (0,0))
            pygame.display.update()
            #print m_remote_path
            sftp_down_file(m_remote_path, m_local_path)
            update_pic = pygame.image.load(os.path.join(current_path,'update_pic.jpg')).convert()
            background = pygame.image.load(os.path.join(current_path,'init.jpg')).convert()
            state=1
            #pygame.quit()#退出  
            os.system("reboot")
def my_callback1(channel):
    global state,device_id
    #print("button1 pressed!")
    client.publish("/zippo/"+device_id+"/satisfy",device_id+",s")
    #state=100
def my_callback2(channel):
    global state,device_id
    #print("button2 pressed!")
    client.publish("/zippo/"+device_id+"/satisfy",device_id+",g")
    #state=100
def my_callback3(channel):
    global state,device_id
    #print("button3 pressed!")
    client.publish("/zippo/"+device_id+"/satisfy",device_id+",u")
    #state=100
    
def my_callback4(channel):
    global state,num_1,num_3,device_id
    #print("button4 pressed!")
    client.publish("/zippo/"+device_id+"/buttonquit","1")
    colorWipe(strip, Color(0,0,0))
    #colorWipe(strip1, Color(0,0,0))
    pygame.quit()#退出  
    sys.exit()

def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])    

def on_connect(client, userdata, flags, rc):  
    #print("Connected with result code " + str(rc))  
    # 连接完成之后订阅gpio主题  
    #client.subscribe("/play",0)
    client.subscribe("/zippo/"+device_id+"/quit",0)
    client.subscribe("/zippo/"+device_id+"/upgrade",0)
    client.subscribe("/zippo/"+device_id+"/update",0)
    client.subscribe("/zippo/"+device_id+"/test",0)
# 消息推送回调函数

def on_message(client, userdata, msg): 
    global state,m_remote_path,m_local_path,mov1_remote_path,mov2_remote_path,mov3_remote_path,mov4_remote_path,mov5_remote_path,config_led_path,config_load_path,program_remote_path,config_init_path,config_upgrade_path
    print(msg.topic+" "+str(msg.payload))  
    # 获得负载中的pin 和 value
    state100=1
    str1=msg.topic
    str2=msg.payload
    if msg.topic=="/zippo/"+device_id+"/upgrade":
        state=99
        if msg.payload=="1":
            m_remote_path=mov1_remote_path
            m_local_path=os.path.join(current_path,'001.mpg')
            
        elif msg.payload=="2":
            m_remote_path=mov2_remote_path
            m_local_path=os.path.join(current_path,'002.mpg') 
            
        elif msg.payload=="3":
            m_remote_path=mov3_remote_path
            m_local_path=os.path.join(current_path,'003.mpg') 
            
        elif msg.payload=="4":
            m_remote_path=mov4_remote_path
            m_local_path=os.path.join(current_path,'004.mpg') 
            
        elif msg.payload=="5":
            m_remote_path=mov5_remote_path
            m_local_path=os.path.join(current_path,'005.mpg') 
        
        elif msg.payload=="0":
            m_remote_path=config_led_path
            m_local_path=os.path.join(current_path,'config_led.txt') 

        elif msg.payload=="6":
            m_remote_path=config_init_path
            m_local_path=os.path.join(current_path,'init.jpg') 

        elif msg.payload=="7":
            m_remote_path=config_upgrade_path
            m_local_path=os.path.join(current_path,'update_pic.jpg') 
                     		
    if msg.topic=="/zippo/"+device_id+"/quit":

        os.system("reboot") 

    if msg.topic=="/zippo/"+device_id+"/update":
        state=100


  
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
        
def sftp_down_file(server_path, local_path):
    global mos1,mos2,mos3,mos4,mos5,device_id,sftp_host,sftp_password,sftp_port,sftp_timeout,sftp_username,sftp_password,state,movie1,movie2,movie3,movie4,movie5,all_frame1,all_frame2,all_frame3,all_frame4,all_frame5,led1_r,led1_g,led1_b,led2_r,led2_g,led2_b,led3_r,led3_g,led3_b,led4_r,led4_g,led4_b,led5_r,led5_g,led5_b,led1_r1,led1_g1,led1_b1,led2_r1,led2_g1,led2_b1,led3_r1,led3_g1,led3_b1,led4_r1,led4_g1,led4_b1,led5_r1,led5_g1,led5_b1
    state_config=0
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(sftp_host, sftp_port, sftp_username,sftp_password)
        t = paramiko.Transport((sftp_host, sftp_port))
        t.connect(username=sftp_username, password=sftp_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
        if (local_path==os.path.join(current_path,'001.mpg')):
            movie1 = pygame.movie.Movie(os.path.join(current_path,'001.mpg'))
            all_frame1=int(movie1.get_length()*25)
            client.publish("/zippo/"+device_id+"/resource","movie1 have download")
            
            # print "transmit over!"
            
        elif (local_path==os.path.join(current_path,'002.mpg')):
            movie2 = pygame.movie.Movie(os.path.join(current_path,'002.mpg'))
            all_frame2=int(movie2.get_length()*25)
            client.publish("/zippo/"+device_id+"/resource","movie2 have download")
            
            
        elif (local_path==os.path.join(current_path,'003.mpg')):
            movie3 = pygame.movie.Movie(os.path.join(current_path,'003.mpg'))
            all_frame3=int(movie3.get_length()*25)
            client.publish("/zippo/"+device_id+"/resource","movie3 have download")
             
        elif (local_path==os.path.join(current_path,'004.mpg')):
            movie4 = pygame.movie.Movie(os.path.join(current_path,'004.mpg'))
            all_frame4=int(movie4.get_length()*25)
            client.publish("/zippo/"+device_id+"/resource","movie4 have download")
        elif (local_path==os.path.join(current_path,'005.mpg')):
            movie5 = pygame.movie.Movie(os.path.join(current_path,'005.mpg'))
            all_frame5=int(movie5.get_length()*25)
            client.publish("/zippo/"+device_id+"/resource","movie5 have download")
             
        elif (local_path==os.path.join(current_path,'init.jpg')):
            background = pygame.image.load(os.path.join(current_path,'init.jpg')).convert()
            client.publish("/zippo/"+device_id+"/resource","init.jpg have download")
             
        elif (local_path==os.path.join(current_path,'update_pic.jpg')):
            update_pic = pygame.image.load(os.path.join(current_path,'update_pic.jpg')).convert()
            client.publish("/zippo/"+device_id+"/resource","update_pic.jpg have download")
            
        elif (local_path==os.path.join(current_path,'config_led.txt')):
            f=open(os.path.join(current_path,'config_led.txt'))
            lines=f.readlines()
            f.close()
            mos=lines[0].split(",")
            mos1=int(mos[0])
            mos2=int(mos[1])
            mos3=int(mos[2])
            mos4=int(mos[3])
            mos5=int(mos[4])
            ledcolor1=lines[1].split(",")
            #print ledcolor1
            led1_r=int(ledcolor1[0])
            #print led1_r
            led1_g=int(ledcolor1[1])
            #print led1_g
            led1_b=int(ledcolor1[2])
            #print led1_b
            ledcolor2=lines[2].split(",")
            #print ledcolor2
            led2_r=int(ledcolor2[0])
            #print led2_r
            led2_g=int(ledcolor2[1])
            #print led2_g
            led2_b=int(ledcolor2[2])
            #print led2_b
            ledcolor3=lines[3].split(",")
            #print ledcolor3
            led3_r=int(ledcolor3[0])
            #print led3_r
            led3_g=int(ledcolor3[1])
            #print led3_g
            led3_b=int(ledcolor3[2])
            #print led3_b
            ledcolor4=lines[4].split(",")
            #print ledcolor4
            led4_r=int(ledcolor4[0])
            #print led4_r
            led4_g=int(ledcolor4[1])
            #print led4_g
            led4_b=int(ledcolor4[2])
            #print led4_b
            ledcolor5=lines[5].split(",")
            #print ledcolor5
            led5_r=int(ledcolor5[0])
            #print led5_r
            led5_g=int(ledcolor5[1])
            #print led5_g
            led5_b=int(ledcolor5[2])
            #print led5_b
            #舞台灯
            '''
            ledcolor21=lines[6].split(",")
            #print ledcolor21
            led1_r1=int(ledcolor21[0])
            #print led1_r1
            led1_g1=int(ledcolor21[1])
            #print led1_g1
            led1_b1=int(ledcolor21[2])
            #print led1_b1
            ledcolor22=lines[7].split(",")
            #print ledcolor22
            led2_r1=int(ledcolor22[0])
            #print led2_r1
            led2_g1=int(ledcolor22[1])
            #print led2_g1
            led2_b1=int(ledcolor22[2])
            #print led2_b1
            ledcolor23=lines[8].split(",")
            #print ledcolor23
            led3_r1=int(ledcolor23[0])
            #print led3_r1
            led3_g1=int(ledcolor23[1])
            #print led3_g1
            led3_b1=int(ledcolor23[2])
            #print led3_b1
            ledcolor24=lines[9].split(",")
            #print ledcolor24
            led4_r1=int(ledcolor24[0])
            #print led4_r1
            led4_g1=int(ledcolor24[1])
            #print led4_g1
            led4_b1=int(ledcolor24[2])
            #print led4_b1
            ledcolor25=lines[10].split(",")
            #print ledcolor25
            led5_r1=int(ledcolor25[0])
            #print led5_r1
            led5_g1=int(ledcolor25[1])
            #print led5_g1
            led5_b1=int(ledcolor25[2])
            #print led5_b1
            '''
            #state=1
            client.publish("/zippo/"+device_id+"/resource","config_led.txt have download")
            #print "download finished"
            
            pass
        else:
            pass			    			
    except Exception, e:
        print e

def main():
    global device_id
    print 'starting at:',ctime()
    #state_status=0
    threads=[]
    t=MyThread(movie_play,(),movie_play.__name__)
    threads.append(t)
    #t2=MyThread(read_data,(),read_data.__name__)
    #threads.append(t2)
    #t3=MyThread(run_task,(),run_task.__name__)
    #threads.append(t3)
    threads[0].start()
    #threads[1].start()
    #threads[2].start()
    print 'all DONE at:',ctime()
    try:  
        # 请根据实际情况改变MQTT代理服务器的IP地址  
        client.connect(mqtt_server, mqtt_port,mqtt_timeout)
        state_status=0	
        if state_status==0:
            my_ip=load(urlopen('https://api.ipify.org/?format=json'))['ip']
            #print 'api.ipify.org',my_ip
            mac=get_mac_address()
            #device_id="z00001"
            #print mac
            info=device_id+","+device_id+","+mac+","+my_ip+","+"zippo_demo.py & zippo.py"+","+"1.0"+","+device_id
            #print info
            client.publish("/zippo/"+device_id+"/info",info)
            time.sleep(1)
            client.publish("/zippo/"+device_id+"/status",device_id+",4")
            #time.sleep(1)
            #client.publish("/zippo/"+device_id+"/status",device_id+",3")
            state_status=1		
        
        client.loop_forever()  
    except KeyboardInterrupt:  
        client.disconnect()  
   
 ###################main##########################
time.sleep(10)
global mos1_frame1,mos1_frame2,mos2_frame1,mos2_frame2,mos3_frame1,mos3_frame2,mos4_frame1,mos4_frame2,mos5_frame1,mos5_frame2,mos1_num,mos2_num,mos3_num,mos4_num,mos5_num,mos1,mos2,mos3,mos4,mos5,mov1_remote_path,mov2_remote_path,mov3_remote_path,mov4_remote_path,mov5_remote_path,config_led_path,config_load_path,config_init_path,config_upgrade_path,program_remote_path,client_id,mqtt_server,mqtt_password,mqtt_port,mqtt_timeout,mqtt_username,sftp_host,sftp_password,sftp_port,sftp_timeout,sftp_username,sftp_password,device_id,m_remote_path,m_local_path,c_remote_path,c_local_path,movie1,movie2,movie3,movie4,movie5,state,all_frame1,all_frame2,all_frame3,all_frame4,all_frame5,led1_r,led1_g,led1_b,led2_r,led2_g,led2_b,led3_r,led3_g,led3_b,led4_r,led4_g,led4_b,led5_r,led5_g,led5_b,led1_r1,led1_g1,led1_b1,led2_r1,led2_g1,led2_b1,led3_r1,led3_g1,led3_b1,led4_r1,led4_g1,led4_b1,led5_r1,led5_g1,led5_b1
os.system("sudo modprobe snd-bcm2835")
state_init=0
current_path=os.path.dirname(__file__)
f=open(os.path.join(current_path,'config_load.txt'))
lines=f.readlines()
f.close()

device_id=lines[1].strip()
#print device_id
mqtt_data=lines[2].split(",")
mqtt_client_id=mqtt_data[0]
#print mqtt_client_id
mqtt_server=mqtt_data[1]
#print mqtt_server
mqtt_username=mqtt_data[2]
#print mqtt_username
mqtt_password=mqtt_data[3]
#print mqtt_password
mqtt_port=int(mqtt_data[4])
#print mqtt_port
mqtt_timeout=int(mqtt_data[5])
#print mqtt_timeout
sftp_data=lines[3].split(",")
#print sftp_data
sftp_host=sftp_data[0]
#print sftp_host
sftp_username=sftp_data[1]
#print sftp_username
sftp_password=sftp_data[2]
#print sftp_password
sftp_port=int(sftp_data[3])
#print sftp_port
sftp_timeout=int(sftp_data[4])
#print sftp_timeout
program_remote_path=lines[4].strip()
#print program_remote_path
config_load_path=lines[5].strip()
#print config_load_path
config_led_path=lines[6].strip()
#print config_led_path
mov1_remote_path=lines[7].strip()
#print mov1_remote_path
mov2_remote_path=lines[8].strip()
#print mov2_remote_path
mov3_remote_path=lines[9].strip()
#print mov3_remote_path
mov4_remote_path=lines[10].strip()
#print mov4_remote_path
mov5_remote_path=lines[11].strip()
#print mov5_remote_path
config_init_path=lines[12].strip()
#print config_init_path
config_upgrade_path=lines[13].strip()
#print config_upgrade_path
f=open(os.path.join(current_path,'config_led.txt'))
lines=f.readlines()
f.close()
mos=lines[0].split(",")
mos1=int(mos[0])
mos2=int(mos[1])
mos3=int(mos[2])
mos4=int(mos[3])
mos5=int(mos[4])
ledcolor1=lines[1].split(",")
#print ledcolor1
led1_r=int(ledcolor1[0])
#print led1_r
led1_g=int(ledcolor1[1])
#print led1_g
led1_b=int(ledcolor1[2])
#print led1_b
ledcolor2=lines[2].split(",")
#print ledcolor2
led2_r=int(ledcolor2[0])
#print led2_r
led2_g=int(ledcolor2[1])
#print led2_g
led2_b=int(ledcolor2[2])
#print led2_b
ledcolor3=lines[3].split(",")
#print ledcolor3
led3_r=int(ledcolor3[0])
#print led3_r
led3_g=int(ledcolor3[1])
#print led3_g
led3_b=int(ledcolor3[2])
#print led3_b
ledcolor4=lines[4].split(",")
#print ledcolor4
led4_r=int(ledcolor4[0])
#print led4_r
led4_g=int(ledcolor4[1])
#print led4_g
led4_b=int(ledcolor4[2])
#print led4_b
ledcolor5=lines[5].split(",")
#print ledcolor5
led5_r=int(ledcolor5[0])
#print led5_r
led5_g=int(ledcolor5[1])
#print led5_g
led5_b=int(ledcolor5[2])
#print led5_b
mos1_data=lines[6].split(",")
mos1_num=int(mos1_data[0])

mos1_frame1=[]
mos1_frame2=[]
time1=[]
if (mos1_num!=0):
    for x in range(0,2*mos1_num,2):
        mos1_frame1.append(int(mos1_data[x+1]))
        mos1_frame2.append(int(mos1_data[x+2]))
        time1.append(0)
mos2_data=lines[7].split(",")
mos2_num=int(mos2_data[0])
mos2_frame1=[]
mos2_frame2=[]
time2=[]
if (mos2_num!=0):
    for x in range(0,2*mos2_num,2):
        mos2_frame1.append(int(mos2_data[x+1]))
        mos2_frame2.append(int(mos2_data[x+2]))
        time2.append(0)

mos3_data=lines[8].split(",")
mos3_num=int(mos3_data[0])
mos3_frame1=[]
mos3_frame2=[]
time3=[]
if (mos3_num!=0):
    for x in range(0,2*mos3_num,2):
        mos3_frame1.append(int(mos3_data[x+1]))
        mos3_frame2.append(int(mos3_data[x+2]))
        time3.append(0)

mos4_data=lines[9].split(",")
mos4_num=int(mos4_data[0])
mos4_frame1=[]
mos4_frame2=[]
time4=[]
if (mos4_num!=0):
    for x in range(0,2*mos4_num,2):
        mos4_frame1.append(int(mos4_data[x+1]))
        mos4_frame2.append(int(mos4_data[x+2]))
        time4.append(0)
mos5_data=lines[10].split(",")
mos5_num=int(mos5_data[0])
mos5_frame1=[]
mos5_frame2=[]
time5=[]
if (mos5_num!=0):
    for x in range(0,2*mos5_num,2):
        mos5_frame1.append(int(mos5_data[x+1]))
        mos5_frame2.append(int(mos5_data[x+2]))
        time5.append(0)

#舞台灯
'''
ledcolor21=lines[6].split(",")
#print ledcolor21
led1_r1=int(ledcolor21[0])
#print led1_r1
led1_g1=int(ledcolor21[1])
#print led1_g1
led1_b1=int(ledcolor21[2])
#print led1_b1
ledcolor22=lines[7].split(",")
#print ledcolor22
led2_r1=int(ledcolor22[0])
#print led2_r1
led2_g1=int(ledcolor22[1])
#print led2_g1
led2_b1=int(ledcolor22[2])
#print led2_b1
ledcolor23=lines[8].split(",")
#print ledcolor23
led3_r1=int(ledcolor23[0])
#print led3_r1
led3_g1=int(ledcolor23[1])
#print led3_g1
led3_b1=int(ledcolor23[2])
#print led3_b1
ledcolor24=lines[9].split(",")
#print ledcolor24
led4_r1=int(ledcolor24[0])
#print led4_r1
led4_g1=int(ledcolor24[1])
#print led4_g1
led4_b1=int(ledcolor24[2])
#print led4_b1
ledcolor25=lines[10].split(",")
#print ledcolor25
led5_r1=int(ledcolor25[0])
#print led5_r1
led5_g1=int(ledcolor25[1])
#print led5_g1
led5_b1=int(ledcolor25[2])
#print led5_b1
'''
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4,GPIO.LOW)   #JP5
GPIO.setup(5, GPIO.IN)
GPIO.setup(6, GPIO.IN)
GPIO.setup(12, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.add_event_detect(5, GPIO.FALLING, callback=my_callback3,bouncetime=200)   #JP
GPIO.add_event_detect(12, GPIO.FALLING, callback=my_callback1,bouncetime=200)   #JP3
GPIO.add_event_detect(6, GPIO.FALLING, callback=my_callback4,bouncetime=200)  #JP2
GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callback2,bouncetime=200)  #JP4
pygame.init()


#c_remote_path="/home/movie/config_led.txt"
c_local_path=os.path.join(current_path,'config_led.txt')
'''
led1_r=255
led1_g=0
led1_b=255
led2_r=255
led2_g=255
led2_b=255
led3_r=0
led3_g=255
led3_b=255
led4_r=255
led4_g=255
led4_b=0
led5_r=255
led5_g=0
led5_b=255
#舞台灯
led1_r1=255
led1_g1=0
led1_b1=255
led2_r1=255
led2_g1=255
led2_b1=255
led3_r1=0
led3_g1=255
led3_b1=255
led4_r1=255
led4_g1=255
led4_b1=0
led5_r1=255
led5_g1=0
led5_b1=255
'''
#screen = pygame.display.set_mode((800, 600),0,32)
screen = pygame.display.set_mode((800, 600),FULLSCREEN,32)
#screen = pygame.display.set_mode((1024, 768),FULLSCREEN,32)
pygame.mouse.set_visible(False)
update_pic = pygame.image.load(os.path.join(current_path,'update_pic.jpg')).convert()
background = pygame.image.load(os.path.join(current_path,'init.jpg')).convert()
while state_init==0:
    screen.blit(background, (0,0))
    pygame.display.update()
    movie1 = pygame.movie.Movie(os.path.join(current_path,'001.mpg'))
    all_frame1=int(movie1.get_length()*25)
    #print all_frame1
    movie2 = pygame.movie.Movie(os.path.join(current_path,'002.mpg'))
    all_frame2=int(movie2.get_length()*25)
    #print all_frame2
    movie3 = pygame.movie.Movie(os.path.join(current_path,'003.mpg'))
    all_frame3=int(movie3.get_length()*25)
    #print all_frame3
    movie4 = pygame.movie.Movie(os.path.join(current_path,'004.mpg'))
    all_frame4=int(movie4.get_length()*25)
    #print all_frame4
    movie5 = pygame.movie.Movie(os.path.join(current_path,'005.mpg'))
    all_frame5=int(movie5.get_length()*25)
    #print all_frame5
    state_init=1

#ser=serial.Serial("/dev/ttyAMA0", 115200)

# LED strip configuration:
LED_COUNT      = 25     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#舞台灯
'''
LED1_COUNT      = 60     # Number of LED pixels.
LED1_PIN        = 19      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED1_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED1_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED1_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED1_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED1_CHANNEL    = 1       # set to '1' for GPIOs 13, 19, 41, 45 or 53
'''
# Process arguments
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
#strip1 = Adafruit_NeoPixel(LED1_COUNT, LED1_PIN, LED1_FREQ_HZ, LED1_DMA, LED1_INVERT, LED1_BRIGHTNESS, LED1_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()
#strip1.begin()
state=1
client_id=(mqtt_client_id)
client = mqtt.Client(client_id=client_id)
client.username_pw_set(mqtt_username,mqtt_password)
client.will_set("/zippo/"+device_id+"/status",device_id+",3",0,retain=True)
client.reconnect_delay_set(10,60)
client.on_connect = on_connect  
client.on_message = on_message    
if __name__ == '__main__':
    
    main()
