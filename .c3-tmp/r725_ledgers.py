# -*- coding: utf-8 -*-
# R725 ledger close: renders README (decl + in-chain row), station-reviews row,
# lc014 README (record + gate block), queue burn row, state.json, status-export.json
import json, io, re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
now = datetime.now()
stamp = now.strftime("%Y-%m-%d %H:%M:%S")
short = now.strftime("%H:%M")

# ---------- 1. renders README: LC-014 declaration + in-chain row ----------
rr = ROOT / "output" / "renders" / "README.md"
lines = rr.read_text(encoding="utf-8").splitlines()
decl = (u"> LC-014 L-卡拆条续投批中间件（queue §E 批活池 E14 件·冗余扩容位第十一件·**光机魂系首拆位=物种面扩展第四档**·"
        u"R722 断洞读腿→R723 起链〔S1 10/10 十三连满分〕→R724 空气预算四道裁链定稿 58.394s+TTS 定稿音轨"
        u"→**R725 渲染腿〔b4 几何前置修=R720 律预执行+全卡几何审计 problems=NONE〕**·收官腿=E8+ASR+E4+M4→F-069 随轮领）："
        u"批中间件 `.lc014-tmp/`（S1 门 1500s 脱壳包装件 s1_call.py+beats v1-v4 裁稿链+评审材料+TTS 分句段+间隙/呼吸件"
        u"+赛博链前后音轨+cards 基线+subs+probe-v10-mid 探针+帧验 tile 族+s2-results.md）——同性质非成品·不入本表")
# insert after the LC-013 declaration line
idx = None
for i, l in enumerate(lines):
    if l.startswith(u"> LC-013 L-卡拆条续投批中间件"):
        idx = i + 1
if idx is None:
    raise SystemExit("LC-013 declaration not found")
lines.insert(idx, decl)
rr.write_text("\n".join(lines) + "\n", encoding="utf-8")

row = (u"| lc-014-v1-shipinhao-60s.mp4 | **在链件（queue §E 批活池 E14 件·冗余扩容位第十一件·源卡=CENSUS-v10 F-029 老晶振·"
       u"R723 起链→R724 定稿音轨→R725 渲染腿毕：S2 三门+帧验三律+全卡几何审计 problems=NONE·收官腿=E8+ASR 终轨+E4+M4→F-069 登记"
       u"→冗余池第十一件落位 待随轮领）** | **R-E shipinhao 12 段 11 柔转场 0 硬切**（9:16 1080×1920·"
       u"**58.394s ffprobe 实测=音轨分毫一致·1.606s 余量**〔plan 内部预估 59.200s=tail 余量项·实测为准〕·hits=[0,11]·"
       u"**S5.5 角标常驻位**=BigStream\\|拆条 014·源城市图鉴 010+§4.5 三开关[glow/scanlines/sys.beat=NN t=MM:SS]·"
       u"plan.series+s45_dials 入 plan.json）·**拆条形态对位=源卡即证据 12/12**（census-card-v10-vertical 源卡画面×12·"
       u"visual-ratio 1.00·源件=F-029 PNG 派生 scale 660+pad y=160+zoompan ≤1.04·13.000s=LC-001~013 R511 法·"
       u"ffprobe 与 v15 参照逐参数一致·素材探针先行=卡面九行全读+AIGC 标签位=卡面左上=F-027/F-028/F-031/F-032/F-034/F-035/F-036/F-038/F-040 同位族）——"
       u"**b4 几何前置修（R720 律预执行·R711 五行块叠压前科防）**：b4 转折拍副题 55 字 4 事实 @60px 纯拆不可行"
       u"（最长行 16 em>15.33 预算）→「·」断点预拆 4 段 verbatim 零字符（build 脚本 zero-char 断言）+per-card size 46"
       u"（920/46=20.0 em 全行可过）=5 行 pitch 69.2 块顶 787 净距 20px=R720 修法地板——"
       u"**全卡几何审计（r725_card_audit wrap 级 12 卡全扫=R721 E8 帧验执法面常驻第二件）problems=NONE**"
       u"（b5/b6/b8 4 行块 788 净距 21px=LC-013 b8 先例同位·余 3 行块 831/874 全净）——"
       u"**S2 三门 R725 循环独立执法全绿**：ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.583s·pacing CV 0.309·"
       u"prosody 9 档 12 拍·copy CV 0.367）+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+"
       u"transition-share 1.00 无连排+timeline 代数过）+spec 微信视频号双 PASS（9:16+58.39s ∈30-60s 窗 1.6s 余量）——"
       u"**帧验三律全过**：拍头 12/12 语义全中（H1 拍名 12/12 逐拍对位+sys.beat 01→12 连续无跳号 t 单调递增+角标 12 帧全在+"
       u"AIGC 帧头标识全在）+段中尾 6/6 稳定零录穿（law2=动态三最长拍 b0/b4/b8〔5.98/8.28/6.27s〕·"
       u"**b4 修后块全分辨率实证=4 行副题逐行净读+来源行「基于硅基城市居民户籍卡档案（展示锚 C-00019）」完全可读零叠压**"
       u"〔fs-pair-h04-h11〕·段尾帧字幕缺席=SRT 逐 cue 显隐律正常行为 R697 判例+段尾重影=crossfade 窗正常合成像 R684/R687/R694/R700 同判）+"
       u"回环 crossings={}（max 拍 8.28s<源 13s·诚实计算）+AIGC 双标识分层可读（帧头标识+卡面左上标签垂直错开零叠压·fs-pair 全分辨率实证·"
       u"R511 避让法前置执行零修红）+tile 缩略疑点三族全分辨率定谳（「两小时城复活」净读〔tile「复话」误读〕/「睁眼」正字〔tile「静眼」误读〕"
       u"=R189 手段问题非画面问题律） | plan.json 入 git·收官腿随轮领（E8+ASR 终轨+E4+M4→F-069→冗余池第十一件→E14 出池） |")
