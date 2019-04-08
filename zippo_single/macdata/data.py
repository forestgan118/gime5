# _*_ coding:utf-8 _*_ import json
import time
from model.data_model import * from flask import Blueprint,request
from dao.slove_dataimport slove_data import logging
recv_data_route = Blueprint('recv_data', name ) @recv_data_route.route('/dsky',methods=['GET','POST']) def recv_data():
try:
start = time.time()
para = request.values.get('data'); data = json.loads(para) detail_info_list= []
rate = 0 wssid = "" wmac		= "" lat	= ""
lon	= ""
addr	= "" detailkeys = "" datakeys=data.keys() if 'rate' in datakeys:
rate = data['rate'] if 'wssid' in datakeys:
wssid = data['wssid']




if 'wmac' in datakeys: wmac = data['wmac']
if 'lat' in datakeys: lat  = data['lat']
if 'lon' in datakeys: lon  = data['lon']
if 'addr' in datakeys: addr = data['addr']
print data.keys() print 'wssid value is' print wssid
master_info = Master_Info(data["id"],
data['mmac'], rate,
wssid, wmac,
lat, lon, addr)
for e in	data["data"]: ts = ""
tmc	= ""
tc	= ""
ds	= "" essid1 = "" essid2 = "" essid3 = ""
essid4 = ""




essid5 = "" essid6 = "" range = ""
detailkeys = e.keys() if 'ts' in detailkeys:
ts = e['ts']
if 'tmc' in detailkeys: tmc = e['tmc']
if 'tc' in detailkeys: tc = e['tc']
if 'ds' in detailkeys: ds = e['ds']
if 'essid1' in detailkeys: essid1 = e['essid1']
if 'essid2' in detailkeys: essid2 = e['essid2']
if 'essid3' in detailkeys: essid3 = e['essid3']
if 'essid4' in detailkeys: essid4 = e['essid4']
if 'essid5' in detailkeys: essid5 = e['essid5']
if 'essid6' in detailkeys: essid6 = e['essid6']
if 'range' in detailkeys: range = e['range']
detail_info = Detail_Info(e["mac"],
e["rssi"],




range, ts, tmc, tc,
ds,essid1,essid2,essid3,essid4,essid5,essid6) detail_info_list.append(detail_info)

mslove_data =slove_data() mslove_data.save_data(master_info, detail_info_list) end = time.time()
logging.info(u'end request totol time: %d',int(end-start)) except:
import sys
ExecInfo = sys.exc_info() logging.error(ExecInfo[1]) raise Exception(ExecInfo[1])
return "Done"