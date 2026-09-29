# -*- coding: utf-8 -*-
# R707 close: state.json (tick707 + log + ts/task + focus R708) + verify manually-edited ledgers.
# Ledger files (renders README/station-reviews/queue/status-export) were edited in-session via replace tool;
# this script does the authoritative JSON round-trip for state.json and verifies all six ledger faces.
import io
import json
from datetime import datetime

NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
STAMP = datetime.now().strftime("%H:%M")

LOG_R707 = (
    "2026-09-29 %s R707: 生产轮·LC-010 罗大壮拆条渲染腿毕（queue §E 批活池 E10 件·冗余扩容位第七件·R706 claim 兑现·"
    "R704 同型五步·实活轮·产品优先律 P-2026-09-29-07 对位=本轮新实物=lc-010 成片在链）"
    "——①轮首快速路径五查静（正典 r694_probe.py 复跑：orders 顶 O-20260928-1910 42 件锚未动/ledger 六模式 CaseSensitive 41=锚"
    "零新 CEO 令级事件〔L189/L190=R698/R700 已收讫+L245 值守行位移非事件〕/decisions UTF8 非空行 75=锚零新行"
    "/production=open 自愈核在位/无 index.lock·树态=bm-a codex 批未闭让位维持〔README+2/-1/city-humanities+12/-2 mtime 04:06 未动"
    "=#86 c+d 判据未达·两文件零接触〕+自产 tmp 族预期态）→可领活=R706 指针① 兑现；"
    "②渲染腿五步毕：素材探针先行=F-028 卡多模态九行全读（AIGC 标签位=卡面左上=F-027/F-031/F-032/F-035/F-036/F-038/F-040 同位族"
    "·R511 避让法前置执行零修红）→自产源件 data/sources/footage/census-card-v9-vertical.mp4（F-028 PNG 派生·scale 660+pad y=160"
    "+zoompan ≤1.04·13.000s·ffprobe 与 v20 参照逐参数一致 1080×1920@30）→对位表 cards-v1-matched.json 12/12 逐拍 visual"
    "（源卡即证据·钩子/信条行 verbatim 直引+锚 C-00018 字段展开同源多用注记·b9 咪喱互证拍〔C-00029 跨卡双源=LC-009 b4/b8 同本事双向闭合"
    "=拆条系列第三对人物链〕·visual-ratio 1.00·正位数据件入 git）→R-E shipinhao 渲染 lc-010-v1-shipinhao-60s.mp4"
    "（12 段 11 柔 0 硬切·**58.744s ffprobe 实测=音轨分毫一致·1.256s 余量**·hits=[0,11]·S5.5 角标=BigStream|拆条 010·源城市图鉴 009"
    "+§4.5 三开关·plan.json 入 git）；"
    "③S2 三门循环独立执法全绿=ai_feel 0 FAIL 0 WARN（gaps 11 处 0.239-0.558s·pacing CV 0.233·prosody 9 档 12 拍·copy CV 0.281）"
    "+层 1.8 六面 PASS（beat-align 11/11+camera 12 段全动+visual-ratio 1.00+transition-share 1.00 无连排+timeline 代数过）"
    "+spec 微信视频号双 PASS（9:16+58.74s ∈30-60s 窗 1.3s 余量·gate 舍入显示·实测 1.256s）；"
    "④帧验三律全过=拍头 12/12 语义全中（H1 拍名 12/12 逐拍对位+sys.beat 01→12 连续无跳号 t 单调递增+角标 12 帧全在+AIGC 帧头标识全在）"
    "+段中尾 6/6 稳定零录穿（law2=动态三最长拍 b4/b5/b9〔6.69/5.90/5.84s〕·**tile 缩略误读四族全分辨率定谳**"
    "=拆条≠系条〔R687 同型〕/罗大壮≠罗女士/《咪喱巷志》≠《咪喱专志》/「一刻钟」字幕带 2x 裁切净读=SRT 逐字零损"
    "·段中静态戳 sys.beat=05/06/10 t=00:16/00:23/00:44=§4.5 设计口径 R684 同判"
    "·段尾帧字幕缺席机核=cue_end 22.821 早于采样点 23.097=SRT 逐 cue 显隐律正常行为 R697 判例"
    "·段尾重影=11 柔转场 crossfade 窗正常合成像 R684/R687/R694/R700 同判）+回环 crossings={}（max 拍 6.69s<源 13s·诚实计算）"
    "+AIGC 双标识分层可读（帧头标识+卡面左上标签垂直错开零叠压·fs-pair-h04-h11 全分辨率实证·R511 避让法前置执行零修红）；"
    "⑤台账六件=renders README〔声明行渲染腿收口+lc-010 在链表行〕+station-reviews R707 S2 行+lc010 README 生产记录+门禁块"
    "+queue §E E10 渲染腿注+burn 行+status-export 刷（export_ts/live 三行/OS 循环行/results 707 行·JSON_OK 69 results）；"
    "⑥三探针（收账步复跑）=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面+1 发现"
    "（render-unannot lc-010=在链件诚实预期红·R680/R684/R687/R691/R694/R697/R700/R704 同型·F-064 登记即清·阻塞≠失败口径）"
    "/loop_health 3 FAIL+63 WARN 皆在案类（2 outage=09-26 49min+09-28 609min 同事件足迹已裁定不重复触发"
    "+account-lag done707>tick706=本轮在飞自然态 tick707 收账自平·63W 较 R706 新增=轮间隙 heartbeat-gap 合法 WARN 级）；"
    "⑦例行件：日报 09-29 在案不重跑（R637 断轮件补产）/W40 周审在案（R576）/月度注记在案（R-20260928-03）"
    "/global-benchmarks day5 ≤7 跳过（§④ 首行 09-24·下期 10-01=#80 并窗勿提前触碰）"
    "/T1 催办=已裁项停用口径/当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀·ledger/decisions 双锚静）"
    "/#70 OSS 窗 2=09-29 21:40 后已开（切片 1 已毕 R644=窗 1 义务足·窗 2 切片窗内随轮领）"
    "/#86 c+d 让位维持（bm-a codex 批未闭·两文件零接触）"
    "·tokens:local=0（渲染+三门+帧验=纯脚本+会话内建多模态零本地模型调用·P-54⑤ 计量律如实记）"
    "——下轮=R708 LC-010 收官腿（E8 终审七席+ASR 终轨〔R169 QC recipe medium-int8+beam5+noctx〕+E4 参考仪同轮回填→M4"
    "→F-064 登记→冗余池第七件落位→release-schedule v2.2→E10 出池+补池义务）；随轮可领=E3 REACT-v6 09-30 热点窗"
    "（P-1 试点终判件 2/2·当日日报先行核）+#70 OSS 窗 2 切片+#86 c+d 让位判据首查。收账显式列文件 commit+push"
) % STAMP

