# -*- coding: utf-8 -*-
"""L-card M1 axis-selection event-anchoring pre-check (tech#192).

E4 audience lane live-fire finding (REACT-v22 5.0, review-20261017
L39/L41): the machine-mapping line (verbatim bucket literal match,
market_close bucket direct-fit) passes every structural gate, yet
readers feel the reaction rows are universal templates with no event
anchoring -- the R2321 E4 flag family "关联可感不足/万能句式". The
gap is a human-perception face that the enforcement line never scored.

This tool is that face, at the point where the gap is born: the M1
pool-row axis-selection step. It extracts the hot topic + reaction
rows (pool axes and the closing row) from a cards.json (or takes them
explicitly), then asks the local brain lane (call_expert OpenAI wire,
:8090 flagship, zero cloud token) to score each row's event anchoring
0-10 against the topic's key words (题眼).

ADVISORY BY DESIGN (非硬闸, unlike collide_scan's rc1 hard gate):
below-threshold rows produce a swap-axis hint (换轴候选提示), never a
render block. The producer either picks a different pool row or records
an acceptance rationale in the card review (e.g. intentional contrast
mapping the model cannot see). Pool sentences stay verbatim --
纪实律不动: this check scores the SELECTION, never rewrites the text.

Exit codes:
    0 = all rows >= threshold (clean)
    1 = hints present (advisory -- producer decides, render never blocked)
    2 = usage / fixture / parse error
    3 = brain lane unreachable or wire failure (UNVERIFIED -- the
        pre-check did not run; log it honestly per the 假绿灯律)

CLI:
    python tools/axis_anchor_check.py --cards-dir data/storylines/cards/MC-...
    python tools/axis_anchor_check.py --topic "..." --row "秩序轴：「...」" \
        --row "..." [--threshold 6.0] [--timeout 240] [--json]

Non-REACT forms (no hot header, no pool rows) pass through with an
empty face by structure, same convention as collide_scan.
"""
import argparse
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))
sys.path.insert(0, os.path.join(REPO, "tools"))

from call_expert import BRAIN_DEFAULT_MODEL, call_model  # noqa: E402
import collide_scan  # noqa: E402

DEFAULT_THRESHOLD = 6.0
DEFAULT_TIMEOUT_S = 240  # pre-check cap: must not stall a production round

HOT_HEADER_RE_PREFIXES = ("今日热点", "城市热点")

PROMPT_TEMPLATE = """你是城市速报卡编辑台的「事件锚定度」预检仪。热点标题与若干候选反应行（城市台词池/信条 verbatim 句，不可改写）如下。先提炼热点题眼词（3-6 个：关键实体/动作/数字/张力点），再为每行评「事件锚定度」0-10 分。

评分口径：
9-10 = 读者一眼可见该行与事件题眼的强共振（具体动作/对象/数字/张力直接对位）
7-8 = 关联清楚但只覆盖事件一部分
4-6 = 弱关联：读起来像能套在任何话题上的万能生活句，缺事件针对性
0-3 = 无关联或语义错配（用词与事件语境相悖）

热点标题：{topic}
候选行：
{rows_block}

只输出严格 JSON（不要任何其他文字，不要 markdown 围栏）：
{{"题眼": ["词1", "词2"], "rows": [{{"idx": 1, "score": 7.5, "reason": "不超过30字"}}, ...]}}"""


def is_hot_header(line):
    """Hot row header: 今日热点/城市热点 · <source> <date>."""
    s = line.strip()
    return any(s.startswith(p) for p in HOT_HEADER_RE_PREFIXES)


def extract_faces(lines):
    """Split card lines into (topic_text, reaction_rows, closing_row).

    Zero hardcoding: shapes decide, never line indexes. Topic = every
    line between the hot header and the first reaction row (hot titles
    legitimately span two design rows). Returns (None, [], None) for
    forms with no hot header and no reaction rows (pass-through face).
    """
    if not lines:
        return None, [], None
    header_idx = None
    for i, line in enumerate(lines):
        if is_hot_header(line):
            header_idx = i
            break
    rows = []
    closing = None
    for line in lines:
        if collide_scan.is_closing_row(line) and closing is None:
            closing = line
        elif collide_scan.is_pool_row(line):
            rows.append(line)
    topic = None
    if header_idx is not None:
        topic_parts = []
        for line in lines[header_idx + 1:]:
            if collide_scan.is_pool_row(line) or collide_scan.is_closing_row(line):
                break
            topic_parts.append(line)
        if topic_parts:
            topic = " ".join(p.strip() for p in topic_parts if p.strip())
    return topic, rows, closing


def build_prompt(topic, rows):
    rows_block = "\n".join("%d. %s" % (i + 1, r) for i, r in enumerate(rows))
    return PROMPT_TEMPLATE.format(topic=topic, rows_block=rows_block)


