# Finding your stove's addresses

Micronova addresses change from one manufacturer and board to another. Rather
than guessing: read the whole memory, change **a single** setting, read again,
and compare.

## 1. Install the scanner

Flash [`esphome/scanner.yaml`](../esphome/scanner.yaml) instead of the normal
configuration. It only sends read commands. While it is installed, the usual
entities disappear from Home Assistant.

## 2. Record two states

| | Example |
|---|---|
| Setting A | setpoint 20.0 °C, power 1 |
| Setting B | setpoint 23.5 °C, power 4 |

For each setting:
1. set it on the remote, wait 1 to 2 minutes;
2. press **Scan EEPROM**, wait for `=== END ===`;
3. press **Scan RAM**, wait for `=== END ===`;
4. copy the logs to a file (`A.txt`, `B.txt`).

Never start a scan before the previous one has finished.

Pick **easy-to-recognise** values: 23.5 °C gives 47 in half-degrees, which is
hard to mistake for anything else.

## 3. Compare

```bash
python3 tools/diff_scans.py A.txt B.txt
```

- In **EEPROM**, only the addresses of the changed setting move (plus,
  sometimes, an internal counter). That is where the settings live.
- In **RAM**, many values move by themselves (temperatures, counters). Look for
  the value that follows the setting, for example 1 → 5.

## 4. Confirm

Add the address you found as a `memory_address_sensor` (read only) in the
normal configuration, and check that it follows the remote during a full
cycle. Only then write to it, and only to **user settings**, never to factory
parameters.
