import datetime
kml_title = ""
kml_desc = ""
tx_lng = 0
tx_lat = 0
qrz_sess = "none"
hh = None

#Routines used for the automated scripts
#Time routines
def time_hh(rtime):
    time_range = []
    delta = datetime.timedelta(minutes=60)
    time_range.append(rtime[0] - delta)
    time_range.append(rtime[1] + delta)
    return time_range
