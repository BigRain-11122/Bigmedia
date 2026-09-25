# R280 state.json closeout: tick 279->280, append R280 log, refresh ts/task/focus (text surgery + JSON_OK validate)
import io, json, time

P = r'src/os/state.json'
now = time.strftime('%Y-%m-%d %H:%M:%S')
r280_ts = time.strftime('%H:%M')  # narrative minute precision per convention

LOG = ('2026-09-25 {TS} R280: 生产轮·#31 ch.3 v3 收官（O-20260925-1756 风格校准令音频重渲染腿 ch.3 收官·实活轮）——'
 '①轮首快速路径五查静（无新令 orders 顶=O-1756 R275 已记账·ledger 严格行含 @ 四模式 17 行=锚零新转办〔P-05/P-06 R276 收讫态维持〕·'
 'decisions UTF8 非空行 29〔总 32〕=锚零新行·树净零锁〔仅 R279 自产 tmp 批次未闭预期态〕·ch.5 v3 稿未落盘=novel 实证止 ch.4 v3）'
 '→backlog 顶行 #31 可认领=实活轮照 focus；'
 '②S2 席 ASR 终轨回听（R169 QC recipe medium-int8+beam5+noctx·Start-Process 后台 PID 47696·sc001-03-v3-tmp/asr-check.srt 28 cues/132.23s'
 '+asr-diff-r280 difflib 量化）：**时间锚 100% 存活**（每周三×2/1975/四十多年/每十分钟/立国那天 全净读）+数字面 C-00011/07 值存活'
 '·**2 处邻位形差如实**（74 岁→「1974岁」合并年读〔值 74 在位·年龄读数年份化〕/**微秒双位一存一退**〔误差压进微秒位存活/守着微秒位→「归一秒」重写〕·字幕轨正源零损）'
 '+专名面 **朱鸿奎→诸红魁 首提退化**〔对照 v1 ch.3 ×3 全净读=紧凑文本 whisper 代价面·M6 真人校准线〕/时空校准师→时空校准时/数据粥铺→数据周固'
 '/档案馆→当安管+档案管区/心跳备份→心跳倍奋/QUANT 城→框子城/归档者→归荡者·**金句三净读**（「走得快的表不算好表，走得稳的才是」全净'
 '+「老瓶装新酒，两个时代的交情」全净+「慢，是硅基城市里最贵的东西」值存活〔归基 同音族内〕）+沪语年轮句辰光→晨光〔v1 同位〕'
 '+「差之毫秒谬以全城」→妙以全程〔v1 同型〕+声明尾词「见图文页」→「建筑文件」同音重写+**章尾双钩同音代价如实**（「像档案柜的名字」→「相当暗贵的名字」'
 '+「给失败立碑」→「给失败了一杯」）+代词带 它→他 ×1（硅基徒弟章·较 ch.2 女主代词带 ~15 处收窄）+**同音噪声 43 sites/68 diff chars/553 字=字位 ≈12.3%**'
 '（char-level difflib 量化=系列带·口径分解=数字形差 3+代词带 1+沪语带 1+系列在案同音族持续〔归基×3/编冕史/探鸡×2/归鸡×2/周固/当安管/归荡者/框子城/校→笑×2/墙光/硬一声/表格/基辛/静口/旗〕）'
 '·字幕轨=edge-tts 精确直出 12/12 零损→S2 9.0；'
 '③E8 终审听审评审单 docs/reviews/review-20260925-sc00103-v3.md（R223 定标维度复用·S1=N/A 同文本律继承位/S2 9.0/S3 9.0〔2:12.2=较 v1 缩 58.0s **系列最大缩幅**=语体整句律紧凑带〕'
 '/S4 9.0+终审七席全 9.0——E8 节奏位=ch.3 两档节拍曲线〔v1 0.461/0.509→v3 0.501/0.527=节拍维持高位·缩 58.0s 下 CV 不降=紧凑不伤参差〕'
 '·E7=两代同声线纯文本层对照链·E2=事实性赛博意象优先律 ch.3 实证〔强光看不清游丝/光芯/心跳备份〕+禁俗词表零命中）；'
 '④E4 参考仪同轮回填毕（起飞 PID 62400→19:03:05 落地：**8.0 会听完+选择订阅**·**ch.2 E4 旗① 在 ch.3 未再现=系列语境兑现实证**'
 '〔R278 旗①=章尾钩抽象→本章即该钩正解展开=钩兑现章·E4 对照链 ch.2 旗→ch.3 消旗〕·**无一眼假明说=信任面四连**·旗①=彩头规矩句空泛+「心跳备份」抽象'
 '=系列语境吸收位〔ch.2 已埋彩头规矩·同文本律禁有声线改写〕·最弱=情节深度〔2:12 单集固有·M6〕·非拦截·净本 expert-verdicts/20260925-190305-E4-audience.md）；'
 '⑤**F-010 指针升 v3 处置毕**（output/finished.md：v3=产线默认·v1 标「已被取代·盘上留档」历史档·R189 SUPERSEDED 先例·R227 判据存证保留=假绿灯律①·'
 'ch.3 无 v2 中间档=两令合并一档）+audio/README v3 行升成品标/v1 行标历史档+station-reviews 三行（r280_append.py UTF-8 通道=编码律）'
 '+backlog #31 R280 收官行——**O-1756 音频重渲染腿 ch.3 收官**；'
 '⑥三探针=board 0 FAIL（exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+0 发现（弃件清账新基线维持·阻塞≠失败口径 exit 1）'
 '/loop_health 0 FAIL 18 WARN（11 log-order+7 heartbeat-gap 皆在案史实·tick279=done279 对账平·state-ts 门零红零滞后）；'
 '例行件：日报 2026-09-25+W39 周审在案不重跑·global-benchmarks 更新记录 2026-09-24 day2 ≤7 跳过刷新（下期 ~10-01）·'
 'T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·素材窗未探（实活轮生产优先·R275/R277 延续态免探针先例·下轮快速路径复核）·'
 'tokens:local=2（faster-whisper medium×1 ASR 终轨+E4 qwen2.5:14b 同轮回填·本地栈零 API token·P-54⑤ 计量律如实记）。'
 '下轮=R281 ch.4 v3 有声重渲染起链（#31 按序·稿已落盘）→ch.5 v3 稿未落（bm-a 面）=稿落即认领。收账显式列文件 commit+push。').replace('{TS}', r280_ts)

