#!/usr/bin/env python2

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

#Call script
print datetime.datetime.now() , "starting rssi_check.sh"
os.system("/root/base_monitor/rssi_check.sh")

# function to read
def read_rssi():
  if DEBUG:
    print "Reading rssi..."
  return subprocess.check_output(["awk '{print $1}' rssi.out"], shell=True)

# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastream(feed):
  try:
    datastream = feed.datastreams.get("rem_base_rssi")
    if DEBUG:
      print "Found existing datastream"
    return datastream
  except:
    if DEBUG:
      print "Creating new datastream"
    datastream = feed.datastreams.create("rem_base_rssi", tags="rssi_01")
    return datastream

# main program entry point - runs continuously updating the datastream

def run():
  
  feed = api.feeds.get(FEED_ID)

  datastream = get_datastream(feed)
  datastream.max_value = None
  datastream.min_value = None

  while True:
    os.system("/root/base_monitor/rssi_check.sh")
    rem_base_rssi = read_rssi()

    if DEBUG:
      print "Updating Xively feed with value: %s" % rem_base_rssi

    datastream.current_value = rem_base_rssi
    datastream.at = datetime.datetime.utcnow()
    try:
      datastream.update()
    except requests.HTTPError as e:
      print datetime.datetime.now() , "HTTPError({0}): {1}".format(e.errno, e.strerror)
    time.sleep(60)

run()
