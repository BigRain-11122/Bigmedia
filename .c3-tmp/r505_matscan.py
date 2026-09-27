# -*- coding: utf-8 -*-
"""R505 agenda-3 material scan: city_time / rhythm / events-creatures windows + quote pools + census.
Read-only cross-repo (BigLife). Dumps UTF-8 findings file for the loop to read."""
import io, json, os, re

LIFE = r"C:\Users\sjs20\Desktop\FluxGroup\life\BigLife"
OUT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r505_matscan.txt"
out = io.open(OUT, "w", encoding="utf-8")
w = out.write

def sec(t):
    w("\n" + "=" * 8 + " " + t + " " + "=" * 8 + "\n")

# 1) chronicle: type distribution + recent non-order events (city real happenings)
sec("city-chronicle.jsonl overview")
lines = [l for l in io.open(os.path.join(LIFE, "cognition", "city-chronicle.jsonl"), encoding="utf-8") if l.strip()]
w("total events: %d\n" % len(lines))
evs = []
for l in lines:
    try:
        evs.append(json.loads(l))
    except Exception:
        pass
types = {}
for e in evs:
    t = e.get("source_ref", {}).get("type", "?")
    types[t] = types.get(t, 0) + 1
w("type distribution: %s\n" % json.dumps(types, ensure_ascii=False))
w("first date: %s  last date: %s\n" % (evs[0].get("date"), evs[-1].get("date")))
# last 30 events, compact: date | type | summary (truncate 160)
w("\n-- last 30 events --\n")
for e in evs[-30:]:
    s = e.get("source_ref", {})
    w("%s | %s | %s\n" % (e.get("date"), s.get("type"), (s.get("summary") or "")[:160]))
# non CEO_ORDER events (city happenings: stages, creature, broadcast...)
w("\n-- last 25 non-CEO_ORDER events --\n")
seen = 0
for e in reversed(evs):
    s = e.get("source_ref", {})
    if "ORDER" not in (s.get("type") or ""):
        w("%s | %s | %s\n" % (e.get("date"), s.get("type"), (s.get("summary") or "")[:200]))
        seen += 1
        if seen >= 25:
            break

# 2) pools.json (quote pools / cognition)
sec("cognition pools.json")
try:
    p = json.load(io.open(os.path.join(LIFE, "cognition", "pools.json"), encoding="utf-8"))
    if isinstance(p, dict):
        w("top keys: %s\n" % list(p.keys()))
        for k, v in list(p.items())[:8]:
            if isinstance(v, list):
                w("pool %s: n=%d\n" % (k, len(v)))
                for item in v[:3]:
                    w("   sample: %s\n" % json.dumps(item, ensure_ascii=False)[:220])
            elif isinstance(v, dict):
                w("pool %s: dict keys=%s\n" % (k, list(v.keys())[:10]))
    else:
        w("type: %s len=%d\n" % (type(p), len(p)))
except Exception as ex:
    w("ERR pools: %s\n" % ex)

# 3) census overview
sec("census dir overview")
cd = os.path.join(LIFE, "census")
try:
    names = os.listdir(cd)
    w("census entries: %d\n" % len(names))
    w("first 12: %s\n" % names[:12])
    anchors = [n for n in names if "anchor" in n.lower()]
    w("anchor-like files: %d -> %s\n" % (len(anchors), anchors[:5]))
    # read one anchor card if exists
    for n in anchors[:1]:
        fp = os.path.join(cd, n)
        if os.path.isfile(fp):
            txt = io.open(fp, encoding="utf-8", errors="replace").read()
            w("-- anchor sample %s (first 1500 chars) --\n%s\n" % (n, txt[:1500]))
        elif os.path.isdir(fp):
            fs = os.listdir(fp)
            w("anchor dir %s: %d files -> %s\n" % (n, len(fs), fs[:8]))
            if fs:
                t2 = io.open(os.path.join(fp, fs[0]), encoding="utf-8", errors="replace").read()
                w("-- sample %s (first 1200 chars) --\n%s\n" % (fs[0], t2[:1200]))
except Exception as ex:
    w("ERR census: %s\n" % ex)

# 4) search BigLife for city_time / 节律 / 生灵 window definitions
sec("city_time / rhythm / creature-window keyword scan (BigLife docs+state)")
hits = []
for root, dirs, files in os.walk(LIFE):
    dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "package", ".codely-cli")]
    for f in files:
        if f.endswith((".md", ".json", ".py", ".txt")):
            fp = os.path.join(root, f)
            try:
                txt = io.open(fp, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            for kw in ("city_time", "节律", "生灵"):
                if kw in txt:
                    hits.append((fp, kw))
                    break
seen_fp = set()
for fp, kw in hits[:15]:
    if fp in seen_fp:
        continue
    seen_fp.add(fp)
    w("HIT %s  kw=%s\n" % (fp.replace(LIFE, "BigLife"), kw))

# 5) BigLife state snapshot (city clock/rhythm fields)
sec("state snapshot")
for cand in ("state/state.json", "state.json", "state/city.json"):
    fp = os.path.join(LIFE, cand)
    if os.path.isfile(fp):
        try:
            st = json.load(io.open(fp, encoding="utf-8"))
            w("file: %s\n" % cand)
            for k, v in list(st.items())[:30]:
                w("  %s: %s\n" % (k, json.dumps(v, ensure_ascii=False)[:180]))
        except Exception as ex:
            w("ERR state %s: %s\n" % (cand, ex))
        break
out.close()
print("written", OUT)
