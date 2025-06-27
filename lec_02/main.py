from machine import Pin
from time import sleep

# Define LED pins (from LSB to MSB)
led_pins = [Pin(15, Pin.OUT), Pin(14, Pin.OUT), Pin(13, Pin.OUT), Pin(12, Pin.OUT)]

while True:
    for count in range(16):  # Count from 0 to 15
        for bit in range(4):
            led_pins[bit].value((count >> bit) & 1)
        sleep(0.5)  # 500 ms delay
