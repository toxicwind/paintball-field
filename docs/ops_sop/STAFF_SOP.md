# SPECTREBAND STAFF SOP — 1-PAGE LAMINATED CARD

## DAILY SETUP (5 minutes)

1. **Power on field router** — wait 30s for WiFi
2. **Power on 6 AP nodes** — green LED = good, red = check power
3. **Power on server** (Raspberry Pi) — wait for "Server Ready" on display
4. **Test 1 band** — power on, verify "CONNECTED" within 10s
5. **Place bands in charging rack** — green = full, red = charging

## PLAYER CHECK-IN (1 minute per player)

1. **Hand band to player** — "Strap it on your non-trigger wrist"
2. **Team select** — player holds button 2s for red, 4s for blue
3. **Self-test** — band shows PASS or FAIL. FAIL = swap band.
4. **Quick demo** — "Glance at your wrist to see teammates. Green dots = friends."
5. **Rules** — "When you get hit, press the button once. Go to checkpoint. Wait for buzz."

## STARTING A MATCH (30 seconds)

1. **Open command station** — tablet shows live map
2. **Select mode** — Hunter-Prey (beginners) or Domination (experienced)
3. **Count players** — verify all bands show on map
4. **Announce** — "SpectreBand active. Masks on. Game starts in 10 seconds."
5. **Press START** — all bands buzz simultaneously

## DURING THE MATCH

- **Referee tablet shows**: player positions, health, battery levels
- **Force eliminate**: tap player on tablet → "ELIMINATED" → band buzzes long
- **Force revive**: tap player → "REVIVED" → band short buzz
- **Low battery**: tablet shows red battery icon → swap band at next break

## ENDING A MATCH

1. **Press STOP** on tablet — all bands show "MATCH OVER"
2. **Collect bands** — check for damage, wipe paint
3. **Place in charging rack** — verify LEDs turn red
4. **Check server logs** — any disconnects or issues?

## TROUBLESHOOTING

| Problem | Quick Fix |
|---------|-----------|
| Band shows "OFFLINE" | Walk closer to AP. If still offline, swap band. |
| Band not charging | Check pogo pin alignment. Wiggle band in slot. |
| Player says "radar is wrong" | Normal. RSSI accuracy is 2-3m. Tell them to trust their eyes. |
| Band took direct hit | Inspect case. If cracked, retire band for repair. |
| Server crashed | Power cycle Pi. Takes 60s to restart. |
| AP node red LED | Check PoE connection or power adapter. |

## EMERGENCY

- **Band fire/smoke**: Remove from player. Submerge in water bucket.
- **Player injury**: SpectreBand does not interfere with first aid. Remove band if needed.
- **Severe weather**: Power down all electronics. AP nodes are IP65 but not hurricane-proof.

## CONTACT

- **Tech support**: denverchrisortega@gmail.com
- **Urgent**: 303-667-3831 (text preferred)
- **GitHub issues**: github.com/toxicwind/paintball-field/issues

---
**Print this on 8.5x11, laminate, attach to charging rack with zip ties.**
