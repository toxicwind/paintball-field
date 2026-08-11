# SpectreBand — Modular Paintball Game System

<p align="center">
  <img src="https://img.shields.io/badge/hardware-ESP32--C3%20%7C%20OLED%20%7C%20BLE%205.0-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/players-8--64%20per%20field-green?style=flat-square" />
  <img src="https://img.shields.io/badge/latency-%3C150ms-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/band-cost-%7E%2412-lightgrey?style=flat-square" />
  <img src="https://img.shields.io/badge/field-kit-%7E%24150-lightgrey?style=flat-square" />
  <img src="https://img.shields.io/badge/modes-11%20built--in-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/license-MIT-black?style=flat-square" />
</p>

**SpectreBand** is a modular paintball game system. Venues buy a field kit. Players rent or buy a wristband. Each game mode is a different way to use positioning, proximity, and haptic feedback — not just "see through walls."

---

## How It Works

| Layer | What It Does | Tech | Cost |
|-------|-------------|------|------|
| **Band** | Wrist-worn. Radar HUD, haptic hits, team LED, auto-pair. | ESP32-C3 + OLED + BLE | ~$12/player |
| **Field Kit** | 6x WiFi AP anchors + Pi server + router. | ESP32-C3 AP nodes | ~$150/field |
| **Cloud** | Optional. Leaderboards, replays, match analytics. | FastAPI + SQLite | $29/mo/venue |

---

## Game Modes

| Mode | Type | Core Mechanic | Band Behavior | Players | Duration |
|------|------|--------------|---------------|---------|----------|
| [Spectre](modes/spectre/README.md) | Assassination | One player per team has wall-penetrating vision | Spectre sees all enemies; others see only teammates | 4v4–8v8 | 10 min |
| [Hunter-Prey](modes/hunter_prey/README.md) | Pulse Vision | All players get 3s wall vision every 60s | Vibrate 1s before pulse; red dots flash | 5v5–10v10 | 15 min |
| [Ghost](modes/ghost/README.md) | Respawn Intel | Dead players become invisible spotters | Dead band = green dots only; living = full radar | 6v6 | 12 min |
| [Capture the Flag](modes/capture_flag/README.md) | CTF | Positioning reveals flag carrier to enemy team | Flag carrier = pulsing yellow dot; enemies see it | 5v5–8v8 | 15 min |
| [Domination](modes/domination/README.md) | Zone Control | Hold zones to reveal enemies inside captured zones | Captured zone = red dots visible inside boundary | 5v5–10v10 | 12 min |
| [Search & Destroy](modes/search_destroy/README.md) | Bomb Defusal | Bomb site proximity triggers band vibration | Near bomb = rapid pulse; defusing = steady tone | 4v4–6v6 | 10 min |
| [Infection](modes/infection/README.md) | Zombie | Infected players chase survivors; survivors see infected through walls | Survivor = red dots (infected); infected = only survivor dots | 6–16 | 10 min |
| [VIP Escort](modes/vip_escort/README.md) | Escort | VIP has no weapons; team must extract across field | VIP = gold dot; team sees VIP always; enemy sees VIP every 30s | 5v5 | 12 min |
| [Battle Royale](modes/battle_royale/README.md) | Shrinking Zone | Safe zone shrinks; players outside take damage | Outside zone = red border warning + damage tick haptic | 8–32 | 15 min |
| [Data Heist](modes/data_heist/README.md) | Objective Chain | Hack 3 terminals in sequence; positioning reveals hacker | Hacking = pulsing purple dot; team defends | 4v4–6v6 | 15 min |
| [Blindside](modes/blindside/README.md) | Pure Audio | No radar; haptic patterns indicate direction of last hit | OLED off. Haptic only. | 3v3–5v5 | 10 min |
| [Overwatch](modes/overwatch/README.md) | Commander | One player gets drone-view; team follows pings | Overwatch band = zoomed 2D map. Others = standard radar | 4v4 | 15 min |

---

## Band Hardware

| Component | Part | Price | Purpose |
|-----------|------|-------|---------|
| MCU | ESP32-C3-MINI-1 | $2.50 | WiFi scan + BLE beacon |
| Display | SSD1306 0.96" OLED | $1.50 | Radar HUD |
| Haptic | DRV2605 + 10mm motor | $1.00 | Hit alerts, direction cues |
| LEDs | WS2812B x3 | $0.30 | Team color, hit flash, low battery |
| Battery | 502535 500mAh LiPo | $2.50 | 4+ hour runtime |
| Charger | MCP73831 + USB-C | $0.70 | LiPo charging |
| PCB + Case + Strap | 30x40mm FR4 + TPU + NATO | $3.00 | Wrist-worn enclosure |
| Passives | 0402 R/C | $0.50 | Decoupling, pullups |
| **Total** | | **$12.00** | |

[Full band docs →](band/README.md)

---

## Field Kit

| Component | Qty | Unit | Total | Purpose |
|-----------|-----|------|-------|---------|
| AP Node (ESP32-C3-DevKitM) | 6 | $6 | $36 | Anchor points |
| Server (Raspberry Pi 5 4GB) | 1 | $80 | $80 | FastAPI + WebSocket |
| Router (GL.iNet MT300N-V2) | 1 | $25 | $25 | Field WiFi |
| Enclosures (IP65 box) | 6 | $3 | $18 | Weatherproof |
| Power (5V 3A adapters) | 6 | $4 | $24 | AP power |
| **Total** | | | **$183** | |

[Full field docs →](field/README.md)

---

## Quick Start

```bash
# Clone
git clone https://github.com/toxicwind/paintball-field.git
cd paintball-field

# Deploy field server
cd field
pip install -r server/requirements.txt
python server/main.py --config config/field_layout.json --mode capture_flag

# Flash a band
cd ../band/firmware
pio run --target upload --environment esp32c3
```

---

## Architecture

```
Player Band (ESP32-C3)
  ├── WiFi RSSI scan ──> AP Mesh (6x) ──> MQTT ──> Game Server (Pi 5)
  ├── BLE proximity ──> Hit detection (player-to-player)
  ├── LoRaWAN ──> Long-range hit confirmation / game events
  └── OLED + Haptic + LED <── WebSocket <── Server state (5Hz)
```

---

## License

MIT. Build it. Sell it. Run a field.
