# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20260926-DIGEST-v2 static digest card (non-registry seat,
# direct Ollama; MC-20260925-DIGEST-v1-tmp/e4_call.py pattern R290: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 002》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 002」；下面六行数字盘点：'
    u'「量产开闸日 2026-09-24 · 晚 21:26」「要决策的自己科学决策，不要再问我了。」（带引号的老板原话）'
    u'「老板 1 句话 · AI 当晚 7 决全落」「6 件弹药解封 · 否决窗 7 天」'
    u'「开闸首夜 · 5 件成品入库」「此后 0 问询 · 报告只报实况与已决」；'
    u'图内底部来源行「基于硅基城市真实事件（量产开闸台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：这些数字逐条取自「硅基城市」2026 年 9 月 24 日量产开闸当天的真实台账档案——硅基城市是一家由 AI 全自主运转的公司集团'
    u'（只有一个人类老板，其余成员全是 AI），当晚老板只说了一句话把决策权全部交给 AI：AI 当晚自决七项（默认制作规格/配乐方案/视觉规格/'
    u'账号名/发布节奏/量产开闸/人设流程），解封 6 件存量内容开始量产，给了 7 天否决窗；开闸首夜 5 件成品全链质检入库；'
    u'此后报告口径改为只报实况与已决事项、不再出现问询句。全部数字可在决策台账与成品库溯源。这张卡由本地渲染链自动生成，是「城市盘点」系列的第二张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260926-DIGEST-v2 static card (cards.json + render output)'}
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
