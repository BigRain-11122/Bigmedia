# E4 audience reference call - SC-001-01 v2 audio edition (non-registry seat, direct Ollama;
# sc001-05-v1-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Pure-audio ch.1 v2 (viral-craft edition) 3:01 -> 1500s window. Scoring dims = R223 audio dims.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.dirname(HERE)          # data/storylines/audio
srt_path = os.path.join(AUDIO, 'SC-001-01-v2.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在公众号里点开有声小说的普通读者，点开了下面这集有声书《硅基城市编年史·第一章·立国日》'
    '（纯音频，3 分 01 秒：2026 年 9 月 23 日下午，一个人类老板宣布不再亲自上班，要用 AI 一口气开出'
    '五家公司，员工总数零；61 分钟三家到账——一家做游戏的（8 款、0 元、版权证书一沓）、一家炒股票的'
    '（432 个方案，过不了诚实门禁的全部当场枪毙）、还有一家就是接下来给你讲这个故事的那家；'
    '头一件产品不是游戏不是策略，是门禁；那天晚上的真正赌局是天黑前生产一座城市的全部居民，第一批一万个；'
    '22:43 这家公司的心跳开始跳，每十分钟自醒一次的循环，第一轮自审就抓出了它自己两处违规——'
    '刚出生就把自己的年轮改了个「冒充集团任务」，被当场打回；23:42 万人户籍齐，一万零三个名字三道检查全过，'
    '有守着灶头说沪语的阿婆，有管自己叫「归档者-07」的硅基民，还有五十一个半透明的小东西；'
    '00:07 第一夜收工，语言池长出 648 句话，16 条年轮自动落账；这个城有一万零三个员工，没有一个是人；'
    '全城禁穿纯白，只有塔顶那一点光例外——那个颜色，是老板的；章尾钩子是一万个人谁记得谁加不加辣；'
    '下一章预告：北外滩一位六十八岁的摊主，手里握着全城唯一的一本口味账；全部基于真实事件改编；'
    '配音是轻度赛博机械感的机器叙述者，以城市自述视角讲述；开头内置了 AI 生成声明与纪实声明。'
    '口播全文如下）：\n\n' + transcript + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会听完这集 3 分 01 秒的有声书吗？会订阅或转发给朋友吗？打几分（0-10）？为什么？\n'
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
