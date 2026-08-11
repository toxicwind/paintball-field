# AGENTS.md — SpectreBand Internal Operations

> **This document is for project collaborators and field operators.**  
> It contains operational details, vendor relationships, and deployment timelines that are not in the public README.

---

## Primary Deployment: Blitz Paintball, Dacono CO

**Status**: Active pilot planning  
**Contact**: Blitz Staff via blitzpaintball.net  
**Address**: 5340 Summit Blvd, Dacono, CO 80514  
**Phone**: 303-337-7109

### Why Blitz First

Blitz is the ideal pilot field:

- **4 distinct fields** = 4 test environments in one location
- **Urban Combat** (60x40m, 200+ bunkers) = stress test for multipath
- **Military Base** (50x50m, helicopter, missile silos) = worst-case metal interference
- **Hyperball** (55x50m, 68 bunkers) = best accuracy field
- **Hyper-Spool** (30x25m) = small-group pilot field

### Blitz Pilot Timeline

| Phase | Weeks | Bands | Field | Modes | Goal |
|-------|-------|-------|-------|-------|------|
| **1** | 1-2 | 8 | Hyper-Spool | Hunter-Prey, Ghost | Validate honor system, test strap durability |
| **2** | 3-4 | 8 | Urban Combat | + Domination, CTF | Test objective nodes in 200-bunker field |
| **3** | 5 | 8 | Military Base | + Frontline, Data Heist | Full system, charging rack, ref training |
| **4** | 6+ | 16+ | All fields | All Tier 0-2 modes | Scale to full rental fleet |

### Blitz-Specific Config

See `fields/blitz_dacono/config.json` for:
- Per-field AP placement coordinates
- Per-field path loss calibration targets
- Recommended modes per field

### Pricing for Blitz

- **Rental add-on**: $8/player/session
- **Band BOM v1.0**: $12.40 (pilot)
- **Band BOM v1.1**: $19.70 (production with IMU + shock sensor)
- **Payback**: 2 rentals at $8
- **Target margin**: 60% after band cost recovered

### Staff Training

- **2 refs minimum** for pilot
- **1-page laminated SOP** attached to charging rack
- **Self-test on boot** — staff knows in 2 seconds if band is dead

---

## Secondary Deployments (Pipeline)

| Field | Location | Status | Notes |
|-------|----------|--------|-------|
| TBD | Denver metro | Phase 2 | After Blitz proven |
| TBD | Colorado Springs | Phase 3 | Need local partner |
| TBD | National | Phase 4 | White-label licensing |

---

## Contractor Info

**Christopher Ortega**  
- Email: denverchrisortega@gmail.com
- GitHub: github.com/toxicwind
- Portfolio: resume.effusionlabs.com
- Specialization: LLM infrastructure, embedded systems, real-time positioning

### Engagement Model

| Service | Deliverable | Timeline | Rate |
|---------|-------------|----------|------|
| Field pilot setup | Full deploy at your field | 2-4 weeks | Flat fee + hardware |
| Custom firmware | New game modes, hardware variants | 1-2 weeks | $150/hr |
| Server backend | FastAPI + WebSocket + analytics | 1-2 weeks | $125/hr |
| Hardware design | PCB, case, BOM optimization | 2-4 weeks | Project-based |
| Training | Staff SOP, ref training, troubleshooting | 1 day | Flat fee |

---

## Development Notes

### Branch Strategy

- `main` — stable, public-facing
- `blitz-pilot` — Blitz-specific tweaks, calibration data
- `v1.1-hardware` — IMU + shock sensor development
- `feature/*` — New game modes, experimental

### Secrets Management

- No API keys in repo
- Drive9 mount for persistent state: `/mnt/agents/output/`
- GitHub PAT stored in `.env` (gitignored)
- Field configs contain no PII

### Testing

- `tests/perl/` — Perl-based hardware simulation and validation
- `tests/python/` — Server unit tests, integration tests
- `tests/simulation/` — Full match simulation without hardware

---

## License

Same as public repo: MIT. This document is also MIT — share with collaborators freely.
