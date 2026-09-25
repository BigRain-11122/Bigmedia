# -*- coding: utf-8 -*-
"""R271 collect: capabilities C-30 row + state.json (tick/log/ts/task/focus) + status-export refresh."""
import io, json, re, sys, datetime

sys.stdout.reconfigure(encoding="utf-8")
NOW = datetime.datetime.now()
TS = NOW.strftime("%Y-%m-%d %H:%M:%S")
ISO = NOW.strftime("%Y-%m-%dT%H:%M:%S+08:00")
LOG_MIN = NOW.strftime("%H:%M")

# ---------- 1) capabilities.md: C-30 row + v1.29 changelog ----------
CP = r"docs\capabilities.md"
t = io.open(CP, encoding="utf-8").read()
assert "storyline-craft" not in t, "already registered"
i = t.find("| C-29")
assert i > 0
end = t.find("\n", i)
c30 = ("\n| C-30 | 故事线爆款工艺（storyline-craft T1-T9/C1-C3/A1-A2） | 内容生产部（总裁办公室立制·循环收账入册） | live | "
       "**CEO 反馈令 O-20260925-1720「要大众喜闻乐见的，要有爆款潜质的」**——视频线工艺资产（H1-H8/P1-P8/趣律）向文字/图像/音频三介质移植："
       "文字线 T1-T9（黄金百字/赌局骨架/冲突密度/爽点节拍/金句配额/当事人感/卧槽位/章尾冲突钩/真实瑕疵=爽点）+漫画 C1-C3（尾格 PUNCH/字幕带=梗位/反差前置）"
       "+有声 A1-A2（前 30 秒定留存/单集完整钩+悬念尾）+随件自检表（产稿即检·缺表=草案未完成）；**T1/T2/T3/T8=M4 硬门**（✗=不过）·T4-T7=抽审·红线五条+三重标注照旧前置；"
       "首证双落=ch.1 v2 文字版（SC-001-01-v2·bm-a 闭环·v2=产线默认）+ch.1 v2 有声版（SC-001-01-v2.mp3·R271 循环音频腿：A1 钩位 17.8s 实证+pacing CV 0.666/copy CV 0.719 双高于 v1 散文版 0.396/0.425=爆款节拍机检读数）；"
       "charter v1.3 §5 门禁接线（三线+L-卡 四列全接）。 |")
t = t[:end] + c30 + t[end:]
changelog = ("- 2026-09-25: v1.29 storyline-craft 爆款工艺入册（O-20260925-1720 CEO 反馈令·bm-a 交互会话立制+循环 R271 收账步升表）——"
             "C-30 新席：T1-T9/C1-C3/A1-A2+随件自检表（T1/T2/T3/T8=M4 硬门）·正典=docs/storyline-craft.md v1.0"
             "（证据底座=research/storyline-virality-research-v1.md·现产五篇诚实终诊全违 H1=散文化病根在案）；"
             "首证双落=ch.1 v2 文字版（bm-a·v2=产线默认）+ch.1 v2 有声版（R271·A1/A2 适配机检实证）。live×25。")
t = t.rstrip("\n") + "\n" + changelog + "\n"
io.open(CP, "w", encoding="utf-8", newline="\n").write(t)
print("capabilities.md: C-30 + v1.29 appended")

# ---------- 2) state.json ----------
SP = r"src\os\state.json"
s = io.open(SP, encoding="utf-8").read()
json.loads(s)  # pre-check

