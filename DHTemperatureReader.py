import Adafruit_DHT
import time
import urllib
import requests

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
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field1="+str(tm)
        print urllib.urlopen(url).read()
        time.sleep(30)
        url = "https://api.thingspeak.com/update?api_key=LJ4VRHELTZKXIIXK&field2="+str(hu)
        print urllib.urlopen(url).read()
        requestmsg = "{'name' : 'bedroom','temperatureReading' : 10.3,'timestamp' : }"
        r = requests.post("http://bugs.python.org", data=requestmsg)
        print("POST Response" + r.status_code, r.reason)
    except IOError:
        print "ERROR WHILE POSTING DATA!"
    return "OK"

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
