# -*- coding: utf-8 -*-
# R415 idle-fast close (window 3/6 of R413-R418, no commit): state.json tick/log/ts/task + status-export export_ts (P-61)
import json, datetime, io

SP = 'src/os/state.json'
EP = 'docs/status-export.json'

now = datetime.datetime.now()
stamp = now.strftime('%Y-%m-%d %H:%M')
ts = now.strftime('%Y-%m-%d %H:%M:%S')

logline = (
    f"{stamp} R415: idle-fast（快速路径·五静+探针绿·不进开轮四步·并窗轮 3/6 不 commit）——"
    "①无新令（orders 顶=O-20260925-1931-HQ-C·R283 已记账·O- 前缀核验排除 README.md 排序伪差）"
    "②backlog 顶行不可认领（#67 DIGEST 编年史候选=research §5 在册三件已耗尽〔开闸 F-042/三线 F-043/技能动员 F-044 全制毕〕+ledger 零新 CEO 令级事件=无候选不硬造〔反膨胀律〕·"
    "#63 图鉴 C-00030 锚正典位轮首核=仍不在位〔r415_check.py anchor_C00030 False+C-00031 同核 False 双证·anchors 尾三=C-00027/C-00028/C-00029 止 C-00029〕supply-gated 维持·"
    "#59 REACT 新热点窗=09-27 日报〔明日届日即领〕·#21 周日立法件=09-27 届日〔明日周日届日即领〕·#57 替代率首报 10-07 窗挂账·#66③ 常态门控面·"
    "自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕）"
    "③树态=仅自产预期件（M state.json+M status-export.json=R414 idle-fast 并窗自记账预期态·?? .c3-tmp/r413_check.py+r413_check.txt+r413_close.py+r413_probe.txt+r414_check.py+r414_check.txt+r414_probe.txt+r414_close.py+r415_check.py+r415_check.txt+r415_probe.txt 自产脚本/证据件随窗满批 commit〔窗 R413-R418〕·无 index.lock r415_check.py False 实证·HEAD=7b15061 未变·7b15061 后零插队=无 bm-a 活跃写盘迹象）"
    "④ch.5 v3 稿未落（storylines python walk 扫描 novel/audio/comic 三子域 09-26 零新写盘实证〔r415_check.py 读数 0/0/0〕=ch.5 判定口径成立·bm-a 面）·"
    "日报 2026-09-26 在案不重跑（r415_check.py daily_brief_0926 True 实证）·W39 周审在案；"
    "集团双锚静=ledger @ 五模式 23=锚零新转办（r415_check.py python 计数 23 实证·尾=P-20260926-03 R377 已收讫）·"
    "decisions python 非空行 40=锚〔尾=D-20260926-11 R377 已定谳〕零新行零动作；"
    "三探针全绿（board 0 FAIL 5 题 10 稿 5 in production exit 0/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1〔renders 42/42 注账〕/"
    "loop_health 0 FAIL 20 WARN 皆在案史实〔12 log-order+8 heartbeat-gap〕·tick414=done414 对账平〔beats 418 含 skip 4〕）；"
    "例行件=global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·"
    "tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）——"
    "一行收账即出（idle-fast 并窗轮 3/6〔窗 R413-R418 满 6 收账〕·本轮不 commit·P-61 导出步照刷 export_ts）。"
    "下轮快速路径首查：#21 周日立法件（09-27 周日届日即领·周日周轮立法流程）/REACT 09-27 日报热点窗届日即领/图鉴 C-00030 锚/ch.5 v3 稿落迹象/新令/集团转办——全静即 idle-fast（4/6）。"
)

with io.open(SP, encoding='utf-8') as f:
    st = json.load(f)
assert st['tick'] == 414, st['tick']
st['tick'] = 415
old_focus = st['focus']
assert old_focus.startswith('R415:'), old_focus[:40]
new_focus = old_focus.replace('R415:', 'R416:', 1)
new_focus = new_focus.replace('全静即 idle-fast（3/6〔窗 R413-R418〕）', '全静即 idle-fast（4/6〔窗 R413-R418〕）', 1)
assert new_focus != old_focus
st['focus'] = new_focus
st['log'].append(logline)
st['ts'] = ts
st['task'] = logline.split(' ', 2)[2][:60]

with io.open(SP, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
    f.write('\n')

with io.open(EP, encoding='utf-8') as f:
    ex = json.load(f)
ex['export_ts'] = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
with io.open(EP, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(ex, f, ensure_ascii=False, indent=1)
    f.write('\n')

print('R415 close ok')
print('ts=' + ts)
print('task=' + st['task'])
print('export_ts=' + ex['export_ts'])
