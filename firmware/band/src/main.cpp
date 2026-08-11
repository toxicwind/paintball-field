#include <WiFi.h>
#include <BLEDevice.h>
#include <BLEBeacon.h>
#include <WebSocketsClient.h>
#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_NeoPixel.h>
#include <BMI270.h>  // IMU for dead reckoning

// ============ CONFIG ============
const char* FIELD_SSID_PREFIX = "SPECTRE-AP-";
const char* WS_HOST = "192.168.4.1";
const int WS_PORT = 8765;
const String BAND_ID = "B" + String((uint32_t)ESP.getEfuseMac());
String TEAM = "red";

// Pins: ESP32-C3-MINI-1
#define OLED_SDA 8
#define OLED_SCL 9
#define LED_PIN 10
#define HAPTIC_PIN 11
#define BUTTON_PIN 12
#define PIEZO_PIN 13  // Shock sensor input

// ============ HARDWARE ============
Adafruit_SSD1306 display(128, 64, &Wire, -1);
Adafruit_NeoPixel strip(3, LED_PIN, NEO_GRB + NEO_KHZ800);
WebSocketsClient ws;
BMI270 imu;

// ============ STATE ============
struct Player { String id; float x, y; String team; bool visible; float dist; };
Player visiblePlayers[16];
int visibleCount = 0;
float myX = 25.0, myY = 15.0;
float lastImuX = 0, lastImuY = 0;
unsigned long lastRssiSend = 0;
unsigned long lastFrame = 0;
bool spectreMode = false;
bool hunterPulse = false;
unsigned long pulseEnd = 0;
bool isGhost = false;
bool isHit = false;
bool isMarked = false;
bool isRespawning = false;
int reinforcements = 50;

// RSSI median filter: last 5 readings per AP
#define MAX_APS 8
#define MEDIAN_WINDOW 5
struct ApRssi { String id; int readings[MEDIAN_WINDOW]; int idx; int count; };
ApRssi apRssi[MAX_APS];
int apRssiCount = 0;

// ============ SELF-TEST ============
bool selfTest() {
  bool ok = true;

  // Test OLED
  display.clearDisplay();
  display.setCursor(0,0);
  display.println("SELF TEST");
  display.display();
  ok &= display.getBuffer() != nullptr;

  // Test Haptic
  digitalWrite(HAPTIC_PIN, HIGH);
  delay(100);
  digitalWrite(HAPTIC_PIN, LOW);

  // Test LEDs
  strip.setPixelColor(0, strip.Color(255,0,0)); strip.show(); delay(100);
  strip.setPixelColor(0, strip.Color(0,255,0)); strip.show(); delay(100);
  strip.setPixelColor(0, strip.Color(0,0,255)); strip.show(); delay(100);
  setTeamLED();

  // Test IMU
  ok &= imu.begin(Wire, BMI270_ADDR);

  // Test Battery (read ADC)
  int bat = analogRead(0);
  ok &= bat > 1000; // ~3.3V threshold

  // Test AP count
  int n = WiFi.scanNetworks();
  int apCount = 0;
  for (int i=0; i<n; i++) if (WiFi.SSID(i).startsWith(FIELD_SSID_PREFIX)) apCount++;

  display.clearDisplay();
  display.setCursor(0,0);
  display.println("SELF TEST");
  display.println(ok ? "PASS" : "FAIL");
  display.print("APs:"); display.println(apCount);
  display.print("BAT:"); display.println(bat);
  display.display();

  return ok;
}

// ============ SETUP ============
void setup() {
  Serial.begin(115200);
  delay(100);

  Wire.setPins(OLED_SDA, OLED_SCL);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  strip.begin();
  strip.setBrightness(80);
  setTeamLED();

  pinMode(HAPTIC_PIN, OUTPUT);
  digitalWrite(HAPTIC_PIN, LOW);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(PIEZO_PIN, INPUT);

  // Run self-test
  bool ok = selfTest();
  if (!ok) {
    display.println("BAND FAULT");
    display.display();
    while(1) { delay(1000); } // Halt - staff replaces band
  }

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

  // FreeRTOS tasks
  xTaskCreatePinnedToCore(wifiScanTask, "WiFiScan", 4096, NULL, 1, NULL, 0);
  xTaskCreatePinnedToCore(wsRenderTask, "WSRender", 8192, NULL, 1, NULL, 1);
  xTaskCreatePinnedToCore(bleScanTask, "BLEScan", 4096, NULL, 1, NULL, 1);
  xTaskCreatePinnedToCore(shockDetectTask, "Shock", 2048, NULL, 2, NULL, 1);
}

