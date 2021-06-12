import os
import Adafruit_DHT
import time
import http.client
import requests
import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

tm = 0
hu = 0
token = "wt3xcNU-JXTRgFZpBVA5CEI78M4uOO-5PViTN-P6T3rXCog-UZpS8Ts5lw3shULA4gQeprnlREfCwQ71j2Y1XA=="
org = "alan.mangroo@gmail.com"
bucket = "Temperatures"
client = InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token)

def dhTemp():
    humidity, temperature = Adafruit_DHT.read_retry(22, 4)
    print ('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
    global tm 
    tm = temperature
    global hu
    hu = humidity
    return temperature

def post_data(temp):
    global tm
    global hu
    try:
        print ("About to post temperature")
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field1="+str(tm)
        conn = http.client.HTTPSConnection("api.thingspeak.com")
        conn.request("GET", url)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = "temperature,location=bedroom1 value="+str(tm)
        write_api.write(bucket, org, data)
        print("Start wait")
        time.sleep(60)
        print("End wait")

        print ("About to post humidity")
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field2="+str(hu)
        conn = http.client.HTTPSConnection("api.thingspeak.com")
        conn.request("GET", url)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = "humidity,location=bedroom1 value="+str(hu)
        write_api.write(bucket, org, data)
        print("Start wait2")
        time.sleep(60)
        print("End wait2")


    except IOError:
        print ("ERROR WHILE POSTING DATA!")
    except Exception:
        print (" 2 ERROR WHILE POSTING DATA!")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        return "OK"

while True:
    try:
        t = str(dhTemp())
        resp = post_data(t)
        print("post_data response :" + resp)
        print("Temperature posted :" + t)
        f= open('output.csv','a')
        f.write(time.strftime("%H:%M:%S") + ',' )
        f.write(t)
        f.write('\n')
        f.close()
        print("Start wait3")
        time.sleep(60)
        print("End wait3")
        sys.stdout.flush()
    except Exception:
        print ("ERROR IN WHILE!")
