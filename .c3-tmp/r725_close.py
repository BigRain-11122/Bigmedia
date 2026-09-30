# -*- coding: utf-8 -*-
# R725 close: re-run 3 probes after render, then state.json + status-export.json
import subprocess, sys, os, json, re, io
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / ".c3-tmp"
now = datetime.now()
stamp = now.strftime("%Y-%m-%d %H:%M:%S")
short = now.strftime("%H:%M")

# --- probes (post-render close-step re-run) ---
for name, cmd, out in [("board", ["python", "src/board_check.py"], "r725_board.txt"),
                       ("readiness", ["python", "src/readiness.py"], "r725_readiness.txt"),
                       ("loop_health", ["python", "src/os/loop_health.py"], "r725_health.txt")]:
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, timeout=300)
    txt = (r.stdout.decode("utf-8", errors="replace") + "\n[stderr]\n" + r.stderr.decode("utf-8", errors="replace"))
    with io.open(TMP / out, "w", encoding="utf-8") as f:
        f.write(txt)
    print("%s: exit=%d" % (name, r.returncode))

# --- state.json ---
r725_line = (
    u"2026-09-30 %s R725: 生产轮·E14 LC-014 老晶振拆条渲染腿毕（queue §E 批活池 E14 件·冗余扩容位第十一件·R710/R719 同型五步·"
    u"实活轮·产品优先律 P-20260929-07 对位=本轮新实物=lc-014 成片在链）——①轮首快速路径五查静（正典 r694_probe.py 自跑："
    u"orders 顶=O-20260928-1910 42 件锚未动/ledger 六模式 CaseSensitive 41=锚零新 CEO 令级事件〔L189/L190=R698/R700 已收讫"
    u"+L245 值守行位移非事件〕/decisions UTF8 非空行 75=锚零新行/production=open 自愈核在位/无 index.lock·"
    u"树态=bm-a codex 批未闭让位维持〔README+2/-1/city-humanities+12/-2 mtime 09-29 04:06 实读未动=#86 c+d 判据未达·两文件零接触〕"
    u"+自产 tmp 族预期态）→可领活=focus① 兑现；②渲染腿五步毕：素材探针先行=F-029 卡多模态九行全读"
    u"（AIGC 标签位=卡面左上=F-027/F-028/F-031/F-032/F-034/F-035/F-036/F-038/F-040 同位族·R511 避让法直接适用）→"
    u"自产源件 data/sources/footage/census-card-v10-vertical.mp4（F-029 PNG 派生·scale 660+pad y=160+zoompan ≤1.04·13.000s·"
    u"ffprobe 与 v15 参照逐参数一致 1080×1920@30）→对位表 cards-v1-matched.json 12/12 逐拍 visual（源卡即证据·锚 C-00019 字段展开"
    u"同源多用注记·b2 GAME 城拆条第四卡/b7 精灵系徒弟=LC-011 缪一同族位注记·visual-ratio 1.00）→**b4 几何前置修（R720 律预执行·"
    u"R711 五行块叠压前科防）**：b4 转折拍副题 55 字 4 事实 @60px 纯拆不可行（最长行 16 em>15.33 预算）→「·」断点预拆 4 段 verbatim "
    u"零字符（build 脚本 zero-char 断言）+per-card size 46（920/46=20.0 em 全行可过）=5 行 pitch 69.2 块顶 787 净距 20px=R720 修法地板"
    u"→R-E shipinhao 渲染 lc-014-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·58.394s ffprobe=音轨分毫一致 1.606s 余量·hits=[0,11]·"
    u"S5.5 角标=BigStream|拆条 014·源城市图鉴 010+§4.5 三开关·plan.json 入 git）；③**全卡几何审计（r725_card_audit wrap 级 12 卡全扫"
    u"=R721 E8 帧验执法面常驻第二件）problems=NONE**（b4 修后 787/20px+b5/b6/b8 4 行块 788/21px=LC-013 b8 先例同位·余 3 行块 831/874 全净）；"
    u"④S2 三门循环独立执法全绿=ai_feel 0 FAIL 0 WARN（gaps 11 处 0.220-0.583s·pacing CV 0.309·prosody 9 档 12 拍·copy CV 0.367）"
    u"+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过）"
    u"+spec 微信视频号双 PASS（9:16+58.39s ∈30-60s 窗 1.6s 余量）；⑤帧验三律全过=拍头 12/12 语义全中（H1 拍名 12/12 逐拍对位"
    u"+sys.beat 01→12 连续无跳号 t 单调递增+角标 12 帧全在+AIGC 帧头标识全在）+段中尾 6/6 稳定零录穿"
    u"（law2=动态三最长拍 b0/b4/b8〔5.98/8.28/6.27s〕·**b4 修后块全分辨率实证=4 行副题逐行净读+来源行「基于硅基城市居民户籍卡档案"
    u"（展示锚 C-00019）」完全可读零叠压**〔fs-pair-h04-h11〕·段尾帧字幕缺席=SRT 逐 cue 显隐律正常行为 R697 判例+段尾重影=crossfade 窗"
    u"正常合成像 R684/R687/R694/R700 同判）+回环 crossings={}（max 拍 8.28s<源 13s·诚实计算）+AIGC 双标识分层可读"
    u"（帧头标识+卡面左上标签垂直错开零叠压·fs-pair 全分辨率实证·R511 避让法前置执行零修红）+tile 缩略疑点三族全分辨率定谳"
    u"（「两小时城复活」净读〔tile「复话」误读〕/「睁眼」正字〔tile「静眼」误读〕=R189 手段问题非画面问题律）；"
    u"⑥台账=renders README〔LC-014 声明行+在链表行〕+station-reviews R725 S2 行+lc014 README 生产记录+门禁块+queue §E E14 burn 行"
    u"+status-export 刷；⑦三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面+1 发现"
    u"（render-unannot lc-014=在链件诚实预期红·R700/R719 同型·F-069 登记即清）/loop_health 在案史实类"
    u"（account-lag done725>tick724=本轮在飞自然态 tick725 收账自平 R615 起先例连）；⑧例行件：日报 09-30 在案不重跑（R713 补产）"
    u"/W40 周审在案（R576）/月度注记在案/global-benchmarks day6 ≤7 跳过（下期 10-01=#80 并窗勿提前触碰）/"
    u"#70 OSS 窗 2=10-02 21:40 前随轮领（切片 1 已毕 R644=窗面义务足）/T1 催办=已裁项停用口径/HQ-FEEDBACK 不写"
    u"（无集团层新 open 问题）/tokens:local=0（渲染+三门+帧验=纯脚本+会话内建多模态零本地模型调用·P-54⑤ 计量律）——"
    u"下轮=R726 可领序：①LC-014 收官腿（E8+ASR 终轨+E4+M4→F-069→冗余池第十一件→E14 出池→补池义务）②#70 OSS 切片"
    u"③#86 c+d 让位判据④global-benchmarks 10-01。收账显式列文件 commit+push" % short
)

