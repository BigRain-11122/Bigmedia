# -*- coding: utf-8 -*-
# R870 E4 same-round backfill: expert-verdicts archive + review/finished/README/station/state updates
import io, json

E4 = json.load(io.open('data/storylines/cards/MC-20261001-DIGEST-v11-tmp/e4-result.json', encoding='utf-8'))
verdict = E4['verdict'].strip()
ts = E4['ts']  # 2026-10-01 16:43:25 wrapper start

# 1) expert-verdicts archive (net verdict)
ev = (
    u'# E4 参考仪判词净本 · MC-20261001-DIGEST-v11《城市盘点 011·产品优先令数字盘点》（R870 同轮回填）\n\n'
    u'- 起飞：{}（Start-Process 脱壳 PID 80000·本地 Ollama qwen2.5:14b·零 API token）\n'
    u'- 评分：8.0（会停下来看=明说；打 8 分=明说；保存/转发=条件式如实〔对 AI 管理与企业运营感兴趣的读者会保存·不感兴趣只浏览〕）\n'
    u'- 正面定性：「内容具有一定的信息量和故事性，能够引发读者的好奇心」「信息丰富且具有一定的实用性和阅读价值」\n'
    u'- 信任面：「这张卡的内容中没有一眼假或空洞套话的地方」=正面明说\n'
    u'- 旗①：「立制：实物 2 分 · 改动 1 分 · 纯记账 0 分」行缺评分对象语境（扣分旗=MC-003 语境门槛族压缩变体·'
    u'立法原文 verbatim 不可改写·吸收位=M5 图文页语境）\n'
    u'- 最弱：46% 簿记占比缺转化语境（DIGEST 形态边界=数字盘点卡固有·M5 图文页正解）\n'
    u'- 净本（判词原文）：\n\n```\n{}\n```\n'
).format(ts, verdict)
io.open('expert-verdicts/20261001-164325-E4-audience.md', 'w', encoding='utf-8').write(ev)

E4_OLD_FIN = (
    u'E4 参考仪 **异步在飞**（Start-Process 脱壳 PID 80000·1500s 窗·下轮回填=R517→R518/R577→R578/'
    u'R631→R632/R682 追加制先例·非拦截席）')
E4_NEW_FIN = (
    u'E4 参考仪 **同轮回填毕 8.0**（16:43:25 起飞热载快落=R643/R674/R682 先例·会停下来看+打 8 分=明说·'
    u'保存/转发条件式如实〔R293 型〕·「没有一眼假或空洞套话的地方」=信任面正面明说·'
    u'旗①=「立制三档」行缺评分对象语境〔MC-003 语境门槛族压缩变体·立法原文 verbatim 不可改写·吸收位=M5 图文页语境〕·'
    u'最弱=46% 占比缺转化语境〔DIGEST 形态边界·M5 图文页正解〕·'
    u'**DIGEST 带 v2-v11 十连 8.0 持平〔v1 9.0 峰带内〕**·净本 expert-verdicts/20261001-164325-E4-audience.md·非拦截席）')

# 2) finished.md
p = 'output/finished.md'
t = io.open(p, encoding='utf-8').read()
assert E4_OLD_FIN in t, 'finished E4 anchor missing'
t = t.replace(E4_OLD_FIN, E4_NEW_FIN, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('FIN-OK')

# 3) cards README
p = 'data/storylines/cards/README.md'
t = io.open(p, encoding='utf-8').read()
old_r = (u'E4 异步在飞（Start-Process 脱壳 PID 80000·'
         u'下轮回填 R682 追加制先例）')
new_r = (u'E4 同轮回填 8.0（16:43:25 热载快落·会停+打 8 分明说·保存/转发条件式·零一眼假明说·'
         u'DIGEST 带 v2-v11 十连 8.0 持平·旗①=立制行语境〔M5 吸收位〕·'
         u'净本 expert-verdicts/20261001-164325-E4-audience.md）')
assert old_r in t, 'README E4 anchor missing'
t = t.replace(old_r, new_r, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('README-OK')

# 4) station-reviews
p = 'docs/reviews/station-reviews.md'
t = io.open(p, encoding='utf-8').read()
old_s = u'E4 参考仪异步在飞（PID 80000·1500s 窗·下轮回填）'
new_s = (u'E4 参考仪同轮回填 8.0（16:43:25 热载快落·会停+打 8 明说·保存/转发条件式·'
         u'零一眼假明说·DIGEST 带 v2-v11 十连 8.0 持平·净本 expert-verdicts/20261001-164325-E4-audience.md）')
assert old_s in t, 'station E4 anchor missing'
t = t.replace(old_s, new_s, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('STATION-OK')

# 5) review file E4 row + 已测面
p = 'docs/reviews/review-20261001-mcdigest-v11.md'
t = io.open(p, encoding='utf-8').read()
old_v = u'| E4 参考仪（受众） | 在飞 | **异步非拦截席**（PID 80000·1500s 窗·R517→R518/R682 追加制先例·下轮回填） |'
new_v = (u'| E4 参考仪（受众） | 8.0 | 同轮回填毕（16:43:25 热载快落·会停+打 8 分明说·保存/转发条件式如实·'
         u'「没有一眼假或空洞套话」正面明说·旗①=立制行缺评分对象语境〔MC-003 族压缩变体·吸收位=M5〕·'
         u'最弱=46% 占比缺转化语境〔形态边界·M5 正解〕·DIGEST 带 v2-v11 十连 8.0 持平·'
         u'净本 expert-verdicts/20261001-164325-E4-audience.md） |')
assert old_v in t, 'review E4 row anchor missing'
t = t.replace(old_v, new_v, 1)
old_m = (u'木桶=6×9.0+E7 N/A 维度复用+E4 在飞注记 → **放行候选 PASS**（E4 回填位=下轮）。')
new_m = (u'木桶=6×9.0+E4 8.0+E7 N/A 维度复用 → **放行候选 PASS**（E4 同轮回填毕·零在飞席位）。')
assert old_m in t, 'review wood-line anchor missing'
t = t.replace(old_m, new_m, 1)
old_u = u'未测：E4 参考仪判词（在飞·下轮回填）；发布面（M5 账号物理件未开·未上线=未测量·发布锁不动）。'
new_u = u'未测：发布面（M5 账号物理件未开·未上线=未测量·发布锁不动）。（E4 已同轮回填毕 8.0·零未测评审席位）'
assert old_u in t, 'review untested anchor missing'
t = t.replace(old_u, new_u, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('REVIEW-OK')

# 6) state log line E4 segment
p = 'src/os/state.json'
t = io.open(p, encoding='utf-8').read()
old_l = u'→E4 异步在飞（PID 80000·1500s 窗·下回合填 R682 追加制先例）'
new_l = (u'→E4 同轮回填毕 8.0（16:43:25 热载快落·会停+打 8 分明说·保存/转发条件式·零一眼假明说·'
         u'旗①=立制行语境 M5 吸收位·DIGEST 带 v2-v11 十连 8.0 持平·净本 expert-verdicts/20261001-164325-E4-audience.md）')
assert old_l in t, 'state E4 anchor missing'
t = t.replace(old_l, new_l, 1)
import json as _j
d = _j.loads(t)
assert d['tick'] == 870 and ' R870: ' in d['log'][-1] and '同轮回填毕 8.0' in d['log'][-1]
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('STATE-OK')
print('BACKFILL-ALL-OK')
