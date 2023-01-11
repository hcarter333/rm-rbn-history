These are the jq strings that work so far:  
**Spots**  
`.spots|to_entries[]|"\(.key), \(.value | .[0:5])"`  
**Call_info**  
`.call_info|to_entries[]|"\(.key), \(.value | .[6:8])"`  
