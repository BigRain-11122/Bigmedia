# -*- coding: utf-8 -*-
# R1992 loop close: chronicle batch-3 deliverable round accounting (two-stage: stage-1 deliverable commit c0f1b649 done)
import io
import json
import re
import sys
from datetime import datetime

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
sys.path.insert(0, ROOT + r"\src")
sys.path.insert(0, ROOT + r"\src\os")

from close_commit import finalize_state, run_close_commit, autodetect_close_script
from group_scan import current_orders_watermark
import export_refresh

STATE = ROOT + r"\src\os\state.json"
EXPORT = ROOT + r"\docs\status-export.json"

log_line = (
    "2026-10-11 18:3x R1992: 实活轮·main#9 编年史续采批三=city-chronicle v1.3「全曲冲刺日」节点续入"
    "（历史事件 26→27：CEO 七令簇〔六项整改/30 秒线终止封存 v4.5 样片终版/导演席审查硬门+tw-mv-director 立档/"
    "女主每曲独立选角律/执行落地机制令/MV 评审分层定谳〕+D-20261011-06 盘燃减负三帽采纳+媒体司六成品日 F-170~175"
    "〔审查执法双日盘点/台风梅花夜事件纪实首件/口述史首件批老晶振·陆海峰·缪一/云勒索信值守题〕+"
    "雷达判据窗验收〔连续第二窗 0 入刊+评分门 60 压线天花板定谳→selection-score 锚例标定上线〕·"
    "orders/decisions/finished 只读正源逐条可溯）+R1898 header 漏升 v1.2 勘正一并收口（v1.1→v1.3 版本谱对齐）"
    "+codex README 版本胞/变更记录双同步+main#9 R1992 注+tech#107 种子落队（codex header 版本谱漂移守卫候选·"
    "单例锚·真发现非凑数）；轮首五查全静=origin_gap_check QUIET ahead0 behind0（R1500 前置位）+"
    "group_scan decisions truly_new=0 水位 141 维持+ORDERS 行水位 quiet rows=270 tail_key='10-11 13:4x'==R1979 基线"
    "（tech#103 机制·漏检 0）+ledger @BigStream 5 行==值锚零新转办+own orders 顶=O-20260908-1105 mtime 锚；"
    "查看位=meme V1 成片仍未落地（R1989 起连续）+krea2 双路径零新到件（14:00:46 EXECUTION-FIX-LEDGER=R1978 已消费件）；"
    "fire 面=tech#106 序律 comfy_activity 18:23:59 quiet rc0（queue 0/0+cpu delta 0.0ms·PID 58200）→"
    "fire_window_card 18:24:55 no-fire（gate-static-no-go：vram worst 460<2048+util 99>80+band 9967MB 秒级负载循环 "
    "advisory）——SC-005-04/05/06 fire-ready 维持结转 F-176/177/178+DIGEST v18 尾 F-179 后段位（tech#105 消费序）；"
    "三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号物理+M4 GATE 6/10+#17）"
    "0 发现/loop_health 2F+249W 皆在案史实基线持平；例行件=W42 周审 10-12 未到+REACT-v15 10-12 窗未到+"
    "global-benchmarks ≤7d 跳过；tokens:local=0（纯文件续采轮零本地模型调用·P-54⑤ 计量律如实记）。"
    "下轮=fire 窗开即 SC-005 三连 S1 连发（tech#105 序）；waiting 面=GPU fire 窗 ETA=MV 渲染波歇。"
)

# --- stage-2a: state.json accounting (single writer) ---
ow = current_orders_watermark()
summary = finalize_state(log_line, orders_watermark=ow, state_path=STATE)
print("FINALIZE:", summary)

# --- stage-2b: export refresh (single-truth writer) ---
with io.open(EXPORT, "r", encoding="utf-8") as f:
    base = json.load(f)

depts = base.get("depts", [])
for d in depts:
    if d.get("n") == "总裁办公室":
        d["t"] = re.sub(r"\b1963\b", "1992", d.get("t", ""))
chips = [list(c) for c in base.get("chips", [])]
if len(chips) < 14 and not any(c[0] == "编年史 v1.3" for c in chips):
    chips.append(["编年史 v1.3", "live"])

patch = {
    "do": "编年史补上「全曲冲刺日」一页；显卡渲染没空档，三件口述史音频在排队。",
    "live": {
        "current": "编年史新页写好；等显卡空档出后续音频。",
        "latest": "编年史 v1.3 新页《全曲冲刺日》（2026-10-11 18:3x）",
        "milestone": "明早八点读雷达日报筛选线新读数（10-12 08:00）。",
    },
    "depts": depts,
    "chips": [list(c) for c in chips],
}

rc, lines, violations = export_refresh.refresh_export(EXPORT, patch=patch)
for l in lines:
    print("EXPORT:", l)
if rc != 0:
    print("EXPORT REFUSED rc=%d - state written, export untouched" % rc)
    sys.exit(2)

# --- stage-2c: close commit (explicit list + self-include via autodetect) ---
files = [STATE, EXPORT]
self_path = autodetect_close_script(ROOT, STATE)
if self_path:
    files.append(self_path)
extra = [ROOT + r"\.c3-tmp\r1992_seed_append.py"]
for p in extra:
    try:
        io.open(p, "rb").close()
        files.append(p)
    except OSError:
        pass

msg = (
    "R1992 loop close: chronicle batch-3 deliverable round (event 26->27 full-song-sprint day; "
    "R1898 header version fix; tech#107 codex-version-drift seed; five-checks quiet; fire card "
    "no-fire GPU window - SC-005 trio + DIGEST v18 tail carried; probes in-band baseline) [via bm-a]"
)
ok = run_close_commit(files, msg, root=ROOT, push=True)
print("CLOSE_COMMIT:", "OK" if ok else "FAILED")
