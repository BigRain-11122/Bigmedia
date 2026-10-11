# -*- coding: utf-8 -*-
# R1954 close: finalize_state (tech#76 single writer) + export_refresh
# (tech#70 canonical writer) + two-segment commit (tech#27 deliverables
# first, then accounting) + r1953 transient-log purge (tech#64).
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src", "os"))

from close_commit import finalize_state, run_close_commit  # noqa: E402

# --- 1. purge r1953 transient logs (absorbed by R1953 ledger; keep the
# pending-fire probe script r1953_score_ab.py - it rides the close commit)
PURGE = [
    "r1953_md0002_out.log", "r1953_md0002_out2.log", "r1953_md0002_out3.log",
    "r1953_md0002_out4.log", "r1953_md0002_err.log", "r1953_md0002_err2.log",
    "r1953_md0002_err3.log", "r1953_md0002_err4.log",
    "r1953_ab_out.log", "r1953_ab_err.log", "r1953_all_lines.txt",
    "r1953_prompt_v1_backup.txt",
]
for name in PURGE:
    p = os.path.join(ROOT, ".c3-tmp", name)
    if os.path.exists(p):
        os.remove(p)
        print("purged:", name)

# --- 2. state accounting (verbatim log line; no placeholders exist) -------
LOG = (
    "2026-10-11 08:4x R1954: 等待窗取活轮·MD-0002 配音腿第一程交付（main#4 CPU 面可执行项·T2I=tech#29 门维持不抢跑）——"
    "三声部档位声直出（tech#2 定谳）+逐镜实测：narrator 8 镜 Yunyang 产线默认/system 2 镜 Yunjian rate-10% pitch-3Hz 机械播报克制/"
    "afeng 3 镜 Xiaoxiao rate+4% pitch+2Hz〔上海话跨语=R1785 保留面·档位声直出本程〕；"
    "空气预算律（6s 镜窗≥0.3s 空气）12/13 fit（shot02 +15%/shot05 +8% rate bump=verbatim 保真机械窗预算·E8 听审可 A/B 回退）+"
    "shot07（04:30 主题锚句）+15% 仍超→自然语速 6.79s=extend-shot 7.1s 候选（+15% 压速与延伸哲学相抵判弃=保锚句自然 delivery）；"
    "drama-ep 窗验证：speech 55.53s+12 gap 求解投影 57.0-74.6s∈[60,90]（floor 面=求解器补 air 正常路径·ceiling 面 74.6<90 留裕）；"
    "资产=data/storylines/audio/MD-0002-voice-v1-shotNN.mp3×13+draft 预览（gitignored·charter §4）+voice-v1.json=装配腿消费正源+"
    "gen-voice-v1.py 可复跑件（路径缺陷 parents[3]→[4] 轮内咬住=data\\data 错位目录清理重跑·首跑产物零泄漏）——"
    "fire 卡 no-fire（util 96%>80=MV lane 满载·gate-credit effective_free 10546 过 vram 面单闸败）→tech#92 A/B 探针维持 GPU 窗发射位"
    "（r1953_score_ab.py 入库保全）·tech#92 判据窗=10-12 08:00 届日即领（锚例版已上线）——"
    "meme V1 查看位零新到件（15:41:53 锚维持·成片未落=TTS/装配腿在飞）·explore#24 刀④ 未领承继（窗内时间让位配音腿）——"
    "轮首五查静（own orders O-20260908-1105==R1733 锚+origin_gap QUIET ahead0 behind0+group_scan truly_new=0 水位 137 维持+"
    "ledger @BigStream 4 行==值守锚+HQ orders 02:06:39==R1935 消费锚+树态=MV sprint 会话域在飞件零接触 R1745 承继）；"
    "三探针=board 0 FAIL〔5 题 10 稿·5 in production〕/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17〕0 发现〔78 renders unannot=0〕"
    "/loop_health 2F+240W 皆在案史实（两 outage 已裁定不重触发·drift 17==基线带内）·证据 .c3-tmp/r1954_probes.txt；"
    "例行件=10-11 日报在案不重跑（R1927 一份为真相）+W42 周审 10-12 未到+GB §④ v1.3 下期 10-15 跳过+export 经正典写入器刷（live 三行大白话 tech#74 常设）+"
    "HQ-FEEDBACK 不写（零集团层新 open 零膨胀）+tokens:local=0（edge-tts=微软免费云端端点零计费·纯 CPU 工程+档案读写·P-54⑤ 计量律）——"
    "下轮=R1955 快速路径首查（tech#92 判据窗 10-12 08:00 届日即领〔zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〕+"
    "A/B 探针 GPU 窗发射位随轮 fire 卡判断+MD-0002 下一腿〔T2I=tech#29 门/装配腿 voice-v1.json 消费〕+explore#24 刀④+meme V1 成片查看位）。"
)
FOCUS = (
    "R1955 tech#92 判据窗 10-12 08:00 届日即领（锚例版 selection-score 已上线·zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补）"
    "+A/B 探针 GPU 窗发射位（r1953_score_ab.py 已入库·fire 卡随轮判断）+MD-0002 下一腿（T2I=tech#29 门〔CEO 点头+GPU 窗〕/装配腿〔voice-v1.json 消费〕）"
    "+explore#24 刀④ 承继+meme V1 成片查看位随轮"
)
summary = finalize_state(LOG, tick=1954, focus=FOCUS)
print("state: tick=%s ts=%s wm_added=%s" % (
    summary["tick"], summary["ts"], summary["wm_added"]))

