import facebook
import requests
import json
import sys
import datetime
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
        else:
            self.created = ""
        if 'likes' in post_dict:
            self.likes=post_dict['likes']['data']
            self.like_count=len(post_dict['likes']['data'])
        else:
            self.likes=[]
            self.like_count=0
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
print (len(makePostInstances()))
def dictPostsByDay(post_insts):
    dictPosts = {}
    for x in post_insts:
        createdTime = x.created
        dayOfWeek = convertToDayOfWeek(createdTime)
        dictPosts[dayOfWeek] = dictPosts.get(dayOfWeek, 0) + 1
    return dictPosts
print (dictPostsByDay(makePostInstances()))
