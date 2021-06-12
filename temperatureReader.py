import os

import time
import http.client
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

os.system('modprobe w1-gpio')

os.system('modprobe w1-therm')


temp_sensor ='/sys/bus/w1/devices/28-0000066ee2e3/w1_slave'

token = "wt3xcNU-JXTRgFZpBVA5CEI78M4uOO-5PViTN-P6T3rXCog-UZpS8Ts5lw3shULA4gQeprnlREfCwQ71j2Y1XA=="
org = "alan.mangroo@gmail.com"
bucket = "Temperatures"

client = InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token)

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
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field3="+temp
        print("GET URL : " + url);
        conn = http.client.HTTPSConnection("api.thingspeak.com")
        conn.request("GET", url)
        r1 = conn.getresponse()
        conn.close()
        print(r1.status, r1.reason)

        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = "temperature,location=garden value="+temp
        write_api.write(bucket, org, data)

    except IOError:
        print ("ERROR WHILE POSTING DATA!")
    return r1

while True:
    try:
        t = str(read_temp())
        resp = post_data(t)
        print(t)
        f= open('output.csv','a')
        f.write(time.strftime("%H:%M:%S") + ',' )
        f.write(t)
        f.write('\n')
        f.close()
        time.sleep(60)
    except Exception:
        print ("ERROR IN WHILE!")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
