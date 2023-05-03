The pota_qso.py script outputs a [POTA](https://pota.app/#/) suitable adif file from the current contents of the qso_update.csv file. Usage is  
  
python pota_qso.py -k [park_code] > my_pota_name.adif  
  
where the -k argument is required, and is the POTA code for the park, ([K-4551](https://pota.app/#/park/K-4551) for example), and 'my_pota_name' is the filename chosen by the user.  
  
One [adif](https://docs.pota.app/docs/activator_reference/ADIF_for_POTA_reference.html) compatible line per QSO found in qso_update.csv is sent to stdout.  

For implementation information see [#41](https://github.com/hcarter333/rm-rbn-history/issues/41)
