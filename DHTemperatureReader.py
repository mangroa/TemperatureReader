import os

import time
import urllib

import sys
import Adafruit_DHT

t = 0
h = 0

def dhTemp():
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
    t = temperature
    h = humidity
    return temperature

def post_data(temp):
    try:
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field1="+t
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field2="+h
        response = urllib.urlopen(url).read()
    except IOError:
        print "ERROR WHILE POSTING DATA!"
    return response

while True:
    try:
        t = str(dhTemp())
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
