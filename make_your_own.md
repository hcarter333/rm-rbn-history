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
These instructions will get an animated map up and running. There are other things you can do with filters in kepler.gl please explore.  
[kepler.gl](https://kepler.gl/) is a freeware mapping web app. The data in rm_rnb_history_pres.csv is formatted to  be read directly into the app. Try as I might, I haven't been able to serve the data from github straight to the kepler.gl site, so use the following states to move your data over:  
**Get the data**
1. Navigate to your latest version of [rm_rnb_history_pres.csv](rm_rnb_history_pres.csv)  
2. Click the 'Raw' button: </br>![image](https://user-images.githubusercontent.com/363004/213496317-88e7c903-a527-40a3-9220-37bce5cc2fdf.png)  
3. Copy the resulting screen's data to a text editor (Notepad on Windows for example.)
![image](https://user-images.githubusercontent.com/363004/213496661-dd6d0b8a-c93f-41a0-a997-af2b23f1e646.png)
4. Save the file with your preffered name and a .csv extension.

**Load the data into kepler.gl**
1. Go to [kepler.gl](https://kepler.gl/)
2. Click the 'Get Started' button  </br>![image](https://user-images.githubusercontent.com/363004/213497146-aded04de-596a-4242-8bd9-71abb278935c.png)
3. In the resulting dialog, navigate to your file location and then upload it
4. The static map will be displayed.</br>![image](https://user-images.githubusercontent.com/363004/213497515-7fba56c2-71d2-4c79-bb15-a5fa2f0f557a.png)

**Animate the map**
1. Click on the 'Filters' icon </br>![image](https://user-images.githubusercontent.com/363004/213497759-fd327078-f255-49ad-83cf-755c6d471298.png)
2. Click the 'Add Filter' button </br>![image](https://user-images.githubusercontent.com/363004/213497926-b5d2cbc3-1ba2-4a26-bad7-d8d5b5798ff3.png)
3. Clik in the 'Select a field' edit box, then select 'timestamp' </br>![image](https://user-images.githubusercontent.com/363004/213498165-e0bec079-122a-40a1-a4aa-6c532b6c63ae.png)
4. An animated timeline control will appear. If you hit the 'Play' button, absolutely nothing will happen: here's how to get around that
5. The map starts with the entire 'time window' selected, so there's no way to move the window across the data. Change the 'time window' from this </br></br>![image](https://user-images.githubusercontent.com/363004/213499702-86819df1-9678-4ddc-bbcd-018e6e361584.png)
6. To something like this by dragging the either of the handles at the left and right edge of the 'time window'</br>![image](https://user-images.githubusercontent.com/363004/213499997-951e11c2-3b9d-49a6-924f-84185314b990.png)
7. Now, click the play button. The newly defined 'time window' will be swept across the map data creating an animation:  
![naqcc_results_KD0FNR-2023 01 19-07_21_03](https://user-images.githubusercontent.com/363004/213500447-56428868-6cf8-4d6b-bb2d-ea46042296c6.gif)
