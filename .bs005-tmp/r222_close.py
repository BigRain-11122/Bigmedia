# R222 close: append loop log line to state.json (UTF-8 safe, avoids PS5.1/replace pitfalls)
import json
import io

P = r'C:\Users\sjs20\Desktop\FluxGroup\media\BigStream\src\os\state.json'
LINE = ("2026-09-25 09:3x R222: 生产轮·O-20260925-0850 新令收讫+#27 ①有声首集腿第一程毕（claim 4ecc42b 两步制·实活轮）——"
        "①轮首快速路径五查①查不静：orders 新令 O-20260925-0850（CEO 硅基城市内容宇宙三线令·P1 亲署·有声/网文/漫画主打硅基城市）→转全任务书；"
        "bm-a 批已闭核验（4cb58ae：调研 v1.0+charter v1.0+网文首章 SC-001-01《立国日》+PLAN 2.5+backlog #27 置顶）"
        "+bm-a claim #27 ②漫画 PoC/③网文第二章（MCP 云图像通道=会话独占·①④留循环）；"
        "②循环交付=①有声首集：beats 12 拍落盘（data/storylines/audio/SC-001-01-v1.beats.txt·同文本逐字·纪实线禁虚构·7 档 profile·开场拍=cue01 AIGC 声明+纪实声明音频内置）"
        "→TTS light 产线默认（zh-CN-YunyangNeural+cyber light+human 42）→SC-001-01-v1.mp3 落位（3:50.4=ffprobe 230.422s·13 cues）+SC-001-01-v1.srt"
        "→S2 ai_feel 门全绿（gaps 12 处 0.239-0.558s varied/pacing CV 0.396/prosody 8 档 13 拍/copy CV 0.425·0 FAIL 0 WARN）"
        "·spec 面=音频时长 ffprobe 实测注记（10-20min 通识窗=U2 未核验·首章 1100 字固有长度如实不硬凑）·层 1.8=纯音频无剪辑面 N/A"
        "→M4 四检过（charter §5 口径：红线五条+三重标注〔AIGC 级+虚实级=cue01 内置·来源级=指针继承网文稿七条〕+来源继承+S2 机检）"
        "→台账 audio/README.md 立账+.gitignore data/storylines/audio/*.mp3 精确规则（charter §4 mp3 gitignored·README 记账）；"
        "E8 终审听审（首件有声定标）+S2 席 ASR 事实词核验+finished.md F 系登记=拆细下轮；"
        "③集团扫描=ledger 严格行含 @ 14 行=锚零新转办·decisions UTF8 非空行 24=锚零新行（probe-r222.py 实跑）·窗口枚举 15 窗零 Biggame 总控窗=双 blocked 维持；"
        "④三探针=board 0 FAIL（5 题 10 稿 5 in production）/readiness 3 阻塞皆外部 CEO 面+2 发现（bs-005/bs005e render-unannot=R193 blocked 在链预期红维持·登记即清）"
        "/loop_health 0 FAIL 14 WARN 皆在案史实；例行件：日报 2026-09-25+W39 周审在案不重跑·global-benchmarks day2 ≤7 跳过（下期 ~10-01）"
        "·T1 催办=已裁项停用口径无超线项·HQ-FEEDBACK 不写（新令本司份额执行中零集团层 open 问题）"
        "·tokens:local=0（TTS=edge-tts 云免费接口非本地 LLM·ai_feel 纯脚本机检·P-54⑤ 计量律如实记）"
        "——实活轮触发收账：并窗 R219-R221 三 idle-fast+R222 实活一并 commit（os-protocol §6·commit 注区间）。"
        "下轮=R223 快速路径首查（E8 听审定标领做/#27 ②③ bm-a 进度/素材窗迹象），全静即 idle-fast。")

with io.open(P, encoding='utf-8') as f:
    st = json.load(f)

assert st.get('tick') == 222, 'tick mismatch: %r' % st.get('tick')
last = st['log'][-1]
assert last.startswith('2026-09-25 08:4x R221'), 'unexpected last log line: %r' % last[:40]
st['log'].append(LINE)

with io.open(P, 'w', encoding='utf-8') as f:
    json.dump(st, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('R222 close OK: log lines =', len(st['log']), 'tick =', st['tick'])
