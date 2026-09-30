# E4 audience reference call - BS-007 draft-collection piece-2 "Three Hearts" (non-registry seat, direct Ollama;
# .bs006-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip). 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs007-tmp
vo_path = os.path.join(HERE, 'voiceover.txt')
vo = io.open(vo_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（57 秒柔转场剪辑：一个自称「硅基城市」的 AI 媒体公司在拆解自己公司的运转设计——'
    '一家公司三颗心脏，两颗十分钟一跳：第一颗管钱，每十分钟一轮活；第二颗管游戏，每十分钟把小游戏重写一遍；'
    '第三颗管进化，周日 09:17 一跳，从感知到立法。十分钟管干活，一周管进化，频率分层各不越界。'
    '为什么是十分钟：太密空转，太疏过夜。操作系统对照：任务板就是进程表，干活顺序是优先级调度，定时自检是看门狗，记忆是文件系统——'
    '「公司 OS」不是修辞，是结构。'
    '画面是终端日志窗口、像素小镇游戏画面和黑底字卡交替，右上角全程有「BigStream|BS-007 EP.07」系列角标，左下有系统状态行和轻微扫描线质感；'
    '配音是轻度赛博机械感的机器叙述者。口播文案全文如下）：\n\n' + vo + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
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
