# -*- coding: utf-8 -*-
# R723 close: state.json hole-fix double record (tick 721->723) + export + queue E15 row + burn.
import json, re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
now = datetime.now()
stamp = now.strftime("%Y-%m-%d %H:%M:%S")
short = now.strftime("%H:%M")

r722 = ("2026-09-30 04:06 R722 断洞修复（账目·R723 承办·R718/R712/R714 先例）：03:52 起跑轮（R721 收账 03:47 后）"
    "04:06 被杀 exit=1 零 state 写盘（可见足迹=.c3-tmp/r722_probe.txt 仅探针 03:54:31·读腿工作=五查+queue §E 补池确认"
    "+E14 行读+E15 候选快验〔C-00011/C-00014 卡面·其控制台 GBK 误读名在案·权威表=C-00011 朱鸿奎/C-00014 周浩宇〕"
    "·round.lock 由启动器硬帽回收）——读腿产出全由 R723 吸收零重做，tick 721→723 断洞双记（R689/R690 同法）。")

r723 = ("2026-09-30 %s R723: 生产轮·queue §E 补池义务兑现=E14 LC-014 老晶振 standby→active 起链+E15 LC-015 朱鸿奎 standby 入池"
    "（R722 断洞承接·lane ≥2 达标·实活轮·产品优先律对位=本轮新实物=LC-014 拍稿三件套落盘）——"
    "①五查静（orders 顶 O-20260928-1910 42 件锚未动/ledger 六模式 CaseSensitive 41=锚/decisions UTF8 非空行 75=锚"
    "/production=open 自愈核在位/无 index.lock·树态=bm-a codex 批未闭让位维持〔README/city-humanities mtime 09-29 04:06 未动"
    "=#86 c+d 判据未达·零接触〕+自产 tmp 族预期态）；"
    "②E14 兑现=老晶振 C-00019（**光机魂系首拆位**〔碳基×8→像素灵×2→精灵系×1 后物种阶梯第四档〕+**GAME 城拆条第四卡**"
    "〔王多多 LC-008→咪喱 LC-009→苏梓涵 LC-013→老晶振 LC-014·经历字段「出诊箱在游戏楼有一张专用椅子」=游戏楼连接位〕"
    "+最科技物种×最手工台账反差位·源卡 CENSUS-v10 F-029 在册·锚卡逐字段实读 life/BigLife/census/anchors/C-00019.md 跨仓只读）；"
    "③LC-014 起链腿落盘：拍稿 v1 12 拍 ≈274 字（锚 C-00019 逐拍字段级溯源对表 s1-review-material-v1.md·盲评材料律合规零嵌审计史"
    "·「台账」=词表唯一命中→L18 卡口分工〔口播=手写记录白话换位·卡锚列保留原词·LC-009 回测田/LC-010 门禁链/LC-011 打轴 同型〕）"
    "+M1 即检 v1=0 FAIL 1 WARN（b2 居民档案行 3 逗长句→v2 机械裁链句拆收口·LC-011 v1 0F1W→终稿 0F0W 同型）"
    "+S1 v1.5+L18-L20 门 wrapper 脱壳起飞（.lc014-tmp/s1_call.py=LC-013 同型·1500s 窗·s1-result.json 轮间异步落地=R712→R713 先例）"
    "+TTS light v1 起飞（.c3-tmp/r723_tts_run.py·--template=.lc013-tmp/cards.json 链式承继·BGM-A 纯净）"
    "——空气预算机械裁链（v1 实测读数→裁→定稿）+S1 首读=R724 首位；"
    "④E15 选优定谳=朱鸿奎 C-00011 standby 入池（时间校准主题系列首件位+F-010 有声线同源人格面已验〔跨载体人物复用先例在案〕"
    "+CENSUS 图鉴量产按序首件锚·源卡 CENSUS-v2 F-021 在册·E4 8.0 三意愿正面在案·runner-up=周浩宇 C-00014 注记"
    "〔题材与 LC-002 归档者-07「给失败立碑」/LC-012 毙稿理由档案重叠=系列题材重复风险+量化主题合规三落负担→后顺位〕"
    "·BS-007 稿集件=顺位后置维持 R712 口径）——lane=E14〔active〕+E15〔standby〕≥2 达标（C-20260929-02 B 款口径）；"
    "⑤台账=data/sources/lc014/（beats v1+评审材料+README）+queue §E E15 standby 池行+burn 行；"
    "⑥例行件：日报 09-30 在案不重跑（R713 补产）/W40 周审在案/global-benchmarks day6 ≤7 跳过（下期 10-01=#80 并窗）"
    "/T1 催办停用口径/HQ-FEEDBACK 不写（无集团层新 open 问题）·tokens:local=S1+TTS 在飞未落=落地轮记账（P-54⑤ 计量律如实预注）"
    "——下轮=R724 可领序：①LC-014 空气预算裁链续做（v1 读数→v2/v3 定稿）+S1 首读→TTS 定稿音轨→渲染腿（R710 同型：F-029 PNG 派生"
    " census-card-v10-vertical→对位表→R-E shipinhao〔拆条 014·源城市图鉴 010〕→S2 三门→帧验三律）→收官腿（E8+ASR+E4+M4→F 登记"
    "→冗余池第十一件→E14 出池）②#70 OSS 窗 2 切片（≤10-02 21:40）③#86 c+d 让位判据（bm-a codex 批闭 commit 落地）"
    "④global-benchmarks 7 日刷（10-01=#80 并窗）。收账显式列文件 commit+push" % short)

