auto_geo_update accepts a csv file as input. The csv file has the following format after the first three lines  
call,date_time,rx_rst,tx_rst  
The first three lines contain, repectively, the map title, the tx station longitude, and the tx station latitude

The script outputs a line, with the calling stations location, compatible with [rm_rnb_history_pres.csv](https://github.com/hcarter333/rm-rbn-history/blob/main/rm_rnb_history_pres.csv) for each input line.  
  
As a separate feature, code will be implemented that can be used for the following:  
Then, the script outputs a set of lines, (corresponding to the same calls), that follow the format  
call,date,time,rx_rst,date_time,address  
These lines can be copied to the QSL mailing spreadsheet


**Methods Called**  
get_qrz_session(username)
This method returns a (hopefully) valid QRZ session ID based on the username and a password stored in a repository secret. The session id is used in all calls to the QRZ.com data interface.
  
get_qrz_call_geo_address(callsign)
This method retrieves the address (minus zip code) that is passed to Google to get the callsigns actual location. The adddress is pulled from the QRZ.com data service subscription.

