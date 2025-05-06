# 💡 ESP32 Relay: Wiring Guide

---

## ⭐ Fully Qualified for SmartDash

- ✅ Relay control via GPIO
- ✅ Suitable for 220V AC loads
- ✅ Compatible with `/toggle` and `/sensor-data` API

---

## 🧰 Components Required

- ESP32 Dev Board
- 1-Channel 5V Relay Module
- Breadboard
- Jumper Wires (Male-to-Male)
- 240V AC Power Source
- AC Light Bulb (or any 220V load)

---

## 🔌 Pin Connections

<div align="center">
  <img src="https://raw.githubusercontent.com/t0ry003/SmartDash/refs/heads/master/device_setup/static/ESP32-Pinout.png" alt="ESP32 Pinout" style="max-width: 100%;">
</div>

| Module | Pin Name | ESP32 Pin  | Description          |
|--------|----------|------------|----------------------|
| Relay  | VCC      | 3V3        | Power Supply (3.3V)  |
| Relay  | GND      | GND        | Ground               |
| Relay  | IN       | GPIO 5     | Control Signal       |
| Load   | L (Live) | AC Input   | 240V AC Live Line    |
| Load   | N        | AC Neutral | 240V AC Neutral Line |

---

## 🖼️ Wiring Diagram

<div align="center">
  <img src="https://raw.githubusercontent.com/t0ry003/SmartDash/refs/heads/master/device_setup/static/projects/ESP32_RELAY/breadboard.png" alt="ESP32 Relay Wiring" style="max-width: 80%;">
</div>

---

## 📦 Required Arduino Libraries

- None required for basic relay control
- Optional: `ArduinoJson` for JSON APIs

---

## ⚠️ Tips

- Be **extremely careful** when working with 220V AC — never handle live wires while powered.
- Use **LOW trigger relays** (active-low) with ESP32.
- You may need to power the relay using 5V if it doesn’t activate reliably on 3.3V.
- Consider opto-isolated relay modules for electrical safety.

---

## 🧠 How It Works

- GPIO 5 controls the relay (on/off)
- Toggled via SmartDash through `/toggle`
- Current relay state can be queried from `/sensor-data`

---

## 📡 Example JSON Response

```json
{
  "state": "on"
}
```
