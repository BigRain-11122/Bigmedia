# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20261005-DIGEST-v15 static digest card (non-registry seat,
# direct Ollama; v14 pattern R1095: UTF-8 stdin pipe + ANSI strip + braille strip).
# Async in-flight seat (Start-Process detached, 1500s window; backfill same-round if landed,
# else next round per R517->R518 precedent). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 015》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 015」；下面七行数字盘点：'
    u'「集团令批 2026-10-04（深夜 4 行 · 雷达双令）」'
    u'「不仅仅是游戏的，那些其他方面的都要去抓取，然后去学习调研。深入调研。」'
    u'（引号里是老板原话：老板说雷达扫描不能只盯着游戏，其他方面的也都要去抓取，'
    u'去学习调研、深入调研）'
    u'「雷达路由闭环 · 扫描七司业务域 · 深研 L1-L3」'
    u'「过目双通道 · 候选认领制 · 两率入周报」'
    u'「收益导向 · 可变现升权 · 四段闭环链」'
    u'「收益 3 型：省 token · 省工时 · 直接营收」；'
    u'图内底部来源行「基于硅基城市真实事件（集团令批台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'10 月 4 日深夜，老板在半小时内连发四道令：先把跨机分发链提速到秒级，'
    u'再把一个游戏项目整体打回重新验收，然后连下两道「雷达令」：第一道要求把原来只盯'
    u'GitHub 技术的收获雷达扩成全领域扫描——七家子公司业务域加通用技术域每窗必扫，'
    u'发现按 L1 判读/L2 映射/L3 深研三级分级，候选清单既给各公司循环过目、也周报给决策'
    u'委员会过目，各公司认领后转任务单，认领率加落地率进周报计量；第二道给雷达加收益'
    u'透镜——商业化、自动化、创新绩效优先，可变现的升权、纯玩具降权，'
    u'落地链从研究、接线、执行一直延长到收益四段闭环，每个契合件都必须写清楚预期收益'
    u'是省 token、省工时还是直接营收三型里的哪一型。全部数字可在集团台账溯源。'
    u'这是「城市盘点」系列第十五张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261005-DIGEST-v15 static card (cards.json + render output)'}
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
