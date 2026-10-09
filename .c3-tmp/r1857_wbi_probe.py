# -*- coding: utf-8 -*-
"""R1857 explore#6: bilibili vertical leaderboard wbi-signature channel probe.

Judgment (pre-registered):
  J1: anonymous GET /x/web-interface/nav returns wbi keys (img_key + sub_key)
  J2: wbi-signed GET /x/web-interface/ranking/v2?rid=138&type=all returns code==0 with >=1 list entry
  PASS = J1 and J2.  FAIL = honest negative trace (P-2026-09-28-02 i).
Zero-key, anonymous, read-only, ~5 requests total.
"""
import json
import time
import hashlib
import urllib.request
import urllib.parse

OUT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\.c3-tmp\r1857_wbi_evidence.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
NAV_URL = "https://api.bilibili.com/x/web-interface/nav"
RANK_URL = "https://api.bilibili.com/x/web-interface/ranking/v2"

MIXIN_TAB = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52,
]


def get(url, referer=None, cookie=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    if referer:
        req.add_header("Referer", referer)
    if cookie:
        req.add_header("Cookie", cookie)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, r.read().decode("utf-8", "replace")


def get_buvid():
    st, body = get("https://api.bilibili.com/x/frontend/finger/spi",
                   "https://www.bilibili.com/")
    d = json.loads(body).get("data") or {}
    return {"b3": d.get("b_3"), "b4": d.get("b_4")}


def get_wbi_keys():
    st, body = get(NAV_URL, "https://www.bilibili.com/")
    data = json.loads(body)
    wbi = (data.get("data") or {}).get("wbi_img") or {}
    img_url = wbi.get("img_url") or ""
    sub_url = wbi.get("sub_url") or wbi.get("img_sub_url") or ""
    img_key = img_url.rsplit("/", 1)[-1].split(".")[0] if img_url else ""
    sub_key = sub_url.rsplit("/", 1)[-1].split(".")[0] if sub_url else ""
    return {
        "http": st, "code": data.get("code"), "isLogin": (data.get("data") or {}).get("isLogin"),
        "img_key": img_key, "sub_key": sub_key,
    }


def mixin_key(img_key, sub_key):
    raw = img_key + sub_key
    return "".join(raw[i] for i in MIXIN_TAB)[:32]


def wbi_sign(params, key):
    params = dict(params)
    params["wts"] = int(time.time())
    filtered = {}
    for k, v in sorted(params.items()):
        v = str(v)
        for ch in "!'()*":
            v = v.replace(ch, "")
        filtered[k] = v
    qs = urllib.parse.urlencode(filtered)
    w_rid = hashlib.md5((qs + key).encode()).hexdigest()
    return qs + "&w_rid=" + w_rid


def main():
    ev = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "requests": 0}

    # R0 unsigned baseline (replicates R1362 -352 reading)
    st, body = get(RANK_URL + "?rid=138&type=all", "https://www.bilibili.com/")
    ev["requests"] += 1
    r0 = json.loads(body)
    ev["unsigned_rid138"] = {"http": st, "code": r0.get("code"), "message": r0.get("message")}

    # J1 wbi keys
    nav = get_wbi_keys()
    ev["requests"] += 1
    ev["J1_nav"] = nav
    j1 = bool(nav["img_key"] and nav["sub_key"])
    ev["J1_pass"] = j1
    if not j1:
        ev["verdict"] = "FAIL"
        json.dump(ev, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("J1 FAIL:", nav)
        return

    mk = mixin_key(nav["img_key"], nav["sub_key"])
    ev["mixin_key_len"] = len(mk)

    # J2 signed request rid=138 (搞笑 vertical)
    signed_qs = wbi_sign({"rid": "138", "type": "all"}, mk)
    st, body = get(RANK_URL + "?" + signed_qs, "https://www.bilibili.com/")
    ev["requests"] += 1
    r2 = json.loads(body)
    data = (r2.get("data") or {})
    lst = data.get("list") or []
    ev["signed_rid138"] = {"http": st, "code": r2.get("code"), "message": r2.get("message"),
                           "list_len": len(lst), "note": data.get("note")}
    j2 = (r2.get("code") == 0 and len(lst) >= 1)

    # J2b retry with anonymous buvid cookie (finger/spi = browser first-visit standard)
    if not j2:
        bv = get_buvid()
        ev["requests"] += 1
        ev["buvid"] = {k: (v[:8] + "...") if v else None for k, v in bv.items()}
        if bv.get("b3"):
            cookie = "buvid3=%s; buvid4=%s" % (bv["b3"], bv.get("b4") or "")
            mk2 = mk  # keys unchanged; re-sign for fresh wts
            signed_qs = wbi_sign({"rid": "138", "type": "all"}, mk2)
            st, body = get(RANK_URL + "?" + signed_qs, "https://www.bilibili.com/", cookie)
            ev["requests"] += 1
            r3 = json.loads(body)
            data = (r3.get("data") or {})
            lst = data.get("list") or []
            ev["signed_rid138_buvid"] = {"http": st, "code": r3.get("code"),
                                         "message": r3.get("message"),
                                         "list_len": len(lst), "note": data.get("note")}
            j2 = (r3.get("code") == 0 and len(lst) >= 1)
    sample = []
    for it in lst[:3]:
        owner = (it.get("owner") or {}).get("name", "")
        stat = it.get("stat") or {}
        sample.append({
            "title": it.get("title"), "owner": owner,
            "view": stat.get("view"), "like": stat.get("like"),
            "duration_s": it.get("duration"),
        })
    ev["sample_top3"] = sample
    ev["J2_pass"] = j2

    ev["verdict"] = "PASS" if (j1 and j2) else "FAIL"
    json.dump(ev, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("J1", j1, "J2", j2, "verdict", ev["verdict"],
          "| unsigned code:", ev["unsigned_rid138"]["code"],
          "| signed code:", ev["signed_rid138"]["code"],
          "| list_len:", ev["signed_rid138"]["list_len"])


if __name__ == "__main__":
    main()
