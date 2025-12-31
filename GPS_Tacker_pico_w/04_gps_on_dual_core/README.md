# GPS Tracker with OLED Display

A MicroPython-based GPS tracker that displays real-time location data on an SSD1306 OLED screen using dual-core threading.

## 📋 Hardware Requirements

- **Microcontroller**: Raspberry Pi Pico
- **GPS Module**: UART GPS module (9600 baud)
- **Display**: SSD1306 OLED (128x64, I2C, 4-pin)

## 🔌 Wiring Diagram

```
Raspberry Pi Pico          GPS Module
------------------         -----------
GPIO 8 (TX)    --------→   RX
GPIO 9 (RX)    ←--------   TX
3.3V           --------→   VCC
GND            --------→   GND

Raspberry Pi Pico          OLED Display (SSD1306)
------------------         -----------------------
GPIO 2         --------→   SDA
GPIO 3         --------→   SCL
3.3V           --------→   VCC
GND            --------→   GND
```

## 🚀 How It Works

### Architecture Overview

The code uses a **dual-core threading approach** to handle GPS data collection and display updates simultaneously:

```
┌─────────────────────────────────────────────────────────────┐
│                      Main Thread (Core 0)                    │
│  • Reads GPS data from shared dictionary                    │
│  • Parses NMEA sentences                                     │
│  • Updates OLED display every 10 seconds                     │
│  • Prints data to console                                    │
└─────────────────────────────────────────────────────────────┘
                              ↕
                    Thread-Safe Data Lock
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                      GPS Thread (Core 1)                     │
│  • Continuously reads UART data from GPS                     │
│  • Collects NMEA sentences character by character            │
│  • Updates shared dictionary with latest data                │
└─────────────────────────────────────────────────────────────┘
```

### 1. Initialization Phase

**I2C Setup (SoftI2C)**
```python
i2c2 = SoftI2C(sda=Pin(2), scl=Pin(3), freq=100000)
dsp = SSD1306_I2C(128, 64, i2c2)
```
- Uses Software I2C for reliable communication with OLED
- Frequency: 100 kHz (prevents I2C write errors)

**UART Setup**
```python
GPS = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
GPS.write(b"$PMTK314,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n")
```
- Configures GPS to output specific NMEA sentences
- Command enables: GPGGA, GPGSA, GPRMC, GPVTG

**Thread Safety**
```python
dataLock = _thread.allocate_lock()
```
- Mutex lock prevents data corruption between threads

### 2. GPS Thread (Background Collection)

**Function**: `gpsThread()`

**Process Flow**:

1. **Wait for GPS Data**
   - Waits until GPS starts sending data
   - Clears initial buffer

2. **Character-by-Character Reading**
   ```
   Read 1 byte → Decode to UTF-8 → Append to sentence → Check for newline
   ```

3. **NMEA Sentence Detection**
   - Identifies sentence type by checking characters [1:6]
   - `$GPGGA` → Position and fix data
   - `$GPGSA` → Satellite info and DOP values
   - `$GPRMC` → Recommended minimum data
   - `$GPVTG` → Course and speed

4. **Data Update**
   ```
   Once all 4 sentences collected → Acquire lock → Update NMEAdata → Release lock
   ```

### 3. Main Loop (Display & Processing)

**Runs every 10 seconds**:

**Step 1: Thread-Safe Data Copy**
```python
dataLock.acquire()
NMEAmain = NMEAdata.copy()
dataLock.release()
```

**Step 2: Parse GPS Data** - `parseGPS()`

Extracts and converts:

- **Fix Status**: From GPGGA field 6 (0=no fix, 1=GPS, 2=DGPS)
- **Latitude**: DDMM.MMMM → DD.DDDD decimal degrees
  - Extracts degrees (first 2 digits) and minutes (remaining)
  - Formula: `DD + (MM.MMMM / 60)`
- **Longitude**: DDDMM.MMMM → DDD.DDDD decimal degrees
  - Extracts degrees (first 3 digits) and minutes (remaining)
- **Speed**: Direct from GPRMC field 7 (knots)
- **Heading**: Direct from GPRMC field 8 (degrees)
- **Satellites**: Count from GPGGA field 7

**Step 3: Update Display** - `dispOLED()`

Two display modes:

**No Fix Mode**:
```
Waiting for Fix...
```

**Fix Acquired Mode**:
```
ULTIMATE GPS:
LAT:33.9493
LON:72.5277
SPD:0.0kts
HDG:0.0      SAT:8
```

### 4. Data Flow Diagram

```
GPS Module (UART)
       ↓
   [Character Stream]
       ↓
   GPS Thread
   • Collect sentences
   • Identify type
       ↓
   [Mutex Lock]
       ↓
   Shared Dictionary
   (NMEAdata)
       ↓
   [Mutex Lock]
       ↓
   Main Loop
   • Copy data
   • Parse fields
       ↓
   GPSdata Dictionary
   • latDD, lonDD
   • heading, knots
   • fix, sats
       ↓
   OLED Display
   (128x64 SSD1306)
```

### 5. NMEA Sentence Structure

**Example GPGGA Sentence**:
```
$GPGGA,065005.00,3356.97603,N,07231.66384,E,1,08,1.12,313.2,M,-40.7,M,,*7D
       └─Time─┘ └─Latitude─┘ └─Longitude──┘ │ │  └─Alt─┘
                                           Fix│
                                         Sats─┘
```

**Fields Used**:
- Field 2: Latitude (DDMM.MMMM)
- Field 3: N/S indicator
- Field 4: Longitude (DDDMM.MMMM)
- Field 5: E/W indicator
- Field 6: Fix quality (0/1/2)
- Field 7: Number of satellites

## 📊 Code Structure

```
gps_dual_core_oled.py
├── Initialization
│   ├── SoftI2C setup (GPIO 2, 3)
│   ├── UART setup (GPIO 8, 9)
│   ├── Thread lock allocation
│   └── Data dictionaries
│
├── gpsThread() function
│   ├── Wait for GPS data
│   ├── Read UART character by character
│   ├── Parse NMEA sentences
│   └── Update shared dictionary
│
├── parseGPS() function
│   ├── Check fix status
│   ├── Convert coordinates to decimal degrees
│   ├── Extract speed and heading
│   └── Handle empty fields
│
├── dispOLED() function
│   ├── Clear display buffer
│   ├── Show fix status or GPS data
│   └── Update OLED screen
│
└── Main Loop
    ├── Copy GPS data (thread-safe)
    ├── Parse and update
    ├── Display on OLED
    └── Print to console
```

## ⚙️ Configuration Options

**Update Interval**:
```python
time.sleep(10)  # Change display update frequency (seconds)
```

**I2C Pins**:
```python
i2c2 = SoftI2C(sda=Pin(2), scl=Pin(3), freq=100000)
```

**UART Pins**:
```python
GPS = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
```

**OLED Address** (if different):
```python
dsp = SSD1306_I2C(128, 64, i2c2, addr=0x3d)  # Default is 0x3c
```

## 🎯 Usage

1. Wire hardware as per diagram above
2. Upload `gps_dual_core_oled.py` to Raspberry Pi Pico
3. Run the script
4. Place GPS outdoors for satellite acquisition
5. Wait for "Waiting for Fix..." to change to GPS data
6. Press `Ctrl+C` to exit cleanly

---

**File**: `gps_dual_core_oled.py`  
**Version**: v1.0