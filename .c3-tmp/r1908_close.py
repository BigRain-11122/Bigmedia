# -*- coding: utf-8 -*-
"""R1908 close: state tick+log, export refresh via tech#70 writer (P-6 round 2/3),
tech#74 progress note, embedded close_commit (tech#65/67 law)."""
import io
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATE = os.path.join(ROOT, "src", "os", "state.json")
TECHQ = os.path.join(ROOT, "state", "queue", "tech.md")

import datetime
now = datetime.datetime.now()
ts = now.strftime("%Y-%m-%d %H:%M:%S")

LOG_BODY = (
    "等待轮·tech#74 P-6 大白话试点第 2/3 轮收账面执行（O-20261009-1246 取活·两段制收账=close_commit 末步内嵌·"
    "waiting=GPU VRAM 他 lane 合法满载〔ETA=VRAM 释放即四腿点火〕+#112 城市口径判据窗〔ETA 2026-10-11 08:00〕）——"
    "①轮首五查全静=own orders 顶 O-20261008-1105 mtime 12:08:14==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）"
    "+group_scan 固定探针三面静（decisions dnum 内容寻址差集 truly_new=0 水位 131 维持+ledger @BigStream 4 行==值守锚零新转办"
    "+HQ orders 20:15:33==R1907 消费锚零新行）+无 index.lock+树态=mv0001/mv001/whisper v3/drama_takt bm-a MV sprint 会话批域在飞件零接触（R1745 承继）；"
    "②GPU 窗 C-37 fresh 判读=NO-GO（pause_face clear 8/8=O-2006 算力解禁态·vram_face free 418MB<9216 守卫=他 lane 合法并行满载）"
    "+ollama 探针 --ledger=rc2 TimeoutError face=busy-contended gpu_util 97%（满载窗让路面判读不升级·face 框架 tech#55 正用）"
    "→四腿（MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 v13）维持 fire-ready gated（材料 R1870/R1871/R1875 turnkey）；"
    "③查看位双路径并读（R1762 律）=meme outbound 零新到件（止于 15:41 narration.mp3==R1899 锚·V1 成片 mp4 未到=TTS/装配腿在飞维持）"
    "+krea2 30s-reel-v1 零新到件（止于 20:03:42 DELIVERY-NOTE-v44==R1907 锚）禁重扫；"
    "④三队盘点=main 全 gated/查看位（#111 零接触跟踪位·#112 判据窗 10-11 08:00 届日即领·#115 meme 成片随轮盯）"
    "+tech 全 done/gated（#74 试点本轮第 2/3 轮收账面执行·#53 到点 10-11·#59/#63/#42 各窗）"
    "+explore 全 done/gated/到点未到（#14/#22/#24=10-17 窗·#18=10-16/11-09·#19=GPU 窗）"
    "→等待窗内无独立可领项=tech#74 收账面并窗执行即本轮流活；"
    "⑤tech#74 P-6 试点第 2 轮=export live 三行大白话维持（export_refresh 正典写入器 live-clock·三行零内部代号复发自检过=判据①第 2/3 轮·三要素齐=判据③·观察窗 ≤10-24·第 3 轮 R1909 收账面后收口判断）；"
    "⑥三探针=probe_capture 证据件 .c3-tmp/r1908_probes.txt（board 0 FAIL〔5 题 10 稿·5 in production〕"
    "/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17 needs-CEO〕0 发现〔78 renders 全注账 unannot=0〕"
    "/loop_health 2F+史实带内〔两 outage=09-26/09-28 已裁定不重触发·drift 17==adjudicated 基线带内〕）；"
    "⑦例行件=10-10 日报在案不重跑（R1845 00:03 一份为真相）·W41 周审在案 W42 件 10-12 未到·GB §④ v1.3 下期 10-15 跳过"
    "·#99 blocked-on-channel 维持（SLA ≤10-13）·15:07 盘燃已点名毕不重扫·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）"
    "·tokens:local=0（纯探针+只读读数+工程收账零本地模型产出调用·P-54⑤ 计量律）；"
    "⑧队列补货步=真无新种子如实注记零膨胀（本轮五查全静零真发现·禁凑数律）"
    "+临时件=r1908 探针证据件+close 脚本+ollama-probe-ledger 本轮行入账收口（tech#64 律）"
    "——下轮=R1909 快速路径首查（10-11 08:00 #112 判据窗届日即领〔≥60 ≥2 件+tech#53 双新源首报〕+GPU C-37 fresh 四腿判断+meme V1 成片查看位+P-6 第 3 轮收账面收口）"
)
LOG = "%s R1908: %s" % (ts, LOG_BODY)

