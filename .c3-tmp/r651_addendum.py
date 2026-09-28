# -*- coding: utf-8 -*-
# R651+R652 round-end addendum: readout correction (honesty law, append-only)
import io, json, datetime

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
now = datetime.datetime.now()
ts_str = now.strftime('%Y-%m-%d %H:%M:%S')
ts_min = now.strftime('%H:%M')

addendum = (
    "2026-09-29 " + ts_min + " R651+R652 轮末补记（读数更正·诚实律·追加制原行不改写）——"
    "①codex zone 读数更正=前句「city-humanities staged +14 worktree 再 +17 增写」系误读（+31 层=R650 自身 commit a548635 的 stat 混入·非 worktree 增量）；git diff --cached 与 git diff 双 plumbing 复核定谳=bm-a staged 件恰为 README +3/city-humanities +14 且 worktree==index（mtime 04:06:09-16=04:06 落盘 staged 未闭批态·「活跃写盘增写中」定性收窄为「04:06 落盘未闭批」——让位判定不变：五维计数台账共享面 staged 未提交=认领制让位照立·R20 先例）；"
    "②本循环 pathspec commit 零卷入零丢失复核=commit 128083d 前后 diff --cached 读数一致（README +3/city-humanities +14 staged 态原样保留·bm-a 批闭时自行 commit 不受影响·R19 教训①「显式列文件」执法闭环）；"
    "③status-export outs/results 同步更正（+17 伪数清除·F3 律实况派生）；周报双件生成于更正前但其数据源=state git 源机械生成不含该伪数（零涉及）"
)

sp = ROOT + r'\src\os\state.json'
with io.open(sp, encoding='utf-8') as f:
    state = json.load(f)
assert state['tick'] == 652, state['tick']
state['log'].append(addendum)
state['ts'] = ts_str
with io.open(sp, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)
    f.write('\n')
print('state.json addendum appended, log entries:', len(state['log']))

xp = ROOT + r'\docs\status-export.json'
with io.open(xp, encoding='utf-8') as f:
    exp = json.load(f)
exp['export_ts'] = now.strftime('%Y-%m-%dT%H:%M:%S') + '+08:00'
fixed0 = 0
if 'worktree 再 +17' in exp['outs'][0][1]:
    exp['outs'][0][1] = exp['outs'][0][1].replace(
        'city-humanities staged +14 worktree 再 +17·mtime 04:06·R650 收账后新发生',
        'city-humanities staged +14·worktree==index·mtime 04:06=R650 收账后新发生 staged 未闭批')
    fixed0 += 1
if 'worktree 再 +17' in exp['results'][0][1]:
    exp['results'][0][1] = exp['results'][0][1].replace(
        'city-humanities staged +14 worktree 再 +17 mtime 04:06:09·vs HEAD a548635 R650 收账 03:58:59 后新发生',
        'city-humanities staged +14·worktree==index·mtime 04:06:09-16 vs HEAD a548635=R650 收账 03:58:59 后新发生 staged 未闭批〔读数更正见 R651+R652 轮末补记〕')
    fixed0 += 1
with io.open(xp, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(exp, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('status-export.json corrected fields:', fixed0, 'export_ts:', exp['export_ts'])
