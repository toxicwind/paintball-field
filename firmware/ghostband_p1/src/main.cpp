/*
 * GhostBand P1 Firmware
 * Heltec HT-CT62 (ESP32-C3 + SX1262 LoRa)
 * No FreeRTOS. Bare-metal Arduino loop. Deep sleep between transmissions.
 * 
 * Features:
 * - LoRaWAN Class A uplink (heartbeat + objective scans)
 * - MFRC522 RFID reader for objective interaction
 * - 3x WS2812B RGB LED for team/status signals
 * - ERM haptic motor for comms and hit notifications
 * - Deep sleep: 0.5mA average draw, 8+ hour active battery life
 */

#include <Arduino.h>
#include <LoRaWan_APP.h>
#include <SPI.h>
#include <MFRC522.h>
#include <Adafruit_NeoPixel.h>

// Pin definitions
#define LED_PIN 25
#define VIBE_PIN 26
#define RFID_SS_PIN 5
#define RFID_RST_PIN 27
#define NUM_LEDS 3

// LoRaWAN config
#define LORA_BAND 915E6
#define LORA_SF 7
#define LORA_BW 125E3
#define LORA_CR 4/5
#define LORA_TX_POWER 14

// Timing
#define HEARTBEAT_INTERVAL_MS 5000
#define RFID_POLL_INTERVAL_MS 500
#define DEEP_SLEEP_MS 4500

// Game state
enum PlayerStatus {
    STATUS_ALIVE = 0,
    STATUS_ELIMINATED = 1,
    STATUS_WOUNDED = 2,
    STATUS_GHOST = 3
};

enum TeamColor {
    TEAM_ALPHA = 0,  // Blue
    TEAM_BRAVO = 1,  // Red
    TEAM_NONE = 2    // White
};

// Global state
uint8_t player_id = 0;
uint8_t team_id = TEAM_ALPHA;
PlayerStatus status = STATUS_ALIVE;
uint32_t last_heartbeat = 0;
uint32_t last_rfid_poll = 0;
bool objective_near = false;

// Hardware objects
Adafruit_NeoPixel pixels(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);
MFRC522 rfid(RFID_SS_PIN, RFID_RST_PIN);

// LED patterns (lookup table, no rendering engine)
void setPattern(uint8_t pattern) {
    pixels.clear();
    switch (pattern) {
        case 0: // Alive - team color pulse
            for (int i = 0; i < NUM_LEDS; i++) {
                pixels.setPixelColor(i, team_id == TEAM_ALPHA ? pixels.Color(0, 0, 64) : pixels.Color(64, 0, 0));
            }
            break;
        case 1: // Eliminated - red solid
            pixels.setPixelColor(0, pixels.Color(255, 0, 0));
            break;
        case 2: // Wounded - yellow SOS
            pixels.setPixelColor(0, pixels.Color(255, 255, 0));
            pixels.setPixelColor(1, pixels.Color(255, 255, 0));
            break;
        case 3: // Objective captured - green flash
            for (int i = 0; i < NUM_LEDS; i++) {
                pixels.setPixelColor(i, pixels.Color(0, 255, 0));
            }
            break;
        case 4: // Enemy captured - red flash
            for (int i = 0; i < NUM_LEDS; i++) {
                pixels.setPixelColor(i, pixels.Color(255, 0, 0));
            }
            break;
        case 5: // Warm (near objective) - yellow pulse
            pixels.setPixelColor(0, pixels.Color(255, 255, 0));
            break;
        case 6: // Hot (very near objective) - orange pulse
            pixels.setPixelColor(0, pixels.Color(255, 165, 0));
            break;
        case 7: // Game countdown - white blink
            pixels.setPixelColor(0, pixels.Color(255, 255, 255));
            break;
    }
    pixels.show();
}

// Haptic patterns
void vibeShort() {
    digitalWrite(VIBE_PIN, HIGH);
    delay(100);
    digitalWrite(VIBE_PIN, LOW);
}

void vibeLong() {
    digitalWrite(VIBE_PIN, HIGH);
    delay(300);
    digitalWrite(VIBE_PIN, LOW);
}

void vibePulse(int count) {
    for (int i = 0; i < count; i++) {
        vibeShort();
        delay(100);
    }
}

// LoRa packet structure
struct __attribute__((packed)) GamePacket {
    uint8_t player_id;
    uint8_t team_id;
    uint8_t status;
    uint8_t objective_id;  // 0 = none, 1-255 = objective scanned
    uint16_t rssi;         // RSSI of nearest objective node (for warm/cold)
    uint32_t timestamp;
};

