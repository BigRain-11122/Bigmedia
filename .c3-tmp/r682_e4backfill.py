# -*- coding: utf-8 -*-
# R682 E4 same-round backfill (fast landing 12:28:16, R643/R674 precedent):
# review v1.1 E4 section + verdict archive + expert-calls row + finished/cards backfill sentences.
import io, json

ROOT = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream'
REV = ROOT + r'\docs\reviews\review-20260929-mcdigest-v10.md'
VD = ROOT + r'\docs\reviews\expert-verdicts\20260929-122816-E4-audience.md'
EC = ROOT + r'\docs\reviews\expert-calls.md'
FIN = ROOT + r'\output\finished.md'
CARDS = ROOT + r'\data\storylines\cards\README.md'

res = json.load(io.open(ROOT + r'\data\storylines\cards\MC-20260929-DIGEST-v10-tmp\e4-result.json', encoding='utf-8'))
verdict = res['verdict']

# 1. verdict archive
head = (u"# E4 参考仪判词·MC-20260929-DIGEST-v10《城市盘点 010·云端 token 机制令数字盘点》"
        u"（2026-09-29 12:28:16 落判·qwen2.5:14b·1500s 脱壳窗内热载快落·同轮回填=R643/R674 先例·非拦截席）\n\n```\n")
tail = (u"\n```\n\n"
        u"- 读数判读：**8.0**——会停下来看+有很大可能会保存或转发给朋友+打 8 分=三意愿正面明说〔保存/转发条件式「有很大可能」〕"
        u"·「数据驱动的决策模式+管理层面策略制定与执行=很高参考价值」+「实用性和前瞻性」=纪实密度+治理题材双正面定性"
        u"〔DIGEST 带 v2-v10 九连 8.0 持平·v1 9.0 峰带内〕\n"
        u"- 旗①：「委员会 7/7 有条件赞成」被疑「实际操作中难以达成如此统一和迅速的共识」扣 1——**事实面注记**："
        u"C-20260929-01 记名票档=FluxGroup/docs/decisions.md 委员会节正典在案〔七席独立意见 7/7 有条件赞成逐席留档〕"
        u"·当日令→当日过会=CEO 直令明示委员会通道+同窗收口授权〔council §五 排期律首用·C-20260928-02 范式〕"
        u"=E4 知识截止误判族〔REACT-v1 卡面日期伪影同型·非卡面文字旗〕·吸收位=M5 图文页证据链语境（记名票档指针）\n"
        u"- 最弱：「三缺口」表述抽象·「三径未升格」缺具体解释——卡面=台账短标签压缩"
        u"〔全称：生成面三径未升格集团执法=池内直用→本地先试→云端纯生成三径闸未集团执法化·全称入 source_facts〕"
        u"·MC-003 语境门槛族短标签压缩变体·纪实汇编不可改写·吸收位=M5 图文页语境+系列语境·M6 校准位\n"
        u"- 判定：非拦截·七席 ≥9 PASS 维持（F-056 登记态不动）\n")
with io.open(VD, 'w', encoding='utf-8') as f:
    f.write(head + verdict + tail)

# 2. review file: E4 section update + untested-face update + changelog line
rv = io.open(REV, encoding='utf-8').read()
old_sec = (u"## E4 参考仪（在飞·dept-review §6 双态制·非拦截）\n\n"
           u"- 状态：**异步在飞**（Start-Process 脱壳 1500s 窗·e4-result.json 轮间落地=下轮回填追加制 R517→R518/R577→R578/R631→R632 先例·非拦截席）\n"
           u"- 判定：非拦截·七席 ≥9 PASS 维持（回填轮如常对表三意愿/旗面/最弱项如实入行）")
new_sec = (u"## E4 参考仪（已回填·dept-review §6 双态制·非拦截）\n\n"
           u"- 状态：**同轮回填毕（起飞 12:28 脱壳→12:28:16 落判热载快落=R643/R674 快落型先例）**\n"
           u"- 读数：**8.0**——会停下来看+有很大可能会保存或转发给朋友+打 8 分=三意愿正面明说〔保存/转发条件式「有很大可能」〕"
           u"·「数据驱动的决策模式+管理层面策略制定与执行=很高参考价值」+「实用性和前瞻性」=纪实密度+治理题材双正面定性"
           u"〔**DIGEST 带 v2-v10 九连 8.0 持平**·v1 9.0 峰带内〕\n"
           u"- 旗①：「委员会 7/7 有条件赞成」被疑「难以达成如此统一和迅速的共识」扣 1——**事实面注记**："
           u"C-20260929-01 记名票档=decisions.md 委员会节正典逐席留档·当日令→当日过会=CEO 直令明示委员会通道+同窗收口授权"
           u"〔council §五 排期律·C-20260928-02 范式〕=E4 知识截止误判族〔REACT-v1 卡面日期伪影同型·非卡面文字旗〕"
           u"·吸收位=M5 图文页证据链语境\n"
           u"- 最弱：「三缺口」表述抽象·「三径未升格」缺具体解释——卡面=台账短标签压缩"
           u"〔全称=生成面三径闸未升格集团执法·池内直用→本地先试→云端纯生成〕·MC-003 语境门槛族短标签压缩变体"
           u"·吸收位=M5+系列语境·M6 校准位\n"
           u"- 判定：非拦截·七席 ≥9 PASS 维持（F-056 登记态不动）·净本 expert-verdicts/20260929-122816-E4-audience.md")
