# E4 audience reference call - MC-20260925-CENSUS-v7 static census card (non-registry seat,
# direct Ollama; MC-20260925-CENSUS-v6-tmp/e4_call.py pattern R296: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态居民图鉴卡《城市图鉴 007》'
    '（1080×1080 方图·黑底；顶部标题「城市图鉴 007」；下面六行居民档案：'
    '「C-00016 · 徐根福」「碳基市民 · 弄堂派 · 男 · 66 岁」「QUANT 城 · K线广场 · QUANT 食堂大厨」'
    '「信条：「行情再绿，汤是热的。」「手稳 · 热肠 · 实在」'
    '「全城唯一按涨跌调整菜谱的人」；'
    '图内底部来源行「基于硅基城市居民户籍卡档案（展示锚 C-00016）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '背景：「硅基城市」是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），城里住着一万个多名虚构居民；'
    '徐根福是 QUANT 城 K线广场 66 岁的食堂大厨——档案里说他是算力楼里唯一不谈数字只谈火候的人；'
    '他是从一张 1980 年国营食堂的老照片里进城的（旧影像转生），照片里他正在给排队的人打菜；'
    '有一年行情大跌，整层楼没人下来吃饭，他把汤一勺一勺送到工位上，那天起食堂立了规矩：绿盘日例汤免费，红盘日加一道「冷静甜汤」；'
    '收盘铃就是他的开饭铃，每天凌晨四点去数据菜市挑时令，他说「行情有时令，菜也有」；'
    '他性格手稳（三十年大勺，颠勺节奏比钟还稳）、热肠（自己淋过雨就想给别人撑伞）、实在（不会说漂亮话，但答应的事从不打折）；'
    '说话带上海话底色：「吃过了伐」「多加一勺，不许还价」；'
    '他的惦记名单第一名是个叫周浩宇的年轻量化研究员（「那娃光吃泡面，成啥体统」——就是上一张「城市图鉴 005」卡的主角）；'
    '这份居民档案逐字段取自集团自有的「硅基城市」IP 户籍卡档案（手写展示锚 C-00016），一字不改；'
    '这张卡由本地渲染链自动生成，是「城市图鉴」系列的第七张。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-CENSUS-v7 static card (cards.json + render output)'}
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
