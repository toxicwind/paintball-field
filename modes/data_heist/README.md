# Data Heist

## Overview

Asymmetric objective mode. Attackers must hack 3 terminals in sequence (A → B → C). Each terminal hack takes 15s and reveals the hacker objective progress to defenders as a pulsing purple dot. Defenders must protect all 3. The twist: hackers can "mask" their signal (hide dot for 5s) once per terminal, but masking disables their own radar. High-risk, high-reward stealth.

## Rules

| Rule | Detail |
|------|--------|
| Teams | Attackers vs Defenders, 4–6 players each |
| Terminals | 3 fixed points (A, B, C) |
| Hack | 15s channel at terminal. Interrupted = reset. |
| Sequence | Must hack A, then B, then C in order |
| Mask | Once per terminal: hide purple dot for 5s. Radar disabled during mask. |
| Win Condition | Attackers: hack all 3. Defenders: prevent within 15 min. |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| Hacker at terminal | Progress bar + "HACKING" | Steady tone | Purple |
| Hacker masked | "MASKED" + no tactical display | None | Off |
| Defender | Purple dot = hacker position | Urgent when hacker near terminal | Red |
| Terminal hacked | "TERMINAL A: HACKED" | Success buzz | Green flash |
| All terminals hacked | "DATA HEIST COMPLETE" | Victory pattern | Rainbow |

## Terminal Configuration

```json
{
  "terminals": [
    {"id": "A", "x": 5, "y": 5, "hack_time": 15},
    {"id": "B", "x": 25, "y": 15, "hack_time": 15},
    {"id": "C", "x": 45, "y": 25, "hack_time": 15}
  ],
  "mask_duration": 5,
  "mask_cooldown": 60
}
```

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Parallel Heist** | All 3 terminals can be hacked simultaneously; defenders split | Hard |
| **Mobile Terminal** | One terminal moves every 2 min | Medium |
| **Decoy Hack** | Fake terminals that trigger alarms when hacked | Hard |
