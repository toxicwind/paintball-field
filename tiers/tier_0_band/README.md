# Tier 0 — Core Band

The foundation. Every player wears one. $12 to build, $25 to buy, $5 to rent per session.

## What It Does

| Feature | How | Player Experience |
|---------|-----|-------------------|
| Tactical Display | 32x32 OLED shows objectives, scores, timers, team status | Glance at wrist → game state at a glance |
| Team LED | WS2812B glows team color | Instant team ID at a glance |
| Hit Haptic | DRV2605 vibration motor buzzes on hit | Feel hits without looking down |
| Auto-Pair | Scans for SPECTRE-AP-* on boot | Turn on → play. Zero config |
| 4hr Battery | 500mAh LiPo, deep sleep between scans | Full day on one charge |

## BOM — Per Band

| Component | Part Number | Supplier | Unit Price | Qty | Purpose | Alt |
|-----------|-------------|----------|------------|-----|---------|-----|
| MCU | ESP32-C3-MINI-1 | JLCPCB/LCSC | $2.50 | 1 | WiFi scan + BLE beacon | ESP32-C3-WROOM-02 |
| Display | SSD1306 0.96" I2C OLED | LCSC | $1.50 | 1 | Radar HUD | SH1106 1.3" (+$0.80) |
| Haptic | DRV2605L + 10mm ERM motor | LCSC | $1.00 | 1 | Hit alerts | LRA motor (+$0.50) |
| LEDs | WS2812B 5050 RGB | LCSC | $0.10 | 3 | Team color, hit flash | SK6812 drop-in |
| Battery | 502535 500mAh LiPo | AliExpress | $2.50 | 1 | 4hr runtime | 602535 600mAh |
| Charger | MCP73831T + TYPE-C 16P | LCSC | $0.70 | 1 | USB-C charging | TP4056 |
| PCB | 2-layer 30x40mm FR4 | JLCPCB | $1.50 | 1 | Mainboard (5pcq = $0.30/ea) | Hand-wire |
| Case | 3D-printed TPU wristband | Self/Printables | $1.00 | 1 | Impact protection | Silicone sleeve |
| Strap | 20mm NATO watch strap | AliExpress | $1.50 | 1 | Field-tough adjustable | Elastic (-$0.80) |
| Passives | 0402 R/C/pullups | LCSC | $0.50 | — | Decoupling | — |
| **Total** | | | **$12.00** | | | |

## Assembly Time

- SMD soldering: 15 min with hot plate
- Case print: 45 min (TPU, 0.2mm layer)
- Flash firmware: 2 min
- **Total per band: ~1 hour**

## Firmware

See [`firmware/band.cpp`](../../firmware/band.cpp) — PlatformIO project for ESP32-C3.

## Modes Unlocked

- [Spectre](../../modes/spectre/README.md) — Assassination with tactical overview
- [Hunter-Prey](../../modes/hunter_prey/README.md) — Haptic pulse every 60s
- [Ghost](../../modes/ghost/README.md) — Dead players become spotters