with io.open(rr, "a", encoding="utf-8") as fh:
    fh.write(row + "\n")

# ---------- 2. station-reviews row ----------
sr = ROOT / "docs" / "reviews" / "station-reviews.md"
sr_row = (u"| 2026-09-30 | **S2 三门循环独立执法+帧验三律+全卡几何审计前置修零缺陷（lc-014-v1-shipinhao=queue §E 批活池 E14 件·"
          u"冗余扩容位第十一件·源卡 CENSUS-v10 F-029 老晶振·R725 渲染腿）** | lc-014-v1-shipinhao-60s.mp4"
          u"（R-E shipinhao 12 段·11 柔转场 0 硬切·58.394s=音轨分毫一致 1.606s 余量）+cards-v1-matched（b4 几何前置修件）"
          u"+r725_card_audit.txt | 循环独立执法（ai_feel+层 1.8+spec 微信视频号·纯脚本机检零 LLM）+帧验三律"
          u"（会话内建多模态+全分辨率 pair） | —（机检档·E8 终审待收官腿 R726） | "
          u"**b4 前置修=R720 律预执行**（R711 b9 五行块叠压前科→b4 转折拍副题 55 字 4 事实 @60px 纯拆不可行"
          u"〔最长行 16 em>15.33 预算〕→「·」断点预拆 4 段 verbatim 零字符+per-card size 46=5 行 pitch 69.2 块顶 787 净距 20px）"
          u"→**全卡几何审计 12 卡 problems=NONE**（b5/b6/b8 788 净距 21px=LC-013 b8 先例同位·"
          u"audit=R721 E8 帧验执法面常驻第二件）+S2 三门全绿（ai_feel 0F0W gaps 11 处 0.220-0.583s·pacing CV 0.309·"
          u"prosody 9 档·copy CV 0.367+层 1.8 六面 PASS visual-ratio 1.00 12/12+spec 双 PASS 9:16+58.39s 1.6s 余量）+"
          u"帧验三律全过（拍头 12/12〔H1 逐拍+sys.beat 01→12 连续+角标+AIGC 全帧〕+段中尾 6/6 零录穿"
          u"〔law2=b0/b4/b8 5.98/8.28/6.27s·b4 修后块 4 行副题逐行净读+来源行完全可读零叠压 fs-pair 全分辨率实证〕+"
          u"回环 crossings={}〔max 8.28s<源 13s〕+AIGC 双标识分层可读）+tile 缩略疑点三族全分辨率定谳"
          u"（城复活/睁眼=净读正字·R189 手段问题律） |")
with io.open(sr, "a", encoding="utf-8") as fh:
    fh.write(sr_row + "\n")

