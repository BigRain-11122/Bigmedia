# E4 audience reference call - F-002 v15 remake edition (non-registry seat, direct Ollama;
# .bs001-v15-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Shipinhao 60s soft-cut vertical remake per P-20260926-11 (plain-language + series template) -> 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs002-v15-tmp
beats_path = os.path.join(ROOT, 'data', 'sources', 'bs002', 'voiceover-v15.beats.txt')
beats = io.open(beats_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（57 秒柔转场剪辑：凌晨三点一个人类老板查岗 AI 员工办公室、'
    '发现人数为零的全程实录——AI 公司 10 分钟自动唤醒心跳循环、19 项体检修自己排第一、闹钟过期自己批指令重建、'
    '三颗心脏管钱游戏进化周日 09:17、交接文档零条、把公司做成操作系统会都不用开。画面全部是真实工作电脑录屏素材——'
    '城市值守屏、AI 公司 OS 循环日志、评审台账文档，配锚点数字字卡；右上角全程有「BigStream | BS-002 EP.02」系列角标，'
    '左下有系统状态行和轻微扫描线质感；配音是轻度赛博机械感的机器叙述者，文案刚按「外行一眼懂」标准重写过白话释义。'
    '口播文案全文如下）：\n\n' + beats + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会看完这条 57 秒的视频吗？会点赞或转发吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话、听不懂的地方？有的话扣几分、指出原句？\n'
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
