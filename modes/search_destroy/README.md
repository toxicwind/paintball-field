# Search & Destroy

## Overview

Bomb defusal mode. Attackers plant a bomb at one of two sites. Defenders protect sites. The twist: bomb proximity creates a "tension field" on every player's band — the closer you are to the bomb, the more intense the haptic feedback. Defenders can "feel" when attackers are near a site.

## Rules

| Rule | Detail |
|------|--------|
| Teams | Attackers vs Defenders, 4–6 players each |
| Rounds | Best of 7 |
| Bomb Sites | 2 sites (A and B) |
| Plant Time | 5s uninterrupted at site |
| Defuse Time | 7s uninterrupted |
| Win Condition | Attackers: plant + detonate (45s fuse). Defenders: defuse or eliminate all attackers. |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| Near bomb site (<8m) | Distance counter + direction arrow | Slow pulse, increases with proximity | Yellow warning |
| Very near bomb site (<3m) | "PLANT" or "DEFUSE" prompt | Rapid pulse | Red flash |
| Planting bomb | Progress bar | Steady tone | Solid red |
| Defusing bomb | Progress bar | Steady tone | Solid green |
| Bomb planted | Countdown timer visible to all | Tick every 5s | Red pulse |
| Bomb detonated | Full screen flash | Long vibration | White flash |

## Proximity Mechanics

- Bomb emits BLE beacon at -4dBm
- Every band within 15m receives proximity signal
- Haptic intensity = `1 / distance^2` — closer = more urgent
- Defenders get directional arrow pointing to nearest bomb site when within 10m

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Multi-Bomb** | 3 sites, 2 bombs, attackers must plant both | Hard |
| **Fake Bomb** | One site has a decoy; defusing decoy = instant loss for defenders | Medium |
| **Sabotage** | Defenders can "sabotage" a planted bomb (reverse plant bar) to speed up detonation | Hard |
