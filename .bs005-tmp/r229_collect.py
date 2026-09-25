# -*- coding: utf-8 -*-
# R229 collection step (assert-guarded, R228 pattern)
import io, json
from datetime import datetime, timezone, timedelta

now_str = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%dT%H:%M:%S+08:00')
hm = datetime.now(timezone(timedelta(hours=8))).strftime('%H:%M')

# ---------- 1. backlog: append R229 delivery line after R228 delivery line ----------
bp = r'src/os/backlog.md'
bs = io.open(bp, encoding='utf-8').read()
r228_tail = '（R222→R223/R224→R225/R226→R227 先例节律·tmp 批闭收账随收官轮）]**'
assert r228_tail in bs and 'R229 交付毕' not in bs, 'backlog anchor/dup guard'
delivery = ('\n\n**[R229 交付毕 2026-09-25 ' + hm + '：#27 ①有声线 ch.4 收官=F-011 登记（claim 3731dd4 续做·新连载节律第二件·成品库第十件·'
            '**有声线四件在库 F-008/F-009/F-010/F-011**）——S2 席 ASR 终轨回听（R169 QC recipe medium-int8+beam5+noctx·'
            'R229 后台新跑：**数字面 100% 零退化=系列第二件**+纪念碑田双位全净+朱鸿奎净读系列第四件+'
            '徐根福双位一存一退〔R200 同型〕+归档者-07 首提退化〔M6 真人校准线〕+'
            '同音噪声 79 sites/122 chars=字位 15.1% 系列新高带〔difflib 量化=量化术语密度最高件+它→他 ×13〕·'
            '字幕轨=edge-tts 精确直出 12/12 零损）+E8 终审听审七席全 9.0（R223 定标维度复用·'
            '`docs/reviews/review-20260925-sc00104-v1.md`·E1=系列钩兑现章第三件〔ch.3 命名礼钩→本集正解+ch.5 徐根福钩承接〕）+'
            'E4 参考仪同轮回填 **8.0 会听完=批次参考线新高持平四连**（10:13:02 落地窗内·'
            '旗=电波猫/徐根福拍连载语境吸收位·最弱=术语背景=纪实线来源律 M6 注释位·非拦截）→'
            '**F-011 登记**（`output/finished.md`）+audio/README 升成品标+station-reviews 三行+'
            'sc001-04-v1-tmp 批闭收账随 commit（asr-check.srt+asr-diff-r229+e4_call.py/e4-result.json+seg/gap/breath）；'
            '②③ bm-a 复核=零新进展（网文止 ch.5·漫画止 ep.2·r229_scan.py 实证）；'
            '发布锁=M5 账号物理件不变；后续有声章件 ch.5《徐根福的食堂》网文稿盘上=新连载节律随轮认领]**')
bs = bs.replace(r228_tail, r228_tail + delivery, 1)
io.open(bp, 'w', encoding='utf-8', newline='\n').write(bs)
print('OK backlog R229 delivery line')

# ---------- 2. state.json: tick / focus / log append ----------
sp = r'src/os/state.json'
ss = io.open(sp, encoding='utf-8').read()
assert '"tick": 228,' in ss and '"tick": 229,' not in ss, 'tick guard'
ss = ss.replace('"tick": 228,', '"tick": 229,', 1)

FOCUS_NEW = ('R230: ①快速路径五查（素材窗迹象优先：新令/ledger 严格行含 @ 前缀锚 14/decisions UTF8 非空行锚 24/树态/bm-a 写盘迹象）'
             '②生产线=BS-005 原版+bs005e 双 blocked 维持（共享开窗实录批·素材窗一开即续链：对位表重构→重渲→S2 复跑→E8→M4→登记'
             '〔bs005e=F-007 预留位·BS-005 原版=编号顺延〕·新源规格化 prep_vertical --batch 一跑直达）'
             '③#27 ①有声线续件判断（ch.5《徐根福的食堂》网文稿盘上=ch.4 cta 钩承接在位·新连载节律随轮认领）'
             '+②③ bm-a 进度复核（网文 ch.6 待落·漫画 ep.3 待见）'
             '④例行=探针三件套照跑（readiness 预期=bs-005/bs005e 双 render-unannot blocked 在链预期红维持·双件登记即清）'
             '⑤idle-fast 并窗计数=0/6（R229 实活轮已收账·R230 起重计）。')
