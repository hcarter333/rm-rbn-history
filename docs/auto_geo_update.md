auto_geo_update accepts a csv file as input. The csv file has the following format  
call,rx_rst,tx_rst,date_time  

The script outputs a line, with the calling stations location, compatible with [rm_rnb_history_pres.csv](https://github.com/hcarter333/rm-rbn-history/blob/main/rm_rnb_history_pres.csv) for each input line.  Then, the script outputs a set of lines, (corresponding to the same calls), that follow the format  
call,date,time,rx_rst,date_time,address  
These lines can be copied to the QSL mailing spreadsheet


