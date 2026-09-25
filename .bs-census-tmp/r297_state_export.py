# -*- coding: utf-8 -*-
# R297 state.json + status-export.json refresh (PT-20260925-02 ts/task heartbeat fields + P-61 export step)
import io, json, os, time

REPO = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now_sec = time.strftime('%Y-%m-%d %H:%M:%S')
stamp = time.strftime('%H:') + time.strftime('%M')[0] + 'x'

LOG_LINE = (
    "2026-09-25 " + stamp + " R297: 生产轮·图鉴系列量产按序领件第六件=MC-20260925-CENSUS-v7《城市图鉴 007·徐根福》全链走门毕（F-026 登记·成品库第二十五件·实活轮）——"
    "①轮首快速路径五查：无新令（orders 顶=O-20260925-1931-HQ-C R283 已记账）/ledger 含 @ 四模式 17 行=锚零新转办/decisions UTF8 非空行 29〔总 32 双口径〕=锚零新行/树净零锁（HEAD=cb5a41b R296）/ch.5 v3 稿未落盘=novel 实证止 ch.5 v1〔bm-a 面·稿落即认领·音频线优先口径维持〕"
    "→backlog 量产线图鉴续件认领判断成立（R296「图鉴续件=万人卡按卡号序随轮领〔C-00016 起〕」口径·按卡号序 C-00015→C-00016·C-00016 手写锚存在性核=life/BigLife/census/anchors/C-00016.md 在位）=实活轮照 focus·backlog #44 留痕行落+done 标；"
    "②全链=M0 选题四维分 7/8=A 档进 M1（钩 2 反差链〔66 岁食堂大厨 vs 按涨跌调整菜谱=最烟火职业×最量化行为反差·K线广场唯一不谈数字的人却按行情做饭=事实性赛博意象+信条「行情再绿，汤是热的」=市场冷绿×人间热汤反差对仗金句级+钩子行「全城唯一」具体稀缺性·徐根福=F-012 有声线 ch.5《徐根福的食堂》已验人格面同源人物=IP 人物面跨载体复用第四件〔顾阿凤 F-009→朱鸿奎 F-010→周浩宇 F-012 ch.5→徐根福 F-012 ch.5 主角〕·novel ch.4 cta「徐根福的食堂」钩承接兑现位/情 1 弄堂烟火温情温和共鸣如实/时 2 人物档案常青/台 2 公众号方图承载=MC-001~013 S3 实证复用·cards.json meta.hit_chain_m0 数据件自证）"
    "→M1 纪实字段汇编律系列化复用（R291 首定制·六行逐条溯 C-00016 手写锚：卡题行+编号/物种+性别·年龄 verbatim 合并/城区两级选材+职业首词 verbatim〔破折号阐释尾「算力楼里唯一不谈数字只谈火候的人——回撤再大也得吃饭」=选材排除〕/信条 verbatim/性格三关键词 verbatim〔括号注=选材排除〕/钩子首句 verbatim〔破折号尾「绿盘日免费例汤，红盘日加一道『冷静甜汤』，食堂日志跟行情日志一起进了档案馆」=选材排除〕——零改写虚构逐行可机核·人设权红线专项核=C-00016 非荣誉席·脱敏律核=年轮〔含令牌号〕/思想/语言/服装/经历/行为/关系字段选材排除不进卡面）"
    "→M2 --poster 出图 exit 0（1080×1080·3.4s 副产 mp4 入 tmp）+**验图 5/5 一次过**（转写先行防偏：九行逐字对照全中/零重叠零越界零截断/全行单行零折行/来源行闭合/AIGC 角标清晰/层级留白明确·**h2_size 44 前置适配系列化第四件=拉丁混合长行驱动**——binding 行=城区职业行「QUANT 城 · K线广场 · QUANT 食堂大厨」≈19.35em<20.9em〔QUANT×2+K 混排=系列拉丁密度最高行·R295 ASCII 0.55em 估宽法复用〕·钩子 13 全角字系列短带·初稿即正字系列化第六连）"
    "→M3 标题「城市图鉴 007」四禁零中+系列编号连载识别→M4 四检过（红线五条/三重标注图内双落〔底部行「基于硅基城市居民户籍卡档案（展示锚 C-00016）」〕/来源双落/编辑价值）"
    "→M4.5 七席 ≥9（6×9.0+E7 N/A 维度复用·站审 M0-M6 判据行全链留痕=review-20260925-mccensus-v7.md）"
    "→E4 参考仪同轮回填 **8.0 会停下来看+会保存〔「很有收藏价值」明说〕+转发条件式**（Start-Process 后台起飞→22:35:34 窗内落地热载快落·CENSUS-v1/v2/v4/v5 8.0 带持平·「没有一眼看出明显的空洞套话」正面明说=信任面续证·「上海地方文化×金融市场跨界融合」+「设计感强黑白底红字」=文化混搭面与视觉面正面读数·旗①=性格三词「手稳·热肠·实在」略显陈词滥调扣 1〔卡面 verbatim 不可改写·三词标签族性最弱位第四现·吸收位=M5 图文页正文人格展开〕+旗②=「行情有时令，菜也有」过于文艺扣 0.5〔**非卡面文字=E4 材料语境段旗**·行为字段=选材排除不进卡面·CENSUS-v4/v6 同型〕·Q2 自算 7.5 与 Q1 总分 8 内部算术不同步=R293 先例同型如实注记·最弱=信条「行情再绿，汤是热的」语境门槛缺普遍性〔MC-003 族·吸收位=M5 图文页语境+系列语境〕·净本 expert-verdicts/20260925-223534-E4-audience.md）=零未测面遗留"
    "→F-026 登记（成品库第二十五件·L-卡 第十四件·图鉴系列量产第六件）+cards/README 台账行+变更行+station-reviews R297 行+finished.md F-026 块+变更行+**随行补账=finished.md F-025 块级登记补块**（R296 收账缺口·变更行 L218 已在·原行不改写·R150 补账先例·假绿灯律① 分数史不改写）+backlog #44 done 标+status-export 刷；"
    "③三探针全绿=board 0 FAIL（5 题 10 稿·5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+0 发现（阻塞≠失败口径 exit 1·弃件清账新基线维持）/loop_health 0 FAIL 18 WARN 皆在案史实（heartbeat-gap 在案带·tick296=done296 对账平·state-ts 门零红零滞后）；"
    "例行件：日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks 更新记录 2026-09-24 day1 ≤7 天跳过刷新（下期 ~10-01）·T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=1（E4 qwen2.5:14b 本地 Ollama 一次直调·零 API token·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（公众号=批次① 未开·未上线=未测量）；"
    "下轮=R298 快速路径首查（新令/ch.5 v3 稿落迹象/集团转办），量产线图鉴续件=万人卡按卡号序随轮领（C-00017 起·R294 归档者-07=C-00017 另卡同名混淆防核在案·手写锚存在性轮首核）·L-卡 P0 形态余项=热点速报城市反应版（第三位）·日签变体随时可续，全静即 idle-fast。收账显式列文件 commit+push。"
)

