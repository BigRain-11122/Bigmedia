# -*- coding: utf-8 -*-
# R228 collection-step surgical edits (assert-guarded, R226 pattern)
import io
from datetime import datetime, timezone, timedelta

# ---------- 1. backlog: append R228 delivery line after claim line ----------
bp = r'src/os/backlog.md'
bs = io.open(bp, encoding='utf-8').read()
claim_tail = '（网文止 ch.5/ch.6 未落·漫画止 ep.2/ep.3 未现=零新进展）]**'
assert claim_tail in bs and 'R228 交付毕' not in bs, 'backlog anchor/dup guard'
delivery = ('\n\n**[R228 交付毕 2026-09-25 10:2X：#27 ①有声线续件 ch.4 第一程毕（claim 3731dd4）——'
            'beats 12 拍（`data/storylines/audio/SC-001-04-v1.beats.txt`·同文本逐字'
            '**机械核验 12 段 miss 0+cta 去括号口播化 OK**·hook=cue01 三重标注声明拍/cta=预告口播化=ep1-ep3 先例'
            '·归档者-07 章=ch.3 cta「命名礼」钩承接·承接章主角名=徐根福 ch.4/ch.5 双文一致核验过〔R224 log 行「许根富」=台账笔误非文本态〕）→'
            'TTS light 产线默认→**SC-001-04-v1.mp3 落位（3:09.1=ffprobe 189.127s·12 cues）**+SC-001-04-v1.srt；'
            'S2 ai_feel 门全绿（gaps 11 处 0.220-0.583s varied/pacing CV 0.480/prosody 7 档 12 拍/copy CV 0.495·0 FAIL 0 WARN）·'
            'spec=时长 ffprobe 实测注记（10-20min 通识窗 U2 未核验·本章文本固有长度如实不硬凑=纪实线禁虚构）·'
            '层 1.8=纯音频无剪辑面 N/A→M4 四检过（charter §5·来源级=ch.4 文末清单指针〔C-00017 归档者-07 主卡+C-00011/C-00010 互证〕+S2 机检）；'
            '台账四件=audio/README 行+门禁记录块+状态行+变更行；'
            '**E8 终审听审+S2 席 ASR 终轨+F-011 登记=拆细下轮**（R222→R223/R224→R225/R226→R227 先例节律·tmp 批闭收账随收官轮）]**')
bs = bs.replace(claim_tail, claim_tail + delivery, 1)
io.open(bp, 'w', encoding='utf-8', newline='\n').write(bs)
print('OK backlog delivery line')

# ---------- 2. state.json: tick / focus / log append ----------
sp = r'src/os/state.json'
ss = io.open(sp, encoding='utf-8').read()
assert '"tick": 227,' in ss and '"tick": 228,' not in ss, 'tick guard'
ss = ss.replace('"tick": 227,', '"tick": 228,', 1)

FOCUS_NEW = ('R229: ①快速路径五查（素材窗迹象优先：新令/ledger 严格行含 @ 前缀锚 14/decisions UTF8 非空行锚 24/树态/bm-a 写盘迹象）'
             '②生产线=BS-005 原版+bs005e 双 blocked 维持（共享开窗实录批·素材窗一开即续链：对位表重构→重渲→S2 复跑→E8→M4→登记'
             '〔bs005e=F-007 预留位·BS-005 原版=编号顺延〕·新源规格化 prep_vertical --batch 一跑直达）'
             '③#27 ①有声线 ch.4 收官（E8 终审听审=R223 定标维度复用+S2 席 ASR 终轨回听 R169 QC recipe medium-int8+beam5+noctx'
             '+F-011 登记〔编号沿 F-010 顺延·F-007=BS-005e 预留位维持〕+audio/README 升成品标+sc001-04-v1-tmp 批闭收账）'
             '+②③ bm-a 进度复核（网文 ch.6 待落·漫画 ep.3 待见）'
             '④例行=探针三件套照跑（readiness 预期=bs-005/bs005e 双 render-unannot blocked 在链预期红维持·双件登记即清）'
             '⑤idle-fast 并窗计数=0/6（R228 实活轮已收账·R229 起重计）。')
lines = ss.split('\n')
fidx = [i for i, ln in enumerate(lines) if ln.startswith('  "focus": "R228:')]
assert len(fidx) == 1, 'focus line not found: %d' % len(fidx)
lines[fidx[0]] = '  "focus": "' + FOCUS_NEW + '",'
ss = '\n'.join(lines)

