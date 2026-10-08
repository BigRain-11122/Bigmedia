# -*- coding: utf-8 -*-
"""e4_backfill_r1779.py - same-round E4 backfill (append-only + review v1.1 edit)."""
import io, json, os, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
HERE = ROOT + r"\data\storylines\cards\MC-20261009-REACT-v12-tmp"

res = json.load(io.open(os.path.join(HERE, "e4-result.json"), encoding="utf-8"))

# --- 1) clean verdict archive
EV = ROOT + r"\docs\reviews\expert-verdicts\20261009-001434-E4-audience.md"
body = (
u"# E4 参考仪判词 · MC-20261009-REACT-v12《城市速报 012·加油站 20 米之问》（净本存档）\n\n"
u"> 起飞=R1779 00:0x（PID 36924·e4_call.py 脱壳·1500s 窗）→落判=00:14:34（快评 ~6min）·模型=qwen2.5:14b·"
u"原始件=e4-result.json（MC-20261009-REACT-v12-tmp·subprocess PIPE 通道零 ANSI/盲文轮转符污染=原始件即净）·"
u"E4=dept-review §6 双态制参考席（非拦截·七席 ≥9 木桶不受参考位影响）·追加制回填（R180/R187/R1738→R1739 先例）\n\n"
u"## 判词全文（verbatim）\n\n" + res["verdict"] + u"\n"
)
io.open(EV, "w", encoding="utf-8", newline="").write(body)
print("expert-verdicts written:", EV)

# --- 2) review file v1.1: replace in-flight line with backfilled section
RP = ROOT + r"\docs\reviews\review-20261009-mcreact-v12.md"
R = io.open(RP, encoding="utf-8").read()
old = u"- E4 参考仪（受众反应面）：**异步在飞**（R1779 00:1x 起飞 PID 36924·1500s 窗·GPU 争抢态慢评预期〔AIHOT 14b-8k 磨链并窗·R1738→R1739 先例〕→下轮回填追加制·非拦截席·七席 ≥9 木桶不受 E4 参考位影响）。"
new = (
u"- ~~E4 参考仪（受众反应面）：异步在飞~~ → **同轮回填毕（00:14:34 落判快评 ~6min）**：**8.0 三意愿无条件式正面明说**"
u"（会停明说+会保存并转发给朋友明说+8 分明说·「结合真实热点事件和虚构城市的居民反应，形式新颖且有创意」正面定性·"
u"Q2「没有一眼假或空洞套话的地方」明说=信任面续证·附加注=虚构城市对部分读者吸引力折扣如实）·"
u"旗①=逍遥轴位被指略显空洞缺具体建议〔E4 引材料转述句·池句 verbatim 不可改写·**日常口语平淡旗第五现**"
u"=v9「真爽」/v10「早市忙」/v11「热茶暖身」族续·吸收位=M5+M6〕·最弱=侠气轴「有难处，找我准没错」理想化缺实际操作性"
u"〔虚构反应理想化族=v11 最弱同族续·M6 池句选优回访锚〕——**REACT 带读数=v9/v10 8.0→v11 7.0→本件 8.0 回升 1.0 如实记**·"
u"净本 expert-verdicts/20261009-001434-E4-audience.md·非拦截席（七席 6×9.0 木桶维持）\n"
u"\n> v1.1（R1779 同轮回填追加制）：E4 席收口——上节「异步在飞」改回填毕·judgement 全文见净本存档。\n"
)
assert old in R, "review in-flight line not found"
R = R.replace(old, new, 1)
io.open(RP, "w", encoding="utf-8", newline="").write(R)
print("review v1.1 updated")

# --- 3) finished.md E4 backfill line
FB = (
u"\n**F-167 E4 回填（R1779 同轮回填追加制）**：E4 参考仪 00:14:34 落判快评（00:0x 起飞 PID 36924·~6min 窗）**8.0**"
u"（会停明说+会保存并转发给朋友明说+8 分明说=**三意愿无条件式正面明说**·「结合真实热点事件和虚构城市的居民反应，"
u"形式新颖且有创意」正面定性+Q2「没有一眼假或空洞套话的地方」明说=信任面续证·附加注=虚构城市对部分读者吸引力折扣如实）·"
u"旗①=逍遥轴位被指略显空洞缺具体建议〔材料转述句位·池句 verbatim 不可改写·**日常口语平淡旗第五现**"
u"=v9「真爽」/v10「早市忙」/v11「热茶暖身」族续·吸收位=M5+M6〕·最弱=侠气轴「有难处，找我准没错」理想化缺实际操作性"
u"〔虚构反应理想化族=v11 最弱同族续·M6 池句选优回访锚〕·**REACT 带读数=v9/v10 8.0→v11 7.0→本件 8.0 回升 1.0 如实记**·"
u"净本 expert-verdicts/20261009-001434-E4-audience.md·非拦截席（七席 6×9.0 木桶维持）——回填三件毕"
u"（review v1.1 E4 行+净本 expert-verdicts+本行销项）\n"
)
with io.open(ROOT + r"\output\finished.md", "a", encoding="utf-8", newline="") as f:
    f.write(FB)
print("finished.md E4 backfill line appended")

# --- 4) station-reviews row
SR = (
u"| 2026-10-09 | **E4 参考仪同轮回填·MC-20261009-REACT-v12《城市速报 012》（R1779·F-167 链 E4 席收口·快评 ~6min）** | "
u"e4-result.json（MC-20261009-REACT-v12-tmp）+净本 expert-verdicts/20261009-001434-E4-audience.md+review-20261009-mcreact-v12.md v1.1 | "
u"E4 起飞 00:0x→00:14:34 落判 **8.0**：三意愿无条件式正面明说（会停+会保存转发+8 分明说）+「结合真实热点事件和虚构城市居民反应形式新颖且有创意」正面定性+Q2 无一眼假空洞套话明说=信任面；旗①=逍遥轴位空洞缺具体建议〔材料转述句位·池句 verbatim 不可改写·日常口语平淡旗第五现·吸收位 M5+M6〕+最弱=侠气轴「有难处，找我准没错」理想化缺实际操作性〔v11 同族续·M6 池句选优〕·REACT 带 v9/v10 8.0→v11 7.0→8.0 回升如实记·非拦截席·七席木桶维持 |\n"
)
with io.open(ROOT + r"\docs\reviews\station-reviews.md", "a", encoding="utf-8", newline="") as f:
    f.write(SR)
print("station-reviews E4 row appended")
print("ALL-E4-BACKFILL-OK")
