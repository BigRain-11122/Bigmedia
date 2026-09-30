# -*- coding: utf-8 -*-
# R691 closeout: 6 ledger updates + state.json (tick 690->691) + status-export refresh
import json, io, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
now = time.strftime("%Y-%m-%d %H:%M:%S")
now_iso = time.strftime("%Y-%m-%dT%H:%M:%S+08:00")

def rd(p):
    return io.open(ROOT + p, encoding="utf-8").read()
def wr(p, s):
    io.open(ROOT + p, "w", encoding="utf-8").write(s)

# ---------- 1. renders README: declaration row closure + new table row ----------
rr = rd(r"\output\renders\README.md")
old_tail = (u"——余腿=渲染腿（F-036 PNG 派生 census-card-v17-vertical→对位表 12/12→R-E shipinhao"
            u"〔--series-id=拆条 005·源城市图鉴 017〕→S2 三门→帧验三律）→收官腿（E8+ASR+E4+M4→F-059 登记→冗余池第二件落位）随轮领。")
new_tail = (u"——**R691 渲染腿毕**：批中间件增 r691_build_leg_a.py[自产源件+对位表构建件]+r691_render_call.py"
            u"[UTF-8 argv 渲染 wrapper·series-id=拆条 005·源城市图鉴 017]+r691_s2_gates.py[S2 三门执行件]+"
            u"r691_fs_extract.py[帧验采样件·fs-h00~11+fs-m/t 00/04/09+双 tile+labelzone/bottomzone/badgezone 裁切]+"
            u"probe-v17-mid.png[源件探针帧]+s2-results.md[三门读数档]——自产源件=data/sources/footage/"
            u"census-card-v17-vertical（F-036 成品卡 PNG 派生·scale 660+pad y=160+zoompan ≤1.04·13.000s·"
            u"ffprobe 与 v16 参照逐参数一致 1080×1920@30·mp4 gitignored=R21/R512 先例）+对位表 cards-v1-matched.json "
            u"落正位（12/12 逐拍 visual·源卡即证据·visual-ratio 1.00）+R-E shipinhao 渲染 lc-005-v1-shipinhao-60s.mp4"
            u"（12 段 11 柔 0 硬切·55.97s·4.0s 余量·hits=[0,11]·S5.5 角标=BigStream|拆条 005·源城市图鉴 017+§4.5 三开关）+"
            u"S2 三门全绿+帧验三律全过（station-reviews R691 S2 行）→收官腿（E8+ASR+E4+M4→F-059 登记→冗余池第二件落位）R692 随轮领。")
assert old_tail in rr, "renders declaration tail not found"
rr = rr.replace(old_tail, new_tail)

