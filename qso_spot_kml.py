import sys
import random

#Read each line in the qso_file
#format it as as kml and write it to stdout using print
#generate random 32 bit key
def qso_spot_kml(qso_file, key=77):
    placestart = "<Placemark>"
    linestart = "<LineString><coordinates>"
    lineend = "</coordinates></LineString>"
    qso_style = "<Style><LineStyle><color>#ff00ff00</color><width>3</width></LineStyle></Style>"
    spot_style = "<Style><LineStyle><color>#ffff0000</color><width>3</width></LineStyle></Style>"
    place_end = "</Placemark>"
    f = open(qso_file)
    #output the standard header
    print('<?xml version="1.0" encoding="UTF-8"?>')
    print('<kml xmlns="http://earth.google.com/kml/2.0"> <Document>')
    for line in f:
        fields = line.split(",")
        fields = transform_spot_kml(fields)
        if(len(fields)==8):
                print(placestart)
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
    #output file footer
    print('</Document> </kml>')

def transform_spot_kml(fields_list):
    #reformat the timestamp for kml
    fields_list[4] = fields_list[4].replace('/','-')
    fields_list[4] = fields_list[4].replace(' ','T')
    fields_list[4] = "<TimeStamp>"+fields_list[4]+"</TimeStamp>"
    #Then, wrap the timestamp in the appropriate tags
    return fields_list