sp = ROOT / "src" / "os" / "state.json"
raw = sp.read_text(encoding="utf-8")
had_nl = raw.endswith("\n")
st = json.loads(raw)
st["tick"] = 723
st["log"].append(r722)
st["log"].append(r723)
st["focus"] = ("R724: ①LC-014 空气预算裁链（v1 读数→v2/v3 定稿入窗）+S1 首读（.lc014-tmp/s1-result.json）→TTS 定稿音轨→渲染腿"
    "（R710 同型五步）②#70 OSS 窗 2 切片（≤10-02 21:40）③#86 c+d 让位判据（bm-a codex 批闭 commit 落地）"
    "④global-benchmarks 7 日刷（10-01=#80 并窗）——五查锚=orders 顶 O-20260928-1910·ledger 41（六模式 CaseSensitive=正典 "
    "r694_probe.py 口径）·decisions 75")
st["ts"] = stamp
body = re.sub(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})? R723: ", "", r723)
st["task"] = body[:60]
sp.write_text(json.dumps(st, ensure_ascii=False, indent=2) + ("\n" if had_nl else ""), encoding="utf-8")

ex = ROOT / "docs" / "status-export.json"
raw2 = ex.read_text(encoding="utf-8")
had_nl2 = raw2.endswith("\n")
se = json.loads(raw2)
se["export_ts"] = stamp + "+08:00"
se["outs"][0][1] = ("tick 723，R723 生产轮·queue §E 补池义务兑现=E14 LC-014 老晶振 standby→active 起链+E15 朱鸿奎 standby 入池"
    "（R722 断洞双记 tick 721→723·实活轮）：拍稿 v1 12 拍 274 字（光机魂系首拆位·锚 C-00019 逐拍溯源对表·「台账」L18 卡口分工）"
    "+M1 v1 0F1W（b2 三逗→v2 收口）+S1 wrapper 异步+TTS v1 异步（--template .lc013-tmp 链式）——lane=E14 active+E15 standby "
    "≥2 达标——空气预算裁链+S1 首读=R724 首位")
se["results"].insert(0, [
    "723",
    "2026-09-30 %s R723: 生产轮·queue §E 补池义务兑现=E14 LC-014 老晶振 standby→active 起链+E15 LC-015 朱鸿奎 standby 入池"
    "（R722 断洞承接·断洞双记 tick 721→723·lane ≥2 达标·实活轮）：五查静（orders O-20260928-1910 42 件锚/ledger 六模式 CS 41=锚"
    "/decisions 75=锚·production=open·bm-a codex 批未闭让位维持）；E14 兑现=老晶振 C-00019（光机魂系首拆位+GAME 城拆条第四卡"
    "+最科技物种×最手工台账反差位·源卡 CENSUS-v10 F-029 在册）；LC-014 起链腿=拍稿 v1 12 拍 ≈274 字（逐拍溯源对表·盲评律合规"
    "·「台账」L18 卡口分工）+M1 v1 0F1W（b2 三逗长句→v2 收口）+S1 wrapper 脱壳异步+TTS v1 异步（链式承继 .lc013-tmp）"
    "——空气预算裁链+S1 首读=R724 首位；E15 选优=朱鸿奎 C-00011（时间校准主题首件位+F-010 有声线同源人格已验+源卡 CENSUS-v2 "
    "F-021 在册·runner-up=周浩宇 C-00014 题材重叠注记）；台账=data/sources/lc014/ 三件套+queue §E E15 行+burn 行；"
    "例行件：日报 09-30 在案/W40 周审在案/GB day6 ≤7 跳过（10-01=#80 并窗）/T1 停用/HQ-FEEDBACK 不写·tokens:local=在飞未落落地轮记账"
    "——下轮=R724：①LC-014 裁链+S1 首读→定稿→渲染腿（R710 同型）→收官②#70 OSS 窗 2③#86 c+d 判据④GB 7 日刷" % short
])
se["live"] = [
    ["当前活：LC-014 老晶振拆条起链中段（E14 standby→active 兑现·光机魂系首拆位·GAME 城第四卡）：拍稿 v1+M1 0F1W+S1/TTS v1 双异步在飞——空气预算裁链+S1 首读=R724 首位；E15 朱鸿奎 standby 入池=lane ≥2 达标"],
    ["最近实物：data/sources/lc014/（voiceover-v1.beats.txt 12 拍 274 字+s1-review-material-v1.md 逐拍溯源对表+README）·2026-09-30 " + stamp],
    ["下个里程碑：LC-014 定稿音轨+渲染腿+收官（F 登记→冗余池第十一件·窗 ≤10-02）+#70 OSS 窗 2 切片（≤10-02 21:40）+global-benchmarks 7 日刷（10-01=#80 并窗）"],
]
ex.write_text(json.dumps(se, ensure_ascii=False, indent=1) + ("\n" if had_nl2 else ""), encoding="utf-8")

