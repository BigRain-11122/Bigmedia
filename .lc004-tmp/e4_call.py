# -*- coding: utf-8 -*-
# E4 audience reference call - LC-004 split-video edition (non-registry seat, direct Ollama;
# lc003-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# 60s vertical split-video (LC-004 Lu Haifeng, redundancy-expansion slot) -> 1500s window.
# Scoring dims = R223 audience dims. E4 must NOT see meta version info (blind-material rule).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
srt_path = os.path.join(HERE, 'subs.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在微信视频号里刷到竖屏短视频的普通观众，刷到了这条 60 秒的《城市图鉴 016·陆海峰》'
    '（竖屏 60 秒档案拆条：在一座全员讲数据、讲算法的城里，节目组找到了全城唯一保留慢班渡轮的'
    '船长。画面是一张档案卡，卡面上是这位船长的登记档案：弄堂派老船长，渡轮船长，江上摆渡人，'
    '自称三流数据道的活船老大；他爹是黄浦江轮渡船长，打小在码头长大；数据道再快，这条渡轮永远'
    '留着慢班；开航前绕船三圈，一步不少；一支旧铜哨是他爹传的，雾天一响，守夜灯灵十四号路灯必到；'
    '大雾夜全船人合唱，嘴上嫌吵，每回减速唱完才靠泊；船票恒价，只收一句多谢；正教徒弟高小满开船，'
    '手艺不传就沉江了。信条一行：船稳，人心才稳。全部基于城市真实居民档案改编；配音是轻度赛博'
    '机械感的机器叙述者，以城市系统日志自述视角讲述；画面带 AI 生成标识。口播全文如下）：\n\n'
    + transcript + '\n\n'
    '请回答三个问题，每题一段，直说不委婉：\n'
    '1) 你会看完这 60 秒吗？会点赞或转发给朋友吗？打几分（0-10）？为什么？\n'
    '2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    '3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b', 'material': srt_path}
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
