# R1951 close: active round - W3 sweep knives 1-3 (explore#24), two-stage accounting
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, "src/os")

DELIVERABLES = [
    "docs/research/R-20260927-bigstream-04-aigc-labeling-recsys-weekly-scan.md",
    "state/queue/tech.md",
    "state/queue/explore.md",
    ".c3-tmp/r1951_pg57A_fulltext.txt",
    ".c3-tmp/r1951_tc260_links.txt",
]

STAGE1_MSG = (
    "R1951 W3 sweep knives 1-3 (explore#24): TC260-PG-20257A video implicit-labeling "
    "practice guide fulltext direct-captured from tc260.org.cn (19pp pypdf extract + "
    "6-guide official PDF URL set + 7-field JSON / MP4 moov.udta.meta / ffmpeg -metadata "
    "AIGC -movflags use_metadata_tags one-liner = tech#42 input unlocked, gate narrowed "
    "to M5 publish window only); knife2 weixin110 reachable-but-JS-shell re-confirmed; "
    "knife3 bilibili help unreachable re-confirmed + creator-declaration feature "
    "2025-09-20 secondary readings (B-level, no upgrade); knife4 deferred to next window; "
    "R-20260927-04 v1.2 + tech#42 gate note + explore#24 progress note [via bm-a]"
)

LOG = (
    "2026-10-11 07:5x R1951: 等待窗取活轮·explore#24 W3 周扫刀①②③ 交付（08:00 #112 判据窗前 P3 队头可领项·"
    "O-20261009-1246 项 c+两段制收账 tech#27）——"
    "①轮首五查全静=own orders 顶 O-20260908-1105 mtime==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0"
    "（R1500 前置位）+group_scan（tech#50 正典）truly_new=0 水位 137 维持+wm_only=1（C-20261010-01 行内引用族）"
    "+ledger @BigStream 4 行==值守锚零新转办+HQ orders 02:06:39==R1935 消费锚零新行+无 index.lock"
    "+树态=MV sprint 会话域在飞件零接触（R1745 承继·tech#26 撞面维持）；"
    "②P2 队盘点=tech 队全 done/gated（#5/#30/#49/#53=08:00 判据位同窗·#1/#3/#9/#18 GPU 独占窗·#24 W42·"
    "#29 CEO 点头·#40/#59 owner·#43/#47 GPU 释放窗·#48/#27 定版窗·#14/#15/#17/#38/#39/#63 各 gated 维持）"
    "→P3 explore 队头可领=explore#24（10-17 到点窗内）→认领执行："
    "**刀① A 级正身直采=TC260-PG-20257A《AI 生成合成内容标识方法 文件元数据隐式标识 视频文件》V1.0-202508 "
    "19 页全文**（tc260.org.cn 正身 PDF curl 直采+pypdf 文本层提取入档 .c3-tmp/r1951_pg57A_fulltext.txt·"
    "六件 118 号正身 PDF URL 全集定谳入册 57A 视频/58A 文本/59A 图片/510A 音频/511A 安全防护/512A 检测框架"
    "〔名单页 list_2.shtml 锚提取 r1951_tc260_links.txt〕）——**字段级参数=tech#42 技术输入解锁**：七字段 JSON"
    "（Label/ContentProducer/ProduceID/ReservedCode1/ContentPropagator/PropagateID/ReservedCode2=GB 45438 "
    "附录 E 字符串正身）+MP4/MOV 原生嵌入位 moov.udta.meta（keys key=AIGC+ilst value）+ffmpeg 一行式 "
    "-metadata AIGC=... -movflags use_metadata_tags -c copy（读回 ffmpeg -i）+FLV/MKV/AVI/XMP TC260 命名空间"
    "（URI tc260.org.cn/ns/AIGC/1.0）全录——本司 render/export 链 mp4 唯一输出档=原生嵌入方案适用正身；"
    "刀② weixin110.qq.com 可达但零静态内容（JS 壳墙·W1 判读续证·卡点如实）；刀③ help.bilibili.com 连接失败"
    "续证+换刀二手双读数（B 级转载禁升格：B站投稿侧 AI 标识选项 2025-09-01 公告转载+创作者声明功能 "
    "2025-09-20 上线=M5 发布侧声明开关平台标配再证·B站位入 checklist 位）；刀④ CAC 盯位+D 级传闻复查未竟"
    "（≤10-17 窗内余裕·explore#24 余位承载维持开板）——全录 R-20260927-04 §10 v1.2（§十 W3+§十一 应用表五行+变更行）；"
    "③台账回写=tech#42 gate 收窄（W3 刀① 前置已毕→gated M5 发布批窗单前置·判据参数正身入行）+explore#24 "
    "进展注（刀①②③ 毕·刀④ 余位下窗领·item 维持开板）——发布面零动作维持（义务主体=平台非发布用户·自愿增强位）；"
    "④三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE "
    "6/10+#17 needs-CEO）0 发现（78 renders 全注账 unannot=0）/loop_health 2F+240W 皆在案史实（两 outage "
    "09-26/09-28 已裁定不重触发·account-uncommitted WARN=本轮收账 commit 即解）；"
    "⑤例行件=10-11 日报在案不重跑（R1927 一份为真相）·W42 周审 10-12 未到·GB §④ v1.3 下期 10-15 跳过"
    "·#112 城市口径判据窗 08:00 届日即领（07:33 首查 ~27min·tech#53 双新源流量首报+tech#5/#30/#49 判定位同窗）"
    "·meme V1 成片未落=装配腿在飞维持零接触·export 本轮刷新（live 三行大白话 tech#74 常设·live-clock 正典写入器）"
    "·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0（W3 扫=web 定向直查+curl/pypdf 纯 CPU "
    "零本地模型调用·P-54⑤ 计量律）；"
    "⑥队列补货步=真无独立新种子如实注记零膨胀（tech#42 前置更新+explore#24 余位=既有行回写非新增·五查静+探针零新发现"
    "·禁凑数律）·临时件=3 份正身 PDF 二进制+HTML+探针转储轮末删净（提取文本+URL 集两证据件入 git·PDF 可按入册 URL "
    "复采）——下轮=R1952 首读（08:00 #112 城市口径判据窗届日即领〔城市源非回填 ≥60 ≥2 件+tech#53 双新源流量与通过率"
    "首报+tech#5/#30/#49 判定位〕+fire 卡剧本腿判断+meme V1 成片查看位+explore#24 刀④ 随窗）。"
)

