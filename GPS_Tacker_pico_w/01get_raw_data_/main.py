from machine import Pin,I2C,UART
import time

GPS = UART(1,baudrate=9600,tx=Pin(8),rx=Pin(9))


try:
    while True:
        if GPS.any():
            myChar = GPS.read(1).decode('utf-8')
            print(myChar,end="")
        
except KeyboardInterrupt:
    print('\n...Cleaning up UART')
    GPS.deinit()
    time.sleep(1)
    
