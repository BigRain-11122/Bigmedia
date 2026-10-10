# -*- coding: utf-8 -*-
# r1927_close.py -- two-segment accounting close for round R1927 (waiting-
# window executable round: tech#76 deliverable + C-20261010-04/new-order
# consumption + tech#75 formal dual-gate NO-GO held). Pure-ASCII console
# output (encoding law); the state log line is an in-script UTF-8 string
# literal passed verbatim to close_commit.finalize_state() -- the tech#76
# single-writer dogfood (no external template, no placeholder substitution).
# Steps: purge scratch -> deliverables commit (segment 1) -> finalize_state
# (accounting) -> export refresh via canonical writer -> accounting commit
# (segment 2).

import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "src", "os"))

import close_commit as cc  # noqa: E402

SCRATCH = [
    ".c3-tmp/r1927_tech.txt", ".c3-tmp/r1927_tech2.txt",
    ".c3-tmp/r1927_cap.txt", ".c3-tmp/r1927_c39.txt",
    ".c3-tmp/r1927_captail.txt", ".c3-tmp/r1927_t76mod.log",
    ".c3-tmp/r1927_export_cur.txt", ".c3-tmp/r1927_export_patch.json",
    ".c3-tmp/bs-test-suite-r1927.log", ".c3-tmp/bs-test-suite-r1927.log.out",
    ".c3-tmp/bs-test-suite-r1927.log.err",
]

DELIV = [
    "src/os/close_commit.py",
    "tests/test_close_commit.py",
    "docs/capabilities.md",
    "state/queue/tech.md",
    "data/intel/daily/2026-10-11.md",
    ".c3-tmp/r1927_probes.txt",
    ".c3-tmp/r1927_hq_orders.txt",
    ".c3-tmp/r1927_c04.txt",
    ".c3-tmp/r1927_bill.txt",
    ".c3-tmp/bs-test-suite-r1927.log.result",
]

MSG1 = (
    "R1927 deliver: tech#76 finalize_state() single-writer state accounting "
    "(R1920 placeholder-anchor root fix: inline-literal log API with zero "
    "substitution steps, prefix regex born-gate, task 60-char single impl, "
    "tick double-run guard, injected-clock ts, watermark add, atomic write); "
    "+11 tests, suite 800 green rc=0; capabilities v1.80 (C-39 ext); tech#76 "
    "done + tech#77 seed (probe-gate order contamination, this round find); "
    "C-20261010-04 + four new HQ order rows consumed (no BigStream "
    "dispatch); daily brief 10-11 [via bm-a]"
)

LOG_LINE = (
    "2026-10-11 00:2x R1927: 等待窗取活轮·tech#76 交付（O-20261009-1246 取活判走执行·五查破静=新决策+新令→全任务书照走）——"
    "①破静消费集=C-20261010-04 子公司活跃度监督案收讫（HQ orders O-20261010-2350·委员会同窗 7/7 收口·BigStream 实查=活跃〔144 提交/24h〕非点名对象·首轮派单=BigHouse E1+BigCompute·本司零派单=知悉+水位收账+活跃度下限律合规面自证〔本轮真进展件在案〕）"
    "+HQ orders 另三新行知悉零本司份额（00:0x 硅基城直推令=FluxVerse 域/23:5x 2D 截图走查法=游戏产线/00:1x 机队 CPU 满用令=@BigMoney）"
    "——水位 131→132（C-20261010-04 经 finalize_state watermark_add 落账）·group_scan 正名探针三面跑（truly_new=1 收讫·ledger @BigStream 4 行==值守锚·HQ orders mtime 00:06:57 破静源坐实）；"
    "②tech#75 判断位照正法双命令=NO-GO 维持（闸1 ollama_probe face=busy-contended〔rc2 超时 60s+util 100+mem 1934=14b 未驻留冷载慢装·busy 生成优先律交集〕+闸2 gate --samples 6 worst-case util 97>80 单面败·free 4741-4762 band 21 稳态过 2048 守卫）"
    "→四腿（MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 v13）维持 fire-ready gated——真发现=探针-闸序污染面（探针自身冷载 14b=util 分量混入随后 gate 采样窗·face 归因本轮不完全可分）→tech#77 落板真种子（驻留预查/序律文档化/probe-coldload 注记三候选）；"
    "③tech#76 交付毕=close_commit.py 扩件 finalize_state() 单一写入器（R1920 占位符双错锚根除：log 行内联字面直拼零代换步=verbatim 落账+前缀正则出生门+task 60 字律单测实现〔逐轮手算前缀长度脆弱面收口〕+tick 双跑守卫+ts 注入钟+watermark 增量去重+原子写）"
    "·11 新测（TestDeriveTask 3+TestFinalizeState 8·R1920 verbatim 锚=含 @TS 字面照落·自测断言错位 1 笔轮内咬住〔mid 态对照〕）·800 全回归绿 149.2s rc=0（run_suite 正法·result 件存证）·C-39 扩 v1.80+changelog"
    "——本尊 dogfood=本轮收账 finalize_state(watermark_add=[C-20261010-04])+两段 commit 全走 run_close_commit（作者面收编起·r1920 外部模板世代退役·判据「后续轮零 log-ts FAIL」兑现窗=下轮起）；"
    "④五查=own orders O-20260908-1105==R1733 锚+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+树态=MV sprint 会话域在飞件零接触（R1745 承继·whisper_to_srt/tests 修改=tech#26 撞面维持）+无 index.lock；"
    "⑤三探针=probe_capture r1927_probes.txt（board 0 FAIL 5 in production/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17〕0 发现/loop_health 2F+229W 皆在案史实〔09-26/28 outage 已裁定不重触发〕）；"
    "⑥例行件=10-11 日报当窗补产毕（daily_brief items=20·bilibili+zhihu 双源 ok·R1845 00:03 先例同窗型）·W42 周审 10-12 未到·GB §④ 下期 10-15 跳过·export 经正典写入器刷（live 三行大白话纪律常设·tech#74）·HQ-FEEDBACK 不写（C-04=知悉件非 open 问题零膨胀）"
    "·tokens:local=0（探针生成调用=探针件非评审调用 R1888 口径·tech#76 纯 CPU 工程）·队列补货步=tech#77 一条真种子·临时件=scratch 删净+证据件入账（tech#64 律）"
    "——下轮=R1928 快速路径首查（08:00 #112 城市口径判据窗届日即领〔城市源非回填 ≥60 ≥2 件+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕+tech#75 照正法续判+四腿点火判断+meme V1 成片查看位）"
)

