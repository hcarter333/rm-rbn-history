import os
import requests
import xml.etree.ElementTree as ET
import json


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
    print(os.getenv("MAPS_API_KEY"))
    print(geoloc)
    y=json.loads(geoloc.text)

    lat=y["results"][0]["geometry"]["location"]["lat"]
    lng=y["results"][0]["geometry"]["location"]["lng"]
    return str(lat) + ',' + str(lng)

#get session id
#read in csv file with 
#call,rx_rst,tx_rst,date_time
#get address for callsign
#format address into plus string
#get coordinates for address


