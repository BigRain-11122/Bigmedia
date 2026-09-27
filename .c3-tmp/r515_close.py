# -*- coding: utf-8 -*-
# R515 closeout script: release-schedule v1.3 syncs (verified replaces),
# status-export refresh, state.json account update (tick/ts/task/log).
import io, json, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
NOW = time.strftime("%Y-%m-%d %H:%M:%S")
NOW_MIN = time.strftime("%Y-%m-%d %H:%M")
NOW_ISO = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")

fails = []

def rep(path, old, new, tag):
    s = io.open(path, encoding="utf-8").read()
    n = s.count(old)
    if n != 1:
        fails.append("%s count=%d" % (tag, n))
        return
    io.open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new))

# ---------- release-schedule v1.3 ----------
RS = ROOT + r"\docs\release-schedule-v1.md"
rep(RS, "（批次① 开号后 30 天·46 件库存投放映射）", "（批次① 开号后 30 天·48 件库存投放映射）", "RS1-title")
rep(RS,
    "成品库现登记 **47 件**（`output/finished.md` F-001~F-048·F-007=BS-005e 预留位如实跳号）——HQ 令文「10→30」基数=旧快照，**库存面 47 ≥ 30 已超额达成**。批次① 平台口径可用 45 件",
    "成品库现登记 **48 件**（`output/finished.md` F-001~F-049·F-007=BS-005e 预留位如实跳号）——HQ 令文「10→30」基数=旧快照，**库存面 48 ≥ 30 已超额达成**。批次① 平台口径可用 46 件",
    "RS2-inv")
rep(RS,
    "| 视频线 | 机器叙述视频（60s·9:16·v15 现行+拆条） | 5 | F-001~F-004+F-048（LC-001 拆条） | 视频号原生 ✓ |",
    "| 视频线 | 机器叙述视频（60s·9:16·v15 现行+拆条+稿集） | 6 | F-001~F-004+F-048（LC-001 拆条）+F-049（BS-006 稿集） | 视频号原生 ✓ |",
    "RS3-table")
rep(RS,
    "| 机器叙述视频 | 视频号 | 2 | 28.6% | 5 件=2.5 周（W3 起缺口剩 3 档 §五-1） |",
    "| 机器叙述视频 | 视频号 | 2 | 28.6% | 6 件=3 周（W4 起缺口剩 2 档 §五-1） |",
    "RS4-week")
rep(RS,
    "| | D18 | 视频号·视频 | **[G2 缺口位]** | §五-1 补件 |",
    "| | D18 | 视频号·视频 | BS-006《四条规矩》（F-049·R515 落位） | #79 件2 预产 |",
    "RS5-d18")
rep(RS,
    "**盘点**：固定槽投放 27 件（视频 5+图文 17+有声 5）+缺口位 3 档=30 槽；冗余池 18 件（QUOTE F-015~F-018×4+CENSUS F-031~F-036/F-038~F-040×9+DIGEST F-046/F-047×2+REACT 3 件机动）=M6 调仓弹药+30 天日更冗余（45-27=18 件冗余率 67%·令文「冗余」要求超额）。",
    "**盘点**：固定槽投放 28 件（视频 6+图文 17+有声 5）+缺口位 2 档=30 槽；冗余池 18 件（QUOTE F-015~F-018×4+CENSUS F-031~F-036/F-038~F-040×9+DIGEST F-046/F-047×2+REACT 3 件机动）=M6 调仓弹药+30 天日更冗余（46-28=18 件冗余率 64%·令文「冗余」要求超额）。",
    "RS6-tally")
rep(RS,
    "1. **视频号位缺口剩 3 档**（D18/D22/D25·**D15=R512 落位闭一**=LC-001 F-048）——补件双路径按序：①L-卡拆条试投 **毕 1 件**（LC-001=F-048·源卡 CENSUS-v7 徐根福·R510-R512 全链走门·续拆候选随选优轮评估）②稿集 12-拍新产 **=下一件**（板源=data/drafts 10 稿·5 in production=board 探针 09-27 读数·BS-006+ R513 起链）。**预产窗=开号前**（账号=CEO 物理件日期未定=产线跑道在）·建议 ≥2 件预产覆盖 W3 起位·D-BS-06 排序「批次① 目标平台件优先」照守。",
    "1. **视频号位缺口剩 2 档**（D22/D25·**D15=R512/D18=R515 双闭**=LC-001 F-048+BS-006 F-049）——补件双路径按序：①L-卡拆条试投 **毕 1 件**（LC-001=F-048·源卡 CENSUS-v7 徐根福·R510-R512 全链走门）②稿集 12-拍新产 **毕 1 件**（BS-006《四条规矩》=F-049·R513-R515 全链走门）——**预产 ≥2 件建议达成→#79 done**·D22/D25 续补+BS-007+ 稿集续件/续拆候选=随选优轮评估随轮领。**预产窗=开号前**（账号=CEO 物理件日期未定=产线跑道在）·D-BS-06 排序「批次① 目标平台件优先」照守。",
    "RS7-gap")
