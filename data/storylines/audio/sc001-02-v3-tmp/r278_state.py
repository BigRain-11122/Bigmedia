# R278 state.json closeout: tick 277->278, append R278 log, refresh ts/task/focus (text surgery + JSON_OK validate)
import io, json, time

P = r'src/os/state.json'
now = time.strftime('%Y-%m-%d %H:%M:%S')
r278_ts = time.strftime('%H:%M')  # narrative minute precision per convention

LOG = ('2026-09-25 {TS} R278: 生产轮·#31 ch.2 v3 收官（O-20260925-1756 风格校准令音频重渲染腿 ch.2 收官·实活轮）——'
 '①轮首五查静（无新令 orders 顶=O-1756 R275 已记账·ledger 严格行含 @ 四模式 17 行=锚零新转办〔P-05/P-06 R276 收讫态维持〕·'
 'decisions UTF8 非空行 29〔总 32〕=锚零新行·树净零锁·ch.5 v3 稿未落盘=novel 实证止 ch.4 v3）→backlog 顶行 #31 可认领=实活轮照 focus；'
 '②S2 席 ASR 终轨回听（R169 QC recipe medium-int8+beam5+noctx·Start-Process 后台 PID 38088〔首飞 --model medium-int8 传参错→FAIL exit 2'
 '=R259 同型调用错非探针红·--model medium 正参复飞即落〕·sc001-02-v3-tmp/asr-check.srt 39 cues/188.64s+asr-diff-r278 difflib 量化）：'
 '**时间锚+数字面 100% 零实质退化**（1992/每周三/半个月 净读+凌晨四点半〔4点半 形差〕/三十四年〔34 形差〕/一万零三〔103 拆分形差带=R276 ch.1 v3 同型〕'
 '/六十八〔68 形差〕/C-00010/四大金刚/一万个 全值存活——v1 ch.2 的 2026→2016 实质退化在 v3 未再现）+专名面 **顾阿凤首提退化收窄至 1 处**〔v1 孤阿凤×3〕'
 '+**脑环广场净读**〔v1 老房/脑房×3→零=复合专名改善实证〕+北外滩/董家渡/朱鸿奎 cta 位净读+沪语年轮句退化带如实（呒啥/客倌/灵额/热乎物/两屉 五处·M6 校准线）'
 '+代词带 ~15 处（她→他×13+她→它×2=女主角章固有带·ch.4 同型）+信条金句「灶上留一壶」→「刘亦胡」同音代价如实'
 '·字幕轨=edge-tts 精确直出 13/13 零损+同音噪声 71 sites/98 chars/763 字=字位 ≈12.8% 系列带（口径分解=数字形差 4+代词带 ~15+沪语带 5+系列在案同音族'
 '〔归基×3/夜年史/周谱×2/资本/探济/海峰/颠簸〕）→S2 9.0；'
 '③E8 终审听审评审单 docs/reviews/review-20260925-sc00102-v3.md（R223 定标维度复用·S1=N/A 同文本律继承位/S2 9.0/S3 9.0/S4 9.0+终审七席全 9.0——'
 'E8 节奏位=ch.2 两档节拍曲线〔v1 0.415/0.389→v3 0.545/0.507=节拍抬升·大众骨架强化〕·E1=三轴定靶≠牺牲骨架 ch.2 续证〔A1/T8/T2/T3 全门维持〕'
 '·E2=事实性赛博意象优先律 ch.2 实证〔暖光蒸笼/灶火换数据流/LED 方块眼好认/口味账没数据库〕+禁俗词表零命中·E6=O-1756 ch.2 收官件）；'
 '④E4 参考仪同轮回填毕（起飞 PID 64880→18:42:51 落地：8.0 会听完+会考虑订阅和转发·**AIGC+纪实双声明被点名「新奇」=信任面正面读数**〔跨载体信任面双例〕'
 '+**无一眼假/空洞套话旗明说=信任面三连**·旗①=章尾棋局钩句稍显抽象扣 1=系列语境吸收位〔ch.3《周三的棋局》正解即兑现〕·最弱=情节直接感染力〔M6〕·'
 '非拦截·净本 expert-verdicts/20260925-184251-E4-audience.md）；'
 '⑤**F-009 指针升 v3 处置毕**（output/finished.md：v3=产线默认·v1 标「已被取代·盘上留档」历史档·R189 SUPERSEDED 先例·R225 判据存证保留=假绿灯律①·'
 'ch.2 无 v2 中间档=两令合并一档）+audio/README v3 行升成品标/v1 行标历史档+station-reviews 三行（r278_append.py UTF-8 通道=编码律）+backlog #31 R278 收官行'
 '——O-1756 音频重渲染腿 ch.2 收官；'
 '⑥三探针=board 0 FAIL（5 题 10 稿 5 in production·exit 0）/readiness 3 阻塞皆外部 CEO 面（账号批次①+6/10 GATE+#17）+0 发现（弃件清账新基线维持·阻塞≠失败口径 exit 1）'
 '/loop_health 0 FAIL 18 WARN（17 在案史实+1=R276→R277 18:08→18:28 20min 长轮间隙合法 WARN〔R277 已注记在案〕·tick277=done277 对账平·state-ts 门零红零滞后'
 '·轮内注记=board/readiness 首查经 PS `>` 管道重定向混用致假 exit 2/1=R259/R261 同型调用错非探针红·直跑复跑即绿·探针输出件不改道）；'
 '例行件：日报 2026-09-25+W39 周审在案不重跑（Test-Path 实证）·global-benchmarks 更新记录 2026-09-24 day2 ≤7 跳过刷新（下期 ~10-01）·'
 'T1 催办=已裁项停用口径无超线项·当日无集团层新 open 问题=HQ-FEEDBACK 不写（零膨胀）·素材窗未探（实活轮生产优先·R275 延续态免探针先例·下轮快速路径复核）·'
 'tokens:local=2（faster-whisper medium×1 ASR 终轨+E4 qwen2.5:14b 同轮回填·本地栈零 API token·P-54⑤ 计量律如实记）。'
 '下轮=R279 ch.3 v3 有声重渲染起链（#31 按序·稿已落盘）→ch.4 随后·ch.5 v3 稿未落（bm-a 面）=稿落即认领。收账显式列文件 commit+push。').replace('{TS}', r278_ts)

