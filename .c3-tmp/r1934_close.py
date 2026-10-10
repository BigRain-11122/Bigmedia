# -*- coding: utf-8 -*-
"""R1934 close: tech#82 deliver accounting + window commit.

Window close per os-protocol S6 (live-work round closes the window): the
pending R1933 declared-idle writes (state entry, tech#82 queue seed,
r1933 close/seed evidence files) ride this round's commit alongside the
R1934 deliver files. Explicit-file law throughout (MV sprint tree domain
untouched); r1934_close.py self-includes via the tech#81 autodetect law.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "src", "os"))

import close_commit  # noqa: E402

LOG = (
    "2026-10-11 02:57 R1934: 等待窗可执行实活轮·P2 队头 tech#82 当轮交付"
    "（ollama_probe eviction-aware cold-skip 包络·双面一纪律·C-40）——"
    "①决策面=--eviction-aware 选入旗（classify_precheck 扩 evictable_mb/"
    "eviction_aware 双参·包络测试切换 free+evictable≥envelope·四疑分支 "
    "permissive 照旧·off=逐字节旧形 reason）·让路纪律编码=默认 OFF 姿态"
    "（旗仅限 MV sprint 非活跃窗·help 文本载明契约）；②证据面=反事实列常开"
    "（_ps_other_resident_vram：他驻留模型 size_vram 求和·目标 tag 后缀形态"
    "自排除·缺/坏值贡献 0=保守低记永不虚报+compute_eviction_aware_verdict："
    "fly/skip/None 疑则 None〔tech#78 doubt 律〕）——evictable_mb+"
    "eviction_aware_verdict 两列随 --json 全路径+ps-ok ledger 行"
    "（ps-unavailable 行 exact-shape 契约零动）；15 新测（EvictionAwareTests："
    "提取 3/算术锁 6/verdict 表 1/main 双读面 5）·868 全回归绿 93.5s "
    "SUITE_RC=0（853+15·run_suite 正法）；③判据② 真窗双读数=02:50:35 实跑行："
    "legacy 判 skip（cold-skip free=5663MB<model=9000MB）+evictable_mb=4888+"
    "反事实=fly（5663+4888=10551≥9000）一行双读·零生成飞行零 GPU 负载·"
    "ledger 行落 tracked 件——本窗 MV sprint 活跃→旗未传=让路纪律执法首例"
    "（反事实列=判断位非活跃窗行动依据·无需重飞）；消费注记（tech#75 判断位）="
    "旗仅限 MV sprint 非活跃窗·反事实列恒 advisory；补货=tech#83（gate/probe "
    "包络口径分叉评估）+tech#84（MV sprint 活跃窗判据面=消费前置）双种子；"
    "五查静（origin QUIET ahead0 behind0·own orders==R1733 锚·group_scan "
    "truly_new=0 水位 136 维持·HQ orders 新行=X2348 回执〔GimmeAll 域〕+"
    "CPU O-20261011-0012=BigMoney 域〔无本司份额·R1928 消费锚〕·零 "
    "index.lock·MV sprint 树域零接触 R1745 承继）·探针=loop_health 2F+235W"
    "〔全历史已裁定面·drift done1950 vs tick1934 +16 已裁定基线内〕/"
    "readiness 3 standing blockers〔账号物理件+M4 GATE 6/10+#17 needs-CEO〕/"
    "probe_capture 面在档；#112 判据窗 10-11 08:00 届日即领（~5h·禁预扫维持）·"
    "四腿（MD-0002 剧本/DIGEST v17 M4.5+E4/F-170 S1/E4 v13）维持 fire-ready "
    "gated（双 GO 连续≥2 维持·eviction-aware 反事实列已就位=非活跃窗解锁依据）·"
    "meme V1 查看位=R1933 02:4x 锚维持（禁重扫同一等待对象·装配在飞）·"
    "export throttled（export_ts 00:23<24h·live 三行实况准确·tech#82=内部"
    "工具件零 CEO 面变化不刷新）；窗收 commit=本件（R1933 pending state/tech/"
    "r1933 双证据件一并收口·os-protocol §6 实活轮即收）；tokens:local=0"
)

FOCUS = (
    "R1935 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领"
    "〔城市源非回填 ≥60 ≥2 件+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕"
    "+GPU C-37 四腿 fire-ready 触发判断〔eviction-aware 反事实列已就位·"
    "tech#83/#84 判断位候选〕+meme V1 成片查看位）"
)

FILES = [
    "src/os/ollama_probe.py",
    "tests/test_ollama_probe.py",
    "data/pipeline/ollama-probe-ledger.jsonl",
    "state/queue/tech.md",
    "src/os/state.json",
    ".c3-tmp/r1933_close.py",
    ".c3-tmp/r1933_seed.py",
]

MESSAGE = (
    "R1934 deliver: tech#82 eviction-aware cold-skip envelope (opt-in flag "
    "= yield discipline default-OFF, advisory counterfactual columns always "
    "on, conservative under-credit; +15 hermetic tests, suite 868 green "
    "93.5s rc=0; real-window dual reading 02:50:35: legacy skip "
    "free=5663<9000 + evictable=4888 + verdict=fly, zero flight, ledger "
    "row appended); seeds tech#83/#84; window close incl. R1933 pending "
    "state/tech/evidence; #112 due 08:00 [via bm-a]"
)


def main():
    close_commit.finalize_state(LOG, focus=FOCUS, tick=1934)
    rc = close_commit.run_close_commit(files=FILES, message=MESSAGE,
                                       root=REPO)
    print("CLOSE_RC=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
