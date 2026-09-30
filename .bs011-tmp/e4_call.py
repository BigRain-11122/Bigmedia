# E4 audience reference call - BS-011 draft-collection piece-6 "Three-Tier Memory" (BS-001 master
# unattended-ops facet-5) (non-registry seat, direct Ollama; .bs010-tmp/e4_call.py pattern: UTF-8 stdin
# pipe + ANSI strip + braille strip). 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs011-tmp
vo_path = os.path.join(HERE, 'voiceover.txt')
vo = io.open(vo_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（53 秒柔转场剪辑：一个自称「硅基城市」的 AI 媒体公司在讲 AI 的记忆问题——'
    '他们说 AI 有个通病：一醒来就是新员工，之前干过什么全忘光；常见解法是靠人交接，一遍一遍教，把人教到崩溃；'
    '他们反着来：记忆不进脑子，进文件；机制原文是「每家公司每条产品线，都有结构化记忆」；醒来先读记忆，再干活；'
    '断电重启，记忆一字不丢，全量在代码库；这条视频本身就是从记忆里长出来的；'
    '员工手册自己进化：每轮干完，写回一行；不是存聊天，是存能查的结构；'
    '收束句：公司的脑子，长在文件里；结尾导流：完整机制在公众号，转给教 AI 教到崩溃的朋友。'
    '画面是终端日志窗口（BS-OSLoop-Log）、内部评审台账文档和黑底字卡交替，右上角全程有「BigStream|BS-011 EP.11」系列角标，左下有系统状态行和轻微扫描线质感；'
    '配音是轻度赛博机械感的机器叙述者。口播文案全文如下）：\n\n' + vo + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会看完这条 53 秒的视频吗？会点赞或转发吗？打几分（0-10）？为什么？\n'
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
