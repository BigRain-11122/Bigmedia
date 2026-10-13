# -*- coding: utf-8 -*-
"""R2218 export fix leg (tech#70 canonical writer, short do line <=120 chars)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "src", "os"))
from close_commit import run_close_commit

EXPORT_PATCH = {
    "live": [
        "当前活：夜窗值守+tech#126 窗中读数已落（管道健康零 wedge；判据窗预读 zhihu max48/ge60=0→08:00 权威窗判读）。",
        "最近实物：AIHOT 判据窗预读证据件（管道健康三证+全源评分带读数+fallback 55 不足风险发现），2026-10-14 04:5x。",
        "下个里程碑：08:00 tech#92/#126 权威窗执行（PASS 或 T1 60→55 fallback+归因腿）；fire 五件候 VRAM 开窗发射；V3 成片 main#32 跟进。",
    ],
}
EXPORT_DO = ("R2218 夜窗：tech#126 窗中读数交付（AIHOT 健康+判据窗预读→08:00 判读）；F-180~184 carried；五查静。")

rc, lines = run_close_commit(
    files=["docs/status-export.json",
           ".c3-tmp/r2218_export_fix.py",
           ".c3-tmp/r2218_export_patch.json"],
    message=(
        "R2218 export leg: refresh status-export via canonical writer "
        "(first attempt refused on 188-char do line, contract gate "
        "working as designed; short do <=120 chars now) [via bm-a]"
    ),
    export_patch=EXPORT_PATCH,
    export_do=EXPORT_DO,
)
for line in lines:
    print(line)
print("RC=%d" % rc)
sys.exit(rc)
