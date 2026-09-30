# -*- coding: utf-8 -*-
# R748 status-export fix (outs[0] is a 2-tuple [label, text])
import io, json, re
from datetime import datetime

TS_FULL = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TS_HM = datetime.now().strftime('%H:%M')

c = io.open('src/os/state.json', encoding='utf-8').read()
m2 = re.search(r'"(2026-09-30 \d\d:\d\d R748: .*?)(?="\n ],)', c, re.S)
assert m2, 'R748 log row not found in state.json'
R748 = m2.group(1)

E = json.load(io.open('docs/status-export.json', encoding='utf-8'))
E['export_ts'] = TS_FULL
E['outs'][0][1] = ('tick 748，R748 生产轮·LC-019 周浩宇拆条收官腿毕=F-074 登记+冗余池第十六件落位（产品优先律对位=本轮实物增量=lc-019 成片 F-074 入成品库 74 件·'
 'R746/R747 断洞链承接：E4 8.0 断洞轮落地+ASR 双跑证伪 VAD 因果→R748 R711 型两段拼接根修 11 cues 全覆盖 44.9% 字位·E8 七席 ≥9+M4）'
 '——lane=E20 徐根福 standby 单条<2·补池义务随轮领·发布锁=M5 账号物理件不变（未上线=未测量）')
E['results'].insert(0, ['748', R748])
E['live'] = [
 ['当前活：LC-019 周浩宇拆条收官腿毕（R748）——F-074 登记=成品库第七十四件·冗余池第十六件落位（视频号冗余弹药 16 件）·lane=E20 徐根福 standby 单条<2·补池义务随轮领'],
 ['最近实物：lc-019-v1-shipinhao-60s.mp4 成品落位 output/renders/（57.235s·2026-09-30 ' + TS_HM + '）+评审单 review-20260930-lc019-v1.md+ASR 拼接证据件 .lc019-tmp/asr-check.srt'],
 ['下个里程碑：queue §E 补池选优入池（≤48h 窗·lane<2）·#70 OSS 窗 2 切片（≤10-02 21:40）·global-benchmarks 7 日刷（10-01 #80 并窗）'],
]
io.open('docs/status-export.json', 'w', encoding='utf-8').write(json.dumps(E, ensure_ascii=False, indent=1) + '\n')
print('EXPORT_OK', TS_FULL, '| results0=748 len', len(R748))
