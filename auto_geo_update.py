import os
import requests
import xml.etree.ElementTree as ET
import json
import sys
import random
import datetime
import auto_geo_vars

#For now, before each usage, the following two enviornment variables must be set
#QRZ_PSWD and MAPS_API_KEY (see auto_gen_update_keys.txt locally)

def get_qrz_session(username):
    if(auto_geo_vars.qrz_sess == "none"):
        qrz_pswd = os.getenv("QRZ_PSWD")
        qrz_pswd = qrz_pswd.replace('"','')
        request_string = 'https://xmldata.qrz.com/xml/?username='+username+';password='+qrz_pswd
        sess = requests.get('https://xmldata.qrz.com/xml/?username='+username+';password='+qrz_pswd)
        root = ET.fromstring(sess.text)
        sess_id = root.find('{http://xmldata.qrz.com}Session/{http://xmldata.qrz.com}Key')
        auto_geo_vars.qrz_sess = sess_id
    else:
        sess_id = auto_geo_vars.qrz_sess
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

def get_qrz_call_mail_address(callsign,date,time,rx_rst,tx_rst):
    #get the session id
    sess_id = get_qrz_session("KD0FNR")
    #get the address for the callsign
    r = requests.get('https://xmldata.qrz.com/xml/current/?s='+sess_id.text+';callsign='+callsign)
    root = ET.fromstring(r.text)
    #now, get addr1, addr2, and state
    fname = root.find('{http://xmldata.qrz.com}Callsign/{http://xmldata.qrz.com}fname')
    name = root.find('{http://xmldata.qrz.com}Callsign/{http://xmldata.qrz.com}name')
    addr1 = root.find('{http://xmldata.qrz.com}Callsign/{http://xmldata.qrz.com}addr1')
    addr2 = root.find('{http://xmldata.qrz.com}Callsign/{http://xmldata.qrz.com}addr2')
    state = root.find('{http://xmldata.qrz.com}Callsign/{http://xmldata.qrz.com}state')
    zip_code = root.find('{http://xmldata.qrz.com}Callsign/{http://xmldata.qrz.com}zip')
    address_mail = '"' + callsign + '\n' + fname.text + ' ' + name.text + '\n' + addr1.text +\
                   '\n' + addr2.text + ',' + state.text + ' ' + zip_code.text + '"'
    out_string = callsign + ',' + date + ',"' + time + '",' + rx_rst + ',' + tx_rst + ',' + address_mail
    sys.stdout.write(out_string)
    return out_string

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
def dump_rm_rbn_history(csv_file=''):
    
    #read in csv file with 
    #call,date_time,rx_rst,tx_rst
    #date format is '%Y/%m/%d %H:%M:%S'
    #list to store QSOs in
    qso_list = []
    if(csv_file==''):
        csv_file='qso_update.csv'
    f = open(csv_file)
    line_num = 0
    for line in f:
        #pull the map title, tx station lng and lat from the first 
        #three lines of the qso file respectivevly
        if(line_num == 0):
            auto_geo_vars.kml_title = line.replace("\n", "")
            line_num = line_num + 1
            continue
        if(line_num == 1):
            auto_geo_vars.tx_lng = float(line.replace("\n", ""))
            lng = auto_geo_vars.tx_lng
            line_num = line_num + 1
            continue
        if(line_num == 2):
            auto_geo_vars.tx_lat = float(line.replace("\n", ""))
            lat = auto_geo_vars.tx_lat
            line_num = line_num + 1
            continue
        #for now assume the lines are correctly formatted
        fields = line.split(",")
        #Get the geo location for the call sign
        callsign_loc = get_call_lat_lng(fields[0])
        #get the QSO date and time for sorting
        qso_dt = datetime.datetime.strptime(fields[1], "%Y/%m/%d %H:%M:%S")
        #store the qso in a tuple
        qso_tuple = str(random.randrange(0,4294967295)),lng,lat,callsign_loc,\
                    qso_dt,fields[3][0:3],fields[0]
        qso_list.append(qso_tuple)
        #table should have
        #id	tx_lng	tx_lat	rx_lng	rx_lat	timestamp	dB	frequency	Spotter
#        print(str(random.randrange(0,4294967295)) + ',' + 
#              str(lng) + ',' + str(lat) + ',' + callsign_loc + ',' + fields[1] + 
#              ',' + fields[3][0:3] + ',14058.4,' + fields[0])
    result = sorted(qso_list, key=lambda x: x[4])
    for qso in result:
        result_string = qso[0] + ',' + str(qso[1]) + ',' + str(qso[2]) + ',' \
              + qso[3] + ',' + qso[4].strftime("%Y/%m/%d %H:%M:%S") + ',' + \
              qso[5] + ',14058.4,' + qso[6]
        #print(result_string)
    return result
        
    
    



#get session id
#get address for callsign
#format address into plus string
#get coordinates for address


