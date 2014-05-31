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

#Call script
print datetime.datetime.now() , "starting adc2_check.sh"
os.system("/root/base_monitor/adc2_check.sh")

# function to read
def read_volt():
  if DEBUG:
    print "Reading adc2 voltage..."
  return subprocess.check_output(["awk '{print $1}' adc2.out"], shell=True)

# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastream(feed):
  try:
    datastream = feed.datastreams.get("bat_voltage")
    if DEBUG:
      print "Found existing datastream"
    return datastream
  except:
    if DEBUG:
      print "Creating new datastream"
    datastream = feed.datastreams.create("bat_voltage", tags="adc2_01")
    return datastream

# main program entry point - runs continuously updating the datastream

def run():
  
  feed = api.feeds.get(FEED_ID)

  datastream = get_datastream(feed)
  datastream.max_value = None
  datastream.min_value = None

  while True:
    os.system("/root/base_monitor/adc2_check.sh")
    bat_voltage = read_volt()

    if DEBUG:
      print "Updating Xively feed with value: %s" % bat_voltage

    datastream.current_value = bat_voltage
    datastream.at = datetime.datetime.utcnow()
    try:
      datastream.update()
    except requests.HTTPError as e:
      print datetime.datetime.now() , "HTTPError({0}): {1}".format(e.errno, e.strerror)
    time.sleep(5400)

run()
