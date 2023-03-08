When qso files are input to qso_spot_kml.py they are check for errors.  
If either of the two conditions are found, the kml creation process will halt with error messages:
1. The number of fields in the qso input line is not 8
2. A space is found after a comma in the input line (see #13 )

