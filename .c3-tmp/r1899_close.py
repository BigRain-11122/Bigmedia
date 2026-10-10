# -*- coding: utf-8 -*-
"""R1899 accounting close (tech#65 dogfood: this script's LAST step commits).

Absorbed prior-body round. Updates state.json (tick 1899 + log + ts/task/focus),
refreshes docs/status-export.json (P-61: export_ts + results + live), then calls
close_commit.run_close_commit as the final in-script step (kill window shrunk to
inside this script per tech#65).
"""
import datetime
import io
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "src", "os"))
os.environ["PATH"] = r"C:\Program Files\Git\cmd" + os.pathsep + os.environ["PATH"]

import close_commit  # noqa: E402

now = datetime.datetime.now()
TS_FULL = now.strftime("%Y-%m-%d %H:%M:%S")
TS_MIN = now.strftime("%H:%M")
ROUND = "R1899"
PREFIX = "2026-10-10 %s %s: " % (TS_MIN, ROUND)

CONTENT = (
    "断轮吸收+生产轮＝tech#65 收账内嵌提交器 close_commit 交付（R1897 断轮形态种子·R1898 补货·"
    "prior body 15:4x-16:0x 死于交付 commit 前=close_commit.py+tests+capabilities C-39 行全在盘零 commit·"
    "successor 逐件考古吸收+复验后收口——交付段先行 commit ffa9fdf6 push ok＝tech#27 两段制+本件杀窗收窄双律齐用）"
    "——①交付=src/os/close_commit.py（杀窗收窄=收账段「close 脚本毕→body commit 毕」多轮 body 工具往返缩为脚本内部·"
    "R1897 形态根治件）+六法条编码（显式清单永不 add -A/pathspec 提交=吞暂存事故回归锁/ASCII 先验/push warn-only 自愈律/"
    "列内缺失响亮 rc2/超长 WARN 不 FAIL）+16 新测真 git 夹具——**697 全回归绿 91.9s rc=0**（681+16·run_suite 正法）；"
    "判据②本尊 dogfood 达成=交付段+收账段双真跑（CLI ffa9fdf6+r1899_close.py 末步 run_close_commit·显式清单照守 "
    "MV 会话域零卷入）；判据①断轮零遗留=结构保证+测试锁·真读数待复发窗诚实注；"
    "tech#66 补货（断轮前体中间件吸收探针·本窗 R1893/R1895/R1897/R1899 四断轮族实锚）"
    "②轮首五查=own orders 顶 O-20260908-1105==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0+"
    "group_scan 固定探针静（decisions truly_new=0 水位 130 维持+ledger @BigStream 4 行=R1860 值守锚零新动）+"
    "HQ orders mtime 16:11:46 新行两批消费=O-20261010-1520 G 系候选表令+O-20261010-1555 G 系 12 款定名收口令"
    "（CEO 原话「我改好了 你帮我入档，然后去更新文档」·G02 旧物诊所/G04 螺丝仙人/G05 爆护/G07 人从众/G08 开学啦/"
    "G09 医院大当家/G10 涨停板/G12 就差这一笔/G20 夜聊斋/G26 归园田居）——全 MiniGame 域零 BigStream 份额="
    "知悉 ack commit 消息承载·新锚 16:11:46+无 index.lock+树脏=mv0001/mv001/whisper v3（noise-dict v3 改面）"
    "MV sprint 会话在飞域零接触承继（R1745）"
    "③12:00 GPU 窗 C-37 fresh=NO-GO 双面齐触（pause_face 8/8 Disabled=CEO 让路令在役+free 429MB<9216 守卫）→"
    "四腿（MD-0002 剧本腔+DIGEST v17 M4.5/E4/F-170 S1+tech#43 E4 v13）维持 fire-ready gated"
    "④#115 meme V1 查看位=组件前进（narration.mp3 15:41+S4-v3-check+KF-CONTACT-SHEET-v2 15:38 实录）·"
    "成片 mp4 未到=装配腿在飞维持·#112 判据窗 10-11 08:00 届日即领（tech#53 双新源流量首报同窗）"
    "⑤三探针=prior body probe_capture 15:45:12（board 0 FAIL 5 题 10 稿 5 in production/"
    "readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17〕/loop_health 2F+217W 在案史实·两 outage 已裁不重触发）"
    "——例行事=10-10 日报在案不重跑（R1845 一份为真相）·W41 周审在案 W42 未到 10-12·GB §④ v1.3 下期 10-15 跳过·"
    "15:07 盘余=R1825 点名后不重扫·HQ-FEEDBACK 不写（HQ 两新行=MiniGame 域知悉类·零集团层 open 问题零膨胀）"
    "——临时件钩=hq_orders_tail.py+suite .out/.err 删净·.result/probes/tcc/close 证据件入账收口（tech#64 律）"
    "——tokens:local=0（纯工程+套件跑零本地模型产出调用·P-54⑤ 计量）"
    "——下轮 R1900 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领+tech#53 双新源流量首报+"
    "GPU 窗 C-37 fresh 判读四腿+meme V1 成片随轮盯）"
)