rep(RS,
    "- v1.2 2026-09-27 R512：D15 落位闭一（LC-001《城市图鉴 007·徐根福》拆条=F-048·成品库 46→47 件·批次① 平台口径 44→45·机器叙述视频 4→5 件·缺口 4→3 档〔D18/D22/D25〕·预产 1/2 达成·件2 稿集 BS-006+ 随轮领）；§二/§三/§四/§五-1 同步。",
    "- v1.2 2026-09-27 R512：D15 落位闭一（LC-001《城市图鉴 007·徐根福》拆条=F-048·成品库 46→47 件·批次① 平台口径 44→45·机器叙述视频 4→5 件·缺口 4→3 档〔D18/D22/D25〕·预产 1/2 达成·件2 稿集 BS-006+ 随轮领）；§二/§三/§四/§五-1 同步。\n- v1.3 2026-09-27 R515：D18 落位闭二（BS-006《四条规矩》稿集=F-049·成品库 47→48 件·批次① 平台口径 45→46·机器叙述视频 5→6 件·缺口 3→2 档〔D22/D25〕·**预产 ≥2 件达成→#79 done·拆条/稿集双路径全验毕**）；§一标题/§二/§三/§四/§五-1 同步。",
    "RS8-log")

# ---------- status-export ----------
SE = ROOT + r"\docs\status-export.json"
se = json.load(io.open(SE, encoding="utf-8"))
se["export_ts"] = NOW_ISO

os_row_text = ("tick 515：R515 件2 BS-006 收口毕（S2 席 ASR 终轨〔数字面值 3×0 全存活·5.6% 字位系列带内下缘"
               "·ASR 简→繁字形漂移首证=通道伪影化归注记〕+E8 终审七席 9.0+E4 参考仪同轮回填 8.0+M4→"
               "F-049 登记+D18 落位=**#79 整项收官·预产 ≥2 件达成**）——下轮=R516 快速路径首查"
               "（#78 素材面核验/REACT 09-28 窗/W40 周自审开周）")
for row in se.get("outs", []):
    if row and row[0] == "OS 循环":
        row[1] = os_row_text
    if row and row[0] == "media-self-drive O-20260927-1050":
        row[2] = row[2] + ("; R515: piece-2 BS-006 closeout done (ASR final-track digits 3x0 alive + 5.6% char-diff "
                           "in-band + whisper trad-glyph drift normalized and logged + E8 seven seats 9.0 + E4 ref "
                           "same-round 8.0 + M4 + F-049 register = 48th finished piece + D18 slot filled 3->2 -> "
                           "pre-production quota met, both clip-cut and draft-collection paths validated, #79 done)")
    if row and row[0] == "量产产线" and isinstance(row[2], str):
        row[2] = row[2].replace("LC-001 拆条视频 F-048（成品库四十七件",
                                "LC-001 拆条视频 F-048+BS-006 稿集视频 F-049（成品库四十八件")

r515_res = ["515",
    "R515 件2 收口毕（BS-006 S2 席 ASR 终轨：数字面值 3×0 全存活〔0→零形差分离〕+真同音 6 sites/8 chars"
    "+字位 9/11/195≈5.6% 系列带内下缘〔F-004 v15 同位〕+ASR 简→繁字形漂移首证〔通道伪影·diff 繁转简化归计算"
    "如实注记〕+字幕轨 edge-tts 直出 12/12 零损）+E8 终审七席 9.0（review-20260927-bs006-v1.md·E4 参考仪"
    "同轮回填 8.0〔13:45:22 热载快落·旗①=对账声明缺执行细节佐证=信任声明语境门槛族·吸收位 M5 证据链〕）"
    "+M4→F-049 登记（成品库第四十八件·稿集视频线首件）+D18 落位（排期表 v1.3 缺口 3→2 档·预产 ≥2 件达成"
    "→#79 done）；探针=board 0 FAIL/readiness 3 外部阻塞 0 发现（48 renders 全注账）/loop_health 2F+23W "
    "在案定型（account-lag +1 瞬态收账即平）"]