FOCUS = (
    "R1928 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领〔城市源非回填 ≥60 ≥2 件+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕"
    "+tech#75 判断位照正法续判〔ollama_probe --json+gpu_window_gate --samples 6 双 GO 连续 ≥2 方飞·tech#77 驻留预查候选先行评估〕"
    "+四腿点火判断〔MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/E4 v13〕+meme V1 成片查看位）"
)

MSG2 = (
    "R1927 close: waiting-window executable round; tech#75 dual-gate NO-GO "
    "held (probe face busy-contended 14b cold-load + gate worst-case util "
    "97>80; MV sprint on GPU; probe-gate order contamination -> tech#77); "
    "four legs fire-ready gated; #112 window due 10-11 08:00; watermark "
    "+C-20261010-04 via finalize_state dogfood; export via canonical "
    "writer [via bm-a]"
)

EXPORT_PATCH = {
    "live": [
        "当前活：四件评审件仍在等机器空窗，深夜把收账记账工具修结实了",
        "最近实物：30 秒《爱在西元前》改编 MV（逐镜变速新版），昨晚 20:01 交片",
        "下个里程碑：早上 8 点看城市日报验收数；机器空窗一到四件评审件即开工",
    ],
    "do": ("AI 媒体公司自动循环在岗：四件评审件备好等机器空窗（视频制作会话在"
           "用显卡）；本窗把收账记账工具升级成单一写入器，根治占位符错字老毛病；"
           "明早 8 点城市日报验收窗"),
}


def main():
    # 0. purge scratch (temp-file cleanup hook, tech#64 law)
    for p in SCRATCH:
        try:
            os.remove(os.path.join(ROOT, p))
        except OSError:
            pass
    print("STEP scratch purged")

    # 1. deliverables-first commit (two-segment law, os-protocol 6 v1.12)
    rc, lines = cc.run_close_commit(DELIV, MSG1)
    for l in lines:
        print(l)
    if rc != 0:
        print("ABORT segment-1 commit failed rc=%d (state untouched)" % rc)
        return 1

    # 2. state accounting via the new single writer (tech#76 dogfood)
    summary = cc.finalize_state(
        LOG_LINE, focus=FOCUS, tick=1927,
        watermark_add=["C-20261010-04"])
    print("STATE tick=%s ts=%s wm_added=%d" % (
        summary["tick"], summary["ts"], summary["wm_added"]))

    # 3. export refresh via the canonical writer (tech#70)
    patch_path = os.path.join(ROOT, ".c3-tmp", "r1927_export_patch.json")
    with open(patch_path, "w", encoding="utf-8", newline="") as f:
        json.dump(EXPORT_PATCH, f, ensure_ascii=False, indent=1)
    proc = subprocess.run([sys.executable, "src/os/export_refresh.py",
                           "--patch", patch_path],
                          cwd=ROOT, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    print("EXPORT rc=%d %s" % (proc.returncode,
                               proc.stdout.decode("utf-8", "replace").strip()[:200]))
    try:
        os.remove(patch_path)
    except OSError:
        pass
    export_ok = proc.returncode == 0

    # 4. accounting commit (segment 2)
    seg2 = ["src/os/state.json",
            "data/pipeline/ollama-probe-ledger.jsonl"]
    if export_ok:
        seg2.insert(1, "docs/status-export.json")
    else:
        print("WARN export refresh failed - export left <24h fresh, "
              "excluded from segment 2")
    rc2, lines2 = cc.run_close_commit(seg2, MSG2)
    for l in lines2:
        print(l)
    print("CLOSE-RC seg1=%d seg2=%d" % (rc, rc2))
    return 0 if rc2 == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
