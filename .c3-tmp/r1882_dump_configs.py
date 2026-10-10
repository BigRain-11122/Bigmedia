import io
import json
import os
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PSQL = os.path.join(ROOT, "data", "assets", "aihot-poc", "pg17", "pgsql", "bin", "psql.exe")

rows = []
for sid in ("json-bilibili-popular", "json-zhihu-hot", "jsonl-bilibili-popular", "jsonl-zhihu-hotlist"):
    sql = "select id, kind, interval_minutes, enabled, tier, coalesce(config::text,'') from sources where id = '%s'" % sid
    p = subprocess.run([PSQL, "-h", "127.0.0.1", "-p", "55432", "-U", "aihot", "-d", "aihot", "-t", "-A", "-c", sql], capture_output=True, timeout=25)
    out = p.stdout.decode("utf-8", "replace").strip()
    print("ROW %s rc=%s len=%d" % (sid, p.returncode, len(out)))
    rows.append({"id": sid, "raw": out})

with open(os.path.join(ROOT, ".c3-tmp", "r1882_source_configs.json"), "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)
print("SAVED")