row = (u"\n| lc-005-v1-shipinhao-60s.mp4 | **在链·生产件（queue §E 批活池 E5 件·冗余扩容位第二件·源卡=CENSUS-v17 F-036 高小满·"
       u"R689 起链→R691 渲染+S2 三门+帧验三律·收官腿=E8+ASR+E4+M4→F-059 登记→冗余池第二件落位）** | "
       u"**R-E shipinhao 12 段 11 柔转场 0 硬切**·9:16 1080×1920·**55.97s ffprobe 实测·4.0s 余量**·hits=[0,11]·"
       u"**S5.5 角标常驻位**=BigStream\\|拆条 005·源城市图鉴 017+§4.5 三开关[glow/scanlines/sys.beat=NN t=MM:SS]·"
       u"plan.series+s45_dials 入 plan.json·**拆条形态对位=源卡即证据 12/12**（census-card-v17-vertical 源卡画面×12·"
       u"visual-ratio 1.00·源件=F-036 PNG 派生 scale 660+pad y=160+zoompan ≤1.04·13s=LC-001/002/003/004 R511 法·"
       u"素材探针先行=卡面九行全读+AIGC 标签位=卡面左上=与 F-027/F-035 同位族）——**S2 三门 R691 循环独立执法全绿**："
       u"ai_feel 0 FAIL 0 WARN（gaps 11 处 0.233-0.558s·pacing CV 0.221·prosody 9 档 12 拍·copy CV 0.299）+"
       u"层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过）+"
       u"spec 微信视频号双 PASS（9:16+55.97s ∈30-60s 窗 4.0s 余量）——**帧验三律全过**：拍头 12/12 语义全中"
       u"（源卡七行全分辨率零乱码零截断+拍标题逐拍对位+sys.beat 01→12 连续+角标全帧·badgezone 全分辨率定谳=「拆条 005」）+"
       u"段中尾 6/6 稳定零录穿（law2=三最长拍 b0/b4/b9 动态取〔5.93/6.40/5.67s〕·tile 缩略误读全分辨率定谳=卡面文字净·"
       u"手段问题非画面问题·格 1 副标题块内两行=R9「块居中行内左对齐」已知渲染属性非缺陷）+回环 crossings={}"
       u"（max 拍 6.40s<源 13s·诚实计算）+AIGC 双标识分层可读（帧头标识+卡面左上标签垂直错开零叠压·R511 避让法前置执行零修红·"
       u"底部区裁切单行净零碰撞） | plan.json 入 git·收官腿待 R692（E8+ASR+E4→M4→F-059 登记→冗余池第二件落位）")
if not rr.endswith("\n"):
    rr += "\n"
rr += row + "\n"
wr(r"\output\renders\README.md", rr)
print("1 renders README ok")

# ---------- 2. station-reviews: R691 S2 row ----------
sr = rd(r"\docs\reviews\station-reviews.md")
sr_row = (u"\n| 2026-09-29 | **S2 三门循环独立执法+帧验三律（lc-005-v1-shipinhao=queue §E 批活池 E5 件·冗余扩容位第二件·"
          u"源卡 CENSUS-v17 F-036 高小满·R691 渲染腿）** | lc-005-v1-shipinhao-60s.mp4（R-E shipinhao 12 段·11 柔转场 0 硬切·55.97s） | "
          u"循环独立执法（ai_feel+层 1.8+spec 微信视频号·纯脚本机检零 LLM）+帧验三律（会话内建多模态） | —（机检档·E8 终审待收官腿） | "
          u"对位表=cards-v1-matched（**拆条形态源卡即证据 12/12**·visual-ratio 1.00）+S2 三门全绿（ai_feel 0F0W gaps 11 处 0.233-0.558s "
          u"CV 0.221/0.299+层 1.8 六面 PASS+spec 双 PASS 4.0s 余量）+帧验三律全过（拍头 12/12 语义全中+段中尾 6/6 零录穿"
          u"〔law2=b0/b4/b9 动态三最长〕+回环 crossings={} max 6.40s<13s+AIGC 双标识分层〔帧头+卡面左上垂直错开·R511 避让前置零修红〕+"
          u"全分辨率定谳=角标「拆条 005」/卡面七行净/R9 块居中行内左对齐已知属性非缺陷）+台账=renders 在链行+lc005 README 生产记录+queue burn |")
if not sr.endswith("\n"):
    sr += "\n"
sr += sr_row + "\n"
wr(r"\docs\reviews\station-reviews.md", sr)
print("2 station-reviews ok")

