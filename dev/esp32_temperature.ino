#include <WiFi.h>
#include <WebServer.h>

// WiFi credentials
const char* ssid = "wifi_ssid";
const char* password = "wifi_pass";

// Create a web server on port 80
WebServer server(80);

// Simulation variables
float temperature = 0;
float humidity = 0;
float pressure = 0;
int direction = 1; // 1 = ascending, -1 = descending

unsigned long lastUpdate = 0;
const unsigned long updateInterval = 200; // milliseconds

// State variable
String deviceState = "off";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  // Connect to WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

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

  // Update simulated values every `updateInterval` ms
  if (millis() - lastUpdate >= updateInterval) {
    lastUpdate = millis();

    // Update values
    temperature += direction;
    humidity += direction;
    pressure += direction;

    if(temperature)
      deviceState = "on"

    // Reverse direction at bounds
    if (temperature >= 60 || temperature <= 0) {
      direction *= -1;
    }
  }
}