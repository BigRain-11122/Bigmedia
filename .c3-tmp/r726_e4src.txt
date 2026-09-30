# -*- coding: utf-8 -*-
# E4 audience reference call - LC-013 split-video edition (non-registry seat, direct Ollama;
# .lc012-tmp/e4_call.py pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# 60s vertical split-video (LC-013 Su Zihan, GAME city level architect,
# redundancy slot 10, sixth character-chain multi-directional cross-proof piece) -> 1500s window.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
srt_path = os.path.join(HERE, 'subs.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在微信视频号里刷到竖屏短视频的普通观众，刷到了这条 60 秒的《城市图鉴 011·苏梓涵》'
    '（竖屏 60 秒档案拆条：在一座全员讲数据、讲算法的城里，节目组找到了全城唯一给夜班人员留专属彩蛋的关卡建筑师。'
    '画面是一张档案卡，卡面上是这位居民的登记档案：苏梓涵，碳基市民，二十四岁；'
    'GAME 城游戏楼街区，关卡建筑师；'
    '盖完就拆，拆完再盖；'
    '第一个署名关卡上线那晚，她蹲在城门口听了一夜玩家议论，第二天把最狠的差评打印贴在工位；'
    '城生城长，童年在测试关卡里过；'
    '脑子里永远有三十个方案在排队；'
    '下班必去老城门，给守门人带一杯热的；'
    '好关卡像好弄堂，走一遍就舍不得搬走；'
    '守门人、巡夜员、灯塔守望都收到过，谁也没找到全部，他们管这叫梓涵的深夜惊喜；'
    '信条一行：每个转角都该藏一个惊喜。'
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
