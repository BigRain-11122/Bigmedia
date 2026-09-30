# -*- coding: utf-8 -*-
# R813 waiting-state declaration close (declaration window 3/6, no commit per os-protocol S6)
import io, datetime

P = r'src/os/state.json'
txt = io.open(P, encoding='utf-8').read()

now_full = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
now_min = datetime.datetime.now().strftime('%H:%M')

log_line = (
    "2026-10-01 " + now_min + " R813: 等待态声明收轮·声明轮并窗第 3 轮（五查全静=r807_scan.py 内容寻址复跑 06:53：orders 42=锚零新令〔顶=O-20260928-1910〕/"
    "ledger 六模式 40=锚带内〔值守行位移非事件·零 P-20260930+/P-20261001 行〕/decisions dnum 差集 0 新行=112 基线〔D-20260930-19 水位差集制·D-13 SLA 无触发〕/"
    "production=open 自愈核在位 tick812/无 index.lock 实核·树态维持=M CODELY.md〔18:55:34 平台记忆压缩波·R767 定谳·零接触不提交不回退〕"
    "+codex 两件〔README/city-humanities mtime 09-29 04:06 实读未动=#86 c+d 让位判据未达·bm-a 让位·两文件零接触〕"
    "+M state.json=声明轮并窗自账预期态〔R811/R812 行在途未 commit=并窗批量预期态〕+?? .c3-tmp 自产证据件〔r807_scan.txt 刷新+r811/r812_close.py 预期态〕〕"
    "+三探针=board 0 FAIL（5 ideas 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现（阻塞≠失败口径）/"
    "loop_health 3 FAIL+104 WARN 皆在案史实类（09-26 49min+09-28 609min outage 窗已裁定不重复触发+account-lag done813>tick812=本执行体在轮 beat 瞬态·tick813 收账自平）"
    "——可领序四项全时闸维持（R810 稿集通道收口·供给侧五面全闭·R757/R763/R810 供给实核在案禁重扫）：REACT 10-02 热点窗届日未到〔本轮 10-01 06:53·10-01 窗已占 F-077·R796〕/"
    "#70 OSS 窗 3=10-02 21:40 后开/#94 记忆梳理窗=10-04/W41 周轮件=10-05〔周报+自驱提案窗+CLOUD_LINE 首测〕/"
    "queue §E supply-gated 豁免面维持〔新锚卡 C-00030 零落位 anchors 止 C-00029+零新令级事件+REACT 下一窗 10-02+零新选题批注=五面恢复 0/5〕/"
    "#86 c+d 让位判据未达维持（codex mtime 09-29 04:06 未动·零接触）"
    "——三池复核随轮毕（queue 全读：A1-A5 全 done/B1-B4 done·B5 账号期门控=保护态豁免面在案/C1-C4 done·C4 常态位门控=进链件触发/"
    "§D 提案面 P-1 W40 窗件已终判·W41 提案窗=10-05 首周轮/§E 五面全闭 supply-gated）=四查尽·真无活可拉=一行声明合法〔P-2026-09-28-02 ②④序〕"
    "——例行件：export 06:24:37 在 24h 窗内不刷〔产品优先律 2·实况零变化〕·日报 10-01 在案不重跑〔R795·一份为真相〕/W40 周审在案〔R576〕/GB 闸 10-08〔R798 v1.2〕/"
    "T1 催办=已裁项停用口径/HQ-FEEDBACK 不写〔无集团层新 open 问题·dnum 差集 0 零膨胀〕·tokens:local=0（纯探针零模型调用·P-54⑤ 计量律如实记）"
    "——waiting: supply-gated lane held（卡点=新锚卡 C-00030+/新令级事件/REACT 10-02 窗/#70 窗 3 10-02 21:40/W41 10-05）ETA 2026-10-02。"
    "下轮=R814 可领序：①REACT 10-02 热点窗（届日领·10-02 日报缺=先补产 daily_brief 再领·当日一份为真相）②#70 OSS 窗 3（10-02 21:40 后开）"
    "③五面恢复任两路=补池复活④#86 c+d 让位判据〔并窗 3/6〕"
)

new_focus = (
    "R813: 等待态声明轮·可领序全时闸（供给侧五面全闭=R810 稿集通道收口·禁重扫·三池复核=A/B/C done+gated·§D W40 窗毕）——下轮 R814 可领序："
    "①REACT 10-02 热点窗（届日领·10-02 日报缺=先补产 daily_brief 再领·当日一份为真相·#59）"
    "②#70 OSS 窗 3 切片（10-02 21:40 后开·≤3 刀·下窗指针=Ollama 定向/字幕工艺/awesome-tts 生态 R798）"
    "③五面恢复任两路=补池复活（新锚卡 C-00030+/新令级事件/REACT 10-02 窗/新选题批注）"
    "④#86 c+d 让位判据（codex mtime 09-29 04:06 未动=未达·零接触）"
    "——五查锚=orders O-20260928-1910 42·ledger 六模式 40·decisions_watermark dnum 基线 112 项（内容寻址·D-20260930-18 禁行数）·"
    "声明轮并窗 3/6（窗满 6/6 或跨日 10-02 00:00 即 batch commit 区间 R811-首触轮）"
)

# task = log line minus timestamp prefix, first 60 chars
body = log_line.split(' R813: ', 1)[1]
task = body[:60]

# 1) tick 812 -> 813
old = '"tick": 812,'
assert txt.count(old) == 1, 'tick anchor not unique'
txt = txt.replace(old, '"tick": 813,')

# 2) append log line (anchor: closing quote of last log entry + array close + old ts line)
anchor = '"\n  ],\n  "ts": "2026-10-01 06:44:05",'
assert txt.count(anchor) == 1, 'log/ts anchor not unique'
repl = '",\n    "' + log_line + '"\n  ],\n  "ts": "' + now_full + '",'
txt = txt.replace(anchor, repl)

# 3) task line
old_task = '  "task": "等待态声明收轮·声明轮并窗第 2 轮（五查全静=r807_scan.py 内容寻址复跑 06:42：orders 42="'
assert txt.count(old_task) == 1, 'task anchor not unique'
txt = txt.replace(old_task, '  "task": "' + task + '"')

# 4) focus line (whole-line replace)
lines = txt.split('\n')
fi = [i for i, l in enumerate(lines) if l.startswith('  "focus": "R812:')]
assert len(fi) == 1, 'focus anchor not unique'
lines[fi[0]] = '  "focus": "' + new_focus + '",'
txt = '\n'.join(lines)

io.open(P, 'w', encoding='utf-8', newline='\n').write(txt)

# verify round-trip parses and key fields
import json
d = json.load(io.open(P, encoding='utf-8'))
print('CLOSE-OK tick=%d log_len=%d ts=%s' % (d['tick'], len(d['log']), d['ts']))
print('task=%s' % d['task'])
print('focus_head=%s' % d['focus'][:80])
print('last_log_head=%s' % d['log'][-1][:60])
