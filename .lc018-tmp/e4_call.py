# -*- coding: utf-8 -*-
# E4 audience reference call - LC-018 split-video edition (non-registry seat, direct Ollama;
# R738 LC-017 pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# 60s vertical split-video (LC-018 Chen Yawen, QUANT-city risk-control officer, redundancy
# slot 15, 10th character-chain dual-end cross-proof piece; CENSUS-v6 F-025 card -> 2nd
# carrier, rule-governance theme series first piece).
import io, json, os, re, subprocess, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
srt_path = os.path.join(ROOT, '.lc018-tmp', 'subs.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在微信视频号里刷到竖屏短视频的普通观众，刷到了这条 60 秒的《城市图鉴 018·陈雅雯》'
    '（竖屏 60 秒档案拆条：在一座全员讲数据、讲算法的城里，节目组找到了全城唯一在拦截日志里给每单写「一句话理由」的风控官。'
    '画面是一张档案卡，卡面上是这位居民的登记档案：陈雅雯，碳基市民，四十二岁；'
    'QUANT 城风控高地，风控官；'
    '红灯亮起，永远第一个到岗；绿灯常亮，反而睡不着；'
    '那年在风控高地拦下自己师父的一单，挨了骂，第二天师父提着酒来道歉，从此她认准了规矩面前无师徒；'
    '口头禅干脆利落：过、不过、理由三条；从不说应该没问题，只有实测没问题；'
    '性格是把关、稳、防微杜渐：天塌下来先把手里这步做完，听见第一声异响就开始排查；'
    '胸前别着一枚哑光徽章，是女儿画的红绿灯，她给做成了金属的；带徒弟了，第一课永远是先学会说不过；'
    '她说这行最大的奖赏没人看得见：没发生的事，就是她全部的功劳；'
    '量化策略研究员周浩宇说，她是他最怕又最服的人；'
    '信条一行：红灯是为所有人亮的，包括我。'
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
io.open(os.path.join(ROOT, '.c3-tmp', 'e4-result-r742.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
