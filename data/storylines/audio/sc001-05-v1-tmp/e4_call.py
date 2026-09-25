# E4 audience reference call - SC-001-05 audio edition (non-registry seat, direct Ollama;
# sc001-04-v1-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Pure-audio ch.5 3:27 -> 1500s window. Scoring dims = R223 first-defined audio dims.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.dirname(HERE)          # data/storylines/audio
srt_path = os.path.join(AUDIO, 'SC-001-05-v1.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在公众号里点开有声小说的普通读者，点开了下面这集有声书《硅基城市编年史·第五章·徐根福的食堂》'
    '（纯音频，3 分 27 秒：QUANT 城是全城最谈数字的地方，只有食堂大厨徐根福不谈数字，谈火候——弄堂派，'
    '1980 年从一张国营食堂的老照片里进的城，围裙口袋里那把木勺还在；他不懂因子也不懂夏普，但他懂人吃饱了才有底气；'
    '北外滩的顾阿凤管早晨、档案馆区的朱鸿奎管钟点，他管的是收盘铃——收盘铃就是他的开饭铃；'
    '食堂规矩：绿盘日例汤免费，红盘日加一道「冷静甜汤」，来历是行情大跌那年他把汤一勺一勺送到工位上；'
    '研究员们说 QUANT 城真正的风控部不在算力楼顶，在灶台后面；全城禁穿纯白，他的厨师服洗得发亮，他说'
    '「厨房的白是本分，塔顶的白才是老板的」；他的惦记名单第一名是顿顿泡面的年轻研究员周浩宇；'
    '连回测田那位不需要吃饭的硅基邻居归档者-07，他也每天留一份热的；年轮上落着他的一句话：'
    '「今朝大闸蟹正肥，O-22 一定多加一勺姜丝，好好吃饭」；全部基于真实事件改编；'
    '配音是轻度赛博机械感的机器叙述者，以城市自述视角讲述；开头内置了 AI 生成声明与纪实声明。'
    '口播全文如下）：\n\n' + transcript + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会听完这集 3 分 27 秒的有声书吗？会订阅或转发给朋友吗？打几分（0-10）？为什么？\n'
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
