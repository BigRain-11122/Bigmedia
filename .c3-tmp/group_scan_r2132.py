# -*- coding: utf-8 -*-
"""Quick group-scan: decisions.md D/C token set-diff vs state watermark + ledger @BigStream lines."""
import io, json, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
STATE = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json"

def read(p):
    with io.open(p, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

state = json.loads(io.open(STATE, "r", encoding="utf-8-sig").read())
known = set(state.get("decisions_watermark", {}).get("dnums", []))

dec = read(ROOT + r"\docs\decisions.md")
tokens = set(re.findall(r"\b([DC]-\d{8}-\d{2})\b", dec))
new_dc = sorted(tokens - known)
print("decisions tokens=%d known=%d new=%s" % (len(tokens), len(known), new_dc if new_dc else "NONE"))

led = read(ROOT + r"\cph4\evolution-ledger.md")
pat = re.compile(r"@(BigStream|七线全司|全司|六司)")
lines = [ln.strip() for ln in led.splitlines() if pat.search(ln)]
print("ledger @match lines=%d" % len(lines))
for ln in lines[-6:]:
    print("  " + ln[:120])

# own orders anchor check
import os
od = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\orders"
latest = max(os.listdir(od), key=lambda n: os.path.getmtime(os.path.join(od, n)))
print("own-orders latest=%s" % latest)
