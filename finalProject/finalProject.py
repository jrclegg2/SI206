from facebookAccess import *
from gmailAccess import *
from youtubeAccess import *
from darkskyAccess import *

#TODO: define a global activity_insts, post_insts, email_insts, etc.

print ("Welcome to Jack Clegg's final 206 project!\n\nStarting by grabbing all necessary data from various APIs")
print ("-------------------------------------------------------------------------------------------------------")
print ("\nGmail automatically grabs my personal email information...Grabbing now...")
EMAIL_INSTS = makeEmailInstances()
print ("DONE.\n\nNext, grabbing information from Facebook. A window will open up in your browswer for facebook verification, and then take you to a programsinformationpeople website, copy and paste the url AT THE TOP into the terminal.\n")
POST_INSTS = makePostInstances()
print ("\n\nLastly, grabbing data from YouTube. Copy and paste the link given into your browser and follow the steps to copy and paste the given code into the terminal:\n")
ACTIVITY_INSTS = makeActivityInstances()
print ("-------------------------------------------------------------------------------------------------------")
print ("\n\nDone grabbing data. Starting by creating a pie graph of gmail use by day (and storing data in sqlite) using PANDAS...")
gmailPandas(EMAIL_INSTS)
print ("-------------------------------------------------------------------------------------------------------")
print ("\n\nDone with Gmail. Next, creating a pie graph of youtube use by day (and storing data in sqlite)  using plot.ly...")
youtubeGraph(ACTIVITY_INSTS)
print ("-------------------------------------------------------------------------------------------------------")
print ("\n\nDone with Youtube. Next, using primary API (facebook) to create pie graph of posts by day AND time...")
facebookGraph(POST_INSTS)
print ("-------------------------------------------------------------------------------------------------------")
print ("\n\nDone with facebook. Now, combining all data into a bar graph to see how much you post based on weather from darkSky API...")
darkSkyGraph(EMAIL_INSTS, ACTIVITY_INSTS, POST_INSTS)
print ("\n\nView dark sky graph on plot.ly here: https://plot.ly/~jackclegg2/6")
print ("-------------------------------------------------------------------------------------------------------")
print ("\n\nProject completed. Thanks.")