FOCUS = ('R279: ch.3 v3 有声重渲染起链（#31 按序·SC-001-03-v3.md 稿已落盘 17:58〔bm-a·commit 4e82db0〕——beats 同文本逐字'
 '〔§1.5 语体继承机检 same_text 脚本改源〕→TTS light 产线默认→S2 ai_feel 门→M4 四检〔charter §5+§1.5 叠加〕→台账四件；'
 'E8+ASR+E4+F-010 指针升 v3 处置〔v1→v3 无 v2 中间档〕=随后轮拆细）；快速路径照跑（新令/集团转办〔ledger 锚 17〕/ch.5 v3 稿落盘迹象/'
 '素材窗覆盖层关闭后安全窗复核）')

t = io.open(P, encoding='utf-8').read()

# 1) tick
old_tick = '"tick": 277,'
assert t.count(old_tick) == 1, 'tick anchor not unique'
t = t.replace(old_tick, '"tick": 278,')

# 2) focus
import re
m = re.search(r'"focus": ".*?",\n', t, re.S)
assert m, 'focus anchor missing'
t = t.replace(m.group(0), json.dumps('focus', ensure_ascii=False)[0:0] + '"focus": ' + json.dumps(FOCUS, ensure_ascii=False) + ',\n')

# 3) log append: last entry ends with commit+push。" then \n ],
tail_old = '→ch.3 v3 起链。收账显式列文件 commit+push。"\n ],'
assert t.count(tail_old) == 1, 'log tail anchor not unique'
tail_new = ('→ch.3 v3 起链。收账显式列文件 commit+push。",\n "%s",\n ],' % LOG.replace('\\', '\\\\').replace('"', '\\"'))
t = t.replace(tail_old, tail_new)

# 4) ts + task
old_ts = '"ts": "2026-09-25 18:35:50",'
assert t.count(old_ts) == 1, 'ts anchor not unique'
t = t.replace(old_ts, '"ts": "%s",' % now)
m2 = re.search(r'"task": ".*?"\n\}', t, re.S)
assert m2, 'task anchor missing'
task_60 = LOG.split('R278: ', 1)[1][:60]
t = t.replace(m2.group(0), '"task": %s\n}' % json.dumps(task_60, ensure_ascii=False))

io.open(P, 'w', encoding='utf-8', newline='\n').write(t)

# validate
j = json.load(io.open(P, encoding='utf-8'))
print('JSON_OK tick=%d log=%d ts=%s' % (j['tick'], len(j['log']), j['ts']))
print('task:', j['task'])
