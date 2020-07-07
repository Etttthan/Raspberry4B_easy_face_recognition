import RPi.GPIO as GPIO
import time
from time import sleep

address_gpio = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(address_gpio, GPIO.OUT)

GPIO.output(address_gpio, GPIO.HIGH)
#sleep(5)
#GPIO.output(address_gpio, GPIO.LOW)