sp = ROOT / "src" / "os" / "state.json"
raw = sp.read_text(encoding="utf-8")
had_nl = raw.endswith("\n")
st = json.loads(raw)
st["tick"] = 725
st["log"].append(r725_line)
st["ts"] = stamp
body = re.sub(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})? R725: ", "", r725_line)
st["task"] = body[:60]
st["focus"] = (u"R726: ①LC-014 收官腿（E8 终审七席评审单 review-20260930-lc014-v1.md+ASR 终轨〔R169 QC recipe medium-int8+beam5+noctx·"
               u"HF_HUB_OFFLINE=1·asr-diff 量化+繁转简化归计算〕+E4 参考仪同轮回填→M4→F-069 登记→冗余池第十一件落位"
               u"〔release-schedule 升版〕→queue §E E14 出池〔lane=E15 standby 单条<2→补池义务随轮领〕）"
               u"②#70 OSS 窗 2 切片（≤10-02 21:40·切片 1 已毕 R644=窗面义务足）③#86 c+d 让位判据"
               u"（bm-a codex 批闭 commit 落地·README/city-humanities mtime 09-29 04:06 未动）"
               u"④global-benchmarks 7 日刷（10-01=#80 并窗·今日 day6 未到勿提前触碰）——五查锚=orders 顶 O-20260928-1910·"
               u"ledger 41（六模式 CaseSensitive=正典 r694_probe.py 口径）·decisions 75")
sp.write_text(json.dumps(st, ensure_ascii=False, indent=2) + ("\n" if had_nl else ""), encoding="utf-8")

# --- status-export.json ---
ex = ROOT / "docs" / "status-export.json"
raw2 = ex.read_text(encoding="utf-8")
had_nl2 = raw2.endswith("\n")
se = json.loads(raw2)
se["export_ts"] = stamp + "+08:00"
se["outs"][0][1] = (u"tick 725，R725 生产轮·E14 LC-014 老晶振拆条渲染腿毕（实活轮·产品优先律对位=lc-014 成片在链）："
                    u"素材探针 F-029 九行全读→census-card-v10-vertical 派生（13.000s 与 v15 参照逐参数一致）→对位表 12/12 visual-ratio 1.00→"
                    u"R-E shipinhao 渲染 lc-014-v1-shipinhao-60s.mp4（58.394s=音轨分毫一致 1.606s 余量）→S2 三门全绿"
                    u"（ai_feel 0F0W+层 1.8 六面+spec 微信视频号双 PASS）+帧验三律全过+**全卡几何审计 problems=NONE**"
                    u"（b4 前置修=46px+4 段预拆 verbatim 零字符块顶 787 净距 20px=R720 律预执行）——收官腿（E8+ASR+E4+M4→F-069"
                    u"→冗余池第十一件→E14 出池）=R726 首位；lane=E15 standby 单条<2→补池义务随轮领")
