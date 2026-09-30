# -*- coding: utf-8 -*-
"""Restore mis-inserted probe text from OLD entries (history-untouch redline),
then insert into R804 entries precisely (JSON-level, not raw text)."""
import io, json

PROBE = '三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面+决策 0 发现（bs-009 renders 行成品标注后 render-unannot 清零复核过）/loop_health 2 FAIL+99 WARN 皆在案史实（09-26/09-28 outage 已裁定+account-ahead tick804 vs beats801=崩轮断洞+声明轮无 beats 复合瞬态·下轮 beat 落地自平）；例行件：'
PLAIN = '例行件：'

# ---- state.json ----
p = 'src/os/state.json'
s = json.load(io.open(p, encoding='utf-8'))
logs = s['log']
hit_idx = [i for i, l in enumerate(logs) if PROBE in l]
assert len(hit_idx) == 1, ('state hits', hit_idx)
hi = hit_idx[0]
logs[hi] = logs[hi].replace(PROBE, PLAIN, 1)
print('state: restored log[%d], head=%r' % (hi, logs[hi][:40]))
assert hi != len(logs) - 1, 'mis-insert was already in R804?'
r804 = logs[-1]
assert r804.startswith('2026-10-01 03:2x R804:'), 'last log is R804'
assert r804.count(PLAIN) == 1, 'R804 例行件 count'
logs[-1] = r804.replace(PLAIN, PROBE, 1)
io.open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(s, ensure_ascii=False, indent=1) + '\n')
print('state.json: probe now in R804 entry only')

# ---- status-export.json ----
p = 'docs/status-export.json'
e = json.load(io.open(p, encoding='utf-8'))
res = e['results']
hit_r = [r for r in res if PROBE in str(r[1])]
assert len(hit_r) == 1, ('export hits', [r[0] for r in hit_r])
hr = hit_r[0]
assert hr[0] != '804', 'mis-insert was in 804?'
hr[1] = hr[1].replace(PROBE, PLAIN, 1)
print('export: restored result %s' % hr[0])
r804r = [r for r in res if r[0] == '804']
assert len(r804r) == 1 and r804r[0][1].count(PLAIN) == 1, '804 result anchor'
r804r[0][1] = r804r[0][1].replace(PLAIN, PROBE, 1)
io.open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(e, ensure_ascii=False, indent=1) + '\n')
print('status-export: probe now in 804 result only')
