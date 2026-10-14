# -*- coding: utf-8 -*-
"""R2256 close: broken-round absorb accounting + finalize_state + explicit-file close commit + canonical export. UTF-8 (encoding law)."""
import os, sys, time, json, io

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'src', 'os'))
import close_commit as cc

NOW = time.strftime('%Y-%m-%d %H:%M:%S')
hm = time.strftime('%H:%M')[:4] + u'x'

# --- face 0: account_drift absorb bump (R2256 prior body timeout-killed 22:07:02, this body completes accounting) ---
SP = os.path.join(ROOT, 'src', 'os', 'state.json')
with io.open(SP, 'r', encoding='utf-8-sig') as f:
    st = json.load(f)
if st.get('account_drift_adjudicated') == 24:
    st['account_drift_adjudicated'] = 25
    st['account_drift_note'] = st.get('account_drift_note', '') + (
        u" R2256 2026-10-14: +1 broken-round beat absorbed (prior body started 21:42:01, killed by 25min round timeout at "
        u"22:07:02 - heartbeat line 'round timeout killed (age over 25min)'; working files M0-M2 render all on disk zero "
        u"loss; this body completed the accounting under the same round number per absorb convention). Baseline 24 -> 25. "
        u"Evidence: logs/iteration-loop/round_20261014_214201.out; heartbeat 22:07:02 line. Post-accounting verify: "
        u"beats 2277 expected vs tick 2256 + 25 = 2281 ceiling, in-band WARN.")
    tmp = SP + '.tmp'
    with io.open(tmp, 'w', encoding='utf-8', newline='') as f:
        f.write(json.dumps(st, ensure_ascii=False, indent=1) + '\n')
    os.replace(tmp, SP)
    print('ADJUDICATED 24->25 PATCHED')
else:
    print('ADJUDICATED SKIP (current=%r)' % st.get('account_drift_adjudicated'))

LOG = (
    u"2026-10-14 " + hm + u" R2256: 断轮吸收+生产轮·REACT-v19《城市速报 019·58 元咖啡一人一座之问》全链+F-187 登记"
    u"（前体 21:42 起 M0-M2 出图后 22:07 timeout kill〔心跳实锚·工作件全落盘零损失〕·本体同轮号承接=验图五检→M3/M4"
    u"→M4.5→E4 同轮回填→F 登记·R2224/R2235/R2237 吸收先例族）"
    u"——①轮首五查静（origin_gap QUIET ahead0 behind0+group_scan 六面全静：DECISIONS truly_new=0 水位 164+LEDGER @BigStream 5 行值守锚"
    u"+ORDERS worktree quiet 水位 403+ORIGIN-DELTA delta=8=rows 404-411 R2250 已消费同集维持+DIGEST-SUPPLY quiet v20 卡覆盖）"
    u"+树=MV-lane 预期脏面零锁（R1745 承继）；"
    u"②M2 验图五检 5/5（多模态转写逐字对照全中〔全图首读「官」字误读→放大裁剪复核定谳=逐字律执法·R2237「炫晕感」同型〕"
    u"·零重叠零越界零截断·AIGC 角标+底部两态声明行完整）+mp4 迁 renders 正位（1080×1080·30fps·3.40s=2.6 卡+0.8 tail 逐项吻合"
    u"·tech#158 迁档先例执法）；③M3 四禁零中+M4 四检过（258 万热度只入 README 记账·当事夫妻与店家零具名=公开报道面转述）；"
    u"④M4.5 七席=4×9+3 N/A=PASS 放行候选（评审单 review-20261014-mcreact-v19.md）——素材面=知乎 #2 258 万"
    u"（#4/#5 已消费同窗零重复·择优第十九证）+market_close 桶三轴位〔bucket 轮换律第二巡·求新轴池行字面含「咖啡」=池-题字面直配首例〕"
    u"+收束 C-00023 选题官信条（换锚机核=首选 C-00015 撞 REACT-v6 卡面 fleet 咬住当场换锚=零直撞标准第三证）；"
    u"⑤E4 参考仪同轮回填（fire_consume --cpu-lane rc0 PID 38704·probe 7.904 tok/s·实际 68s 落词=保守外推族）=8/10"
    u"（会停看+考虑保存转发·扣 2 指求新轴池行「街角的咖啡还香」=诗意空洞缺话题直接关联"
    u"·**字面直配≠关联可感反证数据点**=tech#171 五连旗族〔v15 侠气/v16 侠气/v17 怀旧/v18 收束信条/v19 求新轴〕）"
    u"·三面回填=评审单 E4 行+净本 20261014-222102-E4-audience.md+finished F-187 行；"
    u"⑥F-187 登记=成品库第 187 件·L-卡第 135 件（REACT 形态第十九件·四台账行+renders/station 双 S2 行落位·零顺延）；"
    u"⑦三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面+0 发现（renders 84 件全注账 unannot=0 收账复验）"
    u"/loop_health account-drift 21≤24 带内+adjudicated 24→25 bump=R2256 吸收注记（state-ts 收账即清）；"
    u"⑧例行件=10-14 日报在案不重跑·W42 周审在案·GB §④ 下期 10-15 跳过·export=canonical writer do 行刷（实况变化=F-187 成品）"
    u"·HQ-FEEDBACK 不写（零集团层新 open 问题）·T1 催办无超线项·tokens:local=1（E4 真飞 14b CPU 单调用=本地 ollama 零 API token·P-54⑤ 计量律）"
    u"·队列补货步=真无新种子如实注记（E4 读数并入 tech#171 既有观察位=消费面更新非新种·禁凑数）·临时件清理钩=r2256 助手件删净"
    u"——下轮=10-15 08:00 tech#92 锚例重判窗（zhihu 头部 ≥3 ≥60=PASS/fallback T1 60→55 递补·tech#159 工具）"
    u"+F-180 S1 拦截席留 GPU 窗+MV V3 终剪守望续（08:43 死线）+REACT-v20 按日热点窗候选"
)

