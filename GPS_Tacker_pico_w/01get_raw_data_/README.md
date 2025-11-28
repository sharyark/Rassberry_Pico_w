# 📡 Pico W GPS UART Learning

This project contains my first experiments with reading **GPS data** using **Raspberry Pi Pico W** and **MicroPython**.  
Goal: Understand how GPS sends NMEA sentences and learn about **GPGGA** and **GPGSV**.

---

## 📝 GPGGA – GPS Fix Data

**Observation from script output:**  
- First field = UTC time  
- Second & third fields = Latitude + N/S hemisphere  
- Fourth & fifth fields = Longitude + E/W hemisphere  
- Sixth field = Fix quality (0=no fix, 1=GPS fix, 2=DGPS fix)  
- Seventh field = Number of satellites used  
- Eighth field = HDOP (accuracy)  
- Ninth field = Altitude  
- Tenth field = Unit of altitude (meters)  
- Eleventh field = Geoid height  
- Twelfth field = Unit of geoid height  
- Thirteenth field = DGPS age (if any)  
- Fourteenth field = Checksum  

**Example NMEA Line:**

| Field | Observation | Meaning |
|-------|------------|---------|
| 1     | 123519     | UTC Time |
| 2     | 4807.038   | Latitude |
| 3     | N          | North/South hemisphere |
| 4     | 01131.000  | Longitude |
| 5     | E          | East/West hemisphere |
| 6     | 1          | Fix quality |
| 7     | 08         | Satellites used |
| 8     | 0.9        | HDOP (accuracy) |
| 9     | 545.4      | Altitude in meters |
| 10    | M          | Unit of altitude |
| 11    | 46.9       | Geoid height above WGS84 |
| 12    | M          | Unit of geoid height |
| 13    |            | DGPS age |
| 14    | *47        | Checksum |

---

## 🛰️ GPGSV – Satellites in View

**Observation from script output:**  
- First field = Total number of GSV messages  
- Second field = Message number  
- Third field = Total satellites in view  
- Subsequent groups of four fields per satellite:  
  - PRN number  
  - Elevation (degrees)  
  - Azimuth (degrees)  
  - SNR (signal strength)  

**Example NMEA Line:**

**Satellite Fields:**

| Satellite | PRN | Elevation | Azimuth | SNR |
|-----------|-----|-----------|---------|-----|
| 1         | 07  | 79        | 045     | 42  |
| 2         | 09  | 62        | 123     | 41  |
| …         | …   | …         | …       | …   |

**Observation:**  
- More satellites + higher SNR → stronger signal and more accurate position  

---

## 🌍 Hemisphere Notation

- Latitude hemisphere: **N** = North, **S** = South  
- Longitude hemisphere: **E** = East, **W** = West  
- Example: `4807.038,N,01131.000,E` → Location in Northern & Eastern hemisphere (Pakistan)

---

## 📌 Summary of Learnings

- Script prints **raw NMEA sentences** via UART  
- Learned **GPGGA fields** and their order  
- Learned **GPGSV satellite info** and SNR meaning  
- Understand **hemisphere notation** for latitude and longitude  
- Observed that GPS data is **structured in a predictable, comma-separated format**  





