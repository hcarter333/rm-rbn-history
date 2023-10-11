import datetime
kml_title = ""
kml_desc = ""
tx_lng = 0
tx_lat = 0
qrz_sess = "none"
hh = None
hhwindow = 60
call_country = ""
call_state = ""
old_start = ""
old_end = ""
old_f2h = ""


#Routines used for the automated scripts
#Time routines
def time_hh(rtime):
    time_range = []
    delta = datetime.timedelta(minutes=hhwindow)
    time_range.append(rtime[0] - delta)
    time_range.append(rtime[1] + delta)
    return time_range
