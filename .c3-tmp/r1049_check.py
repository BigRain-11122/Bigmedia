# -*- coding: utf-8 -*-
# R1035 quick-path probe: five-check + supply/production status. Output -> r1035_check_out.txt (UTF-8, console GBK law)
import json, re, subprocess, os, glob, time
from pathlib import Path

ROOT = Path(r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream")
GRPF = Path(r"C:\Users\sjs20\Desktop\FluxGroup")
tmp = ROOT / ".c3-tmp"
tmp.mkdir(exist_ok=True)
L = []
def w(s=""): L.append(str(s))

state = json.loads((ROOT / "src/os/state.json").read_text(encoding="utf-8"))
w("== state ==")
w("tick=%s | ts=%s | production=%s" % (state.get("tick"), state.get("ts"), state.get("production")))
w("task=%s" % str(state.get("task", ""))[:120])
wm = state.get("decisions_watermark") or {}
dn = set(wm.get("dnums") or [])
w("watermark dnums=%d latest=%s" % (len(dn), sorted(dn)[-4:]))
log = state.get("log") or []
w("log entries=%d" % len(log))
w("--- last 3 log (650 chars each) ---")
for e in log[-3:]:
    w(str(e)[:650]); w()

w("== git ==")
r = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
w("dirty lines=%d" % len([x for x in r.stdout.splitlines() if x.strip()]))
w(r.stdout[:1200])
w("index.lock=%s" % (ROOT / ".git/index.lock").exists())
r2 = subprocess.run(["git", "log", "--oneline", "-3"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
w(r2.stdout.strip())

w("== orders/ latest ==")
for p in sorted(glob.glob(str(ROOT / "orders/*")), key=os.path.getmtime, reverse=True)[:4]:
    w("%s  %s" % (os.path.basename(p), time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(p)))))

w("== group evolution-ledger scan ==")
led = (GRPF / "cph4/evolution-ledger.md").read_text(encoding="utf-8")
pats = ["@BigStream", "@七线全司", "@全司", "@六司", "@八线全量"]
hits = [(i, ln.strip()) for i, ln in enumerate(led.splitlines(), 1) if any(p in ln for p in pats)]
w("pattern hits=%d" % len(hits))
for i, ln in hits[-5:]:
    w("L%d: %s" % (i, ln[:170]))

w("== group decisions diff (content-addressed) ==")
dec = (GRPF / "docs/decisions.md").read_text(encoding="utf-8")
cur = set(re.findall(r"[DC]-\d{8}-\d{2}", dec))
newd = sorted(cur - dn)
w("decisions set=%d | NEW vs watermark=%d %s" % (len(cur), len(newd), newd))
mb = re.search("派工通告板", dec)
if mb:
    block = dec[mb.end():mb.end() + 5000]
    rows = [ln.strip() for ln in block.splitlines() if ("BigStream" in ln or "七司" in ln)]
    w("dispatch-board rows(BigStream/七司)=%d" % len(rows))
    for ln in rows[:6]:
        w("  " + ln[:170])
else:
    w("no dispatch-board header")
gp = GRPF / "docs/orders.md"
if gp.exists():
    gtxt = gp.read_text(encoding="utf-8")
    phys = [ln.strip() for ln in gtxt.splitlines() if any(k in ln for k in ("账号", "商户号", "服务器"))]
    w("group orders physical-item lines=%d (present-status only)" % len(phys))

w("== supply/production checks ==")
fin = (ROOT / "output/finished.md").read_text(encoding="utf-8")
for k in ("城市盘点 011", "城市盘点 012", "城市盘点 013", "F-082 ", "F-083 ", "F-084 ", "DAILY v60", "DAILY v61", "DAILY v62"):
    w("%s in finished.md: %s" % (k, k in fin))
slog = "\n".join(str(e) for e in log)
for k in ("城市盘点 011", "城市盘点 012", "城市盘点 013", "DAILY v62"):
    w("state.log has %r: %s" % (k, k in slog))
w("--- finished.md tail 16 ---")
w("\n".join(fin.splitlines()[-16:]))
cread = (ROOT / "data/storylines/cards/README.md").read_text(encoding="utf-8")
w("--- cards README tail 14 ---")
w("\n".join(cread.splitlines()[-14:]))

w("== queue / standing ==")
q = ROOT / "docs/self-improvement-queue.md"
if q.exists():
    qt = q.read_text(encoding="utf-8")
    w("queue lines=%d" % len(qt.splitlines()))
    eidx = qt.find("§E")
    if eidx < 0:
        m2 = re.search(r"批活池", qt)
        eidx = m2.start() if m2 else max(0, len(qt) - 3000)
    w("--- queue from E-pool marker (2600 chars) ---")
    w(qt[eidx:eidx + 2600])
w("daily 2026-10-03 exists=%s" % (ROOT / "data/intel/daily/2026-10-03.md").exists())
gb = (ROOT / "docs/global-benchmarks.md").read_text(encoding="utf-8")
mi = re.search("更新记录", gb)
dates = re.findall(r"2026-\d{2}-\d{2}", gb[mi.end():mi.end() + 500]) if mi else []
w("global-benchmarks update-record first date=%s (today=2026-10-03)" % (dates[0] if dates else "?"))
w("audits recent=%s" % [os.path.basename(p) for p in sorted(glob.glob(str(ROOT / "docs/audits/*")), key=os.path.getmtime, reverse=True)[:5]])
w("probe scripts src/os=%s" % [os.path.basename(p) for p in glob.glob(str(ROOT / "src/os/*.py"))])

out = "\n".join(L)
(tmp / "r1035_check_out.txt").write_text(out, encoding="utf-8")
print("OK bytes=", len(out))
