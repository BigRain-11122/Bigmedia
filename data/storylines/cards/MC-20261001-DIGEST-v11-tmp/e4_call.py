# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20261001-DIGEST-v11 static digest card (non-registry seat,
# direct Ollama; v10 pattern R682: UTF-8 stdin pipe + ANSI strip + braille strip).
# Async in-flight seat (Start-Process detached, 1500s window; backfill next round per
# R517->R518 / R577->R578 / R631->R632 / R682 precedent). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 011》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 011」；下面七行数字盘点：'
    u'「产品优先令 2026-09-29 午后落账（CEO 直令）」'
    u'「产出落地很少，品质也很差，请从源头梳理和解决这个问题，提高效率，过程能看到，结果早点出」'
    u'（引号里是老板原话：批评大家一直在写规则写流程写文档，真正落地产出的东西很少、品质也差，'
    u'要求从源头解决，提高效率，过程要能看到，结果要早点出）'
    u'「审计：8 仓 7 天 10,524 commit · 本司文档簿记 46%」'
    u'「立制：实物 2 分 · 改动 1 分 · 纯记账 0 分」'
    u'「回应：成品 25 件 40 小时入库 · F-057→F-081」'
    u'「24 小时全 0 分=空转判负 · 本卡=令后第 26 件」；'
    u'图内底部来源行「基于硅基城市真实事件（产品优先令台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'9 月 29 日下午老板在集团台账里直评：产出落地很少，品质也很差，要求从源头梳理解决。'
    u'集团审计读数是 8 个仓 7 天共 10,524 个 commit，其中做这张卡的 BigStream 公司文档簿记类占 46%。'
    u'老板的话当天被写进各公司循环的任务书最高优先级块：每轮先问「这轮结束时老板能看到什么新实物」，'
    u'实物记 2 分、文件改动 1 分、纯记账 0 分，纯记账每轮最多 5 处，连续 24 小时全是 0 分就判空转。'
    u'立制之后这家公司 40 小时里入库了 25 件成品（编号 F-057 到 F-081），这张卡是命令之后第 26 件。'
    u'全部数字可在集团台账与本司成品库台账溯源。这是「城市盘点」系列第十一张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261001-DIGEST-v11 static card (cards.json + render output)'}
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