# ---------- 3. lc005 README: production record ----------
lc = rd(r"\data\sources\lc005\README.md")
lc_rec = (u"\n- 2026-09-29 R691 渲染腿毕（R684/R687 同型五步·R689/R690 claim 沿用）：①素材探针先行=F-036 卡多模态九行全读"
          u"（AIGC 标签位=卡面左上·与 F-027/F-035 同位族=R511 避让法直接适用·前置执行零修红）→②自产源件 "
          u"data/sources/footage/census-card-v17-vertical.mp4（F-036 PNG 派生·scale 660+pad y=160+zoompan ≤1.04·13.000s·"
          u"ffprobe 与 v8/v13/v16 参照逐参数一致 1080×1920@30）→③对位表 cards-v1-matched.json 12/12 逐拍 visual（源卡即证据·"
          u"钩子/档案/信条行 verbatim 直引+锚 C-00026 字段展开同源多用注记·b6 守夜灯灵〔C-00028 互证〕/b9 陆海峰〔C-00025 双向对位="
          u"LC-004 b10 承接·连载链直接续证〕=跨卡互证拍·visual-ratio 1.00）→④R-E shipinhao 渲染 lc-005-v1-shipinhao-60s.mp4"
          u"（12 段 11 柔 0 硬切·55.97s·4.0s 余量·hits=[0,11]·S5.5 角标=BigStream|拆条 005·源城市图鉴 017+§4.5 三开关·plan.json 入 git）→"
          u"⑤S2 三门全绿（ai_feel 0F0W+层 1.8 六面 PASS+spec 微信视频号双 PASS 4.0s 余量）+帧验三律全过（拍头 12/12+段中尾 6/6 零录穿+"
          u"回环 crossings={}+AIGC 双标识分层·station-reviews R691 S2 行）——收官腿=E8+ASR+E4+M4→F-059 登记→冗余池第二件落位（R692 随轮领）。")
if not lc.endswith("\n"):
    lc += "\n"
lc += lc_rec + "\n"
wr(r"\data\sources\lc005\README.md", lc)
print("3 lc005 README ok")

# ---------- 4. queue burn line ----------
q = rd(r"\docs\self-improvement-queue.md")
q_last = u"渲染腿+收官腿随轮领（F-059 登记→冗余池第二件落位）。"
q_new = (q_last + u"\n- 2026-09-29: **E5 LC-005 渲染腿毕（R691·R684/R687 同型五步）：F-036 PNG 派生 census-card-v17-vertical 13.000s+"
         u"对位表 12/12 visual-ratio 1.00+R-E shipinhao lc-005-v1-shipinhao-60s.mp4 55.97s 4.0s 余量（角标拆条 005·源城市图鉴 017）+"
         u"S2 三门全绿+帧验三律全过（拍头 12/12+段中尾 6/6 零录穿+回环 crossings={}+AIGC 双标识分层）**——收官腿"
         u"（E8+ASR+E4+M4→F-059→冗余池第二件落位）R692 随轮领；lane=E3〔09-30 热点窗〕+E5〔active〕维持 ≥2。")
assert q_last in q, "queue burn anchor not found"
q = q.replace(q_last, q_new)
wr(r"\docs\self-improvement-queue.md", q)
print("4 queue burn ok")

# ---------- 5. backlog #79 R691 note (append after last LC-005 sub-bullet if present) ----------
bk = rd(r"\src\os\backlog.md")
bk_lines = bk.splitlines("\n")
anchor_idx = None
for i, l in enumerate(bk_lines):
    if "R690 承接" in l or ("LC-005" in l and "R690" in l):
        anchor_idx = i
if anchor_idx is None:
    for i, l in enumerate(bk_lines):
        if "LC-005" in l and ("渲染腿" in l or "起链" in l):
            anchor_idx = i
bk_note = (u"   **[R691 渲染腿毕=LC-005 出片 2026-09-29（R689/R690 claim 沿用·R684/R687 同型五步）：F-036 PNG 派生 "
           u"census-card-v17-vertical 13s（R511 法零修红）→对位表 12/12 visual-ratio 1.00→R-E shipinhao lc-005-v1-shipinhao-60s.mp4 "
           u"55.97s 4.0s 余量（角标拆条 005·源城市图鉴 017+§4.5 三开关）→S2 三门全绿（ai_feel 0F0W+spec 双 PASS+层 1.8 六面 PASS）→"
           u"帧验三律全过（拍头 12/12+段中尾 6/6 零录穿+回环 crossings={}+AIGC 双标识分层·tile 误读全分辨率定谳）——收官腿"
           u"（E8+ASR+E4+M4→F-059→冗余池第二件落位）R692 随轮领。]**")
