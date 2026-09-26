# -*- coding: utf-8 -*-
# E4 audience reference call - MC-20260926-DIGEST-v4 static digest card (non-registry seat,
# direct Ollama; v3 pattern R381: UTF-8 stdin pipe + ANSI strip + braille strip).
# Same-round E4 for hit-chain v1.0 series production piece (no untested face left). Non-blocking seat.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷到公众号图文/信息流的普通读者，看到下面这张静态盘点卡《城市盘点 004》'
    u'（1080×1080 方图·黑底；顶部标题「城市盘点 004」；下面七行数字盘点：'
    u'「技能动员日 2026-09-26 · 凌晨 00:35」'
    u'「ceo 命令，全部去找适合业务的 skills」（老板原话第一行）'
    u'「并使用，提升生产力」（老板原话第二行）'
    u'「盘点 3 件在役 · 自建 2 件入产线」「建装 5 步 · 校验安装双 PASS」'
    u'「技能 1=四形态全链 · 技能 2=机检三门」「快速件窗 48 小时 · 计数 09-27 00:35」；'
    u'图内底部来源行「基于硅基城市真实事件（技能动员令台账档案）」；'
    u'角部有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'背景：这些数字逐条取自「硅基城市」2026 年 9 月 26 日技能动员令的真实台账档案——硅基城市是一家由 AI 全自主运转的公司集团'
    u'（只有一个人类老板，其余成员全是 AI），当天凌晨 00:35 老板只下了一句话命令：让全部子公司去找适合业务的技能（skills）并用起来提升生产力，'
    u'限时 48 小时交清单回执。BigStream 这家 AI 媒体公司当天盘点出 3 件会话内置在役技能，又用官方技能创建器按五步流程自建了 2 件生产技能'
    u'（一件固化四形态图文卡全链工艺、一件固化机检三门与验图执法），校验安装双双通过，技能登记进公司 README 当轮交付。全部数字可在集团进化台账与公司能力册里溯源。'
    u'这张卡由本地渲染链自动生成，是「城市盘点」系列的第四张。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这张卡你会停下来看吗？会保存或转发给朋友吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime('%Y-%m-%d %H:%M:%S'), 'model': 'qwen2.5:14b',
          'material': 'MC-20260926-DIGEST-v4 static card (cards.json + render output)'}
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
