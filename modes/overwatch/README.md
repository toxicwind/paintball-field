# Overwatch

## Overview

One player per team becomes the Overwatch — they get a zoomed-out 2D map of the entire field on their band, showing all player positions. They cannot shoot. Their team follows their ping commands (the Overwatch can send directional pings to teammate bands). This turns one player into a real-time commander.

## Rules

| Rule | Detail |
|------|--------|
| Teams | 2 teams, 4 players each |
| Overwatch | Randomly assigned, no weapon, stationary spawn |
| Overwatch Vision | Full 2D field map with all player positions |
| Ping | Overwatch can send 3 pings per 10s to teammate bands (direction + distance) |
| Win Condition | Eliminate all enemies |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| Overwatch | Zoomed 2D map (50x30m field scaled to 64x64px) | None | Gold |
| Teammate | Standard radar + ping arrows when Overwatch pings | Ping buzz | Team color |
| Ping received | Arrow + distance number appears | Short buzz | White flash |
| Overwatch down | Team loses map intel for 30s | Warning | Red flash |

## Ping System

```
Overwatch taps band screen → selects teammate → selects direction → teammate receives:
  - Arrow pointing to pinged location
  - Distance in meters
  - Haptic confirmation
```

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Drone Overwatch** | Overwatch can move slowly (crawl speed) but loses map if hit | Medium |
| **Dual Overwatch** | 2 Overwatch players; pings stack for combined intel | Hard |
| **Jammer** | Enemy can jam Overwatch for 10s (disable pings) | Hard |
