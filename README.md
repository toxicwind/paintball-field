# SpectreBand — Tiered Paintball Game System

<p align="center">
  <img src="https://img.shields.io/badge/tiers-4%20levels-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/band-%2412%2Fplayer-green?style=flat-square" />
  <img src="https://img.shields.io/badge/field-kit-%2480%2B-lightgrey?style=flat-square" />
  <img src="https://img.shields.io/badge/modes-11%20built--in-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/insurance-compliant-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/license-MIT-black?style=flat-square" />
</p>

**SpectreBand** is a tiered paintball game system. Fields buy what they can afford. Players rent bands. Each tier adds hardware and unlocks new game modes. All modes work with masks ON — no exceptions.

---

## Insurance-First Design

| Constraint | How We Handle It |
|------------|-----------------|
| Masks stay on at all times | OLED is on the **wristband**, visible without touching mask |
| No night games | All modes work in daylight; no "night vision" gimmicks |
| No physical contact rules | BLE proximity hit detection replaces "touch" mechanics |
| Field owner liability | All hardware is low-voltage (3.3V), battery-powered, no mains |
| Player safety | Haptic feedback replaces audio cues that could mask field marshal calls |

---

## Tier System

| Tier | Name | Cost | What You Get | Unlocks Modes |
|------|------|------|-------------|---------------|
| **Tier 0** | Core Band | $12/player | Wristband: radar HUD, team LED, hit haptic | [Spectre](tiers/tier_0_band/modes/spectre/README.md), [Hunter-Prey](tiers/tier_0_band/modes/hunter_prey/README.md), [Ghost](tiers/tier_0_band/modes/ghost/README.md) |
| **Tier 1** | Objective Node | +$15/node (shared) | Physical box on field: buttons, OLED, LEDs, buzzer | [Capture the Flag](tiers/tier_1_objective/modes/capture_flag/README.md), [Domination](tiers/tier_1_objective/modes/domination/README.md), [Search & Destroy](tiers/tier_1_objective/modes/search_destroy/README.md), [Data Heist](tiers/tier_1_objective/modes/data_heist/README.md) |
| **Tier 2** | Hit Detection | +$3/band upgrade | BLE RSSI proximity sensor for accurate hit registration | [Infection](tiers/tier_2_hitdetect/modes/infection/README.md), [VIP Escort](tiers/tier_2_hitdetect/modes/vip_escort/README.md), [Battle Royale](tiers/tier_2_hitdetect/modes/battle_royale/README.md) |
| **Tier 3** | Command Station | +$50/station (shared) | Referee tablet with full field map, replay, scoring | [Overwatch](tiers/tier_3_command/modes/overwatch/README.md), [Tournament](tiers/tier_3_command/modes/tournament/README.md) |

**Field Startup Cost:**
- Minimum: $80 (Pi 5 server + router) + 8x Tier 0 bands ($96) = **$176 for 8 players**
- Full kit: $176 + 3x Tier 1 nodes ($45) + 8x Tier 2 upgrades ($24) + 1x Tier 3 station ($50) = **$295 for full experience**

---

## Architecture

```
                    SPECTRE FIELD
    ┌─────────────────────────────────────────────┐
    │                                             │
    │   ┌──────────┐         WiFi RSSI            │
    │   │  Tier 0  │ ──────────────────>          │
    │   │   Band   │         5 Hz                 │
    │   │ $12/player│                            │
    │   └────┬─────┘                            │
    │        │ BLE proximity                    │
    │        v                                  │
    │   ┌──────────┐      ┌──────────┐          │
    │   │ Tier 2   │      │ Tier 1   │          │
    │   │ Hit Mod  │      │ Objective│          │
    │   │ +$3      │      │ Node     │          │
    │   │ Accurate │      │ $15/box  │          │
    │   │ hits     │      │ Buttons  │          │
    │   └────┬─────┘      │ OLED     │          │
    │        │            │ Buzzer   │          │
    │        │            └────┬─────┘          │
    │        │                 │ MQTT             │
    │        └─────────────────┼────────────────>│
    │                          │                 │
    │   ┌──────────┐           v                 │
    │   │ Tier 3   │      ┌──────────┐          │
    │   │ Command  │<─────│  Server  │          │
    │   │ Station  │  WS   │ (Pi 5)   │          │
    │   │ $50      │       │ $80      │          │
    │   │ Map view │       └──────────┘          │
    │   └──────────┘                             │
    │                                             │
    └─────────────────────────────────────────────┘
```

