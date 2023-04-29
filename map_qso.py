import argparse
from auto_geo_update import dump_rm_rbn_history
from expe_kml_defs import expe_kml
from qso_spot_kml import qso_spot_kml

def map_qsos(lng,lat,map_title):
    #read QSOs to be mapped, fetch geo_location data and return a list of 
    #mappable QSOs sorted by QSO time, earliest to latest
    result = dump_rm_rbn_history(lng, lat, '')
    #creates a list of QSO formatted the same as rm_rnb_histor_pres.csv
    #then, gathers up spotting entries from the same file, and returns a list
    #of strings formatted as lines in the file that are passed on 
    #to qso_spot_kml to produce a kml map
    result = expe_kml(result[0][1], result[0][2],result[0][4],result[len(result)-1][4],result)
    result = qso_spot_kml("",77,result,map_title)

parser = argparse.ArgumentParser(
                    prog='map_qso.py',
                    description='Creates kml maps from a csv formatted file of QSOs\n\
                    QSOs are read from qso_update.csv by default',
                    epilog='Text at the bottom of help')
parser.add_argument('-t', dest="map_title", help="Title for the map")
parser.add_argument('-n', type=float, dest="lng", help="longitude of the tx site")
parser.add_argument('-a', type=float, dest="lat", help="latitude of the tx site")
args = parser.parse_args()

map_qsos(args.lng,args.lat,args.map_title)

