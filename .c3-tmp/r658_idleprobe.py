import io, json, re
from datetime import date

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
st = json.load(io.open(ROOT + r"\src\os\state.json", encoding="utf-8"))
LOG_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(.*)$")
ROUND_RE = re.compile(r"^R\d+\b")
since, until = date(2026, 9, 28), date(2026, 10, 4)
rows = []
for e in st.get("log", []):
    m = LOG_RE.match(e.strip())
    if not m:
        continue
    d = date.fromisoformat(m.group(1))
    if not (since <= d <= until):
        continue
    rest = m.group(2).strip()
    parts = rest.split(None, 1)
    tail = parts[1].strip() if len(parts) == 2 else ""
    if ROUND_RE.match(tail):
        rows.append(tail)
idle_rows = [t for t in rows if "idle" in t.lower()]
titled = [t for t in idle_rows if re.match(r"^R\d+\s*[:\uff1a]?\s*declared-idle", t)]
print("rounds=", len(rows), "idle_match=", len(idle_rows), "titled_declared=", len(titled))
false_pos = [t for t in idle_rows if t not in titled]
print("false_pos_n=", len(false_pos))
for t in false_pos[:12]:
    print("FP>>", t[:110])
