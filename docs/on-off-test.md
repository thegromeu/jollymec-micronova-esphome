# On/off switch test

Status: **validated** on 2026-11-16 (switching on and off). The switch writes
to RAM `0x21`, the status address.

## Why not ESPHome's default values

The `micronova` component sends `0x01` to switch on and `0x06` to switch off.
On this stove, 6 is the **stabilisation** phase of ignition, and final
cleaning is **9**. So `0x09` is sent to switch off.

Safeguards in the ESPHome component (source `micronova_switch.cpp`):
- "on" is sent **only when the status is 0** (off);
- "off" is not sent when the status is 0 or 6. Here it is therefore refused
  during stabilisation, which is harmless;
- the switch shows "on" for **any status other than 0**, final cleaning
  included.

`restore_mode: DISABLED` prevents any command when the ESP reboots.

## Procedure (in front of the stove, remote in hand)

1. **Stove off and cold**, status "Off", brazier clean.
2. **Switch on** from Home Assistant. Expected: status 1 or 2, then 3, and the
   remote shows ignition.
3. Let it reach **Running** (status 7).
4. **Switch off** from Home Assistant. Expected: status 9, "Final cleaning" on
   the remote, then 0.

**Emergency stop**: if anything unexpected happens (unknown code, alarm, odd
display), switch off **with the remote** and look at the logs.

## Results

| Step | Result |
|---|---|
| On `0x01` | ✅ 2026-11-16, cold stove. Written at 14:37, status 2 → 3 (extractor 93) → 5 at 14:39 (185) → 6 at 14:42 → 7 before 14:51. No alarm |
| Off `0x09` | ✅ 2026-11-16, while running. Written at 17:34, status 9 immediately. Extractor ~225 for ~8 min, then ~111. Fumes 87 → 100 °C, then cooling down. V2 stops around 17:57. Status 0 at 18:25 (≈ 52 min), switch back to "off". No alarm |

## Good to know

- **Final cleaning lasts about 50 minutes.** The switch stays "on" during all
  that time: this is normal. Watch the **Status** sensor to know when the
  stove is really off.
- Switching on again is only accepted once the status is back to 0.
