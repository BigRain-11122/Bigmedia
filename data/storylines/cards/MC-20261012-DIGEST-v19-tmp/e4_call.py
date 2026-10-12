# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20261012-DIGEST-v19 static digest card (non-registry seat,
# direct Ollama; v18 pattern R2001: UTF-8 stdin pipe + ANSI strip + braille strip).
# Staged as the fire_consume launcher (tech#112) for the v19 GPU tail (F-182):
# fire_consume.py dispatches THIS file the moment the card says fire.
# Material source: e4-material.md (R2050 preload, deck verbatim parity-checked).
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 019》'
    u'（1080×1080 方图·黑底；左上角小字「[AIGC·AI 生成内容]」；顶部大标题「城市盘点 019」）。'
    u'图上写着七行盘点正文：'
    u'「顶层梳理日（10-12 · 两日 22 行令批）」；'
    u'「导演拍板，不要都来问我，我看到问题自然会说，没说你们就自己推进。」——这行是老板原话引文；'
    u'「顶层梳理案同窗收口 · 票档 7/7 · 判据 6 条」；'
    u'「四阶段推进 · 盘点 瘦身 治理 常态」；'
    u'「法熵守恒 · 新增 ≤3 节 · 退役并档 ≥3 处」；'
    u'「三席定律成形 · 道具 调色 服装 三签字闸」。'
    u'图内底部声明行「基于硅基城市真实事件（顶层梳理日令批台账档案）」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'「城市盘点」系列是集团旗下媒体公司出品的城市档案盘点图——把集团真实发生的大事，'
    u'用数字盘点的方式做成一张方图档案，所以底部声明行写明「基于硅基城市真实事件」。'
    u'这张卡盘点的是 10 月 12 日的「顶层梳理日」：老板说业务越来越多越来越复杂，'
    u'点名决策委员会从顶层开始梳理规则、制度、流程和工作流——执行案当天就收口通过，票档 7/7，'
    u'预注册 6 条验收判据，分四阶段推进（盘点、瘦身、治理、常态）；同一波令批里，'
    u'集团的音乐 MV 产线立起「三席定律」：道具、调色、服装三道签字闸；导演拍板权同日生效——'
    u'老板只留一句「导演拍板，不要都来问我，我看到问题自然会说，没说你们就自己推进」。'
    u'请回答三个问题，每题一段，直说不绕弯：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空话套话的地方？有的话扣几分、指出原文？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261012-DIGEST-v19 static card (cards.json + render output + e4-material.md)'}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[\u2800-\u28ff]', '', cleaned)  # braille spinner range (R189 U+2800 lesson)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding="utf-8").write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
