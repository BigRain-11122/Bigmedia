# -*- coding: utf-8 -*-
"""R1906 accounting close (tech#72 consumer verification + O-2006 ack round).

Does: state.json tick/log/ts/task, scratch tmp cleanup (evidence kept),
then run_close_commit as the LAST step (tech#65 embedded-commit law).
tech.md / backlog.md / export_refresh.py / export already updated in-body.
"""
import io
import json
import os
import re
import sys
from datetime import datetime

REPO = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
ROUND = "R1906"
LOG_LINE = (
    "2026-10-10 20:2x R1906: 收令+生产轮·O-20261010-2006 全员全面开工令消费+四腿闸门"
    "重判+tech#72 live 消费方核验收口（实活轮·两段制收账=close_commit 末步内嵌）——"
    "①轮首五查破静一处=HQ orders mtime 20:08:26 破 R1902 锚 18:54:32 尾读三批新行："
    "**O-20261010-2006 全员全面开工令·算力全解禁·放开并行**（§全员 resume 广播·"
    "bm-a 已 -Mode resume 20:06·本司份额=让路令解除后闸门重判+本 commit 消息 ack "
    "三要件承载）+**O-20261010-1955 硅基窗自审整改+二级页面+大白话令**（bm-a 交互窗"
    "承接·本司 export 消费面 R1901/R1905 v6.2 合规在位·canonical.html 1308 行在飞"
    "重写态实测=tech#73 复验位入队）+20:0x 价值意义重申令（@BigMoney 域知悉）；余四查"
    "静=own orders 顶 O-20261008-1105==R1733 锚+origin_gap_check QUIET ahead0 behind0"
    "+group_scan decisions truly_new=0 水位 131+ledger @BigStream 4 行==值守锚+无 "
    "index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继）；②四腿闸门 fresh 重判="
    "**C-37 pause_face=clear（8/8 任务恢复=让路令解除实证）但 vram_face free 600MB<9216="
    "NO-GO**+ollama 探针 --ledger rc2 TimeoutError face=busy-contended gpu 100%/11711"
    "（他 lane 合法满载·O-2006 放开并行态非 CEO 让路面）→MD-0002 剧本腿/DIGEST v17 "
    "M4.5·E4/F-170 S1/E4 v13 四腿维持 fire-ready gated（材料 R1870/R1871/R1875 "
    "turnkey·VRAM 让渡即开）；③tech#72 交付（R1905 补货兑现·CPU 面）=**消费方核验"
    "定谳=shaper 不消费 live 键（判负留痕·预注册分支执行）**——generate.ps1 v6.2 "
    "消费块 L180-241 六键集实证（export_ts/do/depts/outs/chips/results）+canonical.html "
    "卡面 s.now 源追定=strings.json 策展 subs[n].now（最新动作=heartbeat last_subj 面）"
    "→守卫降级=export_refresh.py KNOWN_KEYS 注记收口（live 留白名单=CEO 直读面正身"
    "〔产品优先律 §5〕·零新 loop_health 面=反膨胀律·capabilities 不升表=验证类负结果件）"
    "·证据件 .c3-tmp/r1906_t72_consumer_evidence.txt（四扫描块归一）·**767 全回归绿 "
    "108.6s**（注释级改动零漂移）·tech#73 补货（O-1955 硅基窗重构落位后消费面复扫·"
    "gated 交互窗收口）；④查看位双路径（R1762 律）=#111 krea2=**v4.5 变速档成片增量"
    "实录**（30s_reel_v4.mp4 20:01:07 重建 46.9MB+DELIVERY-QC-BOARD-v45 20:02+"
    "DELIVERY-NOTE-v44 v4.5 节 20:03=CEO 20:04 变速终裁「匀速=最大 AI 感·逐镜速度"
    "设计」配套交付·R1902 首版 18:23:58 在案·backlog #111 R1906 注记落账·MV 会话域"
    "零接触）+#115 meme outbound 零新到件（止于 15:41 narration.mp3==R1899 锚·V1 "
    "TTS/装配腿在飞维持）；⑤export 走 tech#70 正典写入器刷 live 三行（export_ts "
    "20:22:36 live-clock·收令+四腿重判+查看位实况·P-61 面）；⑥三探针=board 0 FAIL"
    "（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE "
    "6/10+#17 needs-CEO）0 发现（78 renders 全注账）/loop_health 2F+225W 皆在案史实"
    "（两 outage=09-26/09-28 已裁定不重触发·drift 17=基线带内）；⑦例行件=10-10 日报"
    "在案不重跑（R1845 一份为真相）·W41 周审在案 W42 件 10-12 未到·GB §④ v1.3 下期 "
    "10-15 跳过·#112 判据窗 10-11 08:00 届日即领（tech#53 双新源首报同窗）·#99 "
    "blocked-on-channel 维持（SLA ≤10-13）·HQ-FEEDBACK 不写（零集团层新 open 问题"
    "零膨胀）·tokens:local=0（纯探针+消费面扫描+套件跑零本地模型产出调用·P-54⑤ 计量律）"
    "——下轮=R1907 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领+GPU 窗 C-37 "
    "fresh 四腿判断+meme V1 成片到件随轮盯）。收账显式列文件 commit+push。"
)

