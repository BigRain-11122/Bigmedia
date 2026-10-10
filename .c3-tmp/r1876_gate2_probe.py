# -*- coding: utf-8 -*-
# R1876 gate-2 acceptance probe: first city-source radar daily readings
# Reads: (1) reports/daily compose landing; (2) city-source coverage;
# (3) requeue-26 net effect; (4) failed tail. ASCII output only.
import subprocess, sys, os, json, datetime

PSQL = r'data\assets\aihot-poc\pg17\pgsql\bin\psql.exe'
BASE = [PSQL, '-h', '127.0.0.1', '-p', '55432', '-U', 'aihot', '-d', 'aihot',
        '-A', '-t', '-c']

def q(sql):
    r = subprocess.run(BASE + [sql], capture_output=True, text=True,
                       env={**os.environ, 'PGPASSWORD': ''}, timeout=60)
    if r.returncode != 0:
        print('SQL-ERR:', r.stderr.strip()[:200])
        return ''
    return r.stdout.strip()

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print('=== R1876 gate2 probe @', now, '===')

# 0) compose job state (last few runs)
print('-- compose job_runs (last 6) --')
print(q("SELECT status, left(coalesce(error,'-'),60), count(*) FROM job_runs "
        "WHERE name LIKE '%compose%' GROUP BY 1,2 ORDER BY 1 DESC LIMIT 6"))
print(q("SELECT to_char(created_at,'MM-DD HH24:MI'), status, left(coalesce(output->>'judged','?'),12), "
        "left(coalesce(output->>'selected','?'),12) FROM job_runs "
        "WHERE name LIKE '%compose%' ORDER BY created_at DESC LIMIT 4"))

# 1) reports: latest daily landing
print('-- reports (kind=daily, latest 3) --')
print(q("SELECT id, kind, to_char(published_at,'MM-DD HH24:MI'), "
        "left(title,60) FROM reports WHERE kind='daily' ORDER BY published_at DESC LIMIT 3"))

# 2) publications coverage: non-backfill city-source scored/selected
print('-- city pubs coverage (jsonl-/json- sources, non-backfill) --')
print(q("SELECT p.backfill, count(*), count(p.score) scored, "
        "count(*) FILTER (WHERE p.score >= 60) ge60, "
        "count(*) FILTER (WHERE p.selected) sel "
        "FROM publications p JOIN sources s ON p.source_id = s.id "
        "WHERE s.id IN ('json-bilibili-popular','json-zhihu-hot','jsonl-bilibili','jsonl-zhihu') "
        "GROUP BY 1"))
print('-- city pubs scored max/avg (non-bf) --')
print(q("SELECT s.id, count(p.score), round(max(p.score),1), round(avg(p.score),1) "
        "FROM publications p JOIN sources s ON p.source_id = s.id "
        "WHERE s.id IN ('json-bilibili-popular','json-zhihu-hot','jsonl-bilibili','jsonl-zhihu') "
        "AND p.backfill = false GROUP BY 1"))

# 3) articles processing_state per city source (requeue net effect context)
print('-- articles state x city sources --')
print(q("SELECT s.id, a.processing_state, count(*) FROM articles a "
        "JOIN sources s ON a.source_id = s.id "
        "WHERE s.id IN ('json-bilibili-popular','json-zhihu-hot','jsonl-bilibili','jsonl-zhihu') "
        "GROUP BY 1,2 ORDER BY 1,2"))

# 4) failed tail + signature
print('-- failed tail (all sources) --')
print(q("SELECT a.processing_state, count(*) FROM articles a GROUP BY 1 ORDER BY 1"))
print(q("SELECT left(coalesce(r.error->>'reason', r.outcome),50), count(*) FROM receipts r "
        "WHERE r.created_at > '2026-10-09 18:00' GROUP BY 1 ORDER BY 2 DESC LIMIT 6"))

# 5) global selected / judged snapshot
print('-- pubs global snapshot --')
print(q("SELECT count(*), count(score), count(*) FILTER (WHERE score>=60), "
        "count(*) FILTER (WHERE selected) FROM publications"))
print(q("SELECT count(*) FILTER (WHERE backfill=false AND score>=60), "
        "count(*) FILTER (WHERE backfill=false AND selected) FROM publications"))
print('=== end probe ===')
