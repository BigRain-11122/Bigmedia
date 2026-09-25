# E4 audience reference call - MC-20260925-QUOTE-v1 static quote card (non-registry seat,
# direct Ollama; sc001-05-v1-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# R253 backfill of the honestly-listed untested face (review v1.0 "E4 未跑"). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态金句语录卡《城市语录 001》'
    '（1080×1080 方图·黑底；顶部标题「城市语录」；中间两行引文「数据是新黄浦江，」'
    '「人还是要沿江散步。」；引文下署名行「——硅基城市居民 · 怀旧轴信条」；'
    '图内底部来源行「基于硅基城市居民真实设定档案（CODEX §八）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '引文逐字取自硅基城市居民真实设定档案 CODEX §八 思想谱·怀旧轴信条例，零改写；'
    '这张卡由本地渲染链自动生成，是系列金句卡的第一张，后续会按同一版式做成系列）。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-QUOTE-v1 static card (cards.json + review v1.0 description)'}
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