qp = ROOT / "docs" / "self-improvement-queue.md"
qraw = qp.read_text(encoding="utf-8")
qhad_nl = qraw.endswith("\n")
e15_row = ("- **E15 LC-015 朱鸿奎拆条续投批 standby**（R723 补池选优轮评估兑现·三验字段：假设=拆条系列第十四续件候选"
    "+**时间校准主题系列首件位**〔74 岁修表匠 vs 校准全城的钟=手稳×全城尺度反差·信条「差之毫秒，谬以全城。」〕"
    "+**F-010 有声线同源人格面已验**〔跨载体人物复用先例在案〕+CENSUS 图鉴量产按序首件锚〔C-00011 低卡号未拆存量位〕；"
    "消费面=视频号冗余扩容位+L-卡库；consumer_plan=全链 M0→F 本地执行零云端）：锚=C-00011（手写展示锚在位·非荣誉席）"
    "·源卡=CENSUS-v2 F-021 成品 PNG（R292 登记·E4 8.0 会停下来看+会保存+可能转发三意愿正面在案）——standby"
    "（E14 active 时待领·runner-up=周浩宇 C-00014〔CENSUS-v5〕注记：题材与 LC-002 归档者-07「给失败立碑」/LC-012 毙稿理由档案"
    "重叠=系列题材重复风险+量化主题合规三落负担→后顺位·BS-007 稿集件=顺位后置维持 R712 口径）\n")
anchor = "——standby=lane ≥2 保底（E13 active 时待领·BS-007 稿集件=顺位后置维持 R712 口径）"
if anchor in qraw and e15_row not in qraw:
    qraw = qraw.replace(anchor, anchor + "\n" + e15_row.rstrip("\n"), 1)
burn_line = ("- 2026-09-30: **E14 standby→active 起链中段+补池 E15 入池（R723·R722 断洞双记 tick 721→723〔R722 轮 03:52-04:06 被杀 "
    "exit=1 零 state 写盘·读腿足迹全吸收零重做〕）：LC-014 老晶振拍稿 v1 12 拍 ≈274 字（锚 C-00019 逐拍溯源对表·光机魂系首拆位"
    "·「台账」L18 卡口分工）+M1 v1 0F1W（b2 三逗→v2 收口）+S1 wrapper 异步+TTS v1 异步（--template .lc013-tmp 链式）"
    "·E15=朱鸿奎 C-00011 standby 入池（F-021 源卡在册·F-010 有声线同源人格已验）——lane=E14〔active〕+E15〔standby〕恢复 "
    "≥2 达标（C-20260929-02 B 款口径）**——空气预算裁链+S1 首读+定稿音轨=R724 首位；渲染腿/收官腿随轮领（F 登记→冗余池第十一件落位）。\n")
qp.write_text(qraw + burn_line + ("\n" if qhad_nl else ""), encoding="utf-8")

print("OK state tick=%s log=%d" % (st["tick"], len(st["log"])))
print("OK export ts=%s live=%d" % (se["export_ts"], len(se["live"])))
print("OK queue e15_inserted=%s" % (e15_row.strip()[:40] in qp.read_text(encoding="utf-8")))
