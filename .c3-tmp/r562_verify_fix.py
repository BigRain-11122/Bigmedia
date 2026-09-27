# -*- coding: utf-8 -*-
# R562 verify-fix: read-only round-trip re-verify, overwrite r562_verify.txt as UTF-8 (PS > redirect UTF-16 fix, R541 law; close script NOT re-run to avoid double-append)
import json, io

STATE = 'src/os/state.json'
EXP = 'docs/status-export.json'
s2 = json.load(io.open(STATE, encoding='utf-8'))
e2 = json.load(io.open(EXP, encoding='utf-8'))
lastline = s2['log'][-1]
eng = [d for d in e2['depts'] if d.get('n') == '工程技术部'][0]
lines = [
    'STATE_OK tick=%s ts=%s log_n=%d' % (s2['tick'], s2['ts'], len(s2['log'])),
    'EXPORT_OK ts=%s eng_s=%s eng_s_type=%s' % (e2['export_ts'], eng['s'], type(eng['s']).__name__),
    'TASK=%s' % s2['task'][:60],
    'LASTLOG_HEAD=%s' % lastline[:40],
    'LASTLOG_HAS_R562=%s' % ('R562' in lastline),
    'LASTLOG_COUNT_R562=%d' % sum(1 for l in s2['log'] if l.startswith('2026-09-27 21:53 R562:')),
    'FOCUS_HEAD=%s' % s2['focus'][:40],
    'FOCUS_HAS_R563=%s' % ('R563' in s2['focus']),
]
io.open('.c3-tmp/r562_verify.txt', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
