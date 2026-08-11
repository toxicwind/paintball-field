# Tier P: GhostNet (Pilot Tier)

> **"The band is only for enable/object. No HUD. No map. No radar. The ref sees everything. Players talk through walls."**

## Philosophy

SpectreBand v1 (Tiers 0-3) puts a screen on every player's wrist. That's cool for tech demos, but it's expensive, fragile, and turns paintball into a video game.

**GhostNet** is different. It's a stripped-down, LoRaWAN-first system designed for field owners who want:
- **Objective-based gameplay** without $1200 phones on the field
- **Referee oversight** that actually works at 10:1 player ratios
- **Team coordination** through haptic signals, not screens
- **Profitability** with a sub-$200 kit that pays for itself in 3 sessions

## What Players See

| Signal | Meaning |
|--------|---------|
| Green pulse (slow) | You're alive, team is winning |
| Green pulse (fast) | Objective captured / point scored |
| Red flash | You've been hit — call it out |
| Red SOS | You're "wounded" — teammates must extract you |
| Yellow blink | 1 minute remaining |
| Vibration short | Team comms: "move" |
| Vibration long | Team comms: "hold" |
| Vibration pulse | Enemy near objective |

## What the Ref Sees

A single tablet showing:
- Every player's status (alive / eliminated / wounded / disconnected)
- Objective capture progress in real-time
- Game timer with auto-announcements
- Team balance alerts
- Emergency stop button

No player positions on the ref screen either — just status and objectives. The ref monitors fairness, not GPS stalking.

## Hardware BOM

### GhostBand P1 (Player Wristband)

| Component | Part | Cost | Source |
|-----------|------|------|--------|
| MCU | Heltec HT-CT62 (ESP32-C3 + SX1262) | $4.50 | Heltec / AliExpress |
| LEDs | WS2812B x3 (RGB) | $0.30 | LCSC |
| Haptic | ERM motor + simple driver | $1.20 | LCSC |
| RFID | MFRC522 13.56MHz reader | $1.50 | LCSC |
| Battery | 350mAh LiPo | $1.80 | AliExpress |
| Enclosure | TPU 3D printed wrist strap | $0.80 | Self-printed |
| **Total** | | **$10.10** | |

**No OLED. No WiFi scanning. No position calculation.** The band is a LoRa endpoint + RFID reader + LED/vibe output. That's it. Firmware is <100KB.

### GhostNode P1 (Objective Box)

| Component | Part | Cost | Source |
|-----------|------|------|--------|
| MCU | Heltec HT-CT62 | $4.50 | Heltec |
| RFID Tag | MIFARE Classic 1K (passive) | $0.25 | LCSC |
| LED Ring | WS2812B x8 | $0.60 | LCSC |
| Battery | 18650 + holder | $2.50 | AliExpress |
| Enclosure | Pelican-style case | $3.00 | Amazon |
| **Total** | | **$10.85** | |

### GhostHub P1 (Field Gateway)

| Component | Part | Cost | Source |
|-----------|------|------|--------|
| Gateway | Heltec HT-M00 Dual Channel | $35.00 | Heltec |
| Power | USB-C cable + 5V adapter | $5.00 | Any |
| **Total** | | **$40.00** | |

### Full 8-Player Kit

| Item | Qty | Unit | Total |
|------|-----|------|-------|
| GhostBand P1 | 8 | $10.10 | $80.80 |
| GhostNode P1 | 3 | $10.85 | $32.55 |
| GhostHub P1 | 1 | $40.00 | $40.00 |
| USB Charging Hub | 1 | $15.00 | $15.00 |
| **Grand Total** | | | **$168.35** |

At $8/player add-on, this pays for itself in **3 sessions**.

## Architecture

```
GhostBand (player) ----LoRaWAN----> GhostHub ----MQTT----> Field Server ----WebSocket----> Ref Tablet
     |                                    |
  RFID scan                          SQLite log
  (objective)                        (match history)
     |
GhostNode (objective) <----LoRaWAN----
```

- **LoRaWAN Class A**: Uplink-heavy. Bands send heartbeats every 5s, objective scans immediately.
- **915 MHz ISM**: No license required in the US.
- **Range**: 2-5km outdoor, 500m+ through bunkers/trees.
- **Latency**: 1-3s end-to-end. Fine for paintball.
- **Battery**: Bands last 8+ hours active, 1 week standby. Nodes last 1 week on 18650.

## Firmware

See `firmware/ghostband_p1/` for PlatformIO project.

Key design decisions:
- **No FreeRTOS**. Bare-metal Arduino loop. Simpler, lower power.
- **Deep sleep between transmissions**. Wake every 5s, send packet, sleep. 0.5mA average draw.
- **RFID polling at 2Hz**. Only when near an objective (RSSI > threshold).
- **LED patterns in lookup table**. No rendering engine. Just `setPattern(PATTERN_HIT)`.

## Game Modes

See `modes/` for full mode specifications. Pilot Tier supports 4 modes:

1. **Blackhawk Down** — Defend/capture the crashed helicopter (Blitz exclusive)
2. **Dead Drop** — Sequential RFID objective hunt with warm/cold hints
3. **King of the Hill** — Hold the central node for 60s cumulative
4. **Search & Rescue** — Extract wounded teammates to extraction point

## Comparison to SpectreBand Tiers 0-3

| Feature | Tier 0-3 (SpectreBand) | Tier P (GhostNet) |
|---------|----------------------|-------------------|
| Display | OLED radar screen | 3x RGB LED |
| Positioning | WiFi RSSI trilateration | None (not needed) |
| Range | 50-100m (WiFi) | 2-5km (LoRa) |
| Battery | 4 hours | 8+ hours |
| Player cost | $12/band | $10.10/band |
| Field kit cost | $295 (8 players) | $168 (8 players) |
| Ref oversight | Tournament tablet only | Built-in ref tablet |
| Phone required | No | No |
| Internet required | No | No |
| Player map | Yes | **No** |
| Player positions shown | Yes | **No** |
| Team comms | Screen icons | Haptic patterns |

## Why This Works

**The $1200 phone problem**: Refs don't want to pull out their personal phones on a paintball field. Mud, paint, drops, theft. GhostNet uses a dedicated rugged tablet that lives in a Pelican case.

**The 10:1 monitoring problem**: One ref cannot watch 20 players. GhostNet gives the ref a dashboard. They see eliminations, objective captures, and injuries in real-time. They can focus on safety and fairness instead of guessing.

**The pricing problem**: $200 extra for 8 players kills the deal. $64 extra ($8/person) is a no-brainer upsell. It's less than upgrading from Starter to Intermediate.

## Roadmap

- **Week 1-2**: Build 2 GhostBands + 1 GhostNode + 1 GhostHub. Test LoRa range on Blitz Hyperball field.
- **Week 3-4**: Build full 8-player kit. Test all 4 game modes with volunteer players.
- **Week 5**: Refine haptic patterns based on player feedback. Lock firmware.
- **Week 6**: Document, photograph, publish. Open source the BOM.

## License

MIT. Same as SpectreBand. Build it, break it, mod it, sell it.
