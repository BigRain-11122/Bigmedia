# -*- coding: utf-8 -*-
# R1877 tech#5 prefilter A/B measurement probe (gated on ollama recovery)
# Baseline: current pack wording industry/prompts/prefilter.md (AI-relevance scope)
# Candidate: industry/prompts/prefilter-city.md (full city-hotspot scope)
# Reads BLOCKed city-source articles from the AIHOT pg (schema self-discovering),
# re-judges each with BOTH wordings via ollama, reports the BLOCK->PASS flip rate.
# Run:  python .c3-tmp/r1877_prefilter_ab.py [--limit 12] [--model qwen2.5:14b]
# Gate: do NOT run while ollama is 503-saturated (tech#41); probe first.
import json
import os
import re
import subprocess
import sys
import unicodedata

PSQL = r"data\assets\aihot-poc\pg17\pgsql\bin\psql.exe"
PACK = r"data\assets\aihot-poc\AIHOT\industry\prompts"
CITY_SOURCES = ("json-bilibili-popular", "json-zhihu-hot")
WINDOW = "2026-10-09 08:00"  # gate-2 acceptance window (R1876 anchor)


def q(sql):
    # bytes capture + utf-8/replace manual decode (GBK-locale reader-thread crash pitfall, in-register)
    r = subprocess.run(
        [PSQL, "-h", "127.0.0.1", "-p", "55432", "-U", "aihot", "-d", "aihot", "-A", "-t", "-c", sql],
        capture_output=True, env={**os.environ, "PGPASSWORD": ""}, timeout=60,
    )
    if r.returncode != 0:
        raise SystemExit("psql ERR: " + r.stderr.decode("utf-8", "replace").strip()[:200])
    return r.stdout.decode("utf-8", "replace").strip()


def ollama_ok():
    r = subprocess.run(["ollama", "run", "qwen2.5:7b-instruct", "Say OK"],
                       capture_output=True, text=True, timeout=120)
    return r.returncode == 0 and "503" not in (r.stdout + r.stderr)


def load_prompt(name):
    # mirrors prompts.ts: pack file text, {{siteName}} filled with the site name
    text = open(os.path.join(PACK, name + ".md"), encoding="utf-8").read()
    site = "雷达日报"  # SITE.name from AIHOT site/site.ts (verified R1877)
    return text.replace("{{siteName}}", site)


def judge(model, system_text, user_text):
    r = subprocess.run(["ollama", "run", model, "--verbose"],
                       input=system_text + "\n\n" + user_text,
                       capture_output=True, text=True, timeout=300,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        return {"label": "ERR", "reason": (r.stdout + r.stderr).strip()[:60]}
    m = re.search(r'\{[^{}]*"label"[^{}]*\}', r.stdout, re.S)
    if not m:
        return {"label": "ERR", "reason": r.stdout.strip()[:60]}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {"label": "ERR", "reason": "parse"}


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 12
    model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "qwen2.5:14b"

    print("== relevance distribution (city sources, window) ==")
    srcs = ",".join("'%s'" % s for s in CITY_SOURCES)
    print(q("SELECT an.relevance, count(*) FROM analyses an JOIN articles a ON an.article_id=a.id "
            "JOIN sources s ON a.source_id=s.id WHERE s.id IN (%s) AND a.created_at >= '%s' "
            "GROUP BY 1 ORDER BY 2 DESC" % (srcs, WINDOW)))

    # BLOCK value self-discovery: use the dominant non-PASS label spelling found above
    rows = q("SELECT a.id, replace(a.title, E'\\n', ' ') FROM articles a JOIN analyses an ON an.article_id=a.id "
             "JOIN sources s ON a.source_id=s.id WHERE s.id IN (%s) AND lower(an.relevance)='block' "
             "AND a.created_at >= '%s' ORDER BY a.created_at DESC LIMIT %d" % (srcs, WINDOW, limit))
    if not rows:
        print("no BLOCK rows found by lower(relevance)='block' - check distribution above")
        return
    base = load_prompt("prefilter")
    cand = load_prompt("prefilter-city")
    flips = same = 0
    print("== A/B re-judgement (n=%d, model=%s) ==" % (len(rows.splitlines()), model))
    for line in rows.splitlines():
        aid, title = line.split("|", 1)
        user = "标题：%s\n正文：（仅标题可用，正文缺失）" % title.strip()
        b = judge(model, base, user)
        c = judge(model, cand, user)
        flip = b.get("label") == "BLOCK" and c.get("label") == "PASS"
        flips += flip
        same += b.get("label") == c.get("label")
        print("%s | base=%s/%s | cand=%s/%s | FLIP=%s | %s"
              % (aid, b.get("label"), b.get("reason", "")[:20], c.get("label"), c.get("reason", "")[:20],
                 "Y" if flip else "-", unicodedata.normalize("NFKC", title.strip())[:36]))
    print("== summary: flips=%d/%d  same=%d  flip_rate=%.0f%% =="
          % (flips, len(rows.splitlines()), same, 100.0 * flips / max(1, len(rows.splitlines()))))


if __name__ == "__main__":
    main()
