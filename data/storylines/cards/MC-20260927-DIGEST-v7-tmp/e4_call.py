# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20260927-DIGEST-v7 static digest card (non-registry seat,
# direct Ollama; v6 pattern R461: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 007》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 007」；下面七行数字盘点：'
    u'「商业化定价日 2026-09-27 落账」'
    u'「合理的付费点，还有包装价格」（引号行是这家公司唯一人类老板当天早晨下的一句原话）'
    u'「一句令 · 当日 19 付费点全对表」「定价四层 · 29.9 与 49.9 二选一待裁」'
    u'「居民档案订阅 9.9 元/月设计值」「外部锚 31 源 · 陪伴常态带 20-39 元」'
    u'「过会件当日落档 · 7 席 48 小时记票」；'
    u'图内底部来源行「基于硅基城市真实事件（商业化定价令台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'9 月 27 日早晨老板一句话下令「商业化公司，全面了解现在的业务架构，挖掘与现实之间。合理的付费点，还有包装价格什么之类的。在合法的框架范围内。」'
    u'——当天 AI 集团完成：19 个付费点矩阵（在册 12+新挖 7）、四层价格架构（2-9.9 元钩子/19.9 元主力/29.9-99 元订阅/199-19,800 元身份与 B 端）、'
    u'对照 31 个外部真实市场源校准（AI 陪伴类订阅市场常态带 20-39 元/月）、当日把重大定价变更提交集团决策委员会过会'
    u'（7 席 48 小时意见窗、普通事项过线 4/7、过会前各公司零执行）；其中「29.9 元入门订阅档 vs 维持 49.9 元起」二选一待老板裁；'
    u'「居民成长档案订阅 9.9 元/月」是设计值不是上架价。全部数字可在集团台账溯源。这张卡由本地渲染链自动生成，是「城市盘点」系列的第七张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260927-DIGEST-v7 static card (cards.json + render output)'}
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
