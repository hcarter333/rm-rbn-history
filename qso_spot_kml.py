import sys
import random
import re

#keep track of spotting stations to avoid duplicates
already_spotted = {}
signal_colors = {"1": "#ff004b96",
                 "0": "#ff004b96",
                 "2": "#ff0000ff",
                 "3": "#ff00a5ff",
                 "4": "#ff00ffff",
                 "5": "#ff00ff00",
                 "6": "#ffff0000",
                 "7": "#ff82004b",
                 "8": "#ffff007f",
                 "9": "#ffffffff",
                 }

def db_to_s(db):
    test_db = int(db)
    if(test_db > 32):
        return "9"
    if(test_db > 27):
        return "8"
    if(test_db > 21):
        return "7"
    if(test_db > 15):
        return "6"
    if(test_db > 8):
        return "5"
    if(test_db > 2):
        return "4"
    if(test_db >= 1):
        return "3"


#Read each line in the qso_file
#format it as as kml and write it to stdout using print
#generate random 32 bit key
def qso_spot_kml(qso_file, key=77, qso_list=[], map_title=""):
    test_lines = 0
    if(len(qso_list) == 0):
        f = open(qso_file)
    #output the standard header
    if(map_title == ""):
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<kml xmlns="http://earth.google.com/kml/2.0"> <Document><name>pota_title</name>')
    else:
        #open the output file
        map_file = map_title.replace(" ", "_")
        map_file = map_file.replace("-", "_")
        map_file = map_file.replace("!", "_")
        print("debug: map_file = " + map_file)
        stdout_fileno = sys.stdout
        sys.stdout = open(map_file + ".kml", 'w')
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<kml xmlns="http://earth.google.com/kml/2.0"> <Document><name>' + map_title + \
              '</name>')
    #output the styles for this map
    print_map_style()
    if(len(qso_list) == 0):
        for line in f:
            if(transfom_qso_to_kml(line) == -1):
                sys.exit("qso input has incorrect format, see message above")
    else:
        for line in qso_list:
            test_lines = test_lines + 1
            if(transfom_qso_to_kml(line) == -1):
                sys.exit("qso input has incorrect format, see message above")
    #output file footer
    print('</Document> </kml>')
    #put stdout back where we found it
    if(map_title!=""):
        sys.stdout = stdout_fileno
    return test_lines


def transfom_qso_to_kml(qso_line):
    placestart = "<Placemark>"
    linestart = "<LineString><coordinates>"
    lineend = "</coordinates></LineString>"
    qso_style = "<Style><LineStyle><color>line_color</color><width>4</width></LineStyle></Style>"
    qso_style_no_rst = "<Style><LineStyle><color>line_color</color><width>4</width></LineStyle></Style>"
    spot_style = "<Style><LineStyle><color>line_color</color><width>4</width></LineStyle></Style>"
    QSO_deets_style_table = '<description><![CDATA[<table border="0" cellpadding="0" cellspacing="0" width="322" style="border-collapse: collapse; width: 242pt;">'
    QSO_deets_style_colgroup = '<colgroup><col width="73" style="width: 55pt;"><col width="87" style="width: 65pt;">\
        <col width="81" span="2" style="width: 61pt;"></colgroup><tbody>'
    QSO_deets_row = '<tr height="81" style="height: 60.75pt;">\
        <td height="81" class="xl63" width="73" style="height: 60.75pt; width: 55pt;">QSO_DATE<br></td>\
        <td class="xl64" width="87" style="border-left: none; width: 65pt;">QSO_TIME GMT<br></td>\
        <td class="xl66" width="81" style="width: 61pt;">QSO_RX_RSTrx<br></td>\
        <td class="xl66" width="81" style="width: 61pt;">QSO_TX_RST589tx<br></td></tr>'
    QSO_deets_style_footer = '</tbody></table><div><br></div>]]></description>'
    QSO_deets_style_HEADER = QSO_deets_style_table + QSO_deets_style_colgroup;
    
    place_end = "</Placemark>"
    fields = qso_line.split(",")
    qso_deets = QSO_deets_style_HEADER + QSO_deets_row + QSO_deets_style_footer
    qso_deets_time = qso_deets.replace("QSO_TIME", fields[4])
    qso_deets_time = '<description><![CDATA[<h1>'+fields[7]+'</h1>Date/Time GMT: <div><br></div>' + fields[4]+ ']]></description>'
    fields = transform_spot_kml(fields)
    if(qso_line_error(qso_line, fields) == False):
        print(placestart)
        print('<name>' + fields[7] + '</name>' );
        #Now print the description>
        print(qso_deets_time)
        #output the formatted timestamp
        print(fields[4])
        print(linestart)
        print(fields[0]+","+fields[1]+",0.")
        print(fields[2]+","+fields[3]+",0.")
        print(lineend)
        if(fields[5] == "0"):
            #set for QSO line color with unknown RST
            print(qso_style_no_rst.replace("line_color", signal_colors[fields[5]]))
        elif(len(fields[5]) != 3):
            #set for spot line color (RBN)
            spot_color = spot_style.replace("line_color", signal_colors[db_to_s(fields[5])])
            spot_color_transparent = spot_color.replace("#ff", "#33")
            print(spot_color_transparent)
        elif(len(fields[5]) == 3):
            #set for QSO line color with specified S of RST
            print(qso_style.replace("line_color", signal_colors[fields[5][1]]))
        print(place_end)
        add_placemark(fields)
    else:
        return -1
    return 0

