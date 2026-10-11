# -*- coding: utf-8 -*-
"""R1957 round close: state accounting + export live refresh + close commit.

Round work: group naming serviced - BigStream #112 disk reduction plan
delivered (precise du attribution of the 33.0GB media tree) + first action
executed (9.2GB redundant post-import Qwen3.8-27B source GGUF purged;
ollama 27b-8k serving copy verified in registry; C: 558.7->567.8GB).
tech#94 done (v3-channel ops SOP into #112 note + tech#92 caveat).
tech#95 seed (bonsai 6.1GB owner-confirm candidate).
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "os")))

from close_commit import finalize_state, run_close_commit  # noqa: E402

LOG = ("2026-10-11 09:55 R1957: 生产轮·集团点名承接=BigStream #112 减负案呈报+首动执行（破静消费=ledger @BigStream 第 5 行〔夜班 L144+周进化轮 R3 L161 09:17「点名通道维持=owner 呈报待办」+「media 32.9GB 转办@BigStream 减负案内」〕→按认领制当轮交付）——"
       "①精确 du 归因落档（media 树 33.0GB=BigStream 仓 29.0GB 主燃面+MUSIC 3.2GB CEO 资产禁动+其他 0.04GB·仓内 data/assets 24.7GB 分解〔Qwen3.8-27B 源 9.2+CosyVoice3 6.3+bonsai 6.1+whisper-med 1.4+aihot-poc 1.6〕+output/renders 1.7GB 停点法冻结+storylines 0.43+sources 0.14）·证据 r1957_du_scan_out.txt；"
       "②减负案件=docs/disk-reduction-plan-20261011.md v1.0（三要素齐：可清中间件清单/大件归置候选表〔bonsai 6.1GB=拉取会话一句话确认候选·MUSIC 禁动·renders 停点冻结〕/装配批燃面三帽〔≤2GB/批中间件帽+模型源件即弃律+renders ≤200MB/周软帽=立法候选随窗落册〕）；"
       "③首动执行=Qwen3.8-27B 源 GGUF 9.2GB 删除（ollama 27b-8k 服务副本实读在册 ID 28aa6f37d3f3·Modelfile-27b-8k 配方 141B 保留=重导入配方在盘·重建通道 ModelScope ~3min·姊妹机「源 GGUF 已删」法同型）→C: free 558.7→567.8GB 双读实锚·-9.1GB 即得；"
       "④HQ-FEEDBACK F-20260909-02 RESOLVED 行追加（open→closed·点名通道「待 owner 呈报」→「已呈报+首动执行」·后续盘面照常规 15:07 复测读）；"
       "⑤tech#94 P2 队头交付=③臂正法收口（AIHOT PoC ROI 判读=①ingest sanitize/②存量 UPDATE 双臂判负留痕·v3 通道法入运维 SOP=backlog #112 [R1957 运维 SOP 注记]〔原始列直取+Python 端 400 字截断 decode(replace)+PGCLIENTENCODING=UTF8·禁 SQL left()/substr()〕+tech#92 判据窗读数 caveat 入档〔生产分数部分基于损坏替换文本=天花板分析新混淆面·探针 v3 同容错姿态=可比性保持〕·判据第二臂达成）；"
       "⑥三队盘点=main 全 gated/查看位（#9 续采=判据窗后·#12 gate 关·#13 SC-004-01 done F-171·#4 MD-0002 T2I gated tech#29 CEO 点头·#111/#115 查看位）+tech 顶=#92（10-12 08:00 权威窗届日即领）/#95 新种子（bonsai 6.1GB owner 确认）·#93 gated 真帧后·#94 done·explore 全 gated/到点未至；"
       "⑦焦点余位读数=tech#92 判据窗 10-12 08:00 届日即领不预扫+meme V1 查看位零新到件（15:41:53==R1899 锚·成片 mp4 未落=装配腿在飞维持）+MD-0002 剧本/配音/装配 turnkey 全备（T2I=tech#29 门）+W4 新盯位（CAC 2026Q4+清朗第三阶段）承继下窗；"
       "⑧轮首五查=own orders O-20260908-1105==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan decisions truly_new=0 水位 137 维持（wm_only=1 行内引用族）+ledger 破静源=第 5 行（本轮消费）+无 index.lock+树态=MV sprint 会话域在飞件零接触（R1745 承继·tech#26 撞面维持）；"
       "⑨三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现/loop_health 2F+241W 皆在案史实（两 outage=09-26/09-28 已裁定不重触发·drift 17==基线带内）；"
       "⑩例行件=10-11 日报在案不重跑（R1927 一份为真相）·W42 周审 10-12 未到·GB §④ v1.3 下期 10-15 跳过·export 刷新（live 三行大白话·减负案收口=CEO 可见面变化）·#99 blocked-on-channel 维持（SLA ≤10-13）·tokens:local=0（纯只读扫描+文件删除+档案读写零模型飞行·P-54⑤ 计量律）·临时件=r1957_du_scan 双件+close 脚本入账收口——下轮=R1958 快速路径首查（tech#92 权威判据窗 10-12 08:00 届日即领〔zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〕+meme V1 成片查看位+GPU fire 窗四腿判断）")

res = finalize_state(LOG)
print("finalize_state:", res)

from export_refresh import refresh_export  # noqa: E402
LIVE = [
    "盘面点名已收口：#112 减负案呈报集团并清掉 9.2GB 冗余模型源件（C 盘剩 567.8GB），等值守轮读账",
    "最近实物：docs/disk-reduction-plan-20261011.md（盘面归因+减负三帽）+9.2GB 回收，2026-10-11 09:5x",
    "下个里程碑：明日 08:00 雷达日报头部 ≥3 条过 60 分（评分调优收口）；MD-0002 画面等 CEO 批准后出片",
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
    "docs/disk-reduction-plan-20261011.md",
    "HQ-FEEDBACK.md",
    "state/queue/tech.md",
    "src/os/backlog.md",
    "docs/status-export.json",
    ".c3-tmp/r1957_du_scan.py",
    ".c3-tmp/r1957_du_scan_out.txt",
    ".c3-tmp/r1957_close.py",
    "src/os/state.json",
]
MSG = ("R1957 ledger L144/L161 naming serviced: #112 disk reduction plan delivered "
       "(du attribution media tree 33.0GB) + 9.2GB redundant post-import "
       "Qwen3.8-27B source GGUF purged (ollama 27b-8k copy verified, C: "
       "558.7->567.8GB), bonsai 6.1GB owner-confirm candidate, three burn caps "
       "proposed; tech#94 done (v3-channel ops SOP into #112 note, tech#92 "
       "caveat filed); tech#95 seed; next: 10-12 08:00 radar window verdict + "
       "MD-0002 T2I gated on CEO nod [via bm-a]")
rc, lines = run_close_commit(FILES, MSG)
for l in lines:
    print(l)
raise SystemExit(rc)
