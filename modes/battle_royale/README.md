# Battle Royale

## Overview

Free-for-all or squad-based. Safe zone shrinks over time. Players outside the zone take damage. The twist: the zone boundary is visible on every band as a red ring. Players inside see enemy positions within the zone (red dots). Players outside see nothing but the "storm" warning. Late-game becomes a positioning chess match.

## Rules

| Rule | Detail |
|------|--------|
| Players | 8–32 (solo or squads of 2–4) |
| Zone | Starts as full field, shrinks every 90s |
| Damage | 1 HP/s outside zone; 3 HP/s in final zone |
| Respawn | None — elimination |
| Loot | Honor system: call "loot" when you find paint pods on field |
| Win Condition | Last player/team standing |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| Inside zone | Red dots = enemies in zone | Standard hit click | Team color (squads) or white (solo) |
| Near zone edge (<5m) | Red border warning on screen edge | Slow pulse | Yellow warning |
| Outside zone | "STORM" warning + damage counter | Damage tick every 1s | Red pulse |
| Final 3 players | All remaining positions revealed | Heartbeat | Rapid pulse |
| Victory | "WINNER" + crown animation | Victory march | Rainbow cycle |

## Zone Shrinking

```python
# Zone shrinks by 20% every 90s, centered on random point in current zone
phases = [
    {"duration": 90, "shrink": 1.0},   # Full field
    {"duration": 90, "shrink": 0.8},   # 80%
    {"duration": 90, "shrink": 0.6},   # 60%
    {"duration": 90, "shrink": 0.4},   # 40%
    {"duration": 90, "shrink": 0.2},   # 20%
    {"duration": 60, "shrink": 0.1},   # 10% — final showdown
]
```

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Squad Rez** | Squadmates can revive downed players (3s channel) | Medium |
| **Airdrop** | Supply drops appear in zone; band shows drop location as blue dot | Easy |
| **Zoned Intel** | Each zone phase reveals a different intel type (positions, health, ammo) | Hard |
