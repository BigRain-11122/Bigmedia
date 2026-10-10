# -*- coding: utf-8 -*-
# R1876 gate-2 probe v3: window-filtered selection material + requeue trace
import subprocess, os
PSQL = r'data\assets\aihot-poc\pg17\pgsql\bin\psql.exe'
def q(sql):
    r = subprocess.run([PSQL, '-h', '127.0.0.1', '-p', '55432', '-U', 'aihot', '-d', 'aihot',
                        '-A', '-t', '-c', sql], capture_output=True, text=True,
                       env={**os.environ, 'PGPASSWORD': ''}, timeout=60)
    return r.stdout.strip() if r.returncode == 0 else 'ERR:' + r.stderr.strip()[:150]

print('-- publications columns --')
print(q("SELECT string_agg(column_name, ', ') FROM information_schema.columns WHERE table_name='publications'"))
print('-- audit_log columns --')
print(q("SELECT string_agg(column_name, ', ') FROM information_schema.columns WHERE table_name='audit_log'"))
print('-- selected nonbf pubs (timing) --')
print(q("SELECT p.id, round(p.score,1), to_char(p.created_at,'MM-DD HH24:MI') c, "
        "left(s.id,20) src FROM publications p JOIN sources s ON p.source_id=s.id "
        "WHERE p.selected AND p.backfill=false"))
print('-- nonbf pubs scored ge60 timing (window material) --')
print(q("SELECT to_char(p.created_at,'MM-DD HH24:MI'), round(p.score,1), p.selected, left(s.id,18) "
        "FROM publications p JOIN sources s ON p.source_id=s.id "
        "WHERE p.backfill=false AND p.score>=60 ORDER BY p.created_at DESC LIMIT 10"))
