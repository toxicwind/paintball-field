# AP Node Build Guide

## Overview

AP nodes are the anchor points for positioning. You need 6 per field. Assembly time: ~20 minutes each. Cost: ~$24 each.

## Assembly

1. Flash ESP32-C3-DevKitM-1 with `firmware/ap_node/src/main.cpp`
2. Set SSID to `SPECTRE-AP-01` through `SPECTRE-AP-06`
3. Lock channel: 1, 6, 11, 1, 6, 11 (no overlap)
4. Mount in IP65 enclosure with pole clamp
5. Height: 2.5 meters, facing downward
6. Power: 12V PoE splitter preferred, or 5V 3A USB adapter in waterproof bag

## Field Placement

See `fields/blitz_dacono/config.json` for exact coordinates per field.

## Mounting Diagram

```
        2.5m height
           |
    [AP-01]-----[AP-02]-----[AP-03]
       |                       |
       |      FIELD CENTER     |
       |                       |
    [AP-04]-----[AP-05]-----[AP-06]
           |
        2.5m height
```

All APs face DOWNWARD to reduce ground bounce multipath.
