from auto_geo_update import get_qrz_call_mail_address
from expe_kml_defs import expe_kml
from qso_spot_kml import qso_spot_kml
import auto_geo_vars
import sys, io
import argparse

def pota_qsos(park_code):
    #read QSOs to be mapped, fetch geo_location data and return a list of 
    #mappable QSOs sorted by QSO time, earliest to latest
    csv_file='qso_update.csv'
    f = open(csv_file)
    line_num = 0
    for line in f:
        #print('working on ' + line)
        #pull the map title, tx station lng and lat from the first 
        #three lines of the qso file respectivevly
        if(line_num == 0):
            auto_geo_vars.kml_title = line.replace("\n", "")
            line_num = line_num + 1
            continue
        if(line_num == 1):
            auto_geo_vars.kml_desc = line.replace("\\n", "\n")
            line_num = line_num + 1
            continue
        if(line_num == 2):
            auto_geo_vars.tx_lng = float(line.replace("\n", ""))
            lng = auto_geo_vars.tx_lng
            line_num = line_num + 1
            continue
        if(line_num == 3):
            auto_geo_vars.tx_lat = float(line.replace("\n", ""))
            lat = auto_geo_vars.tx_lat
            line_num = line_num + 1
            continue
        fields = line.split(",")
        fields[3] = fields[3].replace("\n","")
        dt = fields[1].split(" ")
        pota_line = "<station_callsign:6>KD0FNR"
        pota_line = pota_line + "<Call:" + str(len(fields[0])) + ">" + fields[0]
        pota_line = pota_line + "<QSO_DATE:8>" + dt[0].replace("/","")
        pota_line = pota_line + "<TIME_ON:4>" + (dt[1].replace(":",""))[0:4]
        pota_line = pota_line + "<BAND:3>20M<MODE:2>CW<MY_SIG:4>POTA"
        pota_line = pota_line + "<MY_SIG_INFO:" + str(len(park_code)) + ">"
        pota_line = pota_line + park_code + "<eor>"
        print(pota_line)

parser = argparse.ArgumentParser(
                    prog='pota_qsos',
                    description='Creates adif log file for POTA',
                    epilog='Text at the bottom of help')
parser.add_argument('-k', dest="park_code", required=True)
args = parser.parse_args()

#There are no args because the tx station lng, lat, and the map title 
#are in the first three lines of the QSOs file respectively
pota_qsos(args.park_code)
