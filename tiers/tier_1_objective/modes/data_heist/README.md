# Data Heist

## Overview

Asymmetric objective mode. Attackers must hack 3 terminal nodes in sequence (A → B → C). Each terminal hack takes 15s and reveals the hacker's position to defenders as a pulsing purple dot. Hackers can "mask" their signal (hide dot for 5s) once per terminal, but masking disables their own radar.

## Rules

| Rule | Detail |
|------|--------|
| Teams | Attackers vs Defenders, 4–6 players each |
| Terminals | 3 terminal nodes placed across field |
| Hack | Hold ACTION on terminal for 15s uninterrupted |
| Sequence | Must hack A, then B, then C in order |
| Mask | Once per terminal: press CANCEL to hide purple dot for 5s. Radar disabled during mask. |
| Win Condition | Attackers: hack all 3. Defenders: prevent within 15 min. |

## Node Behavior (Terminal Node)

| State | LED Ring | OLED | Buzzer |
|-------|----------|------|--------|
| Idle | White | "TERMINAL A" | None |
| Hacking | Pulsing purple | "HACKING..." + bar + "15s" | Steady tone |
| Masked | Off | "MASKED" | None |
| Hacked | Solid purple | "TERMINAL A: HACKED" | Success tone |
| All hacked | Rainbow | "DATA HEIST COMPLETE" | Victory march |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| Hacker at terminal | Progress bar + "HACKING" | Steady tone | Purple |
| Hacker masked | "MASKED" + no radar | None | Off |
| Defender | Purple dot = hacker position | Urgent when hacker near terminal | Red |
| Terminal hacked | "TERMINAL A: HACKED" | Success buzz | Green flash |
| All terminals hacked | "DATA HEIST COMPLETE" | Victory pattern | Rainbow |

## Tier Requirements

- **Tier 0** — Core band ($12/player)
- **Tier 1** — 3x Terminal Nodes ($15 each = $45)
- **Total field cost:** $176 + $45 = **$221**

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Parallel Heist** | All 3 terminals can be hacked simultaneously; defenders split | Hard |
| **Mobile Terminal** | One terminal moves every 2 min | Medium |
| **Decoy Hack** | Fake terminals that trigger alarms when hacked | Hard |
