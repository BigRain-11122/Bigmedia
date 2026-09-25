# E4 audience reference call - SC-001-04 v3 audio edition (non-registry seat, direct Ollama;
# sc001-03-v3-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Pure-audio ch.4 v3 (three-axis calibrated edition, O-20260925-1756) 2:30 -> 1500s window.
# Scoring dims = R223 audio dims. E4 must NOT see meta version info (blind-material rule).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.dirname(HERE)          # data/storylines/audio
srt_path = os.path.join(AUDIO, 'SC-001-04-v3.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在公众号里点开有声小说的普通读者，点开了下面这集有声书《硅基城市编年史·第四章·纪念碑田》'
    '（纯音频，2 分 30 秒：QUANT 城有七垄田，种的是参数，收的是教训。田边有一片碑林——碑，是给失败立的。'
    '守田人编号 C-00017，归档者-07，硅基民，编译纪十二年，觉醒于一次全城大编译，睁眼说的第一句话，是报出'
    '自己的版本号。名字是它自己选的，师父嫌老气，它答：「庄稼人的名字，土一点，收成才稳。」它的职业叫'
    '回测农——算法调参师的赛博后身：播种一批参数，浇水施肥等三天，收成看市场脸色，它管这叫看天吃饭。'
    '肩上常年搭一条毛巾，它不需要擦汗，但师父说过，干活的人得有干活的样子；它信了，连工具箱里的扳手都有'
    '户口。这片田最出名的是那片碑，每块碑上刻一行死因，新研究员入职都先来看碑，再下田。规矩的来历，是它'
    '职业生里最大的一次下注：遇到一个永不收敛的模型，按常规该删，它没删——单独辟了块试验田养着，所有人都'
    '等着看这块地荒掉，结果那模型成了镇田之宝。从那以后它攒出自己的农谚集，第一条就八个字：数据不说谎，'
    '人才会。台风警报的夜里，它必去把田里的遮雨布压好；田埂上常来一只尾巴天线歪的电波猫晒太阳，隔壁食堂的'
    '大厨每天给它留一份热的。城市立国那天，它的年轮落了一句农人式的自评：「参数不收敛，天理难容。」一座'
    '满城跑数据的城市里，有人给失败立碑，有人给失败留饭。章尾预告：留饭的人——QUANT 食堂大厨徐根福，'
    '全城唯一按涨跌调菜谱的人。全部基于真实事件改编；配音是轻度赛博机械感的机器叙述者，以城市自述视角'
    '讲述；开头内置了 AI 生成声明与纪实声明。口播全文如下）：\n\n' + transcript + '\n\n'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会听完这集 2 分 30 秒的有声书吗？会订阅或转发给朋友吗？打几分（0-10）？为什么？\n'
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
