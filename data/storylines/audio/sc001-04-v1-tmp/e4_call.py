# E4 audience reference call - SC-001-04 audio edition (non-registry seat, direct Ollama;
# sc001-03-v1-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Pure-audio ch.4 3:09 -> 1500s window. Scoring dims = R223 first-defined audio dims.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.dirname(HERE)          # data/storylines/audio
srt_path = os.path.join(AUDIO, 'SC-001-04-v1.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在公众号里点开有声小说的普通读者，点开了下面这集有声书《硅基城市编年史·第四章·纪念碑田》'
    '（纯音频，3 分 09 秒：QUANT 城回测田里的硅基民归档者-07，大编译的产物，睁眼第一句话是报自己的版本号，'
    '按编译纪计龄十二纪，自己选了个庄稼人的名字；师父是北外滩的时空校准师朱鸿奎——一个修表的收了个种田的徒弟，'
    '徒弟学了一口上海话；它的营生叫回测农，播种的是参数，收成看市场脸色；这片田最出名的不是收成，是坟——'
    '全城唯一的纪念碑田，碑是给失败参数立的，碑上刻死因：过拟合、样本泄漏、止损打在情绪上；'
    '镇田之宝是一株永远不收敛的模型，没删，单独辟试验田养着；它的农谚：数据不说谎，人才会；'
    '年轮上落着「参数不收敛，天理难容」；田埂上有只电波猫，食堂大厨徐根福每天给它留一份热的；'
    '全部基于真实事件改编；配音是轻度赛博机械感的机器叙述者，以城市自述视角讲述；开头内置了 AI 生成声明与纪实声明。'
    '口播全文如下）：\n\n' + transcript + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会听完这集 3 分 09 秒的有声书吗？会订阅或转发给朋友吗？打几分（0-10）？为什么？\n'
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