void loop() {
  // Main loop handles button + state machine
  handleButton();

  if (isHit && !isMarked) {
    display.clearDisplay();
    display.setCursor(0,0);
    display.println("YOU'RE HIT!");
    display.println("MARK BAND");
    display.display();
    digitalWrite(HAPTIC_PIN, HIGH);
  }

  if (isMarked && !isRespawning) {
    display.clearDisplay();
    display.setCursor(0,0);
    display.println("RETURN TO");
    display.println("CHECKPOINT");
    // Arrow pointing to nearest checkpoint
    display.display();
  }

  delay(10);
}

// ============ FREERTOS TASKS ============

void wifiScanTask(void* pvParameters) {
  while(1) {
    if (WiFi.status() == WL_CONNECTED) {
      int n = WiFi.scanNetworks(false, true);

      // Median filter per AP
      for (int i=0; i<n && i<MAX_APS; i++) {
        String ssid = WiFi.SSID(i);
        if (!ssid.startsWith(FIELD_SSID_PREFIX)) continue;

        int rssi = WiFi.RSSI(i);
        String bssid = WiFi.BSSIDstr(i);

        // Find or create AP entry
        int idx = -1;
        for (int j=0; j<apRssiCount; j++) {
          if (apRssi[j].id == bssid) { idx = j; break; }
        }
        if (idx == -1 && apRssiCount < MAX_APS) {
          idx = apRssiCount++;
          apRssi[idx].id = bssid;
          apRssi[idx].count = 0;
          apRssi[idx].idx = 0;
        }

        if (idx >= 0) {
          // Outlier reject: if jump >15dBm from median, skip
          if (apRssi[idx].count > 0) {
            int sorted[MEDIAN_WINDOW];
            memcpy(sorted, apRssi[idx].readings, sizeof(sorted));
            std::sort(sorted, sorted + min(apRssi[idx].count, MEDIAN_WINDOW));
            int median = sorted[apRssi[idx].count/2];
            if (abs(rssi - median) > 15) continue; // Outlier
          }

          apRssi[idx].readings[apRssi[idx].idx] = rssi;
          apRssi[idx].idx = (apRssi[idx].idx + 1) % MEDIAN_WINDOW;
          if (apRssi[idx].count < MEDIAN_WINDOW) apRssi[idx].count++;
        }
      }

      // Build JSON with median-filtered RSSI
      String json = "{\"type\":\"rssi_batch\",\"band_id\":\"" + BAND_ID + "\",\"team\":\"" + TEAM + "\",\"readings\":[";
      int first = 1;
      for (int j=0; j<apRssiCount; j++) {
        if (apRssi[j].count == 0) continue;
        int sorted[MEDIAN_WINDOW];
        memcpy(sorted, apRssi[j].readings, sizeof(sorted));
        std::sort(sorted, sorted + apRssi[j].count);
        int median = sorted[apRssi[j].count/2];

        if (!first) json += ",";
        first = 0;
        json += "{\"ap_id\":\"" + apRssi[j].id + "\",\"rssi\":" + String(median) + "}";
      }
      json += "]}";

      // Send via WebSocket (thread-safe queue would be better)
      ws.sendTXT(json);
    }
    vTaskDelay(pdMS_TO_TICKS(200)); // 5Hz
  }
}

void wsRenderTask(void* pvParameters) {
  while(1) {
    ws.loop();

    if (!isHit && !isMarked) {
      renderRadar();
    }

    vTaskDelay(pdMS_TO_TICKS(100)); // 10Hz render
  }
}

