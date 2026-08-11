<!--
  SPECTREBAND — Modular Paintball Game System
  ESP32-C3 · BLE Mesh · FastAPI · WebSocket · SQLite
-->

<h1 align="center">SpectreBand</h1>
<p align="center">
  <b>Real-time positioning · Wall-penetrating HUD · 13 game modes · $12/player</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/tiers-4%20levels-6366f1?style=for-the-badge">
  <img src="https://img.shields.io/badge/modes-13%20built--in-8b5cf6?style=for-the-badge">
  <img src="https://img.shields.io/badge/band-%2412%2Fplayer-10b981?style=for-the-badge">
  <img src="https://img.shields.io/badge/field_kit-%24150-f59e0b?style=for-the-badge">
  <img src="https://img.shields.io/badge/latency-%3C150ms-ef4444?style=for-the-badge">
</p>

---

## Architecture

```mermaid
flowchart TB
    subgraph FIELD["FIELD LAYER"]
        AP1["AP-01 ESP32-C3 Anchor"]
        AP2["AP-02 Anchor"]
        AP3["AP-03 Anchor"]
        AP4["AP-04 Anchor"]
        AP5["AP-05 Anchor"]
        AP6["AP-06 Anchor"]
        NODE["Objective Node<br/>Buttons OLED LED Ring"]
    end

    subgraph PLAYER["PLAYER LAYER"]
        BAND["SpectreBand<br/>ESP32-C3 OLED Haptic LED"]
        BLE["BLE Beacon<br/>Hit Detection"]
        WIFI["WiFi Scan<br/>RSSI Batch 5Hz"]
    end

    subgraph SERVER["SERVER LAYER"]
        FASTAPI["FastAPI<br/>WebSocket Hub"]
        FUSION["Position Fusion<br/>Trilateration"]
        SQLITE["SQLite<br/>Match Replay DB"]
        MQTT["MQTT Broker<br/>Node State Sync"]
    end

    subgraph COMMAND["COMMAND LAYER"]
        TABLET["Command Station<br/>7 inch Touch Pi 5"]
        REFEREE["Referee View<br/>Live Map Replay"]
        BRACKET["Auto Brackets<br/>Tournament Gen"]
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

## Game State Machine

```mermaid
stateDiagram-v2
    [*] --> LOBBY: Power On
    LOBBY --> SCANNING: Auto-Pair Field
    SCANNING --> CONNECTED: Found SPECTRE-AP
    CONNECTED --> REGISTERED: Send Band ID
    REGISTERED --> ALIVE: Match Start
    
    ALIVE --> HIT: BLE Proximity under -55dBm
    HIT --> MARKED: Player Presses ACTION
    HIT --> ALIVE: False Alarm 3s timeout
    
    MARKED --> RESPAWNING: At Checkpoint
    MARKED --> [*]: Reinforcements Depleted
    
    RESPAWNING --> ALIVE: 3s Countdown
    
    ALIVE --> ELIMINATED: Health equals 0
    ELIMINATED --> GHOST: Ghost Mode
    GHOST --> ALIVE: Revive if enabled
    
    ALIVE --> SPECTRE: Random Assignment
    SPECTRE --> ALIVE: Spectre Death
    
    ALIVE --> PULSE: Hunter-Prey Pulse
    PULSE --> ALIVE: 3s Expired
    
    ALIVE --> CARRYING_FLAG: Grab Flag
    CARRYING_FLAG --> SCORED: At Base
    CARRYING_FLAG --> DROPPED: Hit
    DROPPED --> ALIVE: Pickup
    
    ALIVE --> HACKING: At Terminal
    HACKING --> HACKED: 15s Complete
    HACKING --> ALIVE: Interrupted
    
    ALIVE --> PLANTING: At Bomb Site
    PLANTING --> PLANTED: 5s Complete
    PLANTED --> DEFUSING: Defender Action
    DEFUSING --> DEFUSED: 7s Complete
    PLANTED --> DETONATED: 45s Fuse
```

---

## Tier System

```mermaid
flowchart LR
    subgraph T0["Tier 0 - $12 per band"]
        S[Spectre]
        HP[Hunter-Prey]
        G[Ghost]
    end
    
    subgraph T1["Tier 1 - +$15 per node"]
        CF[Capture the Flag]
        DOM[Domination]
        SD[Search and Destroy]
        DH[Data Heist]
    end
    
    subgraph T2["Tier 2 - OTA Upgrade"]
        INF[Infection]
        VIP[VIP Escort]
        BR[Battle Royale]
        FL[Frontline]
    end
    
    subgraph T3["Tier 3 - +$50 per station"]
        OW[Overwatch]
        TOUR[Tournament]
    end
    
    T0 --> T1
    T0 --> T2
    T1 --> T3
    T2 --> T3
