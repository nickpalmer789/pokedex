#!/usr/bin/env python
#Import packages
from requests import exceptions
import argparse
import requests
import cv2
import os

#Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
                help="Search query to search the bing API for.")
ap.add_argument("-o", "--output", required=True,
                help="Path to output directory of images.")
args = vars(ap.parse_args())

#Set up some constants
API_KEY = "21b83c0ce9894c468b10058dc559b843"
MAX_RESULTS = 250 #The number of results to get at max
GROUP_SIZE = 50 #The number of results per "page" should divide MAX_RESULTS
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

#A list of exceptions that can be thrown when downloading images
#We will try to handle these gracefully later
EXCEPTIONS = set([IOError, FileNotFoundError,
                exceptions.RequestException, exceptions.HTTPError,
                exceptions.ConnectionError, exceptions.Timeout])

#Set up objects for the search
term = args["query"]
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q" : term, "offset" : 0, "count" : GROUP_SIZE}

#Make the search
print("[INFO] searching the Bing API for '{}'".format(term))
search = requests.get(URL, headers=headers, params=params)

#Check the validity of the request
search = raise_for_status()

#Get the actual results and the estimated number of results
results = search.json()
estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)

print("[INFO] {} toal results for '{}'".format(estNumResults, term))

#Track the total number of images downloaded
totalDownloaded = 0

#Loop over the estimated number of results in chunks of group_size
for offset in range(0, estNumResults, GROUP_SIZE):
    #Update the search parameters using the current offset
    #Make the request to fetch the results
    print("[INFO] making request for group {}-{} of {}...".format(offset, 
            offset + GROUP_SIZE, estNumResults))

    #Make the request and verify validity of request
    params["offset"] = offset
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()

    results = search.json()

    print("[INFO] saving images for group {}-{} of {}...".format(offset, offset + GROUP_SIZE, estNumResults))
    
    #Loop over the results and try to save each image
    for v in results["value"]:
        #Try to download the image
        try:
            #Make a request to download the image
            print("[INFO] fetching: {}".format(v["contentUrl"]))
            r = requests.get(v["contentUrl"], timeout=30)

            #Build the path to the output image
            
            










    














