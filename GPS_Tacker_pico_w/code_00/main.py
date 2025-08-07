from machine import UART, Pin
import time

# Set up UART1 on GP8 (TX), GP9 (RX)
gps = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

def parse_GPGGA(data):
    try:
        parts = data.split(",")
        fix = int(parts[6])  # 0 = no fix, 1 = GPS fix, 2 = DGPS fix
        lat = parts[2]
        lat_dir = parts[3]
        lon = parts[4]
        lon_dir = parts[5]
        return fix, lat, lat_dir, lon, lon_dir
    except:
        return None, None, None, None, None

print("Waiting for GPS fix...\n")

while True:
    if gps.any():
        line = gps.readline()
        if line:
            try:
                line = line.decode('utf-8').strip()
                if line.startswith("$GPGGA"):
                    fix, lat, lat_dir, lon, lon_dir = parse_GPGGA(line)
                    if fix and fix > 0:
                        print("✅ GPS FIX Acquired!")
                        print("Latitude:", lat, lat_dir)
                        print("Longitude:", lon, lon_dir)
                    else:
                        print("❌ No GPS fix yet.")
            except UnicodeError:
                pass  # Ignore decode errors

    time.sleep(1)