entry = (
    "2026-09-25 " + LOG_MIN + " R271: 生产轮·O-20260925-1720 新令收讫+ch.1 有声 v2 重渲染第一程（实活轮·并窗 R266-R270 五 idle-fast 随本轮一并收账）——"
    "①轮首快速路径五查见新令：orders 顶=O-20260925-1720-bm-a（17:21 落盘·CEO 爆款反馈令「先调研·大众喜闻乐见·爆款潜质」·"
    "bm-a 交互会话全链闭环①调研 virality-research②立制 storyline-craft v1.0〔T1-T9/C1-C3/A1-A2·T1/T2/T3/T8=M4 硬门〕"
    "③ch.1 v2 重制=产线默认④charter v1.3·回执在令）→转全任务书；循环余腿=令文「音频重渲染以 v2 为源」=TTS 链循环辖区→claim 落 backlog #30；"
    "集团双锚静（ledger 行含 @ 15=锚零新转办/decisions UTF8 非空 29 总 32=锚零新行）；"
    "②ch.1 有声 v2 第一程交付：beats 13 拍（SC-001-01-v2.beats.txt·同文本逐字机械核验 12 段 miss 0+cta 去括号 OK+hook 三重标注 OK+A1 钩位 OK·"
    "markdown 粗体剥离=排版面结构处理·same_text_r271.py 实跑）→TTS light 产线默认（Yunyang+cyber light+human 42）→"
    "SC-001-01-v2.mp3 落位（3:01.0=ffprobe 180.95s·13 cues）+srt；S2 ai_feel 门全绿（gaps 12 处 0.239-0.558s varied/pacing CV 0.666/prosody 9 档 13 拍/copy CV 0.719·"
    "CV 双高于 v1 散文版 0.396/0.425=爆款工艺节拍实证）→M4 四检过（charter §5：红线五条+三重标注 cue01 内置+来源级=v2 文末七条清单指针〔与 v1 同源零增删〕+S2 机检；"
    "storyline-craft §3：A1 ✓〔cue01 声明 12.43s→黄金百字 17.8s 入钩零寒暄〕+A2 ✓〔单集完整赌局=天黑前一万个+章尾辣钩+具体下章预告〕·T1/T2/T3/T8 硬门随 v2 源文自检表九条全过在案）；"
    "台账=audio/README 台账行+门禁记录块+状态行+变更行（随行清账=ch.5 表行补 R231 成品标陈账）+backlog #29 done 标+#30 入板顶行+capabilities v1.29 C-30 新席（storyline-craft 完工升表·bm-a 立制循环收账步入册）；"
    "**E8 终审听审+S2 席 ASR 终轨+F-008 指针升 v2 处置（v1 标历史档·R189 SUPERSEDED 先例）=下轮 R272**（R222→R223 先例节律·tmp 批闭收账随收官轮）；"
    "③三探针全绿=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+0 发现（弃件清账新基线维持·阻塞≠失败口径 exit 1）/"
    "loop_health 0 FAIL 17 WARN 皆在案史实（11 log-order+6 heartbeat-gap·tick270=done270 对账平·state-ts 门零红零滞后）——"
    "探针输出件=python 内部 io.open 重定向（R269 教训律执行·首跑 PS > 管道 UTF-16 坑复现即重制·r271 三件留 .bs005-tmp）；"
    "④例行件：日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks 更新记录 2026-09-24 day2 ≤7 跳过（下期 ~10-01）·"
    "T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（O-1720=本司内容面反馈令·bm-a 已闭环零集团层悬项·零膨胀）·"
    "tokens:local=0（TTS=edge-tts 云免费接口非本地 LLM·ai_feel 纯脚本机检·P-54⑤ 计量律如实记）·素材窗核=R270 读数延续态免探针（实活轮预算不烧·Biggame 总控窗仍被 CEO 仪表盘 F11 覆盖线维持）"
    "②③ bm-a 复核=ch.1 v2 已落盘·ch.2-ch.5 v2 未落=稿落即随轮认领（新连载节律同口径）。"
    "下轮=R272 ch.1 v2 收官（E8 听审+ASR+F-008 处置）或快速路径首查。收账显式列文件 commit+push（并窗 R266-R270+R271 一并·区间注记）。"
)

anchor = '\n ],\n "ts": "2026-09-25 17:14:10",'
assert anchor in s, "state tail anchor missing"
s = s.replace(
    'R266-R271）。 "\n ],\n "ts": "2026-09-25 17:14:10",',
    'R266-R271）。",\n "' + entry + '",\n ],\n "ts": "' + TS + '",',
    1,
)
s = s.replace('"tick": 270,', '"tick": 271,', 1)
old_task_prefix = '"task": "R270: idle-fast'
i = s.find(old_task_prefix)
assert i > 0
j = s.find('"', i + 9)
s = s[:i] + '"task": "' + entry.split("R271: ", 1)[1][:60] + '"' + s[j + 1:]

fm = re.search(r'"focus": "([^"]*)"', s)
assert fm, "focus field missing"
new_focus = ("R272: ch.1 v2 收官优先（E8 终审听审+S2 席 ASR 终轨+F-008 指针升 v2 处置〔v1 标历史档·R189 SUPERSEDED 先例〕+tmp 批闭收账）·"
             "快速路径首查照走（新令/集团转办/ch.2-ch.5 v2 稿落盘迹象/素材窗安全窗复核）")
s = s[: fm.start(1)] + new_focus + s[fm.end(1):]

json.loads(s)  # post-check (R256/R257/R260 trailing-comma guard)
io.open(SP, "w", encoding="utf-8", newline="\n").write(s)
print("state.json: tick 271, log R271, ts/task/focus refreshed, JSON_OK")

# ---------- 3) status-export.json ----------
XP = r"docs\status-export.json"
x = io.open(XP, encoding="utf-8").read()
json.loads(x)

