import sys
import random

#Read each line in the qso_file
#format it as kepler_geo and write it to stdout using print
#generate random 32 bit key
def add_qso(qso_file, key=77):
    f = open(qso_file)
    if(key==77):
        key = random.randrange(0,4294967295)
    for line in f:
        fields = line.split(",")
        print(str(key)+',"{""type"":""LineString"",""coordinates"":[['+ fields[0] +\
          ',' + fields[1] + '],['+fields[2]+","+fields[3]+']]}","'+fields[4]+'"'+\
          ','+fields[5]+','+fields[6]+','+fields[7])
    return random.randrange(0,4294967295)