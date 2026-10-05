# -*- coding: utf-8 -*-
# R1354 export refresh (P-61): export_ts + live three lines + results row (F3 law: derive from actual round)
import json, io, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP = os.path.join(ROOT, 'docs', 'status-export.json')

ex = json.load(io.open(EP, encoding='utf-8'))
ex['export_ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

res_row = [
    "1354",
    u"2026-10-05 11:5x R1354: 生产轮·#86 a 腿四批台词池扩充批四 +17 条入志=city-spirit v1.4（83→100·"
    u"侠气 3+怀旧 5+烟火 2+秩序 5+逍遥 2·求新/像素灵零入选如实注·近孪剔除面首立〔verbatim 前缀行 2+主题孪行 5+主题饱和 2〕·"
    u"机核 17/17 PASS=verbatim 对 pools.json+对 #1-83 零重+三志在册面+fleet 卡面级去重承继零撞〔r1354_verify.txt〕·"
    u"四批累计谚语级现量采掘毕=下批待 BigLife 池扩容 fresh 重筛〔不预立律〕·codex README 台账批 12 行+backlog #86 注·"
    u"产品优先律=1 分位实际文件改动·三探针 board 0F/readiness 3 阻塞外部 0 发现/loop_health 3F+138W 基线平）——详见 state.json log R1354 行"
]
# keep results bounded: drop oldest if > 40 entries
if len(ex.get('results', [])) > 40:
    ex['results'] = ex['results'][-40:]
ex.setdefault('results', []).append(res_row)

ex['live'] = [
    [u"当前活：R1354 #86 a 腿四批台词池扩充批四交付毕=city-spirit v1.4 精神条 83→100（17 条谚语级尾部批+机核 17/17 PASS·四批累计谚语级现量采掘毕=下批待池扩容）；下一活=傍晚窗 DAILY v68 standby（~18:00）+今晚 OSS 窗 4 首切片（21:40）（2026-10-05 12:0x）"],
    [u"最近实物：data/storylines/codex/city-spirit.md v1.4（精神条 100 条·#84-100 十七条新增·2026-10-05 11:5x）；上一件=MC-20261005-DAILY-v67 成品卡 F-154（06:2x）"],
    [u"下个里程碑：DAILY v68 傍晚窗 standby 兑现（怀旧/dusk/13·~18:00 后）+OSS 窗 4 首切片=收益透镜 3 型首用（21:40 后）+REACT-v9 10-06 窗择优（10-06 日报先补产）+10-07 #57 替代率终报——窗 ≤48h"]
]

io.open(EP, 'w', encoding='utf-8').write(json.dumps(ex, ensure_ascii=False, indent=1) + '\n')
print('export_ts=%s results=%d live=%d' % (ex['export_ts'], len(ex['results']), len(ex['live'])))
