# -*- coding: utf-8 -*-
# R226 collection-step surgical edits (assert-guarded, R224 pattern)
import io
from datetime import datetime, timezone, timedelta

# ---------- 1. backlog: append R226 delivery line after claim line ----------
bp = r'src/os/backlog.md'
bs = io.open(bp, encoding='utf-8').read()
claim_tail = '（网文止 ch.5/ch.6 未落·漫画止 ep.2/ep.3 未现=零新进展）]**'
assert claim_tail in bs and 'R226 交付毕' not in bs, 'backlog anchor/dup guard'
delivery = ('\n\n**[R226 交付毕 2026-09-25 09:5X：#27 ①有声线续件 ch.3 第一程毕（claim c948b9b）——'
            'beats 13 拍（`data/storylines/audio/SC-001-03-v1.beats.txt`·同文本逐字·'
            '**机械核验 12 段 miss 0+cta 去括号 OK**·hook=cue01 三重标注声明拍/cta=预告口播化=ep1/ep2 先例）→'
            'TTS light 产线默认→**SC-001-03-v1.mp3 落位（3:10.3=ffprobe 190.258s·13 cues）**+SC-001-03-v1.srt；'
            'S2 ai_feel 门全绿（gaps 12 处 0.220-0.675s varied/pacing CV 0.461/prosody 7 档 13 拍/copy CV 0.509·0 FAIL 0 WARN）·'
            'spec=时长 ffprobe 实测注记（U2 通识窗未核验·固有长度如实）·层 1.8=纯音频 N/A→M4 四检过（charter §5）；'
            '台账四件=audio/README 行+门禁记录块+状态行+变更行；'
            '**E8 终审听审+S2 席 ASR 终轨+F-010 登记=拆细下轮**（R222→R223/R224→R225 先例节律·tmp 批闭收账随收官轮）]**')
bs = bs.replace(claim_tail, claim_tail + delivery, 1)
io.open(bp, 'w', encoding='utf-8', newline='\n').write(bs)
print('OK backlog delivery line')

# ---------- 2. state.json: tick / focus / log append ----------
sp = r'src/os/state.json'
ss = io.open(sp, encoding='utf-8').read()
assert '"tick": 225,' in ss and '"tick": 226,' not in ss, 'tick guard'
ss = ss.replace('"tick": 225,', '"tick": 226,', 1)

FOCUS_NEW = ('R227: ①快速路径五查（素材窗迹象优先：新令/ledger 严格行含 @ 前缀锚 14/decisions UTF8 非空行锚 24/树态/bm-a 写盘迹象）'
             '②生产线=BS-005 原版+bs005e 双 blocked 维持（共享开窗实录批·素材窗一开即续链：对位表重构→重渲→S2 复跑→E8→M4→F-007·新源规格化 prep_vertical --batch 一跑直达）'
             '③#27 ①有声线 ch.3 收官（E8 终审听审=纯音频维度 R223 定标复用+S2 席 ASR 终轨回听 R169 QC recipe+F-010 登记〔编号沿 F-009 顺延〕'
             '+audio/README 升成品标+sc001-03-v1-tmp 批闭收账）+②③ bm-a 进度复核（网文 ch.6=Zhou Haoyu 待落·漫画 ep.3 待见）'
             '④例行=探针三件套照跑（readiness 预期=bs-005/bs005e 双 render-unannot blocked 在链预期红维持·双件登记即清）'
             '⑤idle-fast 并窗计数=0/6（R226 实活轮已收账·R227 起重计）。')
lines = ss.split('\n')
fidx = [i for i, ln in enumerate(lines) if ln.startswith('  "focus": "R226:')]
assert len(fidx) == 1, 'focus line not found: %d' % len(fidx)
lines[fidx[0]] = '  "focus": "' + FOCUS_NEW + '",'
ss = '\n'.join(lines)

