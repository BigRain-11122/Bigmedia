# -*- coding: utf-8 -*-
# R1876 gate-2 probe v4 (fixed columns)
import subprocess, os
PSQL = r'data\assets\aihot-poc\pg17\pgsql\bin\psql.exe'
def q(sql):
    r = subprocess.run([PSQL, '-h', '127.0.0.1', '-p', '55432', '-U', 'aihot', '-d', 'aihot',
                        '-A', '-t', '-c', sql], capture_output=True, text=True,
                       env={**os.environ, 'PGPASSWORD': ''}, timeout=60)
    return r.stdout.strip() if r.returncode == 0 else 'ERR:' + r.stderr.strip()[:150]

print('-- selected nonbf pubs --')
print(q("SELECT p.article_id, round(p.score,1), to_char(p.discovered_at,'MM-DD HH24:MI'), "
        "left(s.id,20) FROM publications p JOIN sources s ON p.source_id=s.id "
        "WHERE p.selected AND p.backfill=false"))
print('-- nonbf ge60 (window 10-09 08:00..10-10 08:00 material) --')
print(q("SELECT p.article_id, round(p.score,1), p.selected, to_char(p.discovered_at,'MM-DD HH24:MI'), "
        "left(s.id,18) FROM publications p JOIN sources s ON p.source_id=s.id "
        "WHERE p.backfill=false AND p.score>=60 "
        "AND p.discovered_at >= '2026-10-09 08:00' ORDER BY p.discovered_at DESC LIMIT 12"))
print('-- city nonbf scored list (all scores) --')
print(q("SELECT p.article_id, round(p.score,1), p.selected, to_char(p.discovered_at,'MM-DD HH24:MI') "
        "FROM publications p JOIN sources s ON p.source_id=s.id "
        "WHERE s.id IN ('json-bilibili-popular','json-zhihu-hot') AND p.backfill=false "
        "AND p.score IS NOT NULL ORDER BY p.score DESC"))
print('-- audit_log requeue rows --')
print(q("SELECT to_char(created_at,'MM-DD HH24:MI'), actor, action, left(subject,50) "
        "FROM audit_log WHERE action ILIKE '%requeue%' AND created_at > '2026-10-09 18:00' "
        "ORDER BY created_at DESC LIMIT 5"))
