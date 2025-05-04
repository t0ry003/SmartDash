#include <WiFi.h>
#include <WebServer.h>
#include <DHT.h> // Include DHT library

// WiFi credentials
const char* ssid = "wifi_ssid";
const char* password = "wifi_pass";

// Create a web server on port 80
WebServer server(80);

// DHT11 setup
#define DHTPIN 5       // DHT11 data pin connected to GPIO5 (D5)
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Sensor readings
float temperature = 0;
float humidity = 0;
float pressure = 0; // Always 0, no real pressure sensor

unsigned long lastUpdate = 0;
const unsigned long updateInterval = 2000; // 2 seconds update

// Device state
String deviceState = "off";

void setup() {
  Serial.begin(115200);
  dht.begin(); // Start DHT sensor

  WiFi.begin(ssid, password);

  // Connect to WiFi
  Serial.println("Connecting to WiFi...");
  unsigned long startAttemptTime = millis();
  unsigned long timeout = 15000; // 15 seconds timeout

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
                  ", \"humidity\": " + String(humidity) +
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

    float newHumidity = dht.readHumidity();
    float newTemperature = dht.readTemperature(); // Celsius

    if (!isnan(newHumidity) && !isnan(newTemperature)) {
      humidity = newHumidity;
      temperature = newTemperature;
      pressure = 0; // Still no pressure sensor

      // Update device state based on temperature
      if (temperature > 0) {
        deviceState = "on";
      } else {
        deviceState = "off";
      }
    } else {
      Serial.println("Failed to read from DHT11 sensor!");
    }
  }
}