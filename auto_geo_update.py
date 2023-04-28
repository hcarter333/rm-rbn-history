import os
import requests
import xml.etree.ElementTree as ET
import json
import sys
import random

#For now, before each usage, the following two enviornment variables must be set
#QRZ_PSWD and MAPS_API_KEY (see auto_gen_update_keys.txt locally)

def get_qrz_session(username):
    qrz_pswd = os.getenv("QRZ_PSWD")
    qrz_pswd = qrz_pswd.replace('"','')
    request_string = 'https://xmldata.qrz.com/xml/?username='+username+';password='+qrz_pswd
    sess = requests.get('https://xmldata.qrz.com/xml/?username='+username+';password='+qrz_pswd)
    root = ET.fromstring(sess.text)
    sess_id = root.find('{http://xmldata.qrz.com}Session/{http://xmldata.qrz.com}Key')
    return sess_id

def get_qrz_call_geo_address(callsign):
    #get the session id
    sess_id = get_qrz_session("KD0FNR")
    #get the address for the callsign
    r = requests.get('https://xmldata.qrz.com/xml/current/?s='+sess_id.text+';callsign='+callsign)
    root = ET.fromstring(r.text)
    #now, get addr1, addr2, and state
    addr1 = root.find('{http://xmldata.qrz.com}Callsign/{http://xmldata.qrz.com}addr1')
    addr2 = root.find('{http://xmldata.qrz.com}Callsign/{http://xmldata.qrz.com}addr2')
    state = root.find('{http://xmldata.qrz.com}Callsign/{http://xmldata.qrz.com}state')
    address_geo = addr1.text + ',' + addr2.text + ',' + state.text
    address_geo = address_geo.replace(' ','+')
    return address_geo

def get_call_lat_lng(callsign):
    geoloc = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+get_qrz_call_geo_address(callsign)+
             '&key='+os.getenv("MAPS_API_KEY"))
    #print(os.getenv("MAPS_API_KEY"))
    #print(geoloc)
    y=json.loads(geoloc.text)

    lat=y["results"][0]["geometry"]["location"]["lat"]
    lng=y["results"][0]["geometry"]["location"]["lng"]
    return str(lng) + ',' + str(lat)

#and then the script goes here?
def dump_rm_rbn_history(lng, lat):
    
    #read in csv file with 
    #call,rx_rst,tx_rst,date_time
    #date format is '%Y/%m/%d %H:%M:%S'
    f = open('qso_update.csv')
    for line in f:
        #for now assume the lines are correctly formatted
        fields = line.split(",")
        #Get the geo location for the call sign
        callsign_loc = get_call_lat_lng(fields[0])
        #table should have
        #id	tx_lng	tx_lat	rx_lng	rx_lat	timestamp	dB	frequency	Spotter
        print(str(random.randrange(0,4294967295)) + ',' + 
              str(lng) + ',' + str(lat) + ',' + callsign_loc + ',' + fields[1] + 
              ',' + fields[3][0:3] + ',14058.4,' + fields[0])
        
    
    



#get session id
#get address for callsign
#format address into plus string
#get coordinates for address


