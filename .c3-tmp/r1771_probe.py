# -*- coding: utf-8 -*-
import json, io, os, re, time, glob

BASE = r"C:\Users\sjs20\Desktop\FluxGroup"
out = []

def w(s):
    out.append(s)

d = json.load(io.open(os.path.join(BASE, r"media\BigStream\src\os\state.json"), encoding="utf-8"))
w("now=%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
w("tick=%s" % d.get("tick"))
w("ts=%s" % d.get("ts"))
w("task=%s" % str(d.get("task"))[:150])
wm = d.get("decisions_watermark") or {}
w("wm_dnums=%s" % json.dumps(wm.get("dnums", [])[-8:], ensure_ascii=False))
w("wm_full=%s" % json.dumps(wm, ensure_ascii=False)[:400])
log = d.get("log", [])
w("log_len=%d" % len(log))
for x in log[-3:]:
    w("---LOG---")
    w(x[:700])

# decisions.md D/C diff
dec = os.path.join(BASE, r"docs\decisions.md")
txt = io.open(dec, encoding="utf-8", errors="replace").read()
nums = set(re.findall(r"[DC]-\d{8}-\d{2}", txt))
old = set(wm.get("dnums", []))
w("dec_new=%s" % json.dumps(sorted(nums - old), ensure_ascii=False))

# evolution-ledger strict @BigStream lines
led = os.path.join(BASE, r"cph4\evolution-ledger.md")
ltxt = io.open(led, encoding="utf-8", errors="replace").read()
pat = re.compile(r"^.*( @BigStream |@七线全司|@全司 |@六司 |@八线全量).*$", re.M)
lines = [l[:80] for l in pat.findall(ltxt)]
w("ledger_at_lines=%d" % len(lines))
w("ledger_tail2=%s" % json.dumps(lines[-2:], ensure_ascii=False))

# orders latest
od = os.path.join(BASE, r"media\BigStream\orders")
files = sorted(glob.glob(os.path.join(od, "*")), key=os.path.getmtime, reverse=True)[:3]
for f in files:
    w("order: %s mtime=%s" % (os.path.basename(f), time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(f)))))

# dirty mv0001 file mtimes
w("---mv0001 dirty mtimes---")
for pat_ in [r"media\BigStream\data\storylines\drama\mv0001\*",
             r"media\BigStream\data\storylines\drama\mv0001\release\*",
             r"media\BigStream\data\sources\mv001\*"]:
    for f in sorted(glob.glob(os.path.join(BASE, pat_)), key=os.path.getmtime, reverse=True)[:6]:
        w("%s %s" % (time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(f))), os.path.basename(f)))

# daily brief today
dbrief = os.path.join(BASE, r"media\BigStream\data\intel\daily\2026-10-08.md")
w("daily_today=%s" % os.path.exists(dbrief))

io.open(os.path.join(BASE, r"media\BigStream\.c3-tmp\r1771_probe.txt"), "w", encoding="utf-8").write("\n".join(out))
print("done")
