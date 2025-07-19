from machine import I2C, Pin
from libs.imu import MPU6050
import time

i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)

mpu = MPU6050(i2c)
prevx = 0
prevy = 0
prevz = 0
while True:
    xAccel = mpu.accel.x
    yAccel = mpu.accel.y
    zAccel = mpu.accel.z
    if xAccel > prevx and zAccel < prevz:
        #print("positive row")
        pass
    elif xAccel < prevx and zAccel < prevz:
        #print("negative row")
        pass
    if yAccel < prevy and zAccel < prevz:
        print("pitch up...^...")
    elif yAccel > prevy and zAccel < prevz:
        print("pitch down....|...")
    
    prevx = xAccel
    prevy = yAccel
    prevz = zAccel
    
    
    
    
   # print('x:', xAccel, 'G', '  y:', yAccel, 'G', '  z:', zAccel,'G' )
    
    time.sleep(0.5)