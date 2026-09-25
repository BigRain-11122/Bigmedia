import io
p = r'data/storylines/audio/README.md'
s = io.open(p, encoding='utf-8').read()
ls = s.splitlines()
row = '| SC-001-02-v1.mp3《硅基城市·第二章·灶头上的顾阿凤》 | 3:26.3（ffprobe 206.32s） | 12 | zh-CN-YunyangNeural+cyber light+human 42（产线默认） | ai_feel 0 FAIL 0 WARN（gaps 11 处 0.239-0.558s varied/pacing CV 0.415/prosody 8 档 12 拍/copy CV 0.389） | **在链·R224 第一程毕（E8 终审听审+S2 席 ASR 终轨+F-009 登记=下轮）** |'
idx = [i for i, l in enumerate(ls) if l.startswith('| SC-001-01-v1.mp3')][0]
assert idx is not None and 'SC-001-02' not in s, 'anchor/dup guard'
ls.insert(idx + 1, row)
s = '\n'.join(ls) + '\n'

gate = '**SC-001-02-v1（R224·M4 四检）**：红线五条 ✓（章节名纪实零标题党/来源全可溯 BigLife 户籍卡 C-00010 七条/无虚构添加——beats=网文稿正文逐字拍化·预告口播化去括号=结构处理·同文本机械核验 11 段 miss 0）；三重标注 ✓（音频开头内置 cue01：AIGC 级「本节目由 AI 参与生成」+虚实级「基于硅基城市真实事件改编」+来源级「完整来源清单见图文页」→`data/storylines/novel/SC-001-02-v1.md` 文末清单）；来源继承 ✓（同文本逐字·charter §3 一题三态·网文稿→有声稿同文本 TTS）；S2 机检 ✓（ai_feel 全绿；spec 面=时长 ffprobe 实测 3:26.3——单集 10-20min=〔通识假设〕U2 未核验·本章文本固有长度如实不硬凑〔纪实线禁虚构〕；层 1.8=纯音频无剪辑面 N/A）\n'
assert '\n## 状态' in s
s = s.replace('\n## 状态', '\n' + gate + '\n## 状态', 1)

st_add = '- **R224 第一程（在链）**：SC-001-02-v1.mp3《灶头上的顾阿凤》=ch.2 有声化第一程毕——beats 12 拍（同文本逐字·机械核验 miss 0）+TTS light 产线默认+ai_feel 0 FAIL 0 WARN+M4 四检过；E8 终审听审+S2 席 ASR 终轨+F-009 登记=下轮（素材窗等待期产能件·claim 1abcf7f）\n\n'
assert '## 变更记录' in s
s = s.replace('## 变更记录', st_add + '## 变更记录', 1)

chg = '- 2026-09-25: R224 第一程——#27 ①有声线续件 ch.2《灶头上的顾阿凤》：beats 12 拍+TTS light（206.30s 音轨）+ai_feel 全绿+M4 四检→SC-001-02-v1.mp3 落位（3:26.3·12 cues）；E8/ASR/F-009=下轮'
s = s.rstrip('\n') + '\n' + chg + '\n'
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('OK ledger row+gate+status+changelog')