assert old_sec in rv, 'E4 section anchor not found'
rv = rv.replace(old_sec, new_sec)
old_chg = (u"- 2026-09-29: v1.0 首版（R682·DIGEST 续件第九件·#67 触发律第三用+queue §E 批活池 E2 首件·云端 token 机制令正行"
           u"+本司 R679/R681 双锚史源·E4 异步在飞）。")
new_chg = (old_chg + u"\n- 2026-09-29: v1.1（R682·E4 参考仪同轮回填 8.0 热载快落 12:28:16〔会停+保存/转发条件式=三意愿正面明说〕"
           u"·DIGEST 带 v2-v10 九连 8.0 持平·旗①=「7/7 有条件赞成」被疑难达成〔事实面注记=记名票档正典在案+同窗收口授权"
           u"=知识截止误判族·M5 吸收位〕·最弱=三缺口短标签抽象〔MC-003 族压缩变体·M5+系列语境吸收位·M6 校准位〕——非拦截·"
           u"七席 ≥9 PASS 维持·F-056 登记态不动·净本 expert-verdicts/20260929-122816-E4-audience.md）。")
assert old_chg in rv, 'changelog anchor not found'
rv = rv.replace(old_chg, new_chg)
old_un = u"- 受众反应面未测（E4 在飞·回填=下轮·E4=本地模型盲评参考线非实测·未上线=未测量·M6 数据回流后校准）"
new_un = u"- 受众反应面已测（E4 8.0 已同轮回填 R682·E4=本地模型盲评参考线非实测·未上线=未测量·M6 数据回流后校准）"
assert old_un in rv, 'untested anchor not found'
rv = rv.replace(old_un, new_un)
io.open(REV, 'w', encoding='utf-8').write(rv)

# 3. expert-calls row
ec_line = (u"\n| 2026-09-29 12:28 | E4-audience | E4 直觉观众（参考仪·非名册席） | "
           u"C:\\Users\\sjs20\\Desktop\\FluxGroup\\media\\BigStream\\data\\storylines\\cards\\MC-20260929-DIGEST-v10\\cards.json | 1 | "
           u"full text=expert-verdicts/20260929-122816-E4-audience.md / 8.0 会停+保存/转发条件式三意愿正面明说 "
           u"(E4 reference call: DIGEST-v10 static card, detached 1500s window, heat-loaded fast landing, same-round backfill R643/R674 precedent) |\n")
with io.open(EC, 'a', encoding='utf-8') as f:
    f.write(ec_line)

# 4. finished.md F-056 backfill sentence
fin = io.open(FIN, encoding='utf-8').read()
old_fin = u"+E4 参考仪异步在飞（Start-Process 脱壳 1500s 窗·下轮回填追加制 R517→R518/R577→R578"
new_fin = (u"+**E4 参考仪同轮回填 8.0**（12:28:16 热载快落=R643/R674 先例：会停下来看+有很大可能会保存或转发给朋友+打 8 分"
           u"=三意愿正面明说〔保存/转发条件式〕·「数据驱动决策+管理策略执行=很高参考价值」+「实用性前瞻性」"
           u"=纪实密度+治理题材双正面定性〔DIGEST 带 v2-v10 九连 8.0 持平·v1 9.0 峰带内〕·旗①=「7/7 有条件赞成」被疑难达成"
           u"〔事实面注记=记名票档正典+同窗收口授权在案=知识截止误判族·M5 吸收位〕·最弱=三缺口短标签抽象"
           u"〔MC-003 族压缩变体·M6 校准位〕·净本 expert-verdicts/20260929-122816-E4-audience.md·非拦截席）"
           u"——原异步注记：Start-Process 脱壳 1500s 窗·R517→R518/R577→R578")
assert old_fin in fin, 'finished anchor not found'
fin = fin.replace(old_fin, new_fin)
io.open(FIN, 'w', encoding='utf-8').write(fin)

# 5. cards README backfill sentence
cd = io.open(CARDS, encoding='utf-8').read()
old_cd = u"·E4 异步在飞（Start-Process 脱壳 1500s 窗·下轮回填 R517→R518/R577→R578/R631→R632 先例·非拦截）"
new_cd = (u"·**E4 参考仪同轮回填 8.0**（12:28:16 热载快落=R643/R674 先例·会停+保存/转发条件式三意愿正面明说"
          u"〔DIGEST 带 v2-v10 九连 8.0 持平〕·旗①=7/7 赞成被疑难达成〔事实注记=记名票档正典+同窗收口授权"
          u"=知识截止误判族·M5 吸收位〕·最弱=三缺口短标签抽象〔MC-003 族·M6 校准位〕"
          u"·净本 expert-verdicts/20260929-122816-E4-audience.md·非拦截）")
assert old_cd in cd, 'cards README anchor not found'
cd = cd.replace(old_cd, new_cd)
io.open(CARDS, 'w', encoding='utf-8').write(cd)

print('backfill done: E4 8.0 same-round, review v1.1 + verdict + ec row + fin/cards sentences')
