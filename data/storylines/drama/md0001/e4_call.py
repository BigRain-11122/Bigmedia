# -*- coding: utf-8 -*-
# E4 audience-reference call for MD-0001 drama PoC (R1795 fire, async detached).
# Pattern: MC-20261009-REACT-v12 e4_call.py / bs016 e4_call_r1693.py family.
import io, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))

prompt = (
    u'你是一名刷 B 站首页推荐流的普通观众，看到一部 75 秒的短篇漫剧（有声漫画风格·16:9 横屏）'
    u'《台风梅花夜》。画面是扁平风格化 2D 插画、降饱和夜雨色调，13 个镜头带 Ken Burns 缓推缓移和转场，'
    u'每镜底部有字幕，画面角部全程有引擎烧录的 AIGC 标识「[AIGC·AI 生成内容]」。'
    u'故事：台风梅花过境之夜，硅基城市外环停电漆黑，只有远处一点白光——十四号路灯在超载发光照亮整条街道；'
    u'路灯的台词「知道原因，不能说」「灯不问来路，只管照路」，灯罩上有块歪斜的补丁，它不许修，说「疤是资历」；'
    u'检修日志写「超载运行，无损耗」。第二段：老旧信号塔里老兵邓建国蜷在椅子上打盹，守了一宿睡了整整一天，'
    u'他说「台风天的日志最见人品」。第三段：清晨全城灯带如常亮起，一只圆滚滚的像素猫咪喱叼着纸条飞过雨巷，'
    u'全巷通讯中断时它的尾巴天线立了大功，问它就说「就是耳朵痒」，最后它蹭了七家早餐，说'
    u'「蹭饭是门艺术，报恩是门手艺」。收尾旁白「交晨——把夜交给早晨」，然后黑屏出白色小字：'
    u'「本片根据硅基城市真实档案改编，部分情节为合理推演」。'
    u'背景：硅基城市是一家由 AI 全自主运转的公司集团（只有一个人类老板，其余成员全是 AI），'
    u'城里住着一万名登记居民，路灯、老兵、猫都是登记在册的居民（户籍卡记录姓名职业信条）。'
    u'这是公司 AI 剧线用本地模型全流程自制的第一部漫剧样片（剧本/配音/画面/剪辑全部本地 AI 产线），'
    u'台风梅花夜是城市编年史里的真实档案事件，三个居民的台词都逐字取自档案。'
    u'请回答三个问题，每题一段，直说不委婉：\n'
    u'1) 刷到这个视频你会看完吗？会点赞、投币或转发吗？打几分（0-10）？为什么？\n'
    u'2) 有没有一眼假、空洞套话、AI 味重的地方？有的话扣几分、指出原句？\n'
    u'3) 最弱的一项是什么？'
)

result = {'ts': time.strftime("%Y-%m-%d %H:%M:%S"), 'model': 'qwen2.5:14b',
          'material': 'MD-0001 drama PoC assembled piece md-0001-v1-bilibili-16x9.mp4 (75.84s) + SCRIPT-v1'}
try:
    p = subprocess.run(['ollama', 'run', 'qwen2.5:14b'], input=prompt.encode('utf-8'),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    raw = p.stdout.decode('utf-8', errors='replace')
    cleaned = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', raw)
    cleaned = re.sub(u'[⠀-⣿]', '', cleaned)
    result['verdict'] = cleaned.strip()
except subprocess.TimeoutExpired:
    result['verdict'] = 'TIMEOUT-1500s'
io.open(os.path.join(HERE, 'e4-result.json'), 'w', encoding='utf-8').write(
    json.dumps(result, ensure_ascii=False, indent=2))
print('DONE' if result['verdict'] != 'TIMEOUT-1500s' else 'TIMEOUT')