lines = ss.split('\n')
fidx = [i for i, ln in enumerate(lines) if ln.startswith('  "focus": "R229:')]
assert len(fidx) == 1, 'focus line not found: %d' % len(fidx)
lines[fidx[0]] = '  "focus": "' + FOCUS_NEW + '",'
ss = '\n'.join(lines)

log_line = ('2026-09-25 ' + hm + ' R229: 生产轮·#27 ①有声线 ch.4 收官=F-011 登记（claim 3731dd4 续做·新连载节律第二件·实活轮）——'
            '①轮首五查静：无新令（orders 顶=O-0850 R222 已记账·时间序核验）·ledger 严格行含 @ 四模式 14 行=锚零新转办（r229_scan.py 实跑）·'
            'decisions UTF8 非空行 24=锚零新行（初读 23=GBK 无参伪差·UTF8 复核定谳=R131/R148/R204 在案坑）·'
            '树态=仅自产 blocked 批中间件+sc001-04-v1-tmp 未提交（批闭收账惯例维持）·无 index.lock·无 bm-a 写盘迹象；'
            '②素材窗迹象核=15 窗枚举零 Biggame 总控窗（Tuanjie 态=Unity Error+Game+DemoScene+Cowork+HMI Version Control+豆包/硅基生命元宇宙 Edge·'
            'R193-R228 定谳线维持）→BS-005/bs005e 双 blocked 维持·②③ bm-a 复核=盘上实证（网文止 ch.5·ch.6 未落/漫画止 ep.2·ep.3 未现）零新进展；'
            '③S2 席 ASR 终轨回听（R169 QC recipe medium-int8+beam5+noctx·Start-Process 后台起飞 PID 56872 与 E4 同轮双飞）：'
            '**数字面 100% 零退化=系列第二件**（十二/三天/一万个人/第四章）+纪念碑田双位全净+**朱鸿奎净读系列第四件**+'
            '徐根福双位一存一退（b10 净/cta 福→湖=R200 同型）+归档者-07→「龟荡者灵漆」首提退化（本集新主角名=M6 真人校准线）+'
            '概念存活面 样本泄漏/天理难容/数据清洗/户口/电波猫/一眼眼/台风警报/遮雨布/蒸笼/师娘/北外滩/立国那天/永远不收敛/机械钟声·'
            '**同音噪声 79 sites/122 diff chars/810 字=字位 15.1%=系列新高带**（difflib 量化=量化术语密度最高件+它→他 ×13+师父→师傅 ×3·'
            '字幕轨=edge-tts 精确直出 12/12=发布面零损）→S2 9.0；'
            '④E8 终审听审评审单 review-20260925-sc00104-v1.md（S1=N/A 同文本律继承位/S2 9.0/S3 9.0/S4 9.0+终审七席全 9.0——'
            'R223 定标维度复用零新立·E1=系列钩兑现章第三件〔ch.3 命名礼钩→本集睁眼报版本号开场正解+ch.5 徐根福钩承接在位〕·'
            'S4=纪实线三卡互证链 C-00017+C-00011+C-00010）；'
            '⑤E4 参考仪同轮回填毕（e4_call.py ch.4 版与 ASR 同轮双飞 PID 45328→10:13:02 记时落地窗内快落=模型热载态：'
            '**8.0 会听完=批次参考线新高持平四连**〔3/7/7/7→8→8→8→8〕·旗=电波猫/徐根福拍连载语境吸收位〔L-文 线 bm-a·同文本律〕·'
            '最弱=术语背景=纪实线来源律不可改写 M6 注释位·无真实性质疑旗·非拦截·净本 expert-verdicts/20260925-101302）；'
            '⑥**F-011 登记**（finished.md 成品库第十件·**有声线四件在库 F-008/009/010/011**·编号沿 F-010 顺延〔F-007=BS-005e 预留位维持〕·'
            'GATE 面核=10 稿集无有声稿不动·发布件 GATE 随 M5 立账）+audio/README 升成品标+station-reviews 三行（S2 ASR/E8+F-011/E4 回填）+'
            'sc001-04-v1-tmp 批闭收账随 commit（asr-check.srt+asr-diff-r229+e4_call.py/e4-result.json+seg/gap/breath+asr_diff_r229.py）；'
            '⑦三探针=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面+2 发现'
            '（bs-005/bs005e render-unannot=blocked 在链预期红维持·登记即清·阻塞≠失败口径 exit 1）/'
            'loop_health 0 FAIL 15 WARN 皆在案史实（9 log-order+6 heartbeat-gap·tick228=done228 对账平·backlog 28 项 23 done 82% 燃尽）；'
            '⑧例行件：日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks day1 ≤7 跳过（下期 ~10-01）·'
            'T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·'
            'tokens:local=2（faster-whisper medium×1 ASR 终轨+qwen2.5:14b×1 E4 参考仪=本地栈零 API token·P-54⑤ 计量律如实记）。'
            '下轮=R230 快速路径首查（素材窗迹象/新令→ch.5《徐根福的食堂》有声化起链判断或 idle-fast）。收账显式列文件 commit+push。')