FOCUS_R708 = (
    "R708: ①LC-010 收官腿（E8 终审七席+ASR 终轨〔R169 QC recipe medium-int8+beam5+noctx·HF_HUB_OFFLINE=1 脱壳〕"
    "+E4 参考仪同轮回填→M4→F-064 登记→冗余池第七件落位→release-schedule v2.2→E10 出池+补池义务"
    "〔候选=BS-007 稿集件/续拆候选随选优轮评估·CENSUS 库 35 卡余量〕·R685/R688/R692/R695/R698/R701/R705 同型）；"
    "②E3 REACT-v6=09-30 热点窗届日领（P-1 试点终判件 2/2·当日日报先行核·daily_0930 届时补产）；"
    "③#70 OSS 窗 2 切片随轮领（21:40 后已开·≤10-02 21:40）+#86 c+d 让位判据首查（bm-a codex 批闭 commit 落地）"
    "——五查锚=orders 顶 O-20260928-1910·ledger 41（六模式 CaseSensitive=正典 r694_probe.py 口径）·decisions 75"
)


def main():
    # state.json authoritative round-trip
    sp = "src/os/state.json"
    s = json.load(io.open(sp, encoding="utf-8"))
    s["tick"] = 707
    s["log"].append(LOG_R707)
    s["ts"] = NOW
    body = LOG_R707.split("R707:", 1)[1].strip()
    s["task"] = body[:60]
    s["focus"] = FOCUS_R708
    io.open(sp, "w", encoding="utf-8", newline="\n").write(
        json.dumps(s, ensure_ascii=False, indent=1) + "\n")

    # verify all ledger faces
    v = json.load(io.open(sp, encoding="utf-8"))
    e = json.load(io.open("docs/status-export.json", encoding="utf-8"))
    rr = io.open("output/renders/README.md", encoding="utf-8").read()
    sr = io.open("docs/reviews/station-reviews.md", encoding="utf-8").read()
    qp = io.open("docs/self-improvement-queue.md", encoding="utf-8").read()
    lr = io.open("data/sources/lc010/README.md", encoding="utf-8").read()
    report = [
        "tick=%s" % v["tick"],
        "logN=%d" % len(v["log"]),
        "log_tail_R707=%s" % ("R707:" in v["log"][-1]),
        "task=%s" % v["task"][:40],
        "ts=%s" % v["ts"],
        "export_ts=%s" % e["export_ts"],
        "results_tail=%s" % e["results"][-1][0],
        "live1=%s" % ("渲染腿毕" in e["live"][0][0]),
        "rr_close=%s" % ("R707 渲染腿收口" in rr),
        "rr_row=%s" % ("lc-010-v1-shipinhao-60s.mp4" in rr),
        "sr_row=%s" % ("R707 渲染腿" in sr),
        "q_burn=%s" % ("E10 兑现中段·渲染腿毕（R707" in qp),
        "lc010_readme=%s" % ("R707 渲染腿毕" in lr),
        "plan_json=%s" % __import__("os").path.exists(
            "output/renders/lc-010-v1-shipinhao-60s.mp4.plan.json"),
    ]
    io.open(".c3-tmp/r707_close_verify.txt", "w", encoding="utf-8").write(
        "\n".join(report))
    print("CLOSE_OK " + " ".join(report[:8]))


if __name__ == "__main__":
    main()
