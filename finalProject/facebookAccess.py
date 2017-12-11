import facebook
import requests
import json
import sys
import datetime
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import sqlite3
import gmplot

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
#TODO: add oauth to get users token yourself
token = 'EAACEdEose0cBADGb3gAMhwArsZAht1uLPDBpqKzjrWkFgvZAtB7mxNGXeNWYxyJMen3vW0fZAZBsYYiQ22IHXrVZAFqsurArV5gRTqQR2gw900hZBrEGXl9ZAoZCa2RCoAcArMoOjVG9hZBKIG8lZA3gxdJrdaYcdP2n97pugEpcHhZAOJitpBVT4Jao36Sf2Da0ZCQZD'

import json
import webbrowser
import unittest
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
APP_ID     = '1868926506720280'
APP_SECRET = '371b6ae794e3d9ef58ebb4e9b2ae1850'
facebook_session = False

CACHE_FNAME = "206finalProjectCache.json"
# Put the rest of your caching setup here:
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

# Reference: https://requests-oauthlib.readthedocs.io/en/latest/examples/facebook.html
def makeFacebookRequest(baseURL, params = {}):
    global facebook_session
    if not facebook_session:
        # OAuth endpoints given in the Facebook API documentation
        authorization_base_url = 'https://www.facebook.com/dialog/oauth'
        token_url = 'https://graph.facebook.com/oauth/access_token'
        redirect_uri = 'https://www.programsinformationpeople.org/runestone/oauth'

        scope = ['user_posts','pages_messaging','user_managed_groups','user_status','user_likes']
        facebook = OAuth2Session(APP_ID, redirect_uri=redirect_uri, scope=scope)
        facebook_session = facebook_compliance_fix(facebook)

        authorization_url, state = facebook_session.authorization_url(authorization_base_url)
        print('Opening browser to {} for authorization'.format(authorization_url))
        webbrowser.open(authorization_url)

        redirect_response = input('Paste the full redirect URL here: ')
        facebook_session.fetch_token(token_url, client_secret=APP_SECRET, authorization_response=redirect_response.strip())

    return facebook_session.get(baseURL, params=params)

class Post():
    """object representing status update"""
    def __init__(self, post_dict={}):
        #added variables .comment_count and .like_count below to use in number 8
        self.id = post_dict['id']
        if 'message' in post_dict:
            self.message = post_dict['message']
        else:
            self.message = ""
        if 'comments' in post_dict:
            self.comments=post_dict['comments']['data']
            self.comment_count=len(post_dict['comments']['data'])
        else:
            self.comments=[]
            self.comment_count=0
        if 'created_time' in post_dict:
            self.created = post_dict['created_time']
            self.hour = int(self.created.split('-')[2][3:5])
        else:
            self.created = ""
        if 'likes' in post_dict:
            self.likes=post_dict['likes']['data']
            self.like_count=len(post_dict['likes']['data'])
        else:
            self.likes=[]
            self.like_count=0
class Event():
    def __init__(self, event_dict = {}):
        self.name = event_dict['name']
        self.id = event_dict['id']
        if 'place' in event_dict:
            if 'name' in event_dict['place']:
                self.locationName = event_dict['place']['name']
        else:
            self.locationName = None
        try:
            google_base = 'https://maps.googleapis.com/maps/api/geocode/json'
            google_params = {'key':'AIzaSyCV5kR3NE6UFCuGZurrxalxtHPG2H-J7uY', 'address':'{}'.format(self.locationName)}
            requesting = requests.get(google_base, params=google_params)
            loading = requesting.text.encode('utf-8')
            googlejson = json.loads(loading)
            self.lat = googlejson['results'][0]['geometry']['location']['lat']
            self.long = googlejson['results'][0]['geometry']['location']['lng']
        except:
            self.lat = None
            self.long = None

