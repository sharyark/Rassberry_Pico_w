from machine import Pin, UART, SoftI2C
import time
import _thread
from ssd1306 import SSD1306_I2C

# Use SoftI2C instead of hardware I2C
i2c2 = SoftI2C(sda=Pin(2), scl=Pin(3), freq=100000)
time.sleep(0.2)
dsp = SSD1306_I2C(128, 64, i2c2)

dataLock = _thread.allocate_lock()
keepRunning = True
GPS = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
GPS.write(b"$PMTK314,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n")

NMEAdata = {
    'GPGGA' : "",
    'GPGSA' : "",
    'GPRMC' : "",
    'GPVTG' : ""
}

GPSdata = {
    'latDD'     : 0,
    'lonDD'     : 0,
    'heading'   : 0,
    'fix'       : False,
    'sats'      : 0,
    'knots'     : 0,
    'date'      : "",  # Date in DDMMYY format
    'time'      : ""   # Time in UTC HHMMSS format
}

def gpsThread():
    print("Thread Running")
    global keepRunning, NMEAdata
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
            myChar = GPS.read(1).decode('utf-8')
            myNMEA = myNMEA + myChar
            if myChar == '\n':
                myNMEA = myNMEA.strip()
                if len(myNMEA) > 6:  # Check minimum length
                    if myNMEA[1:6] == "GPGGA":
                        GPGGA = myNMEA
                    if myNMEA[1:6] == "GPGSA":
                        GPGSA = myNMEA
                    if myNMEA[1:6] == "GPRMC":
                        GPRMC = myNMEA
                    if myNMEA[1:6] == "GPVTG":
                        GPVTG = myNMEA
                    if GPGGA != "" and GPGSA != "" and GPRMC != "" and GPVTG != "":
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

def parseGPS():
    try:
        readFix = int(NMEAmain['GPGGA'].split(',')[6])
        if readFix != 0:
            GPSdata['fix'] = True
            
            # Parse Latitude
            latRAW = NMEAmain['GPGGA'].split(',')[2]
            if latRAW:
                latDD = int(latRAW[0:2]) + float(latRAW[2:])/60
                if NMEAmain['GPGGA'].split(',')[3] == 'S':
                    latDD = -latDD
                GPSdata['latDD'] = latDD
            
            # Parse Longitude
            lonRAW = NMEAmain['GPGGA'].split(',')[4]
            if lonRAW:
                lonDD = int(lonRAW[0:3]) + float(lonRAW[3:])/60
                if NMEAmain['GPGGA'].split(',')[5] == 'W':
                    lonDD = -lonDD
                GPSdata['lonDD'] = lonDD
            
            # Parse Heading
            heading_str = NMEAmain['GPRMC'].split(',')[8]
            if heading_str:
                GPSdata['heading'] = float(heading_str)
            else:
                GPSdata['heading'] = 0
            
            # Parse Speed
            knots_str = NMEAmain['GPRMC'].split(',')[7]
            if knots_str:
                GPSdata['knots'] = float(knots_str)
            else:
                GPSdata['knots'] = 0
            
            # Parse Satellites
            sats = NMEAmain['GPGGA'].split(',')[7]
            sats = int(sats)
            GPSdata['sats'] = sats if sats else '0'
            
            # Parse Date and Time from GPRMC (UTC)
            utc_time = NMEAmain['GPRMC'].split(',')[1]  # UTC Time (HHMMSS)
            utc_date = NMEAmain['GPRMC'].split(',')[9]  # Date (DDMMYY)
            
            if utc_time and utc_date:
                # Extract time and date
                hour = int(utc_time[0:2]) + 5  # Add 5 hours for Pakistan Time
                if hour >= 24:
                    hour -= 24  # Wrap around the hour if it goes over 24
                minute = int(utc_time[2:4])
                second = int(utc_time[4:6])
                day = int(utc_date[0:2])
                month = int(utc_date[2:4])
                year = int("20" + utc_date[4:6])  # Assuming 20th century for simplicity

                # Format Date and Time
                GPSdata['date'] = "{:02d}-{:02d}-{:02d}".format(day, month, year % 100)
                GPSdata['time'] = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
        else:
            GPSdata['fix'] = False
            
    except (ValueError, IndexError) as e:
        print("GPS Parse Error:", e)
        GPSdata['fix'] = False

def dispOLED():
    dsp.fill(0)
    if GPSdata['fix'] == False:
        dsp.text("Waiting for Fix...", 0, 0)
    else:
        # Removed "ULTIMATE GPS" as per your request
        dsp.text("Date: " + str(GPSdata['date']), 0, 0)  # Display date first
        dsp.text("Time: " + str(GPSdata['time']), 0, 12)  # Display time second
        dsp.text("LAT: " + str(round(GPSdata['latDD'], 4)), 0, 24)  # Latitude
        dsp.text("LON: " + str(round(GPSdata['lonDD'], 4)), 0, 36)  # Longitude
        dsp.text("SPD:" + str(round(GPSdata['knots'], 1)) + 'kts', 0, 48)
        dsp.text("HDG:" + str(round(GPSdata['heading'], 1)), 0, 54)
        dsp.text("SAT:" + str(GPSdata['sats']), 90, 54)
    dsp.show()

# Start GPS thread
_thread.start_new_thread(gpsThread, ())
time.sleep(2)

try:
    while True:
        dataLock.acquire()
        NMEAmain = NMEAdata.copy()
        dataLock.release()
        parseGPS()
        
        if GPSdata['fix'] == False:
            print("Waiting for Fix . . .")
        else:
            print("Ultimate GPS Tracker Report:")
            print("Date:", GPSdata['date'])
            print("Time:", GPSdata['time'])
            print("Lat and Lon:", GPSdata['latDD'], GPSdata['lonDD'])
            print("Knots:", GPSdata['knots'])
            print("Heading:", GPSdata['heading'])
            print("Sats:", GPSdata['sats'])
            print()
        
        dispOLED()
        time.sleep(10)
        
except KeyboardInterrupt:
    print("\nStopping Program . . . Cleaning Up UART")
    keepRunning = False
    time.sleep(1)
    GPS.deinit()
    time.sleep(1)
    dsp.fill(0)
    dsp.show()
    print("Exited Cleanly")

