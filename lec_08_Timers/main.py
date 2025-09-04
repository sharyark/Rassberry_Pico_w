from machine import Pin, Timer
import time

led = Pin("LED", Pin.OUT)   # For Pico W (use Pin(2) for ESP32/8266)

def toggle_led(timer):
    led.toggle()

# Create a timer with 60ms period
on_board_timer = Timer(period=60, mode=Timer.PERIODIC, callback=toggle_led)

try:
    while True:
        time.sleep(1)   # keep main loop alive
except KeyboardInterrupt:
    print("Keyboard Interrupt detected! Stopping timer...")
    on_board_timer.deinit()   # turn off timer safely
    led.value(0)              # turn LED off
    print("Timer stopped, LED off.")
