#include <WiFi.h>
#include <WebServer.h>

// WiFi credentials
const char* ssid = "wifi_ssid";
const char* password = "wifi_pass";

// Create a web server on port 80
WebServer server(80);

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
    float temperature = 3;
    float humidity = 50;
    float pressure = 20;

    String json = "{\"temperature\": " + String(temperature) +
                  ", \"humidity\": " + String(humidity) +
                  ", \"pressure\": " + String(pressure) + "}";
    server.send(200, "application/json", json);
  });

  // Start the server
  server.begin();
}

void loop() {
  server.handleClient();
}