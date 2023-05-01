from auto_geo_update import dump_rm_rbn_history
from expe_kml_defs import expe_kml
from qso_spot_kml import qso_spot_kml
import auto_geo_vars

def map_qsos():
    #read QSOs to be mapped, fetch geo_location data and return a list of 
    #mappable QSOs sorted by QSO time, earliest to latest
    result = dump_rm_rbn_history()
    #creates a list of QSO formatted the same as rm_rnb_histor_pres.csv
    #then, gathers up spotting entries from the same file, and returns a list
    #of strings formatted as lines in the file that are passed on 
    #to qso_spot_kml to produce a kml map
    result = expe_kml(result[0][1], result[0][2],result[0][4],result[len(result)-1][4],result)
    result = qso_spot_kml("",77,result,auto_geo_vars.kml_title)

#There are no args because the tx station lng, lat, and the map title 
#are in the first three lines of the QSOs file respectively
map_qsos()

