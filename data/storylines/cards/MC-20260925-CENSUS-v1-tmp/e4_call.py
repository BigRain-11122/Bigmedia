# E4 audience reference call - MC-20260925-CENSUS-v1 static census card (non-registry seat,
# direct Ollama; MC-20260925-DIGEST-v1-tmp/e4_call.py pattern R290: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 001》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 001」；下面六行居民档案：'
    '「C-00010 · 顾阿凤」「碳基市民 · 弄堂派 · 女 · 68 岁」「北外滩 · 脑环广场 · 数据粥铺摊主」'
    '「信条：「灶上留一壶，路过的都是客。」」「热心 · 起早 · 嘴甜」'
    '「全城唯一记得每个早班信使口味的人」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00010）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万个多名虚构居民；'
    '顾阿凤是城里的 68 岁早点摊主居民——蒸笼里升腾的是暖光不是白汽，四大金刚一样不少，'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00010），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第一张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-CENSUS-v1 static card (cards.json + render output)'}
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
