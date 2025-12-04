from machine import Pin, UART
import time

GPS = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

def convert_to_dd(raw, direction):
    raw = float(raw)
    degrees = int(raw / 100)
    minutes = raw - (degrees * 100)
    dd = degrees + minutes / 60

    if direction in ("S", "W"):
        dd = -dd

    return dd


buffer = ""

try:
    while True:
        if GPS.any():

            # Read raw byte — no decoding error possible
            b = GPS.read(1)
            if not b:
                continue

            try:
                char = b.decode('ascii')   # only ASCII allowed in NMEA
            except:
                char = ''   # skip bad characters

            if char == "\n":
                line = buffer
                buffer = ""

                if line.startswith("$GPGGA"):
                    parts = line.split(",")

                    if len(parts) > 5:
                        raw_lat = parts[2]
                        lat_dir = parts[3]
                        raw_lon = parts[4]
                        lon_dir = parts[5]

                        if raw_lat and raw_lon:
                            lat_dd = convert_to_dd(raw_lat, lat_dir)
                            lon_dd = convert_to_dd(raw_lon, lon_dir)

                            print("Latitude:", lat_dd)
                            print("Longitude:", lon_dd)
                            print("--------------------")

            else:
                buffer += char

except KeyboardInterrupt:
    GPS.deinit()
    print("GPS stopped")