```

---

## Data Flow

```mermaid
sequenceDiagram
    participant B as SpectreBand
    participant AP as AP Mesh
    participant S as Game Server
    participant N as Objective Node
    participant C as Command Station

    Note over B,AP: Positioning Loop 5Hz
    B->>AP: WiFi Scan 8 APs RSSI
    AP-->>B: ACK
    AP->>S: MQTT rssi_batch
    S->>S: Trilateration
    S->>B: WS position visible mode
    B->>B: Render Radar HUD

    Note over B,N: Objective Interaction
    B->>N: BLE Proximity under 3m
    N->>N: Button Press Detected
    N->>S: MQTT node_id event progress
    S->>S: Validate Update State
    S->>N: MQTT state owner color
    N->>N: Update LED Ring OLED
    S->>B: WS mode_update visible

    Note over B,S: Hit Detection
    B->>B: BLE Scan nearby bands
    B->>S: WS hit target rssi timestamp
    S->>S: Cross-Reference Position
    S->>B: WS hit_confirmed direction
    B->>B: Haptic Pattern LED Flash

    Note over S,C: Referee View
    S->>C: WS full_state 10Hz
    C->>C: Render Live Map
    C->>S: HTTP Dispute Query
    S->>S: SQLite Replay last 10s
    S-->>C: JSON replay_data
    C->>C: Show Both Perspectives
```

---

## Mode Dependency

```mermaid
flowchart LR
    T0[Tier 0 Core Band] --> T1[Tier 1 Objective Nodes]
    T0 --> T2[Tier 2 Hit Detection]
    T1 --> T3[Tier 3 Command Station]
    T2 --> T3
```

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/toxicwind/paintball-field.git
cd paintball-field

# 2. Deploy field server
cd field_server
pip install -r requirements.txt
python server.py --config field_layout.json --mode frontline

# 3. Flash Tier 0 band
cd ../tiers/tier_0_band/firmware
pio run --target upload --environment esp32c3

# 4. Flash Tier 1 objective node
cd ../../tier_1_objective/firmware
pio run --target upload --environment esp32c3
```

---

## Game Modes

| Tier | Cost | Modes |
|------|------|-------|
| **Tier 0** | $12/band | [Spectre](tiers/tier_0_band/modes/spectre/README.md) · [Hunter-Prey](tiers/tier_0_band/modes/hunter_prey/README.md) · [Ghost](tiers/tier_0_band/modes/ghost/README.md) |
| **Tier 1** | +$15/node | [Capture the Flag](tiers/tier_1_objective/modes/capture_flag/README.md) · [Domination](tiers/tier_1_objective/modes/domination/README.md) · [Search & Destroy](tiers/tier_1_objective/modes/search_destroy/README.md) · [Data Heist](tiers/tier_1_objective/modes/data_heist/README.md) |
| **Tier 2** | +$0 (OTA) | [Infection](tiers/tier_2_hitdetect/modes/infection/README.md) · [VIP Escort](tiers/tier_2_hitdetect/modes/vip_escort/README.md) · [Battle Royale](tiers/tier_2_hitdetect/modes/battle_royale/README.md) · [Frontline](tiers/tier_2_hitdetect/modes/frontline/README.md) |
| **Tier 3** | +$50/station | [Overwatch](tiers/tier_3_command/modes/overwatch/README.md) · [Tournament](tiers/tier_3_command/modes/tournament/README.md) |

---

## Hardware BOM

### SpectreBand (Tier 0) — $12/player

| Component | Part | Price | Purpose |
|-----------|------|-------|---------|
| MCU | ESP32-C3-MINI-1 | $2.50 | WiFi + BLE |
| Display | SSD1306 0.96 inch OLED | $1.50 | Radar HUD |
| Haptic | DRV2605L + ERM | $1.00 | Hit alerts |
| LEDs | WS2812B x3 | $0.30 | Team color |
| Battery | 502535 500mAh LiPo | $2.50 | 4hr runtime |
| Charger | MCP73831 + USB-C | $0.70 | Charging |
| PCB/Case/Strap | 30x40mm + TPU + NATO | $2.50 | Wrist-worn |
| Passives | 0402 R/C | $0.50 | Decoupling |
| **Total** | | **$12.00** | |

### Field Kit — $150

| Component | Qty | Unit | Total |
|-----------|-----|------|-------|
| AP Node (ESP32-C3) | 6 | $6 | $36 |
| Server (Raspberry Pi 5) | 1 | $80 | $80 |
| Router (GL.iNet) | 1 | $25 | $25 |
| Enclosures + Power | 6 | $7 | $42 |
| **Total** | | | **$183** |

---

## License

MIT. Build it. Sell it. Run a field.
