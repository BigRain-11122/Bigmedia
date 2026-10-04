# -*- coding: utf-8 -*-
# R1238 declared-idle close (window 3/6 after R1236 1/6, R1237 2/6; batch close commit at 6/6 per os-protocol sec.6)
import json, io, datetime, re

P = 'src/os/state.json'
d = json.load(io.open(P, encoding='utf-8'))
assert d['tick'] == 1237, 'tick drift: %s' % d['tick']

now = datetime.datetime.now()
stamp = now.strftime('%Y-%m-%d %H:%M')
ts = now.strftime('%Y-%m-%d %H:%M:%S')

line = (
    "%s R1238: declared-idle 一行声明收轮（五查静+探针+四查尽·P-2026-09-28-02 ②）·声明窗 3/6=R1237 顺位承接·"
    "五查 fresh 实证 .c3-tmp/r1238_check.txt 13:43（orders 顶=O-20260928-1910 未变 mtime 09-28 19:12/ledger @target 42=锚 mtime 10-04 03:23 平/"
    "decisions dnums 137==137 NEW=[] 板 46=锚/树净零锁·M state.json=自记账预期态+r1236~r1238 证据件=自产预期态）·"
    "三探针基线平（board 0 FAIL·5 题 10 稿 5 in production/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 3 FAIL+131 WARN 在案史实·account-lag +4 恒偏移）·"
    "全 lane 时序闸 10-05 日界批（10-05 日报补产+E31 REACT-v9 择优 F-151+W41 周轮件〔周报+自驱提案窗+CLOUD_LINE 首测+#94②〕+#70 OSS w4 21:40）·"
    "保护态豁免面在案（素材窗 blocked：CENSUS C-00030 锚轮首核不在位+DAILY/REACT 供给面耗尽待 BigLife 台词池扩容〔R1160 池扩容呈报在案〕/"
    "门控型任务/CEO 物理件=呈现状行不催办）——禁每轮重扫同一等待对象·export 不刷（03:37 <24h flat·F3 律）·"
    "无 commit（声明窗 3/6·并窗律 os-protocol §6·批闭 6/6 收·r1236~r1238 证据件随批闭卷入）"
) % stamp

d['tick'] = 1238
d['ts'] = ts
m = re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2} R\d+: (.*)$', line, re.S)
task_src = m.group(1)
d['task'] = task_src[:60]
d['focus'] = ('R1238: declared-idle 声明窗 3/6（五查静+探针基线平+全 lane 时序闸 10-05 日界批'
              '〔10-05 日报补产+E31 REACT-v9 F-151+W41 周轮件+#70 OSS w4〕·保护态豁免面在案）')
d['log'].append(line)

io.open(P, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print('tick=%d ts=%s task=%s' % (d['tick'], d['ts'], d['task']))
