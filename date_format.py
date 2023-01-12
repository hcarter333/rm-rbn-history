import datetime
e='%H%Mz %d %b'
d=datetime.datetime.strptime("2337z 10 Jan", e)
d=d.replace(2023)
print(datetime.datetime.strftime(d, '%Y/%m/%d %H:%M:%S'))
