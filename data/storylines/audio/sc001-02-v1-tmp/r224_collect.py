# -*- coding: utf-8 -*-
# R224 collection-step surgical edits (assert-guarded)
import io

# ---------- 1. backlog: append R224 delivery line after claim line ----------
bp = r'src/os/backlog.md'
bs = io.open(bp, encoding='utf-8').read()
claim_tail = '网文连载至 ch.5=7d31c89·ch.6 钩已埋）]**'
assert claim_tail in bs and 'R224 交付毕' not in bs, 'backlog anchor/dup guard'
delivery = ('\n\n**[R224 交付毕 2026-09-25 09:3X：#27 ①有声线续件 ch.2 第一程毕（claim 1abcf7f）——'
            'beats 12 拍（`data/storylines/audio/SC-001-02-v1.beats.txt`·同文本逐字·**机械核验 11 段 miss 0**·'
            'hook=cue01 三重标注声明拍/cta=预告口播化去括号=ep1 先例）→TTS light 产线默认→'
            '**SC-001-02-v1.mp3 落位（3:26.3=ffprobe 206.32s·12 cues）**+SC-001-02-v1.srt；'
            'S2 ai_feel 门全绿（gaps 11 处 0.239-0.558s varied/pacing CV 0.415/prosody 8 档 12 拍/copy CV 0.389·0 FAIL 0 WARN）·'
            'spec=时长 ffprobe 实测注记（U2 通识窗未核验·固有长度如实）·层 1.8=纯音频 N/A→M4 四检过（charter §5）；'
            '台账四件=audio/README 行+门禁记录块+状态行+变更行；'
            '**E8 终审听审+S2 席 ASR 终轨+F-009 登记=拆细下轮**（R222→R223 先例节律·tmp 批闭收账随收官轮）]**')
bs = bs.replace(claim_tail, claim_tail + delivery, 1)
io.open(bp, 'w', encoding='utf-8', newline='\n').write(bs)
print('OK backlog delivery line')

# ---------- 2. state.json: tick / focus / log append ----------
sp = r'src/os/state.json'
ss = io.open(sp, encoding='utf-8').read()
assert '"tick": 223,' in ss and '"tick": 224,' not in ss, 'tick guard'
ss = ss.replace('"tick": 223,', '"tick": 224,', 1)

focus_old = ('R224: ①快速路径五查（素材窗迹象优先：新令/ledger 严格行含 @ 前缀锚 14/decisions UTF8 非空行锚 24/树态/bm-a 写盘迹象）'
             '②生产线=BS-005 原版+bs005e 双 blocked 维持（共享开窗实录批·素材窗一开即续链：对位表重构→重渲→S2 复跑→E8→M4→F-007·新源规格化 prep_vertical --batch 一跑直达）'
             '③#27 ②③ bm-a 会话进度复核（小说连载线 09:05 已见 ch.4 Monument Field aa3ece6·漫画 PoC 待见）+有声线第二章起链判断（同文本律=网文稿到位即起链·纯音频件维度已定标 R223）'
             '④例行=探针三件套照跑（readiness 预期=bs-005/bs005e 双 render-unannot blocked 在链预期红维持·双件登记即清）'
             '⑤idle-fast 并窗计数=1/6（R223 实活轮触发收账=双 commit·R224 起重计）。')
focus_new = ('R225: ①快速路径五查（素材窗迹象优先：新令/ledger 严格行含 @ 前缀锚 14/decisions UTF8 非空行锚 24/树态/bm-a 写盘迹象）'
            '②生产线=BS-005 原版+bs005e 双 blocked 维持（共享开窗实录批·素材窗一开即续链：对位表重构→重渲→S2 复跑→E8→M4→F-007·新源规格化 prep_vertical --batch 一跑直达）'
            '③#27 ①有声线 ch.2 收官（E8 终审听审=纯音频维度 R223 定标复用+S2 席 ASR 终轨回听 R169 QC recipe+F-009 登记〔编号沿 F-008 顺延〕+audio/README 升成品标+sc001-02-v1-tmp 批闭收账）'
            '+②③ bm-a 进度复核（网文 ch.6 钩=Zhou Haoyu 已埋·漫画 ep.3 待见）'
            '④例行=探针三件套照跑（readiness 预期=bs-005/bs005e 双 render-unannot blocked 在链预期红维持·双件登记即清）'
            '⑤idle-fast 并窗计数=0/6（R224 实活轮已收账·R225 起重计）。')
