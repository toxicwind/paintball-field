<!--
  SPECTREBAND - Modular Paintball Game System
  ESP32-C3 - BLE Mesh - FastAPI - WebSocket - SQLite
  Built for Blitz Paintball, Dacono CO
-->

<h1 align="center">SpectreBand</h1>
<p align="center">
  <b>Real-time positioning - Wall-penetrating HUD - 13 game modes - $12/player</b><br>
  <sub>Built for Blitz Paintball, Dacono CO - 5340 Summit Blvd</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/toxicwind/paintball-field?style=for-the-badge&color=f59e0b">
  <img src="https://img.shields.io/github/forks/toxicwind/paintball-field?style=for-the-badge&color=6366f1">
  <img src="https://img.shields.io/github/issues/toxicwind/paintball-field?style=for-the-badge&color=ef4444">
  <img src="https://img.shields.io/github/license/toxicwind/paintball-field?style=for-the-badge&color=10b981">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/tiers-4%20levels-6366f1?style=flat-square">
  <img src="https://img.shields.io/badge/modes-13%20built--in-8b5cf6?style=flat-square">
  <img src="https://img.shields.io/badge/band-%2412%2Fplayer-10b981?style=flat-square">
  <img src="https://img.shields.io/badge/field_kit-%24150-f59e0b?style=flat-square">
  <img src="https://img.shields.io/badge/latency-%3C150ms-ef4444?style=flat-square">
  <img src="https://img.shields.io/badge/battery-4%20hours-3b82f6?style=flat-square">
</p>

---

## Table of Contents

