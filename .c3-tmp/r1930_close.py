# -*- coding: utf-8 -*-
"""R1930 close: two-segment accounting (tech#65/76 law, R1927 first dogfood).

Segment 1 = deliverables-first commit (gate attribution face + tests +
caps + tech queue). Segment 2 = finalize_state single-writer accounting +
state.json close commit. Log line is an in-script UTF-8 literal (verbatim
law: no placeholder substitution step exists in this API).
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "src", "os"))

from close_commit import finalize_state, run_close_commit  # noqa: E402

DELIVER_FILES = [
    "src/os/gpu_window_gate.py",
    "tests/test_gpu_window_gate.py",
    "docs/capabilities.md",
    "state/queue/tech.md",
]
DELIVER_MSG = (
    "R1930 deliver: tech#79 gate NO-GO attribution face (--query-compute-apps"
    " pid+process_name; WDDM blocks per-proc VRAM so face is process-name;"
    " PRODUCER_PATTERNS whitelist lists producers with pid, non-whitelist rows"
    " fold to one other count; attach NO-GO only so GO windows pay zero probe"
    " cost; unreadable probe -> explicit error note, never silent omission;"
    " advisory zero gate-face, exit codes untouched; +10 tests, 5 existing"
    " NO-GO cli tests gain query_compute_apps hermetic mock; suite 840 green"
    " 102.1s rc=0; live dogfood = producers ComfyUI python 58200 + Tuanjie"
    " 38828 + llama-server 67696 (+Tuanjie Hub, unityvcstray tray"
    " false-positive -> tech#80 seed), other 29 folded raw 34, zero deviation"
    " vs R1929 manual read [via bm-a]"
)
LOG_LINE = (
    "2026-10-11 01:4x R1930: 等待窗取活轮·tech#79 交付（gpu_window_gate NO-GO"
    " 归因面：--query-compute-apps pid+process_name 进程名面〔WDDM 无"
    " per-process VRAM〕·白名单生产者逐条列+非白名单折叠 other·advisory 零闸面"
    "·GO 轮零查询·10 新测+5 既有 NO-GO CLI 测试补 mock 保 hermetic·840 全回归绿"
    " 102.1s rc=0·真跑 dogfood=三生产者〔ComfyUI python/Tuanjie/llama-server〕"
    "+29 GUI 折叠 raw 34 与手工直读零偏差）+tech#75 判断位双命令 NO-GO（01:24"
    " gate free 604 vram 面单闸败 band 19 稳态饱和域·01:25 探针 face=ok"
    " ps_size_vram 10002 全驻留=tech#78 advisory 真跑首读 offloaded=false 正确"
    "·收账段复读 free 590/util 100/band 5 双闸败+归因面首战揭 util 源·四腿"
    " fire-ready gated 维持）+meme V1 查看位=mp4 未落（TTS/装配腿在飞·交互窗"
    " lane 零接触）+五查静（origin QUIET·wm 136·C-20261010-01=D-20261011-01"
    " 行内内联引用 R1846 吸收惯例非新转办·ledger 零新行〔5 匹配全 ≤10-09 在案"
    "=锚族〕）+tech#80 补货（unityvcstray 误中白名单精化候选）+export 节流"
    "（00:23 <24h）·#112 判据窗 08:00（城市源非回填 ≥60 ≥2 件+tech#53 首报同窗）"
)
FOCUS = (
    "R1931 快速路径首查（#112 城市口径判据窗 08:00 届日即判〔城市源非回填"
    " ≥60 ≥2 件+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕+tech#75 判断位"
    "照新序律续判〔①gate 先行 --samples 6→②ollama_probe 驻留预查·双 GO 连续"
    " ≥2 方飞〕+四腿点火判断〔MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/E4"
    " v13〕+meme V1 成片查看位+tech#80 队头候选）"
)
CLOSE_MSG = (
    "R1930 close: waiting-window executable round; tech#79 delivered (gate"
    " NO-GO attribution face, 840 suite green); tech#75 dual-command NO-GO"
    " held (gate vram-face 604<2048 band 19 stable-saturated, probe face=ok"
    " ps_size_vram 10002 full-resident = tech#78 advisory first live read"
    " offloaded=false correct; close-segment re-read free 590/util 100 with"
    " attribution first run naming the he-lane); four legs fire-ready gated;"
    " meme V1 mp4 not landed (TTS/assembly in flight, interactive lane);"
    " five checks quiet (origin QUIET, wm 136, C-20261010-01 = inline ref"
    " absorbed per R1846, ledger zero new rows); tech#80 restock"
    " (unityvcstray whitelist false-positive); #112 window due 10-11 08:00;"
    " export throttled (00:23 <24h) [via bm-a]"
)


def main():
    rc, lines = run_close_commit(
        DELIVER_FILES, DELIVER_MSG, root=REPO, push=False)
    for line in lines:
        print(line)
    if rc != 0:
        print("SEGMENT1-FAIL rc=%d" % rc)
        return 1
    print("SEGMENT1-OK")
    finalize_state(LOG_LINE, tick=1930, focus=FOCUS,
                   state_path=os.path.join(REPO, "src", "os", "state.json"))
    print("FINALIZE-OK")
    rc2, lines2 = run_close_commit(
        ["src/os/state.json"], CLOSE_MSG, root=REPO, push=True)
    for line in lines2:
        print(line)
    if rc2 != 0:
        print("SEGMENT2-FAIL rc=%d" % rc2)
        return 2
    print("SEGMENT2-OK push included")
    return 0


if __name__ == "__main__":
    sys.exit(main())