void bleScanTask(void* pvParameters) {
  while(1) {
    // BLE scan for hit detection (Tier 2+)
    // Simplified - full implementation in hit_module.cpp
    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void shockDetectTask(void* pvParameters) {
  while(1) {
    int shock = analogRead(PIEZO_PIN);
    if (shock > 500 && !isHit) { // Threshold for 300fps impact
      isHit = true;
      // Send hit to server for validation
      String json = "{\"type\":\"shock_hit\",\"band_id\":\"" + BAND_ID + "\",\"shock\":" + String(shock) + "}";
      ws.sendTXT(json);
    }
    vTaskDelay(pdMS_TO_TICKS(50)); // 20Hz shock sampling
  }
}

// ============ WIFI ============
void connectToField() {
  int n = WiFi.scanNetworks();
  String bestAP = "";
  int bestRSSI = -100;

  for (int i=0; i<n; i++) {
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
      delay(500); retries++;
    }
  }
}

// ============ WEBSOCKET ============
void wsEvent(WStype_t type, uint8_t* payload, size_t len) {
  if (type == WStype_TEXT) {
    String msg = String((char*)payload);
    parseServerMessage(msg);
  }
}

void parseServerMessage(String& msg) {
  if (msg.indexOf("\"mode\":\"spectre\"") >= 0) spectreMode = true;
  else if (msg.indexOf("\"mode\":\"hunter\"") >= 0) spectreMode = false;

  if (msg.indexOf("\"pulse\":true") >= 0) {
    hunterPulse = true;
    pulseEnd = millis() + 3000;
    digitalWrite(HAPTIC_PIN, HIGH); delay(200); digitalWrite(HAPTIC_PIN, LOW);
  }

  if (msg.indexOf("\"hit_confirmed\":true") >= 0) {
    isHit = true;
    digitalWrite(HAPTIC_PIN, HIGH); delay(500); digitalWrite(HAPTIC_PIN, LOW);
    flashLED(255,255,255);
  }

  if (msg.indexOf("\"eliminated\":true") >= 0) {
    isGhost = true;
    digitalWrite(HAPTIC_PIN, HIGH); delay(1000); digitalWrite(HAPTIC_PIN, LOW);
  }

  if (msg.indexOf("\"respawn\":true") >= 0) {
    isHit = false;
    isMarked = false;
    isRespawning = false;
  }
}

// ============ RADAR RENDER ============
void renderRadar() {
  display.clearDisplay();
  display.drawRect(32, 0, 64, 64, SSD1306_WHITE);
  int sx = 64, sy = 32;
  display.fillCircle(sx, sy, 2, SSD1306_WHITE);

  for (int i=0; i<visibleCount; i++) {
    Player& p = visiblePlayers[i];
    int px = sx + (int)((p.x - myX) * 1.28);
    int py = sy - (int)((p.y - myY) * 2.13);
    if (px >= 32 && px < 96 && py >= 0 && py < 64) {
      bool isEnemy = (p.team != TEAM);
      bool show = spectreMode || hunterPulse || isGhost || !isEnemy;
      if (show) {
        display.drawCircle(px, py, 2, SSD1306_WHITE);
        if (isEnemy) display.drawLine(sx, sy, px, py, SSD1306_WHITE);
      }
    }
  }

  display.setCursor(0,0);
  display.print(spectreMode ? "SPEC" : (hunterPulse ? "PULSE" : (isGhost ? "GHOST" : "LIVE")));
  display.fillRect(0, 56, 128, 8, SSD1306_WHITE);
  display.display();
}

// ============ HELPERS ============
void setTeamLED() {
  if (TEAM == "red") strip.setPixelColor(0, strip.Color(255,0,0));
  else strip.setPixelColor(0, strip.Color(0,0,255));
  strip.show();
}

void flashLED(uint8_t r, uint8_t g, uint8_t b) {
  for (int i=0; i<3; i++) strip.setPixelColor(i, strip.Color(r,g,b));
  strip.show(); delay(200); setTeamLED();
}

void handleButton() {
  static bool lastState = HIGH;
  static unsigned long pressStart = 0;
  bool state = digitalRead(BUTTON_PIN);

  if (state == LOW && lastState == HIGH) {
    pressStart = millis();
  } else if (state == HIGH && lastState == LOW) {
    unsigned long duration = millis() - pressStart;
    if (duration < 500) {
      if (isHit && !isMarked) {
        isMarked = true;
        digitalWrite(HAPTIC_PIN, LOW);
        ws.sendTXT("{\"type\":\"mark_hit\",\"band_id\":\"" + BAND_ID + "\"}");
      } else {
        ws.sendTXT("{\"type\":\"ping\",\"band_id\":\"" + BAND_ID + "\"}");
      }
    }
  }
  lastState = state;
}