if anchor_idx is not None:
    bk_lines.insert(anchor_idx + 1, bk_note)
    wr(r"\src\os\backlog.md", "\n".join(bk_lines))
    print("5 backlog note ok after line", anchor_idx + 1)
else:
    print("5 backlog anchor NOT FOUND - skipped (honest)")

# ---------- 6. state.json close ----------
r691 = ("2026-09-29 " + now[11:16] + " R691: 生产轮·LC-005 高小满拆条渲染腿毕（queue §E 批活池 E5 件·冗余扩容位第二件·"
        "R684/R687 同型五步·实活轮）——①轮首快速路径五查静（正典 r689_probe.py 复跑：orders 顶 O-20260928-1910 42 件锚未动/"
        "ledger 六模式 CaseSensitive 38=锚零新转办/decisions UTF8 非空行 75=锚零新行/production=open 自愈核在位/无 index.lock·"
        "树态=bm-a codex 批未闭让位维持〔README+2/-1/city-humanities+12/-2 mtime 04:06 未动〕+自产 tmp 族预期态）→可领活=focus① 兑现；"
        "②渲染腿五步毕：素材探针先行=F-036 卡多模态九行全读（AIGC 标签位=卡面左上·与 F-027/F-035 同位族=R511 避让法直接适用·"
        "前置执行零修红）→自产源件 data/sources/footage/census-card-v17-vertical.mp4（F-036 PNG 派生·scale 660+pad y=160+zoompan ≤1.04·"
        "13.000s·ffprobe 与 v16 参照逐参数一致 1080×1920@30）→对位表 cards-v1-matched.json 12/12 逐拍 visual（源卡即证据·钩子/档案/"
        "信条行 verbatim 直引+锚 C-00026 字段展开同源多用注记·b6 守夜灯灵〔C-00028〕/b9 陆海峰〔C-00025 双向对位=LC-004 b10 承接〕="
        "跨卡互证拍·visual-ratio 1.00）→R-E shipinhao 渲染 lc-005-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·hits=[0,11]·S5.5 角标="
        "BigStream|拆条 005·源城市图鉴 017+§4.5 三开关·plan.json 入 git）；③S2 三门循环独立执法全绿=ai_feel 0 FAIL 0 WARN"
        "（gaps 11 处 0.233-0.558s·pacing CV 0.221·prosody 9 档 12 拍·copy CV 0.299）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+"
        "visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过）+spec 微信视频号双 PASS（9:16+55.97s∈30-60s 窗 4.0s 余量）；"
        "④帧验三律全过=拍头 12/12 语义全中（源卡九行多模态全读+拍标题逐拍对位+sys.beat 01→12 连续+角标 12 帧全在）+段中尾 6/6 稳定零录穿"
        "（law2=三最长拍 b0/b4/b9 动态取〔5.93/6.40/5.67s〕·tile 缩略误读三处全分辨率定谳=卡面文字净/「拆条 005」非「系列」·手段问题非画面问题·"
        "格 1 副标题块内两行=R9「块居中行内左对齐」已知渲染属性非缺陷）+回环 crossings={}（max 拍 6.40s<源 13s·诚实计算）+AIGC 双标识分层可读"
        "（帧头标识+卡面左上标签垂直错开零叠压·fs-h00 全分辨率实证·底部区裁切单行净零碰撞）；⑤台账六件=renders README〔声明行渲染腿收口+在链表行〕+"
        "station-reviews R691 S2 行+lc005 README 生产记录+queue §E burn 行+backlog #79 R691 注+status-export 刷（live 三行=R691 实况）；"
        "⑥三探针（收账步）=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面+1 发现（render-unannot lc-005=在链件诚实预期红·"
        "R680/R684/R687 同型·F-059 登记即清）/loop_health 3 FAIL+54 WARN 皆在案类（2 outage 同事件足迹已裁定+account-lag done691>tick690="
        "轮内自然态 tick691 收账自平）；例行件：日报 09-29 在案不重跑（R637 断轮件补产）/W40 周审在案/global-benchmarks day5 ≤7 跳过"
        "（下期 10-01=#80 并窗）/#70 OSS 下窗切片 2=21:40 后开未到（切片 1 已毕 R644=窗面义务足）/#86 c+d 让位维持（bm-a 批未闭）/"
        "T1 催办=已裁项停用口径/当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）/tokens:local=0（S2 三门纯脚本机检+帧验=会话内建多模态"
        "零本地模型调用·P-54⑤ 计量律）——下轮=R692 LC-005 收官腿（E8+ASR+E4→M4→F-059 登记→冗余池第二件落位→renders 行升成品标→tmp 批闭 commit）"
        "+E3 REACT-v6 09-30 窗。收账显式列文件 commit+push。")

