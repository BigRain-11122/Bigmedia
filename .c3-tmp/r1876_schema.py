# -*- coding: utf-8 -*-
import subprocess, os
PSQL = r'data\assets\aihot-poc\pg17\pgsql\bin\psql.exe'
def q(sql):
    r = subprocess.run([PSQL, '-h', '127.0.0.1', '-p', '55432', '-U', 'aihot', '-d', 'aihot',
                        '-A', '-t', '-c', sql], capture_output=True, text=True,
                       env={**os.environ, 'PGPASSWORD': ''}, timeout=60)
    return r.stdout.strip() if r.returncode == 0 else 'ERR:' + r.stderr.strip()[:150]
for t in ('job_runs', 'reports', 'receipts'):
    print('==', t, '==')
    print(q("SELECT string_agg(column_name, ', ') FROM information_schema.columns WHERE table_name='%s'" % t))
