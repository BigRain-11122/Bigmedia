# -*- coding: utf-8 -*-
"""R2007 stage-2 close (single-writer law: finalize_state verbatim
in-script literals + canonical export refresh + run_close_commit;
tech#76/#70/#81)."""
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "src", "os"))
sys.path.insert(0, os.path.join(REPO, "src"))

import close_commit  # noqa: E402
import export_refresh  # noqa: E402

LOG = (
    "2026-10-11 23:5x R2007: 生产轮·P1 队面消费=main#18 SC-005 二季续供升格回"
    "评+SC-005-07 拍稿预置毕（实活轮·计分=实际文件改动 1 分）——①轮首五查全静"
    "=origin_gap_check QUIET ahead0 behind0（R1500 前置位）+own orders 顶 "
    "O-20261008-1105 mtime==锚零新令+group_scan 四面全静（decisions truly_new=0 "
    "水位 141 维持+ledger @BigStream 5 行==值守锚零新转办+ORDERS 行水位 quiet "
    "rows=270 tail_key='10-11 13:4x'==R1979 基线〔tech#103 判据续窗过〕+HQ "
    "orders 14:00:46==R1978 消费锚）+无 index.lock+树态=MV sprint 会话域在飞件"
    "零接触（mv001/mv0001/drama_takt 批件零碰·R1745 承继）；②取活判读=P1 无 "
    "fire-ready 结转件（SC-005 六件+DIGEST v18 全收官 F-172..179·MD-0002 T2I "
    "gated CEO 点头=GPU 队列空）+10-12 窗三件未到届日（tech#92 权威窗 08:00+"
    "W42 周审+REACT-v15 全在明日）→main#18 可即领（CPU 面·R2006 指针后位候选）"
    "=本轮主活；③**main#18 升格回评执行毕**=B 池余 2 锚逐锚复跑（题眼级信条映"
    "射/未消费切面/载体避让三问+尾带基锚 E4 8.0x5→6.0→7.0 诚实并读·tech#109 "
    "部分回升未满带值判读承继）：**C-00012 沈佩兰→升 A**（弄堂晨操/老街坊=烟"
    "火人际 register·与 8.0x5 performer 族同带、异于尾带制度 register 弱读数"
    "族+口令「对齐——起步——」声音原生+沪语四词〔结棍/灵光/帮帮忙/侬说啥物"
    "事〕+信条「队形不能乱，人心更不能散」3x 年轮 verbatim+Q2 转折〔队散伙→"
    "挨家挨户请回→七人带到四十三人〕冲突-代价-修复三段全+载体避让三问 "
    "PASS〔音频形态空缺=CENSUS v3 一料多吃合法位/台词池零冲突 BigLife pools "
    "grep 实核/SC-005-04 sources 零引用〕）·**C-00023 潘志明→维持 B 判负留"
    "痕**（制度/编辑部 register=尾带 6.0/7.0 弱读数族风险面+Q2/Q3 场强次一"
    "档+红笔按得很重=视觉型钩子音频转译成本·重开条件预注册=SC-005-07 E4 ≥8.0 "
    "或新跨卡资产）——选型件 §7+变更记录 v1.2 落档；④**SC-005-07 沈佩兰拍稿 "
    "v1 三件套预置毕（二季首件·F-180 预指·fire-ready 结转）**=beats 13 拍 797 "
    "字（系列带内 04=864/05=835/06=841）+sources 溯源对表（C-00012 全字段 41 "
    "锚+CENSUS v3 图文卡避让+C-00010 相遇线留白+材料轴检验位 E4 判据预注册："
    "≥8.0=材料轴假设增强/潘志明重开半面·≤7.0=烟火 register 亦不保带值→系列续"
    "供重议）+s1-material（逐字内嵌+溯源对表+推演边界+尾格式锚）——机检 "
    "sc_beats_check CLI（tech#99 dogfood 第五用·--card 首接正主在册锚卡）"
    "**SC-CHECK GREEN rc0**：41 verbatim 锚零 MISS+inclusion 13/13+card_source "
    "MISS=NONE（2 对口播化形差=五十八岁/北外滩治理岸）+leak O-2026 零命中+M1 "
    "plain_language 0F9W（长句顾问带系列同型·06 件 7 WARN 对照）；⑤查看位例"
    "行=krea2 正典根零新到件（14:00:46 R1978 锚后）+meme V1 零新到件（bm-a 会话"
    "域在飞零接触维持）+盘面读 C: free 567.7GB（R1969 572.8 锚后日内 -5.1GB 常规"
    "磨耗带·#112 15:07 复测位 10-11 时点读补记）；⑥三探针=board 0 FAIL（5 题 "
    "10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面 0 发现/loop_health "
    "2F+257W（两 outage 在案史实不重触发·**WARN +1 vs R2006 基线 256**=新 1 条 "
    "heartbeat-gap 23:08→23:35 27min 长轮间隙=在案 dense-fold 家族〔R2005→"
    "R2006 轮间隔〕·drift 18==adjudicated 基线带内·基线勘正 256→257 如实入账）"
    "·证据 .c3-tmp/r2007_probes.txt；⑦例行件=10-11 日报在案不重跑（一份为真"
    "相）·W42 周审+tech#92 权威窗+REACT-v15 热点窗=10-12 届日即领不预扫·GB §④ "
    "v1.3 下期 10-15 跳过·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·"
    "tokens:local=0（纯 CPU 面+探针只读零本地模型调用·P-54⑤ 计量律）；⑧队列补"
    "货步=main#19 生产链行（SC-005-07 fire-ready 消费行·材料轴检验位挂行）+"
    "tech#116 观察位（SC-005-07 ASR 字位·沪语四词+口令族密度·tech#97/#102 同型"
    "第三案·随件收官轮并读）+main#18 done 标回写；下轮=R2008 快速路径首查→"
    "10-12 窗三件届日即领序（tech#92 权威窗 08:00 判读→W42 周审→REACT-v15〔E4 "
    "发射器走 C-46 e4_launcher_gen=tech#113 判据兑现〕）→SC-005-07 fire 窗消费"
    "后段位（F-180）。"
)

