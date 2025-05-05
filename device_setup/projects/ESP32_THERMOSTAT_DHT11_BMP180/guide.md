# 🌡️ ESP32 Thermostat with DHT11 & BMP180: Wiring Guide

---

## ⭐ Fully Qualified for SmartDash

- ✅ Humidity sensor (DHT11)
- ✅ Temperature monitoring
- ✅ Pressure sensor (BMP180)

---

## 🧰 Components Required

- ESP32 Dev Board
- DHT11 Sensor
- BMP180 Barometric Sensor
- Breadboard
- Jumper Wires (Male-to-Male)
- 10kΩ Resistor (pull-up for DHT11)

---

## 🔌 Pin Connections

<div align="center">
  <img src="https://raw.githubusercontent.com/t0ry003/SmartDash/refs/heads/master/device_setup/static/ESP32-Pinout.png" alt="ESP32 Pinout" style="max-width: 100%;">
</div>

| Sensor | Pin Name | ESP32 Pin | Description         |
|--------|----------|-----------|---------------------|
| DHT11  | VCC      | 3V3       | Power Supply        |
| DHT11  | GND      | GND       | Ground              |
| DHT11  | DATA     | GPIO 5    | Signal Input        |
| BMP180 | VIN      | 3V3       | Power Supply (3.3V) |
| BMP180 | GND      | GND       | Ground              |
| BMP180 | SCL      | GPIO 22   | I2C Clock           |
| BMP180 | SDA      | GPIO 21   | I2C Data            |

> 💡 **Note:** Add a 10kΩ pull-up resistor between **VCC** and **DATA** on the DHT11.

---

## 🖼️ Sensor Pinouts

### DHT11 Sensor

<div align="center">
  <img src="https://raw.githubusercontent.com/t0ry003/SmartDash/refs/heads/master/device_setup/static/DHT11.png" alt="DHT11 Pinout" style="max-width: 60%;">
</div>

### BMP180 Sensor

<div align="center">
  <img src="https://lastminuteengineers.com/wp-content/uploads/arduino/BMP180-Module-Pinout.png" alt="BMP180 Pinout" style="max-width: 70%;">
</div>

---

## ⚠️ Tips

- DHT11 sensors are slower (refresh ~1s), avoid frequent polling.
- BMP180 operates best at **3.3V**, no level shifter needed.
- Both sensors use digital signals but different protocols (DHT = single wire, BMP180 = I2C).
- Use solid connections on breadboard for I2C stability.

---

## 🧠 How It Works

- The ESP32 collects:
    - **Temperature** and **humidity** from the DHT11
    - **Pressure** from the BMP180
- The values are updated every **2 seconds**
- A minimal JSON API serves the current sensor readings on:  
  `http://<esp32-ip>/sensor-data`

```json
{
  "temperature": 24.3,
  "humidity": 58.1,
  "pressure": 1007.2,
  "state": "on"
}
```