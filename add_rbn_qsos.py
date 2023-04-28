from auto_geo_update import dump_rm_rbn_history
import argparse

parser = argparse.ArgumentParser(
                        prog='auto_geo_update',
                        description='outputs comma separated list to paste into rm_rnb_history_pres.csv',
                        epilog='Text at the bottom of help')
parser.add_argument('-n', type=float, dest="lng")
parser.add_argument('-a', type=float, dest="lat")
args = parser.parse_args()

#34.801, -106.7995
dump_rm_rbn_history(args.lng, args.lat)
