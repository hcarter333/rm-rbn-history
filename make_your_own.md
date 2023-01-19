**Fork the repoisitory**  
In the upper-right-corner of this click on the Fork button:  
![image](https://user-images.githubusercontent.com/363004/213447107-1a50c8db-58cd-4a53-9dd1-46bb800f199c.png)

  
Using only the github web interface, (the site you're reading this in), this is a **4** step process that looks a bit mysterious.  
**Step 1: Change the URL in the workflow**  
  
In the [scrape.yml](.github/workflows/scrape.yml) file, change the address used in each of the curl commands. Specifically, you'll need to change the cdx= argument to your callsign, or a wildcard pattern that [matches your callsign](https://copaseticflow.blogspot.com/2023/01/today-i-learned-reverse-beacon.html).  

**Step 2: Delete the old raw spotter in preparation for adding data for your callsign (first pass)** 
  Your forked .csv files have data from the original project, we need to remove it and replace it with data specific to your callsign.  
  Delete all but the first line containing the column headings of [rm_rnb_history.csv](rm_rnb_history.csv) in your fork, and commit. 
  At the end of this step, the presentation data set will have data from the original project along with your new data. We're going to get rid of the original project's data in the next two steps.  
  
**Step 3: Delete the old presentation data in preparation for adding data for your callsign** 
Delete all but the first line containing the column headings of [rm_rnb_history_pres.csv](rm_rnb_history_pres.csv) in your fork, and commit.  
Leave this line in place:  
"id,geometry,timestamp,dB,frequency,Spotter"  
This will cause the workflow to pull in your callsign's data again. Since nothing will have changed in rm_rnb_history.csv since step 1, rm_rnb_history_pres.csv won't be updated. It will contain only the column heading labels at the end of this step.

**Step 4: Delete raw spotter data again (second pass)** 
  We need github to find 'new' lines in [rm_rnb_history.csv](rm_rnb_history.csv) (the entire process depends on github diff-ing that file to find your new spots. In other words,  it uses github for what github's good at.)  
  
  Delete all but the first line containing the column headings of [rm_rnb_history.csv](rm_rnb_history.csv) in your fork, and commit. This will kickoff the workflow again, but this time it will be loading your call data into an **empty** version. That will cause the diff to detect all the data returned for your callsign as new. The new data will be added to your empty  [rm_rnb_history_pres.csv](rm_rnb_history_pres.csv)  
  
  At the end of **this** step, the presentation data set will have only data for your callsign, and will update correctly from here on out.  But, what to do with that data?
  
  **Loading the data into kepler.gl**


 
