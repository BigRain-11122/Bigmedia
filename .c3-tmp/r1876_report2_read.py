# -*- coding: utf-8 -*-
# R1876: read daily report id=2 (bytes capture + manual utf-8 decode)
import subprocess, os, json
PSQL = r'data\assets\aihot-poc\pg17\pgsql\bin\psql.exe'
def q(sql):
    r = subprocess.run([PSQL, '-h', '127.0.0.1', '-p', '55432', '-U', 'aihot', '-d', 'aihot',
                        '-A', '-t', '-c', sql], capture_output=True,
                       env={**os.environ, 'PGPASSWORD': ''}, timeout=60)
    out = r.stdout.decode('utf-8', 'replace') if r.stdout else ''
    if r.returncode != 0:
        return 'ERR:' + r.stderr.decode('utf-8', 'replace')[:150]
    return out.strip()

raw = q("SELECT content FROM reports WHERE id=2")
try:
    c = json.loads(raw)
    print('keys:', list(c.keys())[:12])
    lead = c.get('lead') or {}
    print('title:', str(lead.get('title'))[:90])
    print('leadPara:', str(lead.get('leadParagraph'))[:160])
    jr = c.get('judgedReports') or []
    sr = c.get('selectedReports') or []
    print('judged:', len(jr), 'selected:', len(sr))
    for s in sr:
        src = s.get('source') or {}
        print('SEL:', str(s.get('title'))[:75], '|', str(src.get('name') or src)[:20], '|score', s.get('score'))
    secs = c.get('sections') or []
    print('sections:', len(secs))
    for s in secs[:8]:
        items = s.get('items') or s.get('reports') or []
        print(' sec:', str(s.get('title') or s.get('heading'))[:60], 'items:', len(items))
        for it in items[:4]:
            src = it.get('source') or {}
            print('   -', str(it.get('title'))[:65], '|', str(src.get('name') or src)[:18], '|', it.get('score'))
except Exception as e:
    print('parse fail:', e)
    print(raw[:300])
