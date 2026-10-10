"""r1882 fix: switch tech/knowledge sources from stale ranking/v2 payload to fresh
newlist?sort=pubdate (probe: 50 items, all age 0.0d, data.archives shape)."""
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


def q(sql):
    p = subprocess.run([PSQL, "-h", "127.0.0.1", "-p", "55432", "-U", "aihot", "-d", "aihot", "-t", "-A"], input=sql.encode("utf-8"), capture_output=True, timeout=30, env=ENV)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


BASE = {
    "itemsPath": "data.archives",
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
NEW = {
    "json-bilibili-tech": "https://api.bilibili.com/x/web-interface/newlist?rid=188&page=1&sort=pubdate",
    "json-bilibili-knowledge": "https://api.bilibili.com/x/web-interface/newlist?rid=36&page=1&sort=pubdate",
}
for sid, url in NEW.items():
    cfg = dict(BASE)
    cfg["url"] = url
    cfg_json = json.dumps(cfg, ensure_ascii=False).replace("'", "''")
    rc, so, se = q("update sources set config = '%s'::jsonb, next_fetch_at = now(), last_fetch_at = NULL, last_ok_at = NULL, last_error = NULL, fail_count = 0 where id = '%s';\n" % (cfg_json, sid))
    print("UPDATE %s rc=%s out=%r err=%r" % (sid, rc, so.strip()[:40], se.strip()[:150]))

rc, so, se = q("select id, config->>'url', config->>'itemsPath', next_fetch_at is not null from sources where id in ('json-bilibili-tech','json-bilibili-knowledge') order by id;")
for line in so.splitlines():
    if line.strip():
        print("  " + line)
