# -*- coding: utf-8 -*-
"""R659 fix: rebuild status-export.json from HEAD version (restore 22-row history + indent=1 format), re-apply R659 updates."""
import io, os, json, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

h = subprocess.run(['git', 'show', 'HEAD:docs/status-export.json'], capture_output=True).stdout.decode('utf-8')
e = json.loads(h)
assert len(e.get('results', [])) == 22, "unexpected HEAD results count: %s" % len(e.get('results', []))

import datetime
now = datetime.datetime.now()
export_ts = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

e['export_ts'] = export_ts
e['results'].append(["659", "R659 declared-idle 空轮判定（五静+探针绿+可领序尽·窗 1/6）：五查锚静（orders O-1910/ledger 34 rowdiff 0/decisions 68）·bm-a codex 批未闭让位维持（+3/+14 worktree 态·R651 补记 staged 读数更正=双 plumbing 复核 staged 面=空）·供给面专项核验三源全负定谳（a 腿 pools.json 叶数 1440=1440 零增量源闭/b 腿 registry ~9503 张=R316 裁定非手写锚·anchors 止 C-00029 supply-gated 照守/c 腿让位+二轮深采毕）·可领序尽（#86 四腿 gated/#70 未到窗/#67 零新事件/queue gated/W40 提案已交）=保护态豁免面在案·三探针 board 0F/readiness 3 外部 0 发现/loop 在案类·tokens:local=0·下轮可领序 #86 让位判据/#70 21:40/#67 触发律"])

osrow = None
for row in e.get('outs', []):
    if row and row[0] == 'OS 循环':
        osrow = row
        break
assert osrow is not None, "OS row missing"
osrow[1] = "tick 659：R659 declared-idle 空轮判定（五静+探针绿+可领序尽·P-02 ②④序·窗 1/6=R659-R664）：供给面三源核验全负（a 腿源闭 1440=1440/b 腿 registry 9503 张 R316 裁定非手写锚·anchors 止 C-00029/c 腿让位）·bm-a codex 批未闭让位维持·三探针 board 0F/readiness 3 皆外部/loop 在案类·tokens:local=0——下轮 R660 可领序=①#86（bm-a 批闭判据）②#70 切片 2（21:40 后）③#67 触发律"

io.open('docs/status-export.json', 'w', encoding='utf-8').write(json.dumps(e, ensure_ascii=False, indent=1))

# verify: history restored + format matched + updates in place
c = json.load(io.open('docs/status-export.json', encoding='utf-8'))
raw = io.open('docs/status-export.json', encoding='utf-8').read()
d = json.load(io.open('src/os/state.json', encoding='utf-8'))
out = io.open(os.path.join('.c3-tmp', 'r659_verify2.txt'), 'w', encoding='utf-8')
checks = {
    'results_n_23': len(c['results']) == 23,
    'results_first_658': c['results'][0][0] == '658',
    'results_last_659': c['results'][-1][0] == '659',
    'history_578_restored': any(r[0] == '578' for r in c['results']),
    'export_ts_fresh': c['export_ts'] == export_ts,
    'os_row_659': any(r[0] == 'OS 循环' and 'tick 659' in r[1] for r in c['outs']),
    'indent1_line': raw.splitlines()[2].startswith('  "do"') is False and raw.splitlines()[1].startswith(' "do"'),
    'raw_chinese': '\u5a92' in raw[:2000],
    'state_tick_659': d['tick'] == 659,
    'state_focus_r660': d['focus'].startswith('R660:'),
}
allok = True
for k, v in checks.items():
    out.write('%s %s\n' % (k, 'PASS' if v else 'FAIL'))
    allok = allok and v
out.write('ALL_PASS %s\n' % allok)
out.close()
print('results n=%d ALL_PASS=%s' % (len(c['results']), allok))
sys.exit(0 if allok else 1)
