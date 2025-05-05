# 🌡️ ESP32 Thermostat with DHT11: Wiring Guide

---

## 🛠️ Not fully qualified for SmartDash:

- ✅ Humidity sensor (DHT11)
- ✅ Temperature monitoring
- 🚫 No pressure sensor

---

## 🧰 Components Required

- ESP32 Dev Board
- DHT11 Sensor
- Breadboard
- Jumper Wires (Male-to-Male)
- 10k Resistor

---

## 📌 Pin Connections

<div align="center">
  <img src="https://raw.githubusercontent.com/t0ry003/SmartDash/refs/heads/master/device_setup/static/ESP32-Pinout.png" alt="ESP32 Pinout" style="max-width: 100%;">
</div>

| DHT11 Pin | ESP32 Pin | Description         |
|-----------|-----------|---------------------|
| VCC       | 3V3       | Power Supply (3.3V) |
| GND       | GND       | Ground              |
| DATA      | GPIO 5    | Signal Input        |

> **Note**: The DHT11 sensor uses a **10kΩ pull-up resistor** between VCC and DATA for stability.

---

## 🖼️ DHT11 Sensor Pinout

<div align="center">
  <img src="https://raw.githubusercontent.com/t0ry003/SmartDash/refs/heads/master/device_setup/static/DHT11.png" alt="DHT11 Pinout" style="max-width: 60%;">
</div>

---

## ⚠️ Tips

- Use a 10kΩ pull-up resistor on the DATA line.
- Ensure a proper ground connection between ESP32 and DHT11.
- DHT11 sensors are slower (~1s refresh), avoid overly frequent polling.

---

## 🧠 How It Works

- The ESP32 reads **temperature** and **humidity** from the DHT11.
- The pressure sensor is not used in this setup so it is set to `0`.
- Data is served via a **web interface** (`/sensor-data`) as JSON.

```json
{
  "temperature": 25.6,
  "humidity": 60.2,
  "pressure": 0,
  "state": "on"
}
```