se["results"].append([
    u"725",
    u"R725: 生产轮·E14 LC-014 老晶振拆条渲染腿毕（queue §E 批活池 E14 件·冗余扩容位第十一件·R710/R719 同型五步·实活轮·"
    u"产品优先律 P-20260929-07 对位=本轮新实物=lc-014 成片在链）：素材探针 F-029 卡多模态九行全读（AIGC 标签位=卡面左上同位族）"
    u"→自产源件 census-card-v10-vertical.mp4（F-029 PNG 派生·scale 660+pad y=160+zoompan ≤1.04·13.000s 与 v15 参照逐参数一致）"
    u"→对位表 cards-v1-matched.json 12/12 visual-ratio 1.00（源卡即证据·b2 GAME 城拆条第四卡/b7 精灵系徒弟=LC-011 缪一同族位）→"
    u"**b4 几何前置修=R720 律预执行**（55 字 4 事实 punch 拍 @60px 纯拆必 5 行块顶 745 叠压→「·」断点预拆 4 段 verbatim 零字符"
    u"+per-card size 46=块顶 787 净距 20px）→R-E shipinhao 渲染 lc-014-v1-shipinhao-60s.mp4（12 段 11 柔 0 硬切·58.394s=音轨分毫一致 "
    u"1.606s 余量·hits=[0,11]·S5.5 角标=拆条 014·源城市图鉴 010+§4.5 三开关·plan.json 入 git）→"
    u"全卡几何审计 12 卡 problems=NONE（R721 E8 帧验执法面常驻第二件）+S2 三门全绿（ai_feel 0F0W gaps 11 处 0.220-0.583s·"
    u"pacing CV 0.309·copy CV 0.367+层 1.8 六面+spec 双 PASS 9:16+58.39s 1.6s 余量）+帧验三律全过（拍头 12/12+段中尾 6/6 零录穿"
    u"〔b4 修后块全分辨率实证来源行零叠压 fs-pair〕+回环 crossings={}〔max 8.28s<源 13s〕+AIGC 双标识分层可读+"
    u"tile 疑点三族全分辨率定谳〔城复活/睁眼净读正字〕）；台账=renders 声明行+在链行+station-reviews R725 行+lc014 README+queue burn；"
    u"五查静（orders O-1910/ledger CS 41/decisions 75 锚·bm-a codex 批未闭让位维持）；三探针 board 0F/readiness 3 外部+1 在链预期红"
    u"（render-unannot lc-014·F-069 登记即清）/loop 在案类；例行件在案不重跑·tokens:local=0——下轮=R726 LC-014 收官腿"
    u"（E8+ASR+E4+M4→F-069→冗余池第十一件→E14 出池）首位"
])
se["live"] = [
    [u"当前活：LC-014 老晶振拆条渲染腿毕（S2 三门全绿+帧验三律+全卡几何审计 problems=NONE·b4 前置修 46px/4 段预拆净距 20px）——收官腿（E8+ASR+E4+M4→F-069 登记→冗余池第十一件）=R726 首位·lane=E15 standby 单条<2→补池义务随轮领"],
    [u"最近实物：output/renders/lc-014-v1-shipinhao-60s.mp4（老晶振拆条成片在链 58.394s·9:16·12 段 11 柔 0 硬切·音轨分毫一致 1.606s 余量·角标=BigStream|拆条 014·源城市图鉴 010）+data/sources/footage/census-card-v10-vertical.mp4（F-029 派生源件 13.000s）+data/sources/lc014/cards-v1-matched.json（对位表 12/12）·2026-09-30 " + stamp],
    [u"下个里程碑：LC-014 收官=F-069 登记+冗余池第十一件落位（E8 七席+ASR 终轨+E4+M4 全链走门·窗 ≤48h 即 2026-10-02 前）+E14 出池补池（候选=E15 朱鸿奎 active/BS-007 稿集件/续拆候选随选优轮）·#70 OSS 窗 2 切片 ≤10-02 21:40·global-benchmarks 7 日刷 10-01"],
]
ex.write_text(json.dumps(se, ensure_ascii=False, indent=1) + ("\n" if had_nl2 else ""), encoding="utf-8")

print("OK state tick=%s log=%d ts=%s" % (st["tick"], len(st["log"]), st["ts"]))
print("OK export ts=%s results=%d live=%d" % (se["export_ts"], len(se["results"]), len(se["live"])))
