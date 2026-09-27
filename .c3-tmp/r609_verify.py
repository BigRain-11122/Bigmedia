# -*- coding: utf-8 -*-
# r609_verify.py -- post-close verification for R608 (UTF-8 evidence file via io.open, R562/R585 rule)
import io, json, os, datetime

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
ap("LOG_TAIL_HAS_R608=%s" % ("R608:" in tail))
ts_pat = tail.split(" ", 2)
ap("LOG_TAIL_TS_PREFIX=%s %s" % (ts_pat[0], ts_pat[1]))
ap("FOCUS_HEAD=%s" % st["focus"][:120])
ap("FOCUS_HAS_R609_BASE=%s" % (u"r609_lednew5.txt" in st["focus"]))
ap("FOCUS_HAS_WINDOW_RESET=%s" % (u"1/6=R609-R614" in st["focus"]))

xp = json.load(io.open(XP, encoding="utf-8"))
ap("EXPORT_TS=%s" % xp["export_ts"])
mt = datetime.datetime.fromtimestamp(os.path.getmtime(XP)).strftime("%Y-%m-%d %H:%M:%S")
ap("EXPORT_MTIME=%s" % mt)
osrow = [r[1][:100] for r in xp["outs"] if r[0] == u"OS 循环"]
ap("EXPORT_OS_ROW=%s" % (osrow[0] if osrow else "MISSING"))

body = "\n".join(lines)
with io.open(os.path.join(ROOT, ".c3-tmp", "r609_verify.txt"), "w", encoding="utf-8") as fh:
    fh.write(body + "\n")
safe = "\n".join(l for l in lines if all(ord(c) < 128 for c in l))
print(safe)
