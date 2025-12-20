from machine import Pin, UART
import time
import _thread

# Shared data structure with thread lock
gps_data = {
    'lat': None,
    'lon': None,
    'numSat': 0,
    'knots': 0.0,
    'heading': 0.0,
    'fix': False,
    'sats_in_view': 0
}
data_lock = _thread.allocate_lock()

# GPS UART setup
GPS = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9), timeout=1000)

print("Initializing GPS...")
time.sleep(1)

# Configure GPS to output specific NMEA sentences
GPS.write(b"$PMTK314,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n")
time.sleep(1)

# Clear any initial junk data
if GPS.any():
    junk = GPS.read()

print("Starting dual-core GPS system...")
print("Core 0: GPS reading")
print("Core 1: OLED display (simulated with 5s delay)")
print("-" * 50)


# CORE 0: GPS Reading Thread (runs continuously, no delays)
def gps_reading_thread():
    myNMEA = ""
    GPGGA = ""
    GPGGAarray = []
    
    while True:
        if GPS.any():
            try:
                myChar = GPS.read(1).decode('utf-8')
                myNMEA = myNMEA + myChar
                
                if myChar == '\n':
                    if myNMEA.startswith('$'):
                        
                        # Parse GPGGA (Position data)
                        if myNMEA[1:6] == "GPGGA":
                            GPGGA = myNMEA
                            GPGGAarray = GPGGA.split(',')
                            
                            # Update shared data with lock
                            with data_lock:
                                if len(GPGGAarray) > 6 and GPGGAarray[6] and int(GPGGAarray[6]) != 0:
                                    try:
                                        latRAW = GPGGAarray[2]
                                        lonRAW = GPGGAarray[4]
                                        gps_data['numSat'] = int(GPGGAarray[7])
                                        
                                        # Convert to decimal degrees
                                        latDD = int(latRAW[0:2]) + float(latRAW[2:]) / 60
                                        lonDD = int(lonRAW[0:3]) + float(lonRAW[3:]) / 60
                                        
                                        if GPGGAarray[3] == 'S':
                                            latDD = -latDD
                                        if GPGGAarray[5] == 'W':
                                            lonDD = -lonDD
                                        
                                        gps_data['lat'] = latDD
                                        gps_data['lon'] = lonDD
                                        gps_data['fix'] = True
                                        
                                    except (ValueError, IndexError):
                                        pass
                                else:
                                    gps_data['fix'] = False
                        
                        # Parse GPRMC (Speed/Heading)
                        elif myNMEA[1:6] == "GPRMC":
                            GPRMCarray = myNMEA.split(',')
                            
                            with data_lock:
                                try:
                                    if len(GPRMCarray) > 8 and GPRMCarray[7] and GPRMCarray[8]:
                                        gps_data['knots'] = float(GPRMCarray[7])
                                        gps_data['heading'] = float(GPRMCarray[8])
                                except (ValueError, IndexError):
                                    pass
                        
                        # Parse GPGSV (Satellites in view)
                        elif myNMEA[1:6] == "GPGSV":
                            GPGSVarray = myNMEA.split(',')
                            
                            with data_lock:
                                try:
                                    if len(GPGSVarray) > 3:
                                        gps_data['sats_in_view'] = int(GPGSVarray[3])
                                except (ValueError, IndexError):
                                    pass
                    
                    myNMEA = ""
                    
            except UnicodeDecodeError:
                myNMEA = ""


# CORE 1: OLED Display Thread (main thread with delays)
def oled_display_thread():
    """
    This simulates OLED updates with time.sleep(5)
    Replace sleep with actual OLED code later
    """
    while True:
        # Read shared data with lock
        with data_lock:
            lat = gps_data['lat']
            lon = gps_data['lon']
            numSat = gps_data['numSat']
            knots = gps_data['knots']
            heading = gps_data['heading']
            fix = gps_data['fix']
            sats_in_view = gps_data['sats_in_view']
        
        # Display data (simulated)
        print("\n" + "="*50)
        print("OLED DISPLAY UPDATE (Core 1)")
        print("="*50)
        
        if fix and lat is not None:
            print(f"LAT:      {lat:.6f}°")
            print(f"LON:      {lon:.6f}°")
            print(f"SATS:     {numSat}")
            print(f"SPEED:    {knots:.1f} knots")
            print(f"HEADING:  {heading:.1f}°")
        else:
            print(f"Acquiring GPS Fix...")
            print(f"Satellites in View: {sats_in_view}")
        
        print("="*50)
        
        # Simulate OLED update time
        # Replace this with actual OLED code:
        # oled.fill(0)
        # oled.text(f"LAT: {lat}", 0, 0)
        # oled.text(f"LON: {lon}", 0, 10)
        # oled.show()
        
        time.sleep(5)  # 5 second delay - GPS keeps reading on Core 0!


# Start GPS reading on Core 0 (second core)
try:
    _thread.start_new_thread(gps_reading_thread, ())
    print("✓ Core 0 started: GPS reading")
    
    # Run OLED display on Core 1 (main core)
    print("✓ Core 1 started: OLED display\n")
    oled_display_thread()
    
except KeyboardInterrupt:
    print("\nStopping program...")
    GPS.deinit()
    print("Exited cleanly.")