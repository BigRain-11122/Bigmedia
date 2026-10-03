# R1067 round fresh five-check scan (fast-path). Direct read-only per D-20261001-03 (host machine).
# Output -> .c3-tmp/r1067_check.txt (UTF-8 file, not console; GBK console rule).
import json, re, datetime
from pathlib import Path

ROOT = Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream")
HQ = Path(r"C:\Users\sjs20\Desktop\FluxGroup")
out = []
p = out.append

now = datetime.datetime.now()
p(f"[scan time] {now.strftime('%Y-%m-%d %H:%M:%S')} (day-boundary target = 2026-10-04 00:00)")

# 1. orders top
files = sorted((ROOT / "orders").glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
top = files[0]
p(f"1. orders top = {top.name} (mtime {datetime.datetime.fromtimestamp(top.stat().st_mtime)})")

# 2. evolution-ledger @target lines (strict @ prefix four/six-company modes)
ledger = HQ / "cph4" / "evolution-ledger.md"
txt = ledger.read_text(encoding="utf-8", errors="replace")
pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线)")
hits = [ln for ln in txt.splitlines() if pat.search(ln)]
p(f"2. ledger @target lines = {len(hits)} (frozen baseline 41, R1050 PS-count note in case)")
if len(hits) > 41:
    for ln in hits[41:]:
        p("   NEW ROW: " + ln.strip()[:200])
p(f"   ledger mtime = {datetime.datetime.fromtimestamp(ledger.stat().st_mtime)}")

# 3. decisions.md dnum content-addressed diff vs watermark
dec = HQ / "docs" / "decisions.md"
dtxt = dec.read_text(encoding="utf-8", errors="replace")
dnums_file = set(re.findall(r"[DC]-\d{8}-\d{2}", dtxt))
state = json.loads((ROOT / "src" / "os" / "state.json").read_text(encoding="utf-8"))
wm = set(state["decisions_watermark"]["dnums"])
new = sorted(dnums_file - wm)
p(f"3. decisions dnum diff: NEW_DNUMS={new} (watermark {len(wm)} / file {len(dnums_file)})")
p(f"   decisions.md mtime = {datetime.datetime.fromtimestamp(dec.stat().st_mtime)}")
m = re.search(r"派工通告板(.*?)(?:\n#{1,3} |\Z)", dtxt, re.S)
board = m.group(1) if m else ""
brows = [ln.strip() for ln in board.splitlines() if re.search(r"BigStream|七司", ln)]
p(f"   board BigStream/七司 rows = {len(brows)} (collected set = D-20261003-01~04 per R1031)")
for ln in brows:
    p("   BOARD: " + ln[:180])

# 4. lock + production + tree self-accounting state
p(f"4. index.lock exists = {(ROOT / '.git' / 'index.lock').exists()}")
p(f"   production = {state.get('production')} (self-heal: open required per D-BS-06)")
p(f"   tick = {state.get('tick')} / last ts = {state.get('ts')}")

# 5. day-boundary routine gates
p(f"5. intel brief 10-03 exists = {(ROOT / 'data/intel/daily/2026-10-03.md').exists()}"
  f" / 10-04 exists = {(ROOT / 'data/intel/daily/2026-10-04.md').exists()} (day-boundary item)")
w40 = (ROOT / "docs/audits/2026-W40-self-audit.md").exists()
p(f"   W40 weekly self-audit exists = {w40}")
gb = (ROOT / "docs/global-benchmarks.md").read_text(encoding="utf-8", errors="replace")
mm = re.search(r"2026-\d{2}-\d{2}", gb)
p(f"   global-benchmarks latest date mark = {mm.group(0) if mm else 'NONE'} (gate due 10-08)")

# 6. export freshness
raw = (ROOT / "docs/status-export.json").read_text(encoding="utf-8", errors="replace")
em = re.search(r'"export_ts"\s*:\s*"([^"]+)"', raw)
p(f"6. status-export export_ts = {em.group(1) if em else 'NONE'} (refresh only if live change or >24h)")

# 7. backlog top (first item headers)
bl = (ROOT / "src/os/backlog.md").read_text(encoding="utf-8", errors="replace")
p("7. backlog top items (first ~10 header lines):")
cnt = 0
for ln in bl.splitlines():
    if re.match(r"^#{1,4}\s*#?\d+", ln.strip()) or re.match(r"^-\s*\[#\d+", ln.strip()):
        p("   " + ln.strip()[:160])
        cnt += 1
        if cnt >= 10:
            break
if cnt == 0:
    for ln in [l for l in bl.splitlines() if l.strip()][:12]:
        p("   | " + ln.strip()[:150])

(ROOT / ".c3-tmp/r1067_check.txt").write_text("\n".join(out), encoding="utf-8")
print("WROTE", len(out), "lines")

