# -*- coding: utf-8 -*-
"""R771 five-check content-addressed scan (r750_scan equivalent, D-20260930-19 watermark diff)."""
import io, json, re, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
LEDGER = r"C:\Users\sjs20\Desktop\FluxGroup\cph4\evolution-ledger.md"
DECISIONS = r"C:\Users\sjs20\Desktop\FluxGroup\docs\decisions.md"
STATE = ROOT + r"\src\os\state.json"

out = io.StringIO()

# 1) ledger six-mode scan (CaseSensitive, strict @ prefix)
patterns = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线", "@八线全量"]
hits = 0
last_p = None
with io.open(LEDGER, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        if any(p in line for p in patterns):
            hits += 1
            m = re.search(r"P-2026\d\d\d\d-\d\d", line)
            if m:
                last_p = m.group(0)
out.write("ledger_six_mode_hits=%d last_p=%s\n" % (hits, last_p))

# 2) decisions dnum set diff vs state watermark
dn = re.compile(r"\b([DC])-(2026\d{4})-(\d{2})\b")
cur = set()
with io.open(DECISIONS, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        for m in dn.finditer(line):
            cur.add("%s-%s-%s" % (m.group(1), m.group(2), m.group(3)))
with io.open(STATE, "r", encoding="utf-8") as f:
    st = json.load(f)
base = set(st["decisions_watermark"]["dnums"])
new = sorted(cur - base)
out.write("decisions_dnum_total=%d baseline=%d new_rows=%s\n" % (len(cur), len(base), new if new else "NONE"))
out.write("production=%s tick=%d\n" % (st.get("production"), st.get("tick")))

# 3) GB gate: global-benchmarks sec-4 first-line date age (do not touch file)
gb = ROOT + r"\docs\global-benchmarks.md"
first_date = None
with io.open(gb, "r", encoding="utf-8", errors="replace") as f:
    txt = f.read()
m = re.search(r"2026-09-2\d|2026-10-0\d", txt[:4000])
if m:
    first_date = m.group(0)
out.write("gb_head_date_probe=%s (7-day gate: due 10-01, today 09-30 = day6)\n" % first_date)

sys.stdout.buffer.write(out.getvalue().encode("utf-8"))
