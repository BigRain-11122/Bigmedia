# -*- coding: utf-8 -*-
# R1123 five-checks fresh + three probes (night-window round: E30 DAILY v64 candidate gate)
import json, re, os, io, datetime, subprocess

root = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
hq = r"C:\Users\sjs20\Desktop\FluxGroup"
CT = os.path.join(root, ".c3-tmp")
OUT = []

def rd(p):
    with io.open(p, encoding="utf-8", errors="replace") as f:
        return f.read()

st = json.loads(rd(os.path.join(root, "src", "os", "state.json")))
OUT.append("tick=%s ts=%s production=%s" % (st.get("tick"), st.get("ts"), st.get("production")))
OUT.append("task: %s" % ((st.get("task") or ""))[:90])
logs = st.get("log") or []
for e in logs[-2:]:
    OUT.append("LOGTAIL>> " + e[:400])
wm = st.get("decisions_watermark") or {}
dn = wm.get("dnums") if isinstance(wm, dict) else None

odir = os.path.join(root, "orders")
files = sorted((os.path.getmtime(os.path.join(odir, f)), f) for f in os.listdir(odir) if not f.startswith("."))
mt, f = files[-1]
OUT.append("orders top: %s (%s)" % (f, datetime.datetime.fromtimestamp(mt).strftime("%m-%d %H:%M:%S")))

gp = os.path.join(hq, "docs", "orders.md")
gl = rd(gp).split("\n")
bs_hits = [(i, l.strip()) for i, l in enumerate(gl, 1) if "BigStream" in l]
OUT.append("group orders: mtime=%s lines=%d BS-mention=%d" % (
    datetime.datetime.fromtimestamp(os.path.getmtime(gp)).strftime("%m-%d %H:%M:%S"), len(gl), len(bs_hits)))
for i, ln in bs_hits[-3:]:
    OUT.append("GO L%d: %s" % (i, ln[:160]))

lp = os.path.join(hq, "cph4", "evolution-ledger.md")
lines = rd(lp).split("\n")
hits = [(i, ln.strip()) for i, ln in enumerate(lines, 1)
        if re.search(r"@(BigStream|Biggame|BigMoney|BigLife|BigDomain|BigCompute|FluxVerse|CPH4|七线全司|全司|六司|八线全量)", ln)]
OUT.append("ledger: mtime=%s lines=%d target-hits=%d last-tag-L%s" % (
    datetime.datetime.fromtimestamp(os.path.getmtime(lp)).strftime("%m-%d %H:%M:%S"), len(lines), len(hits),
    hits[-1][0] if hits else "?"))
for i, ln in hits[-2:]:
    OUT.append("L%d: %s" % (i, ln[:180]))

dp = os.path.join(hq, "docs", "decisions.md")
dc = rd(dp)
fileset = set(re.findall(r"[DC]-\d{8}-\d{2}", dc))
known = set(dn or [])
OUT.append("decisions: mtime=%s file=%d wm=%d NEW=%s" % (
    datetime.datetime.fromtimestamp(os.path.getmtime(dp)).strftime("%m-%d %H:%M:%S"), len(fileset), len(known),
    sorted(fileset - known)))

OUT.append("daily 10-03: %s | 10-04: %s" % (
    os.path.exists(os.path.join(root, "data", "intel", "daily", "2026-10-03.md")),
    os.path.exists(os.path.join(root, "data", "intel", "daily", "2026-10-04.md"))))
OUT.append("W40 audit: %s" % os.path.exists(os.path.join(root, "docs", "audits", "2026-W40-self-audit.md")))
gbt = rd(os.path.join(root, "docs", "global-benchmarks.md"))[:3000]
OUT.append("GB head dates: %s" % re.findall(r"2026-\d\d-\d\d", gbt)[:3])

pool = json.loads(rd(os.path.join(hq, "life", "BigLife", "cognition", "pools.json")))
ncount = sum(len(v) for b in pool["axes"].values() for v in b.values()) + sum(len(v) for v in pool["sprite"].values())
OUT.append("#86a pools rows=%d (sprite weekend rows=%d)" % (ncount, len(pool["sprite"]["weekend"])))
icp = os.path.join(hq, "life", "BigLife", "cognition", "interchat-ledger.jsonl")
OUT.append("#86c interchat rows=%d" % (len(rd(icp).strip().split("\n")) if os.path.exists(icp) else -1))
an = os.path.join(hq, "life", "BigLife", "census", "anchors")
OUT.append("#86 anchors tail=%s C-00030:%s" % (sorted(os.listdir(an))[-2:], os.path.exists(os.path.join(an, "C-00030.md"))))

ex = json.loads(rd(os.path.join(root, "docs", "status-export.json")))
OUT.append("export_ts=%s" % ex.get("export_ts"))
OUT.append("index.lock: %s" % os.path.exists(os.path.join(root, ".git", "index.lock")))
OUT.append("now: %s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

io.open(os.path.join(CT, "r1123_check.txt"), "w", encoding="utf-8").write("\n".join(OUT))
print("\n".join(OUT))
print("== check written, running probes ==")

probes = [
    ("board", [os.path.join(root, "src", "board_check.py")], "r1123_board.txt"),
    ("readiness", [os.path.join(root, "src", "readiness.py")], "r1123_rd.txt"),
    ("loop", [os.path.join(root, "src", "os", "loop_health.py")], "r1123_loop.txt"),
]
for name, cmd, out in probes:
    p = subprocess.run(["python", cmd], capture_output=True, cwd=root)
    text = (p.stdout.decode("utf-8", "replace") + "\n[stderr]\n" + p.stderr.decode("utf-8", "replace")).strip()
    io.open(os.path.join(CT, out), "w", encoding="utf-8").write(text + "\n")
    print("== %s rc=%d ==" % (name, p.returncode))

s = io.StringIO()
for name, _, out in probes:
    t = io.open(os.path.join(CT, out), encoding="utf-8").read()
    tl = t.splitlines()
    s.write(u"### %s (lines=%d)\n" % (name, len(tl)))
    warn = 0
    for ln in tl:
        low = ln.lower()
        if "[warn]" in low:
            warn += 1
        if ("fail" in low) or ("finding" in low) or ("blocker" in low) or ("not ready" in low) or ("summary" in low and name == "board"):
            s.write(ln[:300] + u"\n")
    if warn:
        s.write(u"warn count=%d\n" % warn)
    s.write(u"-- tail --\n")
    for ln in tl[-4:]:
        s.write(ln[:300] + u"\n")
    s.write(u"\n")
io.open(os.path.join(CT, "r1123_probes_summary.txt"), "w", encoding="utf-8").write(s.getvalue())
print("probes summary written")
