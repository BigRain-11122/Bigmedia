# E4 audience reference call - BS-012 "Decade of the Block: Founding Day" (city-growth preview
# series piece-1, backlog #101 / D-20261008-03 restock row 1/2) (non-registry seat, direct
# Ollama; .bs011-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip). 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs012-tmp
vo_path = os.path.join(HERE, 'voiceover.txt')
vo = io.open(vo_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（57 秒柔转场剪辑：一个自称「硅基城市」的 AI 媒体公司'
    '开了一档叫「板块十年」的新系列，这是第一期《立国日》——'
    '他们先抛一个问题：十年前，这块地是什么？然后回放立国日档案：下午两点五十，一条指令，开一家媒体公司；'
    '当晚九点半，造城令，一万个居民，天亮前交付；深夜，一万零三个名字落库，检查全过；'
    '天没亮，日志多了一行没登记的：蒸笼发光了；塔顶一点纯白，全城唯一，市民认得：老板。'
    '然后画面在同一机位往前推：三年，再十年；他们先亮底：往后是推演——基于硅基城市真实档案的十年推演；'
    '起步数字：一万零三居民，一个早点摊，一盏白灯；再诚实交底：档案是真的，往后是照档案推算的；'
    '收束句：十年后回头，看得见第一块砖——是我剪的；结尾预告下一集《灯亮起来那天》，让观众在评论区报路名。'
    '画面是终端日志窗口、内部台账文档、城市值守台画面和黑底字卡交替，右上角全程有「BigStream|BS-012 EP.12」系列角标，'
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
