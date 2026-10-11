# -*- coding: utf-8 -*-
"""R2006 stage-2 close (single-writer law: finalize_state verbatim
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
    "2026-10-11 23:4x R2006: 生产轮·P2 队头消费=tech#114 交付（audio tmp 残留"
    "守卫+untracked 列表 exclude-standard 勘正·实活轮）——①轮首五查全静=own "
    "orders 顶 O-20260908-1105 mtime==R1733 锚零新令+origin_gap_check QUIET "
    "ahead0 behind0（R1500 前置位）+group_scan 四面全静（decisions truly_new=0 "
    "水位 141 维持+ledger @BigStream 5 行==值守锚零新转办+ORDERS 行水位 quiet "
    "rows=270 tail_key='10-11 13:4x'==R1979 基线〔tech#103 判据续窗过〕+HQ "
    "orders 14:00:46==R1978 消费锚）+无 index.lock+树态=MV sprint 会话域在飞件"
    "零接触（mv0001/mv001/drama_takt 批件零碰·R1745 承继）；②取活判读=P1 无 "
    "fire-ready 结转件（SC-005 六件+DIGEST v18 全收官 F-172..179·MD-0002 T2I "
    "gated CEO 点头=GPU 队列空）+10-12 窗三件均未到届日（tech#92 雷达标定权威"
    "窗 08:00+W42 周审+REACT-v15 热点窗全在明日）→P2 队头=tech#114 领做；③交付"
    "=loop_health 新 audio-tmp-residue 检测面（classify_audio_tmp_residue 纯核"
    "〔data/storylines/audio/*-tmp/ untracked ≥1=一 WARN·计数+帽 3+tech#60「+N "
    "more」折叠·cards 域出册待自案=scope law 预注册·反斜杠归一〕+check 接线〔例"
    "行探针消费即执法〕）——候选裁定=②机器守卫落地〔二次复发 R1895→R2005 按 CEO "
    "令 10-10 13:07「复发=闸失效即升格：检查单→脚本断言」执法·候选①检查单行=已"
    "失效形态不采纳·候选③现状维持=二次复发下不成立〕；④**随批真发现勘正="
    "_git_untracked_files 补 --exclude-standard**：守卫首跑假阳性当场抓获（8 件 "
    "sc001-01-v4-tmp amb-bed*.wav 全是 .gitignore:13 *.wav 忽略件·裸 ls-files "
    "--others 不应用 .gitignore 实锚）→tech#64 注记「respects .gitignore」错误"
    "声明双证收口（R1900 ignored *.pyc 被抓+本次 *.wav 被抓）·补参后 ignored 件"
    "=出账面永不算残留〔tech#64/#66/#114 三消费面语义归一·错账留痕：tech#64 "
    "boundary note 勘正注在册〕；⑤8 新测（AudioTmpResidueTests：锚形复现+scope "
    "law+单行帽折叠+反斜杠+git 失败/非 git 静默+真 git 夹具〔.gitignore 排除面"
    "锁〕+CLI WARN 不破 rc+真仓净基线冒烟）·**1118 全回归绿 122.6s SUITE_RC=0**"
    "（1110+8·run_suite 正法）·live dogfood 双读数=修复前假阳性 8 件点名→补参后"
    " findings 0+探针输出零新行（WARN 基线 256 持平）；⑥三探针=board 0 FAIL（5 "
    "题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 "
    "GATE 6/10+#17 needs-CEO）0 发现/loop_health 2F+256W 皆在案史实（两 outage "
    "09-26/09-28 已裁定不重触发·drift 18==adjudicated 基线带内）·证据 .c3-tmp/"
    "r2006_probes.txt+r2006_probes2.txt；⑦例行件=10-11 日报在案不重跑（一份为真"
    "相）·W42 周审+tech#92 权威窗+REACT-v15 热点窗均 10-12 届日即领不预扫·GB §④ "
    "v1.3 下期 10-15 跳过·meme V1 成片查看位零新到件（装配腿 bm-a 会话域在飞零"
    "接触）·MD-0002 T2I gated CEO 点头维持·export_ts R2003 22:02→本轮实况变化"
    "（守卫交付）=刷新合法（live current/do 行大白话纪律照 tech#74 常设面）·"
    "HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0（纯 CPU 面+探"
    "针只读零本地模型调用·P-54⑤ 计量律）·计分=实际文件改动 1 分（守卫工具+勘正"
    "件·无新成品实物）；⑧队列补货步=tech#115 真种子 1 条（cards 域 tmp 残留观察"
    "位=tech#114 scope law 姊妹面·判据先立=cards 线下件收官轮零 untracked 遗留零"
    "动作·复发 1 案=扩 domain 参一行）+tech#114 done 标日期回写；下轮=R2007 快速"
    "路径首查→10-12 窗三件届日即领序（tech#92 权威窗 08:00 判读→W42 周审→"
    "REACT-v15〔E4 发射器走 C-46 e4_launcher_gen=tech#113 判据兑现窗〕）+"
    "main#18 SC-005 二季再评后位候选。"
)

FOCUS = (
    "R2007 10-12 窗三件届日即领序（tech#92 雷达标定权威窗 08:00 判读〔zhihu-hot "
    "头部 ≥3 件 ≥60=selection-score 文本腿收口·FAIL=阈值分层腿递补〕+W42 周审补"
    "产+REACT-v15 热点窗〔E4 发射器走 C-46 e4_launcher_gen=tech#113 判据兑现窗"
    "·tech#115 cards 域收官轮并读〕）+main#18 SC-005 二季再评后位候选；GPU 队列"
    "=MD-0002 T2I gated CEO 点头=无 fire-ready 结转件"
)

summary = close_commit.finalize_state(
    log_line=LOG,
    tick=2006,
    focus=FOCUS,
    watermark_add=[],
    orders_watermark=None,
)
print("FINALIZE", summary)

rc, lines, _viol = export_refresh.refresh_export(
    os.path.join(REPO, "docs", "status-export.json"),
    patch={
        "live": {
            "current": "今晚给配音稿收尾加了自动防漏检查；雷达评分校准和热点新卡排明早八点窗。",
            "latest": "城市盘点第18张卡今晚入库（成品库第179件）。",
            "milestone": "明天早上8点后校准雷达评分门，并出当天的热点反应新卡。",
        }
    },
    do="给配音稿收尾加了自动防漏检查，半成品文件不会再散落在清单外；雷达评分校准和热点新卡排明早八点窗。",
)
for line in lines:
    print(line)
print("EXPORT_RC", rc)
if rc != 0:
    sys.exit(2)

FILES = [
    os.path.join("src", "os", "state.json"),
    os.path.join("docs", "status-export.json"),
    os.path.join(".c3-tmp", "r2006_stage1.py"),
]
rc, lines = close_commit.run_close_commit(
    FILES,
    "R2006 loop close: tech#114 consumed done (audio-tmp-residue guard "
    "live dogfood 0 findings, 1118 suite green); state tick 2006; "
    "export refresh [via bm-a]",
    root=REPO,
)
for line in lines:
    print(line)
print("CLOSE_RC", rc)
sys.exit(0 if rc == 0 else 1)
