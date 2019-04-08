#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import paho.mqtt.client as mqtt 
import paramiko
import time,threading
import RPi.GPIO as GPIO
from time import sleep,ctime

class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
        
    def run(self):
        self.func(*self.args)
        
def update_software():
    global state,config_all_upgrade_path,config_all_init_path,program_all_remote_path,config_all_load_path,led_all_load_path,mov1_all_remote_path,mov2_all_remote_path,mov3_all_remote_path,mov4_all_remote_path,mov5_all_remote_path,program_remote_path,led_remote_path,config_load_path,program_name,config_init_path,config_upgrade_path,mov1_remote_path,mov2_remote_path,mov3_remote_path,mov4_remote_path,mov5_remote_path
    s_remote_path=program_remote_path
    s_local_path="/root/work/"+program_name+".py"
    c_remote_path=config_load_path
    print mov1_remote_path
    c_local_path="/root/work/config_load.txt"
    mov1_local_path="/root/work/001.mpg"
    mov2_local_path="/root/work/002.mpg"
    mov3_local_path="/root/work/003.mpg"
    mov4_local_path="/root/work/004.mpg"
    mov5_local_path="/root/work/005.mpg"
    local_init_path="/root/work/init.jpg"
    local_upgrade_path="/root/work/update_pic.jpg"
    led_local_path="/root/work/config_led.txt"
    
    print "update"
    while True:
        if state==1:
            kill_process_by_name("zippo_demo")
            sftp_down_file(s_remote_path, s_local_path) 
            
            client.publish("/zippo/"+device_id+"/update","software get")
            #os.system("sudo python /root/work/pygametest9.py")
            os.system("reboot") 
            state=0
        
        if state==2:
            kill_process_by_name("zippo_demo")
            sftp_down_file(c_remote_path, c_local_path) 
            client.publish("/zippo/"+device_id+"/update","config get")
            #os.system("sudo python /root/work/pygametest9.py")
            os.system("reboot") 
            state=0  
        
        if state==3:
            kill_process_by_name("zippo_demo")
            sftp_down_file(s_remote_path, s_local_path) 
            sftp_down_file(c_remote_path, c_local_path)
            client.publish("/zippo/"+device_id+"/update","config && software get")
            #os.system("sudo python /root/work/pygametest9.py")
            os.system("reboot") 
            state=0  

        if state==21:
            kill_process_by_name("zippo_demo")
            sftp_down_file(mov1_remote_path, mov1_local_path)
            client.publish("/zippo/"+device_id+"/update","mov1 get")
            os.system("reboot") 
            state=0
        if state==22:
            kill_process_by_name("zippo_demo")
            sftp_down_file(mov2_remote_path, mov2_local_path)
            client.publish("/zippo/"+device_id+"/update","mov2 get")
            os.system("reboot") 
            state=0
        if state==23:
            kill_process_by_name("zippo_demo")
            sftp_down_file(mov3_remote_path, mov3_local_path)
            client.publish("/zippo/"+device_id+"/update","mov3 get")
            os.system("reboot") 
            state=0
        if state==24:
            kill_process_by_name("zippo_demo")
            sftp_down_file(mov4_remote_path, mov4_local_path)
            client.publish("/zippo/"+device_id+"/update","mov4 get")
            os.system("reboot") 
            state=0
        if state==25:
            kill_process_by_name("zippo_demo")
            sftp_down_file(mov5_remote_path, mov5_local_path)
            client.publish("/zippo/"+device_id+"/update","mov5 get")
            os.system("reboot") 
            state=0
        if state==26:
            kill_process_by_name("zippo_demo")
            sftp_down_file(config_init_path, local_init_path)
            client.publish("/zippo/"+device_id+"/update","init get")
            os.system("reboot") 
            state=0
        if state==27:
            kill_process_by_name("zippo_demo")
            sftp_down_file(config_upgrade_path, local_upgrade_path)
            client.publish("/zippo/"+device_id+"/update","update_pic get")
            os.system("reboot") 
            state=0
        if state==28:
            kill_process_by_name("zippo_demo")
            sftp_down_file(led_remote_path, led_local_path)
            client.publish("/zippo/"+device_id+"/update","config_led get")
            os.system("reboot") 
            state=0
        
        if state==4:
            kill_process_by_name("zippo_demo")
            sftp_down_file(mov1_remote_path, mov1_local_path)
            client.publish("/zippo/"+device_id+"/update","mov1 get")
            sftp_down_file(mov2_remote_path, mov2_local_path)
            client.publish("/zippo/"+device_id+"/update","mov2 get") 
            sftp_down_file(mov3_remote_path, mov3_local_path)
            client.publish("/zippo/"+device_id+"/update","mov3 get") 
            sftp_down_file(mov4_remote_path, mov4_local_path)
            client.publish("/zippo/"+device_id+"/update","mov4 get") 
            sftp_down_file(mov5_remote_path, mov5_local_path)
            client.publish("/zippo/"+device_id+"/update","mov5 get") 
            sftp_down_file(config_init_path, local_init_path)
            client.publish("/zippo/"+device_id+"/update","init get")
            sftp_down_file(config_upgrade_path, local_upgrade_path)
            client.publish("/zippo/"+device_id+"/update","update_pic get")
            sftp_down_file(led_remote_path, led_local_path)
            client.publish("/zippo/"+device_id+"/update","all resource get")
            #os.system("sudo python /root/work/pygametest9.py")
            os.system("reboot") 
            state=0 
 
        if state==9:
            kill_process_by_name("zippo_demo")
            #sftp_down_file(c_remote_path, c_local_path) 
            client.publish("/zippo/"+device_id+"/update","system reboot")
            #os.system("sudo python /root/work/pygametest9.py")
            os.system("reboot") 
            state=0   
        if state==11:
           kill_process_by_name("zippo_demo")
           sftp_down_file(mov1_all_remote_path, mov1_local_path)
           client.publish("/zippo/"+device_id+"/update","mov1 get")
           os.system("reboot") 
           state=0
        if state==12:
           kill_process_by_name("zippo_demo")
           sftp_down_file(mov2_all_remote_path, mov2_local_path)
           client.publish("/zippo/"+device_id+"/update","mov2 get") 
           os.system("reboot")
           state=0
        if state==13:
           kill_process_by_name("zippo_demo")
           sftp_down_file(mov3_all_remote_path, mov3_local_path)
           client.publish("/zippo/"+device_id+"/update","mov3 get")
           os.system("reboot")
           state=0
        if state==14:
           kill_process_by_name("zippo_demo")
           sftp_down_file(mov4_all_remote_path, mov4_local_path)
           client.publish("/zippo/"+device_id+"/update","mov4 get")
           os.system("reboot")
           state=0
        if state==15:
           kill_process_by_name("zippo_demo")
           sftp_down_file(mov5_all_remote_path, mov5_local_path)
           client.publish("/zippo/"+device_id+"/update","mov5 get")
           os.system("reboot")
           state=0
        if state==16:
           kill_process_by_name("zippo_demo")
           sftp_down_file(config_all_init_path, local_init_path)
           client.publish("/zippo/"+device_id+"/update","init get")
           os.system("reboot")
           state=0
        if state==17:
           kill_process_by_name("zippo_demo")
           sftp_down_file(config_all_upgrade_path, local_upgrade_path)
           client.publish("/zippo/"+device_id+"/update","update_pic get")
           os.system("reboot")
           state=0
        if state==18:
           kill_process_by_name("zippo_demo")
           sftp_down_file(config_all_load_path, c_local_path)
           client.publish("/zippo/"+device_id+"/update","config_load get")
           os.system("reboot")
           state=0
        if state==19:
           kill_process_by_name("zippo_demo")
           sftp_down_file(led_all_load_path, led_local_path)
           client.publish("/zippo/"+device_id+"/update","config_led get")
           os.system("reboot")
           state=0
        if state==20:
           kill_process_by_name("zippo_demo")
           sftp_down_file(mov1_all_remote_path, mov1_local_path)
           client.publish("/zippo/"+device_id+"/update","mov1 get")
           sftp_down_file(mov2_all_remote_path, mov2_local_path)
           client.publish("/zippo/"+device_id+"/update","mov2 get") 
           sftp_down_file(mov3_all_remote_path, mov3_local_path)
           client.publish("/zippo/"+device_id+"/update","mov3 get")
           sftp_down_file(mov4_all_remote_path, mov4_local_path)
           client.publish("/zippo/"+device_id+"/update","mov4 get")
           sftp_down_file(mov5_all_remote_path, mov5_local_path)
           client.publish("/zippo/"+device_id+"/update","mov5 get")
           sftp_down_file(config_all_init_path, local_init_path)
           client.publish("/zippo/"+device_id+"/update","init get")
           sftp_down_file(config_all_upgrade_path, local_upgrade_path)
           client.publish("/zippo/"+device_id+"/update","update_pic get")
           sftp_down_file(config_all_load_path, c_local_path)
           client.publish("/zippo/"+device_id+"/update","config_load get")
           sftp_down_file(led_all_load_path, led_local_path)
           client.publish("/zippo/"+device_id+"/update","config_led get")
           client.publish("/zippo/"+device_id+"/update","all resource get")
           os.system("reboot")
           state=0

