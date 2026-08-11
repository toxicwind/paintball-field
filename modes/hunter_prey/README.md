# Hunter-Prey

## Overview

All players get 3 seconds of wall-penetrating vision every 60 seconds. The band vibrates 1 second before the pulse, giving a warning. During the pulse, all enemies are visible as red dots. Between pulses, only teammates are visible. This creates a rhythm of "hunt during pulse, hide between pulses."

## Rules

| Rule | Detail |
|------|--------|
| Teams | 2 teams, 5–10 players each |
| Pulse | Every 60s, all players get 3s wall vision |
| Warning | 1s haptic vibration before pulse |
| Win Condition | Most eliminations in 15 min |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| Normal | Green dots only (teammates) | None | Team color |
| Warning (1s before) | "PULSE INCOMING" | Rapid buzz | Yellow flash |
| Pulse active | Red dots = all enemies | None | White pulse |
| Pulse ending | "3... 2... 1..." countdown | Slow ticks | Dimming white |

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Random Pulse** | Pulse timing is random (40–80s intervals) | Hard |
| **Team Pulse** | Only one team gets pulse at a time; alternates | Medium |
| **Extended Pulse** | 5s pulse but 90s cooldown | Easy |
