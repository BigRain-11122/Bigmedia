# E4 audience reference call - MC-20261002-REACT-v8 static hot-topic reaction card (non-registry
# seat, direct Ollama; v7 e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态热点反应卡《城市速报 008》'
    u'（1080×1080 方图·黑底；顶部标题「城市速报 008」；下面七行：'
    u'「今日热点 · B站热门 2026-10-02」'
    u'「国庆放假百万网红猫留守家中！」'
    u'「上门喂养师，能搞定我家猫咪的奇特怪癖吗？」'
    u'「逍遥轴：「节日热闹，不如在家喝喝茶」」'
    u'「烟火轴：「食堂师傅今天也得加班，做点好吃的」」'
    u'「秩序轴：「这盏灯挂得正，夜里看家里才安心」」'
    u'「夜灯员信条：「灯不问来路，只管照路。」」；'
    u'图内底部来源行「热点转述自B站热门·反应与信条皆取自虚构城市档案」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）虚构 IP，城里住着一万多名虚构居民；'
    u'这张卡是「城市速报」系列的运作方式：当天的真实热点（B站热门上一条国庆假期的新闻——百万粉丝的网红猫的主人出门度假，'
    u'请了上门喂养师假期照看猫，标题原样转述），然后由虚构城市按自己的方式「反应」——三条反应行逐字取自这座城市的居民台词库'
    u'（按性情分成烟火、秩序、求新、怀旧、侠气、逍遥六个轴），编辑从节庆假日的情境（festival 桶）里挑了三个轴位的原句：'
    u'逍遥轴是节日热闹不如在家喝喝茶；'
    u'烟火轴是食堂师傅今天也得加班做点好吃的；'
    u'秩序轴是这盏灯挂得正夜里看家里才安心；'
    u'收束行的信条出自城里一位「夜灯员」（一盏有自我意识的像素路灯，夜里护送独行客）的居民档案——'
    u'他的信条是「灯不问来路，只管照路。」'
    u'这张卡由本地渲染链自动生成，是「城市速报」系列的第八张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话、看不懂的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261002-REACT-v8 static card (cards.json + render output)'}
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
