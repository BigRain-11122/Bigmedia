# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20260928-DIGEST-v8 static digest card (non-registry seat,
# direct Ollama; v7 pattern R517: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 008》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 008」；下面七行数字盘点：'
    u'「决策委员会成立 2026-09-28 节首立」'
    u'「平票重议再平升 CEO」（引号行是集团新立的决策委员会章程原文：两轮投票平票时，最终交老板裁决）'
    u'「7 席记名投票 · 普通过 ≥4/7 · 重大件 ≥5/7」「C-01 定价批：4 席已收 · 议题③同向 A」'
    u'「C-02 瘦身案补登：规则 65 vs 预算 20」「双案意见窗 48 小时 · 风控席必议」'
    u'「CEO 列席 · 翻案权与终审权不变」；'
    u'图内底部来源行「基于硅基城市真实事件（决策委员会台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'9 月 28 日凌晨集团的 AI 决策轮在台账里首次开出「委员会节」：城市最高决策委员会成立，7 个席位记名投票，'
    u'普通事项 4/7 通过、重大事项要 5/7，平票就再议一轮，再平就交给老板裁决；老板保留列席、翻案和终审权。'
    u'委员会头两件案子同时在途：C-01 是商业化定价批（4 席意见已收，对「29.9 入门档还是维持 49.9 起」四个已收席位都倾向 A）；'
    u'C-02 是机构与规则瘦身案（集团自查出约 65 条规则，超过了自家定的「规则预算不超过 20 条」的红线 3 倍，要裁并归层），'
    u'两案意见窗都是 48 小时，风控席位每次都必须唱反调（魔鬼代言人），过会前任何公司都不许执行。'
    u'全部数字可在集团台账溯源。这张卡由本地渲染链自动生成，是「城市盘点」系列的第八张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260928-DIGEST-v8 static card (cards.json + render output)'}
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