---

## Quick Start

```bash
# Clone
git clone https://github.com/toxicwind/paintball-field.git
cd paintball-field

# Deploy field server
cd field_server
pip install -r requirements.txt
python server.py --config field_layout.json

# Flash a Tier 0 band
cd ../tiers/tier_0_band/firmware
pio run --target upload --environment esp32c3

# Flash a Tier 1 objective node
cd ../../tier_1_objective/firmware
pio run --target upload --environment esp32c3
```

---

## Game Modes by Tier

### Tier 0 — Core Band Only ($12/player)

| Mode | Mechanic | Duration | Players |
|------|----------|----------|---------|
| [Spectre](tiers/tier_0_band/modes/spectre/README.md) | One player per team sees all enemies permanently | 10 min | 4v4–8v8 |
| [Hunter-Prey](tiers/tier_0_band/modes/hunter_prey/README.md) | All players get 3s wall vision every 60s | 15 min | 5v5–10v10 |
| [Ghost](tiers/tier_0_band/modes/ghost/README.md) | Dead players become invisible spotters for team | 12 min | 6v6 |

### Tier 1 — Band + Objective Node (+$15/node)

| Mode | Mechanic | Duration | Players | Nodes Needed |
|------|----------|----------|---------|-------------|
| [Capture the Flag](tiers/tier_1_objective/modes/capture_flag/README.md) | Box = flag; carrier visible to enemies | 15 min | 5v5–8v8 | 2 |
| [Domination](tiers/tier_1_objective/modes/domination/README.md) | Stand near box to capture zone; reveals enemies in zone | 12 min | 5v5–10v10 | 3–5 |
| [Search & Destroy](tiers/tier_1_objective/modes/search_destroy/README.md) | Plant/defuse box; proximity haptic tension | 10 min | 4v4–6v6 | 2 |
| [Data Heist](tiers/tier_1_objective/modes/data_heist/README.md) | Hack 3 boxes in sequence; hacker position revealed | 15 min | 4v4–6v6 | 3 |

### Tier 2 — Band + Hit Detection (+$3/band)

| Mode | Mechanic | Duration | Players |
|------|----------|----------|---------|
| [Infection](tiers/tier_2_hitdetect/modes/infection/README.md) | BLE proximity infection; survivors see infected | 10 min | 6–16 |
| [VIP Escort](tiers/tier_2_hitdetect/modes/vip_escort/README.md) | Protect VIP across field; enemy sees VIP every 30s | 12 min | 5v5 |
| [Battle Royale](tiers/tier_2_hitdetect/modes/battle_royale/README.md) | Shrinking zone; last standing wins | 15 min | 8–32 |
| [Frontline](tiers/tier_2_hitdetect/modes/frontline/README.md) | Checkpoint respawn; deplete enemy reinforcements | 15 min | 6v6–10v10 |

### Tier 3 — Band + Command Station (+$50/station)

| Mode | Mechanic | Duration | Players |
|------|----------|----------|---------|
| [Overwatch](tiers/tier_3_command/modes/overwatch/README.md) | Commander sees full map; pings team | 15 min | 4v4 |
| [Tournament](tiers/tier_3_command/modes/tournament/README.md) | Referee validation, replay, brackets | Varies | 4v4–8v8 |
| [Tournament](tiers/tier_3_command/modes/tournament/README.md) | Referee validates hits; generates match replay | Varies | 4v4–8v8 |

---

## License

MIT. Build it. Sell it. Run a field.
