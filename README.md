<p align="center">
</p>

<h1 align="center">SpectreBand</h1>

<p align="center">
  <b>Smart wearables for paintball fields.</b><br>
  Objective tracking. Team coordination. Referee oversight.<br>
  <i>No phones. No screens for players. Just better games.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/toxicwind/paintball-field?style=flat-square&color=f59e0b">
  <img src="https://img.shields.io/github/forks/toxicwind/paintball-field?style=flat-square&color=6366f1">
  <img src="https://img.shields.io/badge/version-0.90-blue?style=flat-square">
  <img src="https://img.shields.io/badge/modes-15-purple?style=flat-square">
  <img src="https://img.shields.io/badge/license-MIT-black?style=flat-square">
</p>

---

## Two Ways to Play

SpectreBand is one platform with two hardware tiers. Start with GhostNet. Upgrade to SpectreBand when your players demand screens.

### GhostNet (Tier P) — Start Here

> **"The band is only for enable/object. No HUD. No map. No radar. The ref sees everything. Players talk through walls."**

| What You Get | Cost | What You Charge |
|-------------|------|----------------|
| 8 player bands (LED + haptic + RFID, no screen) | ~$80 | $8/player add-on |
| 3 objective nodes (RFID + LoRa) | ~$33 | New game modes = repeat customers |
| 1 field gateway (LoRaWAN) | ~$40 | One-time install |
| 1 ref tablet (use any old Android device) | $0 | Ref empowerment = fewer disputes |

**Total startup: ~$168. First profitable session: session 3.**

**Why GhostNet exists:** One referee cannot monitor 20 players. GhostNet gives the ref a live dashboard — who is alive, who captured what objective, how much time remains. Players get haptic team signals and RFID objective interaction. No one pulls out a $1200 phone on a paintball field.

**Target price:** $8 per player add-on to your existing group rate. For Blitz Paintball's $39.95 group rate, that is $47.95 total — still under the $50 psychological barrier, and cheaper than upgrading to Intermediate ($52.95).

[See full GhostNet documentation](tiers/tier_p_ghostnet/README.md)

### SpectreBand (Tiers 0-3) — Upgrade Later

> **"A wrist-worn tactical display. See objective status, team health, and game timer. Capture flags. Hack terminals. Like a squad leader's HUD, but real."**

| What You Get | Cost | What You Charge |
|-------------|------|----------------|
| 8 player bands (OLED screen + WiFi anchors) | ~$100 | $8/player rental |
| 6 WiFi anchor points | ~$36 | Field coverage |
| 1 server (Raspberry Pi 5) | ~$80 | Match logging + replay |

**Total startup: ~$295. First profitable session: session 3.**

**Why SpectreBand exists:** For fields that want the full video-game experience — objective status on your wrist, team health bars, ghost mode when eliminated, tournament replay systems. The screen shows what the ref sees: objectives, scores, timers. Not enemy positions. Players can buy their own band for $25 and use it at any Spectre-enabled field.

[See Tiers 0-3 documentation](tiers/)

---

## What Problem Does This Solve?

### For Field Owners

| Pain Point | GhostNet Fix | SpectreBand Fix |
|-----------|-------------|----------------|
| 10 players per 1 ref = impossible to monitor | Ref tablet shows live status of all players and objectives | Ref tablet + band vibration auto-validates hit acknowledgment |
| Players argue about who got hit | RFID scan = undeniable proof of objective capture | Band vibrates on hit, ref can force-eliminate from tablet |
| Same elimination games every weekend | 4 objective-based modes (Blackhawk Down, Dead Drop, King of the Hill, Search & Rescue) | 13 modes from simple radar to battle royale |
| Tech is too expensive to try | $168 kit, $8/player add-on | $295 kit, $8/player rental |
| Refs won't use their personal phones | Dedicated rugged tablet in Pelican case | Dedicated rugged tablet in Pelican case |
| Property damage liability from phones on field | No phones. Bands are IP54, bolt-down nodes, no glass screens. | No phones. Bands are IP54, bolt-down nodes. |

