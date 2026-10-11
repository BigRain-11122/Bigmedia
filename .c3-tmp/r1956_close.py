# -*- coding: utf-8 -*-
"""R1956 round close: state accounting + export live refresh + close commit.

O-20261009-1246 take-work round, two deliverables:
1) tech#92 A/B probe executed via 3 fire-card GO windows: v1 reading invalid
   (probe body-column discovery bug -> uniform L80 penalty 30s), v2 crash
   root-caused (PG left() server-side invalid-UTF8 in zhihu-hot body ->
   production node-pg tolerant = base scores on partially corrupted text),
   v3 channel-hardened valid reading: base 59/58/54/54/53 -> cand
   45/84/84/56/56, ge60 2/5 -> probe-level FAIL; authoritative judgment
   stays at the 10-12 08:00 production window; tech#94 seed logged.
2) explore#24 blade4 closed: CAC named-app enforcement anchor direct-captured
   (2026-04-28 jianying/maoxiang/jimeng AI, rectify+warn+personnel measures)
   + D-level "2026 revision" rumor re-debunked (single-source, false premise);
   R-20260927-04 v1.3.
"""
import os
import sys

sys.path[0] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "os"))

from close_commit import finalize_state, run_close_commit  # noqa: E402

LOG = ("2026-10-11 09:3x R1956: 等待窗取活轮·双活件交付（O-20261009-1246 取活·两段制收账=close 承载）——"
       "①轮首五查全静=own orders 顶 O-20260908-1105 mtime==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan（tech#50 正典）truly_new=0 水位 137 维持+wm_only=1（C-20261010-01 行内引用族）+ledger @BigStream 4 行==值守锚零新转办+HQ orders 02:06:39==R1935 消费锚零新行+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继）；三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现/loop_health 2F+241W 皆在案史实（两 outage=09-26/09-28 已裁定不重触发·round-debris r1953_score_ab_result.json=本轮 v1 探针自产物本 commit 收口）；"
       "②**tech#92 A/B 探针三连执行毕（fire 卡三连 GO 09:14-09:22 即发·R1952 turnkey 教训执法）**：〔v1〕r1953_score_ab.py 09:15:29 GO 即发→读数 cand 5/5 全 30 均一值→定谳=**探针读数无效**（探针 bug=body 列发现面 (\"content\",\"text\",\"body\",\"summary\") 全不中真 schema〔body_text/excerpt〕→恒喂「正文缺失」→候选 prompt L80「正文残缺→≤30」被模型忠实执行=方法论混淆非 prompt 质量 read·prompt L80 铁证 rg 定位）；〔v2〕修正探针 09:17:37 A-hot-resident GO 即发→psql 通道炸 invalid byte sequence 0xe5→二分隔离定谳=**left(a.body_text,400) 服务端文本函数校验炸**（zhihu-hot 分数头部行 body 前 400 字内含无效 UTF-8 字节·与客户端编码无关·length() 返整数幸存）+**生产 node-pg 容错替换符=base 分数 53-59 系部分损坏文本上算得=新数据质量面（tech#94 补货）**；〔v3〕通道加固版（原始列直取零 SQL 文本函数+逐行 OFFSET 取行+PGCLIENTENCODING=UTF8+Python 端 400 字截断 decode(replace) 容错=与生产同容错姿态）09:22:30 GO 即发→**有效读数：base 59/58/54/54/53 → cand 45/84/84/56/56=ge60 2/5 探针级 FAIL**（判据 ≥3/5）——锚例映射命中面=科技产品 58→84/医疗政策 54→84 两件 +26/+30 lift·文化讨论件 59→45 反降（锚例校准收紧面）·余两件 +2/+3 平移·通道 caveat=ollama run 原生 stdin 单体补全≠生产 /v1 chat 模板 system/user 分离=advisory 前读非判决——**权威判据维持 10-12 08:00 生产窗实测**（锚例版 R1953 已上线 worker）·zhihu-hot 头部 ≥3 件 ≥60 PASS=文本腿收口·FAIL=阈值分层腿递补照预注册；证据 .c3-tmp/r1956_score_ab_v3_result.json+三探针件+三 fire 卡；"
       "③**explore#24 刀④ 毕=全四刀齐 done**：**CAC 点名查处锚③正身全文直采**（2026-04-28《网信部门依法查处「剪映」App 等生成合成内容标识违法问题网站平台》中国网信网 A 级·剪映/猫箱/即梦AI·约谈/责令改正/警告/从严处理责任人=**执法阶梯第三级**〔2025-11-25 批量查处→2026-04-28 点名头部创作工具→2026-09-02 清朗平台扫〕+「从严处理责任人」=个人问责首现于标识专项+**创作工具 App 首次点名**=AI 视频创作产线 AIGC 烧录标识姿态站在执法正确侧·M4 标识门维持从严正面外证）+**D 级「2026 修订版」传闻官方源再证伪**（aisort 孤源·号称工信部 20260805·「2024 试行版」前提与事实不符〔正身=四部门 2025-03-07 联合印发 2025-09-01 施行〕·「罚年营收 5%」无官方支撑·官方源零命中·禁升格维持）+执法常态期三线并行结论（批量通报+点名查处+平台扫·无新法规/修订版·合规基座不变）——R-20260927-04 **v1.3 增版**（§10.4 更新+§十 头行四刀毕+应用表第 4 行收口+变更行）；"
       "④台账=tech.md tech#92 R1956 注记（三连执行实录+读数+caveat）+**tech#94 种子落队**（AIHOT body 无效 UTF-8 字节数据质量面：ingest sanitize/存量清洗/v3 通道法入运维 SOP 三候选·PoC ROI 诚实评估）+explore.md #24 done 标（四刀齐）+队列补货步=tech#94 一条真种子（A/B 通道定谳面真发现·tech#93 之外独立缺口锚）+当轮消费项 explore#24 done 标日期回写；"
       "⑤例行件=10-11 日报在案不重跑（R1927 00:2x 一份为真相）·W42 周审 10-12 未到·GB §④ v1.3 下期 10-15 跳过·#99 blocked-on-channel 维持（SLA ≤10-13）·meme V1 查看位零新到件（outbound 顶 15:41:53==R1899 锚·成片 mp4 未落=TTS/装配腿在飞·bm-a 会话域零接触）·MD-0002 下一腿 T2I 维持 gated tech#29（CEO 点头门）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·临时件清理钩=一次性诊断件五件删净（diag/bytes/ceverify/rawverify/bisect·发现已入 tech.md 注记）+探针证据件批量入账收口；tokens:local=10 本地生成调用（A/B 探针 v1 5+v3 5·qwen2.5:14b-8k 零计费端点零 API token·P-54⑤ 计量律·fire 卡内探针飞行=探针件 R1888 口径不计）——下轮=R1957 快速路径首查（tech#92 权威判据窗 10-12 08:00 届日即领〔zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〕+MD-0002 T2I〔gated tech#29〕+meme V1 成片查看位+W4 新盯位=CAC 2026Q4 新通报+清朗第三阶段）。")

