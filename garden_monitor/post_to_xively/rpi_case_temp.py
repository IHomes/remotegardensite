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
print datetime.datetime.now() , "starting gather_rpi_case_temp.py"
execfile("/root/garden_monitor/RPi_case_temp/gather_rpi_case_temp.py")


# function to read
def read_loadavg():
  if DEBUG:
    print "Reading rpi case temp..."
  return subprocess.check_output(["awk '{print $1}' lastread_rpi_temp.out"], shell=True)

# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastream(feed):
  try:
    datastream = feed.datastreams.get("rpi_case")
    if DEBUG:
      print "Found existing datastream"
    return datastream
  except:
    if DEBUG:
      print "Creating new datastream"
    datastream = feed.datastreams.create("rpi_case", tags="rpi_01")
    return datastream

# main program entry point - runs continuously updating the datastream 
def run():

  feed = api.feeds.get(FEED_ID)

  datastream = get_datastream(feed)
  datastream.max_value = None
  datastream.min_value = None

  while True:
    execfile("/root/garden_monitor/RPi_case_temp/gather_rpi_case_temp.py")
    rpi_case = read_loadavg()

    if DEBUG:
      print "Updating Xively feed with value: %s" % rpi_case

    datastream.current_value = rpi_case
    datastream.at = datetime.datetime.utcnow()
    try:
      datastream.update()
    except requests.HTTPError as e:
      print datetime.datetime.now() , "HTTPError({0}): {1}".format(e.errno, e.strerror)
    time.sleep(300)

run()