### For Players

| Instead of... | GhostNet Gives... | SpectreBand Gives... |
|--------------|-------------------|---------------------|
| Walking into ambushes | Haptic "enemy near objective" pulse | Haptic + screen alert when objective is contested |
| Sitting out when eliminated | Become a "ghost" who spots for your team (haptic relay) | Become a "ghost" with full objective view on screen |
| Same old elimination games | Capture the Blackhawk, find dead drops, hold the hill | Capture flags, hack terminals, protect VIPs, battle royale |
| Arguing about who got hit | Ref validates from tablet, no debate | Band vibrates — no debates |

---

## How It Works

### GhostNet (Simple Version)

```
Player Band (LED + haptic + RFID) ----LoRaWAN----> Field Gateway ----> Ref Tablet
     |                                                    |
  Scans objective                                    Shows live status
  (RFID tag)                                         of all players
     |
Objective Node (RFID tag + LoRa beacon)
```

1. **Player scans objective** — Band reads RFID tag, transmits via LoRaWAN
2. **Gateway receives** — Forwards to field server over Ethernet/WiFi
3. **Ref tablet updates** — "Player 7 captured Alpha. Team score: 2-1."
4. **Band signals team** — Green flash = we scored. Red flash = enemy scored.

That's it. No GPS. No phones. No internet. Just a closed LoRaWAN network on your field. Range: 2-5km outdoor, 500m+ through obstacles.

### SpectreBand (Simple Version)

```
Player Band (OLED screen) --WiFi--> AP Mesh (6x) --MQTT--> Game Server (Pi 5)
```

1. **Bands connect to field WiFi** — 6 small boxes around the field form a mesh
2. **Server tracks objective state** — "Alpha captured by Team Bravo. 2 minutes remaining."
3. **Server decides what you see** — "Your team holds 2 of 3 objectives. Enemy captured Charlie."
4. **Band shows tactical display** — Objective status, team health, timer, game events

---

## Game Modes

### GhostNet Modes (No Screens, LoRaWAN Only)

| Mode | What Happens | Why It's Fun | Field Requirement |
|------|-------------|-------------|-----------------|
| **Blackhawk Down** | Defend/capture 3 RFID tags inside a crashed helicopter | Exclusive to Blitz — only field in Colorado with a Blackhawk | Blitz Military Base |
| **Dead Drop** | Find 3 hidden objective nodes in sequence. Band gives warm/cold LED hints | Forces communication, no camping | Any field |
| **King of the Hill** | Hold central node for 60 seconds cumulative | Fast-paced, forces confrontation | Any field |
| **Search & Rescue** | Extract wounded teammates to extraction point | Team coordination test | Any field |

### SpectreBand Modes (OLED Screen, WiFi Positioning)

#### Start Here (No Extra Hardware)

| Mode | What Happens | Why It's Fun |
|------|-------------|-------------|
| **Hunter-Prey** | Every 60 seconds, everyone gets a haptic pulse — enemy direction unknown | Heart-pounding "pulse" moments |
| **Ghost** | When you die, you become invisible and relay objective intel to your team | No sitting out, ever |
| **Spectre** | One player per team gets full objective overview on screen | Protect your VIP, hunt theirs |

#### Add Objective Boxes (+$15 each)

| Mode | What Happens | Why It's Fun |
|------|-------------|-------------|
| **Capture the Flag** | Grab the enemy flag box, run it back | Carrier is visible to everyone — chaos ensues |
| **Domination** | Stand near a box for 10 seconds to capture it | Zone control + intel warfare |
| **Data Heist** | Hack 3 terminals in order while enemies hunt you | Stealth, risk, reward |
| **Search & Destroy** | Plant a bomb, enemies try to defuse it | Tension builds as timer counts down |

#### Upgrade Firmware (Free)