log_tail = '收账显式列文件 commit+push。"\n  ]\n}'
assert log_tail in ss, 'log tail anchor'
log_line = ('2026-09-25 09:5x R226: 生产轮·#27 ①有声线续件 ch.3 第一程毕（claim c948b9b 两步制·O-0850 三线批·实活轮）——'
            '①轮首五查静：无新令（orders 顶=O-0850 R222 已记账）·ledger 严格行含 @ 四模式 14 行=锚零新转办（r226_scan.py 实跑）·'
            'decisions UTF8 非空行 24=锚零新行·树净零锁（仅自产 tmp）·无 bm-a 写盘迹象；'
            '②素材窗迹象核=15 窗枚举零 Biggame 总控窗（Tuanjie 态=Unity Error+Game+GUIAgentUnity DemoScene+Cowork+HMI Version Control·'
            'R193-R225 定谳线维持）→BS-005/bs005e 双 blocked 维持；'
            '③②③ bm-a 进度复核=盘上实证（网文 ch.1-05·ch.6 未落/漫画 ep.1-02·ep.3 未现）零新进展；'
            '④ch.3 有声化第一程交付：beats 13 拍（data/storylines/audio/SC-001-03-v1.beats.txt·同文本逐字'
            '**机械核验 12 段 miss 0+cta 去括号 OK**·hook=cue01 三重标注声明拍/cta=预告口播化=ep1/ep2 先例）→'
            'TTS light 产线默认（Yunyang+cyber light+human 42）→**SC-001-03-v1.mp3 落位（3:10.3=ffprobe 190.258s·13 cues）**'
            '+SC-001-03-v1.srt；S2 ai_feel 门全绿（gaps 12 处 0.220-0.675s varied/pacing CV 0.461/prosody 7 档 13 拍/copy CV 0.509·'
            '0 FAIL 0 WARN）·spec 面=时长 ffprobe 实测注记（10-20min 通识窗 U2 未核验·固有长度如实不硬凑）·层 1.8=纯音频 N/A→'
            'M4 四检过（charter §5：红线五条+三重标注 cue01 内置+来源级=ch.3 文末清单指针+S2 机检）；'
            '台账四件=audio/README 行+门禁记录块+状态行+变更行；'
            '**E8 终审听审+S2 席 ASR 终轨+F-010 登记=拆细下轮**（R222→R223/R224→R225 先例节律·tmp 批闭收账随收官轮）；'
            '⑤三探针=board 0 FAIL（5 题 10 稿·5 in production）/readiness 3 阻塞皆外部 CEO 面+2 发现'
            '（bs-005/bs005e render-unannot=blocked 在链预期红维持·F-005/F-007 登记即清·阻塞≠失败口径 exit 1）/'
            'loop_health 0 FAIL 15 WARN 皆在案史实（tick225=done225 对账平·本轮 tick226 收账同步）；'
            '例行件：日报 2026-09-25+W39 周审在案不重跑·global-benchmarks day1 ≤7 跳过（下期 ~10-01）·'
            'T1 催办=已裁项停用口径无超线项·HQ-FEEDBACK 不写（无集团层新 open 问题·零膨胀）·'
            'tokens:local=0（TTS=edge-tts 云免费接口非本地 LLM·ai_feel 纯脚本机检·P-54⑤ 计量律如实记）。'
            '下轮=R227 ch.3 收官（E8 听审+ASR+F-010）或素材窗迹象。收账显式列文件 commit+push。')
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
    ('"export_ts": "2026-09-25T09:38:00+08:00"', '"export_ts": "%s"' % now),
    ('①有声线 ch.1 F-008+ch.2 F-009 双成品在库·②漫画 ep.1/ep.2+③网文连载至 ch.5=bm-a 闭批复核在案',
     '①有声线 ch.1 F-008+ch.2 F-009 双成品在库+ch.3 第一程 R226·②漫画 ep.1/ep.2+③网文连载至 ch.5=bm-a 闭批复核在案'),
    ('①有声线=ch.1 成品 F-008+**ch.2 成品 F-009（R225 收官：ASR 终轨+E8 七席 9.0+E4 同轮回填 8.0）=双件在库**',
     '①有声线=ch.1 成品 F-008+ch.2 成品 F-009 双件在库+**ch.3 第一程毕（R226：beats 13 拍同文本核验 miss 0+TTS light+ai_feel 全绿+M4 四检·E8/ASR/F-010=下轮）**'),
    ('OS 循环实活轮 R225（#27 ① 有声线 ch.2 收官：S2 ASR 终轨回听+E8 终审七席 9.0+F-009 登记+E4 参考仪同轮回填 8.0；三探针绿·244 回归绿维持）',
     'OS 循环实活轮 R226（#27 ① 有声线 ch.3 第一程：beats 同文本核验+TTS light+ai_feel 全绿+M4 四检；三探针绿·244 回归绿维持）'),
    ('tick 225·R225（实活轮：#27 ①有声线 ch.2 收官=F-009 登记〔ASR 终轨 1 处数字退化如实+同音噪声 ≈45 处=沪语+专名密度最高件·字幕轨零损·E8 七席 9.0·E4 同轮 8.0〕；#27 批 ①②③ 全毕·④=发布锁内挂账；素材窗 8 窗零 Biggame 总控窗=双 blocked 维持）',
     'tick 226·R226（实活轮：#27 ①有声线 ch.3 第一程=beats 13 拍同文本核验 12 段 miss 0+TTS light 190.26s·13 cues+ai_feel 全绿+M4 四检·E8/ASR/F-010=下轮；素材窗 15 窗零 Biggame 总控窗=双 blocked 维持）'),
    ('（网文连载至 ch.5·有声 ch.1+ch.2 双成品·漫画 ep.1/ep.2 产线定栈）',
     '（网文连载至 ch.5·有声 ch.1+ch.2 双成品+ch.3 第一程·漫画 ep.1/ep.2 产线定栈）'),
    ('（R225 收官：3:26.3·12 cues·ASR 终轨+E8 七席 9.0+E4 8.0 同轮回填·data/storylines/audio/ 台账）——双件在库·后续章件随轮认领',
     '（R225 收官：3:26.3·12 cues·ASR 终轨+E8 七席 9.0+E4 8.0 同轮回填·data/storylines/audio/ 台账）+SC-001-03-v1《周三的棋局》第一程毕（R226：3:10.3·13 cues·ai_feel 全绿+M4 四检·E8/ASR/F-010=下轮）——双件在库+ch.3 在链·连载节律随轮认领'),
    ('[\n      "225",\n      "OS 轮次"\n    ]', '[\n      "226",\n      "OS 轮次"\n    ]'),
    ('回归测试绿（R225 零代码变更·纯产线件+台账轮·维持）', '回归测试绿（R226 零代码变更·纯产线件+台账轮·维持）'),
]
for old, new in pairs:
    assert old in es, 'export anchor missing: ' + old[:40]
    es = es.replace(old, new, 1)
io.open(ep, 'w', encoding='utf-8', newline='\n').write(es)
json.loads(io.open(ep, encoding='utf-8').read())
print('OK status-export refreshed (json valid)')
