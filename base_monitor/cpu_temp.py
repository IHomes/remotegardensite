#!/usr/bin/env python2

import sys
import syslog
import json
import os
import xively
import subprocess
import time
import datetime
import requests

# extract feed_id and api_key from environment variables
#FEED_ID = os.environ["FEED_ID"]
#API_KEY = os.environ["API_KEY"]
#DEBUG = os.environ["DEBUG"] or false

FEED_ID = 1246053635
API_KEY = 'KBDxZyb8EQlldInIuUBITlC92ABbcqjo0QGU4hzS8wW2w6hz'
DEBUG =''

# initialize api client
api = xively.XivelyAPIClient(API_KEY)

#Call /opt/vc/bin/vcgencmd
print datetime.datetime.now() , "starting get cputemp"

def getCPUtemperature():
    res = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastream(feed):
  try:
    datastream = feed.datastreams.get("cpu_temp")
    if DEBUG:
      print "Found existing datastream"
    return datastream
  except:
    if DEBUG:
      print "Creating new datastream"
    datastream = feed.datastreams.create("cpu_temp", tags="cpu_02")
    return datastream

# main program entry point - runs continuously updating the datastream
def run():

  feed = api.feeds.get(FEED_ID)

  datastream = get_datastream(feed)
  datastream.max_value = None
  datastream.min_value = None

  while True:
    cpu_temp = getCPUtemperature()

    if DEBUG:
      print "Updating Xively feed with value: %s" % cpu_temp

    datastream.current_value = cpu_temp
    datastream.at = datetime.datetime.utcnow()
    try:
      datastream.update()
    except requests.HTTPError as e:
      print datetime.datetime.now() , "HTTPError({0}): {1}".format(e.errno, e.strerror) , datetime.datetime.now()
    time.sleep(300)

run()
