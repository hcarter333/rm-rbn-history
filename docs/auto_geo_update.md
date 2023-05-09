auto_geo_update uses a qso_update.csv file as input. 
The first three lines contain, repectively, the map title, the tx station longitude, and the tx station latitude.
The csv file has the following format after the first three lines  
call,date_time,rx_rst,tx_rst,<s2s_lat>,<s2s_lng>  
where date_time is formatted as  
%Y/%m/%d %H:%M:%S  
or to put it more literally as in Excel rather than  Python  
"YYYY/MM/DD HH/MM/SS"  
The last two fields of the line above are optional and are used to specify the location of summits or parks in summit to summit or park to park QSOs. If the last two fields are found, then geocoding using qrz.com and the Google Maps API are skipped and the location fields are used as is. See issue [#42](https://github.com/hcarter333/rm-rbn-history/issues/42) for more details.

The script outputs a line, with the calling stations location, compatible with [rm_rnb_history_pres.csv](https://github.com/hcarter333/rm-rbn-history/blob/main/rm_rnb_history_pres.csv) for each input line.  
  
To dump out a csv list with qsl addresses for mailing, use mail_qsl.py > my_qsls.csv. This is for use with the double response post card Word template at [QSL_picture_paste_MM.docx](https://github.com/hcarter333/kd0fnr_radio_ops/blob/main/QSL_picture_paste_MM.docx)  

**Requirements**
These scripts requires a subscription to the XML data service at qrz.com. You'll need to set an environment variable named QRZ_PSWD to your password for the service. Some of them also require a Google Maps API key. the value of this key should be stred in an environment variable named MAPS_API_KEY.

**Creating a new map**  
Simply execute map_qso.py. The script will pick up data from qso_update.csv including the maps title. The map will be output to maps/map_file_name.kml where map_file_name is the map title defined in qso_update.csv with spaces replaced by underscores. Be careful about using punctuation in map titles for now as not all punctuation is converted to underscore yet.  

The second and third lines of the file (qso_update.csv) are the longitude and latitude respectively.
  
The -hh option to the script will include RBN spots from one half hour on either side of the min/max QSO date range. This is especially useful when there is only 1 QSO during the POTA or SOTA  

**Methods Called**  
get_qrz_session(username)
This method returns a (hopefully) valid QRZ session ID based on the username and a password stored in a repository secret. The session id is used in all calls to the QRZ.com data interface.
  
get_qrz_call_geo_address(callsign)
This method retrieves the address (minus zip code) that is passed to Google to get the callsigns actual location. The adddress is pulled from the QRZ.com data service subscription.

