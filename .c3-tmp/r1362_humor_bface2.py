import json, urllib.request, urllib.error, io, collections, datetime

repo = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
out = io.open(repo + r"\.c3-tmp\r1362_humor_bface2.txt", "w", encoding="utf-8")
w = out.write
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Referer": "https://www.bilibili.com/"})
    return json.loads(urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace"))

w("B-face substitute reading: popular API partition labels %s\n" % datetime.datetime.now().strftime("%F %T"))
try:
    r = fetch("https://api.bilibili.com/x/web-interface/popular?ps=50&pn=1")
    items = (r.get("data") or {}).get("list") or []
    w("code=%s items=%d\n" % (r.get("code"), len(items)))
    dist = collections.Counter(str(it.get("tname")) for it in items)
    for name, n in dist.most_common():
        w("POP-DIST| %s x%d\n" % (name, n))
    w("\n-- humor-labeled (tname contains 搞笑/娱乐/生活/鬼畜) top rows --\n")
    for it in items:
        tn = str(it.get("tname"))
        if any(k in tn for k in ("搞笑", "娱乐", "鬼畜")):
            st = it.get("stat") or {}
            w("HUM| [%s] %s | %s | view=%d\n" % (tn, str(it.get("title"))[:56],
                                                  str((it.get("owner") or {}).get("name"))[:20],
                                                  int(st.get("view") or 0)))
except Exception as e:
    w("FAIL: %s: %s\n" % (type(e).__name__, str(e)[:160]))
out.close()
print("ok")
