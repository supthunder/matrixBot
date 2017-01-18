#!/usr/bin/env python 
from bs4 import BeautifulSoup
import requests
import re
import json
import urllib.request
from time import gmtime, strftime
import tweepy
from tokens import *
import os

# setup twitter
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
api = tweepy.API(auth)
username = ""
tweetId = ""

def tweet(imageName):
    tweet = "@"+username+"\n"
    tweet += "Converted Image:\n"
    tweet += strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(tweet)
    api.update_with_media(imageName,status=tweet,in_reply_to_status_id=tweetId)
    os.remove(imageName)


def getImageName(imageLink):
	nameRegex = re.compile('[^/]*$')
	imageName = "./"
	imageName += re.search(nameRegex, imageLink).group(0)
	return imageName

def getMentions():
	imageUrl = ""
	mentions = api.mentions_timeline(count=1)
	global username
	global tweetId
	for mention in mentions:
		imageUrl = mention.entities['media'][0]['media_url']
		username = mention.user.screen_name
		tweetId = mention.id

	imageName = getImageName(imageUrl)
	urllib.request.urlretrieve(imageUrl, imageName)
	return imageName
        


def uploadImage(url, image):

	file = {'image': open(image,'rb')}
	r  = requests.post(url, files=file)
	soup = BeautifulSoup(r.text,"html.parser")

	imageLink = (soup.find(bgcolor='black')).find('img')['src']
	# nameRegex = re.compile('[^/]*$')
	# imageName = "./"


	# imageName += re.search(nameRegex, imageLink).group(0)
	imageName = getImageName(imageLink)
	urllib.request.urlretrieve(imageLink, imageName)
	tweet(imageName)

def main():
	url = "http://www.text-image.com/convert/matrix.cgi"
	image = getMentions()
	uploadImage(url,image)
	os.remove(image)
main()
