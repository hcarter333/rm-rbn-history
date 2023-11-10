Tool suite info here.

To run the Datasette QSO database with full mapping capabilities use  
`python -m datasette rm_toucans.db --metadata qso_loc.yml --load-extension=SpatiaLite`  

To create the underlying database use  
`csvs-to-sqlite -dt timestamp rm_rnb_history_pres.csv photo_path.csv rm_toucans.db`  

To generate a kml map use  

On the current Chromebook use  
`python3 -m datasette rm_toucans.db --metadata qso_loc.yml --load-extension=/usr/lib/x86_64-linux-gnu/mod_spatialite.so --template-dir plugins/templates`
