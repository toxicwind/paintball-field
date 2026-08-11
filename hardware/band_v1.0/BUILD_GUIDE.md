# SpectreBand v1.0 Build Guide

## Overview

This guide walks you through building a SpectreBand v1.0 from scratch. Assembly time: ~45 minutes per band. Cost: ~$12.40 in parts.

## Tools Required

| Tool | Purpose | Alternative |
|------|---------|-------------|
| Hot plate or reflow oven | SMD soldering | Soldering iron with fine tip (slower) |
| Tweezers | Placing 0402 components | Precision tweezers |
| USB-C cable | Power + firmware flash | Any USB-C data cable |
| Computer with PlatformIO | Firmware compilation | Arduino IDE (not recommended) |
| 3D printer | Case printing | Send to JLCPCB/JLC3DP |
| Multimeter | Continuity + voltage checks | Essential |

## Step-by-Step Assembly

### Step 1: PCB Preparation (5 min)

1. Order PCBs from JLCPCB using gerbers (see `hardware/band_v1.0/gerbers/`)
   - 2-layer, 1.6mm, HASL, any color
   - 5 pieces = ~$7 shipped (JLCPCB new customer deal)
2. Clean PCB with isopropyl alcohol
3. Apply solder paste to pads using stencil or syringe

### Step 2: SMD Placement (15 min)

Place components in this order (smallest to largest):

1. **0402 passives** (resistors, capacitors) — use tweezers
2. **MCP73831T** charging IC — orientation matters, dot = pin 1
3. **USB-C connector** — align with PCB edge
4. **ESP32-C3-MINI-1** — align antenna with PCB edge (LCSC C2935306)
5. **DRV2605L** — dot = pin 1, align with silkscreen (LCSC C527464)
6. **SSD1306 OLED** — solder header pins, do not solder display yet (LCSC C2890361)
7. **WS2812B LEDs** — orientation matters, pin 1 marked on PCB (LCSC C114581)
8. **10mm ERM motor** — solder wires, not SMD (LCSC C2894691)

### Step 3: Reflow Soldering (10 min)

1. Preheat hot plate to 150C for 60 seconds
2. Ramp to 220C over 90 seconds
3. Hold at 220C for 60 seconds
4. Cool naturally — do not blast with air
5. Inspect with magnifying glass for bridges

### Step 4: Through-Hole Components (5 min)

1. Solder ERM motor wires to HAPTIC_PIN (GPIO 11)
2. Solder battery connector (JST-PH 2.0)
3. Attach NATO strap loops

### Step 5: Battery Installation (5 min)

1. Connect 502535 500mAh LiPo battery
2. Slide into case bottom
3. Connect to JST-PH connector

### Step 6: Case Assembly (5 min)

1. Place PCB into TPU case top
2. Align OLED window with display
3. Snap case halves together
4. Thread 20mm NATO strap through loops

### Step 7: Firmware Flash (2 min)

```bash
cd firmware/band
pio run --target upload --environment esp32c3
```

Hold BOOT button, press RESET, release BOOT. Band will show self-test screen.

### Step 8: Field Test

1. Power on band near field APs
2. Verify "CONNECTED" appears within 10 seconds
3. Verify self-test shows PASS
4. Walk field, verify radar shows approximate position
5. Tap button — should send ping to server

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| OLED blank | Backwards or not seated | Check pin 1 alignment |
| No WiFi | Antenna not connected | ESP32-C3-MINI-1 antenna trace must be intact |
| Self-test FAIL | Bad solder joint | Reflow, check with multimeter |
| Battery not charging | MCP73831T orientation | Rotate 180 degrees |
| Haptic weak | Wrong motor polarity | Swap wires |

## Safety Notes

- **LiPo batteries can catch fire if punctured**. Do not use in paintball without protective case.
- **Do not charge unattended**. Use the charging rack.
- **TPU case is not IP rated**. Keep bands dry.
