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



