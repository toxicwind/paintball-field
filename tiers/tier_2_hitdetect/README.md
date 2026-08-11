# Tier 2 — Hit Detection Module

Upgrade for Tier 0 bands. Adds BLE RSSI proximity sensing for accurate hit registration. No more honor system disputes.

## What It Does

| Feature | How | Game Impact |
|---------|-----|-------------|
| BLE Proximity Hit | Band measures RSSI of shooter’s beacon; <2m for 0.5s = hit | Accurate hit detection without physical sensors |
| Directional Haptic | Hit pattern encodes shooter direction (front/back/left/right) | Player knows where fire came from |
| Hit Validation | Server cross-references position + proximity + timestamp | Prevents cheating; generates replay data |
| Kill Feed | Band briefly shows killer’s team color on hit | Instant feedback |

## BOM — Per Band (Upgrade)

| Component | Part Number | Supplier | Unit Price | Qty | Purpose |
|-----------|-------------|----------|------------|-----|---------|
| BLE Antenna | 2.4GHz PCB antenna (already on ESP32-C3) | — | $0.00 | 1 | Uses existing hardware |
| Firmware | Hit detection algorithm | — | $0.00 | 1 | OTA flash to existing band |
| **Total** | | | **$0.00** | | |

**Wait — this is a firmware-only upgrade.** The ESP32-C3 already has BLE. We just need better RSSI calibration and hit logic in firmware.

**Actual cost:** $0 per band if OTA. $3 per band if reflashing via USB-C at field (labor cost).

## Firmware

See [`firmware/hit_module.cpp`](firmware/hit_module.cpp) — OTA flash to existing Tier 0 bands.

## Modes Unlocked

- [Infection](modes/infection/README.md) — BLE proximity = infection touch
- [VIP Escort](modes/vip_escort/README.md) — Accurate hit detection on VIP
- [Battle Royale](modes/battle_royale/README.md) — Validated eliminations, no disputes
