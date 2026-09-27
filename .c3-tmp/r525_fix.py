# -*- coding: utf-8 -*-
# R525 close fix: restore trailing "35" CEO-order row dropped by digit-classification slip
import io, json, subprocess

REPO = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
se_path = REPO + r'\docs\status-export.json'
se = json.load(io.open(se_path, 'r', encoding='utf-8'))

head_txt = subprocess.check_output(['git', 'show', 'HEAD:docs/status-export.json']).decode('utf-8')
hse = json.loads(head_txt)
ceo_rows = [r for r in hse['results'] if r[0] == '35']
assert ceo_rows, 'CEO row not found in HEAD version'
ceo = ceo_rows[0]

if not any(r[0] == '35' for r in se['results']):
    se['results'].append(ceo)

with io.open(se_path, 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(se, fh, ensure_ascii=False, indent=1)

se2 = json.load(io.open(se_path, 'r', encoding='utf-8'))
assert [r[0] for r in se2['results']] == ['525', '524', '523', '522', '521', '520', '35'], 'results order FAIL'
print('FIX_OK results=' + ','.join(r[0] for r in se2['results']))
