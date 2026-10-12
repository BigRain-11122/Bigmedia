# -*- coding: utf-8 -*-
"""R2085 close: deadline-watch + tech#140 dead-round pickup + main#22 done.
Orders row 337->338 consumed (CLOUDWAVE-2 = MV session own line, watch-only)."""
import io, json, re, datetime

STAMP = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

LOG_LINE = (
    "2026-10-13 00:1x R2085: 死线窗值守轮+断轮承接收口（O-2305 成片死线 10-13 08:30+O-2330 榨干令在执·MV CEO 优先线独占·R2084 承接）——"
    "①轮首五查=origin_gap_check QUIET（ahead0 behind0）+group_scan 六面（decisions truly_new=0 水位 152 维持"
    "+ledger @BigStream 5 行==值守锚+**ORDERS rows 337→338 新行 1 件=CLOUDWAVE-2 云端双波实录**"
    "〔O-2305 执行件·CDN 索引族既定消费面·MV 会话自身进度行〕查看位零接触消费+水位 338 落账"
    "+DIGEST-SUPPLY quiet+ORIGIN-DELTA quiet）+树态=MV sprint 会话域在飞件+tech#140 断轮遗留"
    "（R2080 窗 22:03-22:12 写盘未提交·全族零接触让路律）+无 index.lock；"
    "②死线窗轻扫三面=release/ 无 234s 成片（最新=样片v2 10-08）+**comfy queue 0/0=KF 批烧毕**"
    "（R2084 running=1 对照·VRAM 10.3GB 驻留态）+cloudv2 波 12.6min 新鲜在落（INT5_head_bow 23:42 落）"
    "→收口判据未达·撤旗+worker-restart main#21+F-180/181/182 fire 接力顺延维持"
    "（mv probe active 19.9min=CEO 优先线让路正确侧）；"
    "③**tech#140 断轮承接收口**（R155/R459/R804 先例·fire card 14b 载类可行性面缺口）="
    "evaluate_load_class 纯核+classify_fire 保守单向集成（mv-yield 路径永不触面=yield reason 支配设计）"
    "+readings.load_class 字段入卡（fire_consume ledger verdict 面=tech#136/138 同型）+--load-class-mb CLI"
    "+**tests 47 全绿**（双路径 demoted reason 断言回归锁）+**活体首读** .c3-tmp/r2085_t140_card.json"
    "（Krea2 驻留窗 free 1988<required 8704→readings.load_class ok=false 真窗在位·verdict no-fire 零误 GO 达成"
    "·probe skipped-not-resident 零冷载=O-2305 MV 优先窗安全合规）——reason 面 mv-quiet 变体"
    "=收口后 fire 接力窗并读一行即闭环（hermetic 锁已先证）；"
    "④**main#22 done**=00:00 常务轮窗后复读（bill mtime 09:33:59→00:07:33 变更捕获）+§七 实读="
    "**00:1x 常务轮交卷落（15:07 值守班缺交·本班补位）·Phase 0 ①②③ 三件齐**（登记簿 v1 全表 53 件实测"
    "+节律对账表+痛点总账·双指针=§七 本节+decisions D-20261013-02 行·判据 1 消费面达成）"
    "→「落=标 done」分支命中=本项收口（HQ-FEEDBACK 呈报位零触发零膨胀）；"
    "⑤三探针带内=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面"
    "（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现（78 renders unannot=0）"
    "/loop_health 3F+281W 皆在案史实（account-drift 18≤adjudicated 基线 21）；"
    "⑥例行件=10-12 日报+W42 周审在案不重跑+GB §④ v1.3 下期 10-15 ≤7d 跳过"
    "+export_ts 23:25 <24h 零 CEO 可见成品态变化节流不刷（tech#140=引擎内部件非成品件）"
    "+T1 催办无超线项+HQ-FEEDBACK 不写+tokens:local=0（探针/直读零本地模型产出调用·P-54⑤ 计量律）；"
    "⑦队列补货步=本轮种子已消费（tech#140 收口位=R2080 交付面补完+main#22 判据窗位）"
    "·真无独立新种子如实注记零膨胀+临时件钩=card 读数件+close 脚本随 commit 入账"
    "——下轮=R2086 死线窗值守续（成片呈报轻扫先行→收口判据达成即撤旗+worker-restart main#21"
    "+F-180/181/182 fire 接力）+D-20261013-02 新 dnum group_scan 差集消费"
    "+main#27 死线守望 08:30 收口判读三连+tech#92 权威窗 08:00 顺延律随行"
)

FOCUS_NEW = (
    "死线窗值守续（O-2305 成片死线 10-13 08:30+O-2330 榨干令四线在执·MV CEO 优先线独占）"
    "→成片呈报轻扫先行（R2085 读数=release/ 无 234s 成片·comfy queue 0/0 KF 批烧毕"
    "·cloudv2 波在落）→收口判据达成即撤旗（AIHOT pause 旗）+worker-restart main#21"
    "+F-180/181/182 fire 接力；main#27 死线守望 08:30 收口判读三连；tech#92 权威窗 10-13 08:00 顺延律随行；"
    "D-20261013-02 新 dnum=R2086 group_scan 差集既定消费面"
)

# ---------- state.json ----------
raw = io.open('src/os/state.json', 'r', encoding='utf-8-sig').read()

assert '"tick": 2084,' in raw, 'tick anchor missing'
raw = raw.replace('"tick": 2084,', '"tick": 2085,', 1)

assert '"ts": "2026-10-12 23:46:26",' in raw, 'ts anchor missing'
raw = raw.replace('"ts": "2026-10-12 23:46:26",', '"ts": "%s",' % STAMP, 1)

# task: full old value is exactly the 60-char prefix of R2084's log body
old_task = '死线窗值守轮（O-2305 成片死线 10-13 08:30+O-2330 榨干令四线在执·MV CEO 优先线独占·R'
assert ('"task": "%s"' % old_task) in raw, 'task anchor missing'
new_task = LOG_LINE.split('R2085: ', 1)[1][:60]
raw = raw.replace('"task": "%s"' % old_task, '"task": "%s"' % new_task, 1)

# orders_row_watermark 337 -> 338 (CLOUDWAVE-2 line consumed watch-only)
wm_pat = re.compile(r'("orders_row_watermark": \{\s*"rows": )337(,\s*"tail_key": )"10-12 23:3x"')
assert wm_pat.search(raw), 'orders wm anchor missing'
raw = wm_pat.sub(lambda m: '%s338%s"10-12 23:5x"' % (m.group(1), m.group(2)), raw, count=1)

# focus: replace whole value
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
print('state.json OK: tick=2085 ts=%s' % STAMP)
