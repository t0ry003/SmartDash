# 🚀 Flashing Code to Your ESP32

This guide will walk you through uploading the generated Arduino code to your ESP32 board.

---

## 🧰 Requirements

- ✅ ESP32 development board
- ✅ USB cable (data-capable)
- ✅ [Arduino IDE](https://www.arduino.cc/en/software) installed
- ✅ Required libraries installed (e.g., WiFi, sensor-specific libraries)
- ✅ Code copied from the project page

---

## 🛠️ Steps to Upload Code

### 1. Open Arduino IDE

Download and install from [arduino.cc](https://www.arduino.cc/en/software) if you haven’t already.

---

### 2. Install ESP32 Board Support

1. Open **Arduino IDE**
2. Go to `File > Preferences`
3. In **Additional Board URLs**, add:

```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

4. Go to `Tools > Board > Boards Manager`
5. Search for `ESP32` and click **Install**

---

### 3. Select Your Board and Port

- Go to `Tools > Board` and choose your ESP32 model (e.g., **ESP32 Dev Module**)
- Go to `Tools > Port` and select the correct COM port (e.g., `COM3` or `/dev/ttyUSB0`)

---

### 4. Paste the Code

1. Go to `File > New` or open a new sketch
2. Paste the code copied from the project page
3. Replace `const char* ssid = "";` and `const char* password = "";` if not already done

---

### 5. Upload the Code

1. Click the ✅ **Verify** button to compile
2. Press the 🔼 **Upload** button
3. Hold the `BOOT` button on your ESP32 **if upload fails**
4. Wait for the "Done Uploading" message

---

## 🔍 Tips

- If upload fails repeatedly, try changing USB cable or port
- Open the Serial Monitor (Ctrl+Shift+M) to debug output
- Ensure the correct baud rate (typically 115200) in Serial Monitor

---

## 🧪 Example Output (Serial Monitor)

```

Connecting to WiFi...
Connected to WiFi
IP address: xxx.xxx.xxx.xxx

```

Copy this ip address to add it to the SmartDash dashboard

---

## ✅ Done!

Access the SmartDash dashboard with the button below:
