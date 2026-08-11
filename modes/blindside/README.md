# Blindside

## Overview

Pure audio/haptic mode. OLED is off. No radar. Players rely entirely on haptic feedback to know when they've been hit and from what direction. The band vibrates in a pattern that encodes the direction of the hit based on BLE proximity to the shooter. This is the most hardcore mode — pure instinct and sound.

## Rules

| Rule | Detail |
|------|--------|
| Teams | 2 teams, 3–5 players each |
| Vision | None — OLED off for all players |
| Hit Detection | BLE proximity determines shooter direction |
| Haptic Pattern | Short pulse = front. Long pulse = back. Double = left. Triple = right. |
| Win Condition | Classic elimination |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| Normal | OFF | None | Team color (dim) |
| Hit from front | OFF | Short pulse | White flash |
| Hit from back | OFF | Long pulse | White flash |
| Hit from left | OFF | Double pulse | White flash |
| Hit from right | OFF | Triple pulse | White flash |
| Low health (<30%) | OFF | Slow heartbeat | Red pulse |
| Eliminated | OFF | Long buzz | Off |

## Direction Encoding

```
Front  →  .__
Back   →  ____
Left   →  ._.
Right  →  ._._.  (approximate — DRV2605 effect library)
```

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Echo** | Haptic pattern also encodes distance (shorter = closer) | Hard |
| **Silent Hunt** | No haptic on hit; only on elimination | Extreme |
| **Audio Cues** | Band plays tone instead of vibration (requires buzzer) | Medium |
