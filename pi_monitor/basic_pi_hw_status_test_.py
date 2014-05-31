#!/usr/bin/env python
import sys
import syslog
import json
import os
import xively
import subprocess
import time
import datetime
import requests

API_KEY = '25pEM5v7J7wA5iQvPNqoHgeXvUF8VaEOzQszR9VY80Xbtari'
FEED_ID = 1824193320
#DEBUG = os.environ["DEBUG"] or false
#API_URL = '/v2/feeds/{feednum}.xml' .format(feednum = FEED_ID)

# initialize api client
api = xively.XivelyAPIClient(API_KEY)


# extract feed_id and api_key from environment variables
#FEED_ID = os.environ["FEED_ID"]
#API_KEY = os.environ["API_KEY"]

def getCPUtemperature():
    res = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

CPU_temp = getCPUtemperature()
DISK_stats = getDiskSpace()
DISK_total = DISK_stats[0]
DISK_free  = DISK_stats[1]
DISK_perc  = DISK_stats[3]
RAM_stats = getRAMinfo()
RAM_total = round(int(RAM_stats[0]) / 1000,1)
RAM_used  = round(int(RAM_stats[1]) / 1000,1)
RAM_free  = round(int(RAM_stats[2]) / 1000,1)

# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastream1(feed):
  try:
    datastream1 = feed.datastreams.get("CPU_temp")
    if DEBUG:
      print ("Found existing datastream")
    return datastream1
  except:
    if DEBUG:
      print ("Creating new datastream")
    datastream1 = feed.datastreams.create("CPU_temp", tags="temp_01")
    return datastream


# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastream2(feed):
  try:
    datastream2 = feed.datastreams.get("DISK_free")
    if DEBUG:
      print ("Found existing datastream")
    return datastream2
  except:
    if DEBUG:
      print ("Creating new datastream")
    datastream2 = feed.datastreams.create("DISK_free", tags="disk_01")
    return datastream2



# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastream3(feed):
  try:
    datastream3 = feed.datastreams.get("RAM_used")
    if DEBUG:
      print ("Found existing datastream")
    return datastream3
  except:
    if DEBUG:
      print ("Creating new datastream")
    datastream3 = feed.datastreams.create("RAM_used", tags="ramu_01")
    return datastream3



# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastream4(feed):
  try:
    datastream4 = feed.datastreams.get("RAM_free")
    if DEBUG:
      print ("Found existing datastream")
    return datastream4
  except:
    if DEBUG:
      print ("Creating new datastream")
    datastream4 = feed.datastreams.create("RAM_free", tags="ramf_01")
    return datastream4


# main program entry point - runs continuously updating our datastream with the
# current 1 minute load average
def run():
  print ("Starting Xively tutorial script")
  
  feed = api.feeds.get(FEED_ID)

  datastream1 = get_datastream1(feed)
  datastream2 = get_datastream2(feed)
  datastream3 = get_datastream3(feed)
  datastream4 = get_datastream4(feed)
  datastream.max_value = None
  datastream.min_value = None

  while True:
    CPU_Temperature = CPU_temp

    if DEBUG:
      print ("Updating Xively feed with value: %s") % CPU_temp

    datastream.current_value = CPU_temp
    datastream.at = datetime.datetime.utcnow()
    try:
      datastream.update()
    except requests.HTTPError as e:
      print ("HTTPError({0}): {1}").format(e.errno, e.strerror)

    Disk_free = DISK_free

    if DEBUG:
      print ("Updating Xively feed with value: %s") % DISK_free

    datastream.current_value = DISK_free
    datastream.at = datetime.datetime.utcnow()
    try:
      datastream.update()
    except requests.HTTPError as e:
      print ("HTTPError({0}): {1}").format(e.errno, e.strerror)

    RAM_Used = RAM_used

    if DEBUG:
      print ("Updating Xively feed with value: %s") % RAM_used

    datastream.current_value = RAM_used
    datastream.at = datetime.datetime.utcnow()
    try:
      datastream.update()
    except requests.HTTPError as e:
      print ("HTTPError({0}): {1}").format(e.errno, e.strerror)

    RAM_Free = RAM_free

    if DEBUG:
      print ("Updating Xively feed with value: %s") % RAM_free

    datastream.current_value = RAM_free
    datastream.at = datetime.datetime.utcnow()
    try:
      datastream.update()
    except requests.HTTPError as e:
      print ("HTTPError({0}): {1}").format(e.errno, e.strerror)
    time.sleep(20)

run()
