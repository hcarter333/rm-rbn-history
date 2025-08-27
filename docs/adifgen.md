# POTA ADIF file generator
The html file adifgen.html provides a JavaScript app that creates a POTA ADIF file based on a raw URL for a qso_update.csv file. 

## How to use it
Start a server on your machine in the directory of the repo. I usually use  
`python -m http.server 8081 `  
(unless you're trying to avoid port collisions, you can leave out the -p argument)  

Then, open a web browser with http://localhost:8081/adifgen.html  
