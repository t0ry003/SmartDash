# 🌡️ ESP32 Thermostat with BMP180: Wiring Guide

---

## 🛠️ Not fully qualified for SmartDash:

- 🚫 Humidity sensor (DHT11)
- ✅ Temperature monitoring
- ✅ No pressure sensor

---

## 🧰 Components Required

- ESP32 Dev Board
- BMP180 Sensor
- Breadboard
- Jumper Wires (Male-to-Male)

---

## 🔌 Pin Connections

<div align="center">
  <img src="https://raw.githubusercontent.com/t0ry003/SmartDash/refs/heads/master/device_setup/static/ESP32-Pinout.png" alt="ESP32 Pinout" style="max-width: 100%;">
</div>

| BMP180 Pin | ESP32 Pin | Description         |
|------------|-----------|---------------------|
| VIN        | 3V3       | Power Supply (3.3V) |
| GND        | GND       | Ground              |
| SCL        | GPIO 22   | I2C Clock           |
| SDA        | GPIO 21   | I2C Data            |

> **Note**: ESP32 uses GPIO 21 for `SDA` and GPIO 22 for `SCL` by default in many libraries (e.g., Adafruit BMP180,
> SparkFun BMP180).

---

## 🖼️ BMP180 Sensor Pinout

<div align="center">
  <img src="https://lastminuteengineers.com/wp-content/uploads/arduino/BMP180-Module-Pinout.png" alt="BMP180 Pinout" style="max-width: 100%;">
</div>

---

## ⚠️ Tips

- Double-check orientation: VIN is **not** the same as VCC on some boards.
- I2C lines (SCL/SDA) **must** have pull-up resistors — many BMP180 boards include them onboard.
- BMP180 operates at 3.3V — perfect for ESP32 logic levels.

---

## ✅ Summary

You’ve now wired your **ESP32** to the **BMP180** sensor over **I2C**. This setup allows you to measure:

- Atmospheric Pressure (Pa)
- Temperature (°C)
- Approximate Altitude (from pressure)

You can now move on to uploading code using the Adafruit BMP085 or BMP180 library in Arduino IDE.