# ---------- 3. lc014 README: production record + gate block ----------
rd = ROOT / "data" / "sources" / "lc014" / "README.md"
raw = rd.read_text(encoding="utf-8")
rec = (u"\n- [2026-09-30 %s R725 渲染腿毕] 素材探针=F-029 卡多模态九行全读（AIGC 标签位=卡面左上=同位族·R511 避让法直接适用）"
       u"→自产源件 data/sources/footage/census-card-v10-vertical.mp4（F-029 PNG 派生·scale 660+pad y=160+zoompan ≤1.04·13.000s·"
       u"ffprobe 与 v15 参照逐参数一致）→对位表 cards-v1-matched.json 12/12 逐拍 visual（源卡即证据·锚 C-00019 字段展开同源多用注记·"
       u"b2 GAME 城拆条第四卡/b7 精灵系徒弟=LC-011 缪一同族位注记·visual-ratio 1.00·**b4 几何前置修=R720 律预执行**"
       u"〔55 字 4 事实 punch 拍 @60px 纯拆必 5 行块顶 745 叠压→「·」断点预拆 4 段 verbatim 零字符+per-card size 46"
       u"=块顶 787 净距 20px·全卡几何审计 problems=NONE 12 卡全净〕）→R-E shipinhao 渲染 lc-014-v1-shipinhao-60s.mp4"
       u"（12 段 11 柔 0 硬切·58.394s=音轨分毫一致 1.606s 余量·S5.5 角标=BigStream|拆条 014·源城市图鉴 010+§4.5 三开关）→"
       u"**S2 三门循环独立执法全绿**（ai_feel 0F0W gaps 11 处 0.220-0.583s·pacing CV 0.309+层 1.8 六面 PASS+spec 微信视频号双 PASS 1.6s 余量）→"
       u"**帧验三律全过**（拍头 12/12 语义全中+段中尾 6/6 零录穿〔law2=b0/b4/b8·b4 修后块全分辨率实证来源行零叠压〕+"
       u"回环 crossings={}〔max 8.28s<源 13s〕+AIGC 双标识分层可读+tile 疑点三族全分辨率定谳〔城复活/睁眼净读正字〕）。\n" % short)
# append record before the gate block, and update gate block
parts = raw.split(u"## 门禁块")
assert len(parts) == 2, "gate block split failed"
gate_new = (u"\n## 门禁块\n- S1=10/10 PASS（十三连满分）·M1 v4=0F0W·空气预算=v1 73.121s→v2 68.612s→v3 59.344s（薄）→"
            u"**v4 58.394s 定稿（1.606s 余量·fleet 带内）**·渲染腿=R725 毕（S2 三门全绿+帧验三律+全卡几何审计 problems=NONE·"
            u"b4 前置修 46px/4 段预拆净距 20px）。收官腿（E8+ASR 终轨+E4+M4→F-069 登记→冗余池第十一件落位）随轮领。"
            u"发布锁=M5 账号物理件不变（未上线=未测量）。\n")
rd.write_text(parts[0] + rec + gate_new, encoding="utf-8")

# ---------- 4. queue burn row ----------
q = ROOT / "docs" / "self-improvement-queue.md"
qrow = (u"- 2026-09-30: **E14 渲染腿毕（R725·R710 同型五步·b4 几何前置修=R720 律预执行零缺陷）**："
        u"素材探针 F-029 九行全读（AIGC 标签=卡面左上同位族）→census-card-v10-vertical 派生（13.000s 与 v15 参照逐参数一致）"
        u"→对位表 12/12 visual-ratio 1.00→R-E shipinhao 渲染 lc-014-v1-shipinhao-60s.mp4（58.394s=音轨分毫一致 1.606s 余量·hits=[0,11]）"
        u"→S2 三门全绿（ai_feel 0F0W+层 1.8 六面+spec 双 PASS）+帧验三律全过（拍头 12/12+段中尾 6/6+回环 crossings={}"
        u"+AIGC 双标识）+**全卡几何审计 problems=NONE**（b4=55 字 4 事实 punch 拍 @60px 必叠压→46px+4 段预拆 verbatim 零字符块顶 787 净距 20px）"
        u"——收官腿（E8+ASR 终轨+E4+M4→F-069→冗余池第十一件→E14 出池）=下轮首位。\n")
with io.open(q, "a", encoding="utf-8") as fh:
    fh.write(qrow)

print("LEDGERS OK: renders decl+row, sr row, lc014 readme, queue burn")
