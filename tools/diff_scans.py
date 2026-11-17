#!/usr/bin/env python3
"""Compare scan logs produced by esphome/scanner.yaml.

Usage: python3 tools/diff_scans.py A.txt B.txt [C.txt ...]

Each file contains lines such as "RAM 0x21 = 7" or "EEPROM 0x6B = 40"
(plain text, or an RTF copy of the ESPHome logs). Prints the addresses whose
value differs between at least two files.
"""
import re
import sys
from pathlib import Path

LINE = re.compile(r"(EEPROM|RAM) 0x([0-9A-F]{2}) = (\d+)")


def load(path):
    data = {}
    text = Path(path).read_text(encoding="latin-1")
    for zone, addr, value in LINE.findall(text):
        data.setdefault(zone, {})[int(addr, 16)] = int(value)
    return data


def main(paths):
    if len(paths) < 2:
        sys.exit(__doc__)
    scans = [load(p) for p in paths]
    names = [Path(p).stem for p in paths]
    for zone in ("EEPROM", "RAM"):
        print(f"=== {zone}  ({' / '.join(names)})")
        addrs = sorted(set().union(*(s.get(zone, {}).keys() for s in scans)))
        for a in addrs:
            vals = [s.get(zone, {}).get(a) for s in scans]
            known = {v for v in vals if v is not None}
            if len(known) > 1:
                shown = " / ".join("-" if v is None else str(v) for v in vals)
                print(f"0x{a:02X}  {shown}")


if __name__ == "__main__":
    main(sys.argv[1:])
