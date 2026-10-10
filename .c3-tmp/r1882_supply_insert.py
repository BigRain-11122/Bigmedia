"""r1882 tech#30 supply leg insert, v2: stdin-based psql (UTF-8 clean, PGCLIENTENCODING=UTF8)
to bypass ANSI-argv GBK corruption on Chinese display names."""
import io
import json
import os
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PSQL = os.path.join(ROOT, "data", "assets", "aihot-poc", "pg17", "pgsql", "bin", "psql.exe")

ENV = dict(os.environ)
ENV["PGCLIENTENCODING"] = "UTF8"


def psql(sql):
    p = subprocess.run(
        [PSQL, "-h", "127.0.0.1", "-p", "55432", "-U", "aihot", "-d", "aihot", "-t", "-A"],
        input=sql.encode("utf-8"),
        capture_output=True,
        timeout=30,
        env=ENV,
    )
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


report = {"ts": "2026-10-10T09:3x", "steps": [], "note": "v2 stdin insert after 0xbf GBK argv corruption"}

BASE_CONFIG = {
    "itemsPath": "data.list",
    "titlePaths": ["title"],
    "authorPaths": ["owner.name"],
    "urlTemplate": "https://www.bilibili.com/video/{raw:bvid}",
    "summaryPaths": ["desc"],
    "summaryIsBody": True,
    "externalIdPath": "bvid",
    "publishedAtPath": "pubdate",
    "publishedAtUnit": "epoch_s",
    "_aihot": {"initialBackfillLimit": 20},
}

NEW_SOURCES = [
    ("json-bilibili-tech", "B站科技区热榜", "https://api.bilibili.com/x/web-interface/ranking/v2?rid=188&type=all"),
    ("json-bilibili-knowledge", "B站知识区热榜", "https://api.bilibili.com/x/web-interface/ranking/v2?rid=36&type=all"),
]

for sid, sname, url in NEW_SOURCES:
    cfg = dict(BASE_CONFIG)
    cfg["url"] = url
    rc, so, se = psql("select count(*) from sources where id = '%s';" % sid)
    if so.strip() != "0":
        print("SKIP %s already exists" % sid)
        report["steps"].append({"id": sid, "action": "skip-exists"})
        continue
    cfg_json = json.dumps(cfg, ensure_ascii=False).replace("'", "''")
    sname_sql = sname.replace("'", "''")
    sql = (
        "insert into sources (id, name, kind, config, tags, first_party, owner_entity_id, tier, "
        "participation_mode, signal_group_id, interval_minutes, site_fulltext, syndicate_fulltext, "
        "enabled, health, fail_count, cursor, next_fetch_at, icon_url) "
        "select '%s', '%s', kind, '%s'::jsonb, tags, first_party, owner_entity_id, tier, "
        "participation_mode, signal_group_id, interval_minutes, site_fulltext, syndicate_fulltext, "
        "true, 'ok', 0, NULL, now(), icon_url from sources where id = 'json-bilibili-popular';\n"
        % (sid, sname_sql, cfg_json)
    )
    rc, so, se = psql(sql)
    print("INSERT %s rc=%s out=%r err=%r" % (sid, rc, so.strip()[:60], se.strip()[:200]))
    report["steps"].append({"id": sid, "rc": rc, "stdout": so.strip()[:60], "stderr": se.strip()[:200], "url": url})

rc, so, se = psql("select id, name, enabled, tier, interval_minutes, (next_fetch_at is not null) as has_next, health from sources where id in ('json-bilibili-tech','json-bilibili-knowledge') order by id;")
report["verify_rows"] = [x for x in so.splitlines() if x.strip()]
print("VERIFY rc=%s n=%d" % (rc, len(report["verify_rows"])))
for v in report["verify_rows"]:
    print("  " + v)

with open(os.path.join(ROOT, ".c3-tmp", "r1882_supply_insert_report.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=1)
print("SAVED")
