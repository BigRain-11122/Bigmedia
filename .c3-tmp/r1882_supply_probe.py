"""r1882 tech#30 supply-leg probe: AIHOT stack health + source-config introspection
+ Bilibili tech/knowledge region endpoint + Zhihu AI-topic endpoint reachability.
ASCII-only stdout; full UTF-8 report -> .c3-tmp/r1882_supply_probe_report.json
"""
import io
import json
import os
import subprocess
import sys
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .c3-tmp parent = repo root
AIHOT = os.path.join(ROOT, "data", "assets", "aihot-poc", "AIHOT")
PSQL = os.path.join(ROOT, "data", "assets", "aihot-poc", "pg17", "pgsql", "bin", "psql.exe")
REPORT = os.path.join(ROOT, ".c3-tmp", "r1882_supply_probe_report.json")
report = {"ts": "2026-10-10T09:1x"}


def http_probe(url, headers=None, timeout=15):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        try:
            return e.code, e.read()
        except Exception:
            return e.code, b""
    except Exception as e:
        return None, str(e).encode("utf-8", "replace")


def psql(sql, args=None):
    cmd = [PSQL, "-h", "127.0.0.1", "-p", "55432", "-U", "aihot"]
    if args:
        cmd += args
    cmd += ["-t", "-A", "-c", sql]
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=25)
        return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
    except Exception as e:
        return -1, "", str(e)


# 1) AIHOT api health
st, body = http_probe("http://127.0.0.1:3101/api/health")
report["api_health"] = {"status": st, "body": (body[:200].decode("utf-8", "replace") if isinstance(body, bytes) else str(body)[:200])}
print("HEALTH status=%s body=%s" % (st, report["api_health"]["body"][:120]))

# 2) DB connection info from AIHOT .env
db_name = None
env_path = os.path.join(AIHOT, ".env")
env_facts = {}
if os.path.exists(env_path):
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env_facts[k] = v
    db_name = env_facts.get("PGDATABASE") or env_facts.get("DATABASE_NAME") or env_facts.get("POSTGRES_DB")
    url = env_facts.get("DATABASE_URL") or env_facts.get("PG_URL") or ""
    if not db_name and url:
        db_name = url.rsplit("/", 1)[-1].split("?")[0]
report["env_db"] = {"db_name": db_name, "keys": sorted(env_facts.keys())}
print("ENV db_name=%s keys=%d" % (db_name, len(env_facts)))

if db_name:
    rc, so, se = psql(
        "select column_name||' '||data_type from information_schema.columns where table_name='sources' order by ordinal_position",
        args=["-d", db_name],
    )
    report["sources_columns"] = [x for x in so.splitlines() if x.strip()]
    print("SRC_COLS rc=%s n=%d err=%r" % (rc, len(report["sources_columns"]), se[:120]))

    rc, so, se = psql(
        "select id, name, kind, url, config from sources where kind in ('json_list','rss') order by id",
        args=["-d", db_name],
    )
    rows = []
    for line in so.splitlines():
        parts = line.split("|")
        if len(parts) >= 5:
            rows.append({"id": parts[0], "name": parts[1], "kind": parts[2], "url": parts[3], "config": "|".join(parts[4:])})
    report["existing_sources"] = rows
    print("SRC_ROWS rc=%s n=%d err=%r" % (rc, len(rows), se[:120]))

    rc, so, se = psql(
        "select s.id, count(a.id) from sources s left join articles a on a.source_id=s.id group by s.id order by s.id",
        args=["-d", db_name],
    )
    report["article_counts_by_source"] = [x for x in so.splitlines() if x.strip()]
    print("COUNTS rc=%s n=%d" % (rc, len(report["article_counts_by_source"])))

# 6) Bilibili region endpoint probes (any UA avoids 412)
UA = {"User-Agent": "BigStream-radar-source-probe/1.0"}
bili_candidates = {
    "ranking_v2_rid188_tech": "https://api.bilibili.com/x/web-interface/ranking/v2?rid=188&type=all",
    "ranking_v2_rid36_knowledge": "https://api.bilibili.com/x/web-interface/ranking/v2?rid=36&type=all",
    "legacy_region_rid188_day3": "https://api.bilibili.com/x/web-interface/ranking/region?rid=188&day=3",
}
report["bili_probes"] = {}
for key, url in bili_candidates.items():
    st, body = http_probe(url, headers=UA)
    info = {"status": st, "bytes": len(body) if isinstance(body, bytes) else -1}
    try:
        j = json.loads(body)
        data = j.get("data") or {}
        lst = data.get("list") if isinstance(data, dict) else None
        info["code"] = j.get("code")
        info["n_items"] = len(lst) if isinstance(lst, list) else None
        if isinstance(lst, list) and lst:
            first = lst[0]
            info["first_keys"] = sorted(first.keys())[:24]
            info["first_title"] = first.get("title")
            info["first_pubdate"] = first.get("pubdate")
            info["first_create"] = first.get("create")
            info["first_owner"] = (first.get("owner") or {}).get("name") if isinstance(first.get("owner"), dict) else first.get("author")
    except Exception as e:
        info["parse_error"] = str(e)[:100]
    report["bili_probes"][key] = info
    print("BILI %s status=%s code=%s n=%s" % (key, st, info.get("code"), info.get("n_items")))

# 7) Zhihu AI-topic feed candidate (honest UA per R1798; topic id 19551276 = AI candidate)
report["zhihu_probes"] = {}
zhihu_candidates = {
    "topic_19551276_feeds": "https://www.zhihu.com/api/v4/topics/19551276/feeds/timeline_activity?limit=10",
}
for key, url in zhihu_candidates.items():
    st, body = http_probe(url, headers={"User-Agent": "BigStream-radar-source-probe/1.0"})
    info = {"status": st, "bytes": len(body) if isinstance(body, bytes) else -1}
    try:
        j = json.loads(body)
        info["top_keys"] = sorted(j.keys())[:12]
        data = j.get("data") if isinstance(j, dict) else None
        if isinstance(data, list) and data:
            info["n_items"] = len(data)
            info["first_keys"] = sorted(data[0].keys())[:16]
    except Exception as e:
        info["parse_error"] = str(e)[:100]
    report["zhihu_probes"][key] = info
    print("ZHIHU %s status=%s" % (key, st))

with open(REPORT, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print("REPORT_WRITTEN bytes=%d" % os.path.getsize(REPORT))
