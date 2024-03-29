import json
import datetime
from datetime import timedelta

f = open('incidents.json')
h = open('stations_geo.json')

#San Francisco
geo_station = "-122.42299,37.72286"
time_diff = 0
#37.8025536, -122.4774149

#Golden Gate Overlook I
#geo_station = "-122.4774149,37.8025536"
#time_diff = 0

#National Maritime
#geo_station = "-122.421006408453000,37.80776743"
#time_diff = 0


#122.42299,37.72286
#Fort Fun#37.8025536, -122.4774149ston
#geo_station = "-122.503527918121000,37.718750411089600"
#time_diff = 0

#Fort Funston II
#geo_station = "-122.5017746265654,37.72002112924458"
#time_diff = 0

#Tamalpais
#geo_station = "-122.603280202635000,37.903910507922100"
#time_diff = 0

#Rosie Riveter I
#geo_station = "-122.3497911055768,37.91493229232588"
#time_diff = 0

#Rosie Riveter II
#geo_station = "-122.34654548945645,37.915318565746944"
#time_diff = 0

#Los Angelese STate Historical Park
#geo_station = "-118.231391054668000,34.068540984515200"
#time_diff = 0

#San Bruno Mountain Sate Park
#geo_station = "-122.43129925155743, 37.703220169453076"
#time_diff = 0


#Baylor Pass I
#geo_station = "-106.578838, 32.382328"
#time_diff = 7-122.43129925155743"

#Baylor Pass II
#geo_station = "-106.579229, 32.380401"
#time_diff = 7

#Three Rivers Petroglyph Site
#geo_station = "-106.006336, 33.346341"
#time_diff = 7

#Organ Mountains-Desert Peaks National Monument
#geo_station = "-106.556812, 32.373049"
#time_diff = 7

#VillaNueva
#geo_station = "-105.333232818105000,35.265642780552700"
#time_diff = 7

#Cibola
#geo_station = "-105.6740871407319,34.216829239864644"
#time_diff = 0



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
    new_date = new_date - timedelta(hours=time_diff, minutes=0)
    #print(new_date)
    #print(datetime.datetime.strftime(new_date, '%Y/%m/%d %H:%M:%S'))
    #print(today)
    if new_date > today:
        # date not before today, attach *last* year
        new_date = new_date.replace(year=today.year - 1)

    spots[i][5]=datetime.datetime.strftime(new_date, '%Y/%m/%d %H:%M:%S')
    #print(spots[i][5])

print("id,geometry,timestamp,dB,frequency,Spotter")
for i in spots:
    #print(i+',"{""type"":""LineString"",""coordinates"":[['+ geo_station + '],['+\
    #	geo_data[spots[i][0]][7]+","+geo_data[spots[i][0]][6]+\
    #	']]}","'+spots[i][5]+'"'+','+str(spots[i][3])+','+str(spots[i][1])+','+spots[i][0])
    print(i+','+ geo_station + ','+\
    	geo_data[spots[i][0]][7]+','+geo_data[spots[i][0]][6]+\
    	','+spots[i][5]+','+str(spots[i][3])+','+str(spots[i][1])+','+spots[i][0])

