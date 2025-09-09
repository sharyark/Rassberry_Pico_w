from machine import Pin, Timer

# Define LEDs for 4-bit counter
led0 = Pin(2, Pin.OUT)   # LSB
led1 = Pin(4, Pin.OUT)
led2 = Pin(5, Pin.OUT)
led3 = Pin(18, Pin.OUT)  # MSB

# --- Callback functions using toggle() ---
def toggle_led0(timer):
    led0.toggle()

def toggle_led1(timer):
    led1.toggle()

def toggle_led2(timer):
    led2.toggle()

def toggle_led3(timer):
    led3.toggle()

# --- Timers setup ---
tim0 = Timer(0)
tim0.init(period=1000, mode=Timer.PERIODIC, callback=toggle_led0)

tim1 = Timer(1)
tim1.init(period=2000, mode=Timer.PERIODIC, callback=toggle_led1)

tim2 = Timer(2)
tim2.init(period=4000, mode=Timer.PERIODIC, callback=toggle_led2)

tim3 = Timer(3)
tim3.init(period=8000, mode=Timer.PERIODIC, callback=toggle_led3)
