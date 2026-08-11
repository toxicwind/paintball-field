# Charging Rack Build Guide

## Overview

16-slot charging rack for SpectreBands. One PSU powers all slots. Cost: ~$52.

## Parts

| Part | Qty | Notes |
|------|-----|-------|
| 3D printed frame | 1 | PETG, 2 perimeters, 20% infill |
| Pogo pins (2.54mm) | 16x4 | Gold plated, spring loaded |
| Mean Well LRS-150-5 | 1 | 5V 30A, powers 16 bands |
| TP4056 modules | 16 | Per-cell charging control |
| Bicolor LEDs | 16 | Green = full, Red = charging |
| Bus bar PCB | 1 | Fused distribution |

## Assembly

1. Print frame (8 hours on Prusa MK4)
2. Press pogo pins into frame holes
3. Solder TP4056 modules to bus bar
4. Wire LEDs to TP4056 status pins
5. Connect Mean Well PSU to bus bar
6. Test each slot with multimeter

## Usage

1. Place band in slot — pogo pins contact charging pads
2. LED turns RED = charging
3. LED turns GREEN = full (~2 hours for 600mAh)
4. Remove band, give to player

## Safety

- Each slot has its own TP4056 = no cascade failure
- Fused bus bar prevents short circuits
- Fan cooling for 16 simultaneous charges
