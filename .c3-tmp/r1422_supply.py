# -*- coding: ascii -*-
# R1422 window-opening full derive: supply gates + E4 pending + open-lane enumeration
import json, os, re, io, glob, datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = ROOT + r"\media\BigStream"
out = io.StringIO()
def w(s=""):
    out.write(s + "\n")

# 1) CENSUS supply gate: anchors dir top files (canonical position only)
anch_dir = BS + r"\..\..\..\life\BigLife\census\anchors"
# canonical anchors path used by prior rounds: life/BigLife/census/anchors
alt = ROOT + r"\life\BigLife\census\anchors"
for label, d in [("anchors_dir", alt)]:
    if os.path.isdir(d):
        fs = sorted(f for f in os.listdir(d) if f.endswith(".md"))
        w("CENSUS_ANCHORS_COUNT: %d" % len(fs))
        w("CENSUS_ANCHORS_TOP3: %s" % fs[-3:])
        w("CENSUS_C00030: %s" % ("EXISTS" if "C-00030.md" in fs else "absent"))
        w("CENSUS_C00031: %s" % ("EXISTS" if "C-00031.md" in fs else "absent"))
    else:
        w("CENSUS_ANCHORS_DIR: MISSING (%s)" % d)

# 2) pools.json TOTAL_LINES (content-addressed, D-20261001/D-20260930-18)
pools = ROOT + r"\life\BigLife\cognition\pools.json"
if os.path.exists(pools):
    with io.open(pools, "r", encoding="utf-8", errors="replace") as f:
        pj = json.load(f)
    total = 0
    axes = pj.get("axes", {})
    if isinstance(axes, dict):
        for k, v in axes.items():
            if isinstance(v, list):
                total += len(v)
            elif isinstance(v, dict):
                for kk, vv in v.items():
                    if isinstance(vv, list):
                        total += len(vv)
    sp = pj.get("sprite", [])
    if isinstance(sp, list):
        total += len(sp)
    w("POOLS_TOTAL_LINES_EST: %s (mtime %s)" % (total, os.path.getmtime(pools)))
    w("POOLS_MTIME_STR: %s" % datetime.datetime.fromtimestamp(os.path.getmtime(pools)).strftime("%Y-%m-%d %H:%M:%S"))
else:
    w("POOLS: MISSING")

# 3) interchat ledger
ic = ROOT + r"\life\BigLife\cognition\interchat-ledger.jsonl"
if os.path.exists(ic):
    w("INTERCHAT_MTIME: %s" % datetime.datetime.fromtimestamp(os.path.getmtime(ic)).strftime("%Y-%m-%d %H:%M:%S"))
else:
    w("INTERCHAT: MISSING")

# 4) E4 pending: expert-calls rows without verdict backfill
# canonical verdicts dir
vd = BS + r"\docs\reviews\expert-verdicts"
calls = BS + r"\docs\reviews\expert-calls.md"
if os.path.exists(vd):
    vfs = sorted(os.listdir(vd))
    w("VERDICTS_COUNT: %d" % len(vfs))
    w("VERDICTS_TODAY: %s" % [f for f in vfs if f.startswith("2026100")][-6:])
w("ROOT_LEFTOVER_VERDICTS: %d" % len(glob.glob(BS + r"\expert-verdicts\*")))
if os.path.exists(calls):
    with io.open(calls, "r", encoding="utf-8", errors="replace") as f:
        cl = f.read()
    lines = [l for l in cl.splitlines() if l.strip()]
    w("EXPERT_CALLS_ROWS: %d" % len(lines))

# 5) novel ch3+ v4 / ch6 presence (bm-a gate)
for ch in ["SC-001-03", "SC-001-06"]:
    hits = glob.glob(BS + r"\data\storylines\novel\%s*v4*.md" % ch) + glob.glob(BS + r"\data\storylines\novel\%s*.md" % ch)
    w("NOVEL_%s: %s" % (ch, sorted(os.path.basename(h) for h in hits)[-2:] if hits else "absent"))

# 6) OH window files (OSS harvest ledger files)
oh = ROOT + r"\cph4\oss-harvest"
if os.path.isdir(oh):
    w("OH_FILES: %s" % sorted(os.listdir(oh)))

# 7) finished.md tail (last product registered)
fin = BS + r"\output\finished.md"
if os.path.exists(fin):
    with io.open(fin, "r", encoding="utf-8", errors="replace") as f:
        fl = f.read()
    blocks = re.findall(r"F-\d{3}", fl)
    w("FINISHED_F_IDS_SEEN: last=%s count=%d" % (blocks[-1] if blocks else "?", len(set(blocks))))

# 8) export freshness + live three lines
exp = BS + r"\docs\status-export.json"
if os.path.exists(exp):
    with io.open(exp, "r", encoding="utf-8", errors="replace") as f:
        ej = json.load(f)
    w("EXPORT_TS: %s" % ej.get("export_ts"))
    live = ej.get("live") or {}
    for k in ["current", "recent", "next"]:
        v = live.get(k) if isinstance(live, dict) else None
        w("EXPORT_LIVE_%s: %s" % (k, str(v)[:120]))

# 9) round.lock presence (launcher-managed)
lock = BS + r"\logs\iteration-loop\round.lock"
w("ROUND_LOCK: %s" % ("EXISTS" if os.path.exists(lock) else "none"))

with io.open(BS + r"\.c3-tmp\r1422_supply.txt", "w", encoding="utf-8") as f:
    f.write(out.getvalue())
print(out.getvalue())
