import machine
from time import sleep
potPin = 26     #pin from reading
myPot = machine.ADC(potPin)

while True:
    potVal = myPot.read_u16()
    print(potVal)
    y = 3.3/63935*(int(potVal)-1632)
    print(y," volt")
    sleep(.5)