# --- 1) state.json: format round-trip guard, then tick/log/ts/task ---
with io.open(STATE, "r", encoding="utf-8") as fh:
    raw = fh.read()
st = json.loads(raw)
dumped = json.dumps(st, ensure_ascii=False, indent=1) + "\n"
if dumped != raw:
    print("WARN state.json format drift on round-trip (diff %d bytes); continuing with canonical dump"
          % abs(len(dumped) - len(raw)))
st["tick"] = 1908
st["log"].append(LOG)
st["ts"] = ts
st["task"] = LOG_BODY[:60]
with io.open(STATE, "w", encoding="utf-8", newline="") as fh:
    json.dump(st, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("state: tick=1908 log_len=%d ts=%s" % (len(st["log"]), ts))

# --- 2) export refresh via tech#70 canonical writer (P-6 round 2) ---
sys.path.insert(0, os.path.join(ROOT, "src", "os"))
import export_refresh

patch = {
    "do": ("AI 媒体公司自迭代循环：显卡被其他产线占满，配音和评审排队等空档；"
           "明早 8 点验收第一份全城市热点日报；30 秒 MV 变速新版今晚交片"),
    "live": [
        "当前：等明早 8 点验收第一份全城市热点日报；显卡被其他产线占用，配音和评审排队中",
        "最近实物：30 秒《爱在西元前》改编 MV（逐镜变速新版），今晚 20:01 交片",
        "下个里程碑：明早 8 点，第一份全城市热点日报验收出结果，看城市消息能不能进榜",
    ],
}
EXPORT = os.path.join(ROOT, "docs", "status-export.json")
rc, lines, viol = export_refresh.refresh_export(EXPORT, patch=patch)
for ln in lines:
    print(ln)
print("export_refresh rc=%d violations=%d" % (rc, len(viol)))
if rc != 0:
    print("FATAL: export writer refused; aborting close")
    sys.exit(rc)

# --- 3) tech.md tech#74 progress note (assert count==1 anchor) ---
ANCHOR = "——按认领制随轮领做（收账面并窗执行·零独立工时）"
NOTE = (" ——[R1908 第 2/3 轮 2026-10-10]：收账面并窗执行毕（live 三行大白话零内部代号复发"
        "·export_refresh 正典写入器 live-clock·判据①②③本轮自检过·第 3 轮=R1909 收账面后收口判断）")
with io.open(TECHQ, "r", encoding="utf-8") as fh:
    tq = fh.read()
cnt = tq.count(ANCHOR)
if cnt != 1:
    print("FATAL: tech#74 anchor count=%d (expect 1); aborting tech.md edit" % cnt)
    sys.exit(2)
with io.open(TECHQ, "w", encoding="utf-8", newline="") as fh:
    fh.write(tq.replace(ANCHOR, ANCHOR + NOTE, 1))
print("tech.md: tech#74 R1908 note appended")

# --- 4) embedded close commit (tech#65) ---
import close_commit
FILES = [
    "src/os/state.json",
    "docs/status-export.json",
    "state/queue/tech.md",
    "data/pipeline/ollama-probe-ledger.jsonl",
    ".c3-tmp/r1908_probes.txt",
    ".c3-tmp/r1908_close.py",
]
MSG = ("R1908 waiting round: five-checks quiet (origin QUIET, decisions truly_new=0 wm131, "
       "ledger==anchor, HQ orders==R1907 anchor); GPU window C-37 NO-GO (pause clear, vram 418MB "
       "other-lane load), four legs fire-ready; meme/krea2 viewpoints zero new arrivals; #112 gate "
       "due 10-11 08:00; tech#74 P-6 plain-language pilot round 2/3 via canonical export writer "
       "[via bm-a]")
rc, lines = close_commit.run_close_commit(FILES, MSG, root=ROOT)
for ln in lines:
    print(ln)
print("close_commit rc=%d" % rc)
sys.exit(rc)
