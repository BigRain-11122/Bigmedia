# -*- coding: utf-8 -*-
# R380 close: state.json (tick/log/focus/ts/task) + status-export.json (P-61 derived refresh).
import io, json, os, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- state.json ----------
sp = os.path.join(ROOT, "src", "os", "state.json")
st = json.load(io.open(sp, encoding="utf-8"))
st["tick"] = 380

now = time.strftime("%Y-%m-%d %H:%M")
logline = (
    u"2026-09-26 " + now + u" R380: 生产轮·#67 DIGEST 续件首件全链走门毕（R379 研究件 §5 首选候选领做·两步制 claim 当轮闭环·实活轮）——"
    u"①轮首五查静（无新令 orders 顶=O-1931-HQ-C 已记账·ledger 严格 @ 前缀 23=锚零新转办·decisions 非空行 40=锚零新行·树净零锁 HEAD=e82cb44 R379·日报 2026-09-26 在案不重跑·C-00030 锚不在位=图鉴供给门照守）→可认领活存在（R379 focus 遗留指针=DIGEST 续件候选）→转全任务书生产轮·bigstream-lcard-pipeline 技能激活（R378 建装件产线首用）；"
    u"②MC-20260926-DIGEST-v2《城市盘点 002·量产开闸数字盘点》全链走门：M0 四维分 7/8 A 档（钩 2 三组数字反差链：1 句话 vs 当晚 7 决〔F-019 对照数字结构同源母题〕+6 弹药/7 天否决窗 vs 0 问询+开闸首夜 5 件成品/情 1 AI 自治吃瓜温和如实〔G5+G1 双群〕/时 2 开闸 2 日时点·台账档案常青/台 2 方图复用=MC-001~041 S3 实证）"
    u"+M1 纪实数字汇编律系列化复用（**四源指针逐条可机核**=orders/O-20260924-2126-bm-a.md 令件〔21:26+CEO 原话 verbatim 引文块+呈报口径变更节〕+docs/decisions.md 七决台账+iteration_prompt 生产段 N=6+finished.md F-001~005 开闸首夜口径·零改写虚构·编年史 A 级一料多吃 charter §3·署名=纪实线档案级零虚构居民名）"
    u"+M2 --poster 出图 exit 0+验图 5/5 一次过（转写先行防偏=多模态逐字转写九行全中·h2_size 44=CEO 引文行 20.00em 单行最长驱动·**46 档 20.0==20.0 零余量排除律执行=R293/R310 判例复用**·余量 0.91em=v5/v13 先例带·subs 20.00em<24.21em·em-check-r380.txt）"
    u"+M3「城市盘点 002」四禁零中+系列编号连载识别+M4 四检过（红线五条/三重标注图内双落〔底部行「基于硅基城市真实事件（量产开闸台账档案）」〕/来源双落/编辑价值〔1→7→6→5→0 递进链〕）"
    u"+M4.5 七席 ≥9（6×9.0+E7 N/A·review-20260926-mcdigest-v2.md）+E4 参考仪同轮回填 8.0 三意愿正面明说〔条件式〕（「具体的时间和数据点」+「增强了内容的可信度和可读性」=**纪实密度信任面直接收益续证**〔R290 v1 9.0 首证形态内复现〕·旗①=引文行被旗空洞扣 1=CEO 原话令件 verbatim 不可改写·MC-003 语境门槛族事实变体〔v1 432·0 组行同族第二现〕·吸收位=M5 图文页语境·最弱=视觉设计简单〔载体固有·M6〕·净本 expert-verdicts/20260926-124710-E4-audience.md）"
    u"→**F-042 登记**（成品库第四十一件·L-卡 第三十件·DIGEST 形态第二件）；"
    u"③台账=backlog #67 claim+交付毕（留痕行维持开板）+station-reviews 行+cards/README 变更行+finished.md 行级登记（R301+ 制式）；"
    u"④三探针全绿（board 0 FAIL 5 题 10 稿 5 in production/readiness 3 阻塞皆外部 CEO 面 0 发现〔renders 台账零扰动〕/loop_health 0 FAIL 19 WARN 皆在案史实）；"
    u"⑤例行件：日报 2026-09-26+W39 周审在案不重跑·global-benchmarks day2 ≤7 跳过（下期 ~10-01）·T1 催办=已裁项停用无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=1（E4 qwen2.5:14b 一调=本地 Ollama 零 API token·P-54⑤ 计量律如实记）·发布锁=M5 账号物理件不变（未上线=未测量）。"
    u"下轮=R381 快速路径首查→#67 DIGEST 续件候选（三线扩展 O-0850/技能动员 09-26 等编年史事件·随轮认领）/#63 C-00030 锚轮首核（supply-gated 照守）/REACT 09-27 日报热点窗届日即领/#21 周日立法件 09-27 届日即领——全静即 idle-fast。收账显式列文件 commit+push。"
)
st["log"].append(logline)
st["focus"] = (
    u"R381: #67 DIGEST 续件候选随轮认领（编年史事件候选=三线扩展 O-20260925-0850/技能动员 2026-09-26 等·research §5 在册·R379 判据=编年史 A 级事件+数字密度）"
    u"→#63 图鉴 C-00030 锚轮首核（supply-gated 照守·锚落即领）→REACT 09-27 日报热点窗届日即领→#21 周日立法件 09-27 届日即领"
    u"——新令/集团转办/探针红出现即优先；全静即 idle-fast"
)
st["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
prefix = u"2026-09-26 " + now + u" "
st["task"] = logline[len(prefix):len(prefix) + 60]
json.dump(st, io.open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("state.json tick=%d ts=%s" % (st["tick"], st["ts"]))

# ---------- status-export.json (P-61 derived) ----------
ep = os.path.join(ROOT, "docs", "status-export.json")
se = json.load(io.open(ep, encoding="utf-8"))
se["export_ts"] = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
se["do"] = se.get("do", u"") + (
    u"+DIGEST 续件首件量产开闸编年史盘点（R380 MC-20260926-DIGEST-v2=F-042·R379 研究件 §5 首选候选落地·"
    u"四源指针逐条可机核〔令件 CEO 原话 verbatim+七决台账+N=6+首夜 5 件〕·h2 44 引文行驱动·E4 8.0 三意愿正面〔条件式〕）"
)
for d in se["depts"]:
    if d["n"] == u"工程技术部":
        d["t"] = (
            u"OS 循环 R380（生产轮·#67 DIGEST 续件首件全链走门毕=MC-20260926-DIGEST-v2 F-042〔R379 研究件 §5 首选候选领做·"
            u"四源指针逐条可机核·E4 8.0 同轮回填〕·产线 supply-gated 照守=图鉴 C-00030 锚不在位+REACT 新热点窗 09-27+"
            u"#21 周日件 09-27 届日）·state.ts/task 心跳面刷新"
        )
    if d["n"] == u"合规审查部":
        d["t"] = d["t"].replace(u"F-001~F-006+F-008~F-041 过门登记（四十件）", u"F-001~F-006+F-008~F-042 过门登记（四十一件）")
for o in se["outs"]:
    if o[0] == u"OS 循环":
        o[2] = (
            u"tick 380·R380（生产轮·#67 DIGEST 续件首件全链走门毕：MC-20260926-DIGEST-v2《城市盘点 002·量产开闸数字盘点》"
            u"F-042=成品库第四十一件·L-卡 第三十件·DIGEST 形态第二件〔R379 研究件 §5 首选候选领做·M0 7/8 A 档+四源指针逐条可机核+"
            u"验图 5/5 一次过〔h2 44 引文行 20.00em 驱动·46 档零余量排除律执行〕+七席 ≥9+E4 同轮回填 8.0 三意愿正面〔条件式〕〕·"
            u"backlog #67 留痕行维持开板+station-reviews 行+cards/README 变更行+finished 行级登记·三探针全绿·实活轮收账 commit）"
        )
    if o[0] == u"量产产线":
        o[2] = o[2].replace(u"L-卡 二十九件 F-013~F-041（成品库四十件", u"L-卡 三十件 F-013~F-042（成品库四十一件")
        o[2] = o[2] + (
            u"＋**R380 MC-20260926-DIGEST-v2=DIGEST 续件首件**〔F-042《城市盘点 002·量产开闸数字盘点》·R379 研究件 §5 首选候选落地·"
            u"编年史 A 级四源指针〔orders 令件 CEO 原话 verbatim/decisions 七决/任务书 N=6/finished 首夜 5 件〕·h2_size 44 引文行 20.00em 驱动·"
            u"46 档零余量排除律执行·E4 8.0 三意愿正面明说〔条件式〕〕"
        )
for r in se["results"]:
    if r[1] == u"OS 轮次":
        r[0] = u"380"
    if r[1].startswith(u"成品库登记件"):
        r[0] = u"41"
        r[1] = r[1].replace(u"F-001~F-006+F-008~F-041", u"F-001~F-006+F-008~F-042")
        r[1] = r[1] + (
            u"；**F-042 DIGEST 盘点图文第二件=MC-20260926-DIGEST-v2《城市盘点 002·量产开闸数字盘点》〔R380·R379 研究件 §5 首选候选落地·"
            u"编年史 A 级四源指针·E4 8.0 三意愿正面〔条件式〕〕**"
        )
json.dump(se, io.open(ep, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("status-export export_ts=%s" % se["export_ts"])
