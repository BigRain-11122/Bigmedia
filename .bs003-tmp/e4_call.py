# E4 audience reference call (non-registry seat, direct Ollama; call_expert.py call_model pattern:
# UTF-8 stdin pipe + ANSI stream-code strip + long timeout). Result -> e4-result.json beside this script.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs003-tmp
beats_path = os.path.join(ROOT, 'data', 'sources', 'bs003', 'voiceover-v5.beats.txt')
beats = io.open(beats_path, encoding='utf-8').read()

prompt = (
    '你是一名刷短视频的普通观众，刷到下面这条 60 秒竖屏视频（画面全部是真实工作电脑录屏素材：'
    'AI 公司 OS 循环日志、城市值守屏、评审台账文档，配锚点数字字卡；配音是轻度赛博机械感的机器叙述者。'
    '口播文案全文如下）：\n\n' + beats + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会看完这条视频吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b', 'material': beats_path}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    raw = p.stdout.decode('utf-8', errors='replace')
    result['verdict'] = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', raw).strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