COMMIT_FILES = [
    "src/os/state.json",
    "docs/status-export.json",
    "state/queue/tech.md",
    "src/os/backlog.md",
    "src/os/export_refresh.py",
    "data/pipeline/ollama-probe-ledger.jsonl",
    ".c3-tmp/r1906_t72_consumer_evidence.txt",
    ".c3-tmp/r1906_probes.txt",
    ".c3-tmp/r1906_group_scan.json",
]
COMMIT_MSG = (
    "R1906: ack O-20261010-2006 all-hands+compute-unlock (4 legs re-gated: "
    "pause clear 8/8 but VRAM 600MB full -> fire-ready) + O-20261010-1955 ack "
    "(siliconwatch rework; loop share=export face v6.2 clean); tech#72 done: "
    "live-key consumer verify=shaper 6-key set, live unconsumed -> writer "
    "whitelist annotation, 767 green; viewpos: krea2 v4.5 speed-cut reel 20:01 "
    "(#111), meme outbound no arrivals (#115); next R1907: 10-11 08:00 radar "
    "city-criteria gate + GPU legs fresh gate [via bm-a]"
)
SCRATCH = [
    "r1906_orders_tail.txt", "r1906_live_hits.txt", "r1906_consume_block.txt",
    "r1906_canon_scan.txt", "r1906_now_src.txt", "r1906_writer_head.txt",
    "r1906_tech_head.txt", "r1906_tech_tail.txt", "r1906_bl_anchor.txt",
    "r1906_t72_consolidate.py", "r1906_now_src_probe.py",
    "r1906_export_patch.json",
]


def main():
    steps = []

    # --- 1. state.json: tick/log/ts/task ---
    state_path = os.path.join(REPO, "src", "os", "state.json")
    with io.open(state_path, "r", encoding="utf-8", newline="") as fh:
        state = json.load(fh)
    if state.get("tick") == 1906 and state.get("task", "").startswith("收令+生产轮"):
        steps.append("state.json: already closed at tick 1906 (prior partial run)")
    else:
        assert state["tick"] == 1905, "expected tick 1905, got %s" % state["tick"]
        state["tick"] = 1906
        state["log"].append(LOG_LINE)
        state["ts"] = NOW
        m = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{1,2}x? R\d+: (.*)$", LOG_LINE)
        assert m, "log line prefix shape"
        state["task"] = m.group(1)[:60]
        with io.open(state_path, "w", encoding="utf-8", newline="") as fh:
            json.dump(state, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        steps.append("state.json: tick=1906, log+1, ts=%s" % NOW)

    # --- 2. scratch cleanup (evidence files kept) ---
    removed = []
    for name in SCRATCH:
        p = os.path.join(REPO, ".c3-tmp", name)
        if os.path.isfile(p):
            os.unlink(p)
            removed.append(name)
    steps.append("scratch removed: %d file(s)" % len(removed))

    for s in steps:
        print("OK", s.encode("ascii", "replace").decode("ascii"))

    # --- 3. embedded accounting commit (LAST step, tech#65 law) ---
    sys.path.insert(0, os.path.join(REPO, "src", "os"))
    import close_commit
    rc, lines = close_commit.run_close_commit(
        COMMIT_FILES, COMMIT_MSG, root=REPO, push=True)
    for line in lines:
        print(line.encode("ascii", "replace").decode("ascii"))
    print("CLOSE-DONE rc=%d ts=%s" % (rc, NOW))
    return rc


if __name__ == "__main__":
    sys.exit(main())
