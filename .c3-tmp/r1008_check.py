# -*- coding: utf-8 -*-
# R1008 five-check fresh scan -> .c3-tmp/r1008_scan.txt
import io, json, os, re, glob

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup"
BS = os.path.join(ROOT, "media", "BigStream")
out = []

def w(s):
    out.append(s)

# 1. orders top
orders_dir = os.path.join(ROOT, "docs", "orders")
files = sorted(glob.glob(os.path.join(orders_dir, "*")), key=os.path.getmtime, reverse=True)
top = os.path.basename(files[0]) if files else "NONE"
all_o = len(glob.glob(os.path.join(orders_dir, "*")))
w("orders: %d files, top = %s" % (all_o, top))

# 2. ledger mtime + @BigStream/@all-company hits
led = os.path.join(ROOT, "cph4", "evolution-ledger.md")
w("ledger mtime: %s" % os.path.getmtime(led))
led_txt = io.open(led, encoding="utf-8").read()
hits = [ln for ln in led_txt.splitlines() if (u"@BigStream" in ln or u"@全司" in ln or u"@七线全司" in ln or u"@六司" in ln)]
w("ledger @hits: %d" % len(hits))
w("ledger @hit last-3: %s" % " | ".join(h[-80:] for h in hits[-3:]))

# 3. decisions mtime + dnum content-addressed diff vs state watermark
dec = os.path.join(ROOT, "docs", "decisions.md")
dec_txt = io.open(dec, encoding="utf-8").read()
w("decisions mtime: %s" % os.path.getmtime(dec))
st = json.load(io.open(os.path.join(BS, "src", "os", "state.json"), encoding="utf-8"))
wm = set(st["decisions_watermark"]["dnums"])
cur = set(re.findall(r"D-\d{8}-\d{2}|C-\d{8}-\d{2}", dec_txt))
new = sorted(cur - wm)
w("dnum diff (content-addressed): %s (wm=%d, cur=%d)" % (new if new else "NONE", len(wm), len(cur)))

# 4. index.lock + production + tick
lock = os.path.exists(os.path.join(BS, ".git", "index.lock"))
w("index.lock: %s" % lock)
w("production: %s (tick %d)" % (st["production"], st["tick"]))

# 5. daily report 10-02 / CENSUS C-00030 / OH-20261002
w("daily 2026-10-02: %s" % os.path.exists(os.path.join(BS, "data", "intel", "daily", "2026-10-02.md")))
anchors = glob.glob(os.path.join(ROOT, "life", "BigLife", "**", "C-0003*.md"), recursive=True)
c30 = [a for a in anchors if re.search(r"C-0003(\d\d)", a) and int(re.search(r"C-0003(\d\d)", a).group(1)) >= 30]
w("CENSUS C-00030+: %s (%s)" % (bool(c30), c30[:3] if c30 else "absent"))
oh = os.path.join(BS, "docs", "oss-harvest") if os.path.isdir(os.path.join(BS, "docs", "oss-harvest")) else None
oh_hit = glob.glob(os.path.join(BS, "docs", "**", "OH-20261002*"), recursive=True)
w("OH-20261002-bigstream present: %s (%s)" % (bool(oh_hit), oh_hit[:2]))

# 6. tree state quick
w("scan done: %s" % io.open(os.path.join(BS, ".c3-tmp", "r1008_pool.txt"), encoding="utf-8").read().split("\n")[0])

io.open(os.path.join(BS, ".c3-tmp", "r1008_scan.txt"), "w", encoding="utf-8").write("\n".join(out))
print("SCAN OK")
