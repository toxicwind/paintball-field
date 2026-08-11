# SpectreBand v1.1 Build Guide

## Overview

This guide walks you through building a SpectreBand v1.1 from scratch. Assembly time: ~45 minutes per band. Cost: ~$19.70 in parts.

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

1. Order PCBs from JLCPCB using `hardware/band_v1.1/gerbers.zip`
   - 2-layer, 1.6mm, HASL, any color
   - 5 pieces = ~$7 shipped
2. Clean PCB with isopropyl alcohol
3. Apply solder paste to pads using stencil or syringe

### Step 2: SMD Placement (15 min)

Place components in this order (smallest to largest):

1. **0402 passives** (resistors, capacitors) — use tweezers
2. **MCP73831T** charging IC — orientation matters, dot = pin 1
3. **USB-C connector** — align with PCB edge
4. **ESP32-C3-MINI-1** — align antenna with PCB edge
5. **BMI270 IMU** — dot = pin 1, align with silkscreen
6. **SH1106 OLED** — solder header pins, do not solder display yet
7. **WS2812B LEDs** — orientation matters, pin 1 marked on PCB
8. **Piezo shock sensor** — solder wires, not SMD

### Step 3: Reflow Soldering (10 min)

1. Preheat hot plate to 150C for 60 seconds
2. Ramp to 220C over 90 seconds
3. Hold at 220C for 60 seconds
4. Cool naturally — do not blast with air
5. Inspect with magnifying glass for bridges

### Step 4: Through-Hole Components (5 min)

1. Solder piezo shock sensor wires to PIEZO_PIN (GPIO 13)
2. Solder haptic motor wires to HAPTIC_PIN (GPIO 11)
3. Solder battery connector (JST-PH 2.0)
4. Attach silicone strap loops

### Step 5: Battery Installation (5 min)

1. Connect 2x 300mAh hard pouch LiPo batteries in parallel
2. Insert into steel shield + DW5812 protection PCB
3. Slide into case bottom
4. Connect to JST-PH connector

### Step 6: Case Assembly (5 min)

1. Place PCB into polycarbonate case top
2. Align OLED window with display
3. Press TPU gasket into groove
4. Snap case halves together
5. Thread 20mm silicone strap through loops

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
| Shock sensor always triggered | Sensitivity too high | Add 10k resistor in series |

## Safety Notes

- **LiPo batteries can catch fire if punctured**. The steel shield + DW5812 protection is mandatory for paintball use. A 300fps direct hit can puncture an unprotected pouch.
- **Do not charge unattended**. Use the charging rack, not random USB chargers.
- **IP54 rating** means splash-resistant, not waterproof. Do not submerge.
