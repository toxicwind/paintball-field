# Tier 1 — Objective Node

Physical boxes placed on the field. Players interact with them to capture, plant, defuse, or hack. Shared across all players — one node serves an entire match.

## What It Does

| Feature | How | Game Impact |
|---------|-----|-------------|
| Button Interface | 2x tactile buttons ("ACTION" + "CANCEL") | Plant bomb, capture zone, start hack |
| OLED Display | 0.96" OLED shows team color + progress bar | Visual feedback for all players nearby |
| LED Ring | 8x WS2812B in circle around box | Zone ownership color + countdown flash |
| Buzzer | Piezo buzzer for audio cues | Planting tone, defuse alarm, capture chime |
| BLE Beacon | Advertises node ID for proximity detection | Band knows when player is near node |
| WiFi Client | Connects to field server via MQTT | State sync: captured, planted, hacked |

## BOM — Per Node

| Component | Part Number | Supplier | Unit Price | Qty | Purpose |
|-----------|-------------|----------|------------|-----|---------|
| MCU | ESP32-C3-DevKitM-1 | AliExpress | $6.00 | 1 | WiFi client + BLE beacon + GPIO |
| Display | SSD1306 0.96" I2C OLED | LCSC | $1.50 | 1 | Progress bar + status |
| LED Ring | 8x WS2812B 5050 circle | AliExpress | $1.20 | 1 | Team color + countdown |
| Buttons | 12mm tactile switch | LCSC | $0.20 | 2 | Action + Cancel |
| Buzzer | 5V active piezo buzzer | LCSC | $0.50 | 1 | Audio cues |
| Battery | 18650 2600mAh + holder | AliExpress | $4.00 | 1 | All-day runtime |
| Charger | TP4056 + USB-C module | LCSC | $1.00 | 1 | Field charging |
| Enclosure | IP65 ABS box 120x80x50mm | AliExpress | $3.00 | 1 | Weatherproof |
| Passives | Wires, resistors, headers | LCSC | $1.00 | — | Connections |
| **Total** | | | **$18.40** | | |

**Bulk discount:** 5pcq = $15/node. 10pcq = $12/node.

## Assembly Time

- Wiring: 20 min
- Flash firmware: 2 min
- **Total per node: ~25 min**

## Firmware

See [`firmware/objective_box.cpp`](firmware/objective_box.cpp) — PlatformIO project.

## Modes Unlocked

- [Capture the Flag](modes/capture_flag/README.md) — Node = flag; grab and return
- [Domination](modes/domination/README.md) — Node = zone; hold to capture
- [Search & Destroy](modes/search_destroy/README.md) — Node = bomb site; plant/defuse
- [Data Heist](modes/data_heist/README.md) — Node = terminal; hack sequence
