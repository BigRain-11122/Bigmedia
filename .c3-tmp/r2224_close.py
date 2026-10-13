# -*- coding: utf-8 -*-
"""R2224 close: orphan-beat absorb (adjudicated 21->22) + finalize_state + commit.
Anchor: loop_health account-lag FAIL at 06:04 probe (beats 2245 > tick 2223 + 21).
Evidence: run_20261014_055202.log / round_20261014_055202.out (132B one line) /
heartbeat 2026-10-14 05:53:22 exit=0 / no commit after c69c86e7.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "os"))
from close_commit import finalize_state, run_close_commit  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
STATE = os.path.join(ROOT, "src", "os", "state.json")

NOTE_APPEND = (
    " R2224 2026-10-14: +1 broken-round beat absorbed (first silent-exit exit=0 "
    "variant: prior body spawned 05:52:02, finished 05:53:22 exit=0 with a single "
    "narration line in round_20261014_055202.out, zero accounting, zero commits; "
    "successor completed accounting under round number R2224 per absorb "
    "convention). Baseline 21 -> 22. Evidence: logs/iteration-loop/"
    "run_20261014_055202.log (spawn 05:52:02, headless round finished exit=0 "
    "05:53:22); round_20261014_055202.out 132B single line; heartbeat "
    "2026-10-14 05:53:22 exit=0; state tick stayed 2223, no commit after "
    "c69c86e7. Post-adjudication verify: beats 2245 vs tick 2224 + 22 = 2246 "
    "in-band once this round-end beat lands (2246)."
)

LOG_LINE = (
    "2026-10-14 06:1x R2224: 断账吸收轮+等待态一行面（夜窗 00:00-08:00·R2223 后 "
    "05:52 静默退出轮吸收·08:00 权威窗前 ~1.8h）——①loop_health account-lag FAIL "
    "定性收口=orphan beat 05:53:22 exit=0（run_20261014_055202 spawn "
    "05:52:02→finished 05:53:22·.out 仅一行叙事 132B 零收账·state tick 停 2223 零 "
    "R2224 前行·零 commit〔c69c86e7 后无新提交〕）=broken-round 吸收族第四案·首例 "
    "exit=0 静默退出变体（R1479/R1536=exit=1 kill 族）→adjudicated 21→22+证据注入 "
    "account_drift_note（run log/heartbeat/无 commit 三证·本实体同轮号 R2224 "
    "补账·吸收后判据 beats 2246=2224+22 带内自愈）；②五查全静=own orders 锚 "
    "O-20260908-1105 mtime 10-08 12:08 维持+origin_gap_check QUIET ahead0 behind0"
    "（R1500 前置位）+group_scan 六面 fresh 06:03 全静（DECISIONS truly_new=0 水位 "
    "155 维持+LEDGER @BigStream 5 行值守锚零新转办+ORDERS rows=382 tail '10-13 "
    "23:5x'==stored 零新行+DIGEST-SUPPLY quiet〔v20 卡覆盖 10-14〕+ORDERS-ORIGIN-"
    "DELTA delta=0）+树=MV-lane 预期脏面零锁（mv0001/mv001 域 MV sprint 会话件·"
    "R1745 零接触承继·release/ 目录=C-20261013-01 gitignore 收口后 10-08 旧样片 "
    "v1/v2 显形非新成片）；③三探针=board 0 FAIL（5 题 10 稿 5 in production）/"
    "readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）+2 发现 "
    "react-v16/digest-v20 unannot=F-183/184 fire 窗登记即清预期态（R2118 裁定维"
    "持）/loop_health 4F+298W（三 outage 窗+drift 21=adjudicated 基线带内·"
    "account-lag 本轮吸收收口·复检预期回 3F 族）；④fire 面=fire_consume --ledger "
    "正身直发=no-fire rc1 reason=card-no-fire: gate-static-no-go;vram-face "
    "worst-case free 746MB<guard 2048MB;load-class-starved（06:0x 收据·ledger 行"
    "随本 commit 入账）→F-180 SC-005-07 flight-4+F-181 REACT-v15+F-182 "
    "DIGEST-v19+F-183 REACT-v16+F-184 DIGEST-v20 五件 fire-ready carried（真窗="
    "util/VRAM 门开·fire_window_card 唯一仲裁面）；⑤main#32 三联守望=V3 成片仍未"
    "落位（release/=10-08 旧档显形+kf-demo 顶=23:57 r977 fix3 波已消费·查看位零接"
    "触维持）；⑥发现注记=cockpit-heartbeat 用户级 Notification 钩子（用户级 "
    "settings.json·MiniGame CockpitHeartbeat.ps1 -AsHook·CLI 安全闸拦置未信=新改"
    "钩子安全默认面）=他司域如实注记零动作零代信·本司零消费面；⑦例行件=10-14 日"
    "报在案不重跑（R2205 补产·一份为真相）·W42 周审在案（R2011）·GB §④ 下期 "
    "10-15 ≤7d 跳过+export=skip <24h（R2215 canonical writer 刷后 ~1.5h 龄·实况"
    "零变化〔吸收裁定=账面修非产线实况〕·tech#148 强制律下 skip=零写入安全态·"
    "live 三行核读仍准）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·T1 催办无"
    "超线项（账号物理件=呈现状行不催办）·tokens:local=0（探针/直读/fire 卡读=档案"
    "读写零本地模型产出调用·P-54⑤ 计量律）；⑧队列补货步=真无独立新种子如实注记零"
    "膨胀（吸收=在案约定执法非新机制缺口·检测面 loop_health account-lag 本轮实弹"
    "工作正证·钩子注记=他司域·禁凑数律）·临时件清理钩=本轮读数会话内直读零落盘·"
    "close 脚本照 tech#81 自含律入账——下轮=08:00 tech#92/#126 权威窗读数（PASS "
    "或 fallback T1 60→55 判读+tech#156 归因腿触发判定）+晨窗回滚序（re-enable "
    "MiniGameOllama 双任务+LEG-3 未毕收 app 窗口位）+VRAM 门开即 fire 接力 "
    "F-180→184"
)

FOCUS_NEXT = (
    "08:00 tech#92/#126 authority window reads (PASS or T1 60->55 fallback + "
    "tech#156 attribution-leg trigger) + morning rollback re-enable "
    "MiniGameOllama dual tasks + F-180 relay on util/VRAM gate open + main#32 "
    "V3 film watch (R2224)"
)

MESSAGE = (
    "R2224 absorb: orphan beat 05:53:22 exit=0 (silent-exit variant, "
    "run_20261014_055202 one-line .out, zero accounting) absorbed, adjudicated "
    "21->22 with evidence; five checks quiet, board 0F/readiness 3 CEO-blockers/"
    "2 expected unannot, fire no-fire (VRAM 746MB<2048, MV V3 lane yield) "
    "F-180..184 carried; main#32 V3 cut not landed (release/ = 10-08 old "
    "samples resurfaced via gitignore cleanup); cockpit-heartbeat user hook "
    "(MiniGame lane) noted, zero action. Next=08:00 tech#92/#126 window + "
    "morning rollback + fire relay. [via bm-a]"
)

FILES = ["src/os/state.json", "data/pipeline/fire-consume-ledger.jsonl"]


def bump_adjudicated():
    with io.open(STATE, encoding="utf-8") as f:
        data = json.load(f)
    cur = data.get("account_drift_adjudicated")
    if cur != 21:
        raise SystemExit("ABORT adjudicated=%r, expected 21 (concurrent writer?)" % (cur,))
    data["account_drift_adjudicated"] = 22
    note = data.get("account_drift_note", "")
    data["account_drift_note"] = note + NOTE_APPEND
    tmp = STATE + ".tmp_adj"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=1))
    os.replace(tmp, STATE)
    print("ADJUDICATED-BUMP 21->22 note_len=%d" % len(data["account_drift_note"]))


def main():
    bump_adjudicated()
    summary = finalize_state(LOG_LINE, tick=2224, focus=FOCUS_NEXT)
    print("FINALIZE-SUMMARY %r" % (summary,))
    rc, lines = run_close_commit(files=FILES, message=MESSAGE, expect_tick=2224)
    for ln in lines:
        print(ln)
    print("CLOSE-RC %d" % rc)
    raise SystemExit(0 if rc == 0 else 1)


if __name__ == "__main__":
    main()
