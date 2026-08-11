# Domination

## Overview

Zone-control with physical nodes. Teams fight to capture and hold zone nodes. Capturing a zone reveals enemy positions inside that zone to your team. Nodes are placed across the field as capture points.

## Rules

| Rule | Detail |
|------|--------|
| Teams | 2 teams, 5–10 players each |
| Zones | 3–5 zone nodes placed across field |
| Capture | Stand within 3m of zone node + hold ACTION for 10s uninterrupted |
| Decay | Zone reverts to neutral after 30s uncontested |
| Win Condition | First to 300 points, or highest at 12 min |

## Scoring

| Action | Points |
|--------|--------|
| Zone captured | +50 |
| Hold per 5s | +10 |
| Enemy kill in your zone | +15 |
| Death in enemy zone | -5 |

## Node Behavior (Zone Node)

| State | LED Ring | OLED | Buzzer |
|-------|----------|------|--------|
| Neutral | White pulse | "NEUTRAL" | None |
| Capturing | Blinking team color | Progress bar | Building tone |
| Captured (Red) | Solid red | "RED CONTROL" | None |
| Captured (Blue) | Solid blue | "BLUE CONTROL" | None |
| Contested | Alternating red/blue | "CONTESTED!" | Alarm tone |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| In neutral zone | Zone boundary flashes white | Slow pulse | Team color |
| Capturing zone | Progress bar on screen | Building rumble | Team color + white pulse |
| Zone captured | Enemies inside = red dots | Victory buzz | Solid team color |
| Enemy captures zone | Your team loses intel | Warning buzz | Red flash |
| In enemy zone | No enemy intel | None | Dim team color |

## Tier Requirements

- **Tier 0** — Core band ($12/player)
- **Tier 1** — 3–5x Zone Nodes ($15 each = $45–$75)
- **Total field cost:** $176 + $60 (4 nodes) = **$236**

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **King of the Hill** | One zone, 200 points to win, constant brawl | Easy |
| **Linked Zones** | Must hold A+B or B+C to get intel; A alone = nothing | Hard |
| **Mobile Zone** | Zone node moves every 60s to random location | Medium |
