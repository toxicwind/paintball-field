# Domination

## Overview

Zone-control mode. Teams fight to capture and hold zones. Capturing a zone reveals objective contest status inside that zone to your team. This creates a "information warfare" layer on top of standard domination — you want zones not just for points, but for intel.

## Rules

| Rule | Detail |
|------|--------|
| Teams | 2 teams, 5–10 players each |
| Zones | 3–5 zones placed across field |
| Capture | Stand in zone for 10s uninterrupted |
| Decay | Zone reverts to neutral after 30s uncontested |
| Win Condition | First to 300 points, or highest at 12 min |

## Scoring

| Action | Points |
|--------|--------|
| Zone captured | +50 |
| Hold per 5s | +10 |
| Enemy kill in your zone | +15 |
| Death in enemy zone | -5 |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| In neutral zone | Zone boundary flashes white | Slow pulse | Team color |
| Capturing zone | Progress bar on screen | Building rumble | Team color + white pulse |
| Zone captured | Enemies inside = red dots | Victory buzz | Solid team color |
| Enemy captures zone | Your team loses intel | Warning buzz | Red flash |
| In enemy zone | No enemy intel | None | Dim team color |

## Zone Configuration

Zones are 5m radius circles. AP nodes double as zone beacons — no extra hardware needed.

```json
{
  "zones": [
    {"id": "A", "x": 10, "y": 15, "radius": 5},
    {"id": "B", "x": 25, "y": 15, "radius": 5},
    {"id": "C", "x": 40, "y": 15, "radius": 5}
  ]
}
```

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **King of the Hill** | One zone, 200 points to win, constant brawl | Easy |
| **Linked Zones** | Must hold A+B or B+C to get intel; A alone = nothing | Hard |
| **Mobile Zone** | Zone moves every 60s to random location | Medium |
