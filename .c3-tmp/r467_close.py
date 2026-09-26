# -*- coding: utf-8 -*-
# R467 idle-fast close: state.json tick/log/ts/task + focus R468 (win 5/6) + status-export export_ts (P-61)
import json, datetime, io

SP = 'src/os/state.json'
EP = 'docs/status-export.json'
V = '.c3-tmp/r467_verify.txt'

now = datetime.datetime.now()
stamp = now.strftime('%Y-%m-%d %H:%M')
ts = now.strftime('%Y-%m-%d %H:%M:%S')

logline = (
    stamp + " R467: idle-fast（快速路径·五静+探针定谳绿·不进开轮四步·并窗轮 5/6 不 commit）——"
    "①无新令（orders O- 前缀核验=r467_check·锚=O-20260925-1931-HQ-C·O- 34 件零新增·orders_edited_since_anchor NONE=D-20260927-05② 检测线绿）+"
    "无新集团转办（ledger 五模式 29=锚零新行·r467_check python 计数实证·内容寻址勿全文重读）+"
    "无新决策行（decisions UTF8 非空行 45=锚·D-20260927-01~05 批后零新）；"
    "②backlog 顶行不可认领（#74/#71/#73 done·#72 素材消费面知悉挂账〔BigLife 互聊台账 ≤09-28 12:00 到位前零动作〕·"
    "#59 REACT 09-27 窗已毕〔R456 F-045〕09-28 窗届日即领〔daily_brief 09-28 缺则先补产〕·"
    "#63 图鉴 C-00030/C-00031 锚正典位轮首核均不在位〔r467_check anchor_C00030/31 False 双证·anchors 尾三止 C-00029〕supply-gated 维持·"
    "#70 OH 下窗 09-29 21:40 后开〔首窗三切片 R432/R458/R459 齐=窗面满〕·#57 替代率首报 10-07 挂账·"
    "W40 周自审 09-28 开周+月度统计注记首件 ≤09-30 随 W40 周审轮·"
    "#67 DIGEST 史源耗尽待 ledger 新 CEO 令级事件〔反膨胀律照守〕·自进池 open 项全门控〔B5 账号期站内采样/B3 周更 W40/C4 首进链件触发位〕）；"
    "③树态=仅自产预期件（无 index.lock r467_check False 实证·树态=M state.json+M status-export.json=R463~R466 idle-fast 并窗自记账预期态非 bm-a 迹象+"
    "untracked .c3-tmp r463~r467 证据件随并窗批 commit〔窗 R463-R468〕·"
    "storylines 三子域 04:44 后零新写盘 0/0/0=r467_check·HEAD=662686f 未变 git log 零插队=无 bm-a 活跃写盘迹象）；"
    "④例行件：日报 09-27 在案不重跑（R443 补产件）·W39 周审在案（W40 明日 09-28 开周）·"
    "global-benchmarks day3 ≤7 跳过（下期 ~10-01 并窗 M4/S4 门参数复核=R457 调研部首件选题窗）·"
    "T1 催办=已裁项停用口径·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀·ledger/decisions 双锚静）·"
    "tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）；"
    "三探针定谳=board 0 FAIL（5 题 10 稿·5 in production·exit 0）/"
    "readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1〔46 renders 全注账〕/"
    "loop_health 2 FAIL+21 WARN 全定谳在案类零新增（FAIL① heartbeat-outage 49min=R425 调度器漏触发同事件足迹 R426 已裁定·"
    "FAIL② account-lag done467>tick466=+1 恒态足迹〔03-26 中断执行体 done-beat·R459/R462 在案·新断洞判据 lag ≥2·本轮 lag=+1 未破线零新断洞〕·"
    "21 WARN=13 log-order+8 heartbeat-gap 全 ≤09-27 03:15 史实零新增·backlog 75 项 61 done 81% 燃尽）——"
    "探针复制律第五证（r467_check.py/r467_probes.py/r467_state_tail.md=write_file 新建+OUTP 改指·零 PS 往返零历史件覆写="
    "R462 防再犯律+R466 write_file 预核 tracked 态律双守·本轮零操作红）；"
    "一行收账即出（idle-fast 并窗轮 5/6〔窗 R463-R468 满 6 收账·跨日边界 09-28 00:00 先到即收〕·本轮不 commit·P-61 导出步照刷 export_ts 轻量）。"
    "下轮=R468 并窗 6/6 窗满收账 commit（区间消息注明 R463-R468 idle-fast batch·窗重置 1/6）+"
    "#59 REACT 09-28 热点窗届日领（daily_brief 09-28 缺则先补产）/W40 周自审开周+月度统计注记首件（09-28 起·docs/audits/2026-W40-self-audit.md 缺任意轮补产）/"
    "图鉴 C-00030 锚/新令/集团转办——异常或实活轮出现即提前收账。"
)

with io.open(SP, encoding='utf-8') as f:
    st = json.load(f)
assert st['tick'] == 466, st['tick']
st['tick'] = 467
old_focus = st['focus']
assert old_focus.startswith('R467:'), old_focus[:40]
new_focus = old_focus.replace('R467:', 'R468:', 1)
new_focus = new_focus.replace('（并窗 4/6·R463 起算）', '（并窗 5/6·R463 起算）', 1)
assert 'R468:' in new_focus and '5/6' in new_focus, new_focus[:60]
st['focus'] = new_focus
st['log'].append(logline)
st['ts'] = ts
st['task'] = logline.split(' ', 3)[3][:60]

with io.open(SP, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(st, f, ensure_ascii=False, indent=1)
    f.write('\n')

with io.open(EP, encoding='utf-8') as f:
    ex = json.load(f)
ex['export_ts'] = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
with io.open(EP, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(ex, f, ensure_ascii=False, indent=1)
    f.write('\n')

# post-close verify dump (UTF-8, read back via read_file per encoding law)
st2 = json.load(io.open(SP, encoding='utf-8'))
with io.open(V, 'w', encoding='utf-8') as f:
    f.write('tick=%s\nts=%s\ntask=%s\ntask_len=%d\n' % (st2['tick'], st2['ts'], st2['task'], len(st2['task'])))
    f.write('focus_head=%s\n' % st2['focus'][:80])
    f.write('focus_tail=%s\n' % st2['focus'][-90:])
    f.write('log_len=%d\n' % len(st2['log']))
    f.write('last_log_head=%s\n' % st2['log'][-1][:120])
    f.write('prev_log_head=%s\n' % st2['log'][-2][:80])
    f.write('production=%s\n' % st2['production'])
    f.write('export_ts=%s\n' % ex['export_ts'])

print('R467 close ok')
print('ts=' + ts)
print('tick=' + str(st2['tick']))
