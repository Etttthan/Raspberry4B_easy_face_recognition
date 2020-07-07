#encoding:utf-8
import RPi.GPIO as GPIO
import time
from time import sleep
time_out=1
Infrared=20


GPIO.setmode(GPIO.BCM)
GPIO.setup(Infrared,GPIO.IN)



while True:
    if(GPIO.input(Infrared)==True):
        print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" Smoe is here !")
    else:
        print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" Nobody !")
    time.sleep(time_out)
        

GPIO.cleanup()



