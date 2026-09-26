# E4 audience reference call - F-004 v15 remake edition (non-registry seat, direct Ollama;
# .bs003-v15-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# Shipinhao 60s soft-cut vertical remake per P-20260926-11 (plain-language + series template) -> 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root = parent of .bs004-v15-tmp
beats_path = os.path.join(ROOT, 'data', 'sources', 'bs004', 'voiceover-v15.beats.txt')
beats = io.open(beats_path, encoding='utf-8').read()

prompt = (
    '你是一名刷微信视频号的普通观众，刷到下面这条竖屏 9:16 短视频（59 秒柔转场剪辑：讲一家 AI 公司怎么用数据管钱——'
    '他们给自己的钱建了一道门禁：历史数据重算之后，最好的年化 3.8%，432 组全灭、0 组过线，门还活着；'
    '然后拿 20 条纯随机假策略同场跑对照，随机策略都能做到稳定打分 1.4；'
    '所以刷屏的「神策略」日志判定：不敢跟随机比；五道门=老办法全灭、海选、出厂、成本加倍、组合软化；'
    '注册的时候自带历史成绩单，强到哪、死在哪都在里面；'
    '五句清单：先定什么算假、随机同场比、试验记账、成本加倍照妖镜、全灭开酒；'
    '最后声明：不构成投资建议，实录在公众号，转给想学用数据管钱的人。'
    '画面全部是真实工作电脑录屏素材——AI 公司 OS 循环日志、评审台账文档、像素小镇驾驶舱、剪辑网格，配字卡；'
    '右上角全程有「BigStream | BS-004 EP.04」系列角标，左下有系统状态行和轻微扫描线质感；'
    '配音是轻度赛博机械感的机器叙述者，文案刚按「外行一眼懂」标准重写过白话释义。'
    '口播文案全文如下）：\n\n' + beats + '\n\n请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会看完这条 59 秒的视频吗？会点赞或转发吗？打几分（0-10）？为什么？\n'
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
