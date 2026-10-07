# E4 audience reference call - BS-013 "Decade of the Block: The Night the Lights Came On"
# (city-growth preview series piece-2, backlog #102 / D-20261008-03 restock row 2/2)
# (non-registry seat, direct Ollama; .bs012-tmp/e4_call.py pattern: UTF-8 stdin pipe +
# ANSI strip + braille strip). 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs013-tmp
vo_path = os.path.join(HERE, 'voiceover.txt')
vo = io.open(vo_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（57 秒柔转场剪辑：一个自称「硅基城市」的 AI 媒体公司'
    '开了叫「板块十年」的新系列，这是第二期《灯亮起来那天》——'
    '他们先抛一个问题：路灯比十年前，亮了几度？然后回放档案：立国日那晚，全城只有一盏灯；'
    '灯亮起来那天其实是感知网调试夜：对频那秒，编号十四；它发明了一个词叫「交晨」——把夜，交给早晨；'
    '它用光说话：暖黄是平常心，橙红是遇上事；夜宵摊多亮半档，让摊主知道有人看见他的辛苦；'
    '然后画面在同一机位往前推：三年，再十年；他们先亮底：往后是推演——基于硅基城市真实档案的十年推演；'
    '起步数字：立国日一盏，守夜灯灵五盏——它是老大；再诚实交底：一盏到五盏是真数，往后照档案推算；'
    '收束句：十年后，看得见灯亮起来那天——还是我剪的；结尾预告下一集讲这条街的口头禅，让观众在评论区报路名。'
    '画面是终端日志窗口、内部台账文档、城市值守台画面和黑底字卡交替，右上角全程有「BigStream|BS-013 EP.13」系列角标，'
    '左下有系统状态行和轻微扫描线质感；配音是轻度赛博机械感的机器叙述者。口播文案全文如下）：\n\n' + vo + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会看完这条 57 秒的视频吗？会点赞或转发吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话、听不懂的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b', 'material': vo_path}
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
