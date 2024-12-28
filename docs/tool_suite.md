Tool suite info here.

To run the Datasette QSO database with full mapping capabilities use  
`python -m datasette rm_toucans.db --metadata qso_loc.yml --load-extension=SpatiaLite`  

To create the underlying database use  
`csvs-to-sqlite -dt timestamp rm_rnb_history_pres.csv photo_path.csv rm_toucans.db`  

To generate a kml map use  

On the current Chromebook use  
`python3 -m datasette rm_toucans.db --metadata qso_loc.yml --load-extension=/usr/lib/x86_64-linux-gnu/mod_spatialite.so --template-dir plugins/templates`

To run on any machine with the kml plugin, use the following extra plugins-dir argument
```
python3 -m datasette rm_toucans.db --metadata qso_loc.yml --load-extension=/usr/lib/x86_64-linux-gnu/mod_spatialite.so --plugins-dir=plugins --template-dir plugins/templates --root
```

Let's talk about SpatiaLite and Windows
For new datasette installs, until the proposed Windows fix is accepted, make sure to add the fix shown [here](https://github.com/simonw/datasette/issues/2198#issuecomment-2081257809).
Then, you can simply use the command:
```
python3 -m datasette rm_toucans.db --metadata qso_loc.yml --load-extension=spatialite --plugins-dir=plugins --template-dir plugins/templates --root
```

**POTA Analysis tools**  
To find calls that may have been miscopied use  
python3 extract_callsigns.py qso_update.csv | python3 missingpota.py | grep "cannot be found"  

extract_callsigns.py outputs a list of callsigns from the input file passed in.
missingpota.py queries the POTA database for each callsign. If the callsign is not found, then a line containing "cannot be found" is output. See issue [100](https://github.com/hcarter333/rm-rbn-history/issues/100) for more details.  
