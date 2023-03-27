Using the date range feature:

1. Get a fresh copy of the data by executing 'git pull'
2. -b and -e are used to specify the 'b'eginning and 'e'nd of the datetime range, and should  be in the format YYYY-MM-DD HH24:MM:SS embedded in double quotes on the command line, (see exampl)
3. -n specifies the lo'n'gitude to be substituted for the location of the tx station, 'a' the l'a'titude.
4. Command line example:

<pre>
expe_kml.py -b "2023/03/25 16:15:00" -e "2023/03/25 18:19" -n -122.600424744673000  -a 37.897649811896700  > muir_woods_II_a.csv
</pre>
