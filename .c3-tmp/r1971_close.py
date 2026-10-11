# -*- coding: utf-8 -*-
# R1971 close: canonical finalize_state (tech#76 single writer) + export chips
# refresh (tech#70 canonical writer) + run_close_commit (tech#81 self-include).
import io
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)
sys.path.insert(0, os.path.join(BASE, 'src', 'os'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import close_commit as cc  # noqa: E402

# ---- segment 1: deliverables commit (P-51 carriers: order ref + round + next action)
SEG1_FILES = [
    os.path.join('src', 'render', 'sc_beats_check.py'),
    os.path.join('tests', 'test_sc_beats_check.py'),
    os.path.join('state', 'queue', 'tech.md'),
    os.path.join('state', 'queue', 'main.md'),
    os.path.join('src', 'os', 'backlog.md'),
    os.path.join('.c3-tmp', 'r1971_sc_dogfood.py'),
    os.path.join('.c3-tmp', 'r1971_sc_check_evidence.txt'),
]
MSG1 = ("R1971 delivery: tech#96/#99 canonical SC beats check CLI src/render/sc_beats_check.py "
        "(5 faces format/anchors/material-inclusion/card-cross/leak-guard; 22 new tests; 999 suite green; "
        "SC-005-05 dogfood parity vs r1970 ad-hoc readouts); ack HQ orders 11:3x fullmv-fix-20261011 "
        "sprint order via backlog #111 view-position (CEO-FEEDBACK-fullmv-fix-20261011.md verified in "
        "place; MV session executes; loop zero-touch); next: SC-005-04 F-176 on next fire window + radar caliper 10-12 08:00 [via bm-a]")
rc1, lines1 = cc.run_close_commit(SEG1_FILES, MSG1)
for ln in lines1:
    print('SEG1:', ln)
print('SEG1 rc=%d' % rc1)

logline = ("2026-10-11 12:5x R1971: 生产轮·HQ orders 11:3x「mv0001 全曲整改冲刺令 @BigStream」查看位消费+tech#96/#99 正典机检 CLI 交付"
"（O-20261009-1246 取活·fire 卡 no-fire MV 优先线让路·两段制收账=close 承载）——"
"①轮首五查=own orders 顶 O-20260908-1105 mtime 12:08:14==R1733 锚零新令+origin_gap_check QUIET ahead0 behind0（R1500 前置位）"
"+group_scan（tech#50 正典）decisions truly_new=0 水位 141 维持+ledger @BigStream 5 行==R1957 消费锚零新转办"
"+**HQ orders 破静=新行 11:3x「mv0001 全曲整改冲刺令 @BigStream」**（CEO 原话「有点意思了…准备出完整的MV成片，一定要把故事写好！！！！！！"
"逻辑通顺！！！！自然！！！立意高！！！！」=30s 预览方向获认可+六项整改+全曲冲刺+剧本四令）——查看位消费=正典件 "
"CEO-FEEDBACK-fullmv-fix-20261011.md 实读在位（cph4/fleet/mv0001-handover/outbound/krea2/30s-reel-v1/·12:01:31 落·晚于 R1906 锚 20:03=新到件："
"六项整改参数级表〔①掉帧=实测非真掉帧·变速无插值根因→minterpolate 修法/②瑕疵=帧级六检升格/③调色=v5 深研对标 2001 胶转磁/④剪辑=whisper 词级重核切点落拍/"
"⑤运镜动作=三维语言+动作物理链/⑥故事=剧本 v5 全曲重写〕+剧本 v5 四令〔六轴/因果链闭合/留白自然/原版记忆点升华〕+执行分工序列〔深研波→盲评十席→CEO 定版→KF/i2v 重摇→装配 v5→成片呈 CEO〕"
"+验收线六条全在册）+执行实况互证=fire 卡 mv-active 43min（MV sprint 会话在执=CEO 优先线正确侧）→ack=backlog #111 R1971 查看位注+commit 含令引用（P-51 双载体）·MV 会话域零接触 R1745 承继；"
"②fire_window_card 单命令四腿判断=no-fire（12:45:38 卡：mv-active 43min·gate 静态双闸败 worst-case free 433MB<2048 守卫+util 99>80·probe busy-contended·readings-age tech#90 在役）"
"→SC-005-04/05 双件 fire-ready 维持结转（F-176/F-177 双预指·下个 fire 窗 S1 连发·R1964/R1965 单轮全链同型）；"
"③tech#96/#99 双项交付=**src/render/sc_beats_check.py 单一真相 CLI**（as-built 名偏离候选名 verbatim_check.py 如实注：五校验位=format〔九词表+3 列+去标点字数〕"
"/anchors〔--anchors 数据文件制·#注释行跳过〕/material inclusion〔tech#96〕/card cross〔--card+--card-anchors `beats_form||card_form` 对文件制·裸行=双面同形〕"
"/leak guard〔--leak 可重复·脱敏组合守卫〕·rc 0/1/2〔format 坏=rc2 响亮=same_text_check BAD-BEATS-ROW 同律〕+--out 证据件 UTF-8 无 BOM）"
"+22 新测〔tests/test_sc_beats_check.py〕+**999 全回归绿 125.9s SUITE_RC=0**（977+22·run_suite 正法·零漂移）"
"+**真跑 dogfood parity=SC-005-05 全件**（r1970 ad-hoc 锚 38+card_pairs 34+leak 2 经 ast 提取喂 CLI：rows=13/spoken_nchars=835/verbatim_anchors=38 MISS=NONE/"
"inclusion 13/13 bad=NONE/card_source_MISS=NONE/leak_face_hits=NONE/SC-CHECK GREEN rc0=与 R1970 手检逐面一致·证据 .c3-tmp/r1971_sc_check_evidence.txt）"
"→八代 ad-hoc 复制线 r1874→r1970 收口（tech#87/tech#91 wrapper 世代收口线第三件同族）·判据兑现窗=SC-005-04/05 收官轮起零复制新脚本；"
"④三队盘点=main 顶=SC-005-04/05 fire-ready（fire 窗位）+MD-0002 T2I gated CEO 点头（tech#29）+#106/#12 gated 留痕·"
"tech 顶=#92 雷达标定权威窗 10-12 08:00 届日即领不预扫+观察位三连族 #97/#98/#100 随件收官轮并读+零可领（#96/#99 done 本轮）·explore 全 gated/到点未至；"
"⑤三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面（账号批次①+M4 GATE 6/10+#17 needs-CEO）0 发现"
"/loop_health 2F+242W 皆在案史实（两 outage 09-26/09-28 已裁定不重触发·drift 17==基线带内）；"
"⑥例行件=10-11 日报在案不重跑（R1927 00:2x 一份为真相）·W42 周审 10-12 未到·GB §④ 下期 10-15 跳过·meme V1 查看位禁重扫（R1899 锚维持·成片 mp4 未落=装配腿在飞）"
"·HQ-FEEDBACK 不写（11:3x 令=MV 会话域正典行内已覆响应计划·本司=查看位 ack·零集团层新 open 问题零膨胀）"
"·tokens:local=0（纯只读+CPU 工程+套件跑零本地模型产出调用·P-54⑤ 计量律）·队列补货步=真无独立新种子如实注记零膨胀"
"（本轮真发现=tech#96/#99 已消费进交付件·11:3x 令=查看位消费件非本司执行件·禁凑数律）·export=chips 刷 999 测绿（真实况变化面·live/do 三行核读仍准确维持）；"
"——下轮=R1972 快速路径首查（fire 卡复查 GO 即发=SC-005-04 单轮全链 F-176〔R1964/R1965 同型〕→SC-005-05 同窗连发 F-177"
"+tech#92 雷达标定判据窗 10-12 08:00 届日即领〔zhihu-hot 头部 ≥3 件 ≥60=PASS·FAIL=阈值分层腿递补〕+meme V1 成片查看位）。收账显式列文件 commit+push。")

cc.finalize_state(logline, tick=1971)

# export chips refresh (canonical writer, tech#70): 977 -> 999 test-green chip.
patch_path = os.path.join(BASE, '.c3-tmp', 'r1971_export_patch.json')
export_path = os.path.join(BASE, 'docs', 'status-export.json')
with io.open(export_path, encoding='utf-8') as fh:
    cur = json.load(fh)
new_chips = []
for c in cur.get('chips', []):
    if isinstance(c, list) and c and c[0] == '977 测绿':
        new_chips.append(['999 测绿', c[1] if len(c) > 1 else 'live'])
    else:
        new_chips.append(c)
with io.open(patch_path, 'w', encoding='utf-8', newline='\n') as fh:
    json.dump({'chips': new_chips}, fh, ensure_ascii=False)
import subprocess
r = subprocess.run([sys.executable, os.path.join(BASE, 'src', 'os', 'export_refresh.py'),
                    '--patch', patch_path], capture_output=True)
sys.stdout.write(r.stdout.decode('utf-8', errors='replace'))
print('export_refresh rc=%d' % r.returncode)

# close commit: state + export + self (tech#81 autodetect adds r1971_close.py)
rc, lines = cc.run_close_commit(
    [os.path.join('src', 'os', 'state.json'), os.path.join('docs', 'status-export.json')],
    "R1971 close: tick 1971; HQ orders 11:3x fullmv sprint order consumed (backlog #111 view-position ack, "
    "CEO-FEEDBACK-fullmv-fix-20261011.md verified, MV session executes, loop zero-touch); fire card no-fire "
    "(MV priority lane) SC-005-04/05 fire-ready carryover; tech#96/#99 done (sc_beats_check.py, 999 suite green); "
    "next: SC-005-04 F-176 full chain on next fire window + radar caliper 10-12 08:00 [via bm-a]")
for ln in lines:
    print(ln)
print('run_close_commit rc=%d' % rc)