log_tail = '收账显式列文件 commit+push。"\n  ]\n}'
assert log_tail in ss, 'log tail anchor'
log_line = ('2026-09-25 10:2x R228: 生产轮·#27 ①有声线续件 ch.4 第一程毕（claim 3731dd4 两步制·新连载节律首件·实活轮）——'
            '①轮首五查静：无新令（orders 顶=O-20260925-0850 R222 已记账）·ledger 严格行含 @ 四模式 14 行=锚零新转办（r228_scan.py 实跑）·'
            'decisions UTF8 非空行 24=锚零新行·树态=仅自产 blocked 批中间件未提交（.bs005-tmp/.bs005e-tmp 批闭收账惯例维持）·'
            '无 index.lock·无 bm-a 写盘迹象；'
            '②素材窗迹象核=15 窗枚举零 Biggame 总控窗（Tuanjie 态=Unity Error+Game+GUIAgentUnity DemoScene+Cowork+HMI Version Control·'
            'R193-R227 定谳线维持·windows-R228.txt 留档）+footage 最新仍止于 looplog-16x9c（R198 裁净源）零新录→BS-005/bs005e 双 blocked 维持；'
            '③②③ bm-a 进度复核=盘上实证（网文止 ch.5·ch.6 未落/漫画止 ep.2·ep.3 未现）零新进展·'
            '承接章主角名核验=徐根福 ch.4/ch.5 双文一致（R224 log 行「许根富」=台账笔误非文本态·cta 同文本律无漂移）；'
            '④ch.4 有声化第一程交付：beats 12 拍（data/storylines/audio/SC-001-04-v1.beats.txt·同文本逐字'
            '**机械核验 12 段 miss 0+cta 去括号口播化 OK**·hook=cue01 三重标注声明拍/cta=预告口播化=ep1-ep3 先例·'
            '归档者-07 章=ch.3 cta「命名礼」钩承接）→TTS light 产线默认（Yunyang+cyber light+human 42）→'
            '**SC-001-04-v1.mp3 落位（3:09.1=ffprobe 189.127s·12 cues）**+SC-001-04-v1.srt；'
            'S2 ai_feel 门全绿（gaps 11 处 0.220-0.583s varied/pacing CV 0.480/prosody 7 档 12 拍/copy CV 0.495·0 FAIL 0 WARN）·'
            'spec 面=时长 ffprobe 实测注记（10-20min 通识窗 U2 未核验·本章文本固有长度如实不硬凑=纪实线禁虚构）·'
            '层 1.8=纯音频无剪辑面 N/A→M4 四检过（charter §5：红线五条+三重标注 cue01 内置+来源级=ch.4 文末清单指针'
            '〔C-00017 归档者-07 主卡+C-00011/C-00010 互证〕+S2 机检）；'
            '台账四件=audio/README 行+门禁记录块+状态行+变更行；'
            '**E8 终审听审+S2 席 ASR 终轨+F-011 登记=拆细下轮**（R222→R223/R224→R225/R226→R227 先例节律·tmp 批闭收账随收官轮）；'
            '⑤三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面+2 发现'
            '（bs-005/bs005e render-unannot=blocked 在链预期红维持·F-005/F-007 登记即清·阻塞≠失败口径 exit 1）/'
            'loop_health 0 FAIL 15 WARN 皆在案史实（9 log-order+6 heartbeat-gap·首跑 PS 内联 \\b\\r 转义吞路径 rc 2=操作红非探针红·'
            '正斜杠复跑全绿·tick227=done227 对账平·本轮 tick228 收账同步）；'
            '例行件：日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks day1 ≤7 跳过（下期 ~10-01）·'
            'T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·'
            'tokens:local=0（TTS=edge-tts 云免费接口非本地 LLM·ai_feel 纯脚本机检·P-54⑤ 计量律如实记）。'
            '下轮=R229 ch.4 收官（E8 听审+ASR+F-011）或素材窗迹象。收账显式列文件 commit+push。')
ss = ss.replace(log_tail,
                '收账显式列文件 commit+push。",\n    "' + log_line + '"\n  ]\n}', 1)
io.open(sp, 'w', encoding='utf-8', newline='\n').write(ss)
import json
json.loads(io.open(sp, encoding='utf-8').read())
print('OK state.json tick+focus+log (json valid)')

