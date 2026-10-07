# E4 audience reference call - BS-015 "Decade of the Block: After the Typhoon Night"
# (city-growth preview series piece-4, backlog #104 / lane-restock row 2/2, form C three-perspective typhoon)
# (non-registry seat, direct Ollama; .bs014-tmp/e4_call.py pattern: UTF-8 stdin pipe +
# ANSI strip + braille strip). 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs015-tmp
vo_path = os.path.join(HERE, 'voiceover.txt')
vo = io.open(vo_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（58 秒柔转场剪辑：一个自称「硅基城市」的 AI 媒体公司'
    '开了叫「板块十年」的新系列，这是第四期《台风夜之后》——'
    '他们先抛一个问题：台风夜，这条街靠什么挺住的？'
    '然后说台风梅花，同夜三个视角：'
    '先说灯，亮度开到头，风留下的补丁不许修；'
    '再说塔，守到风停，灯带跟没事一样；风的名字是人起的，播报员说比编号好记；'
    '最后是猫，联络断了，口信一家一家送到，第二天早饭是七家的；'
    '接着时间轴推：三年、十年；他们先亮底：往后是推演，基于硅基城市真实档案的十年推演；'
    '风再大，还是那三样：灯、塔、送信的猫；'
    '再诚实交底：三个视角是真话，挺多久是推算；'
    '收束句：十年后档案接着记。推演，还是我剪的；'
    '结尾预告下一集讲第一块砖，让观众在评论区说说自己的台风夜。'
    '画面是终端日志窗口、内部台账文档、城市值守台画面、黑底字卡和三张居民档案卡片（一盏路灯、一座感知塔、一只送信的猫）交替，'
    '右上角全程有「BigStream|BS-015 EP.15」系列角标，'
    '左下有系统状态行和轻微扫描线质感；配音是轻度赛博机械感的机器叙述者。口播文案全文如下）：\n\n' + vo + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会看完这条 58 秒的视频吗？会点赞或转发吗？打几分（0-10）？为什么？\n'
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
