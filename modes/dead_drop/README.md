# Dead Drop

> **"Three packages. Unknown locations. One sequence. Find them before the enemy does."**

## Overview

Three GhostNode P1 objective boxes are hidden across the field. Each team must find and scan all 3 in a specific sequence. The catch: only the referee knows the sequence, and the band gives warm/cold hints via LED color.

This is a stealth and communication mode. Running around randomly gets you killed. Coordinated searching with your team wins the game.

## Field Setup

### Required Hardware
- 3x GhostNode P1 (objective boxes)
- 8+ GhostBand P1 (player bands)
- 1x GhostHub P1
- 1x RefCommand tablet

### Objective Placement
The ref hides 3 nodes before players arrive. Nodes are:
- **Camouflaged**: Same color as surroundings (olive drab, tan, gray)
- **RFID-active**: Player bands read them from 0-10cm
- **LED-off until scanned**: No glow until someone finds it

**Placement rules:**
- At least 20m apart from each other
- At least 10m from any spawn point
- Not inside buildings (RFID doesn't work through walls well)
- Under bushes, behind bunkers, inside barrels, taped to trees

### Sequence Generation
The ref tablet randomizes the scan sequence at game start. Only the ref sees it.

Example sequences:
- Alpha → Bravo → Charlie
- Bravo → Alpha → Charlie
- Charlie → Bravo → Alpha

## Teams

Both teams have the same goal: find all 3 drops in the correct order.

| | Team Alpha | Team Bravo |
|--|------------|------------|
| **Goal** | Find 3 drops in sequence | Find 3 drops in sequence |
| **Respawns** | Unlimited, 30s delay at base | Unlimited, 30s delay at base |
| **Intel** | Warm/cold LED hints | Warm/cold LED hints |

## Game Flow

### Phase 1: Briefing (3 minutes)
1. Ref explains: "3 drops hidden. Find them in order. Your band will tell you if you're getting warmer."
2. Ref starts game. All bands vibrate once = GO.
3. Bands show solid green = searching for Drop 1.

### Phase 2: Hunt
1. Players spread out. Band LED shows:
   - **Blue pulse** = cold (no drop nearby)
   - **Yellow pulse** = warm (drop within 20m)
   - **Orange pulse** = hot (drop within 5m)
   - **Green flash** = drop found and scanned!
2. When a player scans the correct next drop, band vibrates 2x and LED goes solid green for 3 seconds.
3. Band then switches to searching for Drop 2 (blue pulse resumes).
4. If a player scans the WRONG drop (out of sequence), band vibrates 1x red. Ref tablet shows "False scan by Player [X]." No penalty, just wasted time.

### Phase 3: Race to Finish
First team to scan all 3 in correct order wins.

Ref tablet shows:
- Team Alpha progress: [Alpha] [Bravo] [Charlie] — 2/3 complete
- Team Bravo progress: [Bravo] [Alpha] [Charlie] — 1/3 complete

## Band LED Signals (Dead Drop Mode)

| LED Pattern | Meaning |
|-------------|---------|
| Blue pulse (slow) | Searching — no drop nearby |
| Yellow pulse | Warm — drop within ~20m |
| Orange pulse (fast) | Hot — drop within ~5m |
| Green flash x2 | Correct drop scanned! |
| Red flash x1 | Wrong drop scanned (out of sequence) |
| Red SOS | You've been hit — call it out |
| All LEDs off | Eliminated / spectator |

## Warm/Cold Logic

The GhostNode broadcasts a LoRa beacon every 2 seconds. Player bands measure RSSI:

```
RSSI > -50 dBm  → Hot (within 5m)
RSSI > -70 dBm  → Warm (within 20m)
RSSI < -70 dBm  → Cold (far away)
```

**Important**: The band only measures RSSI for the NEXT drop in sequence. It ignores other drops. This prevents confusion.

## Referee Role

- **Setup**: Hide nodes, verify RFID range (0-10cm), test warm/cold thresholds
- **Monitor**: Watch both teams' progress on tablet. Call out "Team Alpha found Drop 1!" for drama.
- **Adjust**: If one team is dominating, ref can "accidentally reveal" a drop location via a "loudspeaker announcement" (simulated intel leak).
- **Safety**: Players tunnel-vision on their bands. Ref must watch for unsafe play near boundaries.

## Why This Mode Works

1. **Forces communication**: "I'm getting warm near the north bunker!" Teams must talk.
2. **No camping**: Drops are scattered. Sitting in one spot loses the game.
3. **Ref involvement**: The ref is the game master, not just a safety observer.
4. **Replayability**: Randomized sequences and hidden locations mean every game is different.
5. **Low hardware cost**: 3 nodes, 8 bands. Same kit as Blackhawk Down.

## Scaling

| Players | Nodes | Duration | Notes |
|---------|-------|----------|-------|
| 8 | 3 | 20 min | 4v4, intense |
| 12 | 3 | 20 min | 6v6, standard |
| 16 | 4 | 25 min | Add 4th node, 8v8 |
| 20+ | 5 | 30 min | Add 5th node, 10v10 |

## Variants

### Saboteur
One player per team is a saboteur. Their band looks normal, but when they scan a drop, it resets to neutral for their team. Only the ref knows who the saboteur is. Teams must figure it out.

### Time Bomb
Each drop has a 5-minute timer. If not found within 5 minutes, it "explodes" (node LED flashes red, all nearby players eliminated). Forces fast play.

### Decoy Drops
Add 2 fake nodes that look identical but have no RFID. Scanning them does nothing. Wastes time. Only the ref knows which are real.

## First Playtest Notes

*To be filled after pilot.*

| Date | Players | Hide Time | Find Time | Issues |
|------|---------|-----------|-----------|--------|
| | | | | |
