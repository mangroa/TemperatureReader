import os

import time
import urllib

os.system('modprobe w1-gpio')

os.system('modprobe w1-therm')


temp_sensor ='/sys/bus/w1/devices/28-0000066ee2e3/w1_slave'

def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

def post_data(temp):
    try:
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field1="+temp
        response = urllib.urlopen(url).read()
    except IOError:
        print "ERROR WHILE POSTING DATA!"
    return response

while True:
    t = str(read_temp())
    resp = post_data(t)
    print(resp)
    print(t)
    f= open('temp.csv','a')
    f.write(time.strftime("%H:%M:%S") + ',' )
    f.write(t)
    f.write('\n')
    f.close()
    time.sleep(60)