FOCUS = (
    "R2008 10-12 窗三件届日即领序（tech#92 雷达标定权威窗 08:00 判读〔zhihu-hot "
    "头部 ≥3 件 ≥60=selection-score 文本腿收口·FAIL=阈值分层腿递补〕+W42 周审"
    "补产+REACT-v15 热点窗〔E4 发射器走 C-46 e4_launcher_gen=tech#113 判据兑现"
    "窗·tech#115/#116 收官轮并读〕）→SC-005-07 沈佩兰 fire 窗消费后段位（F-180 "
    "预指·三件套 fire-ready·材料轴检验位 E4 判据）；GPU 队列=MD-0002 T2I gated "
    "CEO 点头"
)

summary = close_commit.finalize_state(
    log_line=LOG,
    tick=2007,
    focus=FOCUS,
    watermark_add=[],
    orders_watermark=None,
)
print("FINALIZE", summary)

rc, lines, _viol = export_refresh.refresh_export(
    os.path.join(REPO, "docs", "status-export.json"),
    patch={
        "live": {
            "current": "今晚定了口述史第二季的第一位人物：晨操领队沈阿姨（讲她把散了的队伍一家一家请回来），拍稿、来源核对、评审材料三件已备好，等显卡空窗就能出成品；选题评估报告同步归档。",
            "latest": "SC-005-07 沈佩兰拍稿三件套预置（拍稿+溯源+评审材料·2026-10-11 23:5x·待 GPU 窗出成品 F-180）",
            "milestone": "明早八点后跑三件事：雷达评分校准判读、周审补产、当天热点反应新卡；口述史新篇随后等显卡空窗出成品（48h 内）。",
        }
    },
    do="完成口述史第二季首件选角评估（沈佩兰入选、潘志明暂缓留档）并把新篇拍稿三件套全部预置完毕，等显卡空窗出成品。",
)
for line in lines:
    print(line)
print("EXPORT_RC", rc)
if rc != 0:
    sys.exit(2)

FILES = [
    os.path.join("src", "os", "state.json"),
    os.path.join("docs", "status-export.json"),
    os.path.join(".c3-tmp", "r2007_probes.txt"),
]
rc, lines = close_commit.run_close_commit(
    FILES,
    "R2007 loop close: main#18 consumed (C-00012 promoted, SC-005-07 beats "
    "prestage 41 anchors GREEN fire-ready F-180; C-00023 held at B "
    "preregistered); state tick 2007; export refresh [via bm-a]",
    root=REPO,
)
for line in lines:
    print(line)
print("CLOSE_RC", rc)
sys.exit(0 if rc == 0 else 1)
