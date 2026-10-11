# -*- coding: utf-8 -*-
# R1956 tech#92 A/B probe v3 (channel-hardened re-run):
#  - v1 bug: body-column discovery missed real schema (body_text) -> fed
#    "正文缺失" -> candidate prompt L80 (body missing -> <=30) fired 5/5=30. Invalid.
#  - v2 bug: left(a.body_text, 400) fails SERVER-SIDE (invalid UTF-8 byte 0xe5 inside
#    a top-score row's body; PG validates on string-function processing regardless of
#    client encoding). Production node-pg tolerates via replacement chars -> scores 53-59.
#  - v3: raw column select (zero SQL text functions) + per-row OFFSET fetch (record
#    integrity against embedded newlines) + PGCLIENTENCODING=UTF8 (no UTF8->GBK output
#    conversion) + Python-side 400-char cap with decode(replace) == production tolerance.
# Judgment unchanged: >=3 of head-5 land >=60 with candidate wording.
import json
import os
import re
import subprocess
import sys

PSQL = r"data\assets\aihot-poc\pg17\pgsql\bin\psql.exe"
PROMPT = r"data\assets\aihot-poc\AIHOT\industry\prompts\selection-score-city.md"
MODEL = "qwen2.5:14b-8k"
SITE = "雷达日报"
OUT = r".c3-tmp/r1956_score_ab_v3_result.json"
ENV = {**os.environ, "PGPASSWORD": "", "PGCLIENTENCODING": "UTF8"}
BASE = ("SELECT an.score, a.title, a.body_text "
        "FROM analyses an JOIN articles a ON an.article_id=a.id JOIN sources s ON a.source_id=s.id "
        "WHERE s.id='json-zhihu-hot' AND an.score IS NOT NULL ORDER BY an.score DESC "
        "LIMIT 1 OFFSET %d")


def q_one(offset):
    r = subprocess.run(
        [PSQL, "-h", "127.0.0.1", "-p", "55432", "-U", "aihot", "-d", "aihot", "-A", "-t",
         "-F", "\x01", "-c", BASE % offset],
        capture_output=True, env=ENV, timeout=60,
    )
    if r.returncode != 0:
        raise SystemExit("psql ERR (offset %d): " % offset + r.stderr.decode("utf-8", "replace").strip()[:200])
    return r.stdout.decode("utf-8", "replace")


def judge(system_text, user_text):
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
    system_text = open(PROMPT, encoding="utf-8").read().replace("{{siteName}}", SITE)
    results = []
    print("== A/B v3 candidate re-score (raw-channel, model=%s, n=5) ==" % MODEL, flush=True)
    for offset in range(5):
        raw = q_one(offset)
        parts = raw.split("\x01")
        if len(parts) < 2:
            raise SystemExit("unexpected row shape at offset %d: %r" % (offset, raw[:80]))
        base = parts[0].strip()
        title = parts[1].strip()
        body = parts[2].rstrip("\n") if len(parts) > 2 else ""
        body_flat = body.replace("\n", " ").replace("\x01", " ").strip()[:400]
        user = "标题：%s\n正文：%s" % (title, body_flat if body_flat else "（仅标题可用，正文缺失）")
        score, err = judge(system_text, user)
        results.append({"base": float(base), "cand": score, "err": err, "title": title[:48]})
        print("base=%s cand=%s %s | %s" % (base, score, ("ERR:" + err) if err else "", title[:40]), flush=True)
    ge60 = [r for r in results if (r["cand"] or 0) >= 60]
    verdict = "PASS" if len(ge60) >= 3 else "FAIL"
    print("== summary: ge60=%d/5 -> %s (judgment: >=3 of head-5 >=60) ==" % (len(ge60), verdict), flush=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"results": results, "ge60": len(ge60), "verdict": verdict, "channel": "raw-column-v3"},
                  f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
