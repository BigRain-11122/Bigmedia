# -*- coding: utf-8 -*-
# r1356 export refresh: real-state change (group decision batch consumed) -> F3 law
# - export_ts refresh
# - live[0] current-action line updated (live[1] latest deliverable & live[2] milestones unchanged)
# - results append-only: add R1356 row
import json, io, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP = os.path.join(ROOT, 'docs', 'status-export.json')

ex = json.load(io.open(EP, encoding='utf-8'))
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
now_hm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')[:-1] + 'x'

ex['export_ts'] = now

live0 = ('当前活：R1356 集团决策批 D-20261005-06~11 六行消费+回执毕（科学判断闸全过审零驳回·涉司行 D-06=席 6 收讫注记零新执行面·'
         '派工板 +3 行 05①②③ 皆非本司面·水位 142→148）；下一活=傍晚窗 DAILY v68 standby（~18:00）+今晚 OSS 窗 4 首切片（21:40）（%s）' % now_hm)
assert ex['live'][0][0].startswith('当前活：'), 'live[0] unexpected: %s' % ex['live'][0][0][:20]
ex['live'][0][0] = live0

r1356 = ('2026-10-05 %s R1356: 集团决策批消费轮·decisions 水位差集 NEW=6（D-20261005-06~11·12:04 落账=12:00 班后派工当班消费合法·SLA 带内）'
         '科学判断闸全过审零驳回+回执（涉司行 D-06=本司席 6 确认收讫注记·执行面=值守轮 sweep 域零新执行面·D-07/08=bigmoney·D-09=HQ/BigLife·'
         'D-10=值守轮 orders 分卷 15:07 专窗·D-11=HQ 秘书处/BigDomain）+派工板 49→51（+D-20261005-05①②③ 皆非本司面·05① OSS 欠七实体不含本司=w3 义务已满）'
         '+水位 dnums 142→148+ack 三载体（commit 含 (a)D-20261005-06~11 (b)R1356 (c)下一动作 dusk v68→OSS w4）——异常即收独立 commit·'
         '车道门控承继（dusk DAILY v68 ~18:00/OSS w4 21:40/REACT-v9 10-06/#57 10-07）——详见 state.json log R1356 行' % now_hm)
nums = [r[0] for r in ex['results']]
assert '1356' not in nums, 'R1356 already in results'
ex['results'].append(['1356', r1356])

io.open(EP, 'w', encoding='utf-8').write(json.dumps(ex, ensure_ascii=False, indent=1) + '\n')
print('export_ts=%s live0=%d chars results=%d rows' % (ex['export_ts'], len(live0), len(ex['results'])))
