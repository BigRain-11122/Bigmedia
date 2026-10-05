import json, urllib.request, urllib.error, io, time, datetime, collections

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1362_humor_bface.txt", "w", encoding="utf-8")
w = out.write
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Referer": "https://www.bilibili.com/"})
    return json.loads(urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace"))

w("B-face humor vertical structure scan (B5 slice3) %s\n" % datetime.datetime.now().strftime("%F %T"))
w("source-grade: B (platform public ranking pages, zero key)\n\n")

# ---- blade 1: all-site ranking partition distribution -> locate humor vertical tid
r1 = None
try:
    r1 = fetch("https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all")
    items = (r1.get("data") or {}).get("list") or []
    w("BLADE1 all-site ranking: code=%s items=%d\n" % (r1.get("code"), len(items)))
    dist = collections.Counter()
    for it in items:
        dist[it.get("tname") or "?"] += 1
    for name, n in dist.most_common():
        w("  tid-dist| %s x%d\n" % (name, n))
    humor_tids = {it.get("tname"): it.get("tid") for it in items if "搞笑" in str(it.get("tname"))}
    w("humor-tname-hits: %s\n" % humor_tids)
except Exception as e:
    w("BLADE1 FAIL: %s: %s\n" % (type(e).__name__, str(e)[:160]))

# ---- blade 2: candidate verticals (funny zone candidates), probe tnames
candidates = [5, 24, 160, 21]
zone_items = None
zone_used = None
for rid in candidates[:2]:  # politeness: <=3 requests total
    try:
        r2 = fetch("https://api.bilibili.com/x/web-interface/ranking/v2?rid=%d&type=all" % rid)
        its = (r2.get("data") or {}).get("list") or []
        names = sorted({str(it.get("tname")) for it in its})
        w("\nBLADE2 rid=%d: code=%s items=%d tnames=%s\n" % (rid, r2.get("code"), len(its), names[:12]))
        if its and zone_items is None and ("搞笑" in " ".join(names) or rid == 5):
            zone_items, zone_used = its, rid
    except Exception as e:
        w("BLADE2 rid=%d FAIL: %s: %s\n" % (rid, type(e).__name__, str(e)[:160]))

if zone_items:
    rid = zone_used
    w("\n== ZONE rid=%s top-25 structure readings ==\n" % rid)
    views = []
    for i, it in enumerate(zone_items[:25], 1):
        st = it.get("stat") or {}
        v = int(st.get("view") or 0)
        views.append(v)
        pub = time.strftime("%Y-%m-%d", time.localtime(it.get("pubdate") or 0))
        w("%02d| %s | %s | view=%d like=%d pub=%s\n" % (
            i, str(it.get("title"))[:60], str((it.get("owner") or {}).get("name"))[:24],
            v, int(st.get("like") or 0), pub))
    if views:
        sv = sorted(views)
        w("\nview-band: max=%d median=%d min=%d\n" % (sv[-1], sv[len(sv)//2], sv[0]))
    w("sample-frame note: top rows above = C-face (account-period) deep-sampling candidates\n")

out.close()
print("ok")
