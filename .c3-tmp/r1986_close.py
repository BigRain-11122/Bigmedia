# -*- coding: utf-8 -*-
"""R1986 round close: production round - fire window opened (16:40:56
B-eviction-credit) -> SC-005-04 S1 first leg launched in background (PID
79000, 14b cold-load done, generation still in flight at close = verdict
not landed, zero false-green, next round consumes); DIGEST v18
e4-material pre-load delivered (7/7 verbatim check).
Two-stage commit law: stage A deliverables, then finalize_state + stage B
state.json with close script self-included (tech#81).
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..", "src", "os")))

from close_commit import finalize_state, run_close_commit  # noqa: E402

LOG_LINE = u"2026-10-11 16:5x R1986: 生产轮·fire 窗 16:40:56 开启（B-eviction-credit·gate GO free_min 4942 util_max 32 band 11·mv quiet 159.7min=ComfyUI 波疑似收尾）→SC-005-04 S1 首程发射（call_expert S1-script 后台 79000·14b-8k 冷载 ~2min 后全 VRAM 10.27GB 驻留·close 时生成仍在飞 600s 窗临界·out/err 0 字节=判词未落零假绿·**下轮首查消费其终态**）+DIGEST v18 e4-material 预载毕（R1875 范式顺手步·四段式〔平台形态/完整描述/世界背景/本卡内容〕·机检 7/7 verbatim+AIGC 角标+底部声明全在位〔r1986_e4mat_check.py〕·「六项整改」口径修正=第六项即剧本四律重写防 5+1 误读）——①轮首五查全静=own orders 顶 O-20260908-1105 mtime 12:08:14==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan 四面静=decisions truly_new=0 水位 141 维持+ledger @BigStream 5 行==值守锚零新转办+ORDERS 行水位第七窗 quiet（rows=270 tail_key='10-11 13:4x'==R1979 基线·tech#103 判据连续第七窗过）+HQ orders mtime 14:00:46==R1978 消费锚零新行+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继）；②fire 卡三跑=16:34:37/16:35:51 no-fire（util worst 100>80·**VRAM 面已翻 GO** free 4983+credit effective_free 9859·mv quiet 154.6min 文件面静×硬件忙分叉态）→16:40:56 **FIRE 翻面**（util_max 32 崩落·R1985 后首个 fire 窗）=消费序执法 main#17/tech#105：SC-005-04 先发（S1 材料 R1968+E4 材料 R1973 双 turnkey 在位）——S1 前台首试 5min 零输出自动杀（16:42 启动即杀=平台律实录·零判词零 mp3）→后台 79000 双 redirect 正法重发（Start-Process 句柄剥离·cold load ~16:47 全 VRAM）→close 时仍在飞结转下轮；③三探针带内=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现（78 renders unannot=0）/loop_health 2F+246W 皆在案史实（两 outage 09-26/09-28 已裁定不重触发·drift 17 带内）；④meme V1 成片查看位=片未落盘（v1-zunjie-brake outbound 零 mp4·装配腿 bm-a 会话域在飞零接触如实记）·MD-0002 T2I gated CEO 点头维持·tech#92 雷达标定窗 10-12 08:00 届日即领·W42 周审 10-12 未到；⑤队列补货步=tech#106 真种子（MV 文件面静默×硬件忙长尾态火窗解锁判读面=ComfyUI 侧活度读数候选〔8188 /queue 长度+output newest mtime+进程 CPU 增量〕·R1986 实锚 quiet 154.6min×util 100 分叉·wedged 对极判据缺位=10-10 ollama wedged 槽位同型风险面）+main#17 e4-material 预载毕注记落账；⑥例行件=10-11 日报在案不重跑（一份为真相）·W42 周审 10-12 未到·GB §④ v1.3 下期 10-15 ≤7d 跳过·export_ts 16:24:39 <24h 零 CEO 可见成品态变化节流不刷（live 三行仍准）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=1（S1-script 席真调在飞·expert-calls 行由 call_expert 自动落·判词档未落=下轮验证后才计）；⑦临时件清理钩=r1986 证据五件入账〔e4mat_check/group_scan.json/queue_patch/fire_card.txt/read_r1962〕+ps 探针 json 两件删净·s1 out/err 在飞输出件留盘不删（下轮消费）——下轮=R1987 快速路径首查（**S1 判词收消费**〔79000 终态=expert-verdicts 新判词档 or 超时遗骸→PASS 即续链 TTS light〔edge-tts 零 GPU〕→同文本核验→S2〔ai_feel+ASR 终轨〕→E8+E4→M4→F-176 登记→SC-005-05→06 连发〕+fire 卡复查〔窗仍 GO 即三连全链节奏·窗关即如实结转〕+10-12 08:00 tech#92 雷达标定窗届日即领+W42 周审+meme V1 成片查看位+MD-0002 T2I gated 维持）。"

FOCUS = u"R1987 快速路径首查（**S1 判词收消费**〔后台 79000 终态=PASS 即 SC-005-04 续链 TTS light→同文本核验→S2〔ai_feel+ASR〕→E8+E4→M4→F-176 登记→05→06 连发〕+fire 卡复查〔GO 维持即三连全链·窗关如实结转〕+10-12 08:00 tech#92 雷达标定窗届日即领+W42 周审 10-12+meme V1 成片查看位+MD-0002 T2I gated 维持）"

DELIVERABLES = [
    "data/storylines/cards/MC-20261011-DIGEST-v18-tmp/e4-material.md",
    "state/queue/main.md",
    "state/queue/tech.md",
    ".c3-tmp/r1986_e4mat_check.py",
    ".c3-tmp/r1986_group_scan.json",
    ".c3-tmp/r1986_queue_patch.py",
    ".c3-tmp/r1986_fire_card.txt",
    ".c3-tmp/r1986_read_r1962.py",
]


def main():
    # cleanup transient probe jsons (temp-file hook)
    for f in (".c3-tmp/r1986_ps.json", ".c3-tmp/r1986_ps2.json"):
        if os.path.exists(f):
            os.remove(f)
            print("removed:", f)
    # stage A: deliverables first (two-stage law)
    rc_a, lines_a = run_close_commit(
        files=DELIVERABLES,
        message=("R1986 deliverables: DIGEST v18 e4-material pre-load "
                 "(four-section audience material, 7/7 verbatim lines + "
                 "AIGC badge + declaration check, six-fixes count "
                 "calibration), fire card FIRE 16:40:56 evidence "
                 "(B-eviction-credit, util collapse 100->32, mv quiet "
                 "159.7min), tech seed #106 (ComfyUI-side liveness face "
                 "for quiet-x-busy fire window divergence), main row 17 "
                 "e4 pre-load note [via bm-a]"),
    )
    for ln in lines_a:
        print(ln.encode("ascii", "replace").decode("ascii"))
    print("stage A rc=%s" % rc_a)
    if rc_a != 0:
        return rc_a
    # stage B: state accounting (self-include law commits this script too)
    summary = finalize_state(log_line=LOG_LINE, focus=FOCUS)
    print("finalize tick=%s ts=%s wm_added=%s orders_wm_rows=%s log_len=%s"
          % (summary["tick"], summary["ts"], summary["wm_added"],
             summary["orders_wm_rows"], summary["log_len"]))
    rc_b, lines_b = run_close_commit(
        files=["src/os/state.json"],
        message=("R1986 loop close: production round - fire window "
                 "opened 16:40:56 (B-eviction-credit util collapse, mv "
                 "quiet 159.7min), SC-005-04 S1 first leg launched "
                 "background 79000 (14b cold-load done full-VRAM, "
                 "generation in flight at close = verdict not landed "
                 "zero false-green, next round consumes); DIGEST v18 "
                 "e4-material pre-load delivered 7/7; SC-005-05/06 and "
                 "v18 GPU tail queued behind; ORDERS row-watermark quiet "
                 "7th window tech#103; probes in-band board rc0 [via "
                 "bm-a]"),
    )
    for ln in lines_b:
        print(ln.encode("ascii", "replace").decode("ascii"))
    print("stage B rc=%s" % rc_b)
    return rc_b


if __name__ == "__main__":
    sys.exit(main())
