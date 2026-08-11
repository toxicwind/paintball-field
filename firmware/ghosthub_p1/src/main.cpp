/*
 * GhostHub P1 Firmware
 * Heltec HT-M00 Dual Channel LoRa Gateway
 * Bridges LoRaWAN player/objective traffic to field server via Ethernet/WiFi
 */

#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

// LoRa config
#define LORA_BAND 915E6
#define LORA_SF 7
#define LORA_BW 125E3

// Network config (AP mode fallback)
const char* AP_SSID = "GhostNet_Field";
const char* AP_PASS = "paintball2026";

// Server endpoint
const char* SERVER_HOST = "192.168.4.2";  // Field server IP
const int SERVER_PORT = 8000;

WebServer server(80);

// Packet buffer
struct GamePacket {
    uint8_t player_id;
    uint8_t team_id;
    uint8_t status;
    uint8_t objective_id;
    uint16_t rssi;
    uint32_t timestamp;
} __attribute__((packed));

// Downlink queue
struct DownlinkCmd {
    uint8_t cmd;
    uint8_t target_player;
    uint8_t param;
} __attribute__((packed));

void handleStatus() {
    StaticJsonDocument<256> doc;
    doc["status"] = "online";
    doc["uptime"] = millis() / 1000;
    doc["packets_rx"] = 0;  // TODO: track
    doc["packets_tx"] = 0;
    doc["lora_band"] = LORA_BAND;
    doc["clients"] = WiFi.softAPgetStationNum();
    
    String response;
    serializeJson(doc, response);
    server.send(200, "application/json", response);
}

void handleDownlink() {
    if (!server.hasArg("cmd") || !server.hasArg("player")) {
        server.send(400, "text/plain", "Missing cmd or player");
        return;
    }
    
    uint8_t cmd = server.arg("cmd").toInt();
    uint8_t player = server.arg("player").toInt();
    uint8_t param = server.hasArg("param") ? server.arg("param").toInt() : 0;
    
    DownlinkCmd dl;
    dl.cmd = cmd;
    dl.target_player = player;
    dl.param = param;
    
    // TODO: Queue for LoRa transmission
    
    server.send(200, "application/json", "{\"queued\":true}");
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    
    Serial.println("GhostHub P1 initializing...");
    
    // Start AP mode
    WiFi.softAP(AP_SSID, AP_PASS);
    Serial.print("AP IP: ");
    Serial.println(WiFi.softAPIP());
    
    // HTTP endpoints
    server.on("/status", HTTP_GET, handleStatus);
    server.on("/downlink", HTTP_POST, handleDownlink);
    server.begin();
    
    // TODO: Initialize dual-channel LoRa
    // Radio.Init();
    // Radio.SetChannel(LORA_BAND);
    
    Serial.println("GhostHub P1 ready.");
}

void loop() {
    server.handleClient();
    
    // TODO: Process incoming LoRa packets
    // if (Radio.IrqProcess()) {
    //     GamePacket pkt;
    //     Radio.GetRxPacket((uint8_t*)&pkt, sizeof(pkt));
    //     // Forward to server
    // }
    
    // TODO: Process downlink queue
    // Send queued downlink commands via LoRa
    
    delay(10);
}
