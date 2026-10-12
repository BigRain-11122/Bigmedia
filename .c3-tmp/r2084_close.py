# -*- coding: utf-8 -*-
"""R2084 close: death-line watch round -- state tick/log/ts/task/focus. No new orders rows (watermark holds)."""
import io, json, datetime

STAMP = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

LOG_LINE = (
    "2026-10-12 23:4x R2084: 死线窗值守轮（O-2305 成片死线 10-13 08:30+O-2330 榨干令四线在执·MV CEO 优先线独占·R2083 承接）——"
    "①轮首五查全静=own orders 顶 O-20261008-1105 mtime 12:08:14==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）"
    "+group_scan 六面 fresh 23:43（decisions truly_new=0 水位 152 维持+ledger @BigStream 5 行==值守锚零新转办"
    "+ORDERS rows=337 tail '10-12 23:3x'==stored 水位〔R2083 收讫·CDN 索引行族未到=O-2305 执行件既定追加制待下轮消费〕"
    "+DIGEST-SUPPLY quiet〔v19 staged 卡覆盖〕+ORIGIN-DELTA quiet〔delta=0〕+MTIME 静）"
    "+无 index.lock+树态=MV sprint 会话域在飞件+tech#140 他窗在飞（fire_window_card.py+tests M）全族零接触（R1745/R1893 承继）；"
    "②三探针带内=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）"
    "0 发现（78 renders unannot=0）/loop_health 3F+281W 皆在案史实（09-26 49min+09-28 609min 两 outage+10-12 09:59→10:57 晨间窗"
    "·drift 18≤adjudicated 基线 21）；"
    "③tech#121 消费序律=探针毕后下一命令 fire_consume verbatim 正身直发=no-fire rc1（reason=card-no-fire: mv-active"
    "=CEO 死线优先线 yield 正确侧·ledger 行落盘）→F-180 SC-005-07 flight-4+F-181 REACT-v15+F-182 DIGEST-v19 三件 fire-ready 结转维持；"
    "④MV 死线窗读数=收口判据未达：comfy_activity active（queue running=1=KF 批在烧·output newest_age 2298s）"
    "×mv_sprint_probe active（mv-outbound INT5_head_bow.mp4 1.8min 前写=cloudv2 波在落·KF/情绪帧线夜窗在执）"
    "→撤旗+worker-restart main#21+F-180/181/182 fire 接力顺延维持；"
    "⑤成片呈报轻扫=release/ 最新=样片v2 10-08 13:37 无 234s 全曲成片（装配腿 06:43 收片装配在 O-2305 计划窗内·08:30 死线锚）；"
    "⑥三队盘点=承 R2083 23:3x fresh 复读面（~4min 龄零状态变化·禁逐轮重扫反重复律）"
    "=main 全 gated/查看位（#19/#20/#24 fire-gated·#21 resume-gated CEO 面·#22 常务轮复读 10-13 00:00 窗后未到"
    "·#25/#26/#27 夜窗/死线守望位）+tech 全 done/gated/观察位（#92 权威窗 10-13 08:00 届日即领不预扫·#126 gated resume"
    "·#135 fire 窗·#140 他窗在飞）+explore 全 done/gated/到点未至→真无可执行项=一行声明收轮合法"
    "（waiting: O-2305 成片死线 2026-10-13 08:30〔收口判据=comfy output 持续闲 ≥30min 或显式收口+release/ 234s 成片落件〕"
    "·保护态豁免面=CEO 死线优先线独占）；"
    "⑦例行件=10-12 日报在案不重跑（R2008）+W42 周审在案（R2011）+GB §④ v1.3 下期 10-15 ≤7d 跳过"
    "+export_ts 23:25:09 <24h 零 CEO 可见成品态变化节流不刷+T1 催办无超线项（账号物理件=呈现状行不催办）"
    "+HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）+tokens:local=0（探针/直读零本地模型产出调用·P-54⑤ 计量律）；"
    "⑧队列补货步=真无独立新种子如实注记零膨胀（本轮读数全在既有判定面·comfy running=1+INT5_head_bow 1.8min"
    "=O-2305/KF 线既定执行态非新工位·禁凑数律）·临时件清理钩=本轮零新临时件（直读命令零脚本落盘·close 脚本随 commit 入账）"
    "——下轮=R2085 死线窗值守续（成片呈报轻扫先行→达成即撤旗+worker-restart main#21+F-180/181/182 fire 接力）"
    "+main#22 常务轮复读（10-13 00:00 窗后）+tech#92 权威窗 10-13 08:00（R2047 顺延律随行）"
)

FOCUS_NEW = (
    "死线窗值守（O-2305 成片死线 10-13 08:30+O-2330 全量榨干令四线在执·MV CEO 优先线独占）"
    "→成片呈报轻扫先行（R2084 读数=release/ 无 234s 成片·comfy queue running=1 KF 批在烧"
    "·mv-outbound INT5_head_bow 1.8min 新鲜=cloudv2 波在落）"
    "→收口判据达成即撤旗（AIHOT pause 旗）+worker-restart main#21+F-180/181/182 fire 接力；"
    "main#22 常务轮复读 10-13 00:00 窗后；tech#92 权威窗 10-13 08:00 顺延律随行；"
    "CDN 索引行族今夜将追加 orders（O-2305 执行件）=ORDERS-NEW 面既定消费"
)

# ---------- state.json ----------
raw = io.open('src/os/state.json', 'r', encoding='utf-8-sig').read()

assert '"tick": 2083,' in raw, 'tick anchor missing'
raw = raw.replace('"tick": 2083,', '"tick": 2084,', 1)

# ts + task
assert '"ts": "2026-10-12 23:40:21",' in raw, 'ts anchor missing'
raw = raw.replace('"ts": "2026-10-12 23:40:21",', '"ts": "%s",' % STAMP, 1)

old_task_marker = '"task": "收令轮·集团 ORDERS 四新行消费收口（group_scan ORDERS-NEW rows 333→337 tai'
assert old_task_marker in raw, 'task anchor missing'
new_task = LOG_LINE.split('R2084: ', 1)[1][:60]
raw = raw.replace(old_task_marker, '"task": "%s' % new_task, 1)

# focus: replace whole value between "focus": " and the closing " of that string.
i = raw.index('"focus": "') + len('"focus": "')
j = raw.index('"', i)
raw = raw[:i] + FOCUS_NEW + raw[j:]

# log append: last entry then closing "  ],"
tail_anchor = '\n  ],\n  "ts":'
idx = raw.index(tail_anchor)
raw = raw[:idx] + ',\n    ' + json.dumps(LOG_LINE, ensure_ascii=False) + raw[idx:]

# validate JSON
json.loads(raw)
io.open('src/os/state.json', 'w', encoding='utf-8', newline='').write(raw)
print('state.json OK: tick=2084 ts=%s' % STAMP)