def createSQL():
    conn = sqlite3.connect("206finalProject.sqlite")
    cur = conn.cursor()
    try:
        cur.execute("""CREATE TABLE Facebook (
            `id`	TEXT NOT NULL,
            `created_time`	TEXT NOT NULL,
            'like_count' TEXT NOT NULL,
            'comment_count' TEXT NOT NULL,
            PRIMARY KEY(`id`)
        )""")
    except:
        pass
    conn.commit()
    conn.close()
def sqlTable(post_insts):
    conn = sqlite3.connect("206finalProject.sqlite")
    cur = conn.cursor()
    for x in post_insts:
        try:
            id = x.id
            created_time = x.created
            like_count = x.like_count
            comment_count = x.comment_count
            cur.execute("INSERT INTO Facebook VALUES (?,?,?,?)", (id, created_time, like_count, comment_count))
            conn.commit()
        except:
            pass
    conn.close()
def makeEventsInstances():
    baseurl = 'https://graph.facebook.com/me/events'
    events = makeFacebookRequest(baseurl, {'limit':100}).text.encode('utf-8')
    my_events = json.loads(events)
    event_insts = [Event(x) for x in my_events['data']]
    return event_insts
def makeMap(event_insts):
    latitude = []
    longitude = []
    for x in event_insts:
        if (x.lat != None) and (x.long != None):
            latitude.append(x.lat)
            longitude.append(x.long)
    gmap = gmplot.GoogleMapPlotter(latitude[0], longitude[0], 16)
    gmap.plot(latitude, longitude, '#FF6666', edge_width = 75)
    #gmap.scatter(latitude, longitude, '#FF6666', marker = True)
    gmap.draw('eventsmap.html')
    return
def makePostInstances():
    baseurl = 'https://graph.facebook.com/me/feed'
    posts=makeFacebookRequest(baseurl, {'limit':100, 'fields':'comments,likes,name,created_time'}).text.encode('utf-8')
    my_personal_feed=json.loads(posts)
    post_insts=[Post(x) for x in my_personal_feed['data']]
    return post_insts
def convertToDayOfWeek(dateTimeString):
    splitString = dateTimeString.split('-')
    year = int(splitString[0])
    month = int(splitString[1])
    day = splitString[2]
    day = int(day[0:2])
    DayL = ['Mon','Tues','Wednes','Thurs','Fri','Satur','Sun']
    date = DayL[datetime.date(year,month,day).weekday()] + 'day'
    return date
def dictPostsByDay(post_insts):
    dictPosts = {}
    for x in post_insts:
        createdTime = x.created
        dayOfWeek = convertToDayOfWeek(createdTime)
        dictPosts[dayOfWeek] = dictPosts.get(dayOfWeek, 0) + 1
    return dictPosts
def dictPostsByDayTime(post_insts):
    dictPostsTime = {}
    for x in post_insts:
        createdHour = x.hour
        createdDay = convertToDayOfWeek(x.created)
        if (createdHour > 0) and (createdHour <= 5):
            createdString = createdDay + '00:00 - 5:59'
        if (createdHour > 5) and (createdHour <= 11):
            createdString = createdDay + '5:59 - 11:59'
        if (createdHour > 11) and (createdHour <= 17):
            createdString = createdDay + '12:00 - 17:59'
        if (createdHour > 17) and (createdHour <= 24):
            createdString = createdDay + '18:00 - 23:59'
        dictPostsTime[createdString] = dictPostsTime.get(createdString, 0) + 1
    return dictPostsTime
def facebookGraph():
    createSQL()
    postInstances = makePostInstances()
    sqlTable(postInstances)
    dictPosts = dictPostsByDayTime(postInstances)
    plotly.tools.set_credentials_file(username = 'jackclegg2', api_key = 'B3K9rQ0xP0e9RQYjtDvT')
    fbKeys, fbValues = zip(*dictPosts.items())
    trace = go.Pie(labels = fbKeys, values = fbValues)
    py.iplot([trace], filename = 'fbattempt')
    print ("Created pie chart of Facebook activity by day! View at the link here: https://plot.ly/~jackclegg2/2/")
facebookGraph()
