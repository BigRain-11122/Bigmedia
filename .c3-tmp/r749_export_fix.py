# -*- coding: utf-8 -*-
# R749 export fix: correct structure (outs[0] is 2-elem; reuse state R749 log for results)
import io, json
from datetime import datetime

TS_FULL = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TS_HM = datetime.now().strftime('%H:%M')
DN = 93
pre_n = 942
post_est = 73

st = json.load(io.open('src/os/state.json', encoding='utf-8'))
R749 = st['log'][-1]
assert R749.startswith('2026-09-30') and 'R749:' in R749, 'state tail is not R749'

E = json.load(io.open('docs/status-export.json', encoding='utf-8'))
E['export_ts'] = TS_FULL
E['outs'][0][1] = ('tick 749，R749 收讫+回执轮·D-20260930 外审批 25+ 行收账（五查破静=decisions 行数锚陈旧→内容寻址重扫）——BigStream 相关行全过审零驳回；'
 'D-19 机制腿交付（iteration_prompt 投递层消费步+state decisions_watermark ' + str(DN) + ' 项基线+probe 改制）+XL-14 leg1（.c3-tmp 全批收账 dirty ' + str(pre_n) + '→' + str(post_est) + '）'
 '——余腿=sc003 tmp 族+达标复核（≤10-03）·真发布=blocked-on-CEO 账号物理件·发布锁=M5 不变')
E['results'].insert(0, ['749', R749])
E['live'] = [
 ['当前活：R749 收讫+回执轮毕——D-20260930 外审批收账+投递层机制腿（D-19 消费步+内容寻址水位 ' + str(DN) + ' 项基线）+XL-14 leg1 dirty 批账（' + str(pre_n) + '→' + str(post_est) + '·-uall）·下轮=#95 XL-14 余腿+queue §E 补池'],
 ['最近实物：output/reports/production-report-v1.md（产出报表三列 v1·XL-14 交付件·2026-09-30 ' + TS_HM + '）+F-074 lc-019 成片（R748 13:07·成品库第 74 件）'],
 ['下个里程碑：XL-14 dirty<50 达标（≤10-03）+D-19 验收窗（10-02 12:00）+queue §E 补池选优入池（≤48h）+global-benchmarks 刷新（10-01）'],
]
io.open('docs/status-export.json', 'w', encoding='utf-8').write(json.dumps(E, ensure_ascii=False, indent=1) + '\n')
json.load(io.open('docs/status-export.json', encoding='utf-8'))
print('EXPORT_OK')
