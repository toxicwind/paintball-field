#include <WiFi.h>
#include <BLEDevice.h>
#include <BLEBeacon.h>
#include <WebSocketsClient.h>
#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_NeoPixel.h>

// ============ CONFIG ============
const char* FIELD_SSID_PREFIX = "SPECTRE-AP-";
const char* WS_HOST = "192.168.4.1";
const int WS_PORT = 8765;
const String BAND_ID = "B" + String((uint32_t)ESP.getEfuseMac());
String TEAM = "red";  // "red" or "blue"

// Pins: ESP32-C3-MINI-1
#define OLED_SDA 8
#define OLED_SCL 9
#define LED_PIN 10
#define HAPTIC_PIN 11
#define BUTTON_PIN 12

// ============ HARDWARE ============
Adafruit_SSD1306 display(128, 64, &Wire, -1);
Adafruit_NeoPixel strip(3, LED_PIN, NEO_GRB + NEO_KHZ800);
WebSocketsClient ws;

// ============ STATE ============
struct Player {
  String id;
  float x, y;
  String team;
  bool visible;
  float dist;
};

Player visiblePlayers[16];
int visibleCount = 0;
float myX = 25.0, myY = 15.0;
unsigned long lastRssiSend = 0;
unsigned long lastFrame = 0;
bool spectreMode = false;
bool hunterPulse = false;
unsigned long pulseEnd = 0;
bool isGhost = false;

// ============ SETUP ============
void setup() {
  Serial.begin(115200);
  delay(100);

  // OLED
  Wire.setPins(OLED_SDA, OLED_SCL);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED fail");
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.println("SPECTRE BAND");
  display.println(BAND_ID);
  display.display();

  // LED
  strip.begin();
  strip.setBrightness(80);
  setTeamLED();

  // Haptic
  pinMode(HAPTIC_PIN, OUTPUT);
  digitalWrite(HAPTIC_PIN, LOW);

  // Button
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // BLE Beacon
  BLEDevice::init(BAND_ID.c_str());
  BLEBeacon beacon;
  beacon.setManufacturerId(0x4C00);
  beacon.setMajor(TEAM == "red" ? 1 : 2);
  beacon.setMinor(BAND_ID.substring(1).toInt() % 65536);

  // WiFi
  connectToField();

  // WebSocket
  ws.begin(WS_HOST, WS_PORT, "/ws");
  ws.onEvent(wsEvent);
}

// ============ LOOP ============
void loop() {
  ws.loop();

  // 5Hz RSSI scan
  if (millis() - lastRssiSend > 200) {
    sendRssiBatch();
    lastRssiSend = millis();
  }

  // 10Hz render
  if (millis() - lastFrame > 100) {
    renderRadar();
    lastFrame = millis();
  }

  // Button: mode toggle (short press) / ping (long press)
  handleButton();

  // Hunter-Prey pulse timeout
  if (hunterPulse && millis() > pulseEnd) {
    hunterPulse = false;
  }

  delay(10);
}

// ============ WIFI ============
void connectToField() {
  int n = WiFi.scanNetworks();
  String bestAP = "";
  int bestRSSI = -100;

  for (int i = 0; i < n; i++) {
    String ssid = WiFi.SSID(i);
    if (ssid.startsWith(FIELD_SSID_PREFIX) && WiFi.RSSI(i) > bestRSSI) {
      bestAP = ssid;
      bestRSSI = WiFi.RSSI(i);
    }
  }

  if (bestAP != "") {
    WiFi.begin(bestAP.c_str(), "spectrefield");
    int retries = 0;
    while (WiFi.status() != WL_CONNECTED && retries < 20) {
      delay(500);
      retries++;
    }
  }

  display.clearDisplay();
  display.setCursor(0, 0);
  display.println(WiFi.status() == WL_CONNECTED ? "CONNECTED" : "OFFLINE");
  display.println(bestAP);
  display.display();
}

// ============ WEBSOCKET ============
void wsEvent(WStype_t type, uint8_t* payload, size_t len) {
  if (type == WStype_TEXT) {
    String msg = String((char*)payload);
    parseServerMessage(msg);
  }
}

