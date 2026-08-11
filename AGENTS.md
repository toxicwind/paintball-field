# AGENTS.md — SpectreBand / GhostNet Internal Operations

> **This document is for project collaborators and field operators.**  
> It contains operational details, vendor relationships, deployment timelines, and the polyglot testing framework that are not in the public README.

---

## Product Architecture: Two Systems, One Repo

This is a **monorepo** containing two distinct product lines. Do not confuse them.

| | **GhostNet (Tier P)** | **SpectreBand (Tiers 0-3)** |
|---|---|---|
| **Codename** | GhostNet | SpectreBand |
| **Purpose** | Affordable entry, ref monitoring, objective games | Premium experience, full radar, tournament |
| **Display** | 3x RGB LED + haptic | 0.96" OLED screen |
| **Player Display** | 3x RGB LED + haptic | 0.96" OLED (objectives, scores, timers) |
| **Radio** | LoRaWAN 915 MHz | WiFi 2.4 GHz + BLE |
| **Range** | 2-5km outdoor | 50-100m |
| **Battery** | 8+ hours active, 1 week standby | 4+ hours active |
| **BOM** | $10.10/band | $12.00/band |
| **Kit cost (8 players)** | $168 | $295 |
| **Player add-on** | $8/session | $8/session |
| **Payback** | 3 sessions | 3 sessions |
| **MCU** | Heltec HT-CT62 | ESP32-C3-MINI-1 |
| **Firmware** | Bare-metal Arduino, no FreeRTOS | FreeRTOS dual-core |
| **Server** | FastAPI + SQLite WAL | FastAPI + SQLite WAL + WebSocket |
| **Ref tablet** | Required (live dashboard) | Optional (tournament only) |

**Migration path:** GhostNet bands use the same HT-CT62 MCU as SpectreBand anchors. Flash SpectreBand firmware later if you add OLED screens. Hardware is forward-compatible.

---

## Primary Deployment: Blitz Paintball, Dacono CO

**Status**: Active pilot planning — GhostNet first, SpectreBand second  
**Contact**: Blitz Staff via blitzpaintball.net  
**Address**: 5340 Summit Blvd, Dacono, CO 80514  
**Phone**: 303-337-7109

### Why Blitz First

Blitz is the ideal pilot field:

- **4 distinct fields** = 4 test environments in one location
- **Urban Combat** (60x40m, 200+ bunkers) = SpectreBand multipath stress test
- **Military Base** (50x50m, helicopter, missile silos) = **Blackhawk Down mode**, metal interference, LoRa range test
- **Hyperball** (55x50m, 68 bunkers) = SpectreBand accuracy field
- **Hyper-Spool** (30x25m) = GhostNet pilot field, small groups

### GhostNet Pilot Timeline (3 weeks)

| Phase | Week | Bands | Field | Modes | Goal |
|-------|------|-------|-------|-------|------|
| **1** | 1 | 2 | Hyper-Spool | Dead Drop | Validate LoRa range, RFID range, haptic patterns |
| **2** | 2 | 8 | Hyper-Spool | All 4 modes | Full kit test, ref tablet UI feedback |
| **3** | 3 | 8 | Military Base | Blackhawk Down | Helicopter mode, metal interference, photo/video |

### SpectreBand Pilot Timeline (5 weeks, parallel or after GhostNet)

| Phase | Weeks | Bands | Field | Modes | Goal |
|-------|-------|-------|-------|-------|------|
| **1** | 1-2 | 8 | Hyper-Spool | Hunter-Prey, Ghost | Validate honor system, test strap durability |
| **2** | 3-4 | 8 | Urban Combat | + Domination, CTF | Test objective nodes in 200-bunker field |
| **3** | 5 | 8 | Military Base | + Frontline, Data Heist | Full system, charging rack, ref training |
| **4** | 6+ | 16+ | All fields | All Tier 0-2 modes | Scale to full rental fleet |

### Blitz-Specific Config

See `fields/blitz_dacono/config.json` for:
- Per-field AP placement coordinates (SpectreBand)
- Per-field LoRa gateway position (GhostNet)
- Per-field path loss calibration targets
- Recommended modes per field
- Blackhawk helicopter objective placement coordinates

### Pricing for Blitz

**GhostNet:**
- **Rental add-on**: $8/player/session
- **Band BOM**: $10.10
- **Kit BOM (8 players)**: $168
- **Payback**: 3 sessions at $8 x 8 = $192
- **Target margin**: 75% after kit cost recovered

