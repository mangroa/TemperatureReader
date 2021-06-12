import Adafruit_DHT
import time
import http.client
import requests
import datetime

tm = 0
hu = 0

def dhTemp():
    humidity, temperature = Adafruit_DHT.read_retry(22, 4)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
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
        time.sleep(60)
        print ("About to post humidity")
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field2="+str(hu)
        conn = http.client.HTTPSConnection("api.thingspeak.com")
        conn.request("GET", url)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        time.sleep(60)


    except IOError:
        print ("ERROR WHILE POSTING DATA!")
    except Exception as e:
        print (e.message)
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
    except Exception:
        print ("ERROR IN WHILE!")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)