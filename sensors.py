from time import sleep
import os
import glob
from datetime import datetime

import RPi.GPIO as GPIO
import Adafruit_MCP3008
import Adafruit_DHT

import requests

URL = "http://192.168.1.227:8080/api/sensors/data"

#soil moisture sensor
am = Adafruit_MCP3008.MCP3008(clk = 11, cs = 8, miso = 9, mosi = 10)

#air temperature and humidity sensor
DHT_SENSOR = 22
DHT_PIN = 3

#these two lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_path = glob.glob(base_dir + '28*')[0] #get file path of sensor
rom = device_path.split('/')[-1] #get rom name

def read_temp_raw():
    with open(device_path +'/w1_slave','r') as f:
        valid, temp = f.readlines()
    return valid, temp

def read_temp():
    valid, temp = read_temp_raw()

    while 'YES' not in valid:
        time.sleep(0.2)
        valid, temp = read_temp_raw()

    pos = temp.index('t=')
    if pos != -1:
        #read the temperature .
        temp_string = temp[pos+2:]
        temp_celcius = float(temp_string)/1000.0
        return temp_celcius


def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

while True:
    soil_temp = read_temp()
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    moisture_value = am.read_adc(0)
    sensor_dry = 830
    sensor_wet = 1024
    moisture_percentage = map(moisture_value, sensor_dry,sensor_wet,0,100)
    if(moisture_percentage < 0):
        moisture_percentage = (moisture_percentage * -1)

    print("Air Temperature: {0:0.2f}*C".format(temperature))
    print("Air Humidity: {0:0.1f}%".format(humidity))
    print('Soil Temperature: {:,.2f}*C'.format(soil_temp))
    print('Soil Moisture: {0:0.1f}%'.format(moisture_percentage))

    data = {
    'sensorId': 1,
    'airTemperature':temperature,
    'airHumidity': humidity,
    'soilTemperature': soil_temp,
    'soilMoisture':moisture_percentage,
    'measurementTimestamp': datetime.now()
    }

    print(data)

    requests.post(url = URL, data = data)

    sleep(10)