se.setdefault("results", []).insert(0, r515_res)
for row in se.get("results", []):
    if row and row[0] == "47" and isinstance(row[1], str) and "成品库登记件" in row[1]:
        row[0] = "48"
        row[1] = row[1].replace("F-001~F-006+F-008~F-048（", "F-001~F-006+F-008~F-049（")
        row[1] = row[1] + "；**F-049=BS-006《四条规矩》稿集视频线首件（R513-R515 全链走门·D18 落位·排期表缺口 3→2 档·#79 预产达成 done）**"
        break

io.open(SE, "w", encoding="utf-8", newline="").write(json.dumps(se, ensure_ascii=False, indent=1) + "\n")

# ---------- state.json ----------
ST = ROOT + r"\src\os\state.json"
st = json.load(io.open(ST, encoding="utf-8"))

entry = (
    NOW_MIN + " R515: 生产轮·#79 件2 BS-006 收口毕=**#79 整项收官**（O-20260927-1050-HQ-C 议程 2 缺口补件预产线·实活轮·commit 含 P-20260927-07）——"
    "①轮首快速路径五查：orders 36 件〔含 README=R512 定谳口径〕零新增零编辑（顶=O-1050 mtime 12:36:52=R511 收行足迹）+"
    "ledger 五模式正典行数 31=锚零新转办（r515_check 行数口径直计）+decisions UTF8 非空行 56=锚零新行+production=open 自愈核在位+"
    "无 index.lock+树态=仅自产 tmp 批次未闭预期态→backlog 顶行 #79 件2 收口腿=R514 明确指针→转全任务书生产轮；"
    "②S2 席 ASR 终轨（R169 QC recipe medium-int8+beam5+noctx·16 cues/57.34s·asr-check.srt+asr-diff-r515.txt）："
    "**数字面值 3×0 全存活**（0→零=形差分离·值零损·R512 判例）+真同音 6 sites/8 chars（交底→焦底/标识→标时/对账→对照/愿景→院仅/"
    "机制本身→机制时身/脱敏审查→后面）+**字位 9 sites/11 chars/195 字≈5.6%=系列带内下缘**（F-004 v15 同位·LC-001 7.3%/BS-001 v15 9.1% 对照带内）+"
    "**ASR 通道简→繁字形漂移首证**（whisper medium zh 解码面系统性异形·同词同音非语义损伤·diff 以繁转简化归后计算=方法论修红两件轮内咬住"
    "〔首扫 34.8%=标点+字形双未剥口径偏差→PUNCT 集合 int/str 类型 bug 修+TRAD2SIMP 补 从〕·漂移=M6 校准线注记·字幕轨 edge-tts 直出 12/12=发布面零损）；"
    "③E8 终审评审单 review-20260927-bs006-v1.md（环节门 S1 10/10〔R513·13:06:53〕/S2 9.0/S3 9.0〔9:16+57.34s 2.7s 余量+对位 10/12=0.83+"
    "S5.5 角标常驻位 BigStream|BS-006 EP.06〕/S4 9.0〔AIGC 三落自指件首例=b5 拍口播「AI 生成依法打标识包括这条视频」与画面常驻标识同位直证〕+"
    "终审七席 E1/E2/E3/E5/E6/E7/E8 全 9.0——E1=0 交底反差钩+CTA 具名分享对象〔被 AI 吹牛伤过的朋友〕/E2=系统日志体 12 拍一贯+L18 白话换位/"
    "E3=视频号窗 fleet 带内+系列族第 6 件/E6=周全性律对位 D18 缺口主动闭环+呈报纪律口播镜像件〔预估禁止冒充实测=零问询呈报面大众语转译〕/"
    "E7=三源对位+AIGC 全帧直证/E8=层 1.8 六面+hits=[0] hook 白闪仪式位）→七席 ≥9=PASS→**M4 完成态**；"
    "④**E4 参考仪同轮回填 8.0**（e4_call.py 13:45:22 起飞热载快落 23s=R448/R512 同型：会看完+会点赞+可能转发明说〔分享对象具明=对 AI 生成内容"
    "持怀疑态度或被虚假信息困扰的朋友〕=批次参考线带内持平〔视频线 v15 重制带+LC-001 拆条+稿集全 8.0〕·旗①=「数据只从平台后台导出每周跟发布记录"
    "对账」声明可被模仿缺执行细节佐证扣 2=信任声明语境门槛族〔E4 盲评面无证据链固有代价·R444 留痕承诺被评一眼假同族·事实面=声明实真逐轮 git 台账 48 件可机核〕·"
    "吸收位=M5 简介证据链语境·最弱=执行验证机制细节〔未上线未测量诚实边界固有·M6 实测后校准〕·净本 expert-verdicts/20260927-134522-E4-audience）；"
    "⑤**F-049 登记**（成品库第四十八件·稿集视频线首件=稿集路径立线首验·data/drafts 母稿资产复用通道）+**D18 落位**（排期表 v1.3 五处同步："
    "48 件库存/批次① 46/视频 6 件/固定槽 28+缺口 2 档〔D22/D25〕/冗余率 64%·**§五-1 预产 ≥2 件达成〔LC-001 F-048+BS-006 F-049 双路径全验〕→#79 done**·"
    "续产 BS-007+/续拆候选随选优轮评估）；⑥台账=finished.md F-049 行+renders 行升「成品·落位（#79 件2 D18）」+station-reviews R515 行+"
    "bs006 README R515 收口行+backlog #79 done 标+R515 注+orders R515 收行+release-schedule v1.3+status-export 刷（P-61·results 515 行 prepend）；"
    "⑦三探针=board 0 FAIL（5 题 10 稿·5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 物理件+决策 0 发现（48 renders 全注账·exit 1=阻塞≠失败口径）/"
    "loop_health 2 FAIL+23 WARN（FAIL① heartbeat-outage 49min=R425 同事件足迹 R426 已裁定不重复触发·FAIL② account-lag done beats=515>tick=514="
    "本轮在飞 done-beat 先行于收账 tick 瞬态 +1〔R459/R462 在案恒态足迹·新断洞判据 lag ≥2 未破线·本轮收账 tick515 即平〕·23 WARN=13 log-order+"
    "10 heartbeat-gap〔新 1=13:12→13:32 20min=R514 渲染长轮合法 WARN 级〕全在案史实零新增断洞）；"
    "⑧例行件：日报 09-27 在案不重跑（09-28 件=明届日随窗补产）·W39 周审在案（W40 明日 09-28 开周+月度统计注记首件 ≤09-30）·global-benchmarks day3 ≤7 跳过"
    "（下期 ~10-01=#80 并窗）·T1 催办=已裁项停用口径·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·tokens:local=2（S1 qwen2.5:14b=R513 起飞已记账·"
    "E4 qwen2.5:14b 本轮落地记账+ASR=faster-whisper medium 本地 CPU 非生成式 LLM 零 API token 类·本地 Ollama 零 API token·P-54⑤ 计量律）·"
    "发布锁=M5 账号物理件不变（未上线=未测量）·窗口件随查（#78 SC-003 渲染腿维持素材面前置=FluxVerse 实录未到位 r515_check·#63 C-00030/31 锚不在位 "
    "supply-gated 照守·#59 REACT 09-28 窗届日即领〔daily_brief 09-28 缺则先补产〕·#70 OH 下窗 09-29 21:40·#80 10-01 并窗）。"
    "下轮=R516 快速路径首查→#78 SC-003 渲染腿（素材实录到位核验）/REACT 09-28 热点窗/W40 周自审开周，全静即 idle-fast。收账显式列文件 commit+push。"
)

st.setdefault("log", []).append(entry)
st["tick"] = 515
st["ts"] = NOW
prefix = entry.split(" ", 3)
task = entry[len(NOW_MIN) + 1:][:60]
st["task"] = task

io.open(ST, "w", encoding="utf-8", newline="").write(json.dumps(st, ensure_ascii=False, indent=1) + "\n")

# ---------- verify ----------
st2 = json.load(io.open(ST, encoding="utf-8"))
se2 = json.load(io.open(SE, encoding="utf-8"))
print("STATE_OK tick=%s log_n=%d ts=%s" % (st2.get("tick"), len(st2.get("log", [])), st2.get("ts")))
print("EXPORT_OK ts=%s results_n=%d" % (se2.get("export_ts"), len(se2.get("results", []))))
if fails:
    print("REPL_FAILS: " + "; ".join(fails))
else:
    print("RS_REPL_OK")
