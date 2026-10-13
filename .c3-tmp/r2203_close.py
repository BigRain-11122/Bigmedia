# -*- coding: utf-8 -*-
"""R2203 close: orders 380-381 + C-20261013-01 ack, tech#126 pre-window
smoke read annotated, fire mv-active carried, export refreshed (tech#148),
r2202 export-patch debris rides manifest (cleanup hook)."""
import sys, os

sys.path.insert(0, os.path.join("src", "os"))
import close_commit as cc
import group_scan

LOG = ("2026-10-13 23:1x R2203: 收令轮+tech#126 窗前抽读毕（夜窗提前开态·R2202 后 ~30min）"
       "——①五查破静=group_scan fresh 23:03 检出 ORDERS rows 379→381+DECISIONS truly_new=1"
       "（其余面静：own orders 锚 O-20260908-1105 维持+origin_gap_check QUIET ahead0 behind0+"
       "LEDGER @BigStream 5 行值守锚零新转办+DIGEST-SUPPLY advisory 1 row-date 10-13 已裁决面维持"
       "〔F-182 staged+夜窗 DIGEST-v20 产线覆盖〕+ORDERS-ORIGIN-DELTA delta=0）："
       "row 380=CEO 云端放开令 O-20261013-2245（原话「全部项目继续开工，全力运转，云端放开，但不要浪费」"
       "·10-12 资源总纲「云端为否」默认位废止·浪费纪律全保留〔>500 积分闸+意义门四闸+token 台账〕"
       "·V3 全本地验证令不翻案·满载执行图 bm-a CPU 腿〔音源批→whisper 锚点→词面校准 W1-W3〕"
       "已由 MV 主窗 23:2x 词面校准 v1 收口行自执·video-remix 首批 S 池试产 GO=委员会代决 bm-b lane）"
       "=本司承接=云道解禁知悉+推理面全本地在册〔edge-tts/faster-whisper/Ollama/FFmpeg〕"
       "无操作变化零新立法+row 381=C-20261013-01 ② 导演席回执（正典层恢复定谳·MV 域自执件）"
       "+23:2x inline 行=词面校准批 v1 收口（MV 主窗）=查看位零接触承 R1745·"
       "ack=本行+commit 含行号 380/381+R2203+下一动作（P-51 双载体）；"
       "②DECISIONS C-20261013-01 集团工作区清理与git卫生收口（委员会 executed·五条=安全层 45 件删除收口/"
       "正典层 53 件点名导演席窗自决〔row 381 已回执〕/full_mv_v2 171.7MB gitignore 防线/"
       "orders-decisions >1MB 专项监控线/labbench 14GB gitignored 合规不清+CODELY 精简 254→160KB 快照）"
       "=过审 ack·本司 media/BigStream 无点名份额零动作·dnums 水位 154→155（watermark_add）；"
       "③本轮取活=tech#126 窗前抽读腿毕（psql 直读·R1957 编码 SOP）=R2202 requeue 32 池 sweep 后 "
       "22:35-23:0x 读数：score_article completed=16 笔〔≥3 判据臂 PASS〕+prompt_version 全量带 "
       "selection-score@a41b9a736d 城市校准版〔27 analyses=锚例注入生效实证〕+城市源新评分 12 件"
       "（knowledge 7/max31·bilibili-tech 5/max13）·≥60=0〔样本尚薄·权威窗 10-14 08:00 compose 照 "
       "tech#92 预注册判据：zhihu-hot 头部 ≥3 篇 ≥60=文本腿收口/否则阈值分层 fallback T1 60→55〕"
       "+prefilter failed 1096 新池快进争抢族注记〔不 re-requeue·R1800 先例〕+pgboss created 362 在吃"
       "=队列在磨——注记落 tech.md 队列行；④fire_consume --ledger 正身直发=no-fire rc1 "
       "reason=card-no-fire: mv-active（23:05:34 收据·mv_sprint_probe newest_age 25.1min="
       "MV sprint 会话域在执正确让位）→F-180 SC-005-07 flight-4+F-181 REACT-v15+F-182 DIGEST-v19+"
       "F-183 REACT-v16 四件 fire-ready carried·真窗=mv 静（fire_window_card 唯一仲裁面）"
       "+DIGEST-v20 产线同候让位；⑤三探针带内=board 0 FAIL（5 题 10 稿 5 in production）/"
       "readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）+1 发现 react-v16 "
       "unannot=F-183 夜窗登记即清（R2118 裁定维持）/loop_health 3F+291W 皆在案史实"
       "（三 outage 窗=pause-让路窗族+drift 18≤21 adjudicated·WARN +1=稠窗折叠带内）；"
       "⑥例行件=10-13 日报在案不重跑（R2086 一份为真相）·W42 周审在案（R2011）·GB §④ 下期 10-15 ≤7d "
       "跳过+export=实况变化（收令+夜窗态+冒烟读数）走 tech#148 正身刷新（do+live 三行·export_ts 本轮戳）"
       "·HQ-FEEDBACK 不写（row 380-381=MV 域自执件+集团已裁件·零集团层新 open 问题零膨胀）"
       "·T1 催办无超线项（账号物理件=呈现状行不催办）·tokens:local=0（探针/psql 直读/fire 卡读="
       "档案与库表读写零本地模型产出调用·P-54⑤ 计量律）；⑦队列补货步=真无独立新种子如实注记零膨胀"
       "（本轮读数=tech#126 既有件证据面·group 余面静·禁凑数律）·临时件清理钩=r2203_orders_tail/"
       "r2203_c01/r2203_t126/r2203_t126b/r2203_t126_smoke.py/.json 六件轮末删净+"
       "r2202_export_patch.json 残留=本循环前轮 debris 随 manifest 入账收口（tech#81 同族）"
       "——下轮=MV 让位即 fire 接力（F-180~183+DIGEST-v20 产线）+10-14 08:00 tech#92/#126 "
       "权威窗读数+晨窗 08:00 回滚序（re-enable MiniGameOllama 双任务）")

