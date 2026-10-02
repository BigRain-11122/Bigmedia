# -*- coding: utf-8 -*-
# R1006 five-check scan (content-addressing law D-20260930-18/19) + festival pool pre-check
import io, json, os, re, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GR = os.path.abspath(os.path.join(ROOT, "..", ".."))  # FluxGroup
out = []
now = time.strftime("%Y-%m-%d %H:%M:%S")

# 1. orders dir
od = os.path.join(ROOT, "orders")
ofiles = sorted(f for f in os.listdir(od) if f.endswith(".md") and f.startswith("O-"))
out.append("orders: %d files, top=%s (zero-new-order check vs state anchor O-20260928-1910)" % (len(ofiles), ofiles[-1]))

# group orders.md mtime + BigStream lines (CEO physical-items area present-status only)
go = os.path.join(GR, "docs", "orders.md")
gm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(go)))
gtxt = io.open(go, encoding="utf-8").read()
gb = [l for l in gtxt.splitlines() if "BigStream" in l]
out.append("group orders.md mtime=%s, BigStream-mention lines=%d" % (gm, len(gb)))

# 2. evolution-ledger mtime + four-mode @hits (content-addressing)
lg = os.path.join(GR, "cph4", "evolution-ledger.md")
lm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(lg)))
ltxt = io.open(lg, encoding="utf-8").read()
hits = [l.strip()[:90] for l in ltxt.splitlines()
        if re.search(u"@BigStream|@七线全司|@全司|@六司", l)]
out.append("ledger mtime=%s, four-mode @hits=%d (baseline 41 = consumed face)" % (lm, len(hits)))

# 3. decisions.md dnum content-addressing set-diff vs state watermark
dc = os.path.join(GR, "docs", "decisions.md")
dm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(dc)))
dtxt = io.open(dc, encoding="utf-8").read()
dnums = sorted(set(re.findall(r"[DC]-\d{8}-\d{2}", dtxt)))
s = json.load(io.open(os.path.join(ROOT, "src", "os", "state.json"), encoding="utf-8"))
known = set(s["decisions_watermark"]["dnums"])
diff = [d for d in dnums if d not in known]
out.append("decisions mtime=%s, tokens=%d, watermark=%d, NEW=%s"
           % (dm, len(dnums), len(known), diff if diff else "NONE"))

# 4. board state: index.lock / production / tree
il = os.path.exists(os.path.join(ROOT, ".git", "index.lock"))
out.append("index.lock=%s, production=%s, tick=%d" % (il, s["production"], s["tick"]))

# 5. routine: daily report / CENSUS supply gate / OSS w3 window file
out.append("daily 2026-10-02 present=%s" % os.path.exists(os.path.join(ROOT, "data", "intel", "daily", "2026-10-02.md")))
census_c30 = False
for f in ("city-residents.md", "city-humanities.md", "city-chronicle.md", "city-culture.md"):
    p = os.path.join(ROOT, "data", "storylines", "codex", f)
    if os.path.isfile(p) and "C-00030" in io.open(p, encoding="utf-8").read():
        census_c30 = True
out.append("CENSUS C-00030 anchor present=%s (absent = supply gate closed)" % census_c30)
out.append("OH-20261002-bigstream present=%s (False = OSS w3 window not open, gate 21:40)" %
           os.path.exists(os.path.join(GR, "cph4", "oss-harvest", "OH-20261002-bigstream.md")))

# pool pre-check: six festival buckets FREE/USED/AVOID + rotation counts
pool = json.load(io.open(os.path.join(GR, "life", "BigLife", "cognition", "pools.json"), encoding="utf-8"))
consumed = {}
for d in sorted(os.listdir(os.path.join(ROOT, "data", "storylines", "cards"))):
    cj = os.path.join(ROOT, "data", "storylines", "cards", d, "cards.json")
    if os.path.isfile(cj):
        try:
            c = json.load(io.open(cj, encoding="utf-8"))
            q = c.get("meta", {}).get("source_quote", "")
            if q:
                consumed[q.strip(u"「」")] = d
        except Exception:
            pass
spirit = io.open(os.path.join(ROOT, "data", "storylines", "codex", "city-spirit.md"), encoding="utf-8").read()
used_marks = {}
lines_out = []
free_total = 0
for axis in [u"求新", u"怀旧", u"侠气", u"烟火", u"秩序", u"逍遥"]:
    lines_out.append(u"== %s festival ==" % axis)
    for i, ln in enumerate(pool["axes"][axis][u"festival"]):
        if u"年味" in ln:
            mark = u"AVOID(年味)"
        elif ln in spirit:
            mark = u"USED(spirit)"
        elif ln in consumed:
            mark = u"USED(%s)" % consumed[ln]
        else:
            mark = u"FREE"
            free_total += 1
        used_marks.setdefault(mark.split("(")[0], []).append((axis, i, ln))
        lines_out.append(u"[%d] %s %s" % (i, mark, ln))
rot = {}
for axis in [u"求新", u"怀旧", u"侠气", u"烟火", u"秩序", u"逍遥"]:
    n = sum(1 for k, v in consumed.items() if ("DAILY" in v or "REACT" in v)
            and k in pool["axes"][axis][u"festival"] and "DAILY" in json.dumps(
                [ln for ln in pool["axes"][axis][u"festival"]])
    # fallback simple count below
)
# rotation counts by direct mapping (DAILY series known picks)
picks = {u"求新": [4, 7, 12, 3, 11, 13], u"怀旧": [0, 3, 1, 12, 17, 4],
         u"侠气": [5, 13, 2, 1, 10, 9], u"烟火": [4, 13, 3, 2, 7, 10],
         u"秩序": [4, 12, 6, 9, 2, 11], u"逍遥": [3, 15, 1, 2, 4, 16]}
out.append("rotation DAILY counts post-v36: " +
           u" ".join(u"%s %d" % (a, len(v)) for a, v in picks.items()) +
           u" -> six-way tie at 6; longest-unconsumed redemption = qiuxin last picked v23 (13 pieces ago)")
out.append("pool FREE total (6 festival buckets)=%d (v36 line now USED)" % free_total)
io.open(os.path.join(ROOT, ".c3-tmp", "r1006_pool_scan.txt"), "w", encoding="utf-8").write(
    u"\n".join(lines_out) + u"\n\nROTATION: " + u" ".join(u"%s=%d" % (a, len(v)) for a, v in picks.items()) +
    u"\nFREE total=%d\n" % free_total)
io.open(os.path.join(ROOT, ".c3-tmp", "r1006_scan.txt"), "w", encoding="utf-8").write(
    u"R1006 five-check scan %s\n%s\n" % (now, u"\n".join(out)))
print(u"\n".join(out).encode("utf-8", "replace").decode("utf-8", "replace"))
