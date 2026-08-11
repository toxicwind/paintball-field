# Tournament

## Overview

Referee-grade competitive mode. Full hit validation via BLE proximity + position cross-reference. Command station generates match replay, validates disputes, and produces tournament brackets.

## Rules

| Rule | Detail |
|------|--------|
| Teams | 2 teams, 4–8 players each |
| Format | Best of 3, 5, or 7 rounds |
| Hit Validation | Server cross-references: BLE proximity <2m + shooter facing target + timestamp within 2s |
| Dispute | Referee taps player on command station → instant replay of last 10s |
| Penalty | False hit claim = 1-round suspension |
| Win Condition | Eliminate all enemies or complete objective |

## Command Station Features

| Feature | Purpose |
|---------|---------|
| Live Map | All player positions, health, ammo (honor system) |
| Hit Replay | Rewind 10s, see both player perspectives |
| Dispute Button | Instant flag for referee review |
| Auto-Score | No manual scorekeeping |
| Bracket Gen | Auto-generates tournament brackets from match results |
| Export | Match data → JSON for streaming overlay |

## Tier Requirements

- **Tier 0** — Core band ($12/player)
- **Tier 2** — Hit detection firmware (OTA upgrade)
- **Tier 3** — Command Station ($150)
- **Total field cost:** $176 + $150 = **$326**

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Pro League** | 7-round matches, full replay, streaming overlay | Hard |
| **Scrimmage** | Practice mode, no validation, instant respawn | Easy |
| **Showmatch** | Spectator mode, all positions visible to audience | Medium |