- [What is SpectreBand?](#what-is-spectreband)
- [Blitz Paintball Pilot](#blitz-paintball-pilot)
- [How It Works](#how-it-works)
- [System Architecture](#system-architecture)
- [Hardware](#hardware)
- [Firmware](#firmware)
- [Server](#server)
- [Game Modes](#game-modes)
- [Quick Start](#quick-start)
- [Build Guides](#build-guides)
- [Calibration](#calibration)
- [Staff SOP](#staff-sop)
- [Contributing](#contributing)
- [Contact](#contact)
- [License](#license)

---

## What is SpectreBand?

**SpectreBand** is a complete, open-source paintball positioning system. Players wear a wristband with a radar HUD that shows teammate and enemy positions through walls. Fields deploy WiFi anchor points and optional objective nodes. A central server runs the game logic, handles hit detection, and generates tournament replays.

Built on **ESP32-C3**, **FastAPI**, **WebSocket**, and **BLE mesh**. Designed to be:

- **Affordable**: $12 per player band, $150 for a complete field kit
- **Modular**: Start with 3 game modes, upgrade to 13 as your field grows
- **Insurance-compliant**: No mask removal, all wrist-worn, 3.3V battery-powered
- **Open-source**: MIT licensed - build it, sell it, run a field

---

## Blitz Paintball Pilot

This repo is configured for a pilot deployment at **Blitz Paintball** in Dacono, CO.

### Blitz Field Specs

| Field | Size | Surface | Structures | Best Modes |
|-------|------|---------|-----------|------------|
| Urban Combat | 60x40m | Dirt/grass | 6 large structures, 200+ bunkers | Domination, CTF |
| Military Base | 50x50m | Dirt/grass | 40ft helicopter, 100+ bunkers | Search & Destroy, Data Heist |
| Hyperball | 55x50m | Dirt | 68 bunkers, 14 stand-up per side | Hunter-Prey, Ghost, Frontline |
| Hyper-Spool | 30x25m | Dirt | Giant spools, hyperball bunkers | Hunter-Prey, Ghost (pilot field) |

### Pilot Phases

| Phase | Weeks | Bands | Hardware | Modes | Field |
|-------|-------|-------|----------|-------|-------|
| **1** | 1-2 | 8 | Tier 0 only | Hunter-Prey, Ghost | Hyper-Spool |
| **2** | 3-4 | 8 | +3 objective nodes | Domination, CTF | Urban Combat |
| **3** | 5 | 8 | Full system + charging rack | Frontline, Data Heist | Military Base |

### Pricing for Blitz

- **Rental add-on**: $8 per player per session
- **Band BOM**: $12 (v1.0) / $19.70 (v1.1 with IMU + shock sensor)
- **Payback**: 2 sessions at $8 rental
- **Target margin**: 60% after band cost recovered

See `fields/blitz_dacono/config.json` for full field configuration.

---

## How It Works

1. **Field Setup**: Place 6 ESP32-C3 AP nodes around the field at 2.5m height, facing down
2. **Player Bands**: Each player wears an ESP32-C3 wristband. Every 200ms, it scans for the 6 APs and measures signal strength (RSSI)
3. **Position Calculation**: The band sends RSSI readings to a Raspberry Pi 5 server. The server uses Kalman filter + particle filter fusion to estimate position
4. **Game Logic**: The server runs the active game mode (Hunter-Prey, Domination, etc.)
5. **HUD Update**: The server sends position + visibility data back to each band over WebSocket. The band renders a 32x32 pixel radar on OLED
6. **Hit Detection**: v1.0 uses honor system. v1.1 adds piezo shock sensor for real hit detection
7. **Objective Nodes**: Physical boxes on the field for capture, plant, defuse, hack interactions

Round-trip latency: **under 150 milliseconds**.

---

## System Architecture

```mermaid
flowchart TB
    subgraph FIELD["FIELD LAYER"]
        AP1["AP-01 ESP32-C3 Anchor"]
        AP2["AP-02 Anchor"]
        AP3["AP-03 Anchor"]
        AP4["AP-04 Anchor"]
        AP5["AP-05 Anchor"]
        AP6["AP-06 Anchor"]
        NODE["Objective Node - Buttons OLED LED Ring"]
    end

    subgraph PLAYER["PLAYER LAYER"]
        BAND["SpectreBand - ESP32-C3 OLED Haptic LED"]
        BLE["BLE Beacon - Hit Detection"]
        WIFI["WiFi Scan - RSSI Batch 5Hz"]
    end

    subgraph SERVER["SERVER LAYER"]
        FASTAPI["FastAPI - WebSocket Hub"]
        FUSION["Kalman + Particle Filter Fusion"]
        SQLITE["SQLite - Match Replay DB"]
        MQTT["MQTT Broker - Node State Sync"]
    end

    subgraph COMMAND["COMMAND LAYER"]
        TABLET["Command Station - 7 inch Touch Pi 5"]
        REFEREE["Referee View - Live Map Replay"]
        BRACKET["Auto Brackets - Tournament Gen"]
    end

    WIFI --> AP1 & AP2 & AP3 & AP4 & AP5 & AP6
    AP1 & AP2 & AP3 & AP4 & AP5 & AP6 --> FASTAPI
    BAND --> BLE
    BLE --> FASTAPI
    FASTAPI --> BAND
    FASTAPI --> FUSION
    FUSION --> SQLITE
    NODE --> MQTT
    MQTT --> FASTAPI
    FASTAPI --> TABLET
    TABLET --> SQLITE
    TABLET --> REFEREE
    REFEREE --> BRACKET
```

---

## Hardware

### SpectreBand v1.0 - $12/player (Pilot Ready)

| Component | Part | Price | Purpose |
|-----------|------|-------|---------|
| MCU | ESP32-C3-MINI-1 | $2.50 | WiFi + BLE |
| Display | SSD1306 0.96 inch OLED | $1.50 | Radar HUD |
| Haptic | 10mm ERM motor (PWM direct) | $0.40 | Hit alerts |
| LEDs | WS2812B x3 | $0.30 | Team color |
| Battery | 500mAh LiPo | $2.50 | 4hr runtime |
| Charger | MCP73831 + USB-C | $0.70 | Charging |
| Case | 3D printed TPU | $1.00 | Wrist-worn |
| Strap | 20mm silicone | $1.50 | Paint resistant |
| PCB + passives | 30x40mm FR4 | $2.00 | Mainboard |
| **Total** | | **$12.40** | |

### SpectreBand v1.1 - $19.70/player (Production)

| Upgrade | Added | Purpose |
|---------|-------|---------|
| SH1106 1.3 inch OLED | +$0.80 | Readable in sun |
| BMI270 IMU | +$0.80 | Dead reckoning, kills 50% RSSI jitter |
| Piezo shock sensor | +$0.30 | Real hit detection |
| 2x 300mAh hard pouch + steel shield | +$3.50 | 300fps impact safe |
| Polycarbonate case + TPU gasket | +$1.50 | IP54, paint resistant |
| **Total** | **$19.70** | |

See `hardware/band_v1.0/BOM.csv` and `hardware/band_v1.1/BOM.csv` for full parts lists.

### AP Node - $24/node

| Component | Price | Notes |
|-----------|-------|-------|
| ESP32-C3-DevKitM-1 | $6.00 | AP mode + ESP-NOW backhaul |
| SSD1306 OLED | $1.50 | Status display |
| LED ring + buttons + buzzer | $2.10 | User interaction |
| 18650 battery + holder | $4.00 | All-day runtime |
| IP65 enclosure + mount | $5.00 | Weatherproof, 2.5m pole mount |
| PoE splitter or 12V PSU | $5.00 | Reliable power (USB adapters die) |
| **Total** | **$24.10** | |

### Charging Rack - $52 (16-slot)

| Component | Price | Notes |
|-----------|-------|-------|
| 3D printed frame | $8.00 | PETG, holds 16 bands |
| Pogo pins (16x4) | $2.40 | Gold plated contacts |
| Mean Well LRS-150-5 PSU | $18.00 | 5V 30A, one PSU powers all |
| TP4056 modules (16x) | $12.80 | Per-cell charging control |
| Bicolor LEDs (16x) | $1.60 | Green=full, Red=charging |
| Bus bar + fuses | $3.00 | Fused distribution |
| Fan | $2.00 | Cooling |
| **Total** | **$52.60** | |

---

## Firmware

### Band Firmware (FreeRTOS)

- **Core 0**: WiFi scan task (5Hz), median filter last 5 RSSI per AP, outlier reject >15dBm jump
- **Core 1**: WebSocket client + OLED render + BLE scan
- **Self-test on boot**: OLED, haptic, 3x LED, battery, AP count — staff knows in 2 seconds if band is dead
- **OTA with rollback**: Bad flash recovery, no bricks on Saturday

See `firmware/band/src/main.cpp` for full source.

### AP Node Firmware

- ESP-NOW backhaul for outdoor metal bunker environments
- Channel lock: 1, 6, 11 to avoid overlap with field router
- MQTT client for server sync

See `firmware/ap_node/src/main.cpp`.

---

## Server

### Position Fusion

- **Weighted least squares**: Baseline trilateration from RSSI
- **Kalman filter**: Fuses WLS + IMU dead reckoning for smooth tracking
- **Particle filter**: Fallback for bad RSSI conditions (multipath, metal bunkers)
- **Per-AP calibration**: Each AP learns its own path loss exponent from field data

### Features

- SQLite + WAL for match logging
- Simulation mode: `python server.py --simulate 16 --field blitz_outdoor_50x30`
- Force eliminate / revive API for referees
- RSSI CSV export for every game — build dataset, improve accuracy

See `server/src/main.py`.

---

## Game Modes

### Blitz Pilot Ready (Phase 1-3)

| Mode | Tier | Players | Duration | Hardware |
|------|------|---------|----------|----------|
| [Hunter-Prey](modes/hunter_prey/config.json) | 0 | 4-20 | 15 min | Band only |
| [Ghost](modes/ghost/config.json) | 0 | 6-12 | 12 min | Band only |
| [Domination](modes/domination/config.json) | 1 | 6-20 | 12 min | +3 nodes |
| [Capture the Flag](modes/capture_flag/config.json) | 1 | 6-16 | 15 min | +2 nodes |
| [Frontline](modes/frontline/config.json) | 2 | 8-20 | 15 min | +3 nodes |
| [Data Heist](modes/data_heist/config.json) | 1 | 6-12 | 15 min | +3 nodes |

### Shelved for Later

| Mode | Why Shelved | When Enabled |
|------|-------------|--------------|
| Spectre | Needs >3m accuracy for fair play | After v1.1 calibration |
| Search & Destroy | Needs real hit detection | After shock sensor proven |
| Infection | BLE proximity touch = arguments | After shock sensor proven |
| VIP Escort | Needs 8+ patient players | Birthday party maturity |
| Battle Royale | Needs 30cm accuracy for 32p | After UWB upgrade |
| Overwatch | Needs command station + trained refs | Phase 3 |
| Tournament | Needs proven hit validation | Phase 3 |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/toxicwind/paintball-field.git
cd paintball-field

# 2. Deploy server
cd server
pip install -r requirements.txt
python src/main.py --config configs/blitz_outdoor_50x30.json

# 3. Flash band
cd ../firmware/band
pio run --target upload --environment esp32c3

# 4. Calibrate field
python src/calibrate.py --field blitz_outdoor_50x30 --aps 6 --auto

# 5. Simulate without hardware
python src/main.py --simulate 16 --field blitz_outdoor_50x30
```

---

## Build Guides

- [Band v1.0 Build](hardware/band_v1.0/BUILD_GUIDE.md) - $12, 45 min assembly
- [Band v1.1 Build](hardware/band_v1.1/BUILD_GUIDE.md) - $19.70, IMU + shock sensor
- [AP Node Build](hardware/ap_node/BUILD_GUIDE.md) - $24, weatherproof mount
- [Charging Rack Build](hardware/charging_rack/BUILD_GUIDE.md) - $52, 16-slot

---

## Calibration

```bash
# Interactive calibration (walk field with band)
python server/src/calibrate.py --field blitz_outdoor_50x30 --aps 6 --samples 50

# Auto-calibrate from simulation data
python server/src/calibrate.py --field blitz_outdoor_50x30 --auto
```

Produces `server/configs/blitz_outdoor_50x30.json` with per-AP path loss exponents.

---

## Staff SOP

- [Staff SOP - Full](docs/ops_sop/STAFF_SOP.md) - Daily setup, match flow, troubleshooting
- [Quick Reference Card](docs/ops_sop/QUICK_REF.md) - Pocket card for referees

Print the SOP on 8.5x11, laminate, attach to charging rack.

---

## Contributing

- Fork, branch, PR. MIT license.
- Code style: PEP 8 for Python, Arduino conventions for C++
- Test on real hardware if possible

---

## Contact

- **Hit me up**: denverchrisortega@gmail.com
- **Text me**: 303-667-3831
- **GitHub**: github.com/toxicwind
- **Portfolio**: resume.effusionlabs.com
- **Location**: Westminster, CO

### Wanna Make Money With This?

Field licensing, bulk hardware (50+ bands), white-label, partnership:

- **Email**: denverchrisortega@gmail.com
- **Phone**: 303-667-3831
- **Location**: Westminster, CO - come grab a beer and talk shop

---

## License

MIT. Build it, break it, mod it, sell it. No lawyers, no limits.

<p align="center">
  <b>Built with 💜 by Christopher Ortega</b><br>
  <b>Westminster, CO · 303-667-3831 · denverchrisortega@gmail.com</b><br>
  <sub>SpectreBand is an open-source project. MIT licensed.</sub>
</p>
