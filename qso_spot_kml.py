import sys
import random

#Read each line in the qso_file
#format it as as kml and write it to stdout using print
#generate random 32 bit key
def qso_spot_kml(qso_file, key=77):
    f = open(qso_file)
    #output the standard header
    print('<?xml version="1.0" encoding="UTF-8"?>')
    print('<kml xmlns="http://earth.google.com/kml/2.0"> <Document><name>pota_title</name>')
    for line in f:
        if(transfom_qso_to_kml(line) == -1):
          sys.exit("qso input has incorrect format, see message above")
    #output file footer
    print('</Document> </kml>')

def transfom_qso_to_kml(qso_line):
    placestart = "<Placemark>"
    linestart = "<LineString><coordinates>"
    lineend = "</coordinates></LineString>"
    qso_style = "<Style><LineStyle><color>#ff00ff00</color><width>3</width></LineStyle></Style>"
    spot_style = "<Style><LineStyle><color>#ffff0000</color><width>3</width></LineStyle></Style>"
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
    if((len(fields)==8) and (qso_line.find(", ") == -1)):
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
            #set for QSO line color
            print(qso_style)
        else:
            #set for spot line color (RBN)
            print(spot_style)
        print(place_end)
        #add a placemark for the receiving station
        print('<Placemark>')
        print('<name>'+fields[7]+'</name>')
        print('<Point>')
        print('<coordinates>'+fields[2]+','+fields[3]+'</coordinates>')
        print('</Point>')
        print('</Placemark>')
    elif(len(fields)!=8):
        print ("Input line does not have 8 fields:", sys.stderr)
        print (qso_line, sys.stderr)
        return -1
    elif(qso_line.find(", ") != -1):
        print ("Input line has a space after comma:", sys.stderr)
        print (qso_line, sys.stderr)
        return -1
    return 0

def transform_spot_kml(fields_list):
    #reformat the timestamp for kml
    fields_list[4] = fields_list[4].replace('/','-')
    fields_list[4] = fields_list[4].replace(' ','T')
    fields_list[4] = "<TimeStamp>"+fields_list[4]+"</TimeStamp>"
    #Then, wrap the timestamp in the appropriate tags
    return fields_list

#add code to read directly from rm_rnb_history_pres.csv