def kill_process_by_name(name):
    cmd = "ps -ef | grep %s" % name
    f = os.popen(cmd)
    txt = f.readlines()
    print txt
    if len(txt) == 0:
        print "no process \"%s\"!!" % name
        return
    else:
       for line in txt:
           colum = line.split()
           print colum
           pid = colum[1]
           print pid
           cmd = "kill -9 %d" % int(pid)
           print cmd
           rc = os.system(cmd)
           if rc == 0 : 
               print "exec \"%s\" success!!" % cmd
           else:
               print "exec \"%s\" failed!!" % cmd
    return                                 		   

def on_connect(client, userdata, flags, rc):  
    global device_id
    print("zippo Connected with result code " + str(rc))  
    print "zippo sub:","/zippo/"+device_id+"/update"
    # 连接完成之后订阅gpio主题  
    #client.subscribe("/b01",0)
    client.subscribe("/zippo/"+device_id+"/update",0)
    client.subscribe("/zippo/all/update",0)

# 消息推送回调函数
def on_message(client, userdata, msg): 
    global state,device_id
    print(msg.topic+" "+str(msg.payload))  
    # 获得负载中的pin 和 value
    str1=msg.topic
    str2=msg.payload
    if msg.topic=="/zippo/"+device_id+"/update":
         if msg.payload=="1":
            state=1
            #print "state=",state
            #client.publish("/zippo/"+device_id+"/update","get code update")
         if msg.payload=="2":
            state=2
            #client.publish("/zippo/"+device_id+"/update","get config update")
         if msg.payload=="3":
            state=3
            #client.publish("/zippo/"+device_id+"/update","get config update")
         if msg.payload=="4":
            state=4
         if msg.payload=="21":
            state=21
         if msg.payload=="22":
            state=22
         if msg.payload=="23":
            state=23
         if msg.payload=="24":
            state=24
         if msg.payload=="25":
            state=25
         if msg.payload=="26":
            state=26
         if msg.payload=="27":
            state=27
         if msg.payload=="28":
            state=28
    if msg.topic=="/zippo/all/update":
        if msg.payload=="1":     #mov1
            state=11
        if msg.payload=="2":     #mov2
            state=12
        if msg.payload=="3":     #mov3
            state=13
        if msg.payload=="4":     #mov4
            state=14
        if msg.payload=="5":     #mov5
            state=15
        if msg.payload=="6":     #init.jpg
            state=16
        if msg.payload=="7":     #upgrade_pic.jpg
            state=17
        if msg.payload=="8":     #config_load.txt
            state=18
        if msg.payload=="9":     #config_led.txt
            state=19
        if msg.payload=="all":   #all resources
            state=20