# --- 3. export refresh (tech#70 canonical writer; self-check gates write) --
import json  # noqa: E402
patch = {
    "do": "MD-0002 配音第一程毕（三声部 13 镜实测·12 入窗+1 延伸候选）·A/B 探针等 GPU 窗·明日 08:00 判定城市头条评分",
    "live": [
        "MD-0002 漫剧配音第一程完成：三个角色 13 镜语音全部生成，12 镜 fits 6 秒窗，04:30 主题句保自然语速留装配延伸",
        "最近实物：13 镜语音+预览落 data/storylines/audio/MD-0002-voice-v1-shot01..13.mp3（2026-10-11 08:4x）",
        "下步：GPU 让出后补 A/B 评分探针；明日 08:00 出城市头条评分新读数（≥3 件 ≥60=收口）",
    ],
}
patch_path = os.path.join(ROOT, ".c3-tmp", "r1954_export_patch.json")
with open(patch_path, "w", encoding="utf-8") as fh:
    json.dump(patch, fh, ensure_ascii=False, indent=1)
import subprocess  # noqa: E402
r = subprocess.run(
    [sys.executable, os.path.join(ROOT, "src", "os", "export_refresh.py"),
     "--patch", patch_path],
    capture_output=True)
print(r.stdout.decode("utf-8", "replace").strip()[-300:])
if r.returncode != 0:
    print("EXPORT-REFRESH rc=%d stderr=%s" % (
        r.returncode, r.stderr.decode("utf-8", "replace")[-200:]))

# --- 4. two-segment commits (tech#27: deliverables first, then accounting)
DELIV = [
    "data/storylines/drama/md0002/gen-voice-v1.py",
    "data/storylines/drama/md0002/voice-v1.json",
    "data/storylines/drama/md0002/README.md",
    "state/queue/main.md",
]
rc, lines = run_close_commit(
    DELIV,
    "R1954 deliverables: MD-0002 voice leg 1 - three-voice cast 13 shot "
    "segments + air-budget readings (12 fit; shot07 natural 6.79s = "
    "extend candidate), window projection 57-74.6s inside [60,90] via "
    "gap solver [via bm-a]")
print("deliverables commit rc=%s" % rc)
for ln in lines:
    print("  " + ln)

CLOSE = [
    "src/os/state.json",
    "docs/status-export.json",
    ".c3-tmp/r1954_probes.txt",
    ".c3-tmp/r1954_ledger_patch.py",
    ".c3-tmp/r1953_score_ab.py",
]
rc2, lines2 = run_close_commit(
    CLOSE,
    "R1954 close: tick 1954, voice-v1 ledger absorbed (main#4 + md0002 "
    "README), fire card no-fire (util 96) keeps AB probe gated for GPU "
    "window, meme V1 anchor unchanged, r1953 transient logs purged "
    "[via bm-a]")
print("close commit rc=%s" % rc2)
for ln in lines2:
    print("  " + ln)
print("R1954 close done rc=%s/%s" % (rc, rc2))
