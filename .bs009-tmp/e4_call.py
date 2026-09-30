# E4 audience reference call - BS-009 draft-collection piece-4 "First Red Line" (non-registry seat, direct Ollama;
# .bs008-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip). 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs009-tmp
vo_path = os.path.join(HERE, 'voiceover.txt')
vo = io.open(vo_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（54 秒柔转场剪辑：一个自称「硅基城市」的 AI 媒体公司在拆解自己公司立的规矩——'
    '量化行业满屏「年化 30%」、条条曲线漂亮，他们点破：参数在历史数据里反复调试、直到曲线变漂亮，这有名字，叫曲线拟合；'
    '把拟合当优势卖是另一回事，是他们立的第一条红线，红线原文「不许把过拟合，当优势出售」；'
    '曲线漂亮不等于有本事；把修出来的当优势卖，日志判定：这叫骗自己；这条红线先管住自己；先证明你没在骗自己，再谈策略；'
    '在这标准下，难看不是失败，是系统在说真话；曲线可以修漂亮，红线只有一句：拟合不卖；结尾声明「不构成投资建议」，红线全文在公众号。'
    '画面是终端日志窗口、内部台账清单和黑底字卡交替，右上角全程有「BigStream|BS-009 EP.09」系列角标，左下有系统状态行和轻微扫描线质感；'
    '配音是轻度赛博机械感的机器叙述者。口播文案全文如下）：\n\n' + vo + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会看完这条 54 秒的视频吗？会点赞或转发吗？打几分（0-10）？为什么？\n'
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
