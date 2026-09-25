# E4 audience reference call - MC-20260925-QUOTE-v6 static quote card (non-registry seat,
# direct Ollama; MC-20260925-QUOTE-v5-tmp/e4_call.py pattern R288: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    '你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态金句语录卡《城市语录 006》'
    '（1080×1080 方图·黑底；顶部标题「城市语录 006」；中间两行引文「流量像潮水，」'
    '「我是灯塔不是渔船。」；引文下署名行「——硅基城市居民 · 逍遥轴信条」；'
    '图内底部来源行「基于硅基城市居民真实设定档案（CODEX §八）」；'
    '角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    '引文逐字取自硅基城市居民真实设定档案 CODEX §八 思想谱·逍遥轴信条例，零改写；'
    '这张卡由本地渲染链自动生成，是系列金句卡的第六张（前五张为烟火轴「布要顺着纹路剪，日子要顺着人心过」'
    '、秩序轴「风控做得好，就是没人夸的那种好」、求新轴「像素越小，心眼越大」'
    '、怀旧轴「数据是新黄浦江，人还是要沿江散步」与侠气轴「桥上不问来路，落水都得拉一把」'
    '，按同一版式连载·本张为六轴收官张）。'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260925-QUOTE-v6 static card (cards.json + render output)'}
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