focus = ("R692: ①LC-005 收官腿随轮领（R685/R688 同型：E8 终审+ASR 终轨+E4 参考仪→M4→F-059 登记→冗余池第二件落位→"
         "renders 行升「成品·冗余池落位」标→tmp 批闭 commit）；②E3 REACT-v6=09-30 热点窗开随轮领（P-1 试点 2/2 终判挂本件）；"
         "③#70 OSS 下窗切片 2=09-29 21:40 后开随轮领；④#86 c+d 让位解除判据=bm-a codex 批闭 commit 落地随轮首查（mtime 04:06 锚）；"
         "⑤批活池补池随 E5 出池再评（BS-007 稿集件候选）；⑥产品优先律实况面三行随轮刷（status-export live 节）——"
         "五查锚=orders 顶 O-20260928-1910·ledger 38（六模式 CaseSensitive=正典 r689_probe.py 口径·禁自写变体模式）·decisions 75")

task = r691.split(" R691: ", 1)[1]
task = ("R691: " + task)[:60]

st = json.loads(rd(r"\src\os\state.json"))
st["tick"] = 691
st["focus"] = focus
st["log"].append(r691)
st["ts"] = now
st["task"] = task
wr(r"\src\os\state.json", json.dumps(st, ensure_ascii=False, indent=1))
print("6 state.json ok tick", st["tick"], "log", len(st["log"]))

