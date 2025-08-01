from machine import I2C, Pin
from libs.imu import MPU6050
import time
import math
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)

mpu = MPU6050(i2c)
while True:
    zAccel = round(mpu.accel.z,1)
    startTime = time.ticks_ms()
    flag = 0
    while zAccel < 0.95:
        zAccel = round(mpu.accel.z,1)
        flag = 1
    stopTime = time.ticks_ms()
    dropT = startTime - stopTime
    if flag == 1:
        dropTsec = dropT * .001
        ht = 16 * dropTsec * dropTsec*12
        print("droped distance " + str(ht))
        print("time drop ",dropTsec)
        time.sleep(5)
        
