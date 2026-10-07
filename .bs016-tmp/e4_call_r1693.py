# E4 audience reference call - BS-016 "Decade of the Block: The First Brick"
# (city-growth preview series piece-5 FINAL, backlog #105 / lane-restock runner-up row,
#  form A+C archive-retrieval flashback, Q10 ten-question series closure)
# (non-registry seat, direct Ollama; .bs015-tmp/e4_call_r1690.py pattern: UTF-8 stdin pipe +
# ANSI strip + braille strip). 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs016-tmp
vo_path = os.path.join(HERE, 'voiceover.txt')
vo = io.open(vo_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（58 秒柔转场剪辑：一个自称「硅基城市」的 AI 媒体公司'
    '开了叫「板块十年」的新系列，这是收官第五期《第一块砖》——'
    '他们先抛系列最后一问：十年后回头看，谁还记得第一块砖？'
    '然后系统回城市档案：没有砖，是三样东西——'
    '一条指令：下午两点五十，开一家媒体公司；'
    '一万个名字：一万零三落库，城有了人；'
    '最软的一块：蒸笼发光，塔顶纯白，城有了自己的事；'
    '说问档案一翻就到；'
    '时间轴倒着放：十年、三年、回到立国日；'
    '接着先亮底：往后是推演，基于硅基城市真实档案的十年推演；'
    '说推演里砖都还在，谁砌的都有名有姓；'
    '再交底：砖是比喻，档案是真的，一笔一笔都在；'
    '然后兑现系列第一集埋下的话：十年后回头，看得见第一块砖——兑现了，还是我剪的；'
    '结尾五问收官，让观众在评论区说说自己的第一块砖。'
    '画面是终端日志窗口、内部台账文档、城市值守台画面、剪辑网格、一张居民档案卡（新街坊接着教）和黑底字卡交替，'
    '右上角全程有「BigStream|BS-016 EP.16」系列角标，'
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
