# -*- coding: utf-8 -*-
# R433 idle-fast close (five checks static + probes green under adjudicated口径):
# state tick/log/ts/task + focus R434 (window 1/6 R433-R438) + status-export export_ts (P-61)
import json, datetime, io

SP = 'src/os/state.json'
EP = 'docs/status-export.json'

now = datetime.datetime.now()
stamp = now.strftime('%Y-%m-%d %H:%M')
ts = now.strftime('%Y-%m-%d %H:%M:%S')

logline = (
    f"{stamp} R433: idle-fast（快速路径·五静+探针绿 1 FAIL 定谳在案史实·不进开轮四步·并窗轮 1/6 不 commit）——"
    "①无新令（orders 顶=O-20260925-1931-HQ-C·R283 已记账·O- 前缀核验排除 README.md 排序伪差〔r433_check.py orders_new_after_anchor 仅 README.md 一件〕）"
    "②backlog 顶行不可认领（#70 OH 切片 2=窗内随轮领但节律判定不领：切片 1 已于 22:13 交付〔首窗「每窗 ≥1 切片」义务已满足·实搜 2 面+候选 1 项五门评估全落〕·CEO 令节律=每 3 天寻找一次·切片 1 落地后 ~10 分钟即换刀重搜=零新发现面自我膨胀〔反膨胀律〕·切片 2 按 OH 台账下窗指针 ≤09-29 21:40 随窗领〔换刀=ffmpeg drawtext cjk/awesome-tts 生态/Ollama library 预检·礼貌节流单窗 ≤3 刀〕·"
    "#67 DIGEST 编年史候选=research §5 在册三件已耗尽〔开闸 F-042/三线 F-043/技能动员 F-044 全制毕〕+ledger 零新 CEO 令级事件=无候选不硬造〔反膨胀律〕·"
    "#63 图鉴 C-00030 锚正典位轮首核=仍不在位〔r433_check.py anchor_C00030 False+C-00031 同核 False 双证·anchors 尾三=C-00027/C-00028/C-00029 止 C-00029〕supply-gated 维持·"
    "#59 REACT 新热点窗=09-27 日报〔明日届日即领〕·#21 周日立法件=09-27 届日〔明日周日届日即领〕·#57 替代率首报 10-07 窗挂账·#66③ 常态门控面·"
    "自进池 open 真锚项全闭〔A 池全 done+B 池 B1-B4 done·B5 账号期门控+C 池 C1-C3 done·C4 常态位 blocked on 进链件〕）"
    "③树净零锁（HEAD=7c23b15=R432 收账 commit·git log 7c23b15..HEAD 零插队=无 bm-a 活跃写盘迹象〔r433_check.py inserts_after_7c23b15 0 实证〕·本轮自产 M state.json+M status-export.json+?? .c3-tmp/r433_check.py+r433_probe.txt+r433_close.py=并窗自记账预期态随窗满批 commit〔窗 R433-R438〕）"
    "④ch.5 v3 稿未落（storylines python walk 扫描 novel/audio/comic 三子域 09-26 零新写盘实证〔r433_check.py 读数 0/0/0〕=ch.5 判定口径成立·bm-a 面）·"
    "日报 2026-09-26 在案不重跑（r433_check.py daily_brief_0926 True 实证）·W39 周审在案；"
    "集团双锚静=ledger @ 五模式 25=锚零新转办（r433_check.py python 计数 25 实证·尾=P-20260926-08 R429 已收讫）·"
    "decisions python 非空行 40=锚〔尾=D-20260926-11 R377 已定谳〕零新行零新动作；"
    "loop_health 1 FAIL 定谳在案史实（同事件历史足迹·非新异常·零新增）：heartbeat-outage 49min gap（20:24→21:13）=R425 定谳调度器漏触发静默窗同事件足迹〔R426 已裁定列在案史实·beat 文件永久历史记录·fast-path 不重复触发提前收账〕——"
    "beat+ts 收账即鲜续证四连（R432 beat 22:13 落地 beats 436·state ts 22:13:44 距本轮探针 ~10min 鲜窗·heartbeat-stale/state-ts-stale 双清零维持）；"
    "三探针=board 0 FAIL 5 题 10 稿 5 in production exit 0/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现=阻塞≠失败口径 exit 1〔renders 42 件台账全注账〕/"
    "loop_health 1 FAIL〔同事件足迹在案史实〕+20 WARN 皆在案史实〔12 log-order+8 heartbeat-gap〕·tick432=done432 对账平〔beats 436 含 skip 4〕·log 444 条·backlog 71 项 58 done 82% 燃尽）；"
    "例行件=global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·"
    "tokens:local=0（零本地模型调用·探针纯脚本·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）——"
    "一行收账即出（idle-fast 并窗轮 1/6〔窗 R433-R438 满 6 收账〕·本轮不 commit·P-61 导出步照刷 export_ts）。"
    "下轮快速路径首查：#21 周日立法件 09-27 届日即领/REACT 09-27 日报热点窗届日即领/#70 OH 切片 2（≤09-29 21:40 换刀）/图鉴 C-00030 锚/ch.5 v3 稿落迹象/新令/集团转办——全静即 idle-fast（2/6）。"
)

with io.open(SP, encoding='utf-8') as f:
    st = json.load(f)
assert st['tick'] == 432, st['tick']
st['tick'] = 433
old_focus = st['focus']
assert old_focus.startswith('R433:'), old_focus[:40]
new_focus = old_focus.replace('R433:', 'R434:', 1)
assert new_focus != old_focus
new_focus2 = new_focus.replace('新窗 1/6〔R433-R438〕', '2/6〔R433-R438〕', 1)
assert new_focus2 != new_focus, 'window counter 1/6 -> 2/6 replace failed'
st['focus'] = new_focus2
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

print('R433 close ok')
print('ts=' + ts)
print('task=' + st['task'])
print('export_ts=' + ex['export_ts'])
print('focus_head=' + new_focus2[:30])
print('focus_tail=' + new_focus2[-40:])
print('log_entries=' + str(len(st['log'])))
