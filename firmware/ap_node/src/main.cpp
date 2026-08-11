#include <WiFi.h>
#include <esp_now.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_NeoPixel.h>

// AP Node Firmware v1.0
// Uses ESP-NOW for RSSI backhaul + MQTT for server sync

const char* AP_SSID = "SPECTRE-AP-01";  // Change per node: 01-06
const int AP_CHANNEL = 1;  // 1, 6, 11 rotation
const char* MQTT_SERVER = "192.168.4.1";
const int MQTT_PORT = 1883;
const String NODE_ID = "NODE-" + String((uint32_t)ESP.getEfuseMac());

#define OLED_SDA 8
#define OLED_SCL 9
#define LED_RING_PIN 10
#define BUZZER_PIN 11
#define ACTION_BTN 12
#define CANCEL_BTN 13

Adafruit_SSD1306 display(128, 64, &Wire, -1);
Adafruit_NeoPixel ring(8, LED_RING_PIN, NEO_GRB + NEO_KHZ800);
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

String state = "idle";
String ownerTeam = "";
int progress = 0;

void setup() {
  Serial.begin(115200);

  Wire.setPins(OLED_SDA, OLED_SCL);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.println(NODE_ID);
  display.display();

  ring.begin();
  ring.setBrightness(100);

  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(ACTION_BTN, INPUT_PULLUP);
  pinMode(CANCEL_BTN, INPUT_PULLUP);

  // ESP-NOW init
  WiFi.mode(WIFI_AP);
  WiFi.softAP(AP_SSID, "spectrefield", AP_CHANNEL, 0, 8);

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed");
  }

  // MQTT
  mqtt.setServer(MQTT_SERVER, MQTT_PORT);
}

void loop() {
  if (!mqtt.connected()) reconnectMQTT();
  mqtt.loop();

  handleButtons();
  updateDisplay();
  updateLEDs();

  delay(50);
}

void reconnectMQTT() {
  while (!mqtt.connected()) {
    if (mqtt.connect(NODE_ID.c_str())) {
      mqtt.subscribe(("nodes/" + NODE_ID + "/cmd").c_str());
    } else {
      delay(5000);
    }
  }
}

void handleButtons() {
  if (digitalRead(ACTION_BTN) == LOW) {
    // Handle action
  }
  if (digitalRead(CANCEL_BTN) == LOW) {
    // Handle cancel
  }
}

void updateDisplay() {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println(NODE_ID);
  display.println("State: " + state);
  if (progress > 0) {
    display.drawRect(0, 40, 128, 10, SSD1306_WHITE);
    display.fillRect(2, 42, (124 * progress) / 100, 6, SSD1306_WHITE);
  }
  display.display();
}

void updateLEDs() {
  if (state == "idle") {
    for (int i = 0; i < 8; i++) ring.setPixelColor(i, ring.Color(255, 255, 255));
  }
  ring.show();
}
