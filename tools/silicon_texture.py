# -*- coding: utf-8 -*-
"""M0 sentence-picking silicon-identity pre-filter (tech#259 canonization).

R2401 tech#256 E4 backfill verdict on MC-20261019-DAILY-v71 (6.0, first
break of the v61-v70 8.0 band): the weakest axis was "worldview
penetration" -- the picked quote 「听说城主有令，咱先别急着打听」 is
pure generic street talk; strip the series title and the line fits any
dynasty. The silicon-city IP must show through the PICKED line, not
only through the card title.

Gate semantics (ADVISORY DOWNGRADE -- deliberately NOT a render
blocker, contrast with collide_scan which refuses renders):

- texture-pass : at least one lexicon hit in tech words / silicon-city
                 infrastructure words / data-mechanical-algorithm
                 imagery.
- anchor-pass  : zero lexical hits, but a declared contrast-structure
                 worldview anchor is on record (``--anchor`` on the
                 CLI, ``meta.silicon_anchor`` in cards.json). The tool
                 records the declaration; it never judges the reason
                 (machine check does not replace the seat's judgment).
- downgrade    : zero hits and no declared anchor -- a pure generic
                 cliche line. The candidate ranks below any textured
                 sibling at selection time; when the pool offers no
                 textured candidate at all, the card face must carry a
                 worldview anchor elsewhere (lead-in / sub-line) and the
                 M0 score records the loss honestly.

Scope (line-shape decides, never a card index -- collide_scan family
law): the MAIN quoted line(s) of DAILY/QUOTE cards (选句位). REACT pool
rows and hot-topic verbatim are real-world material by design (their
worldview anchor is the mapped reaction, guarded by axis_anchor_check),
so non-DAILY/QUOTE forms pass through with an out-of-scope face.

Exit codes: 0 pass / anchor-pass / out-of-scope, 1 downgrade (advisory:
selection-time signal, never a render blocker), 2 usage error. CLI:

    python tools/silicon_texture.py --line "听说城主有令，咱先别急着打听"
    python tools/silicon_texture.py --line "..." --anchor "contrast reason"
    python tools/silicon_texture.py --cards-dir data/storylines/cards/MC-...
"""
import argparse
import json
import os
import re
import sys

QUOTED_RE = re.compile(r'「(.+?)」')
DIR_RE = re.compile(r'^MC-\d{8}-([A-Z]+)-v\d+$')

# In-scope forms: the sentence-picking face of the gate.
SCOPED_FORMS = ("DAILY", "QUOTE")

# Category A -- tech / data words (digital life vocabulary).
TECH_WORDS = (
    "数据", "算力", "算法", "芯片", "代码", "程序", "指令", "版本", "更新",
    "缓存", "内存", "云端", "字节", "比特", "终端", "服务器", "信号", "电流",
    "像素", "渲染", "扫描", "校验", "复位", "重启", "充电", "蓄电", "能量",
    "参数", "阈值", "同步", "协议", "序列", "固件", "传感", "雷达", "图谱",
    "上传", "下载", "联机", "掉线", "断线", "上线", "日志", "权限",
)

# Category B -- silicon-city infrastructure words (城建设施词).
INFRA_WORDS = (
    "脑塔", "光塔", "中枢", "数据港", "机房", "大屏", "公告栏", "电网",
    "光缆", "管线", "轨道", "霓虹", "钢架", "塔台", "回路", "节点", "基站",
    "天线", "白光", "闸机", "主城", "城域",
)

# Category C -- data-mechanical-algorithm imagery (machine-body metaphor).
MECH_IMAGERY = (
    "齿轮", "机械", "机件", "轴承", "活塞", "发条", "指针", "仪表", "刻度",
    "旋钮", "开关", "上弦", "运转", "机壳", "钢筋", "铁轨", "螺丝", "铆钉",
    "润滑", "生锈", "卡顿", "延迟", "磨损", "报废", "翻新",
)

CATEGORIES = (
    ("tech", TECH_WORDS),
    ("infra", INFRA_WORDS),
    ("mech-imagery", MECH_IMAGERY),
)


def texture_hits(line):
    """Lexical silicon-texture hits in one line: [(category, word), ...]."""
    hits = []
    for cat, words in CATEGORIES:
        for w in words:
            if w in line:
                hits.append((cat, w))
    return hits


