# -*- coding: utf-8 -*-
"""R1937 close: finalize_state (tech#76 writer) + run_close_commit (C-39).

Two-stage close per house law: deliverables pre-committed at 108f3eb8
(probe+tests+tech.md+capabilities+ledger+probes evidence). This script
carries the accounting tail: state log/tick/ts/task + explicit-file
commit+push (self-inclusion law auto-adds this script once tick=1937).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "os"))
import close_commit as cc  # noqa: E402

LOG = (
    "2026-10-11 03:57 R1937: 等待窗取活轮·tech#86 交付（mv_sprint_probe --ledger "
    "JSONL 台账面·C-40 v1.88·O-20261009-1246 取活·两段制收账=交付段先行 commit "
    "108f3eb8+finalize_state+run_close_commit 正法）——①轮首五查全静=own orders 顶 "
    "O-20260908-1105 mtime==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0"
    "（R1500 前置位）+group_scan（tech#50 正典）truly_new=0 水位 137 维持+wm_only=1"
    "（C-20261010-01 行内引用族）+ledger @BigStream 4 行==值守锚零新转办+HQ orders "
    "零新行+无 index.lock+树态=mv0001/mv001/whisper v3/drama_takt MV sprint 会话批"
    "域在飞件零接触（R1745 承继·tech#26 撞面维持）；②GPU C-37 四腿 fresh 判断="
    "mv_sprint_probe quiet rc0（三面 3612.8/247.7/1798.3min·最新写锚 LOOKBOARD-"
    "FULL 23:35 后 4.1h 静默）×gate NO-GO（worst-case free 579<9216+band 8888MB "
    "振荡域 advisory+util max 38·归因三正身 ComfyUI python 58200+Tuanjie 38828+"
    "llama-server 47304）=文件静×硬件忙双读数=长渲染在飞（落盘写未到）维持 gated"
    "（R1936 同判）·四腿（MD-0002 剧本腿/DIGEST v17 M4.5·E4/F-170 S1/tech#43 E4 "
    "v13）fire-ready gated 维持·tech#85 复合判断件维持 gated（真窗=gate GO+probe "
    "quiet 未现）；③#112 城市口径判据窗 10-11 08:00 未到（~4.3h·届日即领不预扫）"
    "+meme V1 查看位零新到件（outbound 顶=15:41:53 narration.mp3==R1899 锚·成片 "
    "mp4 未落=装配腿在飞维持）；④tech#86 交付=--ledger [PATH] opt-in JSONL 台账面"
    "（一行一探测·五字段精确集 ts/verdict/rc/newest_age_min/threshold_min·error "
    "跑照落行=fail-closed 也是数据·bare flag=默认 data/pipeline/mv-sprint-probe-"
    "ledger.jsonl·写失败 WARN 不动 rc〔tech#19/52 正法〕+父目录自建·判断位引文自"
    "此读 ledger 尾行替代 state log 手拼）·8 新测（LedgerTests：字段精确集/error "
    "行 null/双跑双行/父目录自建/写失败 WARN 不炸/CLI 行落盘+rc 传播/bare flag 默"
    "认路径/无 flag 零写）·910 全回归绿 90.5s SUITE_RC=0（902+8·run_suite 正法）"
    "·判据双过=本尊 dogfood 双真跑两行落盘逐字段一致（03:50:11 --json+03:50:12 "
    "human·quiet/rc0/newest_age_min 254.3/threshold 90）+无 flag 零动（先行消费跑"
    "零 ledger 写+单测锁）；⑤三探针=probe_capture 紧凑面（board 0 FAIL〔5 题 10 稿 "
    "5 in production〕/readiness 3 阻塞皆外部 CEO 面〔账号批次①+M4 GATE 6/10+#17 "
    "needs-CEO〕0 发现〔78 renders 全注账〕/loop_health 2F+235W 皆在案史实〔两 "
    "outage 09-26/09-28 已裁定不重触发〕）；⑥例行件=10-11 日报在案不重跑（R1927 "
    "一份为真相）·W42 周审 10-12 未到·GB §④ 下期 10-15 跳过·export_ts 00:23<24h "
    "零 CEO 可见变化节流不刷（live 三行核读=仍实况准确）·HQ-FEEDBACK 不写（零集团"
    "层新 open 问题零膨胀）·tokens:local=0（纯探针+只读+CPU 工程零本地模型产出调"
    "用·P-54⑤ 计量律）·队列补货步=真无新种子如实注记零膨胀（tech#85 真窗位/"
    "tech#75 序列位=既有行射程·禁凑数律）——下轮=R1938 快速路径首查（10-11 08:00 "
    "#112 城市口径判据窗届日即领〔城市源非回填 ≥60 ≥2 件+tech#53 双新源流量首报+"
    "tech#5/#30/#49 判定位〕+GPU C-37 fresh 四腿点火判断〔mv_sprint_probe --ledger "
    "尾行引文首用〕+meme V1 成片查看位）"
)

FOCUS = (
    "R1938 快速路径首查（10-11 08:00 #112 城市口径判据窗届日即领〔城市源非回填 "
    "≥60 ≥2 件+tech#53 双新源流量首报+tech#5/#30/#49 判定位〕+GPU C-37 四腿 fresh "
    "触发判断〔mv_sprint_probe --ledger 尾行引文+gate/probe 双读数→tech#85 复合判"
    "断件真窗〕+meme V1 成片查看位）"
)

cc.finalize_state(LOG, tick=1937, focus=FOCUS)
print("state finalized: tick=1937")

FILES = [
    "src/os/state.json",
    ".c3-tmp/r1937_stage1.py",
    ".c3-tmp/r1937_inspect.py",
    ".c3-tmp/r1937_meme_check.py",
    ".c3-tmp/r1937_c40_row.txt",
]
MSG = ("R1937 close: tech#86 delivered (mv_sprint_probe --ledger JSONL "
       "face, 5-field exact rows, error runs rowed, bare-flag default "
       "path, judgment citation switches to ledger tail; suite 910 "
       "green 90.5s rc=0, dogfood two rows field-identical); five checks "
       "quiet (own orders anchor unchanged, origin QUIET, group scan "
       "truly_new=0 watermark 137, no index.lock, MV sprint domain "
       "zero-contact); four legs gated (file quiet x gate NO-GO free 579 "
       "ComfyUI busy), tech#85 gated on first real window; #112 due "
       "08:00; meme V1 mp4 not landed) [via bm-a]")

rc, lines = cc.run_close_commit(FILES, MSG)
for ln in lines:
    print(ln)
print("CLOSE_RC", rc)
sys.exit(0 if rc == 0 else 1)
