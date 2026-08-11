# Tier 3 — Command Station

Referee/commander tablet with full field map, replay, and tournament validation. One per field.

## What It Does

| Feature | How | Game Impact |
|---------|-----|-------------|
| Full Field Map | 7" touchscreen shows all objective states and team status in real-time | Referee sees everything; resolves disputes instantly |
| Hit Validation | Cross-references BLE proximity + position + timestamp | Tournament-grade anti-cheat |
| Replay System | SQLite records every position, hit, and event | Post-match review; highlight reels |
| Live Scoring | Auto-scores based on mode rules | No manual scorekeeping |
| Ping System | Commander taps map → sends directional ping to team bands | Overwatch mode: real-time command |

## BOM — Per Station

| Component | Part Number | Supplier | Unit Price | Qty | Purpose |
|-----------|-------------|----------|------------|-----|---------|
| Tablet | Raspberry Pi 5 + 7" DSI touchscreen | PiShop | $120.00 | 1 | Display + compute |
| Case | 3D-printed field marshal case | Self | $5.00 | 1 | Weatherproof housing |
| Battery | 10000mAh USB power bank | Amazon | $15.00 | 1 | Portable power |
| Mount | Tripod + tablet clamp | Amazon | $10.00 | 1 | Field placement |
| **Total** | | | **$150.00** | | |

**Cheaper option:** Use existing venue tablet/phone + web dashboard = $0 hardware.

## Software

See [`firmware/command_station.py`](../../firmware/command_station.py) — PyQt5 + WebSocket client.

## Modes Unlocked

- [Overwatch](../../modes/overwatch/README.md) — Commander sees full map, pings team
- [Tournament](../../modes/tournament/README.md) — Full validation, replay, leaderboards