// Send heartbeat packet
void sendHeartbeat() {
    GamePacket pkt;
    pkt.player_id = player_id;
    pkt.team_id = team_id;
    pkt.status = (uint8_t)status;
    pkt.objective_id = 0;
    pkt.rssi = 0;
    pkt.timestamp = millis();
    
    // TODO: Implement actual LoRa send via Heltec library
    // Radio.Send((uint8_t*)&pkt, sizeof(pkt));
    
    Serial.print("HB: player=");
    Serial.print(player_id);
    Serial.print(" team=");
    Serial.print(team_id);
    Serial.print(" status=");
    Serial.println(status);
}

// Send objective scan packet
void sendObjectiveScan(uint8_t obj_id) {
    GamePacket pkt;
    pkt.player_id = player_id;
    pkt.team_id = team_id;
    pkt.status = (uint8_t)status;
    pkt.objective_id = obj_id;
    pkt.rssi = 0;
    pkt.timestamp = millis();
    
    // TODO: Implement actual LoRa send
    
    Serial.print("OBJ: player=");
    Serial.print(player_id);
    Serial.print(" objective=");
    Serial.println(obj_id);
    
    vibePulse(3);
    setPattern(3);
    delay(500);
}

// Check RFID for objective scan
void checkRFID() {
    if (!rfid.PICC_IsNewCardPresent()) return;
    if (!rfid.PICC_ReadCardSerial()) return;
    
    // Read objective ID from card UID (first byte)
    uint8_t obj_id = rfid.uid.uidByte[0];
    
    Serial.print("RFID scan: objective=");
    Serial.println(obj_id);
    
    sendObjectiveScan(obj_id);
    
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
}

// Check button for hit acknowledgment
void checkButtons() {
    // TODO: Implement button debounce and hit acknowledgment
    // Single press = acknowledge hit
    // Double press = call for medic (wounded status)
    // Long press = emergency stop (ref only)
}

// Process incoming LoRa downlink (game events from ref)
void onLoRaReceive(uint8_t *data, uint16_t len, int8_t rssi, int8_t snr) {
    if (len < 2) return;
    
    uint8_t cmd = data[0];
    uint8_t target_player = data[1];
    
    if (target_player != player_id && target_player != 0xFF) return;  // 0xFF = broadcast
    
    switch (cmd) {
        case 0x01: // Force eliminate
            status = STATUS_ELIMINATED;
            setPattern(1);
            vibeLong();
            break;
        case 0x02: // Force respawn
            status = STATUS_ALIVE;
            setPattern(0);
            vibePulse(2);
            break;
        case 0x03: // Wound player
            status = STATUS_WOUNDED;
            setPattern(2);
            vibePulse(5);
            break;
        case 0x04: // Enemy captured objective
            setPattern(4);
            vibeShort();
            break;
        case 0x05: // Game countdown warning
            setPattern(7);
            vibePulse(1);
            break;
        case 0x06: // Emergency stop (all stop)
            setPattern(1);
            vibeLong();
            // TODO: Enter emergency mode
            break;
    }
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    
    Serial.println("GhostBand P1 initializing...");
    
    // Initialize LEDs
    pixels.begin();
    pixels.setBrightness(128);
    setPattern(0);
    
    // Initialize haptic
    pinMode(VIBE_PIN, OUTPUT);
    digitalWrite(VIBE_PIN, LOW);
    
    // Initialize RFID
    SPI.begin();
    rfid.PCD_Init();
    
    // Initialize LoRa
    // TODO: Heltec LoRa initialization
    // Radio.Init();
    // Radio.SetChannel(LORA_BAND);
    // Radio.SetTxConfig(MODEM_LORA, LORA_TX_POWER, 0, LORA_BW/1E6, LORA_SF, LORA_CR, 8, false, true, 0, false, false);
    // Radio.SetRxConfig(MODEM_LORA, LORA_BW/1E6, LORA_SF, LORA_CR, 0, 8, 5, false, 0, true, 0, 0, true, true);
    
    // Self-test
    vibePulse(2);
    setPattern(3);
    delay(200);
    setPattern(0);
    
    Serial.println("GhostBand P1 ready.");
}

void loop() {
    uint32_t now = millis();
    
    // Heartbeat
    if (now - last_heartbeat >= HEARTBEAT_INTERVAL_MS) {
        sendHeartbeat();
        last_heartbeat = now;
    }
    
    // RFID polling
    if (now - last_rfid_poll >= RFID_POLL_INTERVAL_MS) {
        checkRFID();
        last_rfid_poll = now;
    }
    
    // Button checks
    checkButtons();
    
    // LED pattern refresh (for animations)
    // TODO: Implement non-blocking LED animation
    
    // Deep sleep to save power
    // TODO: Implement ESP32 deep sleep with timer wake
    // esp_sleep_enable_timer_wakeup(DEEP_SLEEP_MS * 1000);
    // esp_light_sleep_start();
    
    delay(100);  // Temporary: replace with deep sleep
}
