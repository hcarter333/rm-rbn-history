import sys
import argparse
import datetime

parser = argparse.ArgumentParser(
                    prog='expe_kml',
                    description='Creates kml maps over a time range with the input location',
                    epilog='Text at the bottom of help')
parser.add_argument("-b", "--begin_timestamp", dest="begin_timestamp",
                  help="begin_timestpam", 
                  metavar="MAX_TIMESTAMP(YYYY-MM-DD HH24:MM:SS)")
parser.add_argument("-e", "--end_timestamp", dest="end_timestamp",
                  help="end_timestamp", 
                  metavar="MAX_TIMESTAMP(YYYY-MM-DD HH24:MM:SS)")
parser.add_argument('-n', type=float, dest="lng")
parser.add_argument('-a', type=float, dest="lat")

args = parser.parse_args()
if args.begin_timestamp:
    # Try parsing the date argument
    try:
        begin_timestamp = datetime.datetime.strptime(args.begin_timestamp, "%Y/%m/%d %H:%M:%S")
    except:
        print("Error parsing date input:",sys.exc_info())
        sys.exit(1)

if args.end_timestamp:
    # Try parsing the date argument
    try:
        end_timestamp = datetime.datetime.strptime(args.end_timestamp, "%Y/%m/%d %H:%M:%S")
    except:
        print("Error parsing date input:",sys.exc_info())
        sys.exit(1)

f = open('rm_rnb_history_pres.csv')
firstline = 1
for line in f:
    #throw away the first line
    fields = line.split(",")
    if((firstline != 1) and (len(fields)==9)):
        #print(fields[5])
        try:
            line_date = datetime.datetime.strptime(fields[5], '%Y/%m/%d %H:%M:%S')
        except:
            try:
                line_date = datetime.datetime.strptime(fields[5], '%Y/%m/%d %H:%M')
            except:
                print("Error parsing date input:",sys.exc_info())
                sys.exit(1)

 #       line_date = datetime.datetime.strptime(fields[5], '%Y/%m/%d %H:%M:%S')
        if((line_date > begin_timestamp) and (line_date < end_timestamp)):
            sys.stdout.write(str(args.lng)+','+str(args.lat)+','+fields[3]+','+fields[4]+\
                ','+fields[5]+','+fields[6]+','+fields[7]+','+fields[8])
    else:
        firstline = 0
