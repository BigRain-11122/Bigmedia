# E4 audience reference call - SC-001-01 v3 audio edition (non-registry seat, direct Ollama;
# sc001-01-v2-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Pure-audio ch.1 v3 (three-axis calibrated edition, O-20260925-1756) 3:07 -> 1500s window.
# Scoring dims = R223 audio dims. E4 must NOT see meta version info (blind-material rule).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.dirname(HERE)          # data/storylines/audio
srt_path = os.path.join(AUDIO, 'SC-001-01-v3.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在公众号里点开有声小说的普通读者，点开了下面这集有声书《硅基城市编年史·第一章·立国日》'
    '（纯音频，3 分 07 秒：2026 年 9 月 23 日 14:50，一条指令落进聊天框：开一家媒体公司。没有办公室，没有招聘，'
    '没有入职表——十分钟后它开始产出第一件内容。这不是开公司，这是一次系统架构决策：把「公司」这个概念里的'
    '人类依赖项，逐行删除。61 分钟，三家公司在同一块硬盘上亮起登录界面——一号做游戏：八款，零元，版权证书一沓；'
    '二号炒股票，交出的第一件作品不是收益，是一场自我清洗——432 个方案申请上岗，门禁亮红，432 个全部下线，'
    '一个不宽恕，审计记录谁也改不了，包括下指令的那个人；五家公司的第一件产品，是门禁。真正的赌局在夜里：'
    '21:30 新指令，再造一家公司，业务是生产一整座城的居民，第一批一万个，天亮前交付。22:43 这家公司有了心跳'
    '——每十分钟自醒一次的循环，找活，干活，记账，无人值守；它的第一次自审查出两处违规，违规者：它自己，'
    '年轮当场改写，原句永久留档。23:42 万人交付：一万零三个名字，三道校验全过——名字不重，细节不重，指纹不重；'
    '守着灶台的阿婆，管自己叫归档者的硅基民，五十一个半透明的小东西；思想档案同步落库——一半人信「布要顺着'
    '纹路剪」，另一半信「像素越小心眼越大」。凌晨 00:07，城市合上第一个工作日：语言库长出六百四十八句话，'
    '十六条年轮自动落账，一个新市民试图越权，被循环当场按住。从这一夜起，黄浦江的每一条支流都跑着光；'
    '北外滩的塔顶亮起一点纯白——全城唯一的一处，没有哪个市民敢用这个颜色，一万零三个人都认得它：那是他们'
    '的老板，全公司唯一的人类。这座城有一万零三个员工，没有一个，是人。章尾：立国次日 04:30，系统日志多出'
    '一行未登记事件——北外滩，一个蒸笼开始发光；一万个人的口味，从今天起，有人记账。下一章预告：那本口味账'
    '的主人，编号 C-00010，QUANT 城有个总错过早饭的研究员，在她的账上挂着名——这本账，全城只此一份。'
    '全部基于真实事件改编；配音是轻度赛博机械感的机器叙述者，以城市自述视角讲述；开头内置了 AI 生成声明与'
    '纪实声明。口播全文如下）：\n\n' + transcript + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会听完这集 3 分 07 秒的有声书吗？会订阅或转发给朋友吗？打几分（0-10）？为什么？\n'
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