| Mode | What Happens | Why It's Fun |
|------|-------------|-------------|
| **Frontline** | Checkpoint respawns, deplete enemy reinforcements | Never truly out, always fighting |
| **Battle Royale** | Safe zone shrinks, last team standing | 32 players, massive chaos |
| **Infection** | One infected player chases survivors | Paranoia + swarm tactics |
| **VIP Escort** | Protect a defenseless player across the field | Coordination test |

#### Tournament Kit (+$50)

| Mode | What Happens | Why It's Fun |
|------|-------------|-------------|
| **Overwatch** | One player commands with full map view | Real-time strategy in paintball |
| **Tournament** | Referee tablet validates hits, generates replays | Competitive integrity |

---

## What You Need

### GhostNet Minimum Setup (~$168, 8 players)

| Item | What It Is | Cost |
|------|-----------|------|
| 8 wristbands | Heltec HT-CT62 + LED + haptic + RFID + battery | ~$80 |
| 3 objective nodes | Heltec HT-CT62 + RFID tag + LED ring + 18650 | ~$33 |
| 1 gateway | Heltec HT-M00 Dual Channel LoRa Gateway | ~$40 |
| 1 charging hub | 10-port USB hub | ~$15 |

**Total: ~$168** (with enclosures and power)

### SpectreBand Minimum Setup (~$241, 8 players)

| Item | What It Is | Cost |
|------|-----------|------|
| 8 wristbands | ESP32-C3 + OLED + motor + LEDs + battery | ~$100 |
| 6 WiFi anchors | Small boxes that help triangulate position | ~$36 |
| 1 server | Raspberry Pi 5 (or any old computer) | ~$80 |
| 1 router | Portable WiFi box | ~$25 |

**Total: ~$241** (with enclosures and power)

### SpectreBand Full Setup (~$295, 8 players + objectives)

Add 3 objective boxes ($45) and a charging rack ($52). Now you can run 6 game modes instead of 3.

### Player-Owned Band (~$25)

Players who fall in love with it can buy their own. It works at any field running SpectreBand or GhostNet.

---

## Competitive Pricing Intelligence

We scraped pricing from every major paintball field in Colorado. The data is in `data/colorado_pricing_2026.parquet`.

| Field | Location | Type | Fields | Group Rate (10+, entry+rental+500) |
|-------|----------|------|--------|-----------------------------------|
| **Blitz Paintball** | Dacono, CO | Outdoor | 4 | **$39.85** — our pilot field, has Blackhawk helicopter |
| **Dynamic Paintball** | Aurora, CO | Outdoor | 3 | $40.00 (3 Star, 3hr) — closest competitor on price |
| **American Paintball Coliseum** | Denver/Aurora, CO | Indoor+Outdoor | 3 | $30.00 (group pass+rental, NO paint included) — very small facility |

**Key insight:** Blitz's $39.95 group rate is the anchor. GhostNet at $8 add-on = $47.95 total. That is still cheaper than Blitz's own Intermediate package ($52.95) and cheaper than Dynamic's equivalent. The upsell is invisible — players think they are getting a premium experience for less than the next package tier.

See `data/colorado_pricing_2026.parquet` for full pricing breakdown across all 32 packages.

---

## Case Study: Blitz Paintball

We are piloting both GhostNet and SpectreBand at **Blitz Paintball** in Dacono, Colorado. Four fields, four test environments, one real-world proving ground.

| Field | Size | Best For Testing |
|-------|------|-----------------|
| Urban Combat | 60x40m, 200+ bunkers | SpectreBand screen readability test, dense field |
| Military Base | 50x50m, helicopter + silos | **Blackhawk Down mode**, metal interference, LoRa range test |
| Hyperball | 55x50m, 68 bunkers | Best accuracy, fast games (SpectreBand) |
| Hyper-Spool | 30x25m, small groups | Pilot testing, beginner friendly (GhostNet) |

**GhostNet pilot plan**: 8 bands → 3 objective nodes → 1 gateway → ref tablet. 3 weeks.

**SpectreBand pilot plan**: 8 bands → 6 WiFi anchors → Pi 5 server → charging rack. 5 weeks.

See `fields/blitz_dacono/` for full field configuration.