FOCUS = (
    "R298: focus=快速路径首查（L-卡 图鉴系列量产第六件毕=F-026 登记·成品库二十五件）：查新令/ch.5 v3 稿落迹象〔bm-a 面·稿落即认领·音频线优先〕/"
    "量产线按序领件判断（图鉴续件=万人卡按卡号序随轮领〔C-00017 起手写锚存在性轮首核·R294 归档者-07=C-00017 另卡同名混淆防核在案·人设权红线专项核照守〕·"
    "L-卡 P0 形态余项=热点速报城市反应版〔第三位·包装层新建+合规流程重排在案〕·日签变体随时可续）/集团转办（ledger 锚 17/decisions 锚 29〔总 32〕）——全静即 idle-fast 一行收账"
)

# ---------------- state.json ----------------
sp = os.path.join(REPO, r"src\os\state.json")
raw = io.open(sp, "rb").read()
crlf = b"\r\n" in raw
d = json.loads(raw.decode("utf-8"))
d["tick"] = 297
d["focus"] = FOCUS
d["log"].append(LOG_LINE)
d["ts"] = now_sec
d["task"] = LOG_LINE.split("R297: ", 1)[1][:60]
out = json.dumps(d, ensure_ascii=False, indent=1)
if crlf:
    out = out.replace("\n", "\r\n")
