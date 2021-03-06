import Adafruit_DHT
import time
import urllib
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
        requestmsg = "{'name' : 'bedroom','temperatureReading' : " + str(round(tm,2)) +",'timestamp' : " + str(int(time.time())*1000) + "}"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        print ("About to post " + requestmsg)
        #r = requests.post("http://54.252.155.149:8080/temperatureReading/temperatures", data=requestmsg, headers=headers)
        #print("POST Response" + str(r.status_code), r.reason)
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field1="+str(tm)
        print urllib.urlopen(url).read()
        time.sleep(60)
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field2="+str(hu)
        print urllib.urlopen(url).read()
        time.sleep(60)


    except IOError:
        print "ERROR WHILE POSTING DATA!"
    except Exception as e:
        print e.message
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
        print "ERROR IN WHILE!"
