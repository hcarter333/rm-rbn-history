import os
import requests
import json

#Datasette qeury to retrieve QSOs
qso_rx_geo = requests.get('http://127.0.0.1:8001/rm_toucans_23_10_07.json?sql=\
                          select+Spotter%2C+rx_lng%2C+rx_lat+from+rm_rnb_history_pres+where+\
                          %22dB%22+%3E+%3Ap0+order+by+rowid&p0=99')
#print(qso_rx_geo.text)
q = json.loads(qso_rx_geo.text)
for result in q["rows"]:
    #print(result)
    lng = result[1]
    lat = result[2]
    ds_geo_json = requests.get('http://127.0.0.1:8001/counties.json?sql=select%0D%0A++STATEFP+as+\
                               state_fips%2C%0D%0A++states.abbreviation+as+state%2C%0D%0A++STATEFP+%7C%7C+\
                               COUNTYFP+as+county_fips%2C%0D%0A++counties.NAME+as+county_name%2C%0D%0A++\
                               COUNTYNS%2C%0D%0A++AFFGEOID%2C%0D%0A++GEOID%2C%0D%0A++LSAD%2C%0D%0A++ALAND%2C%0D%0A++\
                               AWATER%0D%0Afrom%0D%0A++counties+join+states+on+counties.STATEFP+%3D+states.fips\
                               %0D%0Awhere%0D%0A++within%28%0D%0A++++MakePoint%28cast%28%3Alongitude+as+\
                               float%29%2C+cast%28%3Alatitude+as+float%29%29%2C%0D%0A++++counties.Geometry%0D%0A++\
                               %29+%3D+1+and+counties.rowid+in+%28%0D%0A++++select%0D%0A++++++rowid%0D%0A++++from%0D%0A++++++\
                               SpatialIndex%0D%0A++++where%0D%0A++++++f_table_name+%3D+%27counties%27%0D%0A++++++and\
                               +search_frame+%3D+MakePoint%28cast%28%3Alongitude+as+float%29%2C+cast%28%3Alatitude+\
                               as+float%29%29%0D%0A++%29%0D%0Alimit%0D%0A++1&longitude='+str(lng)+'&latitude='+str(lat))
    #print(ds_geo_json.text)
    z = json.loads(ds_geo_json.text)
    for localities in z["rows"]:
        print(result[0] + ':' + localities[1] + ' ' + localities[3])
    