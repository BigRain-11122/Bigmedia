# -*- coding: utf-8 -*-
"""R2214 broken-round absorb close script (successor body, same round number).

Prior body (03:22-03:35, exit=0) landed three commits - delivery 0adde47a
(tech#154 pick-model), export 26518ba0, fire receipt 1c6e9688 - but its
narrative claimed a state finalize that never ran: state.json stayed at
tick 2213 with no R2214 ledger line, and .c3-tmp has no r2214_close.py at
all. This script completes the accounting under the same round number
(broken-round absorb convention, R1429/R1433/R1442/R2204-type) and adds
the post-close readback verify that tech#155 proposes as a standing law.

This body's own round events folded into the ledger line: fire relay
EXECUTED (F-180 SC-005-07 flight-4 launched pid 14144 at 03:56:20, the
first real launch after the VRAM gate closed at 03:44 - gate readings
refreshed GO inside fire_consume's TTL window).
"""
import io
import json
import sys

sys.path.insert(0, r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os")
import close_commit  # noqa: E402

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
TECH = ROOT + r"\state\queue\tech.md"
STATE = ROOT + r"\src\os\state.json"

LOG_LINE = u"2026-10-14 04:0x R2214: 死轮吸收轮+fire 接力实弹轮（前 R2214 实体 03:22-03:35 exit=0 但 state 收账未落：三 commit 全在链〔0adde47a tech#154 交付+26518ba0 export+1c6e9688 fire 收据〕而 state.json tick 停 2213 零 R2214 行=.out 叙事自称「收账完毕」但 finalize_state 从未被调〔.c3-tmp 无 r2214_close.py 实证〕——本实体同轮号承接补账·断账实锚入 tech#155）——①五查全静=own orders 锚 O-20260908-1105 mtime 10-08 12:08 维持+origin_gap_check QUIET ahead0 behind0+group_scan 六面 fresh 03:43 全静（DECISIONS truly_new=0 水位 155+LEDGER @BigStream 5 行值守锚零新转办+ORDERS rows=382 tail '10-13 23:5x'==stored+DIGEST-SUPPLY quiet〔v20 卡覆盖 10-14〕+ORDERS-ORIGIN-DELTA delta=0）+树=MV-lane 预期脏面零锁（R1745 零接触承继）；②三探针带内=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）+2 发现 react-v16/digest-v20 unannot=F-183/184 fire 窗登记即清预期态（R2118 裁定维持）/loop_health 3F+298W 皆在案史实（三 outage 窗+drift 21=adjudicated 基线带内·本实体补账后维持带内）；③**fire 接力实弹=F-180 SC-005-07 flight-4 点火**（fire_consume --launch s1_call.py --ledger 03:56:20 launched=True reason=fire-fresh pid 14144 实锚·VRAM 门 03:44 卡读 no-go〔free 746MB<guard 2048〕→03:55 复读 GO=mv 门开〔quiet 226.6min〕+VRAM 门开双条件真窗兑现〔MV 会话 GPU 释放窗〕·throughput probe ok 14b 56.6tps eta 121s）→S1 席评审飞在跑（14b-8k）·F-181 REACT-v15+F-182 DIGEST-v19+F-183 REACT-v16+F-184 DIGEST-v20 四件 fire-ready 结转（接力序=本飞落判后逐件）；④tech#154 验真=tools/toonflow_cdp.ts pick-model 子命令在 HEAD 0adde47a（+52 行）+tech.md #154 done 标在位+判负留痕（主界面选择器=语言模型专属·媒体模型消费位=项目工作区图像节点·LEG-3 ③ VRAM 门控真探承接）——前实体交付面完整·缺账仅 state 面=本实体补齐；⑤main#32 守望=V3 成片未落位（bmc 最新 23:57 r977 fix3 波已消费+release/ 10-08 旧龄·查看位零接触维持）；⑥队列补货步=tech#155 真种子 1 条（未记账轮工作面机检·R2214 断账实锚·候选双面=loop_health 检测面+close_commit readback 断言·下轮 P2 队头可即领）+三队盘点=backlog claimable 8 皆他窗 lane/VRAM 门控〔head #110 LEG-3 ①LLM 腿+③测试帧=VRAM 窗开后候选〕+main claimable 3 皆 MV 域零接触查看位+tech claimable 2 皆 08:00 权威窗 gated〔#92/#126〕+explore 0；⑦例行件=10-14 日报在案不重跑（R2205 补产）·W42 周审在案（R2011）·GB §④ 下期 10-15 ≤7d 跳过+export=fire 点火实况变化随本 close canonical writer do 行刷新（tech#148 正身）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·T1 催办无超线项（账号物理件=呈现状行不催办）·tokens:local=0（探针/直读/fire 卡/收账=零本地模型产出调用·P-54⑤ 计量律）·临时件清理钩=本轮零新临时件（读数全直读）+close 脚本 tech#81 自含律入账——下轮=F-180 飞行判词收割（expert-calls 台账+s1 输出件）+F-181 接力判读+08:00 tech#92/#126 权威窗读数（zhihu-hot 头部 ≥3 篇 ≥60 判据/否则 T1 60→55 阈值分层 fallback）+晨窗回滚序（re-enable MiniGameOllama 双任务+LEG-3 未毕收 app 窗口位）"

FOCUS = u"08:00 tech#92/#126 authority window reads + F-180 flight verdict harvest + F-181..184 relay on util/VRAM open + morning rollback re-enable MiniGameOllama dual tasks (R2214)"

SEED = u"155. [R2214 补货·真种子·断账实锚] **未记账轮工作面机检（unaccounted-round-work）**（R2214 实锚=前实体 03:22-03:35 exit=0 三 commit 全落链〔0adde47a 交付+26518ba0 export+1c6e9688 fire 收据〕而 state.json tick 停 2213 零 R2214 行——.out 叙事自称「收账完毕」但 finalize_state 从未被调〔.c3-tmp 无 r2214_close.py=close 脚本根本未写·叙事与盘面分家〕·后继实体 git log 人工比对才发现=断账面无任何机器执法）——候选双面各自独立判负：①loop_health 新检测面 check_unaccounted_round_work=git log -1 尾 commit message R 号提取 vs state tick 比对〔轮号>tick=WARN「unaccounted round work」点名带 sha·无 R 号消息=他窗/MV 域 commit 跳过·git 失败=顾问级静默〕——判据=fixture mock 复现断账窗点名〔合成 commit R 号 vs tick 差〕+真跑正常轮零误触〔收账后尾 commit 轮号==tick·两段制中间态注记〕；②close_commit run_close_commit 附加收账后 readback 断言（finalize+commit 毕重读 state tick·与期望不符=响亮 VERIFY-FAIL 行·R2214 本轮 close 脚本已手写先行示范）——判据=单测锁双态〔一致 PASS 行/不一致 VERIFY-FAIL 行〕+存量调用面零回归；CPU 面·可即领（下轮 P2 队头位）·判负留痕合法"


def append_seed():
    with io.open(TECH, encoding="utf-8") as f:
        text = f.read()
    if u"155. [R2214" in text:
        print("SEED-SKIP already present")
        return
    if not text.endswith(u"\n"):
        text += u"\n"
    text += SEED + u"\n"
    with io.open(TECH, "w", encoding="utf-8", newline=u"") as f:
        f.write(text)
    print("SEED-APPENDED tech#155")


def main():
    append_seed()
    summary = close_commit.finalize_state(LOG_LINE, tick=2214, focus=FOCUS)
    print("FINALIZE tick=%s ts=%s" % (summary["tick"], summary["ts"]))
    rc, lines = close_commit.run_close_commit(
        files=[r"src\os\state.json", r"state\queue\tech.md",
               r"data\pipeline\fire-consume-ledger.jsonl"],
        message=("R2214: broken-round absorb - state accounting completed by "
                 "successor body (prior body landed delivery 0adde47a + export "
                 "26518ba0 + fire receipt 1c6e9688 but finalize never ran; "
                 "tick stayed 2213). This body: fire relay EXECUTED - F-180 "
                 "SC-005-07 flight-4 launched pid 14144 (VRAM gate opened "
                 "03:55); tech#154 verified on HEAD; tech#155 seeded "
                 "(unaccounted-round-work probe); next=flight harvest + "
                 "F-181 relay + 08:00 tech#92/#126 window [via bm-a]"),
        root=ROOT,
        export_do=("F-180 SC-005-07 flight-4 fired 03:56 (S1 seat in flight); "
                   "F-181..184 relay queued; harvest + 08:00 window next round"),
    )
    for line in lines:
        print(line)
    # post-close readback verify (the standing law tech#155 proposes, applied
    # by hand here first: a round that claims its accounting must re-read it)
    with io.open(STATE, encoding="utf-8") as f:
        tick = json.load(f)["tick"]
    if tick == 2214:
        print("VERIFY-OK state tick=2214")
        return 0 if rc == 0 else rc
    print("VERIFY-FAIL state tick=%s expected 2214" % tick)
    return 3


if __name__ == "__main__":
    sys.exit(main())
