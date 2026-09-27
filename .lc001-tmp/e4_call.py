# E4 audience reference call - LC-001 L-card clip-cut edition (non-registry seat, direct Ollama;
# .bs001-v15-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Shipinhao 60s soft-cut vertical clip-cut per #79 piece-1 (release-schedule D15 slot) -> 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .lc001-tmp
vo_path = os.path.join(HERE, 'voiceover.txt')
vo = io.open(vo_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（58 秒柔转场剪辑：讲硅基城市里一位 66 岁的食堂大厨徐根福——'
    '全城唯一按股市涨跌调菜谱的人：行情绿了人心发慌他例汤免费，行情红了加一道「冷静甜汤」，大跌那年把汤一勺一勺送上工位。'
    '画面全程是这位居民的「城市图鉴」档案卡特写微动镜头——黑底白字六行档案：钩子行、物种年龄职业、城区、信条、性格关键词，'
    '配锚点数字字卡；右上角全程有「BigStream|拆条 001·源城市图鉴 007」系列角标，左下有系统状态行和轻微扫描线质感；'
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
