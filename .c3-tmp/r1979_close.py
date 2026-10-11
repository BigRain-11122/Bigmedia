# -*- coding: utf-8 -*-
# R1979 close: probes evidence -> orders watermark first-store (tech#103
# dogfood) -> finalize_state (single writer, tick guard) -> pathspec commit.
import datetime
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "os"))

import close_commit  # noqa: E402
import group_scan  # noqa: E402

PROBES = [
    ("board", [sys.executable, "src/board_check.py"]),
    ("readiness", [sys.executable, "src/readiness.py", "--summary"]),
    ("loop_health", [sys.executable, "src/os/loop_health.py", "--loop"]),
]


def run_probes():
    chunks = ["# r1979 probes (compact face) %s" %
              datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    for name, cmd in PROBES:
        p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True)
        out = (p.stdout + p.stderr).decode("utf-8", "replace").strip()
        chunks.append("=== %s (rc=%d) ===" % (name, p.returncode))
        chunks.append(out)
        chunks.append("")
    path = ROOT / ".c3-tmp" / "r1979_probes.txt"
    path.write_text("\n".join(chunks) + "\n", encoding="utf-8", newline="\n")
    print("probes evidence: %s (%d B)" % (path, path.stat().st_size))


def cleanup():
    # temp-file hook: PS `>` redirect artifact (UTF-16 noise) from this
    # round's first targeted unittest run - delete, never commit.
    gone = ROOT / ".c3-tmp" / "r1979_unittest_out.txt"
    if gone.exists():
        gone.unlink()
        print("temp cleanup: r1979_unittest_out.txt removed")


LOG = (
    "2026-10-11 14:5x R1979: 生产轮·tech#103 交付=group_scan ORDERS 行水位面+finalize_state orders_watermark 参"
    "（R1978 补货真发现兑现·O-20261009-1246 取活·两段制收账=close 承载）——"
    "①轮首五查静=own orders 顶 O-20260908-1105 mtime 12:08:14==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）"
    "+group_scan（tech#50 正典）decisions truly_new=0 水位 141 维持+ledger @BigStream 5 行==值守锚零新转办"
    "+HQ orders 14:00:46==R1978 消费锚零新行+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继）；"
    "②tech#103 交付=group_scan 第四面 ORDERS 行水位（face_orders+orders_row_stats 纯核〔^\\s*\\| 表行族计数+尾行首格指纹 {rows,tail_key}〕"
    "+缺水位首跑语义 rc1 带 watermark-missing 注强制首存〔缺基线永不读静〕+缩行/改尾/追加三向偏差全破静 fail-closed"
    "+current_orders_watermark turnkey 助手=close 步零手抄）+finalize_state orders_watermark 参"
    "（C-39 v1.94 扩件={rows int≥1, tail_key 非空 str} 坏形先拒零半写+orders_wm_rows 入 summary/ASCII 证据行·单一写入器律内消费锚）"
    "——13 新测（OrdersRowStatsTests 3+OrdersFaceTests 5〔四判据例+缩行向〕+CLI overall 破静 1+live rows>0 形锁 1+finalize_state 3）"
    "·1012 全回归绿 110.1s SUITE_RC=0（999+13·run_suite 正法·夹具束随 ORDERS 面升格带 orders 水位）"
    "·dogfood 首读=live ORDERS rc1 watermark-missing（rows=270 tail_key='10-11 13:4x'·证据 r1979_group_scan_orders.txt）"
    "→本轮收账 finalize_state(orders_watermark=) 落基线=首存闭环·判据「下轮起 orders 面零人工记忆比对+新行漏检 0」兑现窗=后续轮（R1978 三新行=历史对照组）；"
    "③fire_window_card 14:45:15 no-fire（mv-active 43.4min=MV 全曲冲刺 CEO 优先线让路正确侧·gate 静态双闸败 free 465<2048+util 100>80"
    "·probe busy-contended·readings-age tech#90 在役）→SC-005-04/05/06 三件 fire-ready 维持结转"
    "（F-176/F-177/F-178 三预指·下个 fire 窗 S1 连发=R1978 指针照旧）；"
    "④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现"
    "（78 renders unannot=0）/loop_health 2F+244W 皆在案史实（两 outage=09-26/09-28 已裁定不重触发·drift 17==基线带内·证据 r1979_probes.txt）；"
    "⑤例行件=10-11 日报在案不重跑（R1927 一份为真相）·W42 周审 10-12 未到·GB §④ v1.3 下期 10-15 跳过"
    "·export_ts R1978 14:2x <24h 零 CEO 可见成品态变化节流不刷（live 三行核读=实况仍准确·tech#103=内部工具件）"
    "·tech#92 判据窗 10-12 08:00 届日即领不预扫·meme V1 成片查看位零新到件（R1899 锚维持）"
    "·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0（纯 CPU 工程+套件跑+探针只读零本地模型产出调用·P-54⑤ 计量律）；"
    "⑥队列补货步=真无独立新种子如实注记零膨胀（tech#103=R1978 既有种子兑现非新种子·三队盘点零状态变化·禁凑数律）"
    "·临时件清理钩=r1979_unittest_out.txt（PS > 重定向 UTF-16 噪声件）删净。"
    "下轮=R1980 快速路径首查（fire 卡复查〔MV 渲染波间歇 GO 即发=SC-005-04 S1 连发→05→06 三连单轮全链 F-176/F-177/F-178·TTS 落位 sed 时长行顺手步〕"
    "+tech#92 判据窗 10-12 08:00 届日即领〔zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〕"
    "+ORDERS 面水位首战读数〔新行漏检 0 判据兑现窗〕+W42 周审 10-12+meme V1 成片查看位）。收账显式列文件 commit+push。"
)