FOCUS = (
    "R1952 首读 08:00 #112 城市口径判据窗（城市源非回填 ≥60 ≥2 件+tech#53 首报+tech#5/#30/#49 判定位）"
    "+fire 卡剧本腿判断+meme V1 成片查看位+explore#24 刀④ 随窗"
)


def main():
    from close_commit import run_close_commit, finalize_state

    # Stage 1: deliverables-first commit (tech#27 two-stage law)
    rc, lines = run_close_commit(files=DELIVERABLES, message=STAGE1_MSG)
    for l in lines:
        print(l)
    print("STAGE1_RC", rc)
    if rc not in (0,):
        print("stage1 rc=%d - inspect before proceeding" % rc)

    # Export refresh (canonical writer, live-clock, plain-language live lines)
    os.system('python src/os/export_refresh.py --patch .c3-tmp/r1951_export_patch.json')

    # Stage 2: state accounting (single writer law tech#76)
    summary = finalize_state(log_line=LOG, focus=FOCUS)
    for k in ("tick", "ts", "task", "wm_added", "log_len"):
        print(k, "=", summary.get(k))

    rc2, lines2 = run_close_commit(
        files=[
            "src/os/state.json",
            "docs/status-export.json",
            ".c3-tmp/r1950_close.py",
            ".c3-tmp/r1950_fire_card.txt",
            ".c3-tmp/r1950_probes.txt",
        ],
        message=(
            "R1951 accounting close: tick 1951, W3 knives 1-3 delivered (see stage-1 commit), "
            "export live-face refreshed; R1950 statement-window artifacts absorbed (active round "
            "closes the window, os-protocol S6); next R1952 collects 08:00 radar city-criteria window [via bm-a]"
        ),
    )
    for l in lines2:
        print(l)
    print("STAGE2_RC", rc2)


if __name__ == "__main__":
    main()
