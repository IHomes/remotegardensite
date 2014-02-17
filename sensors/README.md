# Sensors used in the projects
-Air Temp Sensor (DS1820)
-Ground Temp Sensor (SHT10)
-Soil Moisture Sensor (SHT10)
-Pi Onboard CPU Temp (onboard/vcgencmd)
-Pi Camera (camera/raspistill)


## DS18B20
An i2c Digital temperature sensor (I happened to use adafruit Waterproof DS18B20 Digital temperature sensor + extras) for this project.

Each has a unique address, found with steps below. Script would need updating if you have more than of this type of sensor, reflecting the specific serial number perhaps

```
sudo modprobe w1-gpio
sudo modprobe w1-therm
cd /sys/bus/w1/devices
ls
cd 28-* #unique serial number for device, if you add multiple make sure to keep track of them
cat w1_slave  #indicates if temp can be provided in first line, temp in second.
```

Python script in this repo (thermometer.py) from this tutorial: 
http://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing

To run program:
```
cd DS18B20
python thermometer.py
```

## SH10
An i2c Soil/Moisture (humidity) sensor (again, I happened to use adafruit offering)

No-unique address, multiple *may* be possible with unique data lines

Followed this exactly:
http://www.john.geek.nz/2012/08/reading-data-from-a-sensirion-sht1x-with-a-raspberry-pi/

Requires BCM2835 library (included as-used in this repo, but latest: http://www.open.com.au/mikem/bcm2835 )

If used version of BCM2835 from this repo:

```
cd ./SHT10/support_files/bcm2835-1.36
./configure
make
sudo make check
sudo make install
```

To build program 

```
cd ../.. #SHT10
gcc -o RPi_SHT1x ./support_files/bcm2835-1.36/src/bcm2835.c ./RPi_SHT1x.c testSHT1x.c
```

To run program:

```
cd SHT10
./RPi_SHT1x
```
## Raspberry Pi Onboard Sensors

Ref: http://elinux.org/RPI_vcgencmd_usage


To list CPU core temp:

```
/opt/vc/bin/vcgencmd measure_temp
# or
gawk '{print $1/1000,"degrees C"}' /sys/class/thermal/thermal_zone0/temp
```


## Pi Camera

Script to grab an image every 30 seconds, Ref: http://www.stuffaboutcode.com/2013/05/time-lapse-video-with-raspberry-pi.html

```
cd camera
capturetimelapse_30secInt.sh
```


