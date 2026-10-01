# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20261001-DIGEST-v12 static digest card (non-registry seat,
# direct Ollama; v11 pattern R870: UTF-8 stdin pipe + ANSI strip + braille strip).
# Async in-flight seat (Start-Process detached, 1500s window; backfill same-round if landed,
# else next round per R517->R518 / R631->R632 / R682 precedent). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 012》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 012」；下面七行数字盘点：'
    u'「集团外审日 2026-09-30（CEO 直令 · 12 轮外审）」'
    u'「作为外部专家逐个看业务/子公司/集团，输入改进清单，让他们科学决策落实」'
    u'（引号里是老板原话：让 AI 充当外部专家，把每个业务/子公司/集团挨个审一遍，'
    u'开出改进清单，让他们科学决策落实）'
    u'「单日批 40 决（编号至 D-20260930-41）」'
    u'「改进清单 XL-1→21 · 修复单 RW-1→7」'
    u'「方法论 M1→M7 · 审计探针 Q1→Q9（P0 命中）」'
    u'「外审 5 次自我勘正 · 六律入章程 · 窗至 10-07」；'
    u'图内底部来源行「基于硅基城市真实事件（集团外审决策批台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI）。'
    u'9 月 30 日老板下令：让 AI 以外部专家身份把集团每个子公司挨个体检，输入改进清单，'
    u'科学决策落实。外审当天跑了 12 轮，单日落了 40 条决策（编号到 D-41，有一号空缺），'
    u'包括全域改进清单 XL-1 到 21 条、某子公司可信度修复单 RW-1 到 7 条、'
    u'量化方法论增强七件 M1 到 M7、审计探针 Q1 到 Q9（首跑命中 4 项，其中 1 项 P0 级缺陷）。'
    u'外审自己也在过程中错了 5 次，每次当场自我勘正，并把六条方法律写进了集团章程。'
    u'这批决策都带 7 天否决窗，到 10 月 7 日，老板一句话可翻案。'
    u'全部数字可在集团决策台账溯源。这是「城市盘点」系列第十二张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20261001-DIGEST-v12 static card (cards.json + render output)'}
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