io.open(sp, "wb").write(out.encode("utf-8"))
print("state.json tick=297 ts=", now_sec, "task=", d["task"][:40], "CRLF=", crlf)

# ---------------- status-export.json ----------------
ep = os.path.join(REPO, r"docs\status-export.json")
raw2 = io.open(ep, "rb").read()
crlf2 = b"\r\n" in raw2
e = json.loads(raw2.decode("utf-8"))
e["export_ts"] = time.strftime('%Y-%m-%dT%H:%M:%S+08:00')

def rep(s, old, new, tag):
    assert old in s, "MISSING ANCHOR: " + tag
    return s.replace(old, new, 1)

# do
e["do"] = rep(e["do"],
    "·E4 7.0 会停+会保存）",
    "·E4 7.0 会停+会保存）+图鉴系列量产按序领件第六件（R297 MC-20260925-CENSUS-v7 徐根福 F-026=按卡号序续领·F-012 有声线 ch.5 主角=跨载体人物复用第四件·h2_size 44 拉丁混合长行 19.35em 一次过·E4 8.0 会停+会保存）",
    "do")

# depts
for dept in e["depts"]:
    if dept["n"] == "内容生产部":
        dept["t"] = rep(dept["t"], "L-卡 十三件 F-013~F-025（成品库二十四件", "L-卡 十四件 F-013~F-026（成品库二十五件", "cns-count")
        dept["t"] = rep(dept["t"],
            "·E4 7.0 会停+会保存〕）·BS-005/bs005e=弃件处置毕（D-BS-08）",
            "·E4 7.0 会停+会保存〕+R297 MC-CENSUS-v7=图鉴系列量产第六件〔按卡号序 C-00016 徐根福=F-012 有声线 ch.5《徐根福的食堂》主角·跨载体人物复用第四件·h2_size 44 拉丁混合长行=QUANT×2+K 混排 19.35em 一次过·E4 8.0 会停+会保存〕）·BS-005/bs005e=弃件处置毕（D-BS-08）",
            "cns-r297")
    if dept["n"] == "合规审查部":
        dept["t"] = rep(dept["t"], "F-008~F-025 过门登记（二十四件）", "F-008~F-026 过门登记（二十五件）", "comp-count")
        dept["t"] = rep(dept["t"], "C-00010/C-00011/C-00012/C-00013/C-00014/C-00015 非荣誉席", "C-00010/C-00011/C-00012/C-00013/C-00014/C-00015/C-00016 非荣誉席", "comp-census")
    if dept["n"] == "工程技术部":
        dept["t"] = ("OS 循环 R297（图鉴系列量产按序领件第六件=MC-20260925-CENSUS-v7 徐根福居民图鉴全链走门【M0 四维分 7/8 A 档+纪实字段汇编律系列化复用+"
                     "h2_size 44 前置适配系列化第四件=拉丁混合长行驱动（binding 行=城区职业行 QUANT×2+K 混排 19.35em<20.9em·R295 ASCII 估宽法复用）·"
                     "验图 5/5 一次过+E4 同轮 8.0 会停+会保存+F-026·按卡号序续领第六件】·前轮 R296 MC-CENSUS-v6 在案）·state.ts/task 心跳面刷新")