FOCUS = (
    "R1980 快速路径首查（fire 卡复查〔MV 渲染波间歇 GO 即发=SC-005-04 S1 连发→05→06 三连单轮全链 "
    "F-176/F-177/F-178·TTS 落位 sed 时长行顺手步〕+tech#92 判据窗 10-12 08:00 届日即领〔zhihu-hot 头部 "
    "≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〕+ORDERS 面水位首战读数〔新行漏检 0 判据兑现窗〕+W42 周审 "
    "10-12+meme V1 成片查看位+MD-0002 T2I gated CEO 点头维持）"
)

MESSAGE = (
    "R1979 tech#103: group_scan ORDERS row-watermark face ({rows,tail_key} vs "
    "state watermark; missing=first-run NEW; shrink/append/tail-edit all break "
    "silence) + finalize_state orders_watermark param (single-writer anchor); "
    "13 tests, 1012 suite green 110.1s SUITE_RC=0; dogfood first-store rows=270 "
    "at close; fire no-fire mv-active 43min yield, SC-005-04/05/06 carried "
    "F-176/177/178; next R1980 quick-path + tech#92 window 10-12 08:00 [via bm-a]"
)

FILES = [
    "src/os/group_scan.py",
    "src/os/close_commit.py",
    "tests/test_group_scan.py",
    "tests/test_close_commit.py",
    "state/queue/tech.md",
    "docs/capabilities.md",
    "src/os/state.json",
    ".c3-tmp/r1979_group_scan_orders.txt",
    ".c3-tmp/r1979_probes.txt",
]


def main():
    run_probes()
    cleanup()

    wm = group_scan.current_orders_watermark()
    print("orders watermark to store: %r" % (wm,))

    summary = close_commit.finalize_state(
        LOG, tick=1979, orders_watermark=wm, focus=FOCUS,
        state_path=str(ROOT / "src" / "os" / "state.json"))
    print("finalize summary: %r" % (summary,))

    rc, _lines = close_commit.run_close_commit(FILES, MESSAGE, root=str(ROOT),
                                               push=True)
    print("run_close_commit rc=%s" % rc)
    return 0 if rc == 0 else 3


if __name__ == "__main__":
    sys.exit(main())
