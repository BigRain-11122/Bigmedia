# -*- coding: utf-8 -*-
"""R1931 close: two-segment accounting (tech#65/76 law).

Segment 1 = deliverables-first commit (tech#80 noise-fold + caps + tech
queue + R1930 close-script evidence-file backfill + probe ledger).
Segment 2 = finalize_state single-writer accounting + state.json close
commit; the close script ITSELF is in the segment-2 explicit list
(tech#81 judgment first manual dogfood: no cross-round untracked
close-script leak this round).
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
    ".c3-tmp/r1930_close.py",
    ".c3-tmp/r1931_gate_dogfood.txt",
    "data/pipeline/ollama-probe-ledger.jsonl",
]
DELIVER_MSG = (
    "R1931 deliver: tech#80 gate attribution GUI-noise fold (candidates"
    " judged: zero-option fails criteria, bare basename match does not"
    " fix unityvcstray -> GUI_NOISE_PATTERNS=(tray,hub) checked BEFORE"
    " the producer whitelist, noise rows fold to other; first-cut lesson"
    " locked as test: noise matches exe BASENAME only, full-path match"
    " false-folds the real Tuanjie editor installed under"
    " \\Tuanjie\\Hub\\Editor\\; producer matching untouched on full path,"
    " noise=() restores raw-whitelist face; +7 tests (R1930 five-row"
    " anchor reproduction + basename-vs-directory regression lock), suite"
    " 847 green 84.9s rc=0; live dogfood criteria met: producers zero"
    " tray/hub false-positives (ComfyUI python 58200 + Tuanjie 38828 +"
    " llama-server 55432), other 31 folded raw 34, zero deviation vs"
    " manual read; C-37 v1.84 [via bm-a]"
)
LOG_LINE = (
    "2026-10-11 01:5x R1931: 等待窗取活轮·tech#80 交付（gpu_window_gate 归因"
    "面 GUI 噪声折叠批：候选裁=③零方案不过判据〔误中留列〕+①basename 单修不动"
    " unityvcstray〔尾名仍含 unity〕→②GUI_NOISE_PATTERNS=(tray,hub) 先于白名单"
    "判定·误中行折叠 other；**首切真发现修正=noise 判定收窄尾名**——全路径匹配"
    "新造假阴性实锚〔真 Tuanjie 编辑器装 \\Tuanjie\\Hub\\Editor\\ 目录·目录名含"
    " hub 折叠正身=R1931 首跑单测抓获〕→noise 族=可执行名特征只读 basename·"
    "producer 匹配全路径零漂移〔tech#79 面零动〕·noise=() 覆盖恢复 raw-whitelist"
    " 面；7 新测〔R1930 实锚五行复现+首切锚回归锁+CLI 集成〕·847 全回归绿 84.9s"
    " rc=0〔840+7·run_suite 正法〕·真跑 dogfood 判据双过=producers 列零 tray/hub"
    " 误中〔ComfyUI python 58200+Tuanjie 38828+llama-server 55432 三正身〕+与"
    "手工直读零偏差〔other 31 折叠 raw 34·R1929/R1930 归因族连续对位〕·C-37 升"
    " v1.84）+tech#75 判断位照新序律双命令 NO-GO（01:44 gate --samples 6"
    " worst-case free 613<2048 vram 面单闸败 band 13 稳态饱和域→探针 precheck"
    " cold-run free=10752 过 9GB 包络真飞 GEN-OK face=ok〔gpu_util 55/gpu_mem"
    " 1526·行入 ledger〕=非双 GO 不点火·收账段复读 free 5310 过 2048 free 闸但"
    " util 99>80 单闸败 band 345·归因面=三正身零误中）→四腿（MD-0002 剧本腿/"
    " DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 v13）维持 fire-ready gated（材料"
    " R1870/R1871/R1875 turnkey）+meme V1 查看位=成片 mp4 未落（outbound 顶="
    " v1-zunjie-brake 15:41:53==R1899 锚·TTS/装配腿在飞维持）+五查静（own orders"
    " O-20260908-1105==R1733 锚零新令·origin QUIET ahead0 behind0〔R1500 前置位〕"
    "·group_scan truly_new=0 水位 136 维持·ledger @BigStream 4 行==值守锚零新"
    "转办·HQ orders 00:27:11==R1928 消费锚零新行·无 index.lock·树态=mv0001/"
    "mv001/whisper v3 MV sprint 会话域在飞件零接触 R1745 承继）+r1930_close.py"
    " 证据件收账缺口本轮补入+tech#81 种子落队（close 清单自含律候选·本轮收账段"
    "手动自含=首 dogfood）+操作红三笔轮内咬住（PS dir 别名坑→Get-ChildItem 正法"
    "/PYTHONIOENCODING 缺置 GBK 炸→utf-8 前置/powershell -File 跑 .py 误通道+`>`"
    " UTF-16 坑→python subprocess 正法〔R1839 在案族〕）+例行件（10-11 日报在案"
    "不重跑〔R1927 00:2x 一份为真相〕·W42 周审 10-12 未到·GB §④ v1.3 下期 10-15"
    " 跳过·#99 blocked-on-channel 维持〔SLA ≤10-13〕·#112 判据窗 10-11 08:00"
    " 届日即领不预扫·export 00:23:10 <24h 零 CEO 可见成品态变化节流不刷〔live"
    " 三行核读=仍实况准确〕·HQ-FEEDBACK 不写=零集团层新 open 问题零膨胀·"
    "tokens:local=0〔探针生成调用=探针件非评审调用 R1888 口径·纯 CPU 工程+套件"
    "跑零本地模型产出调用·P-54⑤ 计量律〕）——下轮=R1932 快速路径首查（10-11"
    " 08:00 #112 城市口径判据窗届日即领〔城市源非回填 ≥60 ≥2 件+tech#53 双新源"
    "流量首报+tech#5/#30/#49 判定位〕+GPU C-37 fresh 四腿点火判断+meme V1 成片"
    "查看位+tech#81 队头候选〔CPU 面〕）"
)
FOCUS = (
    "R1932 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领〔城市源非回填"
    " ≥60 ≥2 件+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕+GPU C-37 fresh"
    " 四腿点火判断〔MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/E4 v13·双 GO"
    " 连续 ≥2 方飞〕+meme V1 成片查看位+tech#81 队头候选〔CPU 面〕）"
)
CLOSE_MSG = (
    "R1931 close: waiting-window executable round; tech#80 delivered"
    " (attribution GUI-noise fold, basename-only noise match after"
    " first-cut lesson, 847 suite green); tech#75 dual-command NO-GO"
    " held (gate worst-case free 613<2048 band 13 stable-saturated at"
    " 01:44, probe cold-run free 10752 flown GEN-OK face=ok; close-seg"
    " re-read free 5310 clears free gate but util 99>80 single-gate"
    " fail, attribution = three true producers zero false-positive);"
    " four legs fire-ready gated; meme V1 mp4 not landed (outbound top"
    " = v1-zunjie-brake 15:41 == R1899 anchor); five checks quiet"
    " (origin QUIET, wm 136, ledger 4==anchor, HQ orders ==R1928 anchor,"
    " MV-sprint tree domain untouched); r1930_close.py evidence"
    " backfilled this round; tech#81 restock (close-script self-inclusion"
    " law, manual dogfood in this segment); #112 window due 10-11 08:00;"
    " export throttled (00:23 <24h, live lines verified accurate)"
    " [via bm-a]"
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
    finalize_state(LOG_LINE, tick=1931, focus=FOCUS,
                   state_path=os.path.join(REPO, "src", "os", "state.json"))
    print("FINALIZE-OK")
    rc2, lines2 = run_close_commit(
        ["src/os/state.json", ".c3-tmp/r1931_close.py"], CLOSE_MSG,
        root=REPO, push=True)
    for line in lines2:
        print(line)
    if rc2 != 0:
        print("SEGMENT2-FAIL rc=%d" % rc2)
        return 2
    print("SEGMENT2-OK push included")
    return 0


if __name__ == "__main__":
    sys.exit(main())
