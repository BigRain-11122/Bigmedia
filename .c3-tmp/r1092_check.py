# R1092 round fresh five-check scan (fast-path). Direct read-only per D-20261001-03 (host machine).
# Clone of r1091_check.py (E30 post-v63 supply verdict retained; fleet auto-includes DAILY-v63
# dir committed in dc9da2ea). Output -> .c3-tmp/r1092_check.txt (UTF-8 file).
import json, re, datetime, io, os
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

bk = ROOT / "src" / "os" / "backlog.md"
qp = ROOT / "docs" / "self-improvement-queue.md"
p(f"7. backlog mtime = {datetime.datetime.fromtimestamp(bk.stat().st_mtime)} / queue mtime = {datetime.datetime.fromtimestamp(qp.stat().st_mtime)} (R1083/R1084 direct-verified 01:29 / 06:54)")
bkt = bk.read_text(encoding="utf-8", errors="replace")
open_items = []
for ln in bkt.splitlines():
    m2 = re.match(r"^(\d+)\.", ln.strip())
    if m2 and "[done" not in ln:
        open_items.append((m2.group(1), ln.strip()[:120]))
p(f"   backlog open (non-done) numbered items = {len(open_items)}: " + ", ".join(n for n, _ in open_items))

# --- #86 content-addressing three legs (pools / interchat / CENSUS gate) ---
pj = LIFE / "cognition" / "pools.json"
t = pj.read_text(encoding="utf-8", errors="replace")
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
    pools_n = "?"
p(f"8. #86 a-leg pools.json content count = {pools_n} (baseline 1440, marker-free since 10-03 09:06 reformat)")
il = LIFE / "cognition" / "interchat-ledger.jsonl"
ti = il.read_text(encoding="utf-8", errors="replace").strip()
p(f"   #86 c-leg interchat entries = {ti.count(chr(10)) + 1 if ti else 0} (baseline 22)")
p(f"   #86 CENSUS C-00030 present = {(LIFE / 'census' / 'anchors' / 'C-00030.md').exists()} (gate closed expected False)")

# --- last log entry tail (R1091 close pointers were truncated at round-start read) ---
last = state["log"][-1]
p("9. last log entry (R1091) tail 1600 chars:")
p("   " + last[-1600:].replace("\n", " "))

# --- E30 DAILY post-v63 supply verdict (r1086_pool_scan.py logic, fleet auto-includes v63) ---
p("10. E30 DAILY post-v63 supply scan (fleet = all card dirs incl. MC-20261003-DAILY-v63):")
pool = json.loads(t)
spirit = (ROOT / "data" / "storylines" / "codex" / "city-spirit.md").read_text(encoding="utf-8", errors="replace")
BASE = ROOT / "data" / "storylines" / "cards"
faces = {}
for d in sorted(os.listdir(BASE)):
    cj = BASE / d / "cards.json"
    if cj.is_file():
        cfg = json.loads(cj.read_text(encoding="utf-8"))
        face = u"\n".join(u"\n".join(c.get("lines", [])) for c in cfg.get("cards", []))
        sq = cfg.get("meta", {}).get("source_quote", u"")
        faces[d] = face + u"\n" + sq
v63_dirs = [d for d in faces if "DAILY-v63" in d]
p(f"    fleet dirs = {len(faces)} (DAILY-v63 dir present: {v63_dirs})")

def shingles(text, lo=2, hi=5):
    s = set()
    for L in range(lo, hi + 1):
        for i in range(0, len(text) - L + 1):
            s.add(text[i:i + L])
    return s

def probe(text):
    for sh in sorted(shingles(text), key=len, reverse=True):
        if any(sh in f for f in faces.values()) or sh in spirit:
            return True
    return False

