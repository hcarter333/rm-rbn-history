from auto_geo_update import get_qrz_call_mail_address
from expe_kml_defs import expe_kml
from qso_spot_kml import qso_spot_kml
import auto_geo_vars
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, newline='\n' )

def mail_qsls():
    #read QSOs to be mapped, fetch geo_location data and return a list of 
    #mappable QSOs sorted by QSO time, earliest to latest
    csv_file='qso_update.csv'
    f = open(csv_file)
    line_num = 0
    sys.stdout.write("Call,Date,Time,rx RST,tx RST,QSL Address\r\n")
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
        get_qrz_call_mail_address(fields[0],dt[0],dt[1],fields[2],fields[3])
        sys.stdout.write("\r")
        sys.stdout.write("\n")
    #creates a list of QSO formatted the same as rm_rnb_histor_pres.csv
    #then, gathers up spotting entries from the same file, and returns a list
    #of strings formatted as lines in the file that are passed on 
    #to qso_spot_kml to produce a kml map

#There are no args because the tx station lng, lat, and the map title 
#are in the first three lines of the QSOs file respectively
mail_qsls()

