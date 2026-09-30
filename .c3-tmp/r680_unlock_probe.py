# -*- coding: utf-8 -*-
# R680: backlog #89 unlock note + post-render probe rerun (board/readiness/loop_health)
import io, subprocess, os, re

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
P = ROOT + r'\src\os\backlog.md'
t = io.open(P, encoding='utf-8').read()
OLD = u"——ack=本行+commit 含令号（P-51 送达）"
assert t.count(OLD) == 1, 'anchor count=%d' % t.count(OLD)
NEW = (u"——ack=本行+commit 含令号（P-51 送达）"
       u"——**[R680 过会核收 2026-09-29：委员会 C-20260929-01 表决=7/7 有条件赞成（普通过 ≥4/7·全员附款随案生效"
       u"·decisions.md 委员会节行落·CEO 翻案权保留·否决窗至 10-06）→票后派发腿解锁=下轮可领序第二位"
       u"（R681 LC-002 收官腿首位后·三径闸 mandate 接线+attribution 单字段发射前必填+周轮云端行聚合三件按 #89 ①②③ 领做）]**")
t = t.replace(OLD, NEW)
io.open(P, 'w', encoding='utf-8').write(t)
print('backlog #89 ok')

# post-render probe rerun
def run(args, outfile):
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    r = subprocess.run(['python', '-X', 'utf8'] + args, cwd=ROOT, capture_output=True, env=env)
    txt = r.stdout.decode('utf-8', errors='replace')
    io.open(outfile, 'w', encoding='utf-8').write(txt + '\n[rc]=' + str(r.returncode) + '\n')
    return txt, r.returncode

b, rc1 = run(['src/board_check.py'], ROOT + r'\.c3-tmp\r680_board2.txt')
rd, rc2 = run(['src/readiness.py'], ROOT + r'\.c3-tmp\r680_readiness2.txt')
h, rc3 = run(['src/os/loop_health.py'], ROOT + r'\.c3-tmp\r680_health2.txt')
print('rc: board=%d readiness=%d health=%d' % (rc1, rc2, rc3))
for name, txt in [('BOARD', b), ('READINESS', rd), ('HEALTH', h)]:
    print('== ' + name)
    for l in txt.splitlines():
        if re.search(r'FAIL|blocker|finding|loop health|summary', l, re.I):
            print('  ' + l[:180])
