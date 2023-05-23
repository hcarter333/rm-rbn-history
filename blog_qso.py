from auto_geo_update import get_qrz_call_mail_address
from expe_kml_defs import expe_kml
from qso_spot_kml import qso_spot_kml
import auto_geo_vars
import sys, io
import argparse

def blog_qsos():
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
        #<tr><td>KBTEST</td><td>539</td><td>559</td><td>16:42</td><td>14058.3 kHz</td></tr>
        blog_line = "<tr><td>"
        blog_line = blog_line + fields[0] + "</td><td>" + fields[2]
        blog_line = blog_line + "</td><td>" + fields[3]
        blog_line = blog_line + "</td><td>" + fields[1] + "<td>14058.4</td></tr>"
        print(blog_line)


def blog_qsos_comma_tag():
    #read QSOs to be mapped, fetch geo_location data and return a list of 
    #mappable QSOs sorted by QSO time, earliest to latest
    csv_file='qso_update.csv'
    f = open(csv_file)
    line_num = 0
    tag_line = ""
    for line in f:
        #print('working on ' + line)
        #pull the map title, dexcription, tx station lng and lat from the first 
        #four lines of the qso file respectivevly
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
        tag_line = tag_line + fields[0] + ", "
        
    print(tag_line)

parser = argparse.ArgumentParser(
                    prog='blog_qsos',
                    description='Creates adif log file for POTA',
                    epilog='Text at the bottom of help')

#There are no args because the tx station lng, lat, and the map title 
#are in the first, thrid, and fourth lines of the QSOs file respectively
blog_qsos()
blog_qsos_comma_tag()
