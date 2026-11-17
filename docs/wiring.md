# Wiring

> ⚠️ The inside of the stove carries 230 V. Only open it **unplugged**.
> The serial connector carries 20 V and 5 V: a wire in the wrong place can
> destroy the interface board or the stove's board. **Measure before
> connecting.**

## Hardware

| Part | Role |
|---|---|
| philibertc's **Micronova Controller** board (rev 1.5) — [repo](https://github.com/philibertc/micronova_controller), [PCB](https://github.com/philibertc/micronova_controller_pcb) | PC817 optocouplers: level shifting and isolation between the stove and the ESP. ESPHome's `micronova` component requires this kind of circuit |
| **WeMos D1 Mini** (ESP8266) | Plugged onto the purple board. Runs ESPHome |
| **5 V USB-output step-down module**, input ≥ 30 V | Powers the D1 Mini from the stove's 20 V |
| **Molex KK 2.54 mm 4-pin** plug (or 4 female Dupont wires) | Clips onto the stove's connector |

D1 Mini pins used: **D4 = TX**, **D3 = RX** (pull-up),
**D2 = receive-enable** of the philibertc board.

## The right connector

On this GLOBE, the 4-pin port **visible at the back of the stove is not the
serial bus**: connected there, ESPHome only gets `Timeout`s. It seems to be
linked to the white "ENC.COC." connector on the mainboard.

The right port is the **black 4-pin connector labelled "SERIALE"** on the
**mainboard**, just below the white "ENC.COC." connector and below the ribbon
cable going to the display. This is where the official WiFi module plugs in.
Access: side panel, stove unplugged.

Pin order (to **confirm with a multimeter** on your board):

```
GND  ·  Serial  ·  20 V  ·  5 V
```

On our board, mounted vertically, GND is at the top, on the white-connector
side.

Measurement, stove powered but off, at the end of the wires (never probes on
the pins): black probe on the pin at one end; moving away you should read
**≈ 5 V, ≈ 20 V, ≈ 5 V**. Otherwise, start again from the other end. If
neither direction gives this sequence: **stop**.

## Connections

```
SERIALE CONNECTOR               DESTINATION
GND    ────────────────────────→ board · "From heater" GND ─┐
                    step-down module · input (−) ───────────┘ same screw
Serial ────────────────────────→ board · "From heater" Serial
20 V   ────────────────────────→ step-down module · input (+)
5 V    ────────────────────────→ board · "From heater" 5V

module · USB 5 V output ─ cable ─→ D1 Mini (USB)
board · "Power in": empty
```

- The connector's **5 V does not power the ESP**: it only feeds the receive
  optocoupler (a few mA).
- The module's **(−) goes to the stove ground** ("From heater" GND), not to
  "Power in", which is on the ESP side, isolated by the optocouplers.
- The cable leaves through an existing opening, away from the transformer, hot
  parts and 230 V terminals, held by a cable tie.

## Power budget

The mainboard transformer is rated **12 V ~ 5.8 VA**. The "20 V" is this 12 V
AC, rectified. The D1 Mini draws ~0.5 W on average and up to ~2 W during WiFi
peaks: a significant share of this small transformer. It works here, but keep
an eye on the stove during the first days. If the display flickers or the
stove restarts, power the D1 Mini from a wall USB charger and keep only GND,
Serial and 5 V.

## First flash

The first flash is done over USB, with the D1 Mini **removed** from the purple
board, for example with [web.esphome.io](https://web.esphome.io) (WebSerial
needs an HTTPS page). Later updates go over WiFi.
