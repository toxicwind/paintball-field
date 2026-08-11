#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_NeoPixel.h>

// ============ CONFIG ============
const char* FIELD_SSID = "SPECTRE-FIELD";
const char* FIELD_PASS = "spectrefield";
const char* MQTT_SERVER = "192.168.4.1";
const int MQTT_PORT = 1883;
const String NODE_ID = "NODE-" + String((uint32_t)ESP.getEfuseMac());
String NODE_TYPE = "bomb";  // "bomb", "zone", "flag", "terminal"

// Pins: ESP32-C3-DevKitM-1
#define OLED_SDA 8
#define OLED_SCL 9
#define LED_RING_PIN 10
#define BUZZER_PIN 11
#define ACTION_BTN 12
#define CANCEL_BTN 13

// ============ HARDWARE ============
Adafruit_SSD1306 display(128, 64, &Wire, -1);
Adafruit_NeoPixel ring(8, LED_RING_PIN, NEO_GRB + NEO_KHZ800);
WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

// ============ STATE ============
String ownerTeam = "";
String state = "idle";  // idle, capturing, captured, planting, planted, defusing, hacked
int progress = 0;
unsigned long actionStart = 0;
unsigned long lastBlink = 0;
bool blinkState = false;

// ============ SETUP ============
void setup() {
  Serial.begin(115200);

  Wire.setPins(OLED_SDA, OLED_SCL);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.println(NODE_ID);
  display.println(NODE_TYPE);
  display.display();

  ring.begin();
  ring.setBrightness(100);
  setRingColor(255, 255, 255);  // White = neutral

  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);
  pinMode(ACTION_BTN, INPUT_PULLUP);
  pinMode(CANCEL_BTN, INPUT_PULLUP);

  WiFi.begin(FIELD_SSID, FIELD_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(500);

  mqtt.setServer(MQTT_SERVER, MQTT_PORT);
  mqtt.setCallback(mqttCallback);
  reconnectMQTT();

  announceNode();
}

// ============ LOOP ============
void loop() {
  if (!mqtt.connected()) reconnectMQTT();
  mqtt.loop();

  handleButtons();
  updateDisplay();
  updateLEDs();

  delay(50);
}

// ============ MQTT ============
void reconnectMQTT() {
  while (!mqtt.connected()) {
    if (mqtt.connect(NODE_ID.c_str())) {
      mqtt.subscribe(("nodes/" + NODE_ID + "/cmd").c_str());
    } else {
      delay(5000);
    }
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int len) {
  String msg = "";
  for (int i = 0; i < len; i++) msg += (char)payload[i];

  if (msg == "RESET") {
    resetNode();
  } else if (msg.startsWith("SET_TYPE:")) {
    NODE_TYPE = msg.substring(9);
  }
}

void announceNode() {
  String json = "{\"type\":\"announce\",\"node_id\":\"" + NODE_ID + "\",\"node_type\":\"" + NODE_TYPE + "\",\"ip\":\"" + WiFi.localIP().toString() + "\"}";
  mqtt.publish("nodes/announce", json.c_str());
}

// ============ BUTTONS ============
void handleButtons() {
  if (digitalRead(ACTION_BTN) == LOW) {
    handleAction();
  }
  if (digitalRead(CANCEL_BTN) == LOW) {
    handleCancel();
  }
}

void handleAction() {
  if (NODE_TYPE == "zone" && state == "idle") {
    state = "capturing";
    actionStart = millis();
  } else if (NODE_TYPE == "bomb" && state == "idle") {
    state = "planting";
    actionStart = millis();
    tone(BUZZER_PIN, 1000, 100);
  } else if (NODE_TYPE == "bomb" && state == "planted") {
    state = "defusing";
    actionStart = millis();
    tone(BUZZER_PIN, 800, 100);
  } else if (NODE_TYPE == "terminal" && state == "idle") {
    state = "hacking";
    actionStart = millis();
  } else if (NODE_TYPE == "flag" && state == "idle") {
    // Pick up flag
    mqtt.publish(("nodes/" + NODE_ID + "/event").c_str(), "{\"type\":\"pickup\"}");
    state = "carried";
  }

  // Progress
  if (state == "capturing" || state == "planting" || state == "defusing" || state == "hacking") {
    unsigned long elapsed = millis() - actionStart;
    int required = (NODE_TYPE == "defusing") ? 7000 : ((NODE_TYPE == "hacking") ? 15000 : 5000);
    progress = (elapsed * 100) / required;

    if (progress >= 100) {
      completeAction();
    }
  }
}

void handleCancel() {
  if (state == "capturing" || state == "planting" || state == "defusing" || state == "hacking") {
    state = (state == "defusing") ? "planted" : "idle";
    progress = 0;
    tone(BUZZER_PIN, 400, 200);
  }
}

void completeAction() {
  if (state == "capturing") {
    state = "captured";
    ownerTeam = "red";  // Would be set from player band team
    mqtt.publish(("nodes/" + NODE_ID + "/event").c_str(), "{\"type\":\"captured\",\"team\":\"red\"}");
  } else if (state == "planting") {
    state = "planted";
    mqtt.publish(("nodes/" + NODE_ID + "/event").c_str(), "{\"type\":\"planted\"}");
  } else if (state == "defusing") {
    state = "defused";
    mqtt.publish(("nodes/" + NODE_ID + "/event").c_str(), "{\"type\":\"defused\"}");
  } else if (state == "hacking") {
    state = "hacked";
    mqtt.publish(("nodes/" + NODE_ID + "/event").c_str(), "{\"type\":\"hacked\"}");
  }
  progress = 100;
  tone(BUZZER_PIN, 2000, 500);
}

void resetNode() {
  state = "idle";
  ownerTeam = "";
  progress = 0;
  setRingColor(255, 255, 255);
}

// ============ DISPLAY ============
void updateDisplay() {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println(NODE_ID);
  display.println(NODE_TYPE.toUpperCase());
  display.println("State: " + state);

  if (progress > 0 && progress < 100) {
    display.drawRect(0, 40, 128, 10, SSD1306_WHITE);
    display.fillRect(2, 42, (124 * progress) / 100, 6, SSD1306_WHITE);
  }

  display.display();
}

// ============ LEDS ============
void updateLEDs() {
  if (state == "idle") {
    setRingColor(255, 255, 255);  // White
  } else if (state == "capturing" || state == "planting" || state == "hacking") {
    // Blink yellow during action
    if (millis() - lastBlink > 200) {
      blinkState = !blinkState;
      lastBlink = millis();
    }
    setRingColor(blinkState ? 255 : 0, blinkState ? 255 : 0, 0);
  } else if (state == "captured") {
    setRingColor(ownerTeam == "red" ? 255 : 0, 0, ownerTeam == "blue" ? 255 : 0);
  } else if (state == "planted") {
    // Red blink countdown
    if (millis() - lastBlink > 500) {
      blinkState = !blinkState;
      lastBlink = millis();
    }
    setRingColor(blinkState ? 255 : 50, 0, 0);
  } else if (state == "defused") {
    setRingColor(0, 255, 0);  // Green
  } else if (state == "hacked") {
    setRingColor(128, 0, 255);  // Purple
  }
}

void setRingColor(uint8_t r, uint8_t g, uint8_t b) {
  for (int i = 0; i < 8; i++) {
    ring.setPixelColor(i, ring.Color(r, g, b));
  }
  ring.show();
}
