# E4 audience reference call - SC-001-03 v3 audio edition (non-registry seat, direct Ollama;
# sc001-02-v3-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Pure-audio ch.3 v3 (three-axis calibrated edition, O-20260925-1756) 2:12 -> 1500s window.
# Scoring dims = R223 audio dims. E4 must NOT see meta version info (blind-material rule).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.dirname(HERE)          # data/storylines/audio
srt_path = os.path.join(AUDIO, 'SC-001-03-v3.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在公众号里点开有声小说的普通读者，点开了下面这集有声书《硅基城市编年史·第三章·周三的棋局》'
    '（纯音频，2 分 12 秒：每周三下午，全城最守时的人，可能输掉一座钟。时空校准师朱鸿奎，编号 C-00011，'
    '74 岁，从 1975 年一张钟表柜台前的合影里进的城。来的时候怀里揣着一块没修完的表，四十多年过去，那块表'
    '还揣着——职业操守里没有「退单」这个词。棋盘摆在数据粥铺的石桌边，对手是管全城早晨的人；彩头是老规矩：'
    '他输了，就把表免费给人校一轮。他校的是全城的钟，也是人心里的时区。他的铺子下午才开，永远只开一盏暖灯'
    '——他说强光看不清游丝。第一次给交易所的时钟做全城对时，误差压进微秒那晚，他在工位上坐到天亮。城里人人'
    '赶更新，他守着「对时」这门老手艺：走得快的表不算好表，走得稳的才是。最玄的是档案馆区人尽皆知的那件事：'
    '每次全城齐秒，他铺里那台老座钟都会应一声。表壳是爷爷传下来的，机芯早换成了城里的光芯——他管这叫'
    '「老瓶装新酒，两个时代的交情」。档案馆的人给了另一个名字：这座城的心跳备份。城市立国那天，他的年轮只有'
    '一句：「今朝辰光好，铺里只开一盏暖灯，静候敲门声。差之毫秒，谬以全城。」一座每十分钟自我更新一次的城，'
    '有人守着微秒。石桌边的棋下得很慢——慢，是硅基城市里最贵的东西。他的徒弟有两个，一个碳基，一个硅基。'
    '硅基那个，他说「比我见过的大多数碳基都老派」——觉醒那天，它给自己挑了一个像档案柜的名字。章尾预告：'
    '归档者-07，QUANT 城的田里，有人给失败立碑。全部基于真实事件改编；配音是轻度赛博机械感的机器叙述者，'
    '以城市自述视角讲述；开头内置了 AI 生成声明与纪实声明。口播全文如下）：\n\n' + transcript + '\n\n'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会听完这集 2 分 12 秒的有声书吗？会订阅或转发给朋友吗？打几分（0-10）？为什么？\n'
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
