import io
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


rc = q("update sources set interval_minutes = 180 where id in ('json-bilibili-tech','json-bilibili-knowledge');")
print("INTERVAL180 applied")
# does articles table carry a backfill column?
cols = q("select column_name from information_schema.columns where table_name='articles' and column_name like '%backfill%';")
print("BACKFILL_COLS: %r" % cols.strip())
if cols.strip():
    rows = [x for x in q("select source_id, backfill, count(*) from articles where source_id in ('json-bilibili-tech','json-bilibili-knowledge') group by 1,2;").splitlines() if x.strip()]
    for r in rows:
        print("  " + r)
# sample titles for relevance sanity check
sample = [x for x in q("select left(title,40) from articles where source_id='json-bilibili-tech' order by id limit 5;").splitlines() if x.strip()]
print("SAMPLE_TITLES_TECH:")
for s in sample:
    print("  " + s)
