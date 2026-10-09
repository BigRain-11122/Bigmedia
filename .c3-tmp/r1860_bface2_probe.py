# -*- coding: utf-8 -*-
"""R1860 explore#21 - B5 main-base hypothesis dual-window strong verdict probe.

Zero-key anonymous GETs. Three legs (pre-registered in queue explore#21):
  J1  rid=138 day=30 monthly window via legacy ranking/region route (untested family, zero assertion)
  J2  general popular list same-window comedy (tid=138) share readout
      (R1362 12% snapshot was cross-window, not directly comparable)
  J3  author recurrence across day=3/7 (R1858 evidence) + day=30 (this probe) windows

Evidence -> .c3-tmp/r1860_bface2_evidence.json
"""
import json
import time
import urllib.request

RANK_API = "https://api.bilibili.com/x/web-interface/ranking/region?rid=138&day=30"
POP_API = "https://api.bilibili.com/x/web-interface/popular?ps=50&pn=1"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": UA, "Referer": "https://www.bilibili.com/"}
OUT = r".c3-tmp/r1860_bface2_evidence.json"
R1858_EVIDENCE = r".c3-tmp/r1858_bface_evidence.json"


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def dur_to_s(d):
    parts = [int(p) for p in d.split(":")]
    s = 0
    for p in parts:
        s = s * 60 + p
    return s


def band(d):
    if d < 60:
        return "lt60"
    if d < 180:
        return "60-180"
    if d < 300:
        return "180-300"
    return "gt300"


def main():
    ev = {"probe_ts": time.strftime("%Y-%m-%d %H:%M:%S"), "legs": {}}

    # J1: day=30 monthly window
    try:
        data = fetch(RANK_API)
        code = data.get("code")
        entries = []
        if code == 0:
            for it in data.get("data", []):
                ds = dur_to_s(it.get("duration", "0:00"))
                entries.append({
                    "bvid": it.get("bvid"), "title": it.get("title"),
                    "author": it.get("author"), "mid": it.get("mid"),
                    "play": it.get("play"), "duration_s": ds, "band": band(ds),
                    "create": it.get("create"), "pts": it.get("pts"),
                })
        ev["legs"]["J1_day30"] = {"code": code, "message": data.get("message"), "n": len(entries), "entries": entries}
    except Exception as e:  # noqa: BLE001
        ev["legs"]["J1_day30"] = {"error": repr(e)}
    time.sleep(1.2)

    # J2: general popular same-window comedy share
    try:
        data = fetch(POP_API)
        code = data.get("code")
        pop_items = []
        if code == 0:
            for it in (data.get("data") or {}).get("list", []):
                pop_items.append({
                    "bvid": it.get("bvid"), "title": it.get("title"),
                    "tid": it.get("tid"), "tname": it.get("tname"),
                    "owner": (it.get("owner") or {}).get("name"),
                    "mid": (it.get("owner") or {}).get("mid"),
                    "play": (it.get("stat") or {}).get("view"),
                })
        comedy = [it for it in pop_items if it.get("tid") == 138]
        tname_counts = {}
        for it in pop_items:
            tname_counts[it.get("tname") or "?"] = tname_counts.get(it.get("tname") or "?", 0) + 1
        ev["legs"]["J2_popular"] = {
            "code": code, "message": data.get("message"),
            "n": len(pop_items), "comedy_n": len(comedy),
            "comedy_share": round(len(comedy) / len(pop_items), 4) if pop_items else None,
            "tname_counts": dict(sorted(tname_counts.items(), key=lambda kv: -kv[1])),
            "comedy_items": comedy,
        }
    except Exception as e:  # noqa: BLE001
        ev["legs"]["J2_popular"] = {"error": repr(e)}
    time.sleep(1.2)

    # J3: author recurrence across windows (day=3/7 from R1858 evidence + day=30)
    try:
        prev = json.load(open(R1858_EVIDENCE, encoding="utf-8"))
        d3 = {e["author"] for e in prev["windows"]["3"]["entries"]} if prev["windows"].get("3", {}).get("entries") else set()
        d7 = {e["author"] for e in prev["windows"]["7"]["entries"]} if prev["windows"].get("7", {}).get("entries") else set()
    except Exception as e:  # noqa: BLE001
        ev["legs"]["J3_authors"] = {"error": "r1858 evidence unreadable: " + repr(e)}
        d3 = d7 = set()

    if "entries" in ev["legs"].get("J1_day30", {}):
        d30 = ev["legs"]["J1_day30"]["entries"]
        counts = {}
        for e in d30:
            counts[e["author"]] = counts.get(e["author"], 0) + 1
        repeat30 = {a: c for a, c in counts.items() if c >= 2}
        d30_authors = set(counts)
        cross = {
            "d3_n": len(d3), "d7_n": len(d7), "d30_n": len(d30_authors),
            "d3_and_d30": sorted(d3 & d30_authors),
            "d7_and_d30": sorted(d7 & d30_authors),
            "d3_d7_d30": sorted(d3 & d7 & d30_authors),
        }
        plays = sorted(e["play"] for e in d30 if isinstance(e["play"], int))
        bands = {}
        for e in d30:
            bands[e["band"]] = bands.get(e["band"], 0) + 1
        ev["legs"]["J3_authors"] = {
            "within_30_repeat": repeat30,
            "cross_window": cross,
            "day30_play_band": {"min": plays[0] if plays else None, "max": plays[-1] if plays else None,
                                 "median": plays[len(plays) // 2] if plays else None},
            "day30_duration_bands": bands,
        }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(ev, f, ensure_ascii=False, indent=1)
    # compact stdout readout
    j1 = ev["legs"].get("J1_day30", {})
    j2 = ev["legs"].get("J2_popular", {})
    j3 = ev["legs"].get("J3_authors", {})
    print("J1 day30: code=%s n=%s" % (j1.get("code"), j1.get("n")))
    if j1.get("entries"):
        plays = sorted(e["play"] for e in j1["entries"] if isinstance(e["play"], int))
        print("  play min/med/max: %s / %s / %s" % (plays[0], plays[len(plays) // 2], plays[-1]))
        print("  bands: %s" % j3.get("day30_duration_bands"))
        print("  create range: %s -> %s" % (j1["entries"][-1].get("create"), j1["entries"][0].get("create")))
    print("J2 popular: code=%s n=%s comedy_n=%s share=%s" % (
        j2.get("code"), j2.get("n"), j2.get("comedy_n"), j2.get("comedy_share")))
    print("  top tnames: %s" % dict(list((j2.get("tname_counts") or {}).items())[:8]))
    print("J3 within30 repeat: %s" % j3.get("within_30_repeat"))
    print("J3 cross: %s" % json.dumps(j3.get("cross_window"), ensure_ascii=False))


if __name__ == "__main__":
    main()
