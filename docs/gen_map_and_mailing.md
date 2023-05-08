The current steps to create a map of your QSOs are 
Enter your qsos into qso_update.csv with the following csv format  
call,rx_rst,tx_rst,date_time
date format is '%Y/%m/%d %H:%M:%S'

Then, to geo_locate all the received stations run (for example)
add_rbn_qsos.py -a 34.801 -n -106.7995 > sota.txt
  
Where -a is the latitude of your transmitting location and -n is the longitude 
Then run  
expe_kml.py -b "2023/04/25 18:10:00" -e "2023/04/25 20:23:00" -a 34.801 -n-106.7995 > cerros_sota_23_04_25.csv  
  
Where -a and -n have the same meaning, and -b and -e are the beginning and end of the time period you're interested in. This will create a .csv file with both your qsos and RBN spots during that timeframe, with all of them anchored at your receiving station location  
  
Change line 3 in qso_kml.py to reference the path and name of the .csv file you created in the immmediately previous step.
  
  
Then, run
qso_kml.py > cerros_sota_23_04_25.kml
Finally, edit the resulting kml file, changing the <Document><name> tag to your desired map title.

This script requires a subscription to the XML data service at qrz.com. You'll need to set an environment variable named QRZ_PSWD to your password for the service.
