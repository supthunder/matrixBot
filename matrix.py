#!/usr/bin/env python 
from bs4 import BeautifulSoup
import requests
import re
import json
import re
import urllib.request




def uploadImage(url):
	file = {'image': open('test.png','rb')}
	r  = requests.post(url, files=file)
	soup = BeautifulSoup(r.text,"html.parser")

	imageLink = (soup.find(bgcolor='black')).find('img')['src']
	nameRegex = re.compile('[^/]*$')
	imageName = "./"
	imageName += re.search(nameRegex, imageLink).group(0)
	urllib.request.urlretrieve(imageLink, imageName)

def main():
	url = "http://www.text-image.com/convert/matrix.cgi"
	uploadImage(url)
main()
