import unittest
import tweepy
import requests
import json
import twitter_info

## SI 206 - HW
## MY NAME: Jack Clegg (jrclegg)
## COMMENT WITH:
## Your section day/time: Thur 6-7pm
## Any names of people you worked with on this assignment: n/a


## Write code that uses the tweepy library to search for tweets with three different phrases of the
## user's choice (should use the Python input function), and prints out the Tweet text and the
## created_at value (note that this will be in GMT time) of the first FIVE tweets with at least
## 1 blank line in between each of them, e.g.


## You should cache all of the data from this exercise in a file, and submit the cache file
## along with your assignment.

## So, for example, if you submit your assignment files, and you have already searched for tweets
## about "rock climbing", when we run your code, the code should use CACHED data, and should not
## need to make any new request to the Twitter API.  But if, for instance, you have never
## searched for "bicycles" before you submitted your final files, then if we enter "bicycles"
## when we run your code, it _should_ make a request to the Twitter API.

## Because it is dependent on user input, there are no unit tests for this -- we will
## run your assignments in a batch to grade them!

## We've provided some starter code below, like what is in the class tweepy examples.

##SAMPLE OUTPUT
## See: https://docs.google.com/a/umich.edu/document/d/1o8CWsdO2aRT7iUz9okiCHCVgU5x_FyZkabu2l9qwkf8/edit?usp=sharing

## **** For extra credit, create another file called twitter_info.py that
## contains your consumer_key, consumer_secret, access_token, and access_token_secret,
## import that file here.  Do NOT add and commit that file to a public GitHub repository.

## **** If you choose not to do that, we strongly advise using authentication information
## for an 'extra' Twitter account you make just for this class, and not your personal
## account, because it's not ideal to share your authentication information for a real
## account that you use frequently.

## Get your secret values to authenticate to Twitter. You may replace each of these
## with variables rather than filling in the empty strings if you choose to do the secure way
## for EC points

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret

## Set up your authentication to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Set up library to grab stuff from twitter with your authentication, and
# return it in a JSON-formatted way

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## Write the rest of your code here!
import sys
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
#### Recommended order of tasks: ####
## 1. Set up the caching pattern start -- the dictionary and the try/except
## 		statement shown in class.
cache_fname = "cache_tweepy.json"
try:
    cache_file = open(cache_fname, 'r')
    cache_contents = cache_file.read()
    cache_diction = json.loads(cache_contents)
    cache_file.close()
except:
    cache_diction = {}

## 2. Write a function to get twitter data that works with the caching pattern,
## 		so it either gets new data or caches data, depending upon what the input
##		to search for is.
def getWithCaching(searchTerm):
    if searchTerm in cache_diction:
        uprint ("Grabbing data from cache.")
        return cache_diction[searchTerm]
    else:
        uprint ("Making request for search...")
        #try:
        cache_diction[searchTerm] = api.search(q = searchTerm, count = 5)
        writeFile = open(cache_fname, 'w')
        dumpedCacheDiction = json.dumps(cache_diction)
        writeFile.write(dumpedCacheDiction)
        writeFile.close()
        return cache_diction[searchTerm]
        #except:
        #    uprint ("Error. Search wasn't in cache and not valid.")
        #    return None

## 3. Using a loop, invoke your function, save the return value in a variable, and explore the
##		data you got back!
i = 0
while (i < 3):
    userSearch = input("Enter Tweet term: ")
    twitterDict = getWithCaching(userSearch)
    listOfTweets = twitterDict['statuses']
    for tweet in listOfTweets:
        uprint ("TEXT: " + tweet['text'])
        uprint ("CREATED AT:  " + tweet['created_at'] + '\n' )
    i += 1

## 4. With what you learn from the data -- e.g. how exactly to find the
##		text of each tweet in the big nested structure -- write code to print out
## 		content from 5 tweets, as shown in the linked example.
