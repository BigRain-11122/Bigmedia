# -*- coding: utf-8 -*-
"""R1858 explore#20 - B face density structure probe (rid=138 legacy ranking/region).

Zero-key anonymous GETs, reuses the legacy route proven in R-20261010-06 (R1857).
Collects title/author/play/duration/create per window (day=1/3/7) and dumps
raw evidence + computed band structure to .c3-tmp/r1858_bface_evidence.json.
"""
import json
import time
import urllib.request

API = "https://api.bilibili.com/x/web-interface/ranking/region?rid=138&day={d}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": UA, "Referer": "https://www.bilibili.com/"}
OUT = r".c3-tmp/r1858_bface_evidence.json"


def fetch(day):
    req = urllib.request.Request(API.format(d=day), headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def dur_to_s(d):
    # duration strings like "10:30" or "1:02:33"
    parts = [int(p) for p in d.split(":")]
    s = 0
    for p in parts:
        s = s * 60 + p
    return s


def main():
    evidence = {"probe_ts": time.strftime("%Y-%m-%d %H:%M:%S"), "windows": {}}
    for day in (1, 3, 7):
        try:
            data = fetch(day)
        except Exception as e:  # noqa: BLE001
            evidence["windows"][str(day)] = {"error": repr(e)}
            continue
        code = data.get("code")
        entries = []
        if code == 0:
            for it in data.get("data", []):
                entries.append({
                    "bvid": it.get("bvid"),
                    "title": it.get("title"),
                    "author": it.get("author"),
                    "mid": it.get("mid"),
                    "play": it.get("play"),
                    "duration_s": dur_to_s(it.get("duration", "0:00")),
                    "duration_raw": it.get("duration"),
                    "create": it.get("create"),
                    "coins": it.get("coins"),
                    "favorites": it.get("favorites"),
                    "pts": it.get("pts"),
                })
        evidence["windows"][str(day)] = {"code": code, "n": len(entries), "entries": entries}
        time.sleep(1.2)
    # band structure readout (merged unique bvid across windows)
    seen = {}
    for w in evidence["windows"].values():
        for e in w.get("entries", []):
            seen[e["bvid"]] = e
    merged = sorted(seen.values(), key=lambda x: -(x["play"] or 0))
    plays = [e["play"] for e in merged if e["play"]]
    durs = [e["duration_s"] for e in merged]
    bands = {"lt60": 0, "60_180": 0, "180_300": 0, "gt300": 0}
    for s in durs:
        if s < 60:
            bands["lt60"] += 1
        elif s < 180:
            bands["60_180"] += 1
        elif s < 300:
            bands["180_300"] += 1
        else:
            bands["gt300"] += 1
    plays_sorted = sorted(plays)
    med = plays_sorted[len(plays_sorted) // 2] if plays_sorted else None
    evidence["structure"] = {
        "unique_bvid": len(merged),
        "play_min": min(plays) if plays else None,
        "play_median": med,
        "play_max": max(plays) if plays else None,
        "duration_bands": bands,
        "duration_min": min(durs) if durs else None,
        "duration_max": max(durs) if durs else None,
        "titles": [e["title"] for e in merged],
        "authors": [e["author"] for e in merged],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(evidence, f, ensure_ascii=False, indent=1)
    print("RC=0 windows=%s unique=%s" % (
        {k: v.get("n") for k, v in evidence["windows"].items()},
        evidence["structure"]["unique_bvid"]))


if __name__ == "__main__":
    main()
