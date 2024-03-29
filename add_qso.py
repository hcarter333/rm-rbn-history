import sys
import random

#Read each line in the qso_file
#format it as kepler_geo and write it to stdout using print
#generate random 32 bit key
def add_qso(qso_file, key=77):
    was_77 = False
    f = open(qso_file)
    for line in f:
        fields = line.split(",")
        if(len(fields)==8):
            if(key==77):
                key = random.randrange(0,4294967295)
                was_77 = True
            #print(str(key)+',"{""type"":""LineString"",""coordinates"":[['+ fields[0] +\
            #  ',' + fields[1] + '],['+fields[2]+","+fields[3]+']]}","'+fields[4]+'"'+\
            #  ','+fields[5]+','+fields[6]+','+fields[7])
            sys.stdout.write(str(key)+','+ fields[0]+','+fields[1]+','+fields[2]+','+fields[3]+\
                ','+fields[4]+','+fields[5]+','+fields[6]+','+fields[7])
            #make sure all keys are random after fist
            if(was_77):
                key = 77
    return random.randrange(0,4294967295)