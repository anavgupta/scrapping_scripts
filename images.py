#!/usr/bin/env python3

import requests
import os
from xml.etree import ElementTree as ET
# To download the images
import urllib

# Images used by Momentum Cloudfront
URL = 'https://d3cbihxaqsuq0s.cloudfront.net/'

# The name space for the xml webpage
xmlns = "{http://s3.amazonaws.com/doc/2006-03-01/}"


# This will connect to the website and return the webpage
# This function might create an overhead incase the website is down
# or the path is broken
def get_webpage(url):
    r = requests.get(url)
    while r.status_code != 200:
        print("Connecting \n")
        r = requests.get(url)
    return r.text


# Function downloads the Image on the URL with a specified name
def download_image(url, count):
    print "Downloading {} image".format(count)
    urllib.urlretrieve(url, "%05d.jpg" % count)


# Parses the main web page for images path
def parse_webpage(text):
    root = ET.fromstring(text)
    print '1'
    keyList = []
    key = '{}Key'.format(xmlns)

    # Get the path to all images
    for content in root.findall('{}Contents'.format(xmlns)):
        for child in content:
            if child.tag == key:
                keyList.append(child.text)

    # Creates a new directory
    os.mkdir('Images')
    os.chdir('./Images')

    # For all paths available download the image
    for count, path in enumerate(keyList):
        url = URL + path
        download_image(url, count)


# It calls all the required functions
if __name__ == '__main__':
    text = get_webpage(URL)
    parse_webpage(text)