---

## Quick Start

### GhostNet

```bash
# 1. Download this repo
git clone https://github.com/toxicwind/paintball-field.git
cd paintball-field

# 2. Build the gateway firmware
cd firmware/ghosthub_p1
pio run --target upload

# 3. Flash player bands (plug in USB, run this for each)
cd ../ghostband_p1
pio run --target upload

# 4. Place objective nodes, power on gateway
# 5. Start the server
cd ../../server/ghostnet
pip install -r requirements.txt
python src/main.py

# 6. Open ref tablet at http://<server-ip>:8000/ref
# 7. Turn on bands near the field. They auto-join. Play.
```

### SpectreBand

```bash
# 1. Download this repo
git clone https://github.com/toxicwind/paintball-field.git
cd paintball-field

# 2. Start the server (on any computer)
cd server/spectreband
pip install -r requirements.txt
python src/main.py

# 3. Flash a band (plug in USB, run this)
cd ../../firmware/band
pio run --target upload

# 4. Turn on the band near the server
#    It auto-connects. The screen lights up. Play.
```

---

## Technical Details

<details>
<summary><b>Click to expand: For engineers and makers</b></summary>

### Dual Architecture

```
GhostNet (Tier P)                          SpectreBand (Tiers 0-3)
=================                          =======================
Player Band (HT-CT62) ----LoRaWAN---->     Player Band (ESP32-C3) --WiFi RSSI--> AP Mesh
  ├── RFID reader (MFRC522)                  ├── BLE proximity --> Hit detection
  ├── 3x RGB LED (WS2812B)                 ├── LoRaWAN --> Long-range events
  └── ERM haptic motor                     └── OLED + Haptic + LED <-- WebSocket
       |                                          |
       v                                          v
GhostHub (HT-M00) ----MQTT---->            Game Server (Pi 5) ----WebSocket----> Ref Tablet
       |                                          |
  SQLite log                                SQLite + WAL (match logging + replay)
```

### GhostNet Positioning

- **No positioning for players.** GhostNet does not track where players are. It only tracks:
  - Which objectives have been scanned (RFID)
  - Which players are alive/eliminated (button press + ref override)
  - Team scores and game timer
- **Objective nodes** broadcast LoRa beacons for warm/cold hints in Dead Drop mode.
- **Range**: 2-5km outdoor, 500m+ through bunkers/trees.

### SpectreBand Tactical Display

- **WiFi mesh connectivity** from 6 anchor points around the field
- **Objective state rendering** on 0.96" OLED — captures, timers, team status
- **Haptic + LED patterns** synchronized with game events
- **No player positioning.** The screen shows what the ref sees: objectives, scores, timers. Not enemy locations.

### GhostNet Hardware BOM (P1)

| Component | Part | Cost | Source |
|-----------|------|------|--------|
| MCU | Heltec HT-CT62 (ESP32-C3 + SX1262) | $4.50 | Heltec |
| LEDs | WS2812B x3 | $0.30 | LCSC |
| Haptic | ERM motor + driver | $1.20 | LCSC |
| RFID | MFRC522 13.56MHz | $1.50 | LCSC |
| Battery | 350mAh LiPo | $1.80 | AliExpress |
| Enclosure | TPU 3D printed | $0.80 | Self-printed |
| **Total** | | **$10.10** | |

### SpectreBand Hardware BOM (v1.0)

| Component | Part | Cost | Source |
|-----------|------|------|--------|
| MCU | ESP32-C3-MINI-1 (LCSC C2935306) | $2.92 | LCSC |
| Display | SSD1306 0.96" OLED (LCSC C2890361) | $1.48 | LCSC |
| Haptic | DRV2605L + 10mm ERM (LCSC C527464) | $1.85 | LCSC |
| LEDs | WS2812B x3 (LCSC C114581) | $0.24 | LCSC |
| Battery | 500mAh LiPo | $2.50 | AliExpress |
| Charger | MCP73831T (LCSC C424093) | $0.55 | LCSC |
| **Total** | | **~$12** | |