SEASONAL = [u"年味", u"过年", u"春联", u"春雨", u"除夕", u"拜年", u"红包", u"元宵", u"汤圆", u"年年有余"]
# R1086 correction note: 菜 added per standing ruling (morning/6+7 = market-stall 3-link-iso any hour)
ISO_MARKET = [u"生意", u"买卖", u"早市", u"摊", u"市集", u"菜场", u"粥", u"开店", u"开市", u"菜"]
ISO_ANGLING = [u"钓", u"竿"]
AXES = [u"求新", u"怀旧", u"侠气", u"烟火", u"秩序", u"逍遥"]
BUCKETS = [u"night", u"festival", u"dusk", u"market_close", u"morning", u"weekend",
           u"rain", u"typhoon", u"heatwave", u"coldsnap", u"market_open", u"ceo_order"]
SEASON_BLOCKED = {u"heatwave", u"coldsnap"}
EVENT_BLOCKED = {u"rain", u"typhoon", u"ceo_order"}
CLOSURE_BLOCKED = {u"market_open"}
HOUR = now.strftime("%H:%M")
ctx = "late-morning" if now.hour < 12 else ("afternoon" if now.hour < 17 else "night-context")
p(f"    context = {now.strftime('%Y-%m-%d %a')} production ~{HOUR} LITERAL {ctx}; day/night adjacency gates set for day hours")

ungated = []
gated_rows = 0
for axis in AXES + [u"sprite"]:
    src = pool["sprite"] if axis == u"sprite" else pool["axes"][axis]
    for bk in BUCKETS:
        for i, line in enumerate(src.get(bk, [])):
            if any(s in line for s in SEASONAL):
                continue
            if probe(line):
                continue
            gate = []
            if bk in SEASON_BLOCKED: gate.append(u"SEASON(Oct)")
            if bk in EVENT_BLOCKED: gate.append(u"NO-EVENT-TODAY")
            if bk in CLOSURE_BLOCKED: gate.append(u"HOLIDAY-CLOSURE-until-10-08")
            if bk == u"night": gate.append(u"NO-NIGHT-ADJACENCY(day)")
            if bk == u"dusk": gate.append(u"NO-DUSK-ADJACENCY(day)")
            if bk == u"morning":
                if any(m2 in line for m2 in ISO_MARKET): gate.append(u"MARKET-STALL/BIZ-3LINK-ISO(any-hour)")
                if any(m2 in line for m2 in ISO_ANGLING): gate.append(u"ANGLING-POSTV62-FUTURE-BLOCK")
                if line == u"鱼竿一甩，梦醒时分": gate.append(u"CONSUMED-v62")
                if not gate: gate.append(u"MORNING-WINDOW-OPEN")
            if bk == u"weekend":
                gate.append(u"WEEKEND-RESET-OPEN(v61+v62 double intervention; v63=weekend run 1)")
                if u"夜" in line: gate.append(u"NIGHT-CONTENT-AT-DAY-WEAK(R1020-literal-law)")
            if axis == u"sprite" and bk == u"market_close":
                gate.append(u"TWIN-BLOCKED(R1031-reg)")
            if axis == u"sprite" and (u"夜" in line and bk != u"night"):
                gate.append(u"NIGHT-CONTENT-AT-DAY-WEAK")
            if not gate:
                ungated.append((axis, bk, i, line))
            else:
                gated_rows += 1
p(f"    clean-vs-fleet rows still context-gated = {gated_rows}")
p(f"    VERDICT ungated at ~{HOUR} = {len(ungated)}")
for a, bk, i, line in ungated:
    p(f"    !! {a}/{bk}/{i} {line}")
p("    note: sprite/weekend/4 叮咚响夜晚 = unique night-content clean row -> opens at LITERAL NIGHT tonight")
p("    (Saturday) subject to fresh evening scan incl. onomatopoeia-band (v50 叮叮当 + v63 嗡嗡嗡 = 2-member")
p("    band registration, third-use-block pattern mirrors morning-scene band pre-reg R1086)")

(ROOT / ".c3-tmp/r1092_check.txt").write_text("\n".join(out), encoding="utf-8")
print("WROTE %d lines; new_dnums=%s ledger_hits=%d pools=%s ungated=%d" % (
    len(out), new if new else "[]", len(hits), pools_n, len(ungated)))