FOCUS = ('R281: ch.4 v3 有声重渲染起链（#31 按序·SC-001-04-v3.md 稿已落盘〔bm-a·commit 4e82db0〕——beats 同文本逐字'
 '〔§1.5 语体继承机检 same_text 脚本改源〕→TTS light 产线默认→S2 ai_feel 门→M4 四检〔charter §5+§1.5 叠加〕→台账四件；'
 'E8+ASR+E4+F-011 指针升 v3 处置〔v1→v3 无 v2 中间档〕=随后轮拆细）；快速路径照跑（新令/集团转办〔ledger 锚 17〕/ch.5 v3 稿落盘迹象/'
 '素材窗覆盖层关闭后安全窗复核）')

t = io.open(P, encoding='utf-8').read()

# 1) tick
old_tick = '"tick": 279,'
assert t.count(old_tick) == 1, 'tick anchor not unique'
t = t.replace(old_tick, '"tick": 280,')

# 2) focus
import re
m = re.search(r'"focus": ".*?",\n', t, re.S)
assert m, 'focus anchor missing'
t = t.replace(m.group(0), '"focus": ' + json.dumps(FOCUS, ensure_ascii=False) + ',\n')

# 3) log append
tail_old = '→ch.4 v3 起链。收账显式列文件 commit+push。"\n ],'
assert t.count(tail_old) == 1, 'log tail anchor not unique'
tail_new = ('→ch.4 v3 起链。收账显式列文件 commit+push。",\n "%s",\n ],' % LOG.replace('\\', '\\\\').replace('"', '\\"'))
t = t.replace(tail_old, tail_new)

# 4) ts + task
old_ts = '"ts": "2026-09-25 18:57:08",'
assert t.count(old_ts) == 1, 'ts anchor not unique'
t = t.replace(old_ts, '"ts": "%s",' % now)
m2 = re.search(r'"task": ".*?"\n\}', t, re.S)
assert m2, 'task anchor missing'
task_60 = LOG.split('R280: ', 1)[1][:60]
t = t.replace(m2.group(0), '"task": %s\n}' % json.dumps(task_60, ensure_ascii=False))

io.open(P, 'w', encoding='utf-8', newline='\n').write(t)

# validate
j = json.load(io.open(P, encoding='utf-8'))
print('JSON_OK tick=%d log=%d ts=%s' % (j['tick'], len(j['log']), j['ts']))
print('task:', j['task'])
