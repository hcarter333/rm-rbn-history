import json
import datetime
from datetime import timedelta

f = open('incidents.json')
h = open('stations_geo.json')

# returns JSON object as 
# a dictionary
spots = json.load(f)
geo_data=json.load(h)

#reformat timestamp
e='%H%Mz %d %b'

today = datetime.datetime.today()
for i in spots:
    new_date=datetime.datetime.strptime(spots[i][5], e)
    new_date = new_date.replace(year=today.year)
    new_date = new_date - timedelta(hours=8, minutes=0)
    #print(new_date)
    #print(datetime.datetime.strftime(new_date, '%Y/%m/%d %H:%M:%S'))
    #print(today)
    if new_date > today:
        # date not before today, attach *last* year
        new_date = new_date.replace(year=today.year - 1)

    spots[i][5]=datetime.datetime.strftime(new_date, '%Y/%m/%d %H:%M:%S')
    #print(spots[i][5])

print("id,geometry,timestamp")
for i in spots:
    print(i+',"{""type"":""LineString"",""coordinates"":[[-122.42299,37.72286],['+\
    	geo_data[spots[i][0]][7]+","+geo_data[spots[i][0]][6]+\
    	']]}","'+spots[i][5]+'"')