# outs
for row in e["outs"]:
    if row[0] == "OS 循环":
        row[2] = ("tick 297·R297（生产轮——图鉴系列量产按序领件第六件=MC-20260925-CENSUS-v7《城市图鉴 007·徐根福》hit-chain §8 全链留痕："
                  "M0 四维分 7/8 A 档〔钩 2 反差链：66 岁食堂大厨 vs 按涨跌调整菜谱=最烟火职业×最量化行为反差·信条「行情再绿，汤是热的」市场冷绿×人间热汤对仗金句级·徐根福=F-012 有声线 ch.5 主角=跨载体人物复用第四件〕+"
                  "M1 纪实字段汇编律系列化复用〔六行逐条溯 BigLife 手写展示锚 C-00016 verbatim 零新增人格·人设权红线专项核过·脱敏律核=年轮令牌号/思想/语言/服装/经历/行为/关系字段选材排除〕+"
                  "验图 5/5 一次过=h2_size 44 前置适配拉丁混合长行〔QUANT×2+K 混排 19.35em<20.9em=系列拉丁密度最高行·钩子 13 字短带·初稿即正字第六连〕+"
                  "七席 ≥9+E4 同轮 8.0 会停下来看+会保存〔「很有收藏价值」明说·转发条件式·「没有一眼看出明显的空洞套话」正面明说=信任面续证〕+F-026 登记=成品库第二十五件·图鉴系列量产第六件；"
                  "随行补账=finished.md F-025 块级登记补块（R296 收账缺口·R150 补账先例）；backlog #44 留痕行 done；"
                  "图鉴续件=万人卡按卡号序随轮领〔C-00017 起·归档者-07 另卡同名混淆防核在案〕·L-卡 P0 形态余项=热点速报城市反应版（第三位）·待随轮认领；"
                  "ch.5 v3 稿未落〔bm-a 面·稿落即认领·音频线优先口径维持〕）")
    if row[0] == "量产产线":
        row[2] = rep(row[2], "L-卡 十三件 F-013~F-025（成品库二十四件", "L-卡 十四件 F-013~F-026（成品库二十五件", "prod-count")
        row[2] = rep(row[2],
            "·h2_size 36 前置适配系列化第三件=25 全角字系列最长钩子〕）；",
            "·h2_size 36 前置适配系列化第三件=25 全角字系列最长钩子〕+R297 MC-CENSUS-v7 图鉴系列量产第六件〔按卡号序 C-00016 徐根福=F-012 ch.5 主角·跨载体复用第四件·h2_size 44 拉丁混合长行 19.35em 一次过·E4 8.0〕）；",
            "prod-r297")
        row[2] = rep(row[2], "有声五件成品+L-卡 图文线十三件·O-1327 全毕", "有声五件成品+L-卡 图文线十四件·O-1327 全毕", "prod-line14")

# results
for row in e["results"]:
    if row[1] == "OS 轮次":
        row[0] = "297"
    if row[1].startswith("成品库登记件"):
        row[0] = "25"
        row[1] = rep(row[1], "F-001~F-006+F-008~F-025", "F-001~F-006+F-008~F-026", "res-range")
        row[1] = rep(row[1], "图文卡十三件", "图文卡十四件", "res-13")
        row[1] = rep(row[1],
            "·h2_size 36 前置适配系列化第三件=25 全角字系列最长钩子·E4 7.0 会停+会保存〕；",
            "·h2_size 36 前置适配系列化第三件=25 全角字系列最长钩子·E4 7.0 会停+会保存〕+**F-026 图鉴系列量产第六件=按卡号序续领·徐根福〔F-012 有声线 ch.5《徐根福的食堂》主角=跨载体人物复用第四件·novel ch.4 cta 钩承接兑现位〕·h2_size 44 前置适配拉丁混合长行=QUANT×2+K 混排 19.35em 一次过·E4 8.0 会停+会保存〕；",
            "res-f026")

out2 = json.dumps(e, ensure_ascii=False, indent=2)
if crlf2:
    out2 = out2.replace("\n", "\r\n")
io.open(ep, "wb").write(out2.encode("utf-8"))
print("status-export.json export_ts=", e["export_ts"], "CRLF=", crlf2)
print("ALL DONE")