tail_anchor = '下轮=R229 ch.4 收官（E8 听审+ASR+F-011）或素材窗迹象。收账显式列文件 commit+push。"\n  ]\n}'
assert tail_anchor in ss, 'log tail anchor'
ss = ss.replace(tail_anchor,
                '下轮=R229 ch.4 收官（E8 听审+ASR+F-011）或素材窗迹象。收账显式列文件 commit+push。",\n    "' + log_line + '"\n  ]\n}', 1)
io.open(sp, 'w', encoding='utf-8', newline='\n').write(ss)
json.loads(io.open(sp, encoding='utf-8').read())
print('OK state.json tick+focus+log (json valid)')

# ---------- 3. status-export.json refresh (F3: derived from current round) ----------
ep = r'docs/status-export.json'
es = io.open(ep, encoding='utf-8').read()
pairs = [
    ('"export_ts": "2026-09-25T10:07:03+08:00"', '"export_ts": "%s"' % now_str),
    ('①有声线三件成品 F-008/F-009/F-010+ch.4 第一程 R228+②漫画 ep.1/ep.2+③网文连载至 ch.5·④发布锁内挂账=bm-a/循环分领在案',
     '①有声线四件成品 F-008/F-009/F-010/F-011（ch.4 收官 R229）+②漫画 ep.1/ep.2+③网文连载至 ch.5·④发布锁内挂账=bm-a/循环分领在案'),
    ('（charter §1 有声线口径·F-008/F-009/F-010 三件成品实证+E4 观众侧印证「轻度赛博机械感为故事增添未来感」=声线定档端到端闭环）',
     '（charter §1 有声线口径·F-008~F-011 四件成品实证+E4 观众侧印证「新颖形式和题材有吸引力」=声线定档端到端闭环）'),
    ('#27 三线批：①有声线=**ch.1/ch.2/ch.3 三件成品在库（F-008/F-009/F-010·R227 批 scope 收官）+ch.4《纪念碑田》第一程毕（R228：beats 12 拍同文本核验 miss 0+TTS light 189.13s·12 cues+ai_feel 全绿+M4 四检·E8/ASR/F-011=下轮）**+②漫画 ep.1/ep.2 产线定栈（居民参考卡制）+③网文连载至 ch.5=bm-a 闭批；短产线=F-001~F-006 六件·BS-005/bs005e 双 blocked 待素材窗',
     '#27 三线批：①有声线=**ch.1-ch.4 四件成品在库（F-008/F-009/F-010/F-011·ch.4《纪念碑田》R229 收官：ASR 终轨数字面 100% 零退化系列第二件+E8 七席 9.0+E4 8.0 四连平）**+②漫画 ep.1/ep.2 产线定栈（居民参考卡制）+③网文连载至 ch.5=bm-a 闭批；短产线=F-001~F-006 六件·BS-005/bs005e 双 blocked 待素材窗'),
    ('M4 门机制全绿·F-001~F-006 六件+F-008/F-009/F-010 有声三件过门登记（九件）·三重标注音频内置三件核验过+纯音频件评分维度定标（charter §5）',
     'M4 门机制全绿·F-001~F-006 六件+F-008~F-011 有声四件过门登记（十件）·三重标注音频内置四件核验过+纯音频件评分维度定标（charter §5）'),
    ('OS 循环实活轮 R228（#27 ① 有声线 ch.4 第一程：beats 同文本核验+TTS light+ai_feel 全绿+M4 四检；三探针绿·244 回归绿维持）',
     'OS 循环实活轮 R229（#27 ① 有声线 ch.4 收官=F-011 登记：ASR 终轨回听+E8 七席 9.0+E4 同轮回填 8.0；三探针绿·244 回归绿维持）'),
    ('tick 228·R228（实活轮：#27 ①有声线 ch.4《纪念碑田》第一程=beats 12 拍同文本核验 12 段 miss 0+TTS light 189.13s·12 cues+ai_feel 全绿+M4 四检·E8/ASR/F-011=下轮；素材窗 15 窗零 Biggame 总控窗=双 blocked 维持）',
     'tick 229·R229（实活轮：#27 ①有声线 ch.4《纪念碑田》收官=F-011 登记·ASR 终轨〔数字面 100% 零退化=系列第二件+朱鸿奎净读第四件+79 sites=字位 15.1% 量化术语密度最高件系列新高带·字幕轨 12/12 零损〕+E8 七席 9.0+E4 8.0 同轮回填四连平；素材窗 15 窗零 Biggame 总控窗=双 blocked 维持）'),
    ('短产线六件在库收官+F-008/F-009/F-010 有声三件（成品库九件）·BS-005/bs005e 双 blocked 待开窗实录批；**新线=硅基城市三线**（网文连载至 ch.5·有声三件成品批 scope 收官·漫画 ep.1/ep.2 产线定栈）',
     '短产线六件在库收官+F-008~F-011 有声四件（成品库十件）·BS-005/bs005e 双 blocked 待开窗实录批；**新线=硅基城市三线**（网文连载至 ch.5·有声四件成品连载节律运转中·漫画 ep.1/ep.2 产线定栈）'),
    ('SC-001-04-v1《纪念碑田》第一程毕（R228：3:09.1·12 cues·ai_feel 全绿+M4 四检·E8/ASR/F-011=下轮）——**三件在库+ch.4 在链**·连载节律随轮认领',
     'SC-001-04-v1《纪念碑田》**成品·F-011**（R229 收官：3:09.1·12 cues·ASR 终轨〔数字面 100% 零退化=系列第二件·朱鸿奎净读系列第四件·同音噪声 79 sites=字位 15.1% 量化术语密度最高件系列新高带·字幕轨 12/12 零损〕+E8 七席 9.0+E4 8.0 同轮回填四连平）——**四件在库**·ch.5《徐根福的食堂》=新连载节律随轮认领'),
    ('[\n      "228",\n      "OS 轮次"\n    ]', '[\n      "229",\n      "OS 轮次"\n    ]'),
    ('[\n      "9",\n      "成品库登记件 F-001~F-006+F-008/F-009/F-010（短产线 N6 收官+有声三件·#27 批 scope 收官；F-007=BS-005e 预留位 blocked 待素材窗）"\n    ]',
     '[\n      "10",\n      "成品库登记件 F-001~F-006+F-008~F-011（短产线 N6 收官+有声四件·新连载节律运转中；F-007=BS-005e 预留位 blocked 待素材窗）"\n    ]'),
    ('回归测试绿（R228 零代码变更·纯产线件+台账轮·维持）', '回归测试绿（R229 零代码变更·纯产线件+台账轮·维持）'),
]
for old, new in pairs:
    assert old in es, 'export anchor missing: ' + old[:40]
    es = es.replace(old, new, 1)
io.open(ep, 'w', encoding='utf-8', newline='\n').write(es)
json.loads(io.open(ep, encoding='utf-8').read())
print('OK status-export refreshed (json valid)')
