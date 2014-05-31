#!/bin/sh
/usr/bin/gawk -n '{printf $1/46}' /sys/class/dnt900/0x001308/ADC2 > adc2.out
