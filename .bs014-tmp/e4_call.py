# E4 audience reference call - BS-014 "Decade of the Block: The Street's Catchphrases"
# (city-growth preview series piece-3, backlog #103 / lane-restock row 1/2, form C quote-digest)
# (non-registry seat, direct Ollama; .bs013-tmp/e4_call.py pattern: UTF-8 stdin pipe +
# ANSI strip + braille strip). 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs014-tmp
vo_path = os.path.join(HERE, 'voiceover.txt')
vo = io.open(vo_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（57 秒柔转场剪辑：一个自称「硅基城市」的 AI 媒体公司'
    '开了叫「板块十年」的新系列，这是第三期《这条街的口头禅》——'
    '他们先抛一个问题：哪句口头禅，是从这条街传出去的？'
    '然后系统回语录库，亮出六句话，一句一个脾气：'
    '「数据是新黄浦江，人还是要沿江散步」「布要顺着纹路剪，日子要顺着人心过」'
    '「风控做得好，就是没人夸的那种好」「桥上不问来路，落水都得拉一把」；'
    '接着时间轴往前推：三年，十年；他们先亮底：这是推演，不是实录——基于硅基城市真实档案的十年推演；'
    '推演十年后的街坊：谁搬走谁顺路捎带，新街坊接着教；'
    '再诚实交底：六句是档案真话，传多远是推算的；'
    '收束句：十年后哪句真传出去，档案接着记——还是我剪的；'
    '结尾预告下一集讲台风夜之后，让观众在评论区报一句自己街上的口头禅。'
    '画面是终端日志窗口、内部台账文档、城市值守台画面、黑底字卡和一张居民档案卡片交替，'
    '右上角全程有「BigStream|BS-014 EP.14」系列角标，'
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