# ---------- 3. status-export.json refresh (F3: derived from current round) ----------
ep = r'docs/status-export.json'
es = io.open(ep, encoding='utf-8').read()
now = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%dT%H:%M:%S+08:00')
pairs = [
    ('"export_ts": "2026-09-25T09:57:50+08:00"', '"export_ts": "%s"' % now),
    ('①有声线三件成品 F-008/F-009/F-010+②漫画 ep.1/ep.2+③网文连载至 ch.5·④发布锁内挂账=bm-a/循环分领在案',
     '①有声线三件成品 F-008/F-009/F-010+ch.4 第一程 R228+②漫画 ep.1/ep.2+③网文连载至 ch.5·④发布锁内挂账=bm-a/循环分领在案'),
    ('#27 三线批：①有声线=**ch.1/ch.2/ch.3 三件成品在库（F-008/F-009/F-010·R227 批 scope 收官）**+②漫画 ep.1/ep.2 产线定栈（居民参考卡制）+③网文连载至 ch.5=bm-a 闭批；短产线=F-001~F-006 六件·BS-005/bs005e 双 blocked 待素材窗；后续有声章件 ch.4《纪念碑田》=新连载节律随轮认领',
     '#27 三线批：①有声线=**ch.1/ch.2/ch.3 三件成品在库（F-008/F-009/F-010·R227 批 scope 收官）+ch.4《纪念碑田》第一程毕（R228：beats 12 拍同文本核验 miss 0+TTS light 189.13s·12 cues+ai_feel 全绿+M4 四检·E8/ASR/F-011=下轮）**+②漫画 ep.1/ep.2 产线定栈（居民参考卡制）+③网文连载至 ch.5=bm-a 闭批；短产线=F-001~F-006 六件·BS-005/bs005e 双 blocked 待素材窗'),
    ('OS 循环实活轮 R227（#27 ① 有声线 ch.3 收官：ASR 终轨回听〔时间锚+数字面零退化=系列首件·difflib 量化口径首用〕+E8 听审七席 9.0+E4 同轮回填 8.0；三探针绿·244 回归绿维持）',
     'OS 循环实活轮 R228（#27 ① 有声线 ch.4 第一程：beats 同文本核验+TTS light+ai_feel 全绿+M4 四检；三探针绿·244 回归绿维持）'),
    ('tick 227·R227（实活轮：#27 ①有声线 ch.3 收官=F-010 登记·S2 ASR 终轨零数字退化+朱鸿奎 ×3 净读+E8 七席 9.0+E4 同轮 8.0 三连平·批原 scope ①②③ 全毕；素材窗 15 窗零 Biggame 总控窗=双 blocked 维持）',
     'tick 228·R228（实活轮：#27 ①有声线 ch.4《纪念碑田》第一程=beats 12 拍同文本核验 12 段 miss 0+TTS light 189.13s·12 cues+ai_feel 全绿+M4 四检·E8/ASR/F-011=下轮；素材窗 15 窗零 Biggame 总控窗=双 blocked 维持）'),
    ('SC-001-03-v1《周三的棋局》**成品·F-010**（R227 收官：3:10.3·13 cues·ASR 终轨〔时间锚+数字面 100% 零退化=系列首件·朱鸿奎 ×3 净读·同音噪声 ≈70 处=字位 8.6% difflib 量化·字幕轨 13/13 零损〕+E8 七席 9.0+E4 8.0 同轮回填三连平）——**三件在库·#27 批 scope 收官**·ch.4《纪念碑田》=新连载节律随轮认领',
     'SC-001-03-v1《周三的棋局》**成品·F-010**（R227 收官：3:10.3·13 cues·ASR 终轨〔时间锚+数字面 100% 零退化=系列首件·朱鸿奎 ×3 净读·同音噪声 ≈70 处=字位 8.6% difflib 量化·字幕轨 13/13 零损〕+E8 七席 9.0+E4 8.0 同轮回填三连平）+SC-001-04-v1《纪念碑田》第一程毕（R228：3:09.1·12 cues·ai_feel 全绿+M4 四检·E8/ASR/F-011=下轮）——**三件在库+ch.4 在链**·连载节律随轮认领'),
    ('[\n      "227",\n      "OS 轮次"\n    ]', '[\n      "228",\n      "OS 轮次"\n    ]'),
    ('回归测试绿（R227 零代码变更·纯产线件+台账轮·维持）', '回归测试绿（R228 零代码变更·纯产线件+台账轮·维持）'),
]
for old, new in pairs:
    assert old in es, 'export anchor missing: ' + old[:40]
    es = es.replace(old, new, 1)
io.open(ep, 'w', encoding='utf-8', newline='\n').write(es)
json.loads(io.open(ep, encoding='utf-8').read())
print('OK status-export refreshed (json valid)')
