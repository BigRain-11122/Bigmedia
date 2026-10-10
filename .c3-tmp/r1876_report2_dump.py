# -*- coding: utf-8 -*-
# R1876: dump exact report id=2 headline to evidence file (utf-8)
import subprocess, os, json, io
PSQL = r'data\assets\aihot-poc\pg17\pgsql\bin\psql.exe'
r = subprocess.run([PSQL, '-h', '127.0.0.1', '-p', '55432', '-U', 'aihot', '-d', 'aihot',
                   '-A', '-t', '-c', "SELECT content FROM reports WHERE id=2"],
                  capture_output=True, env={**os.environ, 'PGPASSWORD': ''}, timeout=60)
c = json.loads(r.stdout.decode('utf-8', 'replace'))
ev = {
    'report_id': 2, 'kind': 'daily', 'key': c.get('date'),
    'window': [c.get('windowStart'), c.get('windowEnd')],
    'title': (c.get('lead') or {}).get('title'),
    'lead': (c.get('lead') or {}).get('leadParagraph'),
    'judged': len(c.get('judgedReports') or []),
    'selected': len(c.get('selectedReports') or []),
    'sections': len(c.get('sections') or []),
    'highlights': len(c.get('highlights') or []),
}
io.open(r'.c3-tmp\r1876_gate2_evidence.json', 'w', encoding='utf-8').write(
    json.dumps(ev, ensure_ascii=False, indent=1))
print('evidence written')
