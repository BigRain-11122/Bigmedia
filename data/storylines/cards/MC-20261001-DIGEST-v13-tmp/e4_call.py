# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20261001-DIGEST-v13 static digest card (non-registry seat,
# direct Ollama; v12 pattern R871: UTF-8 stdin pipe + ANSI strip + braille strip).
# Async in-flight seat (Start-Process detached, 1500s window; backfill same-round if landed,
# else next round per R517->R518 / R870->R871 precedent). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 013》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 013」；下面七行数字盘点：'
    u'「集团治理日 2026-10-01（CEO 一日三令 · 同窗收口）」'
    u'「立了一大堆规则和机制，产出却很少，委员会好好治理」'
    u'（引号里是老板原话：公司立了一大堆规则和机制，实际产出却很少，老板让委员会好好治理）'
    u'「三案：信息同步 · 规则通胀 · 闲置根治（表决 7/7）」'
    u'「单日批 11 行 · 治理 6+5+4 条同日生效」'
    u'「规则面 70% vs 标杆 6% · 规则存量 321 件 md」'
    u'「47 单补录清偿 · 回访 10-08 · 否决窗一句话可翻」；'
    u'图内底部来源行「基于硅基城市真实事件（集团治理批台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'10 月 1 日老板一天发了三道治理令：机队之间信息同步不及时、规则立了一大堆产出却很少、'
    u'机器闲置反复发生，让委员会去审查然后治理。委员会当天收口三案，记名表决全部 7/7 通过：'
    u'信息同步治理六条、规则通胀治理五条（给规则立规矩：新规则每周每仓最多 2 件、'
    u'单条条款最多 120 字、产出计分制——能跑能看的实物才算分）、闲置根治四条'
    u'（含常设备货池已建 11 单）。证据显示总部仓近 7 天提交里规则治理面占 70%，'
    u'标杆子公司只有 6%；规则文件存量 321 件。另有 47 单会话直射任务没登台账，'
    u'自查自首后当天补录清偿。全部判据 10 月 8 日回访检查，否决窗内老板一句话可翻案。'
    u'全部数字可在集团决策台账溯源。这是「城市盘点」系列第十三张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261001-DIGEST-v13 static card (cards.json + render output)'}
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
