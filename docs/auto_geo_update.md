auto_geo_update accepts a csv file as input. The csv file has the following format after the first three lines  
call,date_time,rx_rst,tx_rst  
where date_time is formatted as  
%Y/%m/%d %H:%M:%S  
or to put it more literally as in Excel rather than  Python  
"YYYY/MM/DD HH/MM/SS"  
The first three lines contain, repectively, the map title, the tx station longitude, and the tx station latitude

The script outputs a line, with the calling stations location, compatible with [rm_rnb_history_pres.csv](https://github.com/hcarter333/rm-rbn-history/blob/main/rm_rnb_history_pres.csv) for each input line.  
  
As a separate feature, code will be implemented that can be used for the following:  
Then, the script outputs a set of lines, (corresponding to the same calls), that follow the format  
call,date,time,rx_rst,date_time,address  
These lines can be copied to the QSL mailing spreadsheet

**Creating a new map**  
Simply execute map_qso.py. The script will pick up data from qso_update.csv including the maps title. The map will be output to maps/map_file_name.kml where map_file_name is the map title defined in qso_update.csv with spaces replaced by underscores. Be careful about using punctuation in map titles for now as not all punctuation is converted to underscore yet.

**Methods Called**  
get_qrz_session(username)
This method returns a (hopefully) valid QRZ session ID based on the username and a password stored in a repository secret. The session id is used in all calls to the QRZ.com data interface.
  
get_qrz_call_geo_address(callsign)
This method retrieves the address (minus zip code) that is passed to Google to get the callsigns actual location. The adddress is pulled from the QRZ.com data service subscription.