FOCUS = (
    "R1900 快速路径首查（10-11 08:00 #112 城市口径判据窗验收届日即领+tech#53 双新源流量首报+"
    "GPU 窗 C-37 fresh 判读四腿 fire-ready+meme V1 成片随轮盯+tech#66 P2 队头候选）"
)

RESULT_TEXT = (
    "R1899: prior-body broken-round absorption + tech#65 close_commit embedded accounting-close committer "
    "delivered (C-39 v1.72 - the prior 15:4x-16:0x body died before its delivery commit with close_commit.py "
    "+ tests + capabilities C-39 row all on disk uncommitted; successor archaeology + re-verification then "
    "close-out: kill window for the accounting segment narrowed from close-script-done->body-commit-done "
    "(R1897 form, many body tool round-trips) to inside the close script; six encoded laws: explicit file "
    "list never add -A, pathspec commit = 10-09 staged-sweep regression lock, ASCII message pre-git, push "
    "warn-only self-heal, listed-missing loud rc2, msg-over-500 WARN not FAIL; 16 new real-git tests incl. "
    "R1897-form contract lock; 697 suite green 91.9s rc=0 on re-verify) + judgement-2 dogfood MET both "
    "segments this round (delivery via CLI ffa9fdf6 push ok + accounting via r1899_close.py last-step "
    "run_close_commit - explicit-list law held, MV session domain untouched) + tech#66 restocked "
    "(broken-round prior-body middleware absorption probe candidate - delivery-segment blind spot, four "
    "broken rounds this window) + round-opening five checks quiet (origin QUIET, decisions truly_new=0 "
    "watermark 130 slim-set, ledger 4-line anchor) + HQ orders rows O-20261010-1520/1555 consumed "
    "(G-series naming final table + archive order, all MiniGame domain, zero BigStream share, ack in commit "
    "message, anchor 16:11:46) + GPU window C-37 fresh NO-GO (pause fingerprint 8/8 tasks disabled + free "
    "429MB < 9216, four legs stay fire-ready gated) + #115 meme V1 viewpost: components advanced "
    "(narration.mp3 15:41 + S4-v3-check + KF-CONTACT-SHEET-v2 15:38), film mp4 not yet = assembly leg in "
    "flight"
)

LIVE = [
    "当前活：R1899 断轮吸收（prior body 交付件收口·697 绿复验）+tech#65 close_commit 收账内嵌提交器交付"
    "（C-39 v1.72·交付+收账双 dogfood）+GPU 窗 C-37 NO-GO（pause 指纹在役四腿 fire-ready）",
    "最近实物：src/os/close_commit.py+tests/test_close_commit.py（C-39 v1.72·commit ffa9fdf6 push ok）"
    "+tech.md tech#65 done 标注+tech#66 补货",
    "下个里程碑：①10-11 08:00 #112 城市口径判据窗验收（城市源非回填 ≥60 ≥2 件+tech#53 双新源流量首报）"
    "②GPU 窗 C-37 fresh 判读随轮（pause 指纹在役期四腿 fire-ready gated）③meme-daily-v1 V1 成片到件随轮盯（#115）",
]

MSG = (
    "R1899 accounting close via close_commit dogfood (tech#65 first live): state tick 1899 + log + "
    "ts/task/focus, export refresh (P-61), probe-ledger row settled, r1899 evidence middleware settled "
    "(probes/tcc/suite-result/close per tech#64 law); HQ orders rows O-20261010-1520/1555 (G-series naming, "
    "MiniGame domain) acked zero BigStream share, anchor 16:11:46; next: R1900 gate-2 acceptance 10-11 "
    "08:00 (#112 + tech#53 first report) + GPU window fresh read + meme V1 film watch [via bm-a]"
)

ACCOUNT_FILES = [
    "src/os/state.json",
    "docs/status-export.json",
    "data/pipeline/ollama-probe-ledger.jsonl",
    ".c3-tmp/r1899_close.py",
    ".c3-tmp/r1899_probes.txt",
    ".c3-tmp/r1899_tcc_out.txt",
    ".c3-tmp/r1899_suite.log.result",
]


def main():
    print("close: state.json tick 1898->1899 + log + ts/task/focus")
    with io.open(os.path.join(REPO, "src", "os", "state.json"), encoding="utf-8") as f:
        state = json.load(f)
    state["tick"] = 1899
    state["log"].append(PREFIX + CONTENT)
    state["ts"] = TS_FULL
    state["task"] = CONTENT[:60]
    state["focus"] = FOCUS
    with io.open(os.path.join(REPO, "src", "os", "state.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(state, f, indent=1, ensure_ascii=False)
        f.write("\n")

    print("close: export refresh (P-61: export_ts + results entry + live 3 lines)")
    with io.open(os.path.join(REPO, "docs", "status-export.json"), encoding="utf-8") as f:
        export = json.load(f)
    export["export_ts"] = TS_FULL
    export["results"].append(["1899", RESULT_TEXT])
    export["live"] = LIVE
    with io.open(os.path.join(REPO, "docs", "status-export.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(export, f, indent=1, ensure_ascii=False)
        f.write("\n")

    print("close: last step = run_close_commit (tech#65 kill-window form)")
    rc, lines = close_commit.run_close_commit(ACCOUNT_FILES, MSG, root=REPO, push=True)
    for line in lines:
        print("close-commit: " + line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
