#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

const char* ssid = "wifi_ssid";
const char* password = "wifi_pass";
#define RELAY_PIN 5

WebServer server(80);
String relayState = "off";

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected. IP address: ");
  Serial.println(WiFi.localIP());

  // POST /toggle
  server.on("/toggle", HTTP_POST, []() {
    if (!server.hasArg("plain")) {
      server.send(400, "application/json", "{\"error\": \"No body received\"}");
      return;
    }

    String body = server.arg("plain");
    Serial.println("Received body: " + body);

    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, body);

    if (error) {
      server.send(400, "application/json", "{\"error\": \"Invalid JSON format\"}");
      return;
    }

    const char* state = doc["state"];
    if (state == nullptr) {
      server.send(400, "application/json", "{\"error\": \"Missing 'state' key\"}");
      return;
    }

    if (strcmp(state, "on") == 0) {
      digitalWrite(RELAY_PIN, HIGH);
      relayState = "on";
    } else if (strcmp(state, "off") == 0) {
      digitalWrite(RELAY_PIN, LOW);
      relayState = "off";
    } else {
      server.send(400, "application/json", "{\"error\": \"Invalid state value\"}");
      return;
    }

    server.send(200, "application/json", "{\"message\": \"Relay toggled\", \"state\": \"" + relayState + "\"}");
  });

  // GET /sensor-data
  server.on("/sensor-data", HTTP_GET, []() {
    StaticJsonDocument<100> doc;
    doc["state"] = relayState;

    String response;
    serializeJson(doc, response);
    server.send(200, "application/json", response);
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
