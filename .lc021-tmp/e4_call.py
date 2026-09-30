# -*- coding: utf-8 -*-
# E4 audience reference call - LC-021 split-video edition (non-registry seat, direct Ollama;
# R742 LC-018 / R743 LC-019 pattern: UTF-8 stdin pipe + ANSI strip + braille strip).
# 60s vertical split-video (LC-021 Shen Peilan, morning-exercise captain, redundancy slot 17,
# CENSUS anchor-pool 20-card full-coverage finale piece; CENSUS-v3 F-022 card).
import io, json, os, re, subprocess, time

ROOT = r"C:\Users\sjs20\Desktop\FluxGroup\media\BigStream"
srt_path = os.path.join(ROOT, '.lc021-tmp', 'subs.srt')
lines = io.open(srt_path, encoding='utf-8').read().splitlines()
text_lines = [ln for ln in lines if ln.strip() and '-->' not in ln and not ln.strip().isdigit()]
transcript = '\n'.join(text_lines)

prompt = (
    '你是一名在微信视频号里刷到竖屏短视频的普通观众，刷到了这条 60 秒的《城市图鉴 003·沈佩兰》'
    '（竖屏 60 秒档案拆条：在一座全员讲数据、讲算法的城里，节目组找到了全城唯一能靠光带节奏认出每个队员心气的人。'
    '画面是一张档案卡，卡面上是这位居民的登记档案：沈佩兰，碳基市民，弄堂派，女，五十八岁；'
    '北外滩脑环广场街区，晨操领队——广场舞的光带版；'
    '带队规矩：比太阳起得早，光带音响永远只开三分贝，说是吵醒上夜班的缺德；'
    '那年舞队散伙又重组，她挨家挨户把老姐妹一个个请回来，从此队伍散了人心不能散；'
    '队里从七个人带到四十三个人，年轻教练想接棒，她嘴上不说心里已经点头；'
    '口令简短干脆：对齐——起步——；一句侬说啥物事，比红脉冲还管用；'
    '玫红运动服是她挑的降饱和色，说亮的让给塔顶白光；包里永远有备用光带和三块糖，低血糖的队员比坏设备常见；'
    '带队十九年，看明白一件事：晨操跳的不是舞，是大家都还在；光带音响一响，老街坊一个个从楼里出来，她在队首回头数人头；'
    '半个队员都喊她沈老师，老对头兼老姐妹一年吵三回回回和好；'
    '信条一行：队形不能乱，人心更不能散。'
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
io.open(os.path.join(ROOT, '.c3-tmp', 'e4-result-r756.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