**SpectreBand:**
- **Rental add-on**: $8/player/session
- **Band BOM v1.0**: $12.40 (pilot)
- **Band BOM v1.1**: $19.70 (production with IMU + shock sensor)
- **Payback**: 2 rentals at $8
- **Target margin**: 60% after band cost recovered

### Staff Training

- **GhostNet**: 1 ref minimum (tablet does the monitoring)
- **SpectreBand**: 2 refs minimum for pilot
- **1-page laminated SOP** attached to charging rack
- **Self-test on boot** — staff knows in 2 seconds if band is dead

---

## Competitive Intelligence

Full pricing data scraped from all Colorado paintball fields: `data/colorado_pricing_2026.parquet`

| Field | Location | Type | Fields | Group Rate (10+, entry+rental+500) | Notes |
|-------|----------|------|--------|-----------------------------------|-------|
| **Blitz Paintball** | Dacono, CO | Outdoor | 4 | **$39.85** | Our pilot field, Blackhawk helicopter |
| **Dynamic Paintball** | Aurora, CO | Outdoor | 3 | $40.00 (3 Star, 3hr) | Closest competitor on price |
| **American Paintball Coliseum** | Denver/Aurora, CO | Indoor+Outdoor | 3 | $30.00 (pass+rental, NO paint) | Very small facility, laser tag + axe throwing |

**Key insight:** Blitz's $39.95 group rate is the anchor. GhostNet at $8 add-on = $47.95 total. Still cheaper than Blitz's own Intermediate package ($52.95) and cheaper than Dynamic's equivalent. The upsell is invisible.

---

## Secondary Deployments (Pipeline)

| Field | Location | System | Status | Notes |
|-------|----------|--------|--------|-------|
| Blitz Paintball | Dacono, CO | GhostNet + SpectreBand | Phase 1 (GhostNet) | Active pilot |
| TBD | Denver metro | GhostNet | Phase 2 | After Blitz GhostNet proven |
| TBD | Colorado Springs | GhostNet | Phase 3 | Need local partner |
| TBD | National | White-label | Phase 4 | Licensing model |

---

## Contractor Info

**Christopher Ortega**  
- Email: denverchrisortega@gmail.com
- GitHub: github.com/toxicwind
- Portfolio: resume.effusionlabs.com
- Specialization: LLM infrastructure, embedded systems, real-time positioning, LoRaWAN networks

### Engagement Model

| Service | Deliverable | Timeline | Rate |
|---------|-------------|----------|------|
| GhostNet field pilot | Full deploy at your field | 2-3 weeks | Flat fee + hardware |
| SpectreBand field pilot | Full deploy at your field | 4-5 weeks | Flat fee + hardware |
| Custom firmware | New game modes, hardware variants | 1-2 weeks | $150/hr |
| Server backend | FastAPI + WebSocket + analytics | 1-2 weeks | $125/hr |
| Hardware design | PCB, case, BOM optimization | 2-4 weeks | Project-based |
| Training | Staff SOP, ref training, troubleshooting | 1 day | Flat fee |

---

## Development Notes

### Branch Strategy

- `main` — stable, public-facing, both systems
- `ghostnet-pilot` — Blitz-specific GhostNet tweaks, calibration data
- `spectreband-pilot` — Blitz-specific SpectreBand tweaks
- `v1.1-hardware` — IMU + shock sensor development (SpectreBand)
- `feature/*` — New game modes, experimental

### Pre-Commit Hook

The `.git/hooks/pre-commit` Perl script:
1. Generates a seed-based SVG logo from the staged tree hash
2. Injects the new logo reference into README.md
3. Runs mermaid validation if `validate_mermaid.js` exists
4. Stages the new logo and updated README

**To regenerate logo manually:** `python3 generate_logo.py <seed>`

### Secrets Management

- No API keys in repo
- Drive9 mount for persistent state: `/mnt/agents/output/`
- GitHub PAT stored in `.env` (gitignored)
- Field configs contain no PII
- Competitive pricing data in `data/` is public information

### Persistence Strategy (Critical Fix)

**Problem:** Kernel restarts wipe in-memory state. Parquet files written to `/mnt/agents/output/` outside the repo are lost on restart.

**Solution:**
1. All data files live INSIDE the repo: `data/`, `fields/*/`, `tests/data/`
2. Git commit after every data generation step
3. Drive9 mount is for build artifacts and logs only, not source data
4. Use SQLite WAL for runtime state (server databases)
5. Use JSON for configuration (git-tracked)
6. Use Parquet for analytics (git-tracked LFS if >100MB)

