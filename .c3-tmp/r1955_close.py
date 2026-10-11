# -*- coding: utf-8 -*-
"""R1955 round close: state accounting + export live refresh + close commit.

O-20261009-1246 take-work round: MD-0002 assembly-leg turnkey delivered
(gen-assemble-v1.py, placeholder-mode CPU validation PASS 72.77s in the
drama-ep [60,90] window, 13-cue SRT, AIGC mark + close declaration
frame-verified). tech#93 seed logged (drama S2 beats-contract adapter).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src", "os"))
# actually .c3-tmp sits at repo root -> src/os
sys.path[0] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "os"))

from close_commit import finalize_state, run_close_commit  # noqa: E402

LOG = ("2026-10-11 09:0x R1955: 生产轮·MD-0002 装配腿 turnkey 预置交付（O-20261009-1246 取活·main#4 CPU 面·两段制收账=close 承载）——"
       "①轮首五查全静=own orders 顶 O-20260908-1105 mtime==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）+group_scan（tech#50 正典）truly_new=0 水位 137 维持+wm_only=1（C-20261010-01 行内引用族）+ledger @BigStream 4 行==值守锚零新转办+HQ orders 02:06:39==R1935 消费锚零新行+无 index.lock+树态=MV sprint 会话域在飞件（mv0001/mv001/whisper v3/drama_takt）零接触（R1745 承继）；"
       "②三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现（78 renders 全注账 unannot=0）/loop_health 2F+240W 皆在案史实（两 outage=09-26/09-28 已裁定不重触发·drift 17==基线带内）；"
       "③焦点面读数=tech#92 判据窗 10-12 08:00 未到届日即领不预扫+A/B 探针 GPU 窗发射位=fire_window_card 单命令 no-fire（08:53:56 卡：gate 静态双闸败 worst-case free 594MB<2048 守卫·mv quiet 557.9min·probe face=ok evictable=0 counterfactual=None·readings-age tech#90 在役）→r1953_score_ab.py 维持 GPU 窗 gated+meme V1 查看位零新到件（outbound 顶=PREPRO-V1.md 21:08:17==R1911 锚·成片 mp4 未落=装配腿在飞维持·bm-a 会话域零接触）；"
       "④**交付=MD-0002 装配腿 turnkey 预置件**（main#4 CPU 面可执行项·T2I=tech#29 门 gated 不抢跑→装配 turnkey 先行=R1870 预置范式）：gen-assemble-v1.py=drama-ep 律装配器（tech#7 LAW_PROFILES 承继=场景切割 gap 1.2s 底+0.3s 种子抖动 seed 7306+尾持 1.5s→总长 72.77s∈[60,90] **PASS**〔55.53 speech+14.81 gaps+1.5 tail·窗 FAIL 有牙 exit 1〕）+--placeholder 占位帧模式（PIL 卡·T2I 落地即同一条命令换真帧零改·默认消费 frames/shotNN.png）+字幕 13 cue edge-tts 文本精确直出（MD-0002-v1.srt 落件·R1943 正法）+AIGC 常驻角标（[AIGC·AI 生成内容] white@0.9=D-BS-03 §4.5 机械方括号体·drawtext textfile 正法=_q() 转义对齐 render_card_video 在案先例）+close 推演声明 verbatim（shot13 字幕承载·帧验过）——**占位帧 CPU 全链实跑验证**：72.78s 渲染毕（13 zoompan 段+concat+drawtext 终pass+音轨 apad gap 求解 concat 全链 rc=0）+帧验三面过（cue2 t=5s 字幕「造城令…」+角标 ✓/cue13 t=68.5s 推演声明+角标 ✓/占位卡渲染 ✓·首探 t=2.4s 落 cue 间隙无字幕=字幕窗逻辑正确·证据 .c3-tmp/r1955_probe_{sub,cue2,cue13}.jpg 三件入账+mid/end 两件冗余删净〔临时件清理钩〕）+报告 assemble-validate-v1.txt 落件——**T2I 门后一条命令出片**：python data/storylines/drama/md0002/gen-assemble-v1.py；"
       "⑤台账=md0002 README 生产记录 R1955 节+queue main#4 R1955 注+tech#93 补货（MD-0002 真帧 S2 三门跑面真发现：ai_feel_check 消费 BS beats 契约〔parse_beats PROFILE|card|spoken 九词表〕vs 漫剧 scene+speaker 结构=beats-sidecar 适配候选〔speaker→profile 诚实映射注记〕·gated T2I 真帧重渲后）+export live 刷新（装配 turnkey=实况变化·tech#74 大白话纪律经 export_refresh 正典写入器）；"
       "⑥例行件=10-11 日报在案不重跑（R1927 00:2x 一份为真相）·W42 周审 10-12 未到·GB §④ v1.3 下期 10-15 跳过·#99 blocked-on-channel 维持（SLA ≤10-13）·HQ-FEEDBACK 不写（零集团层新 open 问题零膨胀）·tokens:local=0（纯 CPU 装配+edge-tts 零计费端点+零本地模型调用·P-54⑤ 计量律）——下轮=R1956 快速路径首查（tech#92 判据窗 10-12 08:00 届日即领〔锚例版已上线·zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补〕+A/B 探针 GPU 窗发射位随轮 fire 卡判断+MD-0002 T2I〔gated tech#29〕/meme V1 成片查看位+explore#24 刀④ 承继〔≤10-17 窗〕）")

FOCUS = ("R1956 tech#92 判据窗 10-12 08:00 届日即领（锚例版 selection-score 已上线·zhihu-hot 头部 ≥3 件 ≥60=文本腿收口·FAIL=阈值分层腿递补）+A/B 探针 GPU 窗发射位（r1953_score_ab.py 已入库·fire 卡随轮判断）+MD-0002 下一腿（T2I=tech#29 门〔CEO 点头+GPU 窗〕/装配 turnkey 已备〔frames 落地即出片〕）+explore#24 刀④ 承继+meme V1 成片查看位随轮")

finalize_state(LOG, focus=FOCUS)

from export_refresh import refresh_export  # noqa: E402
LIVE = [
    "MD-0002 第二集漫剧装配骨架已搭好并试跑通过，画面等批准后一条命令出片",
    "最近实物：MD-0002 装配试跑样片（占位画面 72.8 秒）+13 段配音，2026-10-11 09:0x",
    "下个里程碑：明日 08:00 雷达日报头部 ≥3 条过 60 分（评分调优收口）；第二集等 CEO 批准画面",
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
    "data/storylines/drama/md0002/gen-assemble-v1.py",
    "data/storylines/drama/md0002/MD-0002-v1.srt",
    "data/storylines/drama/md0002/assemble-validate-v1.txt",
    "data/storylines/drama/md0002/README.md",
    "state/queue/main.md",
    "state/queue/tech.md",
    "docs/status-export.json",
    ".c3-tmp/r1955_probe_sub.jpg",
    ".c3-tmp/r1955_probe_cue2.jpg",
    ".c3-tmp/r1955_probe_cue13.jpg",
    "src/os/state.json",
]
MSG = ("R1955 MD-0002 assembly-leg turnkey: gen-assemble-v1 drama-ep gap solver "
       "(72.77s in [60,90] PASS), 13-cue SRT, AIGC mark + close declaration, "
       "placeholder-mode CPU validation frame-verified; tech#93 seed; live export "
       "refresh [via bm-a]")
rc, lines = run_close_commit(FILES, MSG)
for l in lines:
    print(l)
raise SystemExit(rc)
