# VIP Escort

## Overview

One player is the VIP (no weapon, gold dot). Their team must escort them from one side of the field to the extraction point on the other side. The enemy team sees the VIP's position every 30s (pulsing gold dot). The escort team sees the VIP always. This creates a "moving target" dynamic where the VIP must be protected, relayed, and hidden during the 30s windows when enemies have intel.

## Rules

| Rule | Detail |
|------|--------|
| Teams | 2 teams, 5 players each |
| VIP | Randomly assigned, no weapon, moves at normal speed |
| Extraction | Fixed point on opposite side of field |
| VIP Visibility | Enemy sees VIP position every 30s for 5s (pulsing gold dot) |
| VIP Death | Escort team loses round |
| Win Condition | Best of 5 rounds |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| You are VIP | No radar (you have no weapon). Team dots only. | None | Solid gold |
| Escort team | Gold dot = VIP always visible | Warning when VIP takes fire | Team color |
| Enemy team | Gold dot pulses every 30s for 5s | Urgent pulse when VIP spotted | Red when VIP visible |
| VIP down | Screen flash | Long buzz | White flash |
| Extraction reached | "EXTRACTED" + confetti animation | Victory pattern | Rainbow pulse |

## VIP Movement Rules

- VIP can be "carried" by teammate (both stationary for 3s, VIP becomes invisible to enemy radar for 10s)
- VIP can "sprint" (honor system: VIP calls "sprinting" — moves 2x speed but band flashes white, visible to all)

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Double VIP** | Each team has a VIP; first extraction wins | Medium |
| **Decoy VIP** | 3 players marked as VIP; only 1 is real. Enemy must guess. | Hard |
| **Extraction Drop** | Extraction point moves every 60s | Hard |
