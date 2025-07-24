# MPU6050 Roll and Pitch Estimator (MicroPython)

This project reads acceleration data from the **MPU6050** sensor using the I2C interface on a microcontroller (such as Raspberry Pi Pico) and calculates **roll** and **pitch** angles manually using the raw accelerometer values and trigonometry (without any library for orientation calculation).

---

## 📦 Hardware Used

- MPU6050 (Accelerometer + Gyroscope)
- Raspberry Pi Pico / ESP32 / Other MicroPython-supported board
- Jumper wires
- Breadboard (optional)

---

## 🔌 Wiring (Example for Raspberry Pi Pico)

| MPU6050 Pin | Pico Pin |
|-------------|----------|
| VCC         | 3.3V     |
| GND         | GND      |
| SDA         | GP14     |
| SCL         | GP15     |

---

## 📁 File Structure