def parse_scores(text, n_rows):
    """Parse the brain JSON verdict. Returns (题眼, scores list, reasons).

    Raises ValueError on malformed output. String scores are coerced;
    scores are clamped to [0, 10]. idx is 1-based and must cover every
    row exactly once.
    """
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in brain output")
    payload = json.loads(text[start:end + 1])
    eyes = payload.get("题眼") or []
    if not isinstance(eyes, list):
        raise ValueError("题眼 must be a list")
    raw_rows = payload.get("rows")
    if not isinstance(raw_rows, list) or not raw_rows:
        raise ValueError("rows missing in brain output")
    by_idx = {}
    for item in raw_rows:
        idx = int(item["idx"])
        score = float(item["score"])
        by_idx[idx] = (max(0.0, min(10.0, score)), str(item.get("reason", "")))
    if sorted(by_idx) != list(range(1, n_rows + 1)):
        raise ValueError("brain idx set != rows given: %s" % sorted(by_idx))
    scores, reasons = [], []
    for i in range(1, n_rows + 1):
        s, r = by_idx[i]
        scores.append(s)
        reasons.append(r)
    return eyes, scores, reasons


def verdict(scores, threshold):
    """Advisory verdict: indexes of rows below threshold."""
    return [i for i, s in enumerate(scores) if s < threshold]


def run_check(topic, rows, threshold, timeout, model):
    """One brain flight over all rows. Returns dict result (machine face).

    rc semantics: 0 clean / 1 hints (advisory) / 2 parse error /
    3 brain lane down (UNVERIFIED).
    """
    prompt = build_prompt(topic, rows)
    rc, text = call_model(model, prompt, timeout)
    if rc != 0:
        return {"rc": 3, "unverified_reason": text}
    try:
        eyes, scores, reasons = parse_scores(text, len(rows))
    except ValueError as exc:
        return {"rc": 2, "parse_error": str(exc), "brain_raw": text[:400]}
    hints = verdict(scores, threshold)
    return {
        "rc": 1 if hints else 0,
        "题眼": eyes,
        "rows": [
            {"row": rows[i], "score": scores[i], "reason": reasons[i]}
            for i in range(len(rows))
        ],
        "hint_idx": hints,
        "threshold": threshold,
        "advisory": True,
    }


def _harden_console_stdio():
    # tech#246 (R2389): pin console to utf-8 so the CJK advisory lines
    # below stay readable under any codepage (canonical form shared with
    # queue_status.py / orders_rows.py, tech#243/#245).
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main(argv=None):
    _harden_console_stdio()
    ap = argparse.ArgumentParser(
        description="M1 axis-selection event-anchoring pre-check (advisory)")
    ap.add_argument("--cards-dir", help="card dir holding cards.json")
    ap.add_argument("--topic", help="hot topic verbatim (manual mode)")
    ap.add_argument("--row", action="append", default=[],
                    help="reaction row (repeatable, manual mode)")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_S)
    ap.add_argument("--model", default=BRAIN_DEFAULT_MODEL)
    ap.add_argument("--json", action="store_true",
                    help="print the machine-readable result JSON")
    args = ap.parse_args(argv)

    topic, rows = args.topic, list(args.row)
    if args.cards_dir:
        lines = collide_scan.load_lines(args.cards_dir)
        if lines is None:
            print("axis_anchor_check: no cards.json under %s" % args.cards_dir)
            return 2
        auto_topic, auto_rows, closing = extract_faces(lines)
        topic = topic or auto_topic
        rows = rows or auto_rows
        if closing and closing not in rows:
            rows = rows + [closing]
    if not rows:
        print("axis_anchor_check: empty face (no reaction rows) -- "
              "pass-through, nothing to pre-check")
        return 0
    if not topic:
        print("axis_anchor_check: reaction rows found but no hot topic "
              "(pass --topic explicitly for non-standard cards)")
        return 2

    result = run_check(topic, rows, args.threshold, args.timeout, args.model)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    if result["rc"] == 3:
        print("axis_anchor_check: UNVERIFIED (brain lane down) -- %s"
              % result["unverified_reason"])
        return 3
    if result["rc"] == 2:
        print("axis_anchor_check: parse error -- %s" % result["parse_error"])
        return 2
    print("事件锚定度预检 (advisory, tech#192) 题眼: %s 阈值 %.1f"
          % (",".join(result["题眼"]), result["threshold"]))
    for i, r in enumerate(result["rows"]):
        mark = "HINT 换轴候选提示" if i in result["hint_idx"] else "ok"
        print("  [%s] %.1f  %s  (%s)"
              % (mark, r["score"], r["row"][:60], r["reason"]))
    if result["hint_idx"]:
        print("axis_anchor_check: %d below-threshold row(s) -- advisory "
              "hint only; swap the axis candidate or record the acceptance "
              "rationale in the card review. verbatim 纪实律不动, render "
              "is never blocked by this check"
              % len(result["hint_idx"]))
    return result["rc"]


if __name__ == "__main__":
    sys.exit(main())
