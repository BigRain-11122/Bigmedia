# E4 audience reference call - MC-20260930-REACT-v6 static hot-topic reaction card (non-registry
# seat, direct Ollama; v5 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round-async E4 for hit-chain v1.0 series production piece. Non-blocking seat.
# P-1 anti-cliche line-selection law v2 pilot FINAL piece 2/2 - verdict row feeds the
# pilot's three-question final judgment (queue section D) next round backfill.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态热点反应卡《城市速报 006》'
    u'（1080×1080 方图·黑底；顶部标题「城市速报 006」；下面六行：'
    u'「今日热点 · 知乎热榜 2026-09-30」'
    u'「8.59 元香菜遭「仅退款」，商家驱车千里跨省讨回」'
    u'「烟火轴：「青菜萝卜两厢情愿，咱这价格明镜儿似的」」'
    u'「侠气轴：「邻里间，小纠纷早化解」」'
    u'「秩序轴：「摊贩出摊了，规矩不能少，日子得按部就班」」'
    u'「风控官信条：「红灯是为所有人亮的，包括我。」」；'
    u'图内底部来源行「热点转述自知乎热榜·反应与信条皆取自虚构城市档案」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）虚构 IP，城里住着一万多名虚构居民；'
    u'这张卡是「城市速报」系列的运作方式：当天的真实热点（知乎热榜上一条电商新闻——一位商家卖了 8.59 元的香菜遭遇平台「仅退款」，'
    u'他开车跨省跑了一千多公里去把这 8.59 元讨了回来，标题原样转述），然后由虚构城市按自己的方式「反应」——'
    u'三条反应行逐字取自这座城市的居民台词库（按性情分成烟火、侠气、秩序等六个轴），编辑从早市场景的情境（morning 桶）里挑了三个轴位的原句：'
    u'烟火轴是早市摊主说自家价格公道（青菜萝卜两厢情愿）；'
    u'侠气轴是城里人习惯把小纠纷早早化解；'
    u'秩序轴是摊贩出摊也得讲规矩；'
    u'收束行的信条出自城里 QUANT 城风控高地的一位风控官的居民档案——她的职业就是替全城把风险关拦在门外，'
    u'她的信条是「红灯是为所有人亮的，包括我。」'
    u'这张卡由本地渲染链自动生成，是「城市速报」系列的第六张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话、看不懂的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260930-REACT-v6 static card (cards.json + render output)'}
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
