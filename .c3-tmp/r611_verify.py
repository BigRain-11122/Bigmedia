# -*- coding: utf-8 -*-
# r611_verify.py -- post-close verification for R611 (UTF-8 evidence file via io.open, R562/R585 rule)
import io, json, os, datetime, subprocess, sys

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
SP = os.path.join(ROOT, "src", "os", "state.json")
XP = os.path.join(ROOT, "docs", "status-export.json")

lines = []
def ap(s):
    lines.append(s)

st = json.load(io.open(SP, encoding="utf-8"))
ap("TICK=%d" % st["tick"])
ap("TS=%s" % st["ts"])
ap("TASK=%s" % st["task"])
ap("TASK_LEN=%d" % len(st["task"]))
ap("LOG_COUNT=%d" % len(st["log"]))
tail = st["log"][-1]
ap("LOG_TAIL_HEAD=%s" % tail[:80])
ap("LOG_TAIL_HAS_R611=%s" % ("R611:" in tail))
ts_pat = tail.split(" ", 2)
ap("LOG_TAIL_TS_PREFIX=%s %s" % (ts_pat[0], ts_pat[1]))
ap("FOCUS_HEAD=%s" % st["focus"][:120])
ap("FOCUS_HAS_R611_BASE=%s" % (u"r611_lednew5.txt" in st["focus"]))
ap("FOCUS_HAS_WINDOW_4_6=%s" % (u"4/6=R609-R614" in st["focus"]))

xp = json.load(io.open(XP, encoding="utf-8"))
ap("EXPORT_TS=%s" % xp["export_ts"])
mt = datetime.datetime.fromtimestamp(os.path.getmtime(XP)).strftime("%Y-%m-%d %H:%M:%S")
ap("EXPORT_MTIME=%s" % mt)
osrow = [r[1][:100] for r in xp["outs"] if r[0] == u"OS 循环"]
ap("EXPORT_OS_ROW=%s" % (osrow[0] if osrow else "MISSING"))

# account-lag self-resolve check: rerun loop_health, look for account-lag line
r = subprocess.run([sys.executable, "src/os/loop_health.py"], cwd=ROOT, capture_output=True)
out = (r.stdout or b'').decode('utf-8', errors='replace')
acct = [l for l in out.splitlines() if 'account-lag' in l]
ap("LOOP_RC=%d" % r.returncode)
ap("ACCOUNT_LAG_LINES=%s" % (" | ".join(acct) if acct else "NONE"))

body = "\n".join(lines)
with io.open(os.path.join(ROOT, ".c3-tmp", "r611_verify.txt"), "w", encoding="utf-8") as fh:
    fh.write(body + "\n")
safe = "\n".join(l for l in lines if all(ord(c) < 128 for c in l))
print(safe)
