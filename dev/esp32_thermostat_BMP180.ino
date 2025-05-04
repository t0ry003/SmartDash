#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>
#include <Adafruit_BMP085.h>

// WiFi credentials
const char* ssid = "wifi_ssid";
const char* password = "wifi_pass";

// Create a web server on port 80
WebServer server(80);

// BMP180 sensor
Adafruit_BMP085 bmp;

// Sensor readings
float temperature = 0;
float pressure = 0;

unsigned long lastUpdate = 0;
const unsigned long updateInterval = 2000;  // 2 seconds update

// Device state
String deviceState = "off";

void setup() {
  Serial.begin(115200);

  if (!bmp.begin()) {
    Serial.println("Could not find a valid BMP180 sensor, check wiring!");
    while (1);
  }

  WiFi.begin(ssid, password);

  // Connect to WiFi
  Serial.println("Connecting to WiFi...");
  unsigned long startAttemptTime = millis();
  unsigned long timeout = 15000;  // 15 seconds timeout

  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < timeout) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to WiFi");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFailed to connect to WiFi");
  }

  // Define the route for sensor data
  server.on("/sensor-data", []() {
    String json = "{\"temperature\": " + String(temperature) +
                  ", \"pressure\": " + String(pressure) +
                  ", \"state\": \"" + deviceState + "\"}";
    server.send(200, "application/json", json);
  });

  // Start the server
  server.begin();
}

void loop() {
  server.handleClient();

  // Update sensor readings every `updateInterval` milliseconds
  if (millis() - lastUpdate >= updateInterval) {
    lastUpdate = millis();

    float newTemperature = bmp.readTemperature();
    float newPressure = bmp.readPressure();

    if (!isnan(newTemperature) && !isnan(newPressure)) {
      temperature = newTemperature;
      pressure = newPressure / 100.0; // Convert Pa to hPa
      deviceState = "on";
    } else {
      Serial.println("Failed to read from BMP180 sensor!");
      deviceState = "error";
    }
  }
}
