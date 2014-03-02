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

FEED_ID = 1824193320
API_KEY = '2XCKLDtPAJdKhzLMAxd9FTIpPfVu4trJIhSENMsbAiYJYxze'
DEBUG =''

# initialize api client
api = xively.XivelyAPIClient(API_KEY)

#Call Thermometer script
#execfile("/root/garden_monitor/soil_monitor/moistSHT1x")
os.system("/root/garden_monitor/soil_monitor/moistSHT1x")

# function to read 1 minute load average from system uptime command
def read_loadavg():
  if DEBUG:
    print "Reading soil moisture..."
  return subprocess.check_output(["awk '{print $1}' lastread_soil_moist.out"], shell=True)

# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastream(feed):
  try:
    datastream = feed.datastreams.get("soil_moist")
    if DEBUG:
      print "Found existing datastream"
    return datastream
  except:
    if DEBUG:
      print "Creating new datastream"
    datastream = feed.datastreams.create("soil_moist", tags="soil_01")
    return datastream

# main program entry point - runs continuously updating our datastream with the
# current 1 minute load average
def run():
  print "Starting Xively tutorial script"

  feed = api.feeds.get(FEED_ID)

  datastream = get_datastream(feed)
  datastream.max_value = None
  datastream.min_value = None

  while True:
    soil_moist = read_loadavg()

    if DEBUG:
      print "Updating Xively feed with value: %s" % soil_moist

    datastream.current_value = soil_moist
    datastream.at = datetime.datetime.utcnow()
    try:
      datastream.update()
    except requests.HTTPError as e:
      print "HTTPError({0}): {1}".format(e.errno, e.strerror)
    os.system("/root/garden_monitor/soil_monitor/moistSHT1x")
    time.sleep(10)

run()