x = x.replace('"export_ts": "2026-09-25T17:14:10+08:00"', '"export_ts": "' + ISO + '"', 1)
x = x.replace(
    '"do": "AI 媒体产线：M0-M6 全链 OS 自治（量产已开闸 D-BS-06·成品库生产模式·发布仍锁账号物理件·未上线=未测量）+硅基城市内容宇宙三线新纪元（O-0850：网文/有声/漫画）+大众内容自动化面扩展（O-1327 CEO 直令 24h 快车道：调研毕→立制+首件）"',
    '"do": "AI 媒体产线：M0-M6 全链 OS 自治（量产已开闸 D-BS-06·成品库生产模式·发布仍锁账号物理件·未上线=未测量）+硅基城市内容宇宙三线新纪元（O-0850：网文/有声/漫画）+大众内容自动化面扩展（O-1327 24h 快车道三执行件全毕）+故事线爆款工艺立制（O-1720：storyline-craft T1-T9/C1-C3/A1-A2·ch.1 v2=产线默认·音频重渲染腿在链）"',
    1,
)
x = x.replace(
    '"t": "O-20260925-1327 三执行件全毕（R250 调研+R251 立制/首件·24h 快车道提前毕）+O-0850 三线批（#27 ①②③ 毕·④发布锁内挂账）·委托决策令 O-2126 七决闭环（否决窗至 10-01）"',
    '"t": "O-20260925-1720 爆款反馈令 bm-a 全链闭环（调研+storyline-craft v1.0 立制+ch.1 v2=产线默认+charter v1.3·循环音频重渲染腿在链 R271）+O-1327 三执行件全毕（R250-R253 提前毕）+O-0850 三线批（#27 ①②③ 毕·④发布锁内挂账）·委托决策令 O-2126 七决闭环（否决窗至 10-01）"',
    1,
)
x = x.replace(
    '"t": "OS 循环 R270（idle-fast：五静+探针绿·并窗 5/6·素材窗安全窗复核=Biggame 总控窗开态延续但仍被 CEO 硅基仪表盘 F11 覆盖〔bm-c 告警 1147min 延续态〕·D-BS-08 复活条款零新面板触发=留档零扰动）·ledger @15/decisions 29 双锚稳·state.ts/task 心跳面刷新·探针复制律=Python UTF-8 通道执行零违例（R266 教训生效）+探针输出重定向=python 内部 io.open（R269 PS > 管道乱码案）"',
    '"t": "OS 循环 R271（实活轮：O-20260925-1720 新令收讫·ch.1 有声 v2 重渲染第一程毕〔SC-001-01-v2.mp3 3:01.0·13 cues·S2 全绿·M4+A1-A2 过〕·并窗 R266-R270 五 idle-fast 随收）·ledger @15/decisions 29 双锚稳·state.ts/task 心跳面刷新·素材窗=R270 延续态免探针（Biggame 总控窗仍被 CEO 仪表盘 F11 覆盖线维持）"',
    1,
)
x = x.replace(
    '"tick 270·R270（idle-fast：五静+探针绿·并窗 5/6——素材窗安全窗复核=Biggame 总控窗开态延续但仍被 CEO 硅基仪表盘 F11 全屏覆盖〔R252 事故窗禁触·bm-c 告警 1147min 延续态〕·D-BS-08 复活条款零新面板触发=留档零扰动待安全窗复核）"',
    '"tick 271·R271（实活轮：O-20260925-1720 爆款反馈令收讫·bm-a ①-④ 闭环+循环音频腿第一程毕——ch.1 v2 重渲染 SC-001-01-v2.mp3 落位〔3:01.0·13 cues·S2 全绿：pacing CV 0.666/copy CV 0.719 双高于 v1 散文版=爆款节拍实证〕·E8/ASR/F-008 升 v2 处置=R272）"',
    1,
)
x = x.replace(
    "——**五件在库**·ch.6 网文稿未落（cta 周浩宇/陈雅雯双钩已埋）=新连载节律随轮认领\"",
    "——**五件在库**·ch.6 网文稿未落（cta 周浩宇/陈雅雯双钩已埋）=新连载节律随轮认领+**SC-001-01-v2 重渲染在链（R271 第一程·O-1720「v2=产线默认·音频重渲染以 v2 为源」·E8/ASR/F-008 升 v2 处置=R272）\"",
    1,
)
x = x.replace(
    '"270",\n      "OS 轮次"',
    '"271",\n      "OS 轮次"',
    1,
)
x = x.replace(
    '"31",\n      "CEO 令收讫（O-20260925-1327-HQ-C 大众内容自动化调研令=R249 收讫认领）"',
    '"32",\n      "CEO 令收讫（O-20260925-1720-bm-a 故事线爆款反馈令=R271 收讫·bm-a ①-④ 闭环+循环音频腿在链）"',
    1,
)
x = x.replace(
    '[\n      "L-卡 图文轻内容线",\n      "live"\n    ]\n  ],',
    '[\n      "L-卡 图文轻内容线",\n      "live"\n    ],\n    [\n      "storyline-craft 爆款工艺",\n      "live"\n    ]\n  ],',
    1,
)
json.loads(x)  # post-check
io.open(XP, "w", encoding="utf-8", newline="\n").write(x)
print("status-export.json: export_ts/do/depts/outs/results/chips refreshed, JSON_OK")
print("DONE", TS)
