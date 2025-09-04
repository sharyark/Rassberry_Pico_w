from machine import Pin
import time
from machine import Timer

#this is how we run our code using timer
#like there is how we run code like parallel we can make multiple timers
led = Pin("LED", Pin.OUT)   # works on Pico / Pico 

def togle_led(Source):
    led.toggle()

on_board_timer = Timer(period=60,mode=Timer.PERIODIC,callback=togle_led)    


while True:
    pass

