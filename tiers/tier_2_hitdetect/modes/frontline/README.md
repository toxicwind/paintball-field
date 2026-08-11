# Frontline

## Overview

Checkpoint-based respawn mode. Teams fight to capture sequential checkpoints across the field. When hit, players must mark their band (press button to confirm), return to their team's furthest checkpoint, and their band unlocks for respawn. The referee command station shows live team strength: alive players + reinforcements remaining. First team to capture all checkpoints or deplete enemy reinforcements wins.

## Rules

| Rule | Detail |
|------|--------|
| Teams | 2 teams, 6–10 players each |
| Checkpoints | 3–5 checkpoints in a line across field |
| Capture | Stand within 3m of checkpoint node for 10s uninterrupted |
| Respawn | When hit: band vibrates → press ACTION to "mark" (confirm hit) → run to your furthest checkpoint → band auto-unlocks |
| Reinforcements | Each team starts with 50 reinforcements (shared lives pool) |
| Death Cost | Each hit + respawn costs 1 reinforcement |
| Band Lock | After marking hit, band OLED shows "RETURN TO SPAWN" and radar is disabled until respawn |
| Win Condition | Capture all checkpoints OR deplete enemy reinforcements |

## Checkpoint Node Behavior

| State | LED Ring | OLED | Buzzer |
|-------|----------|------|--------|
| Neutral | White pulse | "CHECKPOINT 2" | None |
| Capturing (Red) | Blinking red | "RED CAPTURING..." + bar | Building tone |
| Captured (Red) | Solid red | "RED CONTROL" | Victory chime |
| Captured (Blue) | Solid blue | "BLUE CONTROL" | Victory chime |
| Contested | Alternating | "CONTESTED!" | Alarm |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| Alive | Green dots = teammates, red = enemies, checkpoints = white diamonds | Standard | Team color |
| Hit (unconfirmed) | "YOU'RE HIT! MARK BAND" | Rapid pulse | Red flash |
| Marked / Locked | "RETURN TO SPAWN" + arrow pointing to checkpoint | None | Dim red |
| Respawning | Countdown "3... 2... 1..." | Slow ticks | Team color pulse |
| Respawned | "BACK IN ACTION" | Short buzz | Solid team color |
| Near checkpoint | "RESPAWN HERE" | Confirm buzz | Green flash |
| Reinforcements low (<10) | "LOW REINFORCEMENTS" warning | Urgent pulse | Red/yellow flash |

## Command Station (Referee View)

| Metric | Display |
|--------|---------|
| Team Strength | Alive players / Reinforcements remaining |
| Checkpoint Status | Visual map with checkpoint colors |
| Death Rate | Kills per minute per team |
| Match Time | Countdown or elapsed |
| Win Probability | Live estimate based on positions + reinforcements |

## Tier Requirements

- **Tier 0** — Core band ($12/player)
- **Tier 1** — 3–5x Checkpoint Nodes ($15 each = $45–$75)
- **Tier 2** — Hit detection firmware (OTA upgrade, $0)
- **Total field cost:** $176 + $60 = **$236**

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Overtime** | If reinforcements equal at time limit, next checkpoint capture wins | Medium |
| **Blitz** | Only 3 checkpoints, 20 reinforcements, 8 min matches | Hard |
| **King of the Hill** | One moving checkpoint, first to 100 reinforcements spent on captures wins | Medium |
| **Last Stand** | No checkpoints — pure attrition. Last team with reinforcements wins | Easy |