def line_verdict(line, anchor=None):
    """One candidate line -> verdict dict (advisory, never a render gate).

    anchor = declared contrast-structure worldview anchor (reason text).
    """
    hits = texture_hits(line)
    if hits:
        cats = sorted(set(c for c, _ in hits))
        return {
            "verdict": "texture-pass",
            "line": line,
            "hits": hits,
            "categories": cats,
            "anchor": None,
            "reason": "silicon texture present: %s"
                      % ", ".join("%s:%s" % (c, w) for c, w in hits[:5]),
        }
    if anchor:
        return {
            "verdict": "anchor-pass",
            "line": line,
            "hits": [],
            "categories": [],
            "anchor": anchor,
            "reason": "no lexical texture; declared contrast anchor: %s"
                      % anchor,
        }
    return {
        "verdict": "downgrade",
        "line": line,
        "hits": [],
        "categories": [],
        "anchor": None,
        "reason": "pure generic line: no tech/infra/mech imagery and no "
                  "declared worldview anchor (tech#259 downgrade)",
    }


def quoted_sentences(lines):
    """All 「」-quoted sentences across card lines (选句位 face)."""
    found = []
    for ln in lines:
        if not isinstance(ln, str):
            continue
        for s in QUOTED_RE.findall(ln):
            found.append(s)
    return found


def load_card(cards_dir):
    """(meta, lines) of a card dir, or (None, None) when not loadable."""
    path = os.path.join(cards_dir, "cards.json")
    if not os.path.exists(path):
        return None, None
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        cards = d.get("cards", [])
        if not cards:
            return None, None
        return d.get("meta", {}), cards[0].get("lines", [])
    except Exception:
        return None, None


def form_of(dirname):
    """Card form (DAILY/QUOTE/REACT/...) from the MC-YYYYMMDD-FORM-vN name."""
    m = DIR_RE.match(dirname)
    return m.group(1) if m else None


def scan_cards(cards_dir):
    """Card-level report list; [] = structurally out of scope.

    Per-sentence rows for DAILY/QUOTE cards; the card-level verdict is
    the worst sentence verdict (downgrade > anchor-pass > texture-pass).
    A declared meta.silicon_anchor upgrades zero-hit sentences to
    anchor-pass (self-certifying data file, reader_anchor precedent).
    """
    cards_dir = os.path.abspath(cards_dir)
    meta, lines = load_card(cards_dir)
    if meta is None:
        return [{"verdict": "error",
                 "reason": "cards dir has no loadable cards.json: %s"
                           % cards_dir}]
    form = form_of(os.path.basename(cards_dir))
    if form not in SCOPED_FORMS:
        return [{"verdict": "out-of-scope",
                 "form": form,
                 "reason": "form %s is not a 选句位 face (REACT pool rows "
                           "are real-world mapped, axis_anchor_check "
                           "guards them)" % form}]
    anchor = meta.get("silicon_anchor")
    rows = []
    worst = "texture-pass"
    order = {"texture-pass": 0, "anchor-pass": 1, "downgrade": 2}
    for s in quoted_sentences(lines):
        v = line_verdict(s, anchor)
        v["form"] = form
        rows.append(v)
        if order[v["verdict"]] > order[worst]:
            worst = v["verdict"]
    if not rows:
        rows.append({"verdict": "out-of-scope", "form": form,
                     "reason": "no quoted sentence rows on card face"})
    for r in rows:
        r["card"] = os.path.basename(cards_dir)
        r["card_verdict"] = worst
    return rows


def main():
    ap = argparse.ArgumentParser(
        description="M0 sentence-picking silicon-identity pre-filter "
                    "(tech#259, advisory downgrade)")
    ap.add_argument("--line", default=None,
                    help="one candidate sentence to check (选句位)")
    ap.add_argument("--anchor", default=None,
                    help="declared contrast-structure worldview anchor "
                         "(reason text, recorded not judged)")
    ap.add_argument("--cards-dir", default=None,
                    help="card directory containing cards.json "
                         "(DAILY/QUOTE batch face)")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable output")
    args = ap.parse_args()
    if not args.line and not args.cards_dir:
        print("FAIL need --line or --cards-dir")
        return 2
    rows = []
    if args.line:
        rows.append(line_verdict(args.line, args.anchor))
    else:
        if not os.path.isdir(args.cards_dir):
            print("FAIL cards dir not found: %s" % args.cards_dir)
            return 2
        rows = scan_cards(args.cards_dir)
    worst = "texture-pass"
    order = {"texture-pass": 0, "anchor-pass": 1, "downgrade": 2,
             "out-of-scope": 0, "error": 3}
    for r in rows:
        if order.get(r["verdict"], 0) > order.get(worst, 0):
            worst = r["verdict"]
    if args.json:
        print(json.dumps({"rows": rows, "worst": worst},
                         ensure_ascii=False, indent=1))
    else:
        for r in rows:
            print("[%s] %s" % (r["verdict"], r.get("line", r["reason"])))
            print("      %s" % r["reason"])
    if worst == "downgrade":
        print("silicon-texture: DOWNGRADE (tech#259 advisory -- selection-"
              "time signal, never a render blocker)")
        return 1
    print("silicon-texture: %s (tech#259)" % worst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