def sftp_down_file(server_path, local_path):
    global device_id,sftp_host,sftp_password,sftp_port,sftp_timeout,sftp_username,sftp_password
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(sftp_host, sftp_port,sftp_username, sftp_password)
        t = paramiko.Transport((sftp_host, sftp_port))
        t.connect(username=sftp_username, password=sftp_password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
        print "transmit over!"
    except Exception, e:
        print e

def my_callback4(channel):
    global state
    print("button4 pressed!")
    client.publish("/zippo/"+device_id+"/offline","4")
    time.sleep(5)
    os.system("sudo shutdown -h now ")


def main():
    print 'starting at:',ctime()
    
    threads=[]
    t=MyThread(update_software,(),update_software.__name__)
    threads.append(t)
    threads[0].start()
    print 'all DONE at:',ctime()
    
    #os.system("sudo modprobe snd-bcm2835")
    #time.sleep(3)
    #os.system("sudo python /root/work/"+program_name+".py") 
    #print "zippo start"
    try:  
        # 请根据实际情况改变MQTT代理服务器的IP地址  
        client.connect(mqtt_server, mqtt_port,mqtt_timeout)
        state_status=0	
        if state_status==0:
            client.publish("/zippo/"+device_id+"/status",device_id+",2")
            state_status=1	
        client.loop_forever()  
        #os.system("sudo python /root/work/"+program_name+".py")
        #print "zippo start" 
    except KeyboardInterrupt:  
        client.disconnect()  
      
 ###################main##########################
time.sleep(5)
global config_load_path,config_all_upgrade_path,config_all_init_path,program_all_remote_path,config_all_load_path,led_all_load_path,mov1_all_remote_path,mov2_all_remote_path,mov3_all_remote_path,mov4_all_remote_path,mov5_all_remote_path,led_remote_path,config_init_path,config_upgrade_path,mov1_remote_path,mov2_remote_path,mov3_remote_path,mov4_remote_path,mov5_remote_path,program_remote_path,state,client_id,mqtt_server,mqtt_password,mqtt_port,mqtt_timeout,mqtt_username,sftp_host,sftp_password,sftp_port,sftp_timeout,sftp_username,sftp_password,device_id
state=0
current_path=os.path.dirname(__file__)
f=open(os.path.join(current_path,'config_load.txt'))
lines=f.readlines()
f.close()
device_id=lines[1].strip()
client_id=lines[13].strip()
print "zippo:",device_id

mqtt_data=lines[2].strip().split(",")

mqtt_server=mqtt_data[1]
print mqtt_server
mqtt_username=mqtt_data[2]
print mqtt_username
mqtt_password=mqtt_data[3]
print mqtt_password
mqtt_port=int(mqtt_data[4])
print mqtt_port
mqtt_timeout=int(mqtt_data[5])
print mqtt_timeout
sftp_data=lines[3].strip().split(",")
print sftp_data
sftp_host=sftp_data[0]
print sftp_host
sftp_username=sftp_data[1]
print sftp_username
sftp_password=sftp_data[2]
print sftp_password
sftp_port=int(sftp_data[3])
print sftp_port
sftp_timeout=int(sftp_data[4])
print sftp_timeout
led_remote_path=lines[6].strip()
print led_remote_path
program_remote_path=lines[4].strip()
print program_remote_path
config_load_path=lines[5].strip()
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
print config_load_path
program=lines[14].strip().split(".")
program_name=program[0]
print program_name
program_all_remote_path=lines[16].strip()
config_all_load_path=lines[17].strip()
led_all_load_path=lines[18].strip()
mov1_all_remote_path=lines[19].strip()
#print mov1_remote_path
mov2_all_remote_path=lines[20].strip()
#print mov2_remote_path
mov3_all_remote_path=lines[21].strip()
#print mov3_remote_path
mov4_all_remote_path=lines[22].strip()
#print mov4_remote_path
mov5_all_remote_path=lines[23].strip()
#print mov5_remote_path
config_all_init_path=lines[24].strip()
#print config_init_path
config_all_upgrade_path=lines[25].strip()
#print config_upgrade_path

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(5, GPIO.IN)

GPIO.add_event_detect(5, GPIO.FALLING, callback=my_callback4,bouncetime=200)
#client_id=(device_id)
#print client_id
client = mqtt.Client(client_id=client_id)
client.username_pw_set(mqtt_username,mqtt_password)
client.will_set("/zippo/"+device_id+"/status",device_id+",1",0,retain=True)
client.reconnect_delay_set(10,60)
client.on_connect = on_connect  
client.on_message = on_message    
if __name__ == '__main__':
    
    main()
