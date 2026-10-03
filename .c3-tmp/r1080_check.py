# R1076 round fresh five-check scan (fast-path). Direct read-only per D-20261001-03 (host machine).
# Clone of r1075_check.py + #86 content-addressing legs. Output -> .c3-tmp/r1080_check.txt (UTF-8 file).
import json, re, datetime
from pathlib import Path

ROOT = Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream")
HQ = Path(r"C:\Users\sjs20\Desktop\FluxGroup")
LIFE = Path(r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife")
out = []
p = out.append

now = datetime.datetime.now()
p(f"[scan time] {now.strftime('%Y-%m-%d %H:%M:%S')} (day-boundary target = 2026-10-04 00:00)")

files = sorted((ROOT / "orders").glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
top = files[0]
p(f"1. orders top = {top.name} (mtime {datetime.datetime.fromtimestamp(top.stat().st_mtime)})")

ledger = HQ / "cph4" / "evolution-ledger.md"
txt = ledger.read_text(encoding="utf-8", errors="replace")
pat = re.compile(r"@(BigStream|七线全司|全司|六司|八线)")
hits = [ln for ln in txt.splitlines() if pat.search(ln)]
p(f"2. ledger @target lines = {len(hits)} (frozen baseline 41)")
if len(hits) > 41:
    for ln in hits[41:]:
        p("   NEW ROW: " + ln.strip()[:200])
p(f"   ledger mtime = {datetime.datetime.fromtimestamp(ledger.stat().st_mtime)}")

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
p(f"   board BigStream/七司 rows = {len(brows)} (baseline 8, collected set per R1031)")
for ln in brows:
    p("   BOARD: " + ln[:180])

p(f"4. index.lock exists = {(ROOT / '.git' / 'index.lock').exists()}")
p(f"   production = {state.get('production')} (self-heal: open required per D-BS-06)")
p(f"   tick = {state.get('tick')} / last ts = {state.get('ts')}")

p(f"5. intel brief 10-03 exists = {(ROOT / 'data/intel/daily/2026-10-03.md').exists()}"
  f" / 10-04 exists = {(ROOT / 'data/intel/daily/2026-10-04.md').exists()} (day-boundary item)")
w40 = (ROOT / "docs/audits/2026-W40-self-audit.md").exists()
p(f"   W40 weekly self-audit exists = {w40}")
gb = (ROOT / "docs/global-benchmarks.md").read_text(encoding="utf-8", errors="replace")
mm = re.search(r"2026-\d{2}-\d{2}", gb)
p(f"   global-benchmarks latest date mark = {mm.group(0) if mm else 'NONE'} (gate due 10-08)")

raw = (ROOT / "docs/status-export.json").read_text(encoding="utf-8", errors="replace")
em = re.search(r'"export_ts"\s*:\s*"([^"]+)"', raw)
p(f"6. status-export export_ts = {em.group(1) if em else 'NONE'} (refresh only if live change or >24h)")

# --- #86 content-addressing three legs (pools / interchat / CENSUS gate) ---
# R1076 fix per R982 precedent (scan follows BigLife pool restructure):
# BigLife reformatted pools.json at 10-03 09:06 dropping the legacy TOTAL_LINES
# marker comment (content flat 1440, verified r1078_pools_count.txt). Count the
# content itself (JSON parse) instead of the marker; legacy marker kept as fallback.
pj = LIFE / "cognition" / "pools.json"
t = pj.read_text(encoding="utf-8", errors="replace")
pools_n = "?"
try:
    pjdata = json.loads(t)
    tot = 0
    for _ax, buckets in pjdata.get("axes", {}).items():
        if isinstance(buckets, dict):
            tot += sum(len(v) for v in buckets.values() if isinstance(v, list))
    for _bk, v in pjdata.get("sprite", {}).items():
        if isinstance(v, list):
            tot += len(v)
    pools_n = str(tot)
except Exception:
    mw = re.search(r"TOTAL_LINES[^0-9]*(\d+)", t)
    if mw:
        pools_n = mw.group(1)
p(f"7. #86 a-leg pools.json content count = {pools_n} (baseline 1440, content-addressing law, marker-free since 10-03 09:06 reformat)")
il = LIFE / "cognition" / "interchat-ledger.jsonl"
ti = il.read_text(encoding="utf-8", errors="replace").strip()
p(f"   #86 c-leg interchat entries = {ti.count(chr(10)) + 1 if ti else 0} (baseline 22)")
p(f"   #86 CENSUS C-00030 present = {(LIFE / 'census' / 'anchors' / 'C-00030.md').exists()} (gate closed expected False)")

(ROOT / ".c3-tmp/r1080_check.txt").write_text("\n".join(out), encoding="utf-8")
print("WROTE", len(out), "lines; new_dnums=%s ledger_hits=%d board_rows=%d pools=%s" % (
    new if new else "[]", len(hits), len(brows), pools_n))



