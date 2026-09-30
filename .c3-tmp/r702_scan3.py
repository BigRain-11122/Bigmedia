# -*- coding: utf-8 -*-
# R702 #93 scan3: .codely-cli root-level files + user-level deep census + renders README row classification
import os, io, re

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TMP = os.path.join(ROOT, ".c3-tmp")
out = []
def w(s): out.append(s)
def sf(n):
    x = float(n)
    for u in ['B','KB','MB','GB']:
        if x < 1024: return "%.1f%s" % (x, u)
        x /= 1024.0
    return "%.2fTB" % x

# (a) repo .codely-cli root-level files
c1 = os.path.join(ROOT, ".codely-cli")
w("-- repo .codely-cli root-level files:")
s0 = 0
for f in sorted(os.listdir(c1)):
    fp = os.path.join(c1, f)
    if os.path.isfile(fp):
        s = os.path.getsize(fp); s0 += s
        w("  %-14s %s  mtime=%s" % (sf(s), f[:80], __import__("time").strftime("%m-%d %H:%M", __import__("time").localtime(os.path.getmtime(fp)))))
w("  root-files total=%s" % sf(s0))

# (b) user-level .codely-cli deep census (level-2 dirs)
c2 = r"C:\Users\sjs20\.codely-cli"
w("-- user .codely-cli level2 dirs:")
agg = {}
for dp, dn, fn in os.walk(c2):
    rel = os.path.relpath(dp, c2)
    lvl = 0 if rel == "." else rel.count(os.sep) + 1
    if lvl >= 2:
        dn[:] = []
        continue
    if lvl == 1:
        s = 0
        for f in fn:
            try: s += os.path.getsize(os.path.join(dp, f))
            except OSError: pass
        for sub in dn:
            sp = os.path.join(dp, sub)
            for d2, dn2, fn2 in os.walk(sp):
                for f in fn2:
                    try: s += os.path.getsize(os.path.join(d2, f))
                    except OSError: pass
        agg[rel.replace("\\", "/")] = s
tot = 0
for dp, dn, fn in os.walk(c2):
    for f in fn:
        try: tot += os.path.getsize(os.path.join(dp, f))
        except OSError: pass
w("  user .codely-cli total=%s" % sf(tot))
for k, v in sorted(agg.items(), key=lambda kv: -kv[1])[:15]:
    w("  %-30s %s" % (k, sf(v)))

# (c) renders README row classification by status markers
rr = os.path.join(ROOT, "output", "renders", "README.md")
lines = io.open(rr, encoding="utf-8").read().splitlines()
cur, hist, chain, other = [], [], [], []
for ln in lines:
    m = re.search(r"(bs-\S+|lc-\d+|sc-\S+)\.(mp4|png)", ln)
    if not m: continue
    name = m.group(0)
    if "已被取代" in ln or "历史档" in ln:
        hist.append(name)
    elif "成品" in ln:
        cur.append(name)
    elif "在链" in ln or "blocked" in ln:
        chain.append(name)
    elif "测试件" in ln or "中间件" in ln or "tmp" in ln.lower():
        other.append(name)
    else:
        other.append(name + "  || " + ln[:90])
w("-- renders README rows: current=%d hist=%d chain=%d other=%d" % (len(cur), len(hist), len(chain), len(other)))
w("CURRENT: %s" % ", ".join(cur))
w("CHAIN: %s" % ", ".join(chain))
w("HIST(first30): %s" % ", ".join(hist[:30]))
io.open(os.path.join(TMP, "r702_scan3.txt"), "w", encoding="utf-8").write("\n".join(out))
print("SCAN3_DONE lines=%d" % len(out))