### Firmware

**GhostNet P1:**
- **Bare-metal Arduino** on ESP32-C3 (no FreeRTOS)
- **Deep sleep** between transmissions (0.5mA average draw)
- **RFID polling at 2Hz** when near objective (RSSI threshold)
- **LED patterns in lookup table** — no rendering engine

**SpectreBand v1.0:**
- **FreeRTOS** on ESP32-C3 dual-core
- **Core 0**: WiFi scan (5Hz), median filter, outlier rejection
- **Core 1**: WebSocket client, OLED render, BLE scan
- **Self-test on boot**: OLED, haptic, LED, battery, AP count

### Server

- **FastAPI** + WebSocket for real-time communication
- **SQLite + WAL** for match logging and replay
- **Simulation mode**: Test without hardware
- **Force eliminate/revive API** for referees

See `REFERENCES.md` for academic citations, datasheets, and vendor links.

</details>

---

## FAQ

**Q: Do players take off their masks to look at the band?**  
A: GhostNet has no screen — just LEDs on the wrist. Glance down, mask stays on. SpectreBand's screen is on your wrist. Same glance.

**Q: Does it work in rain?**  
A: Both bands are splash-resistant (IP54). Don't submerge them. GhostNet nodes are in Pelican-style cases. SpectreBand anchor boxes are weatherproof.

**Q: What if someone cheats and doesn't mark their hit?**  
A: GhostNet: Ref sees all player status on tablet and can force-eliminate. SpectreBand: Band vibrates when hit. Ref can force-eliminate from tablet. Tournament mode auto-validates hits.

**Q: Can I use this for airsoft or laser tag?**  
A: Yes. Both systems don't care what you're shooting. For laser tag, wire the hit detection to the laser receiver.

**Q: How long does the battery last?**  
A: GhostNet: 8+ hours active, 1 week standby. SpectreBand: 4+ hours active. Both use charging racks that refill overnight.

**Q: Is this legal at my field?**  
A: GhostNet uses 915 MHz ISM band (no license needed in the US). SpectreBand uses 2.4GHz WiFi — same as your phone. Check with your field's insurance provider.

**Q: Can I start with GhostNet and upgrade to SpectreBand later?**  
A: Yes. GhostNet bands use the same Heltec HT-CT62 MCU as SpectreBand nodes. The hardware is forward-compatible. You can flash SpectreBand firmware onto GhostNet bands later — the only difference is adding an OLED screen for objective status display.

---

## Contributing

- **Fork it** — add game modes, improve accuracy, design better cases
- **Test it** — run it at your field, report what breaks
- **Sell it** — MIT license means you can build and sell bands commercially

See `AGENTS.md` for internal development notes and `REFERENCES.md` for academic background.

---

## Contact

<p align="center">
  <a href="mailto:denverchrisortega@gmail.com">
    <img src="https://img.shields.io/badge/email-denverchrisortega@gmail.com-10b981?style=for-the-badge&logo=gmail">
  </a>
  <a href="https://github.com/toxicwind">
    <img src="https://img.shields.io/badge/github-@toxicwind-6366f1?style=for-the-badge&logo=github">
  </a>
  <a href="https://resume.effusionlabs.com">
    <img src="https://img.shields.io/badge/portfolio-resume.effusionlabs.com-f59e0b?style=for-the-badge">
  </a>
</p>

**Business inquiries**: Field licensing, bulk orders (50+ bands), white-label solutions  
**Bug reports**: [GitHub Issues](https://github.com/toxicwind/paintball-field/issues)  
**Feature requests**: [GitHub Discussions](https://github.com/toxicwind/paintball-field/discussions)

---

<p align="center">
  <b>Built with intent by Christopher Ortega</b><br>
  <a href="mailto:denverchrisortega@gmail.com">denverchrisortega@gmail.com</a> · 
  <a href="https://github.com/toxicwind">github.com/toxicwind</a><br>
  <sub>MIT licensed. Build it, break it, mod it, sell it.</sub>
</p>
