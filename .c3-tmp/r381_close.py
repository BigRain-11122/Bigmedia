# -*- coding: utf-8 -*-
"""R381 close-out: state.json tick/log/ts/task/focus + status-export refresh (P-61 step).
Single-source timestamp (R351 lesson): stamp built once, reused for log prefix and ts field.
"""
import io, json, time

STAMP = time.strftime("%Y-%m-%d %H:%M:%S")
LOG_PREFIX = time.strftime("%Y-%m-%d %H:%M")

LOG = (u"%s R381: 生产轮·#67 DIGEST 续件第二件全链走门毕（claim 728afdd 两步制先落防撞·R380 focus 候选序首位=三线扩展 O-20260925-0850 CEO 内容宇宙令领做·bigstream-lcard-pipeline 技能产线第二用）——"
       u"①MC-20260926-DIGEST-v3《城市盘点 003·三线扩展日数字盘点》：M0 四维分 7/8 A 档（钩 2：1 句话 vs 当天 3 条线立制开工=F-042「1 句话 vs 7 决」对照结构同源第二证+万人库/14 派系/台词池 1200+ 素材纵深三组数字+首章 1100 字/漫画四格产出对照/情 1 IP 宇宙扩展期待吃瓜温和如实〔G5+G2 双群〕/时 2 三线扩展 1 日时点/台 2 方图复用）+"
       u"M1 纪实数字汇编律系列化复用（**五源指针逐条可机核**=orders/O-20260925-0850-bm-a.md 内容宇宙令正件〔08:50+CEO 原话 verbatim 引文块跨三行排版零改字+同晨 09:1X「调研+开工同批闭环」执行回执〕+research/city-storylines-research-v1.md v1.0〔万人库/14 派系/台词池 1200+〕+docs/city-storylines-charter.md v1.0 立制件+novel/SC-001-01-v1.md 首章《立国日》约 1100 字+comic/SC-002-01-v1 四格 PoC·零改写虚构·charter §3 一料多吃·署名=纪实线编年史档案级零虚构居民名）+"
       u"M2 **首渲真发现=垂直栈溢出→修参复验 PASS**（七行 deck@44 档栈底 y≈991px 压入 subs 带 y=970px 重叠 21px·验图五检「零重叠」项当场咬住=R381 假绿灯新面首证〔em 机核只测横向·垂直栈预算从未进机检·v2 六行 deck 86px 余量掩盖该面〕→**h2_size 44→40 版式参数律**〔文本 verbatim 零动=R293 教训正面执行〕+**垂直栈预算律入 build 机核**〔pitch=1.35×size+ls 保守模型·栈底 ≤ subs 顶−20px 断言〕→复渲 PIL band-measure 实测 10 带全分离·末行底 y=938px vs subs 顶 y=970px **间隙 32px**·横向 40 档 budget 23.0em 最长引文行 20.0em margin 3.0em·subs 21.0em<24.21em·em-check-r381.txt 横向+VERT 双断言）+"
       u"M3「城市盘点 003」四禁零中+系列编号连载识别+M4 四检过（红线五条/三重标注图内双落〔底部行「基于硅基城市真实事件（三线扩展令台账档案）」〕/来源双落/编辑价值〔1→3→万人→1100→四格递进链〕）+M4.5 七席 ≥9（6×9.0+E7 N/A 维度复用·评审单 docs/reviews/review-20260926-mcdigest-v3.md）+"
       u"E4 参考仪 **异步在飞**（1500s 脱壳·e4-result.json 轮间落地=下轮回填评审单 E4 行+expert-verdicts 存档·R180/R187 追加制先例·非拦截席）→**F-043 登记**（成品库第四十二件·L-卡 第三十一件·DIGEST 形态第三件）；"
       u"②轮首五查静（无新令 orders 顶=O-1931-HQ-C 已记账/ledger 严格 @ 前缀 23=锚零新转办/decisions 非空行 40=锚零新行/树净零锁 HEAD=a185bba·日报 2026-09-26 在案不重跑·C-00030 锚不在位=图鉴供给门照守·ch.5 v3 稿未落=bm-a 面）+三探针全绿（board 0 FAIL 5 题 10 稿 5 in production/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health 0 FAIL 19 WARN 在案史实·tick380=done380 对账平）→backlog 顶行可认领=转全任务书生产轮；"
       u"③例行件：日报 2026-09-26+W39 周审在案不重跑·global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=1（E4 qwen2.5:14b 一调在飞未落=落地轮记账·本地 Ollama 零 API token·P-54⑤ 计量律）·发布锁=M5 账号物理件不变（未上线=未测量）。"
       u"下轮=R382 快速路径首查→E4 e4-result.json 落地回填（追加制）→#67 编年史事件候选随轮领（技能动员 2026-09-26 等 research §5 在册）/#63 图鉴 C-00030 锚轮首核/REACT 09-27 热点窗届日即领/#21 周日立法件 09-27 届日即领——全静即 idle-fast。") % LOG_PREFIX

