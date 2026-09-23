# -*- coding: utf-8 -*-
"""BigStream intel department - daily hot-list collector (O-20260923-2304).

Mission: gather the day's platform hot topics (zero-key, zero-token,
scripted - the interactive session only consumes the structured result)
and render a daily brief that feeds every department:
  selection officer (topic ammunition) / copy craft (calibration data)
  / review panel (rubric grounding) / compliance (risk radar).

Channels (probed live 2026-09-23, both OK with a plain browser UA):
  bilibili-popular  https://api.bilibili.com/x/web-interface/popular
  zhihu-hot         https://api.zhihu.com/topstory/hot-list
Blocked/unparsed channels are recorded in the brief itself (honest
negative results, research-protocol zero-assertion discipline).

ASCII rule: source is pure ASCII; Chinese lives in fetched data and in
the markdown brief this tool writes.

Usage:
    python src/intel/daily_brief.py [--date YYYY-MM-DD] [--out DIR]
Exit codes: 0 ok (even if some channels fail - partials are honest);
            2 bad args; 3 all channels failed.
"""
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO / "data" / "intel" / "daily"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

BILI_API = "https://api.bilibili.com/x/web-interface/popular?ps=%d&pn=1"
ZHIHU_API = "https://api.zhihu.com/topstory/hot-list?limit=%d"
TOP_N = 10


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    raw = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "replace")
    return json.loads(raw)


def parse_bilibili(payload):
    """bilibili popular -> [(title, stat_line)] (pure function, testable)."""
    items = (payload or {}).get("data", {}).get("list", [])
    out = []
    for v in items:
        title = str(v.get("title", "")).strip()
        if not title:
            continue
        owner = str((v.get("owner") or {}).get("name", ""))
        out.append((title, owner))
    return out


def parse_zhihu(payload):
    """zhihu hot-list -> [(title, detail_line)] (pure function, testable)."""
    items = (payload or {}).get("data", [])
    out = []
    for it in items:
        target = it.get("target") or {}
        title = str(target.get("title", "")).strip()
        if not title:
            continue
        heat = it.get("detail_text", "")
        out.append((title, str(heat).strip()))
    return out


def collect(limit=TOP_N):
    """Probe both channels; return {'ok': {name: rows}, 'fail': {name: err}}."""
    ok, fail = {}, {}
    try:
        rows = parse_bilibili(fetch_json(BILI_API % limit))[:limit]
        ok["bilibili-popular"] = rows if rows else []
        if not rows:
            fail["bilibili-popular"] = "empty list"
    except Exception as e:
        fail["bilibili-popular"] = "%s: %s" % (type(e).__name__, str(e)[:80])
    try:
        rows = parse_zhihu(fetch_json(ZHIHU_API % limit))[:limit]
        ok["zhihu-hot"] = rows if rows else []
        if not rows:
            fail["zhihu-hot"] = "empty list"
    except Exception as e:
        fail["zhihu-hot"] = "%s: %s" % (type(e).__name__, str(e)[:80])
    return {"ok": ok, "fail": fail}


def render_brief(day, result):
    """Render the markdown daily brief (data file - Chinese fine here)."""
    lines = []
    lines.append("# 情报日报 %s（BigStream 情报部·自动采集）" % day)
    lines.append("")
    lines.append("> 生成器=`src/intel/daily_brief.py`（零 key 零 token·O-20260923-2304-bm-a）·协议=research-protocol（零断言·负结果如实）。")
    lines.append("> 用途=S0 选题官弹药 / copy-craft 校准参照 / 评审团 rubric 依据 / S4 合规风险雷达。")
    lines.append("")
    for name, rows in result["ok"].items():
        lines.append("## %s（top %d）" % (name, len(rows)))
        lines.append("")
        for i, (title, meta) in enumerate(rows, 1):
            lines.append("%d. %s" % (i, title))
            if meta:
                lines.append("   - %s" % meta)
        lines.append("")
    if result["fail"]:
        lines.append("## 通道卡点（如实）")
        lines.append("")
        for name, err in result["fail"].items():
            lines.append("- %s: %s" % (name, err))
        lines.append("")
    else:
        lines.append("通道：双源全通（%d 条目）。" %
                     sum(len(r) for r in result["ok"].values()))
        lines.append("")
    return "\n".join(lines) + "\n"


def main(argv):
    day = date.today().isoformat()
    out_dir = DEFAULT_OUT
    i = 1
    while i < len(argv):
        if argv[i] == "--date":
            i += 1
            day = argv[i]
        elif argv[i] == "--out":
            i += 1
            out_dir = Path(argv[i])
        i += 1
    result = collect()
    if not result["ok"]:
        print("FAIL all channels down: %s" % result["fail"])
        return 3
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = Path(out_dir) / ("%s.md" % day)
    if out_path.exists():
        # one brief per day: rerun = refresh to latest truth (overwrite)
        pass
    out_path.write_text(render_brief(day, result), encoding="utf-8")
    total = sum(len(r) for r in result["ok"].values())
    print("OK %s ok=%s fail=%s items=%d out=%s"
          % (day, ",".join(result["ok"]) or "-",
             ",".join(result["fail"]) or "-", total, out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
