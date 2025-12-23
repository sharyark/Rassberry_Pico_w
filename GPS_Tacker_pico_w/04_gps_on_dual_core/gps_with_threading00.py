from machine import Pin,I2C,UART
import time
import _thread
dataLock = _thread.allocate_lock()
keepRunning = True
GPS = UART(1, baudrate=9600, tx=machine.Pin(8), rx=machine.Pin(9))
# The following line ensures that the GPS reports the GPVTG NMEA Sentence
GPS.write(b"$PMTK314,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n")
NMEAdata = {
    'GPGGA' : "",
    'GPGSA' : "",
    'GPRMC' : "",
    'GPVTG' : ""
    }
def gpsThread():
    print("Thread Running")
    global keepRunning,NMEAdata
    GPGGA = ""
    GPGSA = ""
    GPRMC = ""
    GPVTG = ""
    while not GPS.any():
        pass
    while GPS.any():
        junk = GPS.read()
        print(junk)
    myNMEA = ""
    while keepRunning:
        if GPS.any():
            myChar=GPS.read(1).decode('utf-8')
            myNMEA = myNMEA + myChar
            if myChar == '\n':
                myNMEA = myNMEA.strip()
                if myNMEA[1:6] == "GPGGA":
                    GPGGA = myNMEA
                if myNMEA[1:6] == "GPGSA":
                    GPGSA = myNMEA
                if myNMEA[1:6] == "GPRMC":
                    GPRMC = myNMEA
                if myNMEA[1:6] == "GPVTG":
                    GPVTG = myNMEA
                if GPGGA != "" and GPGSA!="" and GPRMC!="" and GPVTG!="":
                    dataLock.acquire()
                    NMEAdata = {
                        'GPGGA' : GPGGA,
                        'GPGSA' : GPGSA,
                        'GPRMC' : GPRMC,
                        'GPVTG' : GPVTG
                        }
                    dataLock.release()
                myNMEA = ""
    print("Thread Terminated Cleanly")

_thread.start_new_thread(gpsThread,())
try:
    while True:
        dataLock.acquire()
        NMEAmain = NMEAdata.copy()
        dataLock.release()
        print(NMEAmain['GPGGA'])
        time.sleep(10)
except KeyboardInterrupt:
    print("\nStopping Program . . . Cleaning Up UART")
    keepRunning = False
    time.sleep(1)
    GPS.deinit()
    time.sleep(1)
    print("Exited Cleanly")
