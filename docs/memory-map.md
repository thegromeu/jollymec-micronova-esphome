# Memory map — Jolly-Mec GLOBE 10 kW (Micronova board)

Found by scanning (see [scanning-method.md](scanning-method.md)), then
confirmed by changing the setting on the remote or from Home Assistant.
**They are specific to this stove**: ESPHome's defaults were wrong for the
fumes temperature and for the status. On another stove, check before writing
anything.

Micronova protocol reminder: reads use `0x00` (RAM) or `0x20` (EEPROM)
followed by the address. Writes use `0x80` / `0xA0`: ESPHome adds that bit
itself, so you always declare `memory_location: 0x00` or `0x20`.

## RAM (`memory_location: 0x00`) — live values

| Address | Content | Confidence |
|---|---|---|
| `0x01` | Room temperature, raw value ÷ 2 | ✅ confirmed |
| `0x04` | Speed applied to ducted fan V2 (0 to 5) | ✅ confirmed |
| `0x21` | **Status** (codes below). Also the address of the on/off command | ✅ confirmed |
| `0x34` | Actual flame power (1 to 5), modulated by the thermostat | ✅ confirmed |
| `0x36` | Fumes extractor speed setpoint (round values: 70, 80, 110…) | ✅ confirmed |
| `0x37` | Measured extractor speed (follows `0x36` within ±2) | ✅ confirmed |
| `0x5C` | Fumes temperature, °C | ✅ confirmed |
| `0x60` | Internal sawtooth counter (~60 → ~120) | ❓ not a fan |
| `0x7A`, `0x7B` | ≈ 92 to 107 while running, 0 when off; do not react to V2 | ❓ unknown |

Extractor speed (`0x36`) by phase, recorded over one cycle:

| Phase | Extractor |
|---|---|
| Ignition (status 5) | 185 |
| Stabilisation (status 6) | 155 |
| Flame 4 | 125 |
| Flame 3 | 110 |
| Flame 2 | 80 |
| Flame 1 | 70 |
| Brazier cleaning (status 8) | 225 |
| Final cleaning (status 9) | ~225 for ~8 min, then ~111 |

When the room reaches the setpoint, the stove drops to flame 1 whatever the
requested power.

## Status codes (RAM `0x21`)

Different from ESPHome's default table: here normal running is 7 and final
cleaning is 9.

| Code | State | Confidence |
|---|---|---|
| 0 | Off | ✅ |
| 1 | Starting | ✅ |
| 2 | Pre-ignition (a few seconds right after switching on, extractor at 0) | ✅ |
| 3 | Ignition | ✅ |
| 5 | Ignition, phase 2 (extractor at 185) | 🟡 |
| 6 | Stabilisation (extractor at 155) | 🟡 |
| 7 | Running | ✅ |
| 8 | Periodic brazier cleaning (extractor at 225 for ~1 min) | ✅ happened unattended |
| 9 | Final cleaning (shown on the remote, ~50 min) | ✅ |

Code 4 and the alarm codes have not been observed yet.

## EEPROM (`memory_location: 0x20`) — settings

### User settings (safe to write, by hand)

| Address | Content | Values |
|---|---|---|
| `0x6B` | Room temperature setpoint | half-degrees: 40 = 20.0 °C |
| `0xD0` | Requested power | 0 = Silent, 1 to 5 |
| `0xCD` | V2 (ducted fan): target temperature | half-degrees |
| `0xCE` | V2: mode | 0 = Manual, 2 = Auto (1 = Semi-auto, not verified) |
| `0xCF` | V2: speed | 0 = OFF, 1 to 5 |
| `0xD1`, `0xD2`, `0xD3` | Probably V3: mode, speed, temperature | not verified (no V3 duct here) |

EEPROM supports a limited number of writes: no automation that rewrites it
every few minutes.

### Factory parameters (read only — **never write**)

| Addresses | Values | Interpretation |
|---|---|---|
| `0x0D`–`0x10` | 185, 185, 155, 225 | Extractor speeds per phase (ignition, stabilisation, brazier cleaning) |
| `0x28`–`0x2D` | 70, 80, 110, 125, 136, 165 | Extractor speeds per flame level |
| `0x22`–`0x25` | 105, 133, 153, 190 | Unknown |
| `0xDA`–`0xDF` | 30, 32, 36, 39, 47, 50 | Unknown |
| `0x58`–`0x61` | 20, 22, 24, 26, 28 (twice) | Unknown |
| `0x7D` | 144 | Unknown. An accidental write (20) went back to 144 by itself |
| `0xFA` | changes by itself | Counter |

A wrong value in these parameters can upset combustion.
