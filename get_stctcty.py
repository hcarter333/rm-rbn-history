import os
import requests
import json




#rev_geo = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=36.6584466,138.188353'+'&key='+os.getenv("MAPS_API_KEY"))
State = ""
County = ""
Country = ""
#rev_geo = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=39.6287,-104.842'+'&key='+os.getenv("MAPS_API_KEY")+
#                       '&result_type=administrative_area_level_2')

#-122.42293617440531
#37.72489522009444
rev_geo = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=37.72489522009444,-122.42293617440531'+'&key='+os.getenv("MAPS_API_KEY")+
                       '&result_type=locality')
y=json.loads(rev_geo.text)
#We're looking for counties and states and countries
#County: administrative_area_level_2
#break_out = False
#for result in y["results"]:   #y["results"][x]
#    if(break_out):
#        break
#    for component in result:  #y["results"][0]["address_components"]
#        if(break_out):
#            break
#        #print(component)
#        print("next one")
#        if(component == "types"):
#            for level in result[component]:
#                print(level)
#                if(level == "administrative_area_level_2"):
#                    print(result)
#                    print(result["address_components"][0]["long_name"])
#                    break_out = True
#                    break
#        #for elements in components:
#        #   print()
#        #if(component = ["address_components"]
#print(y["results"][0]["address_components"][1]["types"])
print(rev_geo.text)

#now test just calling a datasette query with requests
ds_geo = requests.get('http://127.0.0.1:8001/counties.csv?sql=select%0D%0A++STATEFP+as+state_fips%2C%0D%0A++states.abbreviation+as+state%2C%0D%0A++STATEFP+%7C%7C+COUNTYFP+as+county_fips%2C%0D%0A++counties.NAME+as+county_name%2C%0D%0A++COUNTYNS%2C%0D%0A++AFFGEOID%2C%0D%0A++GEOID%2C%0D%0A++LSAD%2C%0D%0A++ALAND%2C%0D%0A++AWATER%0D%0Afrom%0D%0A++counties+join+states+on+counties.STATEFP+%3D+states.fips%0D%0Awhere%0D%0A++within%28%0D%0A++++MakePoint%28cast%28%3Alongitude+as+float%29%2C+cast%28%3Alatitude+as+float%29%29%2C%0D%0A++++counties.Geometry%0D%0A++%29+%3D+1+and+counties.rowid+in+%28%0D%0A++++select%0D%0A++++++rowid%0D%0A++++from%0D%0A++++++SpatialIndex%0D%0A++++where%0D%0A++++++f_table_name+%3D+%27counties%27%0D%0A++++++and+search_frame+%3D+MakePoint%28cast%28%3Alongitude+as+float%29%2C+cast%28%3Alatitude+as+float%29%29%0D%0A++%29%0D%0Alimit%0D%0A++1&longitude=-122.42293617440531&latitude=37.72489522009444&_size=max')
print(ds_geo.text)

qso_rx_geo = requests.get('http://127.0.0.1:8001/rm_toucans_23_10_07.json?sql=select+Spotter%2C+rx_lng%2C+rx_lat+from+rm_rnb_history_pres+where+%22dB%22+%3E+%3Ap0+order+by+rowid&p0=99')
#print(qso_rx_geo.text)
q = json.loads(qso_rx_geo.text)
for result in q["rows"]:
    #print(result)
    lng = result[1]
    lat = result[2]
    ds_geo_json = requests.get('http://127.0.0.1:8001/counties.json?sql=select%0D%0A++STATEFP+as+state_fips%2C%0D%0A++states.abbreviation+as+state%2C%0D%0A++STATEFP+%7C%7C+COUNTYFP+as+county_fips%2C%0D%0A++counties.NAME+as+county_name%2C%0D%0A++COUNTYNS%2C%0D%0A++AFFGEOID%2C%0D%0A++GEOID%2C%0D%0A++LSAD%2C%0D%0A++ALAND%2C%0D%0A++AWATER%0D%0Afrom%0D%0A++counties+join+states+on+counties.STATEFP+%3D+states.fips%0D%0Awhere%0D%0A++within%28%0D%0A++++MakePoint%28cast%28%3Alongitude+as+float%29%2C+cast%28%3Alatitude+as+float%29%29%2C%0D%0A++++counties.Geometry%0D%0A++%29+%3D+1+and+counties.rowid+in+%28%0D%0A++++select%0D%0A++++++rowid%0D%0A++++from%0D%0A++++++SpatialIndex%0D%0A++++where%0D%0A++++++f_table_name+%3D+%27counties%27%0D%0A++++++and+search_frame+%3D+MakePoint%28cast%28%3Alongitude+as+float%29%2C+cast%28%3Alatitude+as+float%29%29%0D%0A++%29%0D%0Alimit%0D%0A++1&longitude='+str(lng)+'&latitude='+str(lat))
    #print(ds_geo_json.text)
    z = json.loads(ds_geo_json.text)
    for localities in z["rows"]:
        print(result[0] + ':' + localities[0] + ' ' + localities[3])
    