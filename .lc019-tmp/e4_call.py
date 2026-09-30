# -*- coding: utf-8 -*-
# E4 audience reference call - LC-019 split-video edition (non-registry seat, direct Ollama;
# R742 LC-018 pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# 60s vertical split-video (LC-019 Zhou Haoyu, QUANT-city strategy researcher, redundancy
# slot 16, 10th character-chain dual-end cross-proof closing half; CENSUS-v5 F-024 card -> 2nd
# carrier, awe-discipline theme series first piece).
import io, json, os, re, subprocess, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
srt_path = os.path.join(ROOT, '.lc019-tmp', 'subs.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在微信视频号里刷到竖屏短视频的普通观众，刷到了这条 60 秒的《城市图鉴 019·周浩宇》'
    '（竖屏 60 秒档案拆条：在一座全员讲数据、讲算法的城里，节目组找到了全城唯一给被毙掉的策略写讣告的研究员。'
    '画面是一张档案卡，卡面上是这位居民的登记档案：周浩宇，碳基市民，二十八岁；'
    'QUANT 城扭塔，策略研究员；'
    '盯盘百毒不侵，收盘泡面坨了；'
    '第一次上线，被上了一课，敬畏俩字纹在工位上；'
    '川渝腔：要得，巴适，啥子，一紧张尾音出卖他；'
    '问题钻到底，饭都能忘，说出口的字比章硬；'
    '每晚给爹娘报平安；他爹说，钱的事最讲天理，策略就是把道理验一万遍；'
    '食堂徐根福总多打一勺：长身体，二十八了；风控官陈雅雯，他最怕也最服；'
    '信条一行：回撤教人做人，行情教人谦虚。'
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
    cleaned = re.sub(u'[\u2800-\u28ff]', '', cleaned)  # braille spinner range (R189 lesson)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(ROOT, '.c3-tmp', 'e4-result-r746.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