assert focus_old in ss, 'focus anchor'
ss = ss.replace(focus_old, focus_new, 1)

log_tail = '本笔后单件补记 commit。"\n  ]\n}'
assert log_tail in ss and 'R224:' not in ss.split(log_tail)[0].split('R223 轮末补记')[-1], 'log tail anchor'
log_line = ('2026-09-25 09:3x R224: 生产轮·#27 ①有声线续件 ch.2 第一程毕（claim 1abcf7f 两步制·O-0850 三线批·实活轮）——'
            '①轮首五查：无新令（orders 顶=O-0850 R222 已记账）·ledger 严格行含 @ 四模式 14 行=锚零新转办'
            '（首扫 13=正则漏 @七线全司 模式笔误·当场补扫定谳·R163/R216 同型操作红）·'
            'decisions UTF8 非空行 24=锚零新行·树净零锁（仅自产 tmp）·无 bm-a 在飞写盘；'
            '②#27 ②③ bm-a 复核收账=漫画线 ep.1/ep.2 已落（9d280a7：SC-002-01/02·跨集一致性实验闭=风格锚跨模型成立+主角污染发现→**居民参考卡制**立产线规则+低分轨 608px→ESRGAN×2 验证·charter v1.1 漫画线产线定栈·诚实缺陷入档）'
            '+网文连载至 ch.5（7d31c89《许根富的食堂》C-00016·ch.6 钩=Zhou Haoyu 已埋）——②③=bm-a 认领面零接触；'
            '③**有声线第二章起链判断成立**（同文本律=网文稿 SC-001-02《灶头上的顾阿凤》盘上）→第一程交付：'
            'beats 12 拍（data/storylines/audio/SC-001-02-v1.beats.txt·同文本逐字**机械核验 11 段 miss 0**·'
            'hook=cue01 三重标注声明拍/cta=预告口播化去括号=ep1 结构处理先例）→'
            'TTS light 产线默认（Yunyang+cyber light+human 42）→**SC-001-02-v1.mp3 落位（3:26.3=ffprobe 206.32s·12 cues）**+SC-001-02-v1.srt；'
            'S2 ai_feel 门全绿（gaps 11 处 0.239-0.558s varied/pacing CV 0.415/prosody 8 档 12 拍/copy CV 0.389·0 FAIL 0 WARN）·'
            'spec 面=时长 ffprobe 实测注记（10-20min 通识窗 U2 未核验·固有长度如实不硬凑）·层 1.8=纯音频 N/A→'
            'M4 四检过（charter §5：红线五条+三重标注 cue01 内置+来源级=ch.2 文末清单指针+S2 机检）；'
            '台账四件=audio/README 行+门禁记录块+状态行+变更行（python 脚本编辑落地·replace 目检受 GBK 控制台显示坑阻·R173 先例）；'
            '**E8 终审听审+S2 席 ASR 终轨+F-009 登记=拆细下轮**（R222→R223 先例节律）；'
            '④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面+2 发现'
            '（bs-005/bs005e render-unannot=R193/R204 blocked 在链预期红维持·F-005/F-007 登记即清·阻塞≠失败口径 exit 1）/'
            'loop_health 0 FAIL 15 WARN（14 在案史实+新 1=R222→R223 乱序=R223 预判命中·诚实记录非操作红·tick223=done223 对账平）；'
            '⑤例行件：日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks day2 ≤7 跳过（下期 ~10-01）·'
            'T1 催办=已裁项停用口径无超线项·HQ-FEEDBACK 不写（无集团层新 open 问题·零膨胀）·'
            'tokens:local=0（TTS=edge-tts 云免费接口非本地 LLM·ai_feel 纯脚本机检·P-54⑤ 计量律如实记）；'
            '素材窗核=8 窗枚举零 Biggame 总控窗（Tuanjie 态=Unity Error+UGit+Cowork·R193-R221 定谳线维持）→BS-005 双 blocked 维持。'
            '下轮=R225 快速路径首查→ch.2 收官（E8 听审+ASR+F-009）或素材窗迹象。收账显式列文件 commit+push。"')
ss = ss.replace(log_tail, '本笔后单件补记 commit。",\n    ' + log_line + '\n  ]\n}', 1)
io.open(sp, 'w', encoding='utf-8', newline='\n').write(ss)
print('OK state.json tick+focus+log')

