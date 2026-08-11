# Capture the Flag

## Overview

Classic CTF reimagined with real-time positioning. The flag carrier is visible to the enemy team as a pulsing yellow dot on their tactical display. This creates a "hot potato" dynamic — the carrier must move fast, relay to teammates, or sacrifice themselves to reset visibility.

## Rules

| Rule | Detail |
|------|--------|
| Teams | 2 teams, 5–8 players each |
| Objective | Steal enemy flag, return to your base |
| Flag Visibility | Carrier visible to ALL enemies as pulsing yellow dot |
| Flag Relay | Carrier can pass flag to teammate by being within 2m for 3s |
| Respawn | 15s respawn at base; flag drops on death |
| Win Condition | First to 3 captures, or most captures at time limit |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| Normal play | Green dots = teammates, red = enemies | Standard hit click | Team color |
| You have flag | Your dot pulses yellow; enemies see you | Slow pulse (heartbeat) | Yellow pulse |
| Teammate has flag | Yellow dot on radar | None | Team color |
| Enemy has your flag | Yellow dot on radar + direction arrow | Rapid pulse (urgency) | Red flash |
| Flag dropped | Yellow dot static (no pulse) | Single buzz | Yellow static |

## Positioning Mechanics

- Flag carrier status broadcast to enemy team at 2Hz (slower than normal 5Hz to add jitter)
- Flag relay requires both players stationary within 2m for 3s
- Dropped flag status broadcast to both teams until picked up

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Multi-Flag** | 3 mini-flags, first to 2 wins | Medium |
| **Neutral Flag** | One flag in center, both teams race | Hard |
| **Flag Jammer** | Carrier can press button to hide dot for 5s (60s cooldown) | Hard |
