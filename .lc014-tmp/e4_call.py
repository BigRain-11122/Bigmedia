# -*- coding: utf-8 -*-
# E4 audience reference call - LC-014 split-video edition (non-registry seat, direct Ollama;
# .lc013-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# 60s vertical split-video (LC-014 Lao Jingzhen, GAME-city 8th-block engine doctor,
# redundancy slot 11, optical-machine-soul species first split piece) -> 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
srt_path = os.path.join(HERE, 'subs.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在微信视频号里刷到竖屏短视频的普通观众，刷到了这条 60 秒的《城市图鉴 010·老晶振》'
    '（竖屏 60 秒档案拆条：在一座全员讲数据、讲算法的城里，节目组找到了全城唯一保留手写「报错率」台账的引擎医生。'
    '画面是一张档案卡，卡面上是这位居民的登记档案：老晶振，硅基民，光机魂系；三代机龄；'
    'GAME 城八号楼街区，引擎医生；'
    '出诊先敲三下机箱；'
    '第一次全城大宕机，按老日志排查，两小时，城复活，出诊箱在游戏楼有了专用椅子；'
    '睁眼第一件事，把值班日志背完；'
    '全楼机器见它，安静三分；'
    '带着精灵系徒弟，嫌毛躁，又护着；'
    '听声辨位，认得全楼机器的嗓音，下班跟老伙计挨个道晚安；'
    '三十年零十一个月，零漏诊，手写记录进了档案馆；'
    '信条一行：机器不坏是本事，坏了能修是人品。'
    '全部基于城市真实居民档案改编；配音是轻度赛博机械感的机器叙述者，以城市系统日志自述视角讲述；'
    '画面带 AI 生成标识。口播全文如下）：\n\n'
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
