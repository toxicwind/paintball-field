# Capture the Flag

## Overview

Classic CTF with a physical flag box. The flag carrier is visible to the enemy team as a pulsing yellow dot. Grab the enemy flag box, hold ACTION button for 2s to "pick up," then return to your base box to score.

## Rules

| Rule | Detail |
|------|--------|
| Teams | 2 teams, 5–8 players each |
| Objective | Grab enemy flag box, return to your base box |
| Flag Pickup | Hold ACTION on flag box for 2s |
| Flag Return | Hold ACTION on base box for 2s while carrying flag |
| Flag Visibility | Carrier visible to ALL enemies as pulsing yellow dot |
| Flag Drop | Press CANCEL or get hit → flag drops at location |
| Win Condition | First to 3 captures, or most at time limit |

## Node Behavior (Flag Box)

| State | LED Ring | OLED | Buzzer |
|-------|----------|------|--------|
| At base | Solid team color | "FLAG" + team name | None |
| Carried | Pulsing yellow | "CARRIED" | None |
| Dropped | Static yellow | "DROPPED" + timer | Beep every 5s |
| Scored | Rainbow flash | "SCORE!" | Victory tone |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| Normal play | Green dots = teammates, red = enemies | Standard | Team color |
| You carry flag | Your dot pulses yellow; enemies see you | Slow pulse | Yellow pulse |
| Teammate carries flag | Yellow dot on radar | None | Team color |
| Enemy carries your flag | Yellow dot + direction arrow | Rapid pulse | Red flash |
| Near flag box | "GRAB FLAG" prompt | Short buzz | White flash |

## Tier Requirements

- **Tier 0** — Core band ($12/player)
- **Tier 1** — 2x Objective Nodes ($15 each = $30 total)
- **Total field cost:** $176 (server + 8 bands) + $30 = **$206**

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Multi-Flag** | 3 mini-flags, first to 2 wins | Medium |
| **Neutral Flag** | One flag in center, both teams race | Hard |
| **Flag Jammer** | Carrier can press band button to hide dot for 5s (60s cooldown) | Hard |
