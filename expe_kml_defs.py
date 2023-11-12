import sys
import datetime
import random
import auto_geo_vars

def expe_kml_per_line(lng, lat, fields, begin_timestamp, end_timestamp, out, country="", state=""):
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
         output_string = str(lng)+','+str(lat)+','+fields[3]+','+fields[4]+\
            ','+fields[5]+','+fields[6]+','+fields[7]+','+fields[8]+','+country+\
            ','+state+",,,,,,,"+fields[9]
         if(out == True):
             sys.stdout.write(str(random.randrange(0,4294967295)) + ',' + output_string + "\n")
         #print("Here's the first output string")
         #print(output_string)
         return output_string
    


def expe_kml(lng, lat, begin_timestamp, end_timestamp, qso_list=[]):
    result = []
    #Look in the RBN list and do the QSOs if any
    if(auto_geo_vars.rbn_off == False):
        result = process_rbn_file(lng, lat, begin_timestamp, end_timestamp)

    for qso in qso_list:
        #construct fields (the first one is the unused random key)
        rx_loc=qso[3].split(",")
        fields = [qso[0],str(qso[1]),str(qso[2]),rx_loc[0],rx_loc[1],\
                  qso[4].strftime("%Y/%m/%d %H:%M:%S"),qso[5],'14058.4',qso[6], qso[9]]
        qso_out = expe_kml_per_line(lng, lat, fields, begin_timestamp, 
                                    end_timestamp, True, qso[7], qso[8])
        #print("pass this on " + qso_out)
        if(qso_out != None):
            result.append(qso_out)
    return result

def process_rbn_file(lng, lat, begin_timestamp, end_timestamp):
    result = []
    f = open('rm_rnb_history_pres.csv')
    firstline = 1
    #print("qso processing in file")
    for line in f:
        #throw away the first line
        #add one more field to patch for tx rst if necessary
        line_patch = line + ",patch"
        fields = line_patch.split(",")
        #print("new length of fields is " + str(len(fields)))
        if((firstline != 1) and ((len(fields)==9) or (len(fields)==13) or (len(fields)==10)or (len(fields)==14))):
            qso_out = expe_kml_per_line(lng, lat, fields, begin_timestamp, 
                                        end_timestamp, False)
            if(qso_out != None):
                result.append(qso_out)
        else:
          firstline = 0
    return result