FOCUS = ("MV-yield fire relay (F-180~183 + DIGEST-v20 line) + 10-14 08:00 tech#92/#126 "
         "authoritative window read + morning rollback (re-enable MiniGameOllama tasks)")

EXPORT_PATCH = {
    "do": ("R2203 收令轮：CEO 云端放开令 O-20261013-2245 知悉（本司推理面全本地在册·L 卡产线按 fire 卡仲裁）；"
           "决策 C-20261013-01 过审 ack；tech#126 校准冒烟窗前抽读毕（score 回执 16 笔·城市校准版在役）；"
           "fire 四件候 MV sprint 让位。"),
    "live": [
        "当前活：夜窗已提前开（CEO 下班令 21:0x）：AI 日报 Worker 复役+重排池在磨+校准冒烟抽读毕；L 卡四件 fire 候 MV sprint 让位。",
        "最近实物：城市盘点 019（10-12）；本轮=ORDERS 380-381+决策 C-20261013-01 消费收口+tech#126 冒烟证据（10-13 23:0x）。",
        "下个里程碑：10-14 08:00 tech#92/#126 权威窗读数（城市源 ≥60 判据）；MV 让位后 F-180~183 fire 接力（窗 ≤10-15）。",
    ],
}

MESSAGE = ("R2203: consume ORDERS 380-381 + decision C-20261013-01 (CEO cloud-open order "
           "O-20261013-2245 ack, no named BS share, MV receipts view-only); tech#126 "
           "pre-window smoke read: score_article completed=16 (>=3 arm PASS), city "
           "calibration a41b9a736d active, city >=60=0 thin sample, authoritative window "
           "10-14 08:00; fire no-fire rc1 mv-active (F-180~183 carried); export refreshed "
           "via canonical writer; next: MV-yield fire relay + 08:00 window + morning "
           "rollback [via bm-a]")

FILES = ["src/os/state.json", "state/queue/tech.md",
         "data/pipeline/fire-consume-ledger.jsonl",
         ".c3-tmp/r2202_export_patch.json"]

sumry = cc.finalize_state(LOG, ts="2026-10-13 23:11:00", focus=FOCUS,
                          watermark_add=["C-20261013-01"],
                          orders_watermark=group_scan.current_orders_watermark())
print("finalize:", sumry)

rc, lines = cc.run_close_commit(FILES, MESSAGE, export_patch=EXPORT_PATCH)
for l in lines:
    print(l)
print("close rc:", rc)
sys.exit(rc)
