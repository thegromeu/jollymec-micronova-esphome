# Jolly-Mec GLOBE pellet stove → Home Assistant, locally (ESPHome + Micronova)

Local Home Assistant control of a **Jolly-Mec GLOBE 10 kW** pellet stove
(Micronova board) with ESPHome, after the vendor cloud shut down. Built on
[philibertc's Micronova Controller](https://github.com/philibertc/micronova_controller)
board and ESPHome's [`micronova`](https://esphome.io/components/micronova/)
component.

This repo adds what is specific to this stove: a working ESPHome config, the
memory map found by scanning, a read-only memory scanner and the method to find
the addresses of your own stove.

## Why

The E-FESTO online service that drove this stove closed on 30 June 2023. The
original WiFi module only talks to that defunct server. It stays in place, and
a small add-on talks directly to the stove's Micronova board, with no Internet
and no subscription.

## What works

| Feature | Home Assistant entity | State |
|---|---|---|
| Room temperature, fumes temperature | sensors | ✅ |
| Actual flame power | sensor | ✅ |
| Readable status (ignition, running, cleaning…) | text sensor | ✅ |
| Temperature setpoint (0.5 °C steps) | number | ✅ |
| Requested power 1 to 5, Silent mode | number + button | ✅ |
| Fumes extractor speed | sensor (diagnostic) | ✅ |
| Ducted fan V2: speed, temperature, Manual/Auto mode, off | numbers + buttons | ✅ |
| On / off | switch | ✅ ([test](docs/on-off-test.md)) |

## Hardware

- philibertc's **Micronova Controller** board (rev 1.5), with optocouplers —
  [project](https://github.com/philibertc/micronova_controller),
  [PCB](https://github.com/philibertc/micronova_controller_pcb)
- **WeMos D1 Mini** (ESP8266)
- Step-down module to **5 V USB**, powered from the stove's 20 V
- A **Molex KK 2.54 mm 4-pin** plug for the mainboard's "SERIALE" connector

Details, the rear-port trap and the power budget: [docs/wiring.md](docs/wiring.md).

## Contents

| File | Role |
|---|---|
| [`esphome/pellet-stove.yaml`](esphome/pellet-stove.yaml) | Full ESPHome configuration |
| [`esphome/scanner.yaml`](esphome/scanner.yaml) | Memory scan, read only |
| [`esphome/secrets.example.yaml`](esphome/secrets.example.yaml) | `secrets.yaml` template |
| [`docs/memory-map.md`](docs/memory-map.md) | RAM/EEPROM addresses and status codes of this stove |
| [`docs/scanning-method.md`](docs/scanning-method.md) | Finding the addresses of your own stove |
| [`docs/wiring.md`](docs/wiring.md) | Connector, wiring, power |
| [`docs/on-off-test.md`](docs/on-off-test.md) | On/off switch test and results |
| [`tools/diff_scans.py`](tools/diff_scans.py) | Compares two scans |

## Key points

- **ESPHome's default addresses do not fit this stove**: fumes temperature at
  `0x5C`, status with running = 7 and final cleaning = 9. On another
  Micronova stove, scan before writing.
- **The 4-pin port at the back of the GLOBE is not the serial bus.** The right
  one is "SERIALE" on the mainboard.
- Only **user settings** are written (setpoint, power, fans), and by hand.
  Never factory parameters.

## Disclaimer

Personal project, not affiliated with Jolly-Mec or Micronova. Opening the
stove and writing to its memory is at your own risk: 230 V inside, and a wrong
value can upset combustion. Check your warranty and insurance.

## Credits

- Interface board, guide and original ESPHome work:
  **philibertc** — [micronova_controller](https://github.com/philibertc/micronova_controller)
  ([PCB](https://github.com/philibertc/micronova_controller_pcb))
- ESPHome [`micronova` component](https://esphome.io/components/micronova/)

License: MIT.