FOCUS = (u"R382: E4 e4-result.json 落地回填（追加制·评审单 E4 行+expert-verdicts 存档+台账注记）→#67 DIGEST 编年史事件候选随轮领（技能动员 2026-09-26 等·research §5 在册·R379 判据=编年史 A 级事件+数字密度）→#63 图鉴 C-00030 锚轮首核（supply-gated 照守·锚落即领）→REACT 09-27 日报热点窗届日即领→#21 周日立法件 09-27 届日即领——新令/集团转办/探针红出现即优先；全静即 idle-fast")

# --- state.json ---
p = "src/os/state.json"
d = json.load(io.open(p, encoding="utf-8"))
d["tick"] = 381
d["log"].append(LOG)
d["ts"] = STAMP
d["task"] = LOG[len(LOG_PREFIX) + 1:][:60]  # strip "YYYY-MM-DD HH:MM " prefix, first 60 chars
d["focus"] = FOCUS
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=1))

# --- status-export.json (P-61 step, live-derived, no hardcode) ---
p2 = "docs/status-export.json"
e = json.load(io.open(p2, encoding="utf-8"))
e["export_ts"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
for dept in e["depts"]:
    if dept["n"] == u"工程技术部":
        dept["t"] = (u"OS 循环 R381（生产轮·#67 DIGEST 续件第二件全链走门毕=MC-20260926-DIGEST-v3 F-043〔三线扩展 O-0850 史源·五源指针逐条可机核·"
                     u"**垂直栈预算律首入 build 机核**〔首渲 44 档溢出 21px→40 档间隙 32px 修参复验过=R381 假绿灯新面根修〕·E4 异步在飞下轮回填〕·"
                     u"产线 supply-gated 照守=图鉴 C-00030 锚不在位+REACT 新热点窗 09-27+#21 周日件 09-27 届日）·state.ts/task 心跳面刷新")
for out in e["outs"]:
    if out[0] == u"OS 循环":
        out[2] = (u"tick 381·R381（生产轮·#67 DIGEST 续件第二件全链走门毕：MC-20260926-DIGEST-v3《城市盘点 003·三线扩展日数字盘点》F-043=成品库第四十二件·L-卡 第三十一件·DIGEST 形态第三件"
                  u"〔R380 focus 候选序首位领做·M0 7/8 A 档+五源指针逐条可机核+**首渲垂直栈溢出真发现→h2 44→40 修参复验 5/5 过+垂直栈预算律入 build 机核**〔间隙 32px PIL 实证〕+七席 ≥9+E4 异步在飞下轮回填〕〕·"
                  u"backlog #67 留痕行维持开板+station-reviews 行+cards/README 变更行+finished 行级登记·三探针全绿·实活轮收账 commit）")
    if out[0] == u"量产产线":
        out[2] += (u"+**R381 MC-20260926-DIGEST-v3=DIGEST 续件第二件**〔编年史事件=三线扩展 O-20260925-0850 CEO 内容宇宙令·CEO 原话 verbatim 跨三行+五源指针逐条可机核·F-043 成品库第四十二件〕")
for r in e["results"]:
    if r[0] == "380":
        r[0] = "381"; r[1] = u"OS 轮次"
    if r[0] == u"41" and u"成品库登记件" in r[1]:
        r[0] = u"42"
        r[1] = r[1].replace(u"F-001~F-006+F-008~F-042", u"F-001~F-006+F-008~F-043").replace(u"（短产线 N6 收官", u"（短产线 N6 收官")
for dept in e["depts"]:
    if dept["n"] == u"合规审查部":
        dept["t"] = dept["t"].replace(u"F-001~F-006+F-008~F-042 过门登记（四十一件）", u"F-001~F-006+F-008~F-043 过门登记（四十二件）")
io.open(p2, "w", encoding="utf-8", newline="\n").write(json.dumps(e, ensure_ascii=False, indent=1))

print("CLOSE OK ts=%s" % STAMP)
print("task=%s" % d["task"])
