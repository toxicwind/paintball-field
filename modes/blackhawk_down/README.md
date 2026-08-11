# Blackhawk Down

> **"The helo is down. The enemy is coming. Hold the crash site."**
>
> *Exclusive to Blitz Paintball Military Base field — the only paintball field in Colorado with a real Blackhawk helicopter.*

## Overview

One team defends a crashed UH-60 Blackhawk helicopter. The other team must infiltrate and capture 3 RFID objective tags hidden inside and around the helicopter.

This mode leverages Blitz's unique asset — the only Blackhawk on a paintball field in the state — and turns it into the centerpiece of an objective-based experience that no other field can replicate.

## Field Setup

### Required Hardware
- 3x GhostNode P1 (objective boxes)
- 8+ GhostBand P1 (player bands)
- 1x GhostHub P1 (field gateway)
- 1x RefCommand tablet

### Objective Placement

| Tag | Location | Difficulty |
|-----|----------|------------|
| Alpha | Inside the helicopter cockpit | Hard — defenders will camp this |
| Bravo | Under the tail rotor assembly | Medium — exposed, but hard to reach |
| Charlie | Inside the nearest concrete silo (20m from helo) | Easy — but far from the others |

**Defenders** place the tags during setup. Attackers don't know exact locations, only that all 3 are "in or around the helicopter area."

### Boundaries
- Defenders may not leave a 30-meter radius from the helicopter.
- Attackers respawn at a forward base marked with a flag (50m from helo).
- The helicopter interior is a "hot zone" — see Special Rules.

## Teams

| | Attackers | Defenders |
|--|-----------|-----------|
| **Goal** | Capture all 3 tags (RFID scan) | Prevent capture for 15 minutes |
| **Respawns** | Unlimited at forward base | 2 respawns each, then eliminated |
| **Starting position** | Forward base (50m out) | Helicopter area (30m radius) |
| **Band signal** | Green = alive, fast green = tag captured | Green = alive, red flash = out of lives |

## Game Flow

### Phase 1: Setup (2 minutes)
1. Ref assigns teams. Defenders get 2 minutes to place tags and set up.
2. Attackers wait at forward base. Ref gives them a 30-second countdown.
3. Ref starts game on tablet. All bands vibrate once = GO.

### Phase 2: Assault (15 minutes max)
1. Attackers push toward helicopter. Defenders hold position.
2. When an attacker scans a tag, their band vibrates 3x fast green. Ref tablet shows "Tag [X] captured by Player [Y]."
3. Defenders can eliminate attackers. Attackers respawn at forward base after 30-second delay.
4. Defenders have 2 lives. After second elimination, band goes solid red = spectator.

### Phase 3: Resolution
- **Attackers win**: All 3 tags captured. Ref tablet auto-announces. Bands vibrate victory pattern.
- **Defenders win**: 15 minutes expire with 1+ tag uncaptured. Ref ends game. Bands vibrate defense pattern.
- **Draw**: Both teams eliminated (rare). Ref calls it.

## Special Rules

### Hot Zone (Helicopter Interior)
The helicopter interior is "radioactive." Players inside for more than 30 seconds must respawn.

- Band starts vibrating slowly when you enter the helo.
- At 20 seconds: vibration speeds up.
- At 30 seconds: band flashes red, player is eliminated, must respawn.

**Why**: Prevents defenders from camping inside the helicopter indefinitely. Forces movement. Adds tension.

### Tag Reclamation
If a defender scans a captured tag, it resets to neutral. The attacker must re-scan it.

- This only works if the defender is within 1 meter of the tag (RFID range).
- Ref tablet shows "Tag [X] reset by Player [Y]."

### Wounded Extraction Variant
For larger groups (12+ players), add the Search & Rescue rule:
- When eliminated, a player becomes "wounded" (band flashes yellow) instead of dead.
- A teammate must scan their band to "drag them to safety" (both bands vibrate = extraction complete).
- Extracted players respawn at forward base.

## Referee Role

The ref is the game master. Their tablet shows:
- **Live tag status**: Which tags are captured, neutral, or reset
- **Player counts**: Attackers alive vs. Defenders alive + lives remaining
- **Timer**: 15-minute countdown with 5-min, 2-min, 1-min auto-announcements (band vibrations)
- **Hot zone monitor**: Who is inside the helicopter and for how long
- **Emergency controls**: Force-eliminate, pause game, end game

**The ref does NOT see player positions.** Only status and objective state. This keeps the ref focused on fairness and safety, not GPS stalking.

## Why This Mode Works

1. **Unique asset**: No other field has a Blackhawk. This mode is a Blitz exclusive.
2. **Asymmetric gameplay**: Attackers have numbers + unlimited respawns. Defenders have position + limited lives. Balanced tension.
3. **Objective clarity**: RFID scan = undeniable proof. No arguments about whether someone "touched" the helicopter.
4. **Ref empowerment**: One ref can run this smoothly because the tablet does the monitoring.
5. **Photo moments**: Players posing with the Blackhawk, capturing tags, extraction scenes. Social media gold.

## Scaling

| Players | Attackers | Defenders | Tags | Duration | Notes |
|---------|-----------|-----------|------|----------|-------|
| 8 | 5 | 3 | 3 | 15 min | Minimum viable |
| 12 | 7 | 5 | 3 | 15 min | Standard |
| 16 | 10 | 6 | 3 | 20 min | Add Wounded Extraction |
| 20+ | 12 | 8 | 4 | 20 min | Add 4th tag in second silo |

## Variants

### Night Ops
Run at dusk with glow sticks on tags and LED strips on the helicopter. GhostNode LEDs are visible from 50m. Band LEDs are dimmed to not give away position.

### Blackhawk Rescue
Reverse the roles. The helicopter crew is "downed" and must be extracted by a rescue team. Defenders try to prevent extraction.

### Payload
One tag is a "bomb" that must be carried from the helo to the attacker's base. Carrier is visible to all (band LED bright green). If eliminated, bomb drops. Anyone can pick it up.

## First Playtest Notes

*To be filled after Blitz pilot.*

| Date | Players | Issues | Adjustments |
|------|---------|--------|-------------|
| | | | |

## Files

- `rules.md` — Printable referee cheat sheet
- `setup_checklist.md` — Field setup step-by-step
- `player_briefing.md` — What to tell players before the game
