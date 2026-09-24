# E4 audience reference call - F-006 douyin edition (non-registry seat, direct Ollama;
# .bs001-dd-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Douyin 60s quick-cut vertical -> 1500s window (fleet 60s standard).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs001-dy-tmp
beats_path = os.path.join(ROOT, 'data', 'sources', 'bs001', 'voiceover-v11-trim.beats.txt')
beats = io.open(beats_path, encoding='utf-8').read()

prompt = (
    '你是一名刷抖音的普通观众，刷到下面这条竖屏 9:16 短视频（57 秒快剪：一个人类老板 61 分钟开了三家 AI 公司、'
    '当天翻车当天修复的全程实录。快节奏剪辑：转场+硬切+高光拍白闪，画面全部是真实工作电脑录屏素材——'
    'AI 公司 OS 循环日志、城市值守屏、像素游戏园区、剪辑网格、评审台账文档，配锚点数字字卡；'
    '配音是轻度赛博机械感的机器叙述者。口播文案全文如下）：\n\n' + beats + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会看完这条 57 秒的视频吗？会点赞或转发吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b', 'material': beats_path}
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
