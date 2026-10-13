# -*- coding: utf-8 -*-
"""R2127 export fix leg: the first close's export patch was REFUSED by the
canonical writer (depts.t over the 96-char contract bound - the gate doing
its job live). Shortened patch through the same close param; success path
completes the tech#148 dogfood (both refusal AND write paths in production).
"""
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "src", "os"))

import close_commit as cc  # noqa: E402

EXPORT_DO = ("MV 死线 08:30 收口判读待下一轮；本轮=tech#148 交付（收账 export canonical "
            "writer 强制位·三候选全落）+1328 测试全绿")

EXPORT_PATCH = {
    "depts": [
        {
            "n": "工程技术部",
            "t": ("1328 测试全绿；S2 三门+守卫面 20+ 在役；fire 链四件套"
                  "+comfy 波感探针+收账 export writer 收编（tech#148）全落位"),
            "s": 1,
        }
    ],
    "chips": [["1328 测绿", "live"]],
    "results": [
        ["179", "成品库总数"],
        ["1328", "测试全绿"],
        ["2127", "OS 轮次"],
        ["R2127", "最近交付"],
    ],
    "live": [
        ("当前活：08:30 MV 死线收口判读在下一轮（成片呈报核→收口即撤 AIHOT 旗+"
         "worker-restart+F-180~183 接力）；本轮已交 tech#148 收账 export 守门件"),
        ("最近实物：close_commit.py 收账 export 收编面（tech#70 canonical writer 强制位"
         "——手写 json.dump 直写 export 从此结构性不可能·拒写=保持原样；7 新测·"
         "1328 全回归绿）"),
        ("下个里程碑：08:30 MV 全曲成片呈 CEO（CEO 直令死线）→收口三连+F-180~183 "
         "fire 接力（fire 真窗=10-14 夜窗或 CEO 下班旗）"),
    ],
}

rc, lines = cc.run_close_commit(
    ["docs/status-export.json"],
    "tech#148 dogfood: canonical export refresh via close param (depts len fix) [via bm-a]",
    root=REPO,
    export_patch=EXPORT_PATCH,
    export_do=EXPORT_DO,
)
for line in lines:
    print(line)
print("CLOSE-RC=%d" % rc)
sys.exit(rc)
