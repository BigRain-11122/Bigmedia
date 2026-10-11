# -*- coding: utf-8 -*-
"""R1986 round close (broken-round successor body): prior body died after
launching the SC-005-04 S1 in the 16:40:56 fire window and before running
its own close; the window then slammed shut mid-flight (ComfyUI resumed
100% GPU). This successor body reconstructed the trail, adjudicated the
S1 attempts (4 fired, zero verdicts = NOT passed, zero false-green),
recovered the prior body's stranded deliverables plus the tech#26 R1835
backfill (1012 tests green), and closes the round honestly.
Two-stage commit law: stage A deliverables, then finalize_state + stage B
state.json with this close script self-included (tech#81)."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..", "src", "os")))

from close_commit import finalize_state, run_close_commit  # noqa: E402

LOG_LINE = (
    u"2026-10-11 17:2x R1986: （断轮承接·同轮号收口）生产轮·fire 窗 GO 16:40:56 "
    u"消费即发 SC-005-04 S1→窗中翻脸硬堵如实定谳——①断轮承接=前 R1986 body 于 fire GO"
    u"（B-eviction-credit）消费发 S1 后收账步前阵亡（e4-material 预载+队列双补丁已落盘未 "
    u"commit=本 body 承接续账·R155/R806/R1536 先例）；②S1 消费结局=四发全 ollama timeout"
    u"（15:52 300s/15:56 1500s retry 环/16:42 600s 后台 79000·判词零落 expert-verdicts "
    u"无新档=**S1 未过门·零假绿灯**·SC-005-04 链停在门）；③根因定谳=ComfyUI 复燃窗中翻脸"
    u"（GO 16:40:56 util_max 32→17:0x nvidia-smi 100%/11832MiB·compute-apps 唯一占主="
    u"ComfyUI python 58200〔MV 会话域 CEO 优先线〕·llama-server 被逐零 VRAM→8-token "
    u"最小探针 92s 超时=纯 GPU 饿死族非 wedged 槽位族·让路律正确侧零重启）→fresh 卡 "
    u"17:08:45 no-fire（util-face worst-case 99>80 正确拦停）·M4.5/E4/ASR 终轨全族 "
    u"hard-blocked；④交付面=前 body 件全收编 commit（DIGEST v18 e4-material 预载 7/7 "
    u"verbatim+tech#106 种子+main 16/17 注记）+本 body 增量（tech#106 双证注记〔GO 后窗中"
    u"翻脸面+util-face 拦停面·消费律=GO 消费前 ComfyUI 活度读数先行·窗中翻脸在飞判词一律"
    u"作废重发〕+main16 R1986 结局注+S1 超时证据四件+fire_diag）+**tech#26 R1835 stranded "
    u"回收**（whisper_to_srt v3 扩典+expect 指纹门+asr-noise-dict-v3+34 单测绿+**1012 全"
    u"回归绿**·10-09 起两日跨遗留=临时件清理钩执法）；⑤轮首五查全静（own orders 顶="
    u"O-20260908-1105 mtime 12:08:14==R1733 锚零新令+origin_gap_check QUIET ahead0 "
    u"behind0+group_scan decisions truly_new=0 水位 141 维持+ledger @BigStream 5 行=="
    u"值守锚+ORDERS 行水位 quiet rows=270 tail_key='10-11 13:4x'==R1979 基线+HQ orders "
    u"mtime 14:00:46==R1978 消费锚+无 index.lock+树态=MV sprint 会话域在飞件〔drama/"
    u"mv0001 三件+whisper 会话件零接触不 commit〕）；⑥三探针=board 0 FAIL（5 题 10 稿 5 "
    u"in production）/readiness 3 阻塞皆外部 CEO 面 0 发现（78 renders unannot=0）/"
    u"loop_health 2F+248W 皆在案史实（outage 09-26/09-28 已裁定不重复触发·drift 17 带内"
    u"已裁定·state-ts stale 43min=断轮必然后标本轮收账即平）；⑦例行件=10-11 日报在案不"
    u"重跑（一份为真相）+W42 周审 10-12 未到+GB §④ v1.3 下期 10-15 ≤7d 跳过+meme V1 "
    u"成片查看位=cph4/fleet zunjie/brake/meme/shortvideo mp4 零落盘维持（bm-a 会话域"
    u"在飞零接触如实注记）+export 16:24 <24h 无 F3 实质变化不刷+HQ-FEEDBACK 不写（零集"
    u"团层新 open 问题零膨胀）；⑧队列补货=tech#106 种子（前 body）+双证注记（本 body）"
    u"=本轮补货件·三队盘点=main 16/17 双 gated 线在册+tech 队头 106 判读+explore 队在册——"
    u"下轮=快速路径首查 fire 卡〔tech#106 活度读数面判据先行〕→GO 即重发 SC-005-04 S1"
    u"（标准 1500s 窗）→PASS 续链 TTS light→同文本核验→S2【ai_feel+ASR 终轨】→E8+E4→"
    u"M4→F-176 登记→05→06 连发（窗关如实结轮）·no-fire=等待窗取 P2/P3；10-12 08:00 "
    u"tech#92 雷达标定窗届日即领+W42 周审+REACT-v15 10-12 窗。tokens:local=1（S1 四发 "
    u"ollama 计算耗但判词零落=call_expert 台账零新行·超时件不记成功调用如实注）。"
)

FOCUS = (
    u"R1987 快速路径首查 fire 卡（tech#106 活度读数面判据先行）→GO 即重发 SC-005-04 "
    u"S1（标准 1500s 窗）→PASS 续链 TTS light→同文本核验→S2【ai_feel+ASR 终轨】→E8+E4"
    u"→M4→F-176 登记→05→06 连发（窗关如实结轮）；no-fire=等待窗取 P2/P3；10-12 08:00 "
    u"tech#92 雷达标定窗届日即领+W42 周审+REACT-v15 10-12 窗"
)

DELIVERABLES = [
    "data/storylines/cards/MC-20261011-DIGEST-v18-tmp/e4-material.md",
    "state/queue/main.md",
    "state/queue/tech.md",
    "data/pipeline/gpu-guard-defer-ledger.jsonl",
    "src/render/whisper_to_srt.py",
    "tests/test_noise_dict.py",
    "data/pipeline/asr-noise-dict-v3.json",
    "data/pipeline/whisper-ledger.jsonl",
    ".c3-tmp/r1986_e4mat_check.py",
    ".c3-tmp/r1986_group_scan.json",
    ".c3-tmp/r1986_queue_patch.py",
    ".c3-tmp/r1986_fire_card.txt",
    ".c3-tmp/r1986_read_r1962.py",
    ".c3-tmp/r1986_fire_diag.txt",
    ".c3-tmp/r1986_fulltest.log",
    ".c3-tmp/r1986_s1_00504.out",
    ".c3-tmp/r1986_s1_00504.err",
    ".c3-tmp/r1986_close.py",
    ".c3-tmp/r1986_patch2.py",
]


def main():
    # temp probe jsons cleanup (temp-file hook)
    for f in (".c3-tmp/r1986_ps.json", ".c3-tmp/r1986_ps2.json"):
        if os.path.exists(f):
            os.remove(f)
            print("removed:", f)
    # stage A: deliverables first (two-stage law)
    rc_a, lines_a = run_close_commit(
        files=DELIVERABLES,
        message=(
            "R1986 deliverables (broken-round successor body): DIGEST "
            "v18 e4-material pre-load (7/7 verbatim); tech#106 seed + "
            "double-confirmation (post-GO mid-flight window slam: ComfyUI "
            "resumed 100% GPU, S1 x4 ollama timeouts zero verdicts = S1 "
            "not passed, zero false-green); main row 16 S1 outcome note; "
            "tech#26 R1835 stranded backfill recovered (whisper_to_srt "
            "v3 noise dict + expect fingerprint gate, 34 tests + 1012 "
            "full-suite green); fire-window diagnosis evidence + S1 "
            "timeout trail + defer ledger row [via bm-a]"
        ),
    )
    for ln in lines_a:
        print(ln.encode("ascii", "replace").decode("ascii"))
    print("stage A rc=%s" % rc_a)
    if rc_a != 0:
        return rc_a
    # stage B: state accounting (self-inclusion law commits this script too)
    summary = finalize_state(log_line=LOG_LINE, focus=FOCUS)
    print("finalize tick=%s ts=%s wm_added=%s orders_wm_rows=%s log_len=%s"
          % (summary["tick"], summary["ts"], summary["wm_added"],
             summary["orders_wm_rows"], summary["log_len"]))
    rc_b, lines_b = run_close_commit(
        files=["src/os/state.json", ".c3-tmp/r1986_close2.py"],
        message=(
            "R1986 loop close: production round - fire GO 16:40:56 "
            "consumed, window slammed mid-flight (ComfyUI 100%/11.8GB, "
            "llama-server evicted, 8-token probe 92s timeout = GPU- "
            "starvation family, yield law correct side, no restart); "
            "SC-005-04 S1 four fired calls zero verdicts (not passed, "
            "next fire window relaunch with tech#106 liveness face "
            "first); SC-005-05/06 + DIGEST v18 GPU tails remain gated; "
            "fresh card 17:08:45 no-fire; probes board 0F / readiness 3 "
            "external blockers 0 findings / loop_health 2F adjudicated "
            "historical [via bm-a]"
        ),
    )
    for ln in lines_b:
        print(ln.encode("ascii", "replace").decode("ascii"))
    print("stage B rc=%s" % rc_b)
    return rc_b


if __name__ == "__main__":
    sys.exit(main())
