# Spectre

## Overview

One player per team is the Spectre. The Spectre sees all enemy positions through walls permanently (red dots). Their team must protect them. If the enemy Spectre is eliminated, your team wins.

## Rules

| Rule | Detail |
|------|--------|
| Teams | 2 teams, 4–8 players each |
| Spectre | Randomly assigned per round, no weapon |
| Spectre Vision | Sees all enemies as red dots through walls (permanent) |
| Spectre Death | Team loses round instantly |
| Win Condition | Best of 5 rounds |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| You are Spectre | All enemies visible as red dots + distance | None | Solid purple |
| Protecting Spectre | Green dot = your Spectre; red = enemies | Warning when Spectre takes fire | Team color |
| Enemy Spectre spotted | Purple dot = enemy Spectre (if your team has intel) | Urgent pulse | Red flash |
| Spectre down | Screen flash + "SPECTRE DOWN" | Long buzz | White flash |

## Tier Requirements

- **Tier 0 only** — Core band ($12/player)
- No additional hardware needed

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Double Spectre** | Both teams have 2 Spectres; eliminate both to win | Medium |
| **Mobile Spectre** | Spectre changes every 60s to random teammate | Hard |
| **Spectre Shield** | Spectre can activate 5s invincibility (60s cooldown) | Easy |
