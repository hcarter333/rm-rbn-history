from auto_geo_update import dump_rm_rbn_history
from expe_kml_defs import expe_kml
from qso_spot_kml import qso_spot_kml
import auto_geo_vars
import argparse

def map_qsos():
    #read QSOs to be mapped, fetch geo_location data and return a list of 
    #mappable QSOs sorted by QSO time, earliest to latest
    result = dump_rm_rbn_history()
    #creates a list of QSO formatted the same as rm_rnb_histor_pres.csv
    #then, gathers up spotting entries from the same file, and returns a list
    #of strings formatted as lines in the file that are passed on 
    #to qso_spot_kml to produce a kml map
    if(len(result) != 0):
        if(auto_geo_vars.hh == False):
            result = expe_kml(result[0][1], result[0][2],result[0][4],result[len(result)-1][4],result)
        else:
            qso_times = [result[0][4],result[len(result)-1][4]]
            trange = auto_geo_vars.time_hh(qso_times)
            print(trange)
            result = expe_kml(result[0][1], result[0][2],trange[0],trange[1],result)
            print(result)
        result = qso_spot_kml("",77,result,auto_geo_vars.kml_title)

parser = argparse.ArgumentParser(
                    prog='map_qso',
                    description='Creates kml maps using qso_update.csv',
                    epilog='Text at the bottom of help')
parser.add_argument('-hh', action='store_true')
args = parser.parse_args()
auto_geo_vars.hh = args.hh
print("hh = ")
print(args.hh)
#There are no required args because the tx station lng, lat, and the map title 
#are in the first three lines of the QSOs file respectively
map_qsos()

