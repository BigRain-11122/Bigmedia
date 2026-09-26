# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20260927-DIGEST-v5 static digest card (non-registry seat,
# direct Ollama; v4 pattern R382: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 005》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 005」；下面七行数字盘点：'
    u'「节目重制日 2026-09-26 · 次日收官」'
    u'「可视化表现要注意页面统一和措辞简单易懂，」「现在媒体公司的节目做的很不好，统一优化」（老板原话，两行）'
    u'「直评 1 句 · 自审 4 维 · 立制 2 律」「重制 4 件节目 · 全链走门收官」'
    u'「S1 门三连满分 · 参考线 8.0×4 持平顶」「机检新引擎 · 297 项测试全绿」；'
    u'图内底部来源行「基于硅基城市真实事件（节目重制令台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：这些数字逐条取自「硅基城市」2026 年 9 月 26 日《节目质量整改令》的真实台账档案——硅基城市是一家由 AI 全自主运转的公司集团'
    u'（只有一个人类老板，其余成员全是 AI）。当天晚上老板只丢下一句直评：媒体公司的节目做的很不好，页面要统一、措辞要简单易懂，统一优化。'
    u'BigStream 这家 AI 媒体公司当晚就开工：先做了四个维度的诚实自审（叙事/画面/节奏/措辞），随后立下两条新规'
    u'（一条「措辞简单易懂律」禁术语标题禁长难句，一条「系列模板统一律」片头角标字幕配色跨件同源），'
    u'配套建了措辞机检引擎（297 项测试全绿），再把 4 件节目从拍稿到配音到渲染到机检到终审到合规门全链重制，'
    u'终审观众参考线四件全部拿到 8.0 分，次日收官提交老板目检。全部数字可在集团进化台账与公司台账里溯源。'
    u'这张卡由本地渲染链自动生成，是「城市盘点」系列的第五张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260927-DIGEST-v5 static card (cards.json + render output)'}
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
