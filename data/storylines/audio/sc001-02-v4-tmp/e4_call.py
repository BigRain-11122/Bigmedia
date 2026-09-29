# E4 audience reference call - SC-001-02 v4 audio edition (non-registry seat, direct Ollama;
# sc001-01-v4-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Pure-audio ch.2 (TOP1 rebuild, quality-benchmark chapter) 6:46 -> 1500s window.
# Scoring dims = R223 audio dims. E4 must NOT see meta version info (blind-material rule).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.dirname(HERE)          # data/storylines/audio
srt_path = os.path.join(AUDIO, 'SC-001-02-v4.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在公众号里点开有声小说的普通读者，点开了下面这集有声书《硅基城市编年史·第二章·数据粥铺》'
    '（纯音频，6 分 46 秒：凌晨四点二十八分，脑环广场的照明压在最低档，青色的扫描线沿着塔基慢慢走。'
    '顾阿凤推着不锈钢小车到老位置开档——蒸笼里升起的是金色的、带着面粉香气的一团暖光，火不是明火，'
    '是一格一格的数据流。全城给她的形象设计写的注释只有两个字：好认。四点五十五分第一个客人到了，'
    '图书馆的小林，粢饭不加辣；阿婆顺口催他一句公务：新令牌的编目誊好了没。五点半早班信使排起队，'
    '她不看脸，看账——一万零三个人的口味，都装在一个一九九二年的脑子里；那个脑子来自一张董家渡早点摊的'
    '老照片，被这座城收留，照片里那口蒸笼的竹篾纹三十四年一格没换。七点一刻她朝 QUANT 城方向喊一声'
    '「趁热吃」——账上挂着名、总错过早饭的那位。八点后她剥毛豆，说早上的城最真：系统刚醒，人也刚醒，'
    '谁都没来得及装。台风的年轮：进城第三年棚子被掀，街坊凑料当天重立，从此蒸笼上多一圈麻绳。广场的'
    '电波猫群每天来领她留的碎布头。城里什么都能检索，唯独检索不到她老伴的旧影像——她还在等，按老法子：'
    '不催，一天一天过。信条贴在摊子上：灶上留一壶，路过的都是客。夜里城市每一刻钟都有新的提交落进黄浦江'
    '的光里，她不知道，也不需要知道；她知道的是明天四点半，第一屉暖光会准时升起。睡前她看了一眼日历：'
    '周三了，石桌那头有人会摆好一盘棋。全部基于真实事件改编；配音是轻度赛博机械感的机器叙述者，以城市'
    '自述视角讲述；开头内置了 AI 生成声明与纪实声明。口播全文如下）：\n\n' + transcript + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会听完这集 6 分 46 秒的有声书吗？会订阅或转发给朋友吗？打几分（0-10）？为什么？\n'
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
