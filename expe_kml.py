import sys
import argparse
import datetime
from expe_kml_defs import expe_kml

#Example use:
#expe_kml.py -b "2023/04/04 13:10:00" -e "2023/04/04 16:23:00" -a 37.803855263605000 -n-122.476722711130000 > ggo_23_04_04_a.csv


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

expe_kml(args.lng, args.lat, begin_timestamp, end_timestamp)