# ---------- 7. status-export refresh ----------
ex = json.loads(rd(r"\docs\status-export.json"))
ex["export_ts"] = now_iso
ex["outs"][0] = [
    u"OS 循环",
    (u"tick 691，R691 生产轮·LC-005 高小满拆条渲染腿毕（queue §E 批活池 E5 件·冗余扩容位第二件·R684/R687 同型五步）："
     u"F-036 PNG 派生 census-card-v17-vertical 13.000s（R511 法零修红）→对位表 12/12 visual-ratio 1.00→R-E shipinhao "
     u"lc-005-v1-shipinhao-60s.mp4 55.97s 4.0s 余量（角标拆条 005·源城市图鉴 017+§4.5 三开关·hits=[0,11]）→S2 三门全绿"
     u"（ai_feel 0F0W+spec 微信视频号双 PASS+层 1.8 六面 PASS）→帧验三律全过（拍头 12/12 语义全中+段中尾 6/6 零录穿+回环 "
     u"crossings={}+AIGC 双标识分层·tile 误读全分辨率定谳）；五查三锚静（orders O-1910/ledger 38/decisions 75·bm-a codex 批未闭"
     u"让位维持）·三探针 board 0F/readiness 3 外部+1 在链预期红（F-059 登记即清）/loop 3F+54W 在案类（tick691 收账自平）·"
     u"tokens:local=0·下轮=R692 LC-005 收官腿（E8+ASR+E4→M4→F-059→冗余池第二件落位）+E3 REACT-v6 09-30 窗")
]
ex["results"].append([
    "691",
    (u"R691: 生产轮·LC-005 高小满拆条渲染腿毕（queue §E E5 件·冗余扩容位第二件·R684/R687 同型五步）：源卡探针九行全读→"
     u"census-card-v17-vertical 自产源件 13.000s（R511 法零修红）→对位表 12/12 visual-ratio 1.00→R-E shipinhao 55.97s 4.0s 余量"
     u"（角标拆条 005·源城市图鉴 017+§4.5 三开关）→S2 三门全绿（ai_feel 0F0W+spec 双 PASS+层 1.8 六面 PASS）→帧验三律全过"
     u"（拍头 12/12+段中尾 6/6 零录穿·law2=b0/b4/b9 动态三最长+回环 crossings={}+AIGC 双标识分层+全分辨率定谳=拆条 005/卡面七行/"
     u"R9 块居中行内左对齐已知属性）；台账六件（renders 声明行收口+在链行/station-reviews S2 行/lc005 README/queue burn/backlog #79 注/"
     u"status-export live）；五查三锚静（正典 r689_probe.py 复跑·ledger 38/decisions 75）·三探针 board 0F/readiness 3 外部+1 在链预期红"
     u"（F-059 登记即清）/loop 3F+54W 在案类（tick691 收账自平）·例行件在案（日报/W40 周审/GB ≤7 跳过）·tokens:local=0"
     u"——下轮 R692=LC-005 收官腿（E8+ASR+E4→M4→F-059→冗余池第二件落位）+E3 REACT-v6 09-30 窗")
])
ex["live"] = [
    u"当前活：LC-005 高小满拆条（queue §E E5·冗余扩容位第二件）渲染腿毕——lc-005-v1-shipinhao-60s.mp4 出片 55.97s+S2 三门全绿+帧验三律全过；收官腿（E8+ASR+E4→F-059）随轮领",
    u"最近实物：output/renders/lc-005-v1-shipinhao-60s.mp4（9:16·55.97s·4.0s 余量·角标拆条 005·源城市图鉴 017·S2 三门全绿·2026-09-29 16:4x）+对位表 data/sources/lc005/cards-v1-matched.json 12/12——上件成品=F-058 lc-004-v1-shipinhao-60s.mp4（冗余池首件 15:2x）",
    u"下个里程碑：LC-005 收官=F-059 登记入冗余池第二件（窗 ≤48h·10-01 前）+E3 REACT-v6 09-30 热点窗（P-1 反套路化选句律终判件）"
]
wr(r"\docs\status-export.json", json.dumps(ex, ensure_ascii=False, indent=1))
print("7 status-export ok", now_iso)

# ---------- verify ----------
st2 = json.loads(rd(r"\src\os\state.json"))
ex2 = json.loads(rd(r"\docs\status-export.json"))
lines = open(ROOT + r"\src\os\state.json", encoding="utf-8").read()
checks = {
    "tick": st2["tick"] == 691,
    "log_last_r691": st2["log"][-1].startswith("2026-09-29") and "R691" in st2["log"][-1],
    "log_count": len(st2["log"]) == 716,
    "ts": st2["ts"] == now,
    "task_len60": len(st2["task"]) <= 61 and st2["task"].startswith("R691"),
    "focus_r692": st2["focus"].startswith("R692"),
    "export_ts": ex2["export_ts"] == now_iso,
    "results_tail": ex2["results"][-1][0] == "691",
    "live3": len(ex2["live"]) == 3,
    "state_json_valid": True,
}
io.open(ROOT + r"\.c3-tmp\r691_verify.txt", "w", encoding="utf-8").write(
    "\n".join("%s %s" % (k, v) for k, v in checks.items()))
print("VERIFY", {k: v for k, v in checks.items()})
print("ALL_PASS" if all(checks.values()) else "HAS_FAIL")
