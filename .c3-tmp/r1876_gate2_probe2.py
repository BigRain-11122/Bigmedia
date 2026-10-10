# -*- coding: utf-8 -*-
# R1876 gate-2 acceptance probe v2 (corrected columns)
import subprocess, os, datetime
PSQL = r'data\assets\aihot-poc\pg17\pgsql\bin\psql.exe'
def q(sql):
    r = subprocess.run([PSQL, '-h', '127.0.0.1', '-p', '55432', '-U', 'aihot', '-d', 'aihot',
                        '-A', '-t', '-c', sql], capture_output=True, text=True,
                       env={**os.environ, 'PGPASSWORD': ''}, timeout=60)
    return r.stdout.strip() if r.returncode == 0 else 'ERR:' + r.stderr.strip()[:150]

print('=== R1876 gate2 probe v2 @',
      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '===')

# 1) compose job runs latest
print('-- job_runs compose (latest 5) --')
print(q("SELECT to_char(started_at,'MM-DD HH24:MI'), status, left(coalesce(detail,'-'),70) "
        "FROM job_runs WHERE job LIKE '%compose%' ORDER BY started_at DESC LIMIT 5"))

# 2) reports daily latest
print('-- reports kind=daily (latest 3) --')
print(q("SELECT id, left(key,24), to_char(window_start,'MM-DD HH24:MI'), "
        "to_char(window_end,'MM-DD HH24:MI'), to_char(generated_at,'MM-DD HH24:MI') "
        "FROM reports WHERE kind='daily' ORDER BY created_at DESC LIMIT 3"))
# selected pubs inside current daily window (non-bf)
print('-- nonbf pubs in window 10-09..10-10 (selected/judged material) --')
print(q("SELECT count(*), count(score) scored, count(*) FILTER (WHERE score>=60) ge60, "
        "count(*) FILTER (WHERE selected) sel FROM publications "
        "WHERE backfill=false AND score IS NOT NULL"))

# 3) requeue-26 net effect: audit_log requeue rows + current failed
print('-- audit_log requeue rows (10-09 19:00+) --')
print(q("SELECT to_char(created_at,'MM-DD HH24:MI'), left(action,40), left(coalesce(detail,'-'),50) "
        "FROM audit_log WHERE action ILIKE '%requeue%' AND created_at > '2026-10-09 18:00' "
        "ORDER BY created_at DESC LIMIT 4"))

# 4) failed tail + signature (receipts after 19:00)
print('-- receipts status counts (10-09 19:00+) --')
print(q("SELECT status, count(*) FROM receipts WHERE created_at > '2026-10-09 19:00' "
        "GROUP BY 1 ORDER BY 2 DESC"))
print('-- receipts error signature (10-09 19:00+, non-null error) --')
print(q("SELECT left(error, 60), count(*) FROM receipts "
        "WHERE created_at > '2026-10-09 19:00' AND error IS NOT NULL "
        "GROUP BY 1 ORDER BY 2 DESC LIMIT 5"))

# 5) articles states (all + city)
print('-- articles states (all) --')
print(q("SELECT processing_state, count(*) FROM articles GROUP BY 1 ORDER BY 1"))
print('-- city articles states --')
print(q("SELECT s.id, a.processing_state, count(*) FROM articles a "
        "JOIN sources s ON a.source_id=s.id "
        "WHERE s.id IN ('json-bilibili-popular','json-zhihu-hot') GROUP BY 1,2 ORDER BY 1,2"))
print('=== end v2 ===')
