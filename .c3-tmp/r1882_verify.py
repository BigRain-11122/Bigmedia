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
    return p.stdout.decode("utf-8", "replace")


out = {}
out["src_state"] = [x for x in q("select id, coalesce(last_fetch_at::text,'N'), coalesce(last_ok_at::text,'N'), coalesce(nullif(last_error,''),'none'), fail_count, health from sources where id in ('json-bilibili-tech','json-bilibili-knowledge') order by id;").splitlines() if x.strip()]
out["articles"] = [x for x in q("select source_id, count(*), string_agg(distinct processing_state, ',') from articles where source_id in ('json-bilibili-tech','json-bilibili-knowledge') group by source_id;").splitlines() if x.strip()]
out["runs"] = [x for x in q("select source_id, status, started_at from fetch_runs where source_id in ('json-bilibili-tech','json-bilibili-knowledge') order by started_at desc limit 4;").splitlines() if x.strip()]
print("SRC_STATE:")
for x in out["src_state"]:
    print("  " + x)
print("ARTICLES:")
for x in out["articles"]:
    print("  " + x)
print("RUNS:")
for x in out["runs"]:
    print("  " + x)
with open(os.path.join(ROOT, ".c3-tmp", "r1882_fetch_verify.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("SAVED")