FOCUS = (
    u"R2256 absorbed prior-body timeout-kill and closed F-187 REACT-v19 full-chain "
    u"(verify 5/5 incl char-level zoom ruling + M3/M4 + M4.5 4x9+3N/A + E4 cpu-lane 8/10 same-round backfill; "
    u"market_close bucket 2nd patrol, C-00023 closer swap-anchor after fleet conflict-catch; E4 flag=qiuxin line, "
    u"tech#171 five-flag family); NEXT: 10-15 08:00 tech#92 anchor re-judge window (zhihu head >=3 >=60, tech#159 tool) "
    u"+ F-180 S1 GPU window + MV V3 final-cut watch (08:43 deadline) + REACT-v20 daily hot window candidate."
)

DO = (
    u"R2256: F-187 REACT-v19 full-chain closed (broken-round absorb: prior body M0-M2 render killed 22:07, "
    u"this body verify+M3/M4/M4.5+E4 8/10 backfill+F-register; finished 187th, L-card 135th); "
    u"next: tech#92 anchor re-judge 10-15 08:00 + MV V3 final-cut watch + REACT-v20 daily window"
)

cc.finalize_state(LOG, ts=NOW, focus=FOCUS)

FILES = [
    u"src/os/state.json",
    u"state/queue/tech.md",
    u"docs/reviews/review-20261014-mcreact-v19.md",
    u"docs/reviews/expert-verdicts/20261014-222102-E4-audience.md",
    u"docs/reviews/station-reviews.md",
    u"output/finished.md",
    u"output/renders/README.md",
    u"data/storylines/cards/README.md",
    u"data/storylines/cards/MC-20261014-REACT-v19/cards.json",
    u"data/storylines/cards/MC-20261014-REACT-v19/subs.srt",
    u"data/storylines/cards/MC-20261014-REACT-v19/m1-assert-R2256.txt",
    u"data/storylines/cards/MC-20261014-REACT-v19/em-check-R2256.txt",
    u"data/storylines/cards/MC-20261014-REACT-v19/MC-20261014-REACT-v19.png",
    u"data/storylines/cards/MC-20261014-REACT-v19-tmp/build_v19.py",
    u"data/storylines/cards/MC-20261014-REACT-v19-tmp/e4-body.txt",
    u"data/storylines/cards/MC-20261014-REACT-v19-tmp/e4_call_cpu.py",
]
MSG = ("R2256 [via bm-a]: F-187 REACT-v19 full-chain closed (broken-round absorb: prior body M0-M2 render "
       "killed 22:07, this body verify 5/5 + M3/M4 + M4.5 desk-audit + E4 cpu-lane 8/10 same-round backfill; "
       "market_close bucket 2nd patrol, C-00023 closer swap-anchor; tech#171 five-flag note; adjudicated 24->25)")
rc, lines = cc.run_close_commit(FILES, MSG, export_do=DO, expect_tick=2256)
for ln in lines:
    print(ln.encode('ascii', 'replace').decode('ascii'))
print('CLOSE RC=%d' % rc)
