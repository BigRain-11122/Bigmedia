# E4 audience reference call - BS-010 draft-collection piece-5 "First Discipline" (anti-duplication iron-law
# facet, BS-002 master) (non-registry seat, direct Ollama; .bs009-tmp/e4_call.py pattern: UTF-8 stdin pipe +
# ANSI strip + braille strip). 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs010-tmp
vo_path = os.path.join(HERE, 'voiceover.txt')
vo = io.open(vo_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（58 秒柔转场剪辑：一个自称「硅基城市」的 AI 媒体公司在拆解自己公司立的规矩——'
    '他们说自己这类 AI 最容易犯的病，是热情地重造轮子；机器不知疲倦、热情过头，就是一个接一个的轮子；'
    '治法早写好了，就是他们循环的第一条纪律：反重复；铁律原文是「先读后写，能复用绝不重建，同一仓库多机退避」；'
    '机队条款：两台机器永不同时改一个代码库，同仓只留一个写手；代价判定：重造一个轮子，等于白干一轮；'
    '这条纪律正在跑，这条视频就是按它跑出来的；每一步都落账、日志可查，纪律破没破，账本说了算；'
    '纪律边界：反重复不是不创新，力气要花在没造过的东西上；收束句：去造下一个轮子，别重造这一个；结尾导流：完整铁律在公众号，转给最爱重复造轮子的朋友。'
    '画面是终端日志窗口（BS-OSLoop-Log）、内部评审台账文档和黑底字卡交替，右上角全程有「BigStream|BS-010 EP.10」系列角标，左下有系统状态行和轻微扫描线质感；'
    '配音是轻度赛博机械感的机器叙述者。口播文案全文如下）：\n\n' + vo + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
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
