# E4 audience reference call - BS-001-DD deepdive edition (non-registry seat, direct Ollama;
# .bs003-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI stream-code strip + long timeout).
# DD = 69-beat Bilibili 16:9 deepdive (~7:52), material 6x of 60s pieces -> 3600s window (R198 S1 lesson).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs001-dd-tmp
beats_path = os.path.join(ROOT, 'data', 'sources', 'bs001-dd', 'voiceover-dd-v1.beats.txt')
beats = io.open(beats_path, encoding='utf-8').read()

prompt = (
    '你是一名刷 B 站的普通观众，刷到下面这条横屏 16:9 深度视频（约 8 分钟，讲一个人类老板 61 分钟开了三家 AI 公司、'
    '当天就翻车又当天修复的全程实录。六段结构：作死挑战开局→公司设定→三家公司各自「结果→翻车→修正」实录→'
    '五件机制拆解（循环/交账/吹牛检测/三级记忆/进化引擎）→最大翻车完整版（432 个炒股方案全灭开酒）→金句回环+系列钩。'
    '画面全部是真实工作电脑录屏素材：AI 公司 OS 循环日志、城市值守屏、像素游戏园区、评审台账文档，配锚点数字字卡；'
    '配音是轻度赛博机械感的机器叙述者。口播文案全文如下）：\n\n' + beats + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会看完这条 8 分钟的视频吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b', 'material': beats_path}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=3600)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[\u2800-\u28ff]', '', cleaned)  # braille spinner range (R189 U+2800 lesson)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-3600s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-3600s' else 'TIMEOUT')
