# -*- coding: utf-8 -*-
# R1353 P-61 export step: refresh export_ts + append results entry + live three rows (实况派生·F3 律)
import json, io, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP = os.path.join(ROOT, 'docs', 'status-export.json')

ex = json.load(io.open(EP, encoding='utf-8'))
ex['export_ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

res_entry = [
    '1353',
    u'2026-10-05 11:5x R1353: 生产轮·#86 a 腿三批台词池扩充批三 +19 条入志=city-spirit v1.3（64→83·六轴各 3+像素灵 1·'
    u'晨间/黄昏/高温/寒潮/开市/收市/令件/周末八场景首采·机核 19/19 PASS=verbatim 对 pools.json+零重+fleet 卡面级去重首扩零撞'
    u'〔DAILY v1-v67/REACT v1-v8/L-卡 cards 全量〕·R893「下批 supply-gated」供给判定被 fresh 全量重筛推翻=30+ 声明轮盲区修正'
    u'〔R666/R870/R970 判例族〕·剩余 414 候选密度显著降如实注·codex README 台账批 10 行+backlog #86 注·'
    u'产品优先律=1 分位实际文件改动·三探针 board 0F/readiness 3 阻塞外部 0 发现/loop_health 3F+138W 皆在案）'
    u'——详见 state.json log R1353 行'
]
# replace a pre-existing 1353 entry if present, else append
idx = next((i for i, r in enumerate(ex.get('results', [])) if r and r[0] == '1353'), None)
if idx is None:
    ex.setdefault('results', []).append(res_entry)
else:
    ex['results'][idx] = res_entry

now_hm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
ex['live'] = [
    [u'当前活：R1353 #86 a 腿三批台词池扩充批三交付毕=city-spirit v1.3 精神条 64→83（19 条谚语级精选+机核 19/19 PASS·'
     u'R893 供给判定 fresh 重筛推翻=盲区修正轮）；下一活=傍晚窗 DAILY v68 standby（~18:00）+今晚 OSS 窗 4 首切片（21:40）（%s）' % now_hm],
    [u'最近实物：data/storylines/codex/city-spirit.md v1.3（精神条 83 条·#65-83 十九条新增·2026-10-05 11:4x）；'
     u'上一件=MC-20261005-DAILY-v67 成品卡 F-154（06:2x）'],
    [u'下个里程碑：DAILY v68 傍晚窗 standby 兑现（怀旧/dusk/13·~18:00 后）+OSS 窗 4 首切片=收益透镜 3 型首用（21:40 后）'
     u'+REACT-v9 10-06 窗择优（10-06 日报先补产）+10-07 #57 替代率终报——窗 ≤48h']
]

io.open(EP, 'w', encoding='utf-8').write(json.dumps(ex, ensure_ascii=False, indent=1) + '\n')
print('export_ts=%s results=%d live=%d' % (ex['export_ts'], len(ex['results']), len(ex['live'])))