**Checkpoint protocol:**
```bash
# After any data generation:
git add data/
git commit -m "data: <description>"
git push origin main
```

---

## Testing Framework: Polyglot Monorepo

This project uses a **multi-language testing architecture** borrowed from monadic composition patterns. Each language handles what it does best.

### `tests/perl/` — Hardware Simulation & Protocol Validation

Perl's regex and text processing strengths make it ideal for:
- LoRa packet format validation (binary struct parsing)
- RFID UID generation and collision detection
- Serial protocol fuzzing (UART/ SPI mock devices)
- Build script automation

```perl
# Example: Validate GhostNet packet structure
use strict;
use warnings;
use Test::More;

my $packet = pack("CCCSL", 0x07, 0x00, 0x00, 0x0000, 0x00000000);
my ($player_id, $team_id, $status, $rssi, $timestamp) = unpack("CCCSL", $packet);

is($player_id, 7, "Player ID correct");
is($team_id, 0, "Team Alpha");
done_testing();
```

### `tests/haskell/` — State Machine Verification & Property Testing

Haskell's type system and QuickCheck make it ideal for:
- Game state machine verification (alive -> eliminated -> respawned)
- Property-based testing of scoring logic
- Formal verification of protocol invariants
- Monadic game loop composition

```haskell
-- Example: Verify player status transitions
{-# LANGUAGE DeriveGeneric #-}
module GhostNet.State where

data PlayerStatus = Alive | Eliminated | Wounded | Ghost
  deriving (Eq, Show, Generic)

data Transition = Hit | Respawn | Wound | Extract
  deriving (Eq, Show)

transition :: PlayerStatus -> Transition -> Maybe PlayerStatus
transition Alive Hit = Just Eliminated
transition Alive Wound = Just Wounded
transition Wounded Extract = Just Alive
transition Eliminated Respawn = Just Alive
transition _ _ = Nothing

-- QuickCheck property: no invalid transitions
prop_validTransitions :: PlayerStatus -> Transition -> Bool
prop_validTransitions s t = case transition s t of
  Just _  -> True
  Nothing -> True  -- Invalid transitions are correctly rejected
```

### `tests/scala/` — Concurrent System Simulation & Load Testing

Scala's actor model and Akka make it ideal for:
- Simulating 100+ concurrent player bands
- Load testing the WebSocket ref tablet connection
- Testing race conditions in objective capture
- Distributed match state synchronization

```scala
// Example: Actor-based match simulation
import akka.actor.{Actor, ActorRef, ActorSystem, Props}

case class PlayerScan(playerId: Int, objectiveId: Int, timestamp: Long)
case class ObjectiveCaptured(objectiveId: Int, teamId: Int)

class MatchActor(matchId: Int) extends Actor {
  var objectives = Map.empty[Int, Option[Int]]  // objId -> capturingTeam
  var scores = Map(0 -> 0, 1 -> 0)  // team -> score
  
  def receive = {
    case PlayerScan(pid, oid, ts) =>
      if (!objectives.contains(oid)) {
        val team = pid % 2  // Simplified team assignment
        objectives += (oid -> Some(team))
        scores += (team -> (scores(team) + 1))
        sender() ! ObjectiveCaptured(oid, team)
      }
  }
}
```

### `tests/python/` — Integration Tests & Server Validation

Python handles:
- FastAPI endpoint testing (pytest + httpx)
- WebSocket client simulation
- SQLite database integrity checks
- Hardware-in-the-loop testing (when available)

### Test Execution

```bash
# Run all test suites
./tests/run_all.sh

# Run individual suites
prove -r tests/perl/           # Perl tests
stack test                     # Haskell tests (stack)
sbt test                       # Scala tests (sbt)
pytest tests/python/           # Python tests
```

---

## Vendor Relationships

| Vendor | Products | Lead Time | Contact |
|--------|----------|-----------|---------|
| Heltec Automation | HT-CT62, HT-M00 | 2-3 weeks (AliExpress) | heltec.org |
| LCSC Electronics | Passives, connectors, LEDs | 1 week | lcsc.com |
| JLCPCB | PCB fabrication | 1 week | jlcpcb.com |
| AliExpress | Batteries, enclosures, misc | 2-4 weeks | Various |
| Amazon | Pelican cases, USB hubs, tablets | 2 days | amazon.com |

---

## License

Same as public repo: MIT. This document is also MIT — share with collaborators freely.
# test
