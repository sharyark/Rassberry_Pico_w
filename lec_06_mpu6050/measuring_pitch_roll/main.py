from machine import I2C, Pin
from libs.imu import MPU6050
import time
import math
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)

mpu = MPU6050(i2c)
prevx = 0
prevy = 0
prevz = 0
while True:
    xAccel = mpu.accel.x
    yAccel = mpu.accel.y
    zAccel = mpu.accel.z
    xAccel = max(min(xAccel, 1), -1)
    yAccel = max(min(yAccel, 1), -1)
    zAccel = max(min(zAccel, 1), -1)
    
    theta_pitch = math.atan(yAccel/zAccel)
    theta_roll = math.atan(xAccel/zAccel)
    pitch = (theta_pitch/(2*math.pi))*360
    roll = (theta_roll/(2*math.pi))*360
    #print('x:', xAccel, 'G', '  y:', yAccel, 'G', '  z:', degree,'degree_RoLL' )
    print('pitch is :',pitch,'  roll is :',roll)
    time.sleep(0.05)



