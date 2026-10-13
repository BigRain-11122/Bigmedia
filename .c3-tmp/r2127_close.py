# -*- coding: utf-8 -*-
"""R2127 round close: tech#148 delivery accounting.

Dogfood note (the point of this round): the export refresh goes through
run_close_commit's NEW export_patch/export_do params - the canonical
writer (tech#70) refreshes docs/status-export.json and the file rides
the accounting commit manifest automatically. No hand-written json.dump
anywhere in this close.
"""
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "src", "os"))

import close_commit as cc  # noqa: E402

# --- round-debris cleanup: this round's temp readings (evidence lives in
# the changelog row + queue done mark + suite result lines, not here) ---
for name in ("r2127_item109.txt", "r2127_t148.txt", "r2127_qs.json",
             "r2127_suite.log"):
    p = os.path.join(REPO, ".c3-tmp", name)
    if os.path.isfile(p):
        os.remove(p)

LOG = ("2026-10-13 08:2x R2127: 实活轮·tech#148 交付（收账 export 写入面 canonical writer "
       "强制位=P2 队头当轮兑现·死线窗 08:30 前取活·修法三候选全落）——①轮首五查全静="
       "own orders 顶 O-20260908-1105 mtime 12:08:14==锚零新令+origin_gap_check QUIET "
       "ahead0 behind0（R1500 前置位）+group_scan 六面 fresh 08:12（DECISIONS truly_new=0 "
       "水位 154 维持+LEDGER @BigStream 5 行==值守锚零新转办+ORDERS rows=341 tail "
       "'10-13 04:3x'==stored 水位静〔R2108 已消费〕+DIGEST-SUPPLY advisory 1 已裁决面"
       "〔F-182 staged+main#28 gated 覆盖在位〕+ORDERS-ORIGIN-DELTA quiet delta=0）+无 "
       "index.lock+树态=MV sprint 会话域在飞件（mv0001/mv001 M+??·release/=样片区）零接触"
       "（R1745 承继）；②死线窗读数=release/ 4 件 newest 样片v2 10-08 13:37·full234=False"
       "（08:22 复读·08:30 死线锚在 O-2305 时钟内·main#27 收口判读三连=08:30 后轮）×"
       "fire_consume verbatim=no-fire rc1 reason=bm-a-workday-hours-zero-dispatch"
       "（10-13 工作日时段铁律复执·F-180~183 四件 fire-ready 结转〔fire 真窗=10-14 夜窗/"
       "CEO 下班旗再落〕）；③tech#148 三候选全落=②正身 run_close_commit 新 export_patch/"
       "export_do 参（tech#70 canonical writer 正身刷 export+刷新件自动入 manifest 骑同笔 "
       "accounting commit·拒写 warn-only=export 保持字节原样安全态·RC_WRITER_REFUSE 别名"
       "单测锁+export_now_fn 测试钟位+CLI --export-patch/--export-do）+①任务书 P-61 写入面"
       "强制律一句（禁手写 json.dump·一律走 writer/export 参）+③probe 点名维持（在役零动作）"
       "——7 新测（writer 刷 rides manifest/incremental carryover/拒写 export 原样 close "
       "照落〔R2124 缺陷类回放〕/无参零副作用/dry-run 零写/manifest 去重/别名锁）·1328 全"
       "回归绿 116.6s SUITE_RC=0（1321+7·run_suite 正法）+capabilities v1.113 C-39 面扩+"
       "tech.md #148 done 标；④三探针带内=board 0 FAIL（5 题 10 稿·5 in production）/"
       "readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）+1 发现="
       "render-unannot react-v16（R2118 已裁在链预期红 F-183 登记即清不动）/loop_health 3F"
       "+286W 皆在案史实（三 outage 窗史实+drift 18≤adjudicated 基线 21）；⑤例行件=10-13 "
       "日报在案不重跑（R2086 一份为真相）·W42 周审在案（R2011）·GB §④ v1.3 下期 10-15 "
       "≤7d 跳过+T1 催办无超线项（账号物理件=呈现状行不催办）·HQ-FEEDBACK 不写（零集团层"
       "新 open 问题零膨胀）·tokens:local=0（探针/直读/fire 卡读=零本地模型产出调用·"
       "P-54⑤ 计量律）；⑥队列补货步=真无独立新种子如实注记零膨胀（tech#148 收口=既有项 "
       "done 标非新种子·禁凑数律）·临时件清理钩=.c3-tmp r2127 读数件删净；⑦本尊 dogfood="
       "本轮收账 close 即走新 export 参出 export（canonical writer WROTE 行=判据兑现正身）"
       "——下轮=08:30 后 main#27 死线收口判读三连（成片呈报核→收口判据达成即撤 AIHOT "
       "pause 旗+worker-restart main#21→F-180~183 fire 接力判读面+tech#92 顺延窗维持 "
       "10-14 08:00+main#28 DIGEST-v20 解锁即领）。")

FOCUS = ("08:30 后 main#27 死线收口判读三连（成片呈报核→收口判据达成即撤 AIHOT pause 旗+"
         "worker-restart main#21→F-180~183 fire 接力判读面〔10-13 工作日时段 workday-block "
         "复执=fire 真窗顺延 10-14 夜窗/CEO 下班旗再落〕+main#28 DIGEST-v20 解锁即领）；"
         "react-v16 unannot=在链预期红 F-183 登记即清；tech#92 顺延窗已定谳 10-14 08:00；"
         "watermark 154/341 tail 10-13 04:3x 静；台词池 gate locked 复读 ≥10-17；"
         "close export 一律走 canonical writer/export 参（tech#148 强制律）")

summary = cc.finalize_state(LOG, tick=2127, focus=FOCUS)
print("STATE-SUMMARY %s" % summary)

EXPORT_DO = ("MV 死线 08:30 收口判读待下一轮；本轮=tech#148 交付（收账 export canonical "
            "writer 强制位·三候选全落）+1328 测试全绿")

EXPORT_PATCH = {
    "depts": [
        {
            "n": "工程技术部",
            "t": ("1328 测试全绿；S2 三门+守卫面 20+ 在役；fire 链四件套"
                  "（原子消费+CEO 下班旗+载类闸+吞吐预探）+comfy 波感探针"
                  "+收账 export canonical writer 收编（tech#148）全落位"),
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

FILES = [
    "src/os/close_commit.py",
    "tests/test_close_commit.py",
    "src/os/iteration_prompt.txt",
    "docs/capabilities.md",
    "state/queue/tech.md",
    "src/os/state.json",
]

rc, lines = cc.run_close_commit(
    FILES,
    "tech#148 close_commit canonical export integration (7 tests, suite 1328 green) [via bm-a]",
    root=REPO,
    export_patch=EXPORT_PATCH,
    export_do=EXPORT_DO,
)
for line in lines:
    print(line)
print("CLOSE-RC=%d" % rc)
sys.exit(rc)
