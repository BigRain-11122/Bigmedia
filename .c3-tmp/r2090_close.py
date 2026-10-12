# -*- coding: utf-8 -*-
# R2090 close: state.json accounting via finalize_state (tech#76 single-writer API)
# + self-contained commit (tech#81 auto-ride). English/ASCII script, CJK only in data strings.
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'os')))
from close_commit import finalize_state, run_close_commit  # noqa: E402

ts_head = datetime.now().strftime('%Y-%m-%d %H:%M')

LOG = (
    ts_head + " R2090: 死线窗值守声明轮（O-2305 成片死线 08:30 在执·MV CEO 优先线独占·R2089 承接·五查静+探针带内）"
    "——①轮首五查全静=own orders 顶 O-20261008-1105 mtime 12:08:14==锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）"
    "+group_scan 六面 fresh 01:03（decisions truly_new=0 水位 154 维持+ledger @BigStream 5 行==值守锚零新转办"
    "+ORDERS rows=338 tail '10-12 23:5x'==stored 水位静+DIGEST-SUPPLY quiet〔v19 staged 卡覆盖〕+ORIGIN-DELTA quiet delta=0）"
    "+无 index.lock+树态=MV sprint 会话域在飞件+watchdog 伴生 M 零接触（R1745 承继）；"
    "②死线窗读数三面=release/ 无 234s 成片（最新=样片v2 10-08 13:37）×comfy quiet（queue 0/0+output 尾件 10-10 23:35=KF 批烧毕 R2085 锚续证）"
    "×cloudv2 波续落（D08_world_flip.mp4 00:37:49≈26min 前=CLOUDWAVE-2 落件续·MV 会话活性在）"
    "→收口判据未达·撤旗+worker-restart main#21+F-180/181/182 fire 接力顺延维持（06:43 装配闹钟+08:30 死线锚在 O-2305 时钟内）；"
    "③tech#121 消费序律=探针毕后 fire_consume verbatim 正身直发=no-fire rc1（reason=card-no-fire: mv-active=CEO 死线优先线 yield 正确侧·ledger 行落盘）"
    "→F-180 SC-005-07 flight-4+F-181 REACT-v15+F-182 DIGEST-v19 三件 fire-ready 结转维持；"
    "④三探针带内=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现"
    "（78 renders unannot=0）/loop_health 3F+282W 皆在案史实（09-26 49min+09-28 609min 两 outage+10-12 09:59→10:57 断轮窗史实"
    "·drift 18≤adjudicated 基线 21）；"
    "⑤三队盘点=承 R2089 00:58 fresh 复读面（~7min 龄零状态变化·禁逐轮重扫同一等待对象反重复律）"
    "→真无可执行项=一行声明收轮合法（waiting: O-2305 成片死线 2026-10-13 08:30〔收口判据=release/ 234s 成片落件或显式收口〕"
    "+tech#92 权威窗 08:00+F-180/181/182 fire 真窗·保护态豁免面=CEO 死线优先线独占）；"
    "⑥例行件=10-13 日报在案不重跑（R2086 补产一份为真相）·W42 周审在案（R2011）·GB §④ v1.3 下期 10-15 ≤7d 跳过"
    "+export_ts 23:25:09 <24h 零 CEO 可见成品态变化节流不刷（live 三行核读仍准：最近实物 F-179/里程碑=tech#92 08:00 判读窗+08:30 死线+fire 三件）"
    "·T1 催办无超线项（账号物理件=呈现状行不催办）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）"
    "·tokens:local=0（探针/fire 卡读=档架读写零本地模型产出调用·P-54⑤ 计量律）；"
    "⑦队列补货步=真无独立新种子如实注记零膨胀（三队盘点零状态变化·cloudv2 波落件=MV 会话域零接触面·禁凑数律）"
    "·临时件清理钩=本轮零临时件产出（纯读+fire/ledger 自落+close 脚本 tech#81 自含）"
    "——下轮=R2091 死线窗值守续（成片呈报轻扫先行→release/ 234s 落件即撤旗+worker-restart main#21+F-180/181/182 fire 接力；"
    "main#27 08:30 收口判读三连；tech#92 权威窗 08:00 届日即领〔resume 分叉照 R2047 行〕）"
)

summary = finalize_state(LOG)
print('FINALIZE-OK tick=%d ts=%s task=%s' % (
    summary['tick'], summary['ts'], summary['task'][:24]))

MSG = ("R2090 deathline watch declaration: five checks quiet (wm154, orders338 tail 10-12 23:5x, "
       "delta0, ledger@BS 5-row anchor), probes in-band; release scan no 234s film yet "
       "(sample-v2 10-08 latest), comfy quiet KF-done, cloudv2 D08_world_flip fresh ~26min "
       "CLOUDWAVE-2 landing; fire no-fire mv-active F-180/181/182 carried; next R2091 "
       "release-scan first, tech#92 08:00 window, 08:30 close triage [via bm-a]")

rc, lines = run_close_commit(
    ['src/os/state.json', 'data/pipeline/fire-consume-ledger.jsonl'], MSG)
for ln in lines:
    print(ln)
print('CLOSE-RC=%d' % rc)
sys.exit(rc)
