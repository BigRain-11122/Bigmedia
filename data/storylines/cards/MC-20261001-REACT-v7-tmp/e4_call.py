# E4 audience reference call - MC-20261001-REACT-v7 static hot-topic reaction card (non-registry
# seat, direct Ollama; v6 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round-async E4 for hit-chain v1.0 series production piece. Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态热点反应卡《城市速报 007》'
    u'（1080×1080 方图·黑底；顶部标题「城市速报 007」；下面七行：'
    u'「今日热点 · 知乎热榜 2026-10-01」'
    u'「如何看待江苏高考接近满分记叙文」'
    u'「《衬衫的价格为 9 镑 15 便士》火了」'
    u'「怀旧轴：「老街的灯光，照亮了我半辈子的梦」」'
    u'「逍遥轴：「梦里常回，那些年的灯与影」」'
    u'「烟火轴：「夜深了，人散了，摊位上还留着烟火味」」'
    u'「编年史馆员信条：「城市不会忘记，除非我们偷懒。」」；'
    u'图内底部来源行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）虚构 IP，城里住着一万多名虚构居民；'
    u'这张卡是「城市速报」系列的运作方式：当天的真实热点（知乎热榜上一条教育新闻——江苏高考一篇接近满分的记叙文，'
    u'题目用了课本里那句旧英语听力台词「衬衫的价格为 9 镑 15 便士」，一句话引发一代人的共鸣，标题原样转述），'
    u'然后由虚构城市按自己的方式「反应」——三条反应行逐字取自这座城市的居民台词库（按性情分成怀旧、逍遥、烟火等六个轴），'
    u'编辑从夜深回望记忆的情境（night 桶）里挑了三个轴位的原句：'
    u'怀旧轴是老街灯光照见半辈子的梦；'
    u'逍遥轴是梦里常回那些年的灯与影；'
    u'烟火轴是人散了摊位上还留着烟火味；'
    u'收束行的信条出自城里一位编年史馆员的居民档案——他的职业就是替全城把每天的日常誊进档案，'
    u'他的信条是「城市不会忘记，除非我们偷懒。」'
    u'这张卡由本地渲染链自动生成，是「城市速报」系列的第七张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话、看不懂的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261001-REACT-v7 static card (cards.json + render output)'}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[\u2800-\u28ff]', '', cleaned)  # braille spinner range (R189 U+2800 lesson)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
