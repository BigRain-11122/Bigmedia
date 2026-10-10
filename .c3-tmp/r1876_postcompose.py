# -*- coding: utf-8 -*-
# R1876: wait past 08:00 compose, then read compose + report landing
import time, subprocess, os, datetime
PSQL = r'data\assets\aihot-poc\pg17\pgsql\bin\psql.exe'
def q(sql):
    r = subprocess.run([PSQL, '-h', '127.0.0.1', '-p', '55432', '-U', 'aihot', '-d', 'aihot',
                        '-A', '-t', '-c', sql], capture_output=True, text=True,
                       env={**os.environ, 'PGPASSWORD': ''}, timeout=60)
    return r.stdout.strip() if r.returncode == 0 else 'ERR:' + r.stderr.strip()[:150]

target = datetime.datetime(2026, 10, 10, 8, 0, 40)
while datetime.datetime.now() < target:
    print('waiting...', datetime.datetime.now().strftime('%H:%M:%S'), flush=True)
    time.sleep(20)
print('=== post-compose reading @', datetime.datetime.now().strftime('%H:%M:%S'), '===')
print('-- compose job_runs latest --')
print(q("SELECT to_char(started_at,'MM-DD HH24:MI:SS'), status, "
        "left(coalesce(error,'-'),70) FROM job_runs WHERE job LIKE '%compose%' "
        "ORDER BY started_at DESC LIMIT 3"))
print('-- reports daily latest --')
print(q("SELECT id, left(key,24), to_char(window_start,'MM-DD HH24:MI'), "
        "to_char(generated_at,'MM-DD HH24:MI') FROM reports WHERE kind='daily' "
        "ORDER BY created_at DESC LIMIT 3"))
print('-- ollama queue recheck (minimal) --')
r = subprocess.run(['ollama', 'run', 'qwen2.5:14b', 'Reply OK'], capture_output=True,
                   text=True, timeout=90)
print('rc', r.returncode, '|', (r.stdout or r.stderr).strip()[:90])
