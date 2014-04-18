#!/usr/bin/env python2
#borrowed from http://skding.blogspot.com/2014/02/plotly-and-pi.html
import time
import plotly
import os
import subprocess
import datetime

def update_temp():
  py = plotly.plotly(username_or_email='geekskunk', key='m5b6vstz34')
  i = datetime.datetime.now()
  proc = subprocess.Popen(["cat", "/sys/class/thermal/thermal_zone0/temp"], stdout=subprocess.PIPE)
  t = proc.stdout.read()
  r =  py.plot(i.strftime('%Y-%m-%d %H:%M:%S'),float(t)/1000,
  filename='RPiBaseCPU',
  fileopt='extend',
  layout={'title': 'Base Station RPi CPU Temperature History'})

if __name__ == '__main__':
  import sys
  update_temp()
 
