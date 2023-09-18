In addition to mapping reverse beacon netowrk staitons that have spotted your radio, it's useful to plot out QSOs. Contacts with othe amateur staiotns offers a larger geographical diversity than the spotting network allowing more detailed analsyis of your station's propagation profile.  
![image](https://user-images.githubusercontent.com/363004/218315412-46061dcd-627a-4f6b-b73a-cf72962e9750.png)
<p style="text-align: center;">Reverse Beacon Network spotting sations on 20 meters in North America </p>  
For example, the following two pictures show propagation around Baylor Pass that's more pronounced with the QSO data (green lines) in addition to the spot data (blue lines)  
  
![image](https://user-images.githubusercontent.com/363004/218317147-754a88f6-9a2d-4784-9f1a-cc085b9a55b7.png)
  
  
![image](https://user-images.githubusercontent.com/363004/218317039-e85cd0b8-5f9f-4637-85b1-073e0e2201a1.png)
  
To add QSOs to your collection of data, do the following:
1. Edit [qso_update.csv]([url](https://github.com/hcarter333/rm-rbn-history/blob/6b5f8da9413afe7235bc7c880824f6ec1ad7fadd/qso_update.csv)), (in your fork of course) adding your qsos, one per line, in the following comma separated vairable format:  
sta_lat,sta_lng,rx_lat,rx_lng,yyyy/mm/dd hh:mm:ss,transmitted rst,received rst,rx_call
2. Commit the file.

The worklow action will pull the data from the file, add it to the database, and then delete the contents of the file as described in [#12]([url](https://github.com/hcarter333/rm-rbn-history/issues/12#issue-1568438805)) .

At preent, the frquency is alwasy assigned to 14058.4. This will be changed eventually (by #53 ) so that an actual frquency can be specified.
