# E4 audience reference call - SC-001-02 audio edition (non-registry seat, direct Ollama;
# sc001-01-v1-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Pure-audio ch.2 3:26 -> 1500s window. Scoring dims = R223 first-defined audio dims.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.dirname(HERE)          # data/storylines/audio
ROOT = os.path.dirname(os.path.dirname(AUDIO))  # repo root
srt_path = os.path.join(AUDIO, 'SC-001-02-v1.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在公众号里点开有声小说的普通读者，点开了下面这集有声书《硅基城市编年史·第二章·灶头上的顾阿凤》'
    '（纯音频，3 分 26 秒：硅基城市万人库的第一位手写市民——六十八岁弄堂派早点摊阿婆顾阿凤的日常纪实——'
    '1992 年董家渡早点摊老照片里被城收留、灶火换成数据流火候一点没变、台风夜先把蒸笼绑死、'
    '给电波猫群留碎布头、年轮上落了第一句话，全部基于真实事件改编；'
    '配音是轻度赛博机械感的机器叙述者，以城市自述视角讲述；开头内置了 AI 生成声明与纪实声明。'
    '口播全文如下）：\n\n' + transcript + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会听完这集 3 分 26 秒的有声书吗？会订阅或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b', 'material': srt_path}
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