def add_placemark(fields):
    if((is_repeated_spot(fields) == False)):
        #add a placemark for the receiving station
        print('<Placemark>')
        print('<name>'+fields[7]+'</name>')
        #set icon style
        if(len(fields[5]) != 3):
            print('<styleUrl>#RBN</styleUrl>')
        else:
            print('<styleUrl>#QSO</styleUrl>')
        print('<Point>')
        print('<coordinates>'+fields[2]+','+fields[3]+'</coordinates>')
        print('</Point>')
        print('</Placemark>')
        #mark any spots as already happened after the first time
        set_rbn_spot(fields)
        


def qso_line_error(qso_line, fields):
    if((len(fields)==8) and (qso_line.find(", ") == -1)):
      return False
    elif(len(fields)!=8):
        print ("Input line does not have 8 fields:", sys.stderr)
        print (qso_line, sys.stderr)
        return True
    elif(qso_line.find(", ") != -1):
        print ("Input line has a space after comma:", sys.stderr)
        print (qso_line, sys.stderr)
        return True


def transform_spot_kml(fields_list):
    #reformat the timestamp for kml
    fields_list[4] = fields_list[4].replace('/','-')
    fields_list[4] = fields_list[4].replace(' ','T')
    fields_list[4] = "<TimeStamp>"+fields_list[4]+"</TimeStamp>"
    #Then, wrap the timestamp in the appropriate tags
    return fields_list

def is_rbn_spot(fields_list):
    if(fields_list[5]!= "0"):
        return True
    else:
        return False

def set_rbn_spot(fields_list):
    if(is_rbn_spot(fields_list)):
        already_spotted[fields_list[7]] = 1;

def is_repeated_spot(fields_list):
    return fields_list[7] in already_spotted

def print_map_style():
    print('<Style id="RBN">')
    print('<IconStyle>')
    print('<Icon>')
    print('<href>http://maps.google.com/mapfiles/kml/pal5/icon17.png</href>')
    print('</Icon>')
    print('</IconStyle>')
    print('</Style>')
    print('<Style id="QSO">')
    print('<IconStyle>')
    print('<Icon>')
    print('<href>https://mt.google.com/vt/icon/name=icons/onion/SHARED-mymaps-container-bg_4x.png,icons/onion/SHARED-mymaps-container_4x.png,icons/onion/1529-broadcast_4x.png</href>')
    print('</Icon>')
    print('</IconStyle>')
    print('</Style>')


#add code to read directly from rm_rnb_history_pres.csv

