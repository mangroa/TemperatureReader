import os

import time
import urllib

import sys
import Adafruit_DHT

tm = 0
hu = 0

def dhTemp():
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print "1"
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
    global tm 
    print "2"
    tm = temperature
    print "3"
    global hu
    print "4"
    hu = humidity
    print "5"
    return temperature

def post_data(temp):
    global tm
    global hu
    try:
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field1="+tm
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field2="+hu
        response = urllib.urlopen(url).read()
    except IOError:
        print "ERROR WHILE POSTING DATA!"
    return response

while True:
    try:
        print "6"
        t = str(dhTemp())
        print "7"
        resp = post_data(t)
        print(resp)
        print(t)
        f= open('temp.csv','a')
        f.write(time.strftime("%H:%M:%S") + ',' )
        f.write(t)
        f.write('\n')
        f.close()
        time.sleep(60)
    except Exception:
        print "ERROR IN WHILE!"