FOCUS = ("R1957 tech#92 权威判据窗 10-12 08:00 届日即领（锚例版 selection-score 已上线 worker·zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〔探针前读 2/5·探针级 FAIL 已在案〕）+A/B 探针读数回填消费+MD-0002 T2I（gated tech#29 CEO 点头门）/装配 turnkey 已备+meme V1 成片查看位+tech#94 队头候选+W4 新盯位（CAC 2026Q4+清朗第三阶段）")

finalize_state(LOG, focus=FOCUS)

from export_refresh import refresh_export  # noqa: E402
LIVE = [
    "当前活：给雷达日报的打分标准做新旧对照测试（已跑完），并扫了 AI 标识监管新动态",
    "最近实物：打分对照读数（5 条头条 2 条上 60 分）+监管扫描增补版落档，2026-10-11 09:3x",
    "下个里程碑：明早 08:00 验证新打分标准能否让城市头条 ≥3 条过 60 分（2026-10-12）",
]
try:
    _rc, _lines, _viol = refresh_export("docs/status-export.json",
                                        patch={"live": LIVE})
    if _rc != 0:
        print("export refresh refused:", _viol)
    else:
        print("export refreshed ok")
except Exception as e:  # refresh failure is advisory, never fail close
    print("export refresh warn:", e)

FILES = [
    "docs/research/R-20260927-bigstream-04-aigc-labeling-recsys-weekly-scan.md",
    "state/queue/tech.md",
    "state/queue/explore.md",
    ".c3-tmp/r1953_score_ab_result.json",
    ".c3-tmp/r1956_ab_out.txt",
    ".c3-tmp/r1956_ab_err.txt",
    ".c3-tmp/r1956_ab_v2_out.txt",
    ".c3-tmp/r1956_ab_v2_err.txt",
    ".c3-tmp/r1956_ab_v3_out.txt",
    ".c3-tmp/r1956_ab_v3_err.txt",
    ".c3-tmp/r1956_score_ab_v2.py",
    ".c3-tmp/r1956_score_ab_v3.py",
    ".c3-tmp/r1956_score_ab_v3_result.json",
    "docs/status-export.json",
    "src/os/state.json",
]
MSG = ("R1956 tech#92 A/B probe 3-attempt: v1 invalid (body-column bug, uniform "
       "L80 30s), v2 PG left() invalid-UTF8 crash root-caused (production scores "
       "on corrupted text, tech#94 seed), v3 valid reading ge60 2/5 FAIL "
       "probe-level, authoritative window 10-12 08:00; explore#24 blade4 done: "
       "CAC named-app enforcement anchor 2026-04-28 + D-rumor re-debunked "
       "(R-20260927-04 v1.3) [via bm-a]")
rc, lines = run_close_commit(FILES, MSG)
for l in lines:
    print(l)
raise SystemExit(rc)