# ---------- 3. status-export.json refresh (F3: derived from current round) ----------
ep = r'docs/status-export.json'
es = io.open(ep, encoding='utf-8').read()
pairs = [
    ('"export_ts": "2026-09-25T09:09:00+08:00"', '"export_ts": "2026-09-25T09:38:00+08:00"'),
    ('O-20260925-0850 硅基城市内容宇宙三线令收讫（P1 CEO 亲署·调研+立制+网文首章 bm-a 闭批+**①有声首集腿收官 R223=F-008 登记**）·委托决策令 O-2126 七决闭环（否决窗至 10-01）·集团 D-03 锁标准 R182 回执毕',
     'O-20260925-0850 硅基城市内容宇宙三线令收讫（P1 CEO 亲署·①有声线 ch.1 成品 F-008+ch.2 第一程 R224·②漫画 ep.1/ep.2+③网文连载至 ch.5=bm-a 闭批复核在案）·委托决策令 O-2126 七决闭环（否决窗至 10-01）·集团 D-03 锁标准 R182 回执毕'),
    ('#27 三线批：**①有声首集收官（R223：E8 终审听审首件定标+ASR 事实词全存活+F-008 登记=成品库第七件）**+②漫画 PoC/③网文第二章 bm-a 在飞；短产线=F-001~F-006 六件+F-008 有声件·BS-005/bs005e 双 blocked 待素材窗',
     '#27 三线批：①有声线=ch.1 成品 F-008+**ch.2 第一程毕（R224：beats 12 拍同文本核验 miss 0+TTS light+ai_feel 全绿+M4 四检·E8/ASR/F-009=下轮）**+②漫画 ep.1/ep.2 产线定栈（居民参考卡制）+③网文连载至 ch.5=bm-a 闭批；短产线=F-001~F-006 六件·BS-005/bs005e 双 blocked 待素材窗'),
    ('OS 循环实活轮 R223（#27 ① E8 定标收官：ASR R169 QC recipe 后台新跑+E4 参考仪在飞+纯音频评审维度首定；三探针绿·244 回归绿维持）',
     'OS 循环实活轮 R224（#27 ① 有声线 ch.2 第一程：beats 同文本机械核验+TTS light+ai_feel 全绿+M4 四检；三探针绿·244 回归绿维持）'),
    ('tick 223·R223（实活轮：#27 ①有声首集腿收官=E8 终审听审首件定标+ASR 事实词全存活+F-008 登记；E4 参考仪在飞下轮回填）',
     'tick 224·R224（实活轮：#27 ①有声线 ch.2 第一程=beats/TTS light/S2 ai_feel 全绿/M4 四检·E8 终审听审+ASR+F-009 登记=下轮；②③ bm-a 复核=漫画 ep.1/ep.2+网文 ch.5 收账）'),
    ('production open（D-BS-06）·短产线六件在库收官+F-008 有声件（成品库七件）·BS-005/bs005e 双 blocked 待开窗实录批；**新线=硅基城市三线**（网文首章已发·有声首集成品 F-008·漫画 PoC bm-a 在飞）',
     'production open（D-BS-06）·短产线六件在库收官+F-008 有声件（成品库七件）·BS-005/bs005e 双 blocked 待开窗实录批；**新线=硅基城市三线**（网文连载至 ch.5·有声 ch.1 成品+ch.2 第一程·漫画 ep.1/ep.2 产线定栈）'),
    ('SC-001-01-v1《立国日》**成品·F-008**（R223 E8 终审听审七席 9.0+ASR 事实词全存活+**纯音频件评分维度首定**·E4 参考仪在飞下轮回填·data/storylines/audio/ 台账）',
     'SC-001-01-v1《立国日》**成品·F-008**（R223 定标）+SC-001-02-v1《灶头上的顾阿凤》第一程毕（R224：3:26.3·12 cues·ai_feel 全绿+M4 四检·E8/ASR/F-009=下轮·data/storylines/audio/ 台账）'),
    ('[\n      "223",\n      "OS 轮次"\n    ]', '[\n      "224",\n      "OS 轮次"\n    ]'),
]
for old, new in pairs:
    assert old in es, 'export anchor missing: ' + old[:40]
    es = es.replace(old, new, 1)
io.open(ep, 'w', encoding='utf-8', newline='\n').write(es)
print('OK status-export refreshed')
