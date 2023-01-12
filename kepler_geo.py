import json
import datetime

f = open('spots.json')
h = open('stations_geo.json')

# returns JSON object as 
# a dictionary
spots = json.load(f)
geo_data=json.load(h)

#reformat timestamp
e='%H%Mz %d %b'

for i in spots:
    new_date=datetime.datetime.strptime(spots[i][5], e)
    new_date=new_date.replace(2023)
    spots[i][5]=datetime.datetime.strftime(new_date, '%Y/%m/%d %H:%M:%S')

print("id,geometry,timestamp")
for i in spots:
    print(i+',"{""type"":""LineString"",""coordinates"":[[-122.42299,37.72286],['+\
    	geo_data[spots[i][0]][7]+","+geo_data[spots[i][0]][6]+\
    	']]}","'+spots[i][5]+'"')

