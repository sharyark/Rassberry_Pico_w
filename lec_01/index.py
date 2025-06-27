from machine import Pin
from time import sleep
green_led = Pin(15,Pin.OUT)
blue_led = Pin(14,Pin.OUT)

while True:
    green_led.value(1)
    sleep(.3)
    green_led.value(0)
    sleep(.3)
    blue_led.value(1)
    sleep(.3)
    blue_led.value(0)
    sleep(.3)
