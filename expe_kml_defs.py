import sys
import datetime
import random
from auto_geo_vars import kml_title, tx_lng, tx_lat

def expe_kml_per_line(lng, lat, fields, begin_timestamp, end_timestamp, out):
    try:
        line_date = datetime.datetime.strptime(fields[5], '%Y/%m/%d %H:%M:%S')
    except:
        try:
            line_date = datetime.datetime.strptime(fields[5], '%Y/%m/%d %H:%M')
        except:
            print("Error parsing date input:",sys.exc_info())
            print("Bad line_date")
            print(fields[5])
            sys.exit(1)

 #       line_date = datetime.datetime.strptime(fields[5], '%Y/%m/%d %H:%M:%S')
    if((line_date >= begin_timestamp) and (line_date <= end_timestamp)):
         output_string = str(random.randrange(0,4294967295)) + ',' + str(lng)+','+str(lat)+','+fields[3]+','+fields[4]+\
            ','+fields[5]+','+fields[6]+','+fields[7]+','+fields[8]
         if(out == True):
             sys.stdout.write(output_string)
         #print("Here's the first output string")
         #print(output_string)
         return output_string
    


def expe_kml(lng, lat, begin_timestamp, end_timestamp, qso_list=[]):
    result = []
    #Look in the RBN list and do the QSOs if any
    f = open('rm_rnb_history_pres.csv')
    firstline = 1
    #print("qso processing in file")
    for line in f:
        #throw away the first line
        fields = line.split(",")
        if((firstline != 1) and (len(fields)==9)):
            qso_out = expe_kml_per_line(lng, lat, fields, begin_timestamp, 
                                        end_timestamp, False)
            if(qso_out != None):
                result.append(qso_out)
        else:
          firstline = 0

    for qso in qso_list:
        #construct fields (the first one is the unused random key)
        rx_loc=qso[3].split(",")
        fields = [qso[0],str(qso[1]),str(qso[2]),rx_loc[0],rx_loc[1],\
                  qso[4].strftime("%Y/%m/%d %H:%M:%S"),qso[5],'14058.4',qso[6]]
        qso_out = expe_kml_per_line(lng, lat, fields, begin_timestamp, 
                                    end_timestamp, True)
        #print("pass this on " + qso_out)
        if(qso_out != None):
            result.append(qso_out)
    return result