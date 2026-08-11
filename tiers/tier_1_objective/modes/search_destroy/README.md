# Search & Destroy

## Overview

Bomb defusal with physical bomb nodes. Attackers plant a bomb at one of two sites. Defenders protect sites. The bomb node creates "tension" — proximity to the bomb triggers haptic feedback on every player's band.

## Rules

| Rule | Detail |
|------|--------|
| Teams | Attackers vs Defenders, 4–6 players each |
| Rounds | Best of 7 |
| Bomb Sites | 2 bomb nodes (A and B) |
| Plant | Hold ACTION on bomb node for 5s uninterrupted |
| Defuse | Hold ACTION on planted bomb for 7s uninterrupted |
| Win Condition | Attackers: plant + detonate (45s fuse). Defenders: defuse or eliminate all attackers. |

## Node Behavior (Bomb Node)

| State | LED Ring | OLED | Buzzer |
|-------|----------|------|--------|
| Idle | White | "BOMB SITE A" | None |
| Planting | Blinking red | "PLANTING..." + bar | Beep every 1s |
| Planted | Red countdown blink | "45... 44... 43..." | Tick every 5s |
| Defusing | Blinking green | "DEFUSING..." + bar | Steady tone |
| Defused | Solid green | "DEFUSED!" | Victory tone |
| Detonated | Solid white | "BOOM" | Long tone |

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

- Bomb node emits BLE beacon at -4dBm
- Every band within 15m receives proximity signal
- Haptic intensity = `1 / distance^2` — closer = more urgent
- Defenders get directional arrow pointing to nearest bomb site when within 10m

## Tier Requirements

- **Tier 0** — Core band ($12/player)
- **Tier 1** — 2x Bomb Nodes ($15 each = $30)
- **Total field cost:** $176 + $30 = **$206**

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Multi-Bomb** | 3 sites, 2 bombs, attackers must plant both | Hard |
| **Fake Bomb** | One site has a decoy; defusing decoy = instant loss for defenders | Medium |
| **Sabotage** | Defenders can "sabotage" a planted bomb (reverse plant bar) to speed up detonation | Hard |
