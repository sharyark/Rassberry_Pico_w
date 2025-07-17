from machine import I2C, Pin
from libs.imu import MPU6050
import time

i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)

mpu = MPU6050(i2c)

while True:
    xAccel = mpu.accel.x
    yAccel = mpu.accel.y
    print('x:', xAccel, 'G', 'y:', yAccel, 'G')
    time.sleep(0.5)

