# -*- coding: utf-8 -*-
# R1953 tech#92 A/B probe (candidate-only): re-score zhihu-hot head items with
# the anchor-injected selection-score-city.md via production scorer qwen2.5:14b-8k.
# Base readings = DB scores from the 08:00 window (max 59, R1952 evidence).
# Judgment: >=3 of head-5 land >=60 with candidate wording.
# Run: python .c3-tmp/r1953_score_ab.py
import json
import os
import re
import subprocess
import sys

PSQL = r"data\assets\aihot-poc\pg17\pgsql\bin\psql.exe"
PROMPT = r"data\assets\aihot-poc\AIHOT\industry\prompts\selection-score-city.md"
MODEL = "qwen2.5:14b-8k"
SITE = "雷达日报"  # SITE.name, verified R1877
OUT = r".c3-tmp/r1953_score_ab_result.json"


def q(sql):
    r = subprocess.run(
        [PSQL, "-h", "127.0.0.1", "-p", "55432", "-U", "aihot", "-d", "aihot", "-A", "-t", "-c", sql],
        capture_output=True, env={**os.environ, "PGPASSWORD": ""}, timeout=60,
    )
    if r.returncode != 0:
        raise SystemExit("psql ERR: " + r.stderr.decode("utf-8", "replace").strip()[:200])
    return r.stdout.decode("utf-8", "replace").strip()


def judge(system_text, user_text):
    # R1953 bugfix: bytes-mode subprocess (capture_output w/o text=True) requires
    # bytes input; first launch crashed on str. Also VRAM note: 14b-8k loads 85%
    # CPU-offload on the 12G card in contended state -> fire this probe ONLY in a
    # real GPU window (fire-window-card GO), else each call takes minutes.
    r = subprocess.run(
        ["ollama", "run", MODEL],
        input=(system_text + "\n\n" + user_text).encode("utf-8"),
        capture_output=True, timeout=420,
    )
    out = r.stdout.decode("utf-8", "replace")
    m = re.search(r"\{[^{}]*\"attentionScore\"[^{}]*\}", out, re.S)
    if not m:
        return None, out.strip()[:80]
    try:
        return int(json.loads(m.group(0)).get("attentionScore")), ""
    except Exception:
        return None, "parse:" + out.strip()[:60]


def main():
    # content column discovery (fallback title-only)
    cols = q("SELECT column_name FROM information_schema.columns WHERE table_name='articles'")
    body_col = next((c for c in ("content", "text", "body", "summary") if c in cols.split()), None)
    body_sel = ("left(a.%s, 400)" % body_col) if body_col else "''"
    rows = q(
        "SELECT an.score, replace(a.title, E'\\n', ' '), replace(coalesce(%s, ''), E'\\n', ' ') "
        "FROM analyses an JOIN articles a ON an.article_id=a.id JOIN sources s ON a.source_id=s.id "
        "WHERE s.id='json-zhihu-hot' AND an.score IS NOT NULL ORDER BY an.score DESC LIMIT 5" % body_sel
    )
    system_text = open(PROMPT, encoding="utf-8").read().replace("{{siteName}}", SITE)
    results = []
    print("== A/B candidate-only re-score (model=%s, n=5) ==" % MODEL, flush=True)
    for line in rows.splitlines():
        parts = line.split("|")
        base, title, body = parts[0], parts[1], parts[2] if len(parts) > 2 else ""
        user = "标题：%s\n正文：%s" % (title.strip(), body.strip() if body.strip() else "（仅标题可用，正文缺失）")
        score, err = judge(system_text, user)
        results.append({"base": float(base), "cand": score, "err": err, "title": title.strip()[:48]})
        print("base=%s cand=%s %s | %s" % (base, score, ("ERR:" + err) if err else "", title.strip()[:40]), flush=True)
    ge60 = [r for r in results if (r["cand"] or 0) >= 60]
    verdict = "PASS" if len(ge60) >= 3 else "FAIL"
    print("== summary: ge60=%d/5 -> %s (judgment: >=3 of head-5 >=60) ==" % (len(ge60), verdict), flush=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"results": results, "ge60": len(ge60), "verdict": verdict}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
