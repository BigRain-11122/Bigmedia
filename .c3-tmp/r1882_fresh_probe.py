import io
import json
import os
import sys
import time
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "BigStream-radar-source-probe/1.0"}
now = time.time()
out = {}

candidates = {
    "dynamic_region_rid188": "https://api.bilibili.com/x/web-interface/dynamic/region?rid=188&ps=20",
    "newlist_rid188": "https://api.bilibili.com/x/web-interface/newlist?rid=188&page=1&sort=pubdate",
}
for key, url in candidates.items():
    info = {}
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as r:
            body = r.read()
        j = json.loads(body)
        data = j.get("data") or {}
        lst = data.get("archives") if isinstance(data, dict) else None
        info["code"] = j.get("code")
        info["n"] = len(lst) if isinstance(lst, list) else None
        if isinstance(lst, list) and lst:
            f = lst[0]
            info["first_keys"] = sorted(f.keys())[:20]
            info["first_title"] = f.get("title")
            info["first_pubdate"] = f.get("pubdate")
            info["first_age_days"] = round((now - f.get("pubdate", now)) / 86400, 1) if isinstance(f.get("pubdate"), int) else None
            ages = [(now - x.get("pubdate", now)) / 86400 for x in lst if isinstance(x.get("pubdate"), int)]
            if ages:
                info["age_days_min"] = round(min(ages), 1)
                info["age_days_max"] = round(max(ages), 1)
    except Exception as e:
        info["error"] = str(e)[:150]
    out[key] = info
    print(key, json.dumps({k: v for k, v in info.items() if k != "first_title"}, ensure_ascii=False))

with open(os.path.join(ROOT, ".c3-tmp", "r1882_fresh_probe.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("SAVED")
