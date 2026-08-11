#include <BLEDevice.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

// ============ CONFIG ============
const String BAND_ID = "B" + String((uint32_t)ESP.getEfuseMac());
String TEAM = "red";

// Hit detection thresholds
#define HIT_RSSI_THRESHOLD -55    // dBm: closer than ~2m
#define HIT_DURATION_MS 500         // Must be within threshold for 500ms
#define HIT_COOLDOWN_MS 1000        // 1s between hits
#define DIRECTION_WINDOW_DEG 45   // Front/back/left/right window

// ============ STATE ============
BLEScan* pScan;
unsigned long hitStartTime = 0;
String potentialShooter = "";
bool hitInProgress = false;
unsigned long lastHitTime = 0;

// Direction mapping (simplified: based on beacon signal strength pattern)
// Real implementation would use multiple BLE receivers or antenna diversity
struct ShooterRecord {
  String id;
  int rssi;
  unsigned long firstSeen;
};
ShooterRecord shooters[8];
int shooterCount = 0;

// ============ SETUP ============
void setup() {
  Serial.begin(115200);
  BLEDevice::init(BAND_ID.c_str());
  pScan = BLEDevice::getScan();
  pScan->setActiveScan(true);
  pScan->setInterval(100);
  pScan->setWindow(99);
}

// ============ LOOP ============
void loop() {
  scanForShooters();
  evaluateHits();
  delay(100);
}

// ============ BLE SCAN ============
void scanForShooters() {
  BLEScanResults results = pScan->start(0.1, false);
  shooterCount = 0;

  for (int i = 0; i < results.getCount() && shooterCount < 8; i++) {
    BLEAdvertisedDevice device = results.getDevice(i);
    String name = device.getName().c_str();
    int rssi = device.getRSSI();

    // Only track other SpectreBands (name starts with B)
    if (name.startsWith("B") && name != BAND_ID) {
      shooters[shooterCount].id = name;
      shooters[shooterCount].rssi = rssi;
      shooters[shooterCount].firstSeen = millis();
      shooterCount++;
    }
  }
  pScan->clearResults();
}

// ============ HIT EVALUATION ============
void evaluateHits() {
  if (millis() - lastHitTime < HIT_COOLDOWN_MS) return;

  for (int i = 0; i < shooterCount; i++) {
    if (shooters[i].rssi > HIT_RSSI_THRESHOLD) {
      // Strong signal = close proximity = potential hit
      if (!hitInProgress) {
        hitInProgress = true;
        hitStartTime = millis();
        potentialShooter = shooters[i].id;
      } else if (potentialShooter == shooters[i].id) {
        // Same shooter, still close
        if (millis() - hitStartTime >= HIT_DURATION_MS) {
          registerHit(potentialShooter, shooters[i].rssi);
          hitInProgress = false;
          lastHitTime = millis();
        }
      }
    } else {
      // Shooter moved away
      if (hitInProgress && potentialShooter == shooters[i].id) {
        hitInProgress = false;
      }
    }
  }
}

// ============ HIT REGISTRATION ============
void registerHit(String shooterId, int rssi) {
  // Determine direction from RSSI trend (simplified)
  // In real implementation, use multiple antennas or RSSI history
  String direction = "unknown";

  // Send hit event to server
  String json = "{\"type\":\"hit\",\"target\":\"" + BAND_ID + "\",\"shooter\":\"" + shooterId + "\",\"rssi\":" + String(rssi) + "}";

  // Trigger haptic based on direction
  if (direction == "front") hapticFront();
  else if (direction == "back") hapticBack();
  else if (direction == "left") hapticLeft();
  else if (direction == "right") hapticRight();
  else hapticGeneric();
}

// ============ HAPTIC PATTERNS ============
void hapticGeneric() {
  // Single strong buzz
  digitalWrite(11, HIGH); delay(300); digitalWrite(11, LOW);
}

void hapticFront() {
  // Short pulse
  digitalWrite(11, HIGH); delay(100); digitalWrite(11, LOW); delay(50);
  digitalWrite(11, HIGH); delay(100); digitalWrite(11, LOW);
}

void hapticBack() {
  // Long pulse
  digitalWrite(11, HIGH); delay(400); digitalWrite(11, LOW);
}

void hapticLeft() {
  // Double pulse
  digitalWrite(11, HIGH); delay(100); digitalWrite(11, LOW); delay(100);
  digitalWrite(11, HIGH); delay(100); digitalWrite(11, LOW); delay(100);
  digitalWrite(11, HIGH); delay(100); digitalWrite(11, LOW);
}

void hapticRight() {
  // Triple pulse
  digitalWrite(11, HIGH); delay(80); digitalWrite(11, LOW); delay(80);
  digitalWrite(11, HIGH); delay(80); digitalWrite(11, LOW); delay(80);
  digitalWrite(11, HIGH); delay(80); digitalWrite(11, LOW); delay(80);
  digitalWrite(11, HIGH); delay(80); digitalWrite(11, LOW);
}
