import re, sys, io
import argparse

def linkify_sotals(input_file):
    kml_file="W7U.kml"
    f = open(kml_file)
    for line in f:
        #look for summit names
        pat = '.*?\<name\>.*?CDATA\[(.*)]].*'
        patd = '.*?\<description\>.*?CDATA\[(.*)]].*'
        sname = re.search(pat, line)
        sdesc = re.search(patd,line)
        if(sname != None):
            summit_name = sname.group(1)
            print(line)
        #look for summit descriptions
        elif(sdesc != None):
            summit_desc = sdesc.group(1)
#            print(summit_desc)
            new_summit_desc = '<a href = "https://sotl.as/summits/' + summit_name + \
                              '">' + summit_desc + '</a>'
            print("<description><![CDATA[" + new_summit_desc + "]]></description>")
        else:
            print(line)
parser = argparse.ArgumentParser(
                    prog='map_qso',
                    description='Creates links to sotal pages',
                    epilog='Text at the bottom of help')
parser.add_argument('-hh', action='store_true')
args = parser.parse_args()
#auto_geo_vars.hh = args.hh
#There are no required args because the tx station lng, lat, and the map title 
#are in the first three lines of the QSOs file respectively
linkify_sotals("test")
