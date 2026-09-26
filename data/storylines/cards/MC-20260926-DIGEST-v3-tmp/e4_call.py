# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20260926-DIGEST-v3 static digest card (non-registry seat,
# direct Ollama; v2 pattern R380: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 003》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 003」；下面七行数字盘点：'
    u'「三线扩展日 2026-09-25 · 晨 08:50」'
    u'「创建有声小说，网文，漫画等一系列条线，主打硅基城市里面发生的一切，你们先调研，然后开始」（带引号的老板原话，跨三行）'
    u'「老板 1 句话 · 当天 3 条线立制开工」「素材：万人库 · 14 派系 · 台词池 1200+」'
    u'「首章《立国日》约 1100 字 · 漫画首话四格」；'
    u'图内底部来源行「基于硅基城市真实事件（三线扩展令台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：这些数字逐条取自「硅基城市」2026 年 9 月 25 日三线扩展令的真实台账档案——硅基城市是一家由 AI 全自主运转的公司集团'
    u'（只有一个人类老板，其余成员全是 AI），当天早上 08:50 老板只说了一句话，要求创建有声小说、网文、漫画等一系列内容条线，'
    u'题材主打硅基城市里发生的一切，并要求先调研再开工；AI 当天上午就交出调研盘点、立了新线章程、写完约 1100 字的网文第一章《立国日》，'
    u'还出了四格漫画样稿；素材库里有万人居民档案、14 个派系、1200 多条台词。全部数字可在令件与调研件里溯源。'
    u'这张卡由本地渲染链自动生成，是「城市盘点」系列的第三张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260926-DIGEST-v3 static card (cards.json + render output)'}
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
