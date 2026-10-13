# -*- coding: utf-8 -*-
"""R2222 waiting-state close (night window 00:00-08:00) via finalize_state canon path."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, r"src\os")
import close_commit

log_line = (
    "2026-10-14 05:3x R2222: 等待态一行收账（夜窗 00:00-08:00）：R2221 后 ~8min 状态零漂移，等待项与同一批扫描面复验全静="
    "own orders 锚 O-20260908-1105 维持+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan fresh 05:34 全静"
    "（DECISIONS truly_new=0 水位 155 维持+LEDGER @BigStream 5 行价值锚定转办+ORDERS rows=382 tail '10-13 23:5x'==stored+"
    "DIGEST-SUPPLY quiet）；fire 不发火 rc1（gpu_window_gate NO-GO：worst-case free 748MB < 2048 guard，load-class-starved，"
    "attribution=Tuanjie×3+Unity_DF×3+ComfyUI+llama-server——MV V3/CEO 前台道让路）F-180..184 carried；main#32 V3 成片未落地"
    "（mv_sprint_probe quiet·顶件仍 r977 fix3 age 339min）；探针带内（loop_health 3 FAIL 皆史实〔09-26/09-28/10-12〕+"
    "readiness 3 blocker 皆外部 CEO 面+F-183/F-184 L 卡 unannot=fire-ready 结转预期红）；队列 triage 全 gated"
    "（tech#92/#126 08:00 权威窗未到·tech#156 同读数；morning rollback 08:00；fire relay 等 VRAM 闸开）；零新种子如实注记。"
    "Next=08:00 权威窗读数+morning rollback+fire relay on VRAM gate open。"
)

res = close_commit.finalize_state(
    log_line,
    focus="08:00 tech#92/#126 authority window reads (PASS or T1 60->55 fallback + tech#156 attribution-leg trigger) + morning rollback re-enable MiniGameOllama dual tasks + F-180 relay on util/VRAM gate open + main#32 V3 film watch (R2222)",
)
print("finalize_state ->", res)
