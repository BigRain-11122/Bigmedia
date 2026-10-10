# -*- coding: utf-8 -*-
# R1876: check receipts for 503 burst impact (AIHOT worker side)
import subprocess, os
PSQL = r'data\assets\aihot-poc\pg17\pgsql\bin\psql.exe'
def q(sql):
    r = subprocess.run([PSQL, '-h', '127.0.0.1', '-p', '55432', '-U', 'aihot', '-d', 'aihot',
                        '-A', '-t', '-c', sql], capture_output=True, text=True,
                       env={**os.environ, 'PGPASSWORD': ''}, timeout=60)
    return r.stdout.strip() if r.returncode == 0 else 'ERR:' + r.stderr.strip()[:150]
print('-- receipts per 30min bucket since 06:00 --')
print(q("SELECT to_char(date_trunc('hour',created_at) + "
        "(floor(extract(minute FROM created_at)/30)*30)*interval '1 min','HH24:MI'), "
        "status, count(*) FROM receipts WHERE created_at > '2026-10-10 05:30' "
        "GROUP BY 1,2 ORDER BY 1,2"))
print('-- receipts errors since 07:30 --')
print(q("SELECT left(coalesce(error->>0, error::text,'-'),60), count(*) FROM receipts "
        "WHERE created_at > '2026-10-10 07:30' AND error IS NOT NULL "
        "GROUP BY 1 ORDER BY 2 DESC LIMIT 5"))
