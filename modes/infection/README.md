# Infection

## Overview

Zombie mode. One player starts infected. Survivors see infected through walls (red dots). Infected see only survivor positions (green dots). Infected have unlimited respawn; survivors have one life. The tension: survivors must trust their radar, but infected can coordinate swarm tactics.

## Rules

| Rule | Detail |
|------|--------|
| Players | 6–16 (asymmetric) |
| Start | 1 infected, rest survivors |
| Infection | Touch survivor for 2s (BLE proximity) |
| Survivor Lives | 1 life; become infected on death |
| Infected Respawn | 5s respawn at random field edge |
| Win Condition | Survivors: survive 10 min. Infected: infect all. |

## Band Behavior

| State | OLED Display | Haptic | LED |
|-------|-------------|--------|-----|
| Survivor | Red dots = infected (through walls) | Warning buzz when infected within 5m | Solid green |
| Infected | Green dots = survivors only | None | Pulsing red |
| Just infected | Screen flash | Long buzz | Flash red→green→red |
| Last survivor | All infected visible, countdown | Heartbeat panic | Rapid green pulse |

## Proximity Infection

- Infected must be within 2m of survivor for 2s continuous
- Band vibrates for survivor during infection attempt
- Infected get +20% movement speed (honor system or referee call)

## Variants

| Variant | Change | Difficulty |
|---------|--------|------------|
| **Alpha** | Infected alpha has wall vision; minions do not. Alpha dies = minions lose vision for 10s | Hard |
| **Cure** | One random survivor can "cure" infected by touching them for 3s | Medium |
| **Safe Room** | One 5m zone is safe; survivors inside = invisible to infected | Easy |