void parseServerMessage(String& msg) {
  // JSON parse: {"type":"state","you":{"x":10,"y":20},"visible":[...],"mode":"spectre"}
  // Simplified: extract mode
  if (msg.indexOf("\"mode\":\"spectre\"") >= 0) {
    spectreMode = true;
  } else if (msg.indexOf("\"mode\":\"hunter\"") >= 0) {
    spectreMode = false;
  }

  if (msg.indexOf("\"pulse\":true") >= 0) {
    hunterPulse = true;
    pulseEnd = millis() + 3000;
    hapticBuzz(200);
  }

  if (msg.indexOf("\"hit\":true") >= 0) {
    hapticBuzz(500);
    flashLED(255, 255, 255);
  }

  if (msg.indexOf("\"eliminated\":true") >= 0) {
    isGhost = true;
    hapticBuzz(1000);
  }

  // Parse visible players (simplified)
  visibleCount = 0;
  int idx = msg.indexOf("\"visible\":");
  if (idx >= 0) {
    // Extract array of player objects
    // Real implementation would use ArduinoJson
  }
}

// ============ RSSI SCAN ============
void sendRssiBatch() {
  if (WiFi.status() != WL_CONNECTED) return;

  String json = "{\"type\":\"rssi_batch\",\"band_id\":\"" + BAND_ID + "\",\"team\":\"" + TEAM + "\",\"readings\":[";

  int n = WiFi.scanNetworks(false, true);
  for (int i = 0; i < n && i < 8; i++) {
    if (i > 0) json += ",";
    json += "{\"ap_id\":\"" + WiFi.BSSIDstr(i) + "\",\"rssi\":" + WiFi.RSSI(i) + "}";
  }
  json += "]}";

  ws.sendTXT(json);
}

// ============ RADAR RENDER ============
void renderRadar() {
  display.clearDisplay();

  // Draw field boundary (50x30m scaled to 64x64px)
  display.drawRect(32, 0, 64, 64, SSD1306_WHITE);

  // Draw self at center
  int sx = 32 + 32;  // center x
  int sy = 32;         // center y
  display.fillCircle(sx, sy, 2, SSD1306_WHITE);

  // Draw visible players
  for (int i = 0; i < visibleCount; i++) {
    Player& p = visiblePlayers[i];
    int px = sx + (int)((p.x - myX) * 1.28);  // scale 50m -> 64px
    int py = sy - (int)((p.y - myY) * 2.13);  // scale 30m -> 64px

    if (px >= 32 && px < 96 && py >= 0 && py < 64) {
      bool isEnemy = (p.team != TEAM);
      bool show = false;

      if (spectreMode && isEnemy) show = true;
      else if (hunterPulse && isEnemy) show = true;
      else if (isGhost) show = true;
      else if (!isEnemy) show = true;

      if (show) {
        display.drawCircle(px, py, 2, SSD1306_WHITE);
        if (isEnemy) display.drawLine(sx, sy, px, py, SSD1306_WHITE);
      }
    }
  }

  // Draw mode indicator
  display.setCursor(0, 0);
  display.print(spectreMode ? "SPEC" : (hunterPulse ? "PULSE" : (isGhost ? "GHOST" : "LIVE")));

  // Draw team color bar
  display.fillRect(0, 56, 128, 8, SSD1306_WHITE);

  display.display();
}

// ============ HAPTIC ============
void hapticBuzz(int ms) {
  digitalWrite(HAPTIC_PIN, HIGH);
  delay(ms);
  digitalWrite(HAPTIC_PIN, LOW);
}

// ============ LED ============
void setTeamLED() {
  if (TEAM == "red") strip.setPixelColor(0, strip.Color(255, 0, 0));
  else strip.setPixelColor(0, strip.Color(0, 0, 255));
  strip.show();
}

void flashLED(uint8_t r, uint8_t g, uint8_t b) {
  for (int i = 0; i < 3; i++) {
    strip.setPixelColor(i, strip.Color(r, g, b));
  }
  strip.show();
  delay(200);
  setTeamLED();
}

// ============ BUTTON ============
void handleButton() {
  static bool lastState = HIGH;
  static unsigned long pressStart = 0;
  bool state = digitalRead(BUTTON_PIN);

  if (state == LOW && lastState == HIGH) {
    pressStart = millis();
  } else if (state == HIGH && lastState == LOW) {
    unsigned long duration = millis() - pressStart;
    if (duration < 500) {
      // Short press: ping location to team
      ws.sendTXT("{\"type\":\"ping\",\"band_id\":\"" + BAND_ID + "\"}");
    } else {
      // Long press: nothing yet (reserved)
    }
  }
  lastState = state;
}
