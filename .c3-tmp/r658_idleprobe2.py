import io, json, re
from datetime import date

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
st = json.load(io.open(ROOT + r"\src\os\state.json", encoding="utf-8"))
LOG_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(.*)$")
ROUND_RE = re.compile(r"^R\d+\b")
# title-position idle declaration: covers both regimes
IDLE_TITLE_RE = re.compile(
    r"^R\d+(?:\+R?\d+)*\s*(?:[:\uff1a]\s*)?(?:\u65ad\u6d1e\u53cc\u8bb0\+)?(declared-)?idle",
    re.IGNORECASE)
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
sub = [t for t in rows if "idle" in t.lower()]
titled = [t for t in sub if IDLE_TITLE_RE.match(t)]
fps = [t for t in sub if not IDLE_TITLE_RE.match(t)]
out = []
out.append("rounds=%d idle_substring=%d idle_titled=%d false_pos=%d"
           % (len(rows), len(sub), len(titled), len(fps)))
out.append("--- titled sample ---")
for t in titled[:6]:
    out.append("T>> " + t[:80])
out.append("--- false positives (full list) ---")
for t in fps:
    out.append("FP>> " + t[:130])
io.open(ROOT + r"\.c3-tmp\r658_idleprobe2.txt", "w", encoding="utf-8").write("\n".join(out))
print("